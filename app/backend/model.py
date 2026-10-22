"""
Swappable model loader.
Currently implements TripoSR.
"""

import torch
from typing import Optional


class BaseImageTo3D:
    def generate(self, image, mc_resolution: int = 256):
        raise NotImplementedError


class TripoSRModel(BaseImageTo3D):
    def __init__(self, device: Optional[str] = None):
        if device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.device = device

        try:
            from tsr.system import TSR
        except ImportError as e:
            raise ImportError(
                "Could not import 'tsr'. Make sure the TripoSR repository is on your PYTHONPATH."
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
