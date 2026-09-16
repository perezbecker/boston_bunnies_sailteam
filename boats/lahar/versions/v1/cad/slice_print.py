"""Slice export_print.py's AMFs with the official PrusaSlicer 2.9.6 profiles."""

import argparse
import configparser
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


PRESETS = {
    "print": "0.15mm STRUCTURAL @COREONE 0.4",
    "filament": "Generic PLA @COREONE HF0.4",
    "printer": "Prusa CORE One HF0.4 nozzle",
}


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slicer", required=True, type=Path)
    parser.add_argument("--profiles", required=True, type=Path)
    parser.add_argument("--amf-dir", required=True, type=Path)
    args = parser.parse_args()
    bundle = configparser.ConfigParser(interpolation=None, strict=False)
    bundle.read(args.profiles, encoding="utf-8-sig")
    config = {}
    for kind, name in PRESETS.items():
        config.update(resolve_profile(bundle, kind, name))
        config[f"{kind}_settings_id"] = name
    config.update({
        "binary_gcode": "0",
        "arc_fitting": "disabled",
        "thumbnails": "",
        "layer_height": "0.15",
        "first_layer_height": "0.2",
        "perimeters": "2",
        "top_solid_layers": "4",
        "bottom_solid_layers": "4",
        "top_solid_min_thickness": "0",
        "bottom_solid_min_thickness": "0",
        "fill_pattern": "gyroid",
        "brim_width": "3",
        "brim_type": "outer_only",
        "first_layer_speed": "20",
        "perimeter_speed": "60",
        "external_perimeter_speed": "40",
        "infill_speed": "80",
        "solid_infill_speed": "60",
        "top_solid_infill_speed": "40",
        "bridge_speed": "20",
        "support_material_auto": "1",
        "support_material_style": "snug",
        "support_material_buildplate_only": "1",
        "support_material_contact_distance": "0.2",
        "support_material_interface_layers": "3",
        "complete_objects": "0",
    })
    output = Path(__file__).resolve().parent.parent / "print"
    projects = output / "projects"
    usb = output / "usb"
    projects.mkdir(parents=True, exist_ok=True)
    usb.mkdir(parents=True, exist_ok=True)
    for job, infill, supports in (("Body", "4%", "0"), ("Steering", "15%", "1")):
        settings = dict(config, fill_density=infill, support_material=supports)
        with tempfile.TemporaryDirectory(dir=args.amf_dir) as temporary:
            profile = Path(temporary) / "settings.ini"
            profile.write_text(
                "\n".join(f"{key} = {value}" for key, value in sorted(settings.items())) + "\n",
                encoding="utf-8",
            )
            stem = f"Lahar_{job}_COREONEplus_PLA_04"
            project = projects / f"{stem}.3mf"
            gcode = usb / f"{stem}.gcode"
            subprocess.run([
                str(args.slicer), "--load", slicer_path(profile, args.slicer),
                "--dont-arrange", "--export-3mf", "--output", slicer_path(project, args.slicer),
                slicer_path(args.amf_dir / f"Lahar_{job}.amf", args.slicer),
            ], check=True)
            subprocess.run([
                str(args.slicer), "--load", slicer_path(profile, args.slicer),
                "--dont-arrange", "--export-gcode",
                "--output", slicer_path(gcode, args.slicer), slicer_path(project, args.slicer),
            ], check=True)
            text = gcode.read_text(encoding="utf-8")
            if '; printer_model = COREONE\n' not in text or 'M862.3 P "COREONE"' not in text:
                raise ValueError(f"{gcode.name}: missing CORE One configuration")
            configuration = text.partition("; prusaslicer_config = begin\n")[2]
            configuration, marker, remainder = configuration.partition("; prusaslicer_config = end")
            if not marker:
                raise ValueError(f"{gcode.name}: missing resolved configuration")
            with ZipFile(project, "a", compression=ZIP_DEFLATED) as archive:
                archive.writestr("Metadata/Slic3r_PE.config", configuration)
        print(f"Created {project.name} and {gcode.name}")


if __name__ == "__main__":
    main()