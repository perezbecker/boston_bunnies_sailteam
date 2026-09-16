"""Slice Lahar v2 with official MK4S presets and verify the resulting projects and toolpaths."""

import argparse
import configparser
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


PRESETS = {
    "print": "0.15mm STRUCTURAL @MK4S 0.4",
    "filament": "Generic PLA @MK4S HF0.4",
    "printer": "Original Prusa MK4S HF0.4 nozzle",
}
JOBS = ("Steering", "Body")
NUMBER = re.compile(r"([XYZEF])([-+]?(?:\d*\.\d+|\d+\.?\d*))")


def resolve_profile(bundle, kind, name, ancestors=()):
    section = f"{kind}:{name}"
    if section in ancestors:
        raise ValueError(f"Cyclic preset inheritance: {section}")
    values = dict(bundle[section])
    result = {}
    for parent in values.pop("inherits", "").split(";"):
        if parent.strip():
            result.update(resolve_profile(bundle, kind, parent.strip(), (*ancestors, section)))
    result.update(values)
    for key in ("alias", "renamed_from"):
        result.pop(key, None)
    return result


def slicer_path(path, executable):
    path = path.resolve()
    if executable.suffix.lower() == ".exe" and str(path).startswith("/mnt/"):
        return subprocess.check_output(["wslpath", "-w", str(path)], text=True).strip()
    return str(path)


def run_slicer(executable, arguments, log_path):
    result = subprocess.run([str(executable), *arguments], capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    output = result.stdout + result.stderr
    log_path.write_text(output, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Slicer failed ({result.returncode}): {output}")
    warnings = [line for line in output.splitlines()
                if re.search(r"warning|error|outside|floating bridge|empty layer", line, re.IGNORECASE)]
    if warnings:
        raise RuntimeError("Slicing needs review: " + "\n".join(warnings))


def resolved_configuration(text):
    config = text.partition("; prusaslicer_config = begin\n")[2]
    config, marker, _ = config.partition("; prusaslicer_config = end")
    if not marker:
        raise ValueError("Missing resolved slicer configuration")
    values = {}
    for line in config.splitlines():
        key, separator, value = line.removeprefix("; ").partition(" = ")
        if separator:
            values[key] = value
    return config, values


def validate_gcode(path, job):
    text = path.read_text(encoding="utf-8")
    config_text, config = resolved_configuration(text)
    required = {"printer_model": "MK4S", "bed_shape": "0x0,250x0,250x210,0x210",
                "nozzle_diameter": "0.4", "filament_type": "PLA",
                "layer_height": "0.15", "perimeters": "4", "fill_density": "100%",
                "top_solid_layers": "12" if job == "Body" else "8",
                "bottom_solid_layers": "12", "arc_fitting": "disabled"}
    for key, value in required.items():
        if config.get(key) != value:
            raise ValueError(f"{path.name}: {key}={config.get(key)!r}, expected {value!r}")
    if not re.search(r'M862\.3 P\s*"MK4S"', text) or "M862.1" not in text:
        raise ValueError("Missing MK4S printer/nozzle compatibility checks")
    positions = dict.fromkeys("XYZE", 0.0)
    relative_extrusion = False
    relative_position = False
    printing = False
    path_type = ""
    count = 0
    support_count = 0
    minima = dict.fromkeys("XYZ", float("inf"))
    maxima = dict.fromkeys("XYZ", -float("inf"))
    digest = hashlib.sha256()
    for raw in text.splitlines():
        if raw == ";LAYER_CHANGE":
            printing = True
        if raw.startswith(";TYPE:"):
            path_type = raw[6:]
        command = raw.partition(";")[0].strip()
        if not command:
            continue
        opcode = command.split()[0]
        values = {key: float(value) for key, value in NUMBER.findall(command)}
        if opcode == "M83":
            relative_extrusion = True
        elif opcode == "M82":
            relative_extrusion = False
        elif opcode == "G90":
            relative_position = False
        elif opcode == "G91":
            relative_position = True
        elif opcode == "G92":
            positions.update({key: value for key, value in values.items() if key in positions})
        elif opcode in ("G2", "G3"):
            raise ValueError("Arc found despite disabled arc fitting")
        elif opcode in ("G0", "G1"):
            previous = positions.copy()
            for key in "XYZ":
                if key in values:
                    positions[key] = values[key] + (previous[key] if relative_position else 0)
            extrusion = values.get("E", 0) if relative_extrusion else values.get("E", previous["E"]) - previous["E"]
            positions["E"] = previous["E"] + extrusion
            if printing and extrusion > 0 and ("X" in values or "Y" in values):
                for point in (previous, positions):
                    for key, limit in zip("XYZ", (250, 210, 220)):
                        if not -0.01 <= point[key] <= limit + 0.01:
                            raise ValueError(f"Extrusion outside MK4S build volume: {command}")
                        minima[key] = min(minima[key], point[key])
                        maxima[key] = max(maxima[key], point[key])
                count += 1
                support_count += "Support" in path_type
                digest.update((command + "\n").encode("ascii"))
    if count < 100:
        raise ValueError("Missing or empty printed toolpaths")
    if (job == "Steering") != (support_count > 0):
        raise ValueError(f"Unexpected support paths for {job}: {support_count}")
    mass = re.search(r"^; filament used \[g\] = ([\d.]+)", text, re.MULTILINE)
    time = re.search(r"^; estimated printing time \(normal mode\) = (.+)$", text, re.MULTILINE)
    if mass is None or time is None:
        raise ValueError("Missing slicer mass/time estimates")
    return config_text, {
        "file": path.name, "estimated_time": time.group(1), "filament_including_waste_g": float(mass.group(1)),
        "extruding_moves": count, "support_moves": support_count,
        "extrusion_min_mm": minima, "extrusion_max_mm": maxima,
        "toolpath_sha256": digest.hexdigest(), "gcode_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "printer_preset": config["printer_settings_id"],
        "nozzle_temperature_c": config["temperature"], "first_layer_temperature_c": config["first_layer_temperature"],
        "bed_temperature_c": config["bed_temperature"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slicer", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--amf-dir", type=Path, required=True)
    parser.add_argument("--jobs", nargs="+", choices=JOBS, default=JOBS)
    parser.add_argument("--roundtrip", action="store_true")
    args = parser.parse_args()
    bundle = configparser.ConfigParser(interpolation=None, strict=False)
    bundle.read(args.profiles, encoding="utf-8-sig")
    config = {}
    for kind, name in PRESETS.items():
        config.update(resolve_profile(bundle, kind, name))
        config[f"{kind}_settings_id"] = name
    config.update({
        "binary_gcode": "0", "arc_fitting": "disabled", "thumbnails": "",
        "layer_height": "0.15", "first_layer_height": "0.2", "perimeters": "4",
        "top_solid_layers": "8", "bottom_solid_layers": "12",
        "top_solid_min_thickness": "0", "bottom_solid_min_thickness": "0",
        "fill_density": "100%", "fill_pattern": "rectilinear", "brim_width": "3", "brim_type": "outer_only",
        "first_layer_speed": "20", "perimeter_speed": "40", "external_perimeter_speed": "25",
        "infill_speed": "60", "solid_infill_speed": "50", "top_solid_infill_speed": "30", "bridge_speed": "20",
        "external_perimeter_extrusion_width": "0.45", "perimeter_extrusion_width": "0.45",
        "support_material_auto": "1", "support_material_style": "snug", "support_material_buildplate_only": "1",
        "support_material_contact_distance": "0.2", "support_material_interface_layers": "3", "complete_objects": "0",
    })
    root = Path(__file__).resolve().parent.parent
    projects = root / "print" / "projects"
    usb = root / "print" / "usb"
    reports = root / "reports"
    for directory in (projects, usb, reports):
        directory.mkdir(parents=True, exist_ok=True)
    report_path = reports / "print-validation.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    report = {job: result for job, result in report.items() if job in JOBS}
    for job in args.jobs:
        settings = dict(config, support_material="1" if job == "Steering" else "0",
                        top_solid_layers="12" if job == "Body" else "8")
        if job == "Body":
            settings.update(perimeter_generator="classic", thin_walls="1", bridge_angle="180")
        stem = f"Lahar_v2_{job}_MK4S_PLA_04"
        project = projects / f"{stem}.3mf"
        gcode = usb / f"{stem}.gcode"
        with tempfile.TemporaryDirectory(dir=args.amf_dir) as temporary:
            profile = Path(temporary) / "settings.ini"
            profile.write_text("\n".join(f"{key} = {value}" for key, value in sorted(settings.items())) + "\n", encoding="utf-8")
            run_slicer(args.slicer, ["--load", slicer_path(profile, args.slicer), "--dont-arrange", "--export-3mf",
                       "--output", slicer_path(project, args.slicer),
                       slicer_path(args.amf_dir / f"Lahar_v2_{job}.amf", args.slicer)], reports / f"{job}-project.log")
            run_slicer(args.slicer, ["--load", slicer_path(profile, args.slicer), "--dont-arrange", "--export-gcode",
                       "--output", slicer_path(gcode, args.slicer), slicer_path(project, args.slicer)], reports / f"{job}-slice.log")
            config_text, result = validate_gcode(gcode, job)
            with ZipFile(project, "a", compression=ZIP_DEFLATED) as archive:
                archive.writestr("Metadata/Slic3r_PE.config", config_text)
            with ZipFile(project) as archive:
                if archive.testzip() or archive.read("Metadata/Slic3r_PE.config").decode() != config_text:
                    raise ValueError("Project configuration did not round-trip")
            if args.roundtrip:
                repeated = Path(temporary) / "roundtrip.gcode"
                run_slicer(args.slicer, ["--dont-arrange", "--export-gcode", "--output", slicer_path(repeated, args.slicer),
                           slicer_path(project, args.slicer)], reports / f"{job}-roundtrip.log")
                repeated_config, repeated_result = validate_gcode(repeated, job)
                if result["toolpath_sha256"] != repeated_result["toolpath_sha256"] or repeated_config != config_text:
                    raise ValueError(f"{job}: standalone 3MF re-slice changed toolpaths or configuration")
                result["standalone_project_roundtrip"] = True
            report[job] = result
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"PASS {job}: {result['estimated_time']}; {result['filament_including_waste_g']} g; {result['support_moves']} support moves")


if __name__ == "__main__":
    main()