# Free Image-to-3D

Open-source local image-to-3D tool. Upload a photo (or later multiple photos) and get a downloadable mesh (GLB, OBJ, STL, PLY).

**Current status: Alpha (v0.1)**  
Single-image mode with TripoSR is working. Multi-mode / higher-quality backends are planned for the beta.

## Modes

| Mode | Model | What it does | VRAM | Speed | Quality | Status |
|------|-------|--------------|------|-------|---------|--------|
| Single image – Fast | TripoSR | One photo → mesh | Low (~6 GB) | Fast | Good for quick results | **Working (Alpha)** |
| Single image – Detailed | TRELLIS (quantized/GGUF if needed) | One photo → higher-quality mesh + better materials | Medium | Medium | Better geometry | Planned (Beta) |
| Multi-image | TRELLIS multi-view | Several photos of the same object → more accurate shape | Higher | Slower | Best shape accuracy | Planned (Beta) |

## Features (Alpha)

- Upload a single image
- Automatic background removal (rembg)
- Generate a 3D mesh with TripoSR
- In-browser 3D preview
- Download GLB / OBJ / STL / PLY
- Simple resolution / quality controls
- Windows launcher (`start.bat`) that sets up a virtual environment and dependencies

## Requirements

- Windows 10 / 11 (primary target)
- Python 3.10 or 3.11 (add to PATH during install)
- NVIDIA GPU with CUDA (RTX 3060 12 GB or better recommended)
- ~6–8 GB free VRAM for the current TripoSR path

## Quick start (Windows)

1. Install Python 3.10 or 3.11 from [python.org](https://www.python.org/downloads/) and check **Add python.exe to PATH**.
2. Download or clone this repo.
3. Double-click `start.bat`.
   - It creates a virtual environment
   - Installs dependencies
   - Clones TripoSR if needed
   - Starts the Gradio app at http://localhost:7860

First run takes longer while packages and the TripoSR weights download.

## Manual start (optional)

```bat
python -m venv venv

Project structure

├── app/
│   ├── main.py                 # Gradio UI
│   └── backend/
│       ├── model.py            # Model loading (TripoSR)
│       └── processor.py        # Preprocess, generate, export
├── start.bat                   # Windows launcher
├── requirements.txt
├── README.md
└── LICENSE

RoadmapAlpha (current)
 Single-image TripoSR pipeline
 Background removal
 Multi-format export (GLB, OBJ, STL, PLY)
 Windows launcher
 Basic Gradio UI with preview

Beta (planned)
 Mode selector: Fast / Detailed
 TRELLIS single-image (Detailed) path
 Multi-image upload + TRELLIS multi-view
 Low-VRAM options tuned for 12 GB cards
 Better quality controls (resolution, sampling steps)
 Optional model download on first use

Notes
TripoSR is single-image only and relatively fast/low-VRAM.
TRELLIS (and especially TRELLIS.2) gives higher quality and supports multi-view, but needs more VRAM and setup. These will be added in the beta while keeping the current Fast path as the reliable fallback.
This is an open-source MIT project. Model weights are downloaded separately on first use.

License
MIT

MIT License

Copyright (c) 2026 Oliver Ross Morell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.ok 
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
