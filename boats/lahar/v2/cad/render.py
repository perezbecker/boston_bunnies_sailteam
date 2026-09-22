"""Render the exported Lahar v2 CAD meshes, never a separately modeled illustration."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from PIL import Image
import trimesh


BACKGROUND = "#f5f7f6"
INK = "#243438"


def figure(title, subtitle, size=(15, 10)):
    canvas = plt.figure(figsize=size, facecolor=BACKGROUND)
    canvas.text(0.055, 0.95, title, fontsize=26, fontweight="bold", color=INK)
    canvas.text(0.055, 0.915, subtitle, fontsize=11, color="#4d6468")
    return canvas


def geometry(objects, shifts=None):
    triangles = []
    colors = []
    shifts = shifts or {}
    light = np.array([0.4, -0.5, 0.76])
    light /= np.linalg.norm(light)
    for obj in objects:
        vertices = np.asarray(obj.get("exterior_vertices", obj["vertices"]), dtype=float) + shifts.get(obj["name"], (0, 0, 0))
        indices = np.asarray(obj.get("exterior_triangles", obj["triangles"]), dtype=int)
        vertices, indices = trimesh.remesh.subdivide_to_size(vertices, indices, max_edge=5.0, max_iter=10)
        faces = vertices[indices]
        normals = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
        lengths = np.linalg.norm(normals, axis=1)
        normals /= np.maximum(lengths[:, None], 1e-12)
        illumination = 0.56 + 0.44 * np.maximum(normals @ light, 0)
        face_colors = illumination[:, None] * np.asarray(obj["color"])
        triangles.append(faces)
        colors.append(face_colors)
    return np.concatenate(triangles), np.concatenate(colors)


def draw_3d(canvas, rectangle, objects, elevation=24, azimuth=-55, shifts=None):
    axes = canvas.add_axes(rectangle, projection="3d", facecolor=BACKGROUND)
    faces, colors = geometry(objects, shifts)
    elevation_radians, azimuth_radians = np.radians([elevation, azimuth])
    direction = np.array([np.cos(elevation_radians) * np.cos(azimuth_radians),
                          np.cos(elevation_radians) * np.sin(azimuth_radians), np.sin(elevation_radians)])
    normals = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
    visible = normals @ direction > 1e-9
    axes.add_collection3d(Poly3DCollection(faces[visible], facecolors=colors[visible], edgecolors="none",
                                         linewidths=0, antialiased=False, zsort="average"))
    points = faces.reshape(-1, 3)
    lower = points.min(axis=0)
    upper = points.max(axis=0)
    span = upper - lower
    margin = max(span) * 0.045
    axes.set_xlim(lower[0] - margin, upper[0] + margin)
    axes.set_ylim(lower[1] - margin, upper[1] + margin)
    axes.set_zlim(lower[2] - margin, upper[2] + margin)
    axes.set_box_aspect(span + 2 * margin, zoom=1.12)
    axes.view_init(elev=elevation, azim=azimuth)
    axes.set_proj_type("ortho")
    axes.set_axis_off()
    return axes


def save(canvas, destination, footer):
    canvas.text(0.055, 0.04, footer, fontsize=10, color="#4d6468")
    canvas.savefig(destination, dpi=160, facecolor=BACKGROUND)
    plt.close(canvas)
    with Image.open(destination) as image:
        pixels = np.asarray(image.convert("RGB"))
        if pixels.std() < 12 or np.mean(pixels.max(axis=2) - pixels.min(axis=2) > 30) < 0.015:
            raise ValueError(f"Blank or missing-color render: {destination}")


def clipped_detail(obj, planes):
    mesh = trimesh.Trimesh(vertices=obj.get("exterior_vertices", obj["vertices"]),
                           faces=obj.get("exterior_triangles", obj["triangles"]), process=False)
    for origin, normal in planes:
        mesh = mesh.slice_plane(plane_origin=origin, plane_normal=normal, cap=True, engine="earcut")
    if not len(mesh.faces):
        raise ValueError(f"Empty assembly detail: {obj['name']}")
    return {"name": obj["name"], "vertices": mesh.vertices, "triangles": mesh.faces, "color": obj["color"]}


def main(amf_dir):
    root = Path(__file__).resolve().parent.parent
    destination = root / "renders"
    destination.mkdir(parents=True, exist_ok=True)
    source = amf_dir / "render-meshes.json"
    objects = json.loads(source.read_text())
    objects = [obj for obj in objects if obj["name"] != "Hardware_Fit_Coupon"]
    by_name = {obj["name"]: obj for obj in objects}
    engineering = json.loads((root / "reports" / "engineering.json").read_text())
    cad = json.loads((root / "reports" / "cad-validation.json").read_text())
    prints = json.loads((root / "reports" / "print-validation.json").read_text())
    mass = engineering["mass_budget"]["nominal_all_up_g"]
    clearance = cad["rudder_full_sweep_clearance_mm"]

    beam = cad["parts"]["Trimaran_Body"]["print_bounds_mm"][1]
    canvas = figure("LAHAR V2 / ONE PIECE", f"220 mm main hull  |  {beam:.1f} mm overall hull beam  |  {mass:.0f} g estimated all-up  |  CORE One+ prototype")
    draw_3d(canvas, (0.02, 0.075, 0.96, 0.79), objects, 23, -53)
    save(canvas, destination / "hero.png",
            "Actual CAD geometry. Yellow: sail. Coral: solid printed vane. Silver: hardware. Colors are illustrative; prints are single-material.")

    body = by_name["Trimaran_Body"]
    inverted = dict(body)
    for key in ("vertices", "exterior_vertices"):
        inverted[key] = np.asarray(body[key]) * [1, -1, -1]
    canvas = figure("ONE BODY / TWO VIEWS", "Main hull, amas, crossbeams and skeg are fused into a single enclosed print. No lid seams or ama assembly.")
    deck_axes = draw_3d(canvas, (0.005, 0.16, 0.49, 0.63), [body], 29, -55)
    deck_axes.set_title("Sailing orientation / continuous deck", fontsize=12, color=INK, pad=4)
    bottom_axes = draw_3d(canvas, (0.505, 0.16, 0.49, 0.63), [inverted], 29, -55)
    bottom_axes.set_title("Print orientation / rounded bottoms upward", fontsize=12, color=INK, pad=4)
    save(canvas, destination / "one-piece-body.png",
         "Deck lies on the print bed. Internal roofs are self-supporting; external hull curves remain smooth and continuous.")

    steering = [obj for obj in objects if not any(word in obj["name"] for word in ("Trimaran_Body", "Mast", "Yard", "Sail"))]
    canvas = figure("STEERING / CLEARANCE", f"Quarter-chord rudder  |  {clearance:.1f} mm full-sweep hull clearance  |  1.8 mm clevis tabs / 2.3 mm pin holes")
    draw_3d(canvas, (0.0, 0.10, 0.58, 0.73), steering, 18, -66)
    top = canvas.add_axes((0.59, 0.27, 0.37, 0.46), facecolor=BACKGROUND)
    plan = [obj for obj in steering if obj["name"] in (
        "Vane_Stand", "Rudder_Stand", "Vane_Arm", "Rudder_Tiller", "Vane_Spacer", "Rudder_Spacer",
        "Vane_623ZZ_Reference", "Rudder_623ZZ_Reference", "M2_Rod_45mm_Reference",
        "Vane_Clevis_Envelope_Reference", "Rudder_Clevis_Envelope_Reference", "Vane_M2_Pin_Reference", "Rudder_M2_Pin_Reference")]
    faces, colors = geometry(plan)
    normals = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
    visible = normals[:, 2] > 1e-9
    faces, colors = faces[visible], colors[visible]
    order = np.argsort(faces[:, :, 2].mean(axis=1))
    top.add_collection(PolyCollection(faces[order, :, :2], facecolors=colors[order], edgecolors="none",
                                      linewidths=0, antialiased=False))
    top.set_xlim(132, 254)
    top.set_ylim(-32, 54)
    top.set_aspect("equal")
    top.set_title("Neutral linkage / top view", fontsize=12, color=INK, pad=12)
    top.annotate("Flow toward bow", xy=(144, 45), xytext=(211, 45),
                 arrowprops={"arrowstyle": "->", "color": INK}, fontsize=10, color=INK, va="center")
    top.text(154, -26, "Vane: 12 mm", ha="center", fontsize=10, color=INK)
    top.text(223, -26, "Tiller: 36 mm", ha="center", fontsize=10, color=INK)
    top.axis("off")
    canvas.text(0.61, 0.20, "64 mm pin spacing; the 45 mm rod overlaps both clevises.\nMetal clevises are dimension envelopes, not manufacturing models.\nFork gap and actual travel require a physical fit check.",
                fontsize=10, color=INK, linespacing=1.6)
    save(canvas, destination / "steering-gear.png",
            "Hull omitted. Flat-backed solid vane and solid counterweight bar, no slot. Lash the weight to the bar and rebalance before sailing.")

    printed_vane = dict(by_name["Vane_Frame"])
    vertices = np.asarray(printed_vane["vertices"], dtype=float)[:, [0, 2, 1]] * [1, -1, 1]
    vertices -= vertices.min(axis=0)
    printed_vane["vertices"] = vertices
    canvas = figure("VANE / DIRECT BED CONTACT", "September 22 revision. Flat blade and solid counterweight bar, no slot. The stock socket keeps its original axis.", (16, 9))
    vane_axes = draw_3d(canvas, (0.015, 0.24, 0.49, 0.56), [printed_vane], 24, -63)
    vane_axes.set_title("Print orientation / flat back on smooth PEI", fontsize=12, color=INK, pad=10)
    section_axes = canvas.add_axes((0.55, 0.28, 0.40, 0.48), facecolor=BACKGROUND)
    vane_mesh = trimesh.Trimesh(vertices=vertices, faces=printed_vane["triangles"], process=False)
    first_section = vane_mesh.section(plane_origin=[0, 0, 0.1], plane_normal=[0, 0, 1])
    if first_section is None:
        raise ValueError("The revised vane has no direct first-layer cross-section")
    first_loops = sorted(first_section.discrete,
                         key=lambda loop: abs(np.dot(loop[:, 0], np.roll(loop[:, 1], 1)) -
                                              np.dot(loop[:, 1], np.roll(loop[:, 0], 1))), reverse=True)
    for index, loop in enumerate(first_loops):
        section_axes.fill(loop[:, 0], loop[:, 1], color="#df5140" if index == 0 else BACKGROUND,
                           edgecolor="#aa3f34", linewidth=0.7)
    section_axes.set_xlim(-6, 180)
    section_axes.set_ylim(-6, 105)
    section_axes.set_aspect("equal")
    section_axes.set_title("CAD cross-section through the first 0.2 mm layer", fontsize=11, color=INK, pad=12)
    section_axes.set_xlabel("Print X (mm)", color=INK)
    section_axes.set_ylabel("Print Y (mm)", color=INK)
    section_axes.spines[["top", "right"]].set_visible(False)
    adhesion = engineering["steering_print_adhesion"]
    canvas.text(0.055, 0.16, f"Direct CAD model contact: {cad['vane_first_layer_contact_area_mm2']:.0f} mm2.\nThe blade prints as solid plastic directly on the sheet, not on supports.",
                fontsize=11, color=INK, linespacing=1.6)
    canvas.text(0.555, 0.16, f"Steering brim: {adhesion['brim_mm']:.0f} mm, attached.\nActual first-layer extrusion: no more than {adhesion['maximum_first_layer_speed_mm_s']:.0f} mm/s.",
                fontsize=11, color=INK, linespacing=1.6)
    save(canvas, destination / "vane-print-contact.png",
         "The existing hull and mounting interfaces are unchanged. Bed preparation still matters; the revised vane has not yet been test-printed.")

    canvas = figure("ASSEMBLY / LOCATING DETAILS", "Two four-bolt yard clamps and two distinct, backed steering-mount recesses. Views show actual CAD, exploded for assembly.", (17, 10))
    clamp_objects = [obj for obj in objects if obj["name"].startswith("Lower_Yard_") and obj["name"] != "Lower_Yard_Reference"]
    clamp_objects.extend([
        clipped_detail(by_name["Mast_Reference"], [((0, 0, 15), (0, 0, 1)), ((0, 0, 65), (0, 0, -1))]),
        clipped_detail(by_name["Lower_Yard_Reference"], [((0, -24, 0), (0, 1, 0)), ((0, 24, 0), (0, -1, 0))]),
    ])
    shifts = {}
    for obj in clamp_objects:
        if obj["name"] == "Lower_Yard_Yard_Cap" or "_Bolt_" in obj["name"]:
            shifts[obj["name"]] = (-10, 0, 0)
        elif obj["name"] == "Lower_Yard_Mast_Cap" or "_Nut_" in obj["name"]:
            shifts[obj["name"]] = (10, 0, 0)
    clamp_axes = draw_3d(canvas, (0.015, 0.25, 0.48, 0.56), clamp_objects, 24, -57, shifts)
    clamp_axes.set_title("One set shown / repeat at the upper yard", fontsize=12, color=INK, pad=8)
    mount_deck = clipped_detail(body, [((138, 0, 0), (1, 0, 0)), ((0, -26, 0), (0, 1, 0)),
                                       ((0, 26, 0), (0, -1, 0)), ((0, 0, -2), (0, 0, 1))])
    mount_axes = draw_3d(canvas, (0.515, 0.25, 0.48, 0.56),
                          [mount_deck, by_name["Vane_Stand"], by_name["Rudder_Stand"]], 35, -63,
                          {"Vane_Stand": (0, 0, 12), "Rudder_Stand": (0, 0, 12)})
    mount_axes.set_title("Steering stands raised 12 mm above their keys", fontsize=12, color=INK, pad=8)
    mount_axes.text(154, 0, 47, "Vane", fontsize=10, color=INK, ha="center")
    mount_axes.text(220, 0, 47, "Rudder", fontsize=10, color=INK, ha="center")
    canvas.text(0.055, 0.17, "Each set: yard-side cap + middle saddle + mast-side cap.\nFour M2 x 16 socket-cap bolts and four M2 hex nuts.\n6 mm mast / 4 mm yard; retain the clamping gaps.", fontsize=11, color=INK, linespacing=1.6)
    canvas.text(0.555, 0.17, "Match the asymmetric feet to the forward and aft recesses.\nDry-fit the linkage, then bond the stand bases to the deck.\n0.8 mm-deep keys; at least 1.8 mm of sealed hull backing.", fontsize=11, color=INK, linespacing=1.6)
    save(canvas, destination / "assembly-details.png",
         "Metal bolts/nuts are supplied separately. Recesses locate the stands; they are not snap fasteners. Do not drill through the hull.")

    canvas = figure("CLOSED HULL / INTERNAL ROOFS", "Longitudinal section through the main hull. The outside is rounded; only the hidden cavity roofs are angled.", (15, 8))
    axes = canvas.add_axes((0.07, 0.18, 0.88, 0.64), facecolor=BACKGROUND)
    mesh = trimesh.Trimesh(vertices=body["vertices"], faces=body["triangles"], process=False)
    section = mesh.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])
    if section is None:
        raise ValueError("Missing main-hull centerline section")
    def loop_area(loop):
        along, height = loop[:, 0], loop[:, 2]
        return abs(np.dot(along, np.roll(height, 1)) - np.dot(height, np.roll(along, 1))) / 2
    loops = sorted(section.discrete, key=loop_area, reverse=True)
    for index, loop in enumerate(loops):
        axes.fill(loop[:, 0], loop[:, 2], color="#168c85" if index == 0 else BACKGROUND,
                  edgecolor="#168c85", linewidth=0.7)
    waterline = engineering["upright_cases"][0]["waterline_at_x110_mm"]
    trim = math.radians(engineering["upright_cases"][0]["trim_stern_down_deg"])
    along = np.array([0, 220])
    heights = (waterline + (along - 110) * math.sin(trim)) / math.cos(trim)
    axes.plot(along, heights, color="#326da0", linestyle="--", linewidth=1.2)
    axes.text(3, -12, "Nominal waterline", color="#326da0", fontsize=10)
    axes.annotate("Continuous printed deck", xy=(100, 1.2), xytext=(95, 12),
                  arrowprops={"arrowstyle": "->", "color": INK}, color=INK, fontsize=10)
    axes.annotate("Blind mast well", xy=(70, -20), xytext=(23, -43),
                  arrowprops={"arrowstyle": "->", "color": INK}, color=INK, fontsize=10)
    axes.text(110, -76, "0.9 mm ribs / 12 mm pitch / 45-degree internal roofs / 0.6 mm final gap", fontsize=10, color=INK, ha="center")
    axes.set_xlim(-4, 224)
    axes.set_ylim(-81, 19)
    axes.set_aspect("equal")
    axes.set_xlabel("Bow to stern (mm)", color=INK)
    axes.set_ylabel("Sailing height Z (mm)", color=INK)
    axes.spines[["top", "right"]].set_visible(False)
    save(canvas, destination / "hull-section.png",
         "Body prints upside down. Four perimeters and 12 top/bottom layers; no removable internal supports. Physical leak test still required.")

    canvas = figure("CORE ONE+ / TWO PRINT JOBS", "250 x 220 mm beds. Revised steering: 5 mm brim. Body unchanged: 3 mm brim; no hull reprint needed.", (16, 8))
    for index, job in enumerate(("Steering", "Body")):
        xml = ET.parse(amf_dir / f"Lahar_v2_{job}.amf").getroot()
        job_objects = []
        for element in xml.findall("object"):
            name = element.find("metadata").text
            points = [[float(vertex.find(f"coordinates/{axis}").text) for axis in "xyz"]
                      for vertex in element.findall("mesh/vertices/vertex")]
            faces = [[int(triangle.find(f"v{vertex}").text) for vertex in (1, 2, 3)]
                     for triangle in element.findall("mesh/volume/triangle")]
            job_objects.append({"name": name, "vertices": points, "triangles": faces,
                                "color": by_name.get(name, {"color": [0.6, 0.64, 0.65]})["color"]})
        axes = draw_3d(canvas, (0.02 + index * 0.49, 0.16, 0.46, 0.66), job_objects, 65, -73)
        axes.plot([0, 250, 250, 0, 0], [0, 0, 220, 220, 0], [-0.2] * 5, color="#a4b4b4", linewidth=1)
        axes.set_xlim(-5, 255)
        axes.set_ylim(-5, 225)
        axes.set_zlim(0, 70)
        axes.set_box_aspect((260, 230, 70))
        label = "STEERING + CLAMPS + COUPON" if job == "Steering" else "ONE-PIECE BODY"
        axes.set_title(f"{label}  |  {prints[job]['estimated_time']}  |  {prints[job]['filament_including_waste_g']:.2f} g", fontsize=11, color=INK, pad=0)
    save(canvas, destination / "print-layouts.png",
            "Geometry shown; brims/supports are omitted. All 16 parts are retained. For the reported vane failure, reprint only the steering job.")
    manifest = {
        "mesh_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "images": {path.name: {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                               "pixels": list(Image.open(path).size)} for path in sorted(destination.glob("*.png"))
                   if path.name != "exploded-hulls.png"},
    }
    (root / "reports" / "render-validation.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS: seven nonblank CAD-derived renders generated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amf-dir", type=Path, required=True)
    main(parser.parse_args().amf_dir)