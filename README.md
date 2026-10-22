# Free Image-to-3D

Open-source local image-to-3D web app. Upload a photo of an object and get a downloadable 3D mesh (GLB / OBJ / STL).

Powered by **TripoSR** (Stability AI + Tripo AI). The model backend is written so it can later be swapped for TRELLIS or other models.

## Features

- Upload an image
- Automatic background removal (rembg)
- Generate 3D mesh with TripoSR
- Interactive 3D preview in the browser
- Download GLB, OBJ, and STL
- Resolution / quality controls
- Runs fully locally on your GPU

## Requirements

- Python 3.10+
- NVIDIA GPU with ≥ 6–8 GB VRAM (RTX 3060 or better recommended)
- CUDA installed and matching your PyTorch version

## Quick Start

### 1. Clone TripoSR (required)

```bash
git clone https://github.com/VAST-AI-Research/TripoSR.git
cd TripoSR
pip install -r requirements.txt
