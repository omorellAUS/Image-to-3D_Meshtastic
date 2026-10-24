"""
Image preprocessing, mesh generation, and export helpers.
"""

import os
import tempfile
import traceback
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image
import trimesh

from .model import get_model


_rembg_session = None


def get_rembg_session():
    global _rembg_session
    if _rembg_session is None:
        try:
            import rembg
            _rembg_session = rembg.new_session()
        except Exception as e:
            print(f"rembg session failed: {e}")
            _rembg_session = None
    return _rembg_session


def fill_background(image: Image.Image) -> Image.Image:
    arr = np.array(image).astype(np.float32) / 255.0
    if arr.shape[-1] == 4:
        rgb = arr[:, :, :3] * arr[:, :, 3:4] + (1 - arr[:, :, 3:4]) * 0.5
    else:
        rgb = arr[:, :, :3]
    return Image.fromarray((rgb * 255.0).astype(np.uint8))


def _has_transparency(image: Image.Image) -> bool:
    """True if the image has an alpha channel that is not fully opaque."""
    if image.mode != "RGBA":
        return False
    alpha_min, _ = image.getchannel("A").getextrema()
    return alpha_min < 255


def remove_background(image: Image.Image) -> Optional[Image.Image]:
    """Run rembg on the image. Returns an RGBA cut-out, or None on failure."""
    try:
        import rembg
        session = get_rembg_session()
        return rembg.remove(image.convert("RGB"), session=session)
    except Exception as e:
        print(
            f"WARNING: background removal (rembg) failed: {e}\n"
            "WARNING: continuing with the ORIGINAL image - the background was "
            "NOT removed and the object was NOT re-framed (foreground ratio "
            "ignored). Mesh quality may be poor."
        )
        traceback.print_exc()
        return None


def frame_foreground(image: Image.Image, foreground_ratio: float) -> Image.Image:
    """Crop/pad an RGBA image around its alpha mask, then fill the background."""
    from tsr.utils import resize_foreground

    image = resize_foreground(image, foreground_ratio)
    return fill_background(image)


def preprocess(
    input_image: Image.Image,
    remove_bg: bool = True,
    foreground_ratio: float = 0.85,
) -> Image.Image:
    image = input_image
    if image.mode in ("LA", "PA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        image = image.convert("RGBA")

    has_mask = False
    if remove_bg:
        cutout = remove_background(image)
        if cutout is not None:
            image = cutout
            has_mask = True
        # On failure, fall through with the original image (see warning).

    # Frame the object whenever we have an alpha mask: either the rembg
    # cut-out, or an input that already has a transparent background
    # (e.g. remove_bg=False with a pre-cut PNG). resize_foreground needs RGBA.
    if has_mask or _has_transparency(image):
        try:
            return frame_foreground(image, foreground_ratio)
        except Exception as e:
            print(
                f"WARNING: framing the foreground failed: {e}\n"
                "WARNING: continuing with the original image (not re-framed)."
            )
            traceback.print_exc()
            image = input_image

    # No usable alpha mask: keep the image as plain RGB, not re-framed.
    if image.mode == "RGBA":
        return fill_background(image)
    return image.convert("RGB")


def generate_mesh(
    image: Image.Image,
    mc_resolution: int = 384,
    model_name: str = "triposr",
    smooth: bool = True,
    smooth_iterations: int = 5,
) -> trimesh.Trimesh:
    model = get_model(model_name)
    mesh = model.generate(image, mc_resolution=mc_resolution)

    mesh = mesh.copy()
    mesh.remove_unreferenced_vertices()
    if hasattr(mesh, "remove_degenerate_faces"):
        mesh.remove_degenerate_faces()
    elif hasattr(mesh, "nondegenerate_faces"):
        mesh.update_faces(mesh.nondegenerate_faces())

    if smooth and smooth_iterations > 0:
        try:
            trimesh.smoothing.filter_laplacian(mesh, iterations=smooth_iterations)
        except Exception as e:
            print(f"Smoothing failed: {e}")

    mesh.fix_normals()
    return mesh


def export_meshes(
    mesh: trimesh.Trimesh,
    formats: List[str] = ("glb", "obj", "stl", "ply"),
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
    mc_resolution: int = 384,
    formats: Tuple[str, ...] = ("glb", "obj", "stl", "ply"),
) -> Tuple[Image.Image, dict]:
    processed = preprocess(input_image, remove_bg, foreground_ratio)
    mesh = generate_mesh(processed, mc_resolution, smooth=True, smooth_iterations=5)
    paths = export_meshes(mesh, list(formats))
    return processed, paths