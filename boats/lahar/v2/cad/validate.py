"""CAD checks and exact planar four-bar kinematics for the Lahar v2 prototype."""

import itertools
import math


def linkage_pose(model, vane_angle):
    index = math.radians(model["ARM_INDEX"])
    angle = index + math.radians(vane_angle)
    vane_radius = model["VANE_RADIUS"]
    tiller_radius = model["TILLER_RADIUS"]
    spacing = model["RUDDER_X"] - model["VANE_X"]
    length = math.sqrt(spacing ** 2 - (vane_radius + tiller_radius) ** 2)
    vane_pin = (model["VANE_X"] + vane_radius * math.sin(angle),
                -vane_radius * math.cos(angle))
    relative = (vane_pin[0] - model["RUDDER_X"], vane_pin[1])
    distance = math.hypot(*relative)
    cosine = (distance ** 2 + tiller_radius ** 2 - length ** 2) / (2 * distance * tiller_radius)
    if not -1.0 <= cosine <= 1.0:
        raise ValueError(f"Linkage cannot close at {vane_angle} degrees")
    direction = math.atan2(relative[1], relative[0])
    spread = math.acos(cosine)
    candidates = []
    for sign in (-1, 1):
        polar = direction + sign * spread
        rudder_angle = math.degrees(polar - math.pi / 2 - index)
        rudder_angle = (rudder_angle + 180) % 360 - 180
        candidates.append((rudder_angle, polar))
    rudder_angle, polar = min(candidates, key=lambda candidate: abs(candidate[0]))
    rudder_pin = (model["RUDDER_X"] + tiller_radius * math.cos(polar),
                  tiller_radius * math.sin(polar))
    return rudder_angle, vane_pin, rudder_pin, length


def bounds_overlap(first, second):
    return all(min(getattr(first, axis + "Max"), getattr(second, axis + "Max")) >
               max(getattr(first, axis + "Min"), getattr(second, axis + "Min")) + 0.0001
               for axis in "XYZ")


def assert_clear(first_name, first, second_name, second, context):
    if bounds_overlap(first.BoundBox, second.BoundBox):
        overlap = first.common(second).Volume
        if overlap > 0.001:
            raise ValueError(f"{context}: {first_name} intersects {second_name} ({overlap:.4f} mm3)")


def validate_model(model):
    import FreeCAD as App
    import Part
    from FreeCAD import Vector

    parts = {name: obj.Shape for name, obj in model["parts"].items()
             if name != "Hardware_Fit_Coupon"}
    cell_spans = {name: max(cell.optimalBoundingBox().XLength for cell in cavity.Solids)
                  for name, cavity in model["cavities"].items()}
    if max(cell_spans.values()) > model["RIB_PITCH"] - model["RIB_THICKNESS"] + 0.001:
        raise ValueError("An internal bridge cell exceeds the supported roof span")
    body_solid = parts["Trimaran_Body"].Solids[0]
    expected_cells = sum(len(cavity.Solids) for cavity in model["cavities"].values())
    if len(body_solid.Shells) != expected_cells + 1 or not all(shell.isClosed() for shell in body_solid.Shells):
        raise ValueError("An internal flotation cell is open to the exterior or another cell")
    if model["parts"]["Trimaran_Body"].PrintRotationX != 180:
        raise ValueError("The one-piece body must print deck-down")
    vane_center = Vector(model["VANE_X"] - model["VANE_LEVER"], 0, 83)
    vane_probe = Part.makeLine(vane_center - Vector(0, 2, 0), vane_center + Vector(0, 2, 0))
    if abs(vane_probe.common(parts["Vane_Frame"]).Length - model["VANE_PLATE_THICKNESS"]) > 0.001:
        raise ValueError("The wind vane must have a continuous printed solid web")
    mount_checks = {}
    cavity_shapes = Part.makeCompound(list(model["cavities"].values()))
    for name, keys in model["MOUNT_KEYS"].items():
        pockets = Part.makeCompound(model["mount_key_shapes"](name, model["GUIDE_SIDE_CLEARANCE"], model["GUIDE_DEPTH"]))
        feet = Part.makeCompound(model["mount_key_shapes"](name, 0.0, model["GUIDE_FOOT_HEIGHT"]))
        floor_skin = pockets.distToShape(cavity_shapes)[0]
        if floor_skin < model["WALL"] - 0.001 or pockets.common(parts["Trimaran_Body"]).Volume > 0.001:
            raise ValueError(f"{name}: locating pockets open into or thin the hull")
        if feet.cut(pockets).Volume > 0.001 or feet.common(parts["Trimaran_Body"]).Volume > 0.001:
            raise ValueError(f"{name}: guide feet do not fit their recessed pockets")
        reversed_stand = parts[name].copy()
        center_x = model["VANE_X"] if name == "Vane_Stand" else 204.0
        reversed_stand.rotate(Vector(center_x, 0, 0), Vector(0, 0, 1), 180)
        if reversed_stand.common(parts["Trimaran_Body"]).Volume < 0.01:
            raise ValueError(f"{name}: asymmetric guides accept a reversed stand")
        other_name = "Rudder_Stand" if name == "Vane_Stand" else "Vane_Stand"
        other_center = 204.0 if name == "Vane_Stand" else model["VANE_X"]
        for angle in (0, 180):
            swapped = parts[other_name].copy()
            swapped.translate(Vector(center_x - other_center, 0, 0))
            swapped.rotate(Vector(center_x, 0, 0), Vector(0, 0, 1), angle)
            if swapped.common(parts["Trimaran_Body"]).Volume < 0.01:
                raise ValueError(f"{name}: recessed keys accept the other steering stand")
        mount_checks[name] = {"keys_xy_width_depth_mm": keys, "minimum_backing_mm": floor_skin,
                              "side_clearance_mm": model["GUIDE_SIDE_CLEARANCE"],
                              "vertical_clearance_mm": model["GUIDE_DEPTH"] - model["GUIDE_FOOT_HEIGHT"],
                              "reversed_mount_rejected": True, "swapped_mount_rejected": True}
    clamp_checks = {}
    for prefix, level in zip(("Lower", "Upper"), model["YARD_LEVELS"]):
        clamp_parts = [parts[f"{prefix}_Yard_{name}"] for name in ("Yard_Cap", "Saddle", "Mast_Cap")]
        assembly = Part.makeCompound(clamp_parts)
        mast = Part.makeCylinder(3.0, model["CLAMP_WIDTH"] + 2,
                                 Vector(model["MAST_X"], 0, level - model["CLAMP_WIDTH"] / 2 - 1))
        yard = Part.makeCylinder(2.0, model["CLAMP_WIDTH"] + 2,
                                 Vector(model["YARD_AXIS_X"], -model["CLAMP_WIDTH"] / 2 - 1, level), Vector(0, 1, 0))
        if mast.common(yard).Volume > 0.001 or assembly.common(mast.fuse(yard)).Volume > 0.001:
            raise ValueError(f"{prefix}: crossed rods intersect or do not fit the clamp")
        bolt_names = [f"{prefix}_Yard_M2_Bolt_{index}_Reference" for index in range(1, 5)]
        nut_names = [f"{prefix}_Yard_M2_Nut_{index}_Reference" for index in range(1, 5)]
        for name in bolt_names + nut_names:
            if assembly.common(model["doc"].getObject(name).Shape).Volume > 0.001:
                raise ValueError(f"{prefix}: bolt head, shaft or captive nut does not fit: {name}")
        engagement = model["CLAMP_FRONT_X"] + model["CLAMP_HEAD_DEPTH"] + model["CLAMP_BOLT_LENGTH"] - (
            model["CLAMP_REAR_X"] - model["CLAMP_NUT_DEPTH"] + 1.6)
        if engagement < 0.4:
            raise ValueError("M2 clamp bolts do not extend through the complete nut thickness")
        clamp_checks[prefix] = {"parts": 3, "bolts": 4, "bolt_size": "M2 x 16 socket cap",
                                "nuts": 4, "rod_center_offset_mm": model["MAST_X"] - model["YARD_AXIS_X"],
                                "split_gap_mm": model["CLAMP_SPLIT_GAP"], "bolt_past_nut_mm": engagement}
    for (first_name, first), (second_name, second) in itertools.combinations(parts.items(), 2):
        assert_clear(first_name, first, second_name, second, "Neutral assembly")
    moving_axes = {"Vane_Frame": "VANE_X", "Vane_Arm": "VANE_X",
                   "Rudder_Blade": "RUDDER_X", "Rudder_Tiller": "RUDDER_X"}
    fixed = {name: shape for name, shape in parts.items() if name not in moving_axes}
    samples = []
    for step in range(-int(model["VANE_LIMIT"]), int(model["VANE_LIMIT"]) + 1, 2):
        rudder_angle, vane_pin, rudder_pin, length = linkage_pose(model, step)
        if abs(rudder_angle) >= model["RUDDER_LIMIT"]:
            raise ValueError("Linkage reaches the rudder stop before the vane stop")
        moved = {}
        for name, axis in moving_axes.items():
            shape = parts[name].copy()
            shape.rotate(Vector(model[axis], 0, 0), Vector(0, 0, 1),
                         step if axis == "VANE_X" else rudder_angle)
            moved[name] = shape
            for fixed_name, fixed_shape in fixed.items():
                assert_clear(name, shape, fixed_name, fixed_shape, f"Vane {step} deg")
        for (first_name, first), (second_name, second) in itertools.combinations(moved.items(), 2):
            assert_clear(first_name, first, second_name, second, f"Vane {step} deg")
        height = model["ARM_Z"] + model["TAB_THICKNESS"] / 2
        for name, start, end in (("Vane clevis barrel", vane_pin, rudder_pin),
                                  ("Rudder clevis barrel", rudder_pin, vane_pin)):
            direction = Vector((end[0] - start[0]) / length, (end[1] - start[1]) / length, 0)
            base = Vector(start[0], start[1], height) + 8.0 * direction
            barrel = Part.makeCylinder(4.0, 15.0, base, direction)
            for part_name, shape in {**fixed, **moved}.items():
                assert_clear(name, barrel, part_name, shape, f"Vane {step} deg; conservative barrel")
        samples.append({"vane_deg": step, "rudder_deg": round(rudder_angle, 5)})
    gain = (linkage_pose(model, 0.01)[0] - linkage_pose(model, -0.01)[0]) / 0.02
    if abs(gain + model["VANE_RADIUS"] / model["TILLER_RADIUS"]) > 0.001:
        raise ValueError("Incorrect neutral steering sense or ratio")
    swept = Part.makeCylinder(18.1, model["RUDDER_TOP"] - model["RUDDER_BOTTOM"],
                              Vector(model["RUDDER_X"], 0, model["RUDDER_BOTTOM"]))
    swept = swept.fuse(Part.makeCylinder(4.0, 14.0, Vector(model["RUDDER_X"], 0, model["RUDDER_TOP"] - 2)))
    hull_and_skeg = parts["Trimaran_Body"]
    clearance = swept.distToShape(hull_and_skeg)[0]
    if clearance < 3.0 or swept.common(hull_and_skeg).Volume > 0.001:
        raise ValueError("Insufficient full rudder sweep clearance")
    return {
        "freecad_version": ".".join(App.Version()[:3]),
        "printed_boat_parts": len(parts),
        "minimum_skin_mm": model["minimum_skins"],
        "body_single_solid": len(hull_and_skeg.Solids) == 1,
        "body_print_rotation_x_deg": model["parts"]["Trimaran_Body"].PrintRotationX,
        "internal_rib_pitch_mm": model["RIB_PITCH"],
        "maximum_internal_cell_span_mm": cell_spans,
        "closed_internal_cells": {name: len(cavity.Solids) for name, cavity in model["cavities"].items()},
        "outer_shell_and_cells_closed": True,
        "roof_final_gap_mm": model["CAVITY_ROOF_GAP"],
        "steering_mount_guides": mount_checks,
        "vane_plate_thickness_mm": model["VANE_PLATE_THICKNESS"],
        "yard_clamps": clamp_checks,
        "solid_pla_boat_upper_bound_g": sum(shape.Volume for shape in parts.values()) * 0.00124,
        "rudder_full_sweep_clearance_mm": clearance,
        "neutral_gain": gain,
        "neutral_pin_distance_mm": linkage_pose(model, 0)[3],
        "motion_samples": samples,
        "hardware_assumption": "8 mm OD clevis barrel 8-23 mm from pin; fork gap unverified",
    }


def mass_budget(model, print_report):
    import numpy as np

    components = []
    for name, record in model["parts"].items():
        if name != "Hardware_Fit_Coupon":
            components.append({"name": name, "mass_g": record["volume_mm3"] * 0.00124,
                               "position_mm": record["centroid_mm"],
                               "basis": "CAD volume at 1.24 g/cm3; not weighed"})
    printed = sum(component["mass_g"] for component in components)
    vane = model["parts"]["Vane_Frame"]
    vane_moment = vane["volume_mm3"] * 0.00124 * (model["VANE_X"] - vane["centroid_mm"][0])
    balance_position = vane_moment / 3.0
    if not model["COUNTERWEIGHT_SLOT_START"] <= balance_position <= model["COUNTERWEIGHT_SLOT_END"]:
        raise ValueError("The nominal 3 g vane counterweight cannot balance the printed paddle within its slot")
    clamp_center = (model["CLAMP_FRONT_X"] + model["CLAMP_REAR_X"]) / 2
    index = math.radians(model["ARM_INDEX"])
    extras = [
        ("6 mm hardwood mast", math.pi * 3 ** 2 * 250 * 0.00065, (model["MAST_X"], 0, 102.2)),
        ("Two 4 mm hardwood yards", 2 * math.pi * 2 ** 2 * 210 * 0.00065, (model["YARD_AXIS_X"], 0, 125)),
        ("190 x 170 mm sail, 30 g/m2", 0.190 * 0.170 * 30, (model["CLAMP_FRONT_X"] - 1.0, 0, 125)),
        ("Lower yard four M2 x 16 bolts and four nuts", 2.8, (clamp_center, 0, model["YARD_LEVELS"][0])),
        ("Upper yard four M2 x 16 bolts and four nuts", 2.8, (clamp_center, 0, model["YARD_LEVELS"][1])),
        ("Two 623ZZ bearings", 3.4, ((model["VANE_X"] + model["RUDDER_X"]) / 2, 0, 17.8)),
        ("134 mm of 3 mm carbon stock", math.pi * 1.5 ** 2 * 134 * 0.0016,
         ((62 * model["VANE_X"] + 72 * model["RUDDER_X"]) / 134, 0, (62 * 33 - 72 * 4) / 134)),
        ("45 mm M2 rod, two clevises and screws", 6.0, (180, 7, 25.1)),
        ("Vane fore-aft balance screw and nuts", 3.0, (model["VANE_X"] + balance_position, 0, 83)),
        ("Lateral vane balance nuts allowance", 1.5, (model["VANE_X"] - 24 * math.sin(index), 24 * math.cos(index), model["ARM_Z"])),
        ("Rigging thread and sail attachment", 0.7, (90, 0, 90)),
        ("Adhesive and seal coat allowance", 10.0, (110, 0, -10)),
    ]
    for name, mass, position in extras:
        components.append({"name": name, "mass_g": mass, "position_mm": position,
                           "basis": "Planning assumption; replace with measured value"})
    total = sum(component["mass_g"] for component in components)
    center = sum((np.asarray(component["position_mm"]) * component["mass_g"] for component in components), np.zeros(3)) / total
    extruded = sum(print_report[job]["filament_including_waste_g"] for job in ("Body", "Steering"))
    coupon_mass = model["parts"]["Hardware_Fit_Coupon"]["volume_mm3"] * 0.00124
    boat_extruded = extruded - coupon_mass
    return {
        "components": components, "nominal_all_up_g": total, "nominal_cg_mm": list(center),
        "printed_cad_mass_g": printed, "boat_jobs_filament_with_waste_g": boat_extruded,
        "all_jobs_filament_with_waste_g": extruded, "coupon_cad_mass_excluded_g": coupon_mass,
        "conservative_all_up_g": total + max(0, boat_extruded - printed),
        "note": "The coupon's CAD mass is excluded even though it shares the steering job. The conservative case counts all remaining supports/brims as boat mass. Hardware and adhesive masses are assumptions.",
    }


def hydrostatic_equilibrium(model, mass, center, heel=0.0):
    import numpy as np
    from scipy.optimize import least_squares
    import trimesh

    origin = np.array([110.0, 0.0, 0.0])
    heel_rotation = trimesh.transformations.rotation_matrix(math.radians(heel), (1, 0, 0), origin)
    envelopes = []
    for geometry in model["hulls"].values():
        mesh = trimesh.Trimesh(vertices=geometry["vertices"], faces=geometry["triangles"], process=False)
        if not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume <= 0:
            raise ValueError("Hydrostatic envelope is not a closed, oriented mesh")
        mesh.apply_transform(heel_rotation)
        envelopes.append(mesh)
    center = trimesh.transform_points([center], heel_rotation)[0]

    def evaluate(waterline, trim):
        pitch_rotation = trimesh.transformations.rotation_matrix(math.radians(trim), (0, 1, 0), origin)
        volume = 0.0
        moment = np.zeros(3)
        for envelope in envelopes:
            oriented = envelope.copy()
            oriented.apply_transform(pitch_rotation)
            submerged = oriented.slice_plane(plane_origin=(0, 0, waterline), plane_normal=(0, 0, -1),
                                               cap=True, engine="earcut")
            if len(submerged.faces) == 0:
                continue
            if not submerged.is_watertight:
                raise ValueError("Waterplane clipping produced an open mesh")
            volume += submerged.volume
            moment += submerged.center_mass * submerged.volume
        if volume <= 0:
            raise ValueError("Hydrostatic iteration left the submerged range")
        gravity_center = trimesh.transform_points([center], pitch_rotation)[0]
        return volume / 1000, moment / volume, gravity_center

    def residual(variables):
        displacement, buoyancy, gravity = evaluate(*variables)
        return [(displacement - mass) / 10, buoyancy[0] - gravity[0]]

    solution = least_squares(residual, [-20.0, 1.5], bounds=([-80.0, -12.0], [model["DECK_Z"] - 0.1, 12.0]),
                              jac="3-point", diff_step=0.001, x_scale=[10, 2], max_nfev=60,
                              ftol=1e-8, xtol=1e-8, gtol=1e-8)
    waterline, trim = map(float, solution.x)
    displacement, buoyancy, gravity = evaluate(waterline, trim)
    if not solution.success or abs(displacement - mass) > 0.05 or abs(buoyancy[0] - gravity[0]) > 0.05:
        raise ValueError(f"Mesh hydrostatic solve did not converge: {solution.message}; {solution.fun}")
    pitch_rotation = trimesh.transformations.rotation_matrix(math.radians(trim), (0, 1, 0), origin)
    ama_clearances = []
    for index, envelope in enumerate(envelopes):
        oriented = envelope.copy()
        oriented.apply_transform(pitch_rotation)
        if index:
            ama_clearances.append(float(oriented.bounds[0, 2] - waterline))
    if not model["deck_points"]:
        raise ValueError("Missing continuous deck outline for freeboard calculation")
    deck_points = trimesh.transform_points(model["deck_points"], pitch_rotation @ heel_rotation)
    return {
        "mass_g": mass, "heel_deg": heel, "waterline_at_x110_mm": waterline,
        "trim_stern_down_deg": trim, "minimum_deck_freeboard_mm": float(deck_points[:, 2].min() - waterline),
        "ama_bottom_clearance_mm": min(ama_clearances),
        "longitudinal_balance_error_mm": float(buoyancy[0] - gravity[0]),
        "displacement_error_g": float(displacement - mass),
        "solver_tolerance_g_mm": [0.05, 0.05],
        "restoring_moment_Nmm": float(mass * 0.00980665 * (gravity[1] - buoyancy[1])),
        "solver_evaluations": solution.nfev,
    }


def engineering_report(model, print_report):
    budget = mass_budget(model, print_report)
    center = budget["nominal_cg_mm"]
    loading_check = math.ceil((budget["conservative_all_up_g"] + 15) / 10) * 10
    cases = [hydrostatic_equilibrium(model, mass, center)
             for mass in (budget["nominal_all_up_g"], budget["conservative_all_up_g"], loading_check)]
    if any(case["minimum_deck_freeboard_mm"] < 12 for case in cases):
        raise ValueError(f"Insufficient loaded deck freeboard: {cases}")
    heel_cases = [hydrostatic_equilibrium(model, budget["conservative_all_up_g"], center, heel)
                  for heel in (-10, -5, 5, 10)]
    if any(case["restoring_moment_Nmm"] * case["heel_deg"] <= 0 for case in heel_cases):
        raise ValueError("Non-restoring heel response at the planning load")
    area = model["VANE_WIDTH"] * model["VANE_HEIGHT"] / 1e6
    vane = model["parts"]["Vane_Frame"]
    vane_mass = vane["volume_mm3"] * 0.00124
    vane_moment = vane_mass * (model["VANE_X"] - vane["centroid_mm"][0])
    error = math.radians(10)
    coefficient = 2 * math.sin(error)
    torque_at_one = 0.5 * 1.225 * area * coefficient * model["VANE_LEVER"]
    rudder_angle = abs(math.radians(linkage_pose(model, 10)[0]))
    rudder_area = model["RUDDER_CHORD"] * (model["RUDDER_TOP"] - model["RUDDER_BOTTOM"]) / 1e6
    rudder_force = 0.5 * 1000 * 0.6 ** 2 * rudder_area * 2.5 * rudder_angle
    gain = model["VANE_RADIUS"] / model["TILLER_RADIUS"]
    required = [0.010 + gain * rudder_force * lever for lever in (1, 2, 6)]
    return {
        "mass_budget": budget, "upright_cases": cases, "heel_cases": heel_cases,
        "loading_check_g": loading_check,
        "hydrostatics_method": "CAD-derived 0.04 mm deflection meshes; trimesh capped waterplane clipping; scipy bounded least-squares equilibrium",
        "hydrostatics_note": "Sealed hull envelopes in fresh water; appendage buoyancy omitted conservatively. Loads use the nominal CG. No waves, leakage, sail force or dynamic validation.",
        "steering": {
            "solid_vane_area_mm2": area * 1e6, "vane_center_lever_mm": model["VANE_LEVER"],
            "printed_vane_mass_g": vane_mass,
            "printed_vane_fore_aft_moment_g_mm": vane_moment,
            "paddle_only_counterweight_3g_position_mm": vane_moment / 3.0,
            "counterweight_slot_mm": [model["COUNTERWEIGHT_SLOT_START"], model["COUNTERWEIGHT_SLOT_END"]],
            "balance_note": "Paddle-only static moment; rebalance with stock, arm and clevis connected. Budget includes 3 g fore-aft hardware plus 1.5 g lateral nuts.",
            "v1_area_lever_improvement": area * model["VANE_LEVER"] / (0.036 * 0.072 * 21),
            "vane_torque_at_10deg_Nmm": {str(speed): torque_at_one * speed ** 2 for speed in (0.5, 0.75, 1.0, 1.5, 2.0)},
            "friction_acceptance_target_at_vane_Nmm": 0.010,
            "rudder_force_at_0_6mps_N": rudder_force,
            "required_vane_torque_for_1_2_6mm_hinge_offset_Nmm": required,
            "apparent_wind_break_even_mps_for_1_2_6mm_offset": [math.sqrt(value / torque_at_one) for value in required],
            "assumptions": "Illustrative, not measured: air CN=2sin(error), water lift slope=2.5/rad, 0.6 m/s boat speed, hinge offset 1-6 mm, 0.010 Nmm breakaway friction. Low-Reynolds-number behavior is uncertain; these are not guaranteed thresholds.",
        },
    }


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    import runpy

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engineering", action="store_true")
    parser.add_argument("--amf-dir", type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    if args.engineering:
        if args.amf_dir is None:
            parser.error("--engineering requires --amf-dir from export_print.py")
        model = json.loads((args.amf_dir / "hydrostatics-input.json").read_text())
        report = engineering_report(model, json.loads((source.parent / "reports" / "print-validation.json").read_text()))
        (source.parent / "reports" / "engineering.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in report.items() if key != "mass_budget"}, indent=2))
        print("Mass budget:", report["mass_budget"]["nominal_all_up_g"], "g nominal;",
              report["mass_budget"]["conservative_all_up_g"], "g conservative")
    else:
        model = runpy.run_path(str(source / "lahar.FCMacro"))
        print(json.dumps(validate_model(model), indent=2))