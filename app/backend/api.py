"""
Optional FastAPI backend.
"""

import io
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from PIL import Image

from .processor import process_image

app = FastAPI(title="Free Image-to-3D API", version="1.0")


@app.get("/")
def root():
    return {"message": "Free Image-to-3D API. POST /generate with an image."}


@app.post("/generate")
async def generate(
    file: UploadFile = File(...),
    remove_bg: bool = Form(True),
    foreground_ratio: float = Form(0.85),
    mc_resolution: int = Form(256),
    format: str = Form("glb"),
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGBA")

    _, paths = process_image(
        image,
        remove_bg=remove_bg,
        foreground_ratio=foreground_ratio,
        mc_resolution=mc_resolution,
        formats=(format,),
    )

    out_path = paths.get(format)
    if not out_path or not Path(out_path).exists():
        return {"error": "Generation failed"}

    media_types = {
        "glb": "model/gltf-binary",
        "obj": "model/obj",
        "stl": "model/stl",
    }
    return FileResponse(
        out_path,
        media_type=media_types.get(format, "application/octet-stream"),
        filename=f"model.{format}",
    )
