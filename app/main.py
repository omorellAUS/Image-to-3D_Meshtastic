"""
Gradio frontend for Free Image-to-3D.
"""

import gradio as gr
from PIL import Image

from backend.processor import process_image


def run_pipeline(image, remove_bg, foreground_ratio, mc_resolution):
    if image is None:
        return None, None, None, None, None, None

    try:
        processed, paths = process_image(
            image,
            remove_bg=remove_bg,
            foreground_ratio=foreground_ratio,
            mc_resolution=int(mc_resolution),
        )
        return (
            processed,
            paths.get("glb"),
            paths.get("glb"),
            paths.get("obj"),
            paths.get("stl"),
            paths.get("ply"),
        )
    except Exception as e:
        print(f"Generation failed: {e}")
        return None, None, None, None, None, None


def build_ui():
    with gr.Blocks(title="Free Image-to-3D") as demo:
        gr.Markdown(
            """
            # Free Image-to-3D
            Upload a photo of a real object. The app removes the background, runs TripoSR, and gives you a downloadable 3D mesh.
            """
        )

        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="pil", label="Upload image")
                remove_bg = gr.Checkbox(value=True, label="Remove background")
                foreground_ratio = gr.Slider(0.5, 1.0, value=0.85, step=0.05, label="Foreground ratio (how tightly to crop)")
                mc_resolution = gr.Slider(128, 512, value=384, step=64, label="Mesh resolution (higher = more detail)")
                generate_btn = gr.Button("Generate 3D", variant="primary")

            with gr.Column():
                processed_output = gr.Image(label="Processed input")
                model_output = gr.Model3D(label="3D Preview (GLB)")
                glb_output = gr.File(label="Download GLB")
                obj_output = gr.File(label="Download OBJ")
                stl_output = gr.File(label="Download STL")
                ply_output = gr.File(label="Download PLY")

        generate_btn.click(
            fn=run_pipeline,
            inputs=[image_input, remove_bg, foreground_ratio, mc_resolution],
            outputs=[processed_output, model_output, glb_output, obj_output, stl_output, ply_output],
        )

        gr.Markdown("Open-source · MIT · Powered by TripoSR")

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)