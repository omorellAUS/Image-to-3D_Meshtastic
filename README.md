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
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

## Project structure

```text
├── app/
│   ├── main.py                 # Gradio UI
│   └── backend/
│       ├── model.py            # Model loading (TripoSR)
│       └── processor.py        # Preprocess, generate, export
├── start.bat                   # Windows launcher
├── requirements.txt
├── README.md
└── LICENSE
```

## Roadmap

### Alpha (current)

- [x] Single-image TripoSR pipeline
- [x] Background removal
- [x] Multi-format export (GLB, OBJ, STL, PLY)
- [x] Windows launcher
- [x] Basic Gradio UI with preview

### Beta (planned)

- [ ] Mode selector: Fast / Detailed
- [ ] TRELLIS single-image (Detailed) path
- [ ] Multi-image upload + TRELLIS multi-view
- [ ] Low-VRAM options tuned for 12 GB cards
- [ ] Better quality controls (resolution, sampling steps)
- [ ] Optional model download on first use

## Notes

- TripoSR is single-image only and relatively fast/low-VRAM.
- TRELLIS (and especially TRELLIS.2) gives higher quality and supports multi-view, but needs more VRAM and setup. These will be added in the beta while keeping the current Fast path as the reliable fallback.
- This is an open-source MIT project. Model weights are downloaded separately on first use.

## License

MIT. See [LICENSE](LICENSE).
