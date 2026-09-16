"""Generate checked FreeCAD, STEP, STL, AMF, and render geometry for Lahar v2."""

import argparse
from collections import Counter
import json
from pathlib import Path
import runpy
import xml.etree.ElementTree as ET

import FreeCAD as App
import MeshPart
import Part
from FreeCAD import Vector

from validate import validate_model


LAYOUTS = {
    "Body": {"Trimaran_Body": (15, 5, 0)},
    "Steering": {
        "Hardware_Fit_Coupon": (8, 8, 0),
        "Rudder_Blade": (80, 8, 0), "Rudder_Tiller": (114, 8, 0),
        "Vane_Arm": (156, 8, 0), "Rudder_Stand": (198, 8, 0),
        "Vane_Stand": (8, 58, 0),
        "Vane_Spacer": (210, 50, 0), "Rudder_Spacer": (228, 50, 0),
        "Vane_Frame": (68, 102, 0),
        "Lower_Yard_Yard_Cap": (46, 58, 0), "Lower_Yard_Saddle": (80, 70, 0),
        "Lower_Yard_Mast_Cap": (112, 70, 0), "Upper_Yard_Yard_Cap": (144, 70, 0),
        "Upper_Yard_Saddle": (176, 70, 0), "Upper_Yard_Mast_Cap": (208, 70, 0),
    },
}


def checked_mesh(shape):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04,
                                  AngularDeflection=0.12, Relative=False)
    if mesh.Volume < 0:
        mesh.flipNormals()
    if not mesh.isSolid() or mesh.Volume <= 0:
        raise ValueError("Mesh is not a closed, oriented solid")
    points, triangles = mesh.Topology
    edges = Counter(tuple(sorted(edge)) for triangle in triangles
                    for edge in zip(triangle, (*triangle[1:], triangle[0])))
    if any(count != 2 for count in edges.values()):
        raise ValueError("Mesh has a boundary or non-manifold edge")
    return mesh


def write_amf(path, objects):
    root = ET.Element("amf", unit="millimeter", version="1.1")
    for object_id, (name, mesh, position) in enumerate(objects):
        element = ET.SubElement(root, "object", id=str(object_id))
        ET.SubElement(element, "metadata", type="name").text = name
        mesh_element = ET.SubElement(element, "mesh")
        vertices = ET.SubElement(mesh_element, "vertices")
        points, triangles = mesh.Topology
        for point in points:
            coordinates = ET.SubElement(ET.SubElement(vertices, "vertex"), "coordinates")
            for axis, value, shift in zip("xyz", point, position):
                ET.SubElement(coordinates, axis).text = f"{value + shift:.6f}"
        volume = ET.SubElement(mesh_element, "volume")
        ET.SubElement(volume, "metadata", type="name").text = name
        for indices in triangles:
            triangle = ET.SubElement(volume, "triangle")
            for index, vertex in enumerate(indices, 1):
                ET.SubElement(triangle, f"v{index}").text = str(vertex)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def verify_layout(objects):
    rectangles = []
    for name, mesh, position in objects:
        bounds = mesh.BoundBox
        rectangle = (position[0] - 3.0, position[1] - 3.0,
                     position[0] + bounds.XLength + 3.0, position[1] + bounds.YLength + 3.0)
        if rectangle[0] < 0 or rectangle[1] < 0 or rectangle[2] > 250 or rectangle[3] > 210:
            raise ValueError(f"{name}: outside MK4S bed including brim: {rectangle}")
        for other_name, other in rectangles:
            if min(rectangle[2], other[2]) > max(rectangle[0], other[0]) and \
                    min(rectangle[3], other[3]) > max(rectangle[1], other[1]):
                raise ValueError(f"Print footprints or brims overlap: {name}, {other_name}")
        rectangles.append((name, rectangle))


def export(amf_dir):
    source = Path(__file__).resolve().parent
    root = source.parent
    stl_dir = root / "print" / "stl"
    report_dir = root / "reports"
    for directory in (stl_dir, report_dir, amf_dir):
        directory.mkdir(parents=True, exist_ok=True)
    model = runpy.run_path(str(source / "lahar.FCMacro"))
    report = validate_model(model)
    document = model["doc"]
    print_meshes = {}
    report["parts"] = {}
    render_objects = []
    for obj in document.Objects:
        assembly_mesh = checked_mesh(obj.Shape)
        points, triangles = assembly_mesh.Topology
        render_objects.append({
            "name": obj.Name, "role": obj.Role, "color": [float(value) for value in obj.DisplayColor.split(",")],
            "vertices": [list(point) for point in points], "triangles": triangles,
        })
        if obj.Name == "Trimaran_Body":
            exterior = checked_mesh(obj.Shape.Solids[0].OuterShell)
            exterior_points, exterior_triangles = exterior.Topology
            render_objects[-1]["exterior_vertices"] = [list(point) for point in exterior_points]
            render_objects[-1]["exterior_triangles"] = exterior_triangles
        if obj.Name not in model["parts"]:
            continue
        shape = obj.Shape.copy()
        shape.rotate(Vector(0, 0, 0), Vector(1, 0, 0), obj.PrintRotationX)
        if hasattr(obj, "PrintRotationY"):
            shape.rotate(Vector(0, 0, 0), Vector(0, 1, 0), obj.PrintRotationY)
        mesh = checked_mesh(shape)
        bounds = mesh.BoundBox
        mesh.translate(-bounds.XMin, -bounds.YMin, -bounds.ZMin)
        mesh.write(str(stl_dir / f"{obj.Name}.stl"))
        print_meshes[obj.Name] = mesh
        bounds = mesh.BoundBox
        report["parts"][obj.Name] = {
            "job": obj.PrintJob, "triangles": mesh.CountFacets,
            "volume_mm3": obj.Shape.Volume,
            "centroid_mm": list(obj.Shape.Solids[0].CenterOfMass),
            "print_bounds_mm": [bounds.XLength, bounds.YLength, bounds.ZLength],
        }
        print(f"{obj.Name}: {bounds.XLength:.2f} x {bounds.YLength:.2f} x {bounds.ZLength:.2f}; manifold")
    for job, placements in LAYOUTS.items():
        objects = [(name, print_meshes[name], position) for name, position in placements.items()]
        if set(placements) != {name for name, obj in model["parts"].items() if obj.PrintJob == job}:
            raise ValueError(f"Incomplete job layout: {job}")
        verify_layout(objects)
        write_amf(amf_dir / f"Lahar_v2_{job}.amf", objects)
    engineering_input = {name: value for name, value in model.items()
                         if name.isupper() and isinstance(value, (int, float, list, tuple))}
    engineering_input["parts"] = report["parts"]
    engineering_input["hulls"] = {}
    engineering_input["deck_points"] = [list(point) for edge in model["deck_edges"]
                                        for point in edge.discretize(Deflection=0.05)]
    engineering_input["mesh_deflection_mm"] = 0.04
    for name, envelope in model["envelopes"].items():
        mesh = checked_mesh(envelope)
        if abs(mesh.Volume - envelope.Volume) / envelope.Volume > 0.002:
            raise ValueError(f"{name}: hydrostatic mesh volume differs from CAD")
        points, triangles = mesh.Topology
        engineering_input["hulls"][name] = {"vertices": [list(point) for point in points], "triangles": triangles}
    (amf_dir / "hydrostatics-input.json").write_text(json.dumps(engineering_input), encoding="utf-8")
    document.saveAs(str(source / "Lahar_v2.FCStd"))
    boat_objects = [obj for obj in document.Objects if obj.Name != "Hardware_Fit_Coupon"]
    Part.export(boat_objects, str(source / "Lahar_v2.step"))
    saved_name = document.Name
    App.closeDocument(saved_name)
    reopened = App.openDocument(str(source / "Lahar_v2.FCStd"))
    if len(reopened.Objects) != len(render_objects):
        raise ValueError("FreeCAD file round-trip lost objects")
    App.closeDocument(reopened.Name)
    (report_dir / "cad-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (amf_dir / "render-meshes.json").write_text(json.dumps(render_objects), encoding="utf-8")
    print("PASS: native FreeCAD round-trip, all STL manifolds, bed layouts, steering clearance")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amf-dir", type=Path, required=True)
    export(parser.parse_args().amf_dir)