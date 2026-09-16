"""Run with FreeCAD's Python interpreter to export checked, print-oriented STLs."""

import argparse
from pathlib import Path
import runpy
import xml.etree.ElementTree as ET

import FreeCAD as App
import MeshPart
from FreeCAD import Vector


def make_mesh(shape):
    mesh = MeshPart.meshFromShape(
        Shape=shape, LinearDeflection=0.05, AngularDeflection=0.15,
        Relative=False,
    )
    if not mesh.isSolid():
        raise ValueError("Mesh is not closed")
    return mesh


def write_amf(path, objects):
    root = ET.Element("amf", unit="millimeter", version="1.1")
    for object_id, (name, volumes, position) in enumerate(objects):
        element = ET.SubElement(root, "object", id=str(object_id))
        ET.SubElement(element, "metadata", type="name").text = name
        mesh_element = ET.SubElement(element, "mesh")
        vertices = ET.SubElement(mesh_element, "vertices")
        offset = 0
        for mesh, settings in volumes:
            points, triangles = mesh.Topology
            for point in points:
                vertex = ET.SubElement(vertices, "vertex")
                coordinates = ET.SubElement(vertex, "coordinates")
                for axis, value, shift in zip("xyz", point, position):
                    ET.SubElement(coordinates, axis).text = f"{value + shift:.6f}"
            volume = ET.SubElement(mesh_element, "volume")
            for key, value in settings.items():
                ET.SubElement(volume, "metadata", type=key).text = value
            for indices in triangles:
                triangle = ET.SubElement(volume, "triangle")
                for index, vertex_id in enumerate(indices, 1):
                    ET.SubElement(triangle, f"v{index}").text = str(vertex_id + offset)
            offset += len(points)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export(amf_dir):
    source = Path(__file__).resolve().parent
    output = source.parent / "print" / "stl"
    output.mkdir(parents=True, exist_ok=True)
    model = runpy.run_path(str(source / "lahar.FCMacro"))
    document = model["doc"]
    rotations = {
        "Trimaran_Body": 180,
        "Rudder_Blade": 90,
        "Rudder_Tiller": 0,
        "Vane_Paddle": 90,
        "Vane_Arm": 0,
    }
    meshes = {}
    body_shift = None
    for name, angle in rotations.items():
        shape = document.getObject(name).Shape.copy()
        if not shape.isValid() or len(shape.Solids) != 1:
            raise ValueError(f"{name}: expected one valid solid")
        shape.rotate(Vector(0, 0, 0), Vector(1, 0, 0), angle)
        bounds = shape.BoundBox
        shift = Vector(-bounds.XMin, -bounds.YMin, -bounds.ZMin)
        shape.translate(shift)
        if name == "Trimaran_Body":
            body_shift = shift
        mesh = make_mesh(shape)
        meshes[name] = mesh
        mesh.write(str(output / f"{name}.stl"))
        bounds = mesh.BoundBox
        print(
            f"{name}: {mesh.CountFacets} triangles; "
            f"{bounds.XLength:.2f} x {bounds.YLength:.2f} x "
            f"{bounds.ZLength:.2f} mm; solid"
        )
    amf_dir.mkdir(parents=True, exist_ok=True)
    body_volumes = [(meshes["Trimaran_Body"], {"name": "Trimaran_Body"})]
    for name in ("ama_p", "ama_s"):
        shape = model[name].copy()
        shape.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
        shape.translate(body_shift)
        body_volumes.append((make_mesh(shape), {
            "name": f"{name}_zero_infill",
            "slic3r.modifier": "1",
            "slic3r.fill_density": "0%",
        }))
    body_bounds = meshes["Trimaran_Body"].BoundBox
    write_amf(amf_dir / "Lahar_Body.amf", [(
        "Lahar_Body", body_volumes,
        ((250 - body_bounds.XLength) / 2, (220 - body_bounds.YLength) / 2, 0),
    )])
    placements = {
        "Vane_Paddle": (30, 30, 0),
        "Rudder_Blade": (150, 30, 0),
        "Rudder_Tiller": (150, 100, 0),
        "Vane_Arm": (180, 100, 0),
    }
    write_amf(amf_dir / "Lahar_Steering.amf", [
        (name, [(meshes[name], {"name": name})], position)
        for name, position in placements.items()
    ])
    App.closeDocument(document.Name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amf-dir", required=True, type=Path)
    export(parser.parse_args().amf_dir)