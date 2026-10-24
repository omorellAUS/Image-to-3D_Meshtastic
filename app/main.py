import sys
from pathlib import Path

# Force project root onto sys.path so "app" imports work when run as a script
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import gradio as gr
from app.backend.processor import process_image


def run_pipeline(
    input_image,
    remove_bg,
    foreground_ratio,
    mc_resolution,
):
    if input_image is None:
        return None, None, None, None, None, None

    processed, paths = process_image(
        input_image,
        remove_bg=remove_bg,
        foreground_ratio=foreground_ratio,
        mc_resolution=int(mc_resolution),
    )

    return (
        processed,                  # Processed input
        paths.get("glb"),           # 3D Preview
        paths.get("glb"),           # Download GLB
        paths.get("obj"),           # Download OBJ
        paths.get("stl"),           # Download STL
        paths.get("ply"),           # Download PLY
    )


with gr.Blocks(title="Free Image-to-3D") as demo:
    gr.Markdown(
        """
        # Free Image-to-3D
        Upload a photo of a real object. The app removes the background, runs TripoSR, and gives you a downloadable 3D mesh.

        **Tips**
        - Use a clear, well-lit photo of a single object
        - White or simple backgrounds work best
        - Higher resolution = more detail (slower)
        """
    )

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload image")
            remove_bg = gr.Checkbox(value=True, label="Remove background")
            foreground_ratio = gr.Slider(
                minimum=0.5,
                maximum=1.0,
                value=0.85,
                step=0.01,
                label="Foreground ratio (how tightly to crop)",
            )
            mc_resolution = gr.Slider(
                minimum=128,
                maximum=512,
                value=256,
                step=32,
                label="Mesh resolution (higher = more detail)",
            )
            generate_btn = gr.Button("Generate 3D", variant="primary")

        with gr.Column():
            processed_image = gr.Image(label="Processed input")
            model_viewer = gr.Model3D(label="3D Preview (GLB)")
            glb_file = gr.File(label="Download GLB")
            obj_file = gr.File(label="Download OBJ")
            stl_file = gr.File(label="Download STL")
            ply_file = gr.File(label="Download PLY")

    generate_btn.click(
        fn=run_pipeline,
        inputs=[input_image, remove_bg, foreground_ratio, mc_resolution],
        outputs=[processed_image, model_viewer, glb_file, obj_file, stl_file, ply_file],
    )

    gr.Markdown("*Open-source · MIT · Powered by TripoSR*")


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)