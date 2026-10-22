"""
Swappable model loader.
Automatically searches for TripoSR.
"""

import os
import sys
import torch
from pathlib import Path
from typing import Optional


def find_triposr():
    """Search common locations for the TripoSR repo."""
    candidates = [
        Path(__file__).resolve().parent.parent.parent / "TripoSR",
        Path.cwd() / "TripoSR",
        Path.home() / "TripoSR",
        Path("C:/TripoSR"),
        Path("C:/Users") / os.environ.get("USERNAME", "") / "TripoSR",
    ]
    for path in candidates:
        if (path / "tsr").exists():
            return str(path)
    return None


class BaseImageTo3D:
    def generate(self, image, mc_resolution: int = 256):
        raise NotImplementedError


class TripoSRModel(BaseImageTo3D):
    def __init__(self, device: Optional[str] = None):
        if device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.device = device

        triposr_path = find_triposr()
        if triposr_path and triposr_path not in sys.path:
            sys.path.insert(0, triposr_path)

        try:
            from tsr.system import TSR
        except ImportError as e:
            raise ImportError(
                "Could not import 'tsr' from TripoSR.\n"
                "Place the TripoSR folder inside this project or set it up via start.bat."
            ) from e

        print(f"Loading TripoSR on {self.device} ...")
        self.model = TSR.from_pretrained(
            "stabilityai/TripoSR",
            config_name="config.yaml",
            weight_name="model.ckpt",
        )
        self.model.renderer.set_chunk_size(8192)
        self.model.to(self.device)
        self.model.eval()
        print("TripoSR ready.")

    @torch.no_grad()
    def generate(self, image, mc_resolution: int = 256):
        scene_codes = self.model([image], device=self.device)
        mesh = self.model.extract_mesh(
            scene_codes, has_vertex_color=True, resolution=mc_resolution
        )[0]
        return mesh


def get_model(model_name: str = "triposr", device: Optional[str] = None):
    name = model_name.lower()
    if name == "triposr":
        return TripoSRModel(device=device)
    else:
        raise ValueError(f"Unknown model: {model_name}. Available: triposr")
