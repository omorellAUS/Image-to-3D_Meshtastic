"""
Free Image-to-3D — Gradio frontend
"""

import sys
from pathlib import Path

import gradio as gr
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.processor import process_image


def run_pipeline(
    input_image,
    remove_bg: bool,
    foreground_ratio: float,
    mc_resolution: int,
):
    if input_image is None:
        raise gr.Error("Please upload an image first.")

    if not isinstance(input_image, Image.Image):
        input_image = Image.fromarray(input_image)

    processed, paths = process_image(
        input_image,
        remove_bg=remove_bg,
        foreground_ratio=foreground_ratio,
        mc_resolution=int(mc_resolution),
        formats=("glb", "obj", "stl", "ply"),
    )

    return (
        processed,
        paths.get("glb"),
        paths.get("obj"),
        paths.get("stl"),
        paths.get("ply"),
    )


def build_ui():
    with gr.Blocks(title="Free Image-to-3D", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # Free Image-to-3D
            Upload a photo of a real object. The app removes the background, runs **TripoSR**, and gives you a downloadable 3D mesh.

            **Tips**
            - Use a clear, well-lit photo of a single object
            - White or simple backgrounds work best
            - Higher resolution = more detail (slower)
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="Upload image",
                    type="pil",
                    image_mode="RGBA",
                    height=320,
                )
                remove_bg = gr.Checkbox(label="Remove background", value=True)
                foreground_ratio = gr.Slider(
                    minimum=0.5,
                    maximum=1.0,
                    value=0.85,
                    step=0.05,
                    label="Foreground ratio (how tightly to crop)",
                )
                mc_resolution = gr.Slider(
                    minimum=64,
                    maximum=320,
                    value=256,
                    step=32,
                    label="Mesh resolution (higher = more detail)",
                )
                submit = gr.Button("Generate 3D", variant="primary")

            with gr.Column(scale=1):
                processed_image = gr.Image(label="Processed input", interactive=False)
                model_3d = gr.Model3D(label="3D Preview (GLB)", clear_color=[0.0, 0.0, 0.0, 0.0])

        with gr.Row():
            glb_file = gr.File(label="Download GLB")
            obj_file = gr.File(label="Download OBJ")
            stl_file = gr.File(label="Download STL")
            ply_file = gr.File(label="Download PLY")

        submit.click(
            fn=run_pipeline,
            inputs=[input_image, remove_bg, foreground_ratio, mc_resolution],
            outputs=[processed_image, model_3d, glb_file, obj_file, stl_file, ply_file],
        )

        gr.Markdown(
            """
            ---
            Open-source · MIT · Powered by TripoSR
            """
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.queue(max_size=1)
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
