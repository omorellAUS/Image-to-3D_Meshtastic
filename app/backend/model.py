"""
Model loader for TRELLIS (best free quality).
Falls back gracefully if TRELLIS is not available.
"""

import sys
from pathlib import Path
from typing import Optional

import torch
from PIL import Image

# Make TRELLIS importable if it sits next to the project
ROOT = Path(__file__).resolve().parent.parent.parent
TRELLIS_PATH = ROOT / "TRELLIS"
if TRELLIS_PATH.exists() and str(TRELLIS_PATH) not in sys.path:
    sys.path.insert(0, str(TRELLIS_PATH))

_pipeline = None


def get_pipeline(device: str = "cuda"):
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    try:
        from trellis.pipelines import TrellisImageTo3DPipeline
    except ImportError as e:
        raise ImportError(
            "TRELLIS not found. Clone https://github.com/microsoft/TRELLIS "
            "into the project folder and install its dependencies."
        ) from e

    print("Loading TRELLIS on", device, "...")
    pipe = TrellisImageTo3DPipeline.from_pretrained("microsoft/TRELLIS-image-large")
    pipe.to(device)
    _pipeline = pipe
    print("TRELLIS ready.")
    return _pipeline


def generate_trellis_mesh(
    image: Image.Image,
    seed: int = 42,
    simplify: float = 0.95,
    texture_size: int = 1024,
) -> "trimesh.Trimesh":
    import trimesh
    from trellis.utils import postprocessing_utils

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    pipe = get_pipeline()
    outputs = pipe.run(
        image,
        seed=seed,
        formats=["mesh", "gaussian"],
        preprocess_image=True,
    )

    # Convert to clean trimesh via official post-processor
    glb_mesh = postprocessing_utils.to_glb(
        outputs["gaussian"][0],
        outputs["mesh"][0],
        simplify=simplify,
        texture_size=texture_size,
        fill_holes=True,
        verbose=False,
    )

    # postprocessing_utils.to_glb already returns a trimesh.Trimesh
    mesh = glb_mesh if isinstance(glb_mesh, trimesh.Trimesh) else trimesh.load(glb_mesh, file_type="glb")

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return mesh