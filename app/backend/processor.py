"""
Image preprocessing, mesh generation, and export helpers.
"""

import os
import tempfile
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image
import trimesh

from .model import get_model


_rembg_session = None


def get_rembg_session():
    global _rembg_session
    if _rembg_session is None:
        import rembg
        _rembg_session = rembg.new_session()
    return _rembg_session


def fill_background(image: Image.Image) -> Image.Image:
    arr = np.array(image).astype(np.float32) / 255.0
    if arr.shape[-1] == 4:
        rgb = arr[:, :, :3] * arr[:, :, 3:4] + (1 - arr[:, :, 3:4]) * 0.5
    else:
        rgb = arr[:, :, :3]
    return Image.fromarray((rgb * 255.0).astype(np.uint8))


def preprocess(
    input_image: Image.Image,
    remove_bg: bool = True,
    foreground_ratio: float = 0.85,
) -> Image.Image:
    if remove_bg:
        import rembg
        session = get_rembg_session()
        image = input_image.convert("RGB")
        image = rembg.remove(image, session=session)
        from tsr.utils import resize_foreground
        image = resize_foreground(image, foreground_ratio)
        image = fill_background(image)
    else:
        image = input_image
        if image.mode == "RGBA":
            image = fill_background(image)
        else:
            image = image.convert("RGB")
    return image


def generate_mesh(
    image: Image.Image,
    mc_resolution: int = 256,
    model_name: str = "triposr",
) -> trimesh.Trimesh:
    model = get_model(model_name)
    mesh = model.generate(image, mc_resolution=mc_resolution)

    mesh = mesh.copy()
    mesh.remove_unreferenced_vertices()
    mesh.remove_degenerate_faces()
    mesh.fix_normals()
    return mesh


def export_meshes(
    mesh: trimesh.Trimesh,
    formats: List[str] = ("glb", "obj", "stl"),
    output_dir: Optional[str] = None,
) -> dict:
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="mesh_")
    os.makedirs(output_dir, exist_ok=True)

    paths = {}
    for fmt in formats:
        path = os.path.join(output_dir, f"model.{fmt}")
        mesh.export(path)
        paths[fmt] = path
    return paths


def process_image(
    input_image: Image.Image,
    remove_bg: bool = True,
    foreground_ratio: float = 0.85,
    mc_resolution: int = 256,
    formats: Tuple[str, ...] = ("glb", "obj", "stl"),
) -> Tuple[Image.Image, dict]:
    processed = preprocess(input_image, remove_bg, foreground_ratio)
    mesh = generate_mesh(processed, mc_resolution)
    paths = export_meshes(mesh, list(formats))
    return processed, paths
