# Free Image-to-3D

Open-source local image-to-3D web app. Upload a photo of an object and get a downloadable 3D mesh (GLB / OBJ / STL).

Powered by **TripoSR**. The model backend is written so it can later be swapped for other models.

## Features

- Upload an image
- Automatic background removal
- Generate 3D mesh with TripoSR
- Interactive 3D preview in the browser
- Download GLB, OBJ, and STL
- Resolution / quality controls
- Runs fully locally on your GPU

## Requirements

- Python 3.10+
- NVIDIA GPU with 6–8 GB+ VRAM
- CUDA installed

## Project Structure
Image-to-3D_Meshtastic/
├── app/
│   ├── main.py
│   └── backend/
│       ├── model.py
│       ├── processor.py
│       └── api.py
├── models/
├── examples/
├── requirements.txt

## License

MIT


├── Dockerfile
├── LICENSE
└── README.md
