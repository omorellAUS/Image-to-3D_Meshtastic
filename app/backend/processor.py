def generate_mesh(
    image: Image.Image,
    mc_resolution: int = 256,          # ignored for TRELLIS, kept for UI compatibility
    model_name: str = "trellis",
) -> trimesh.Trimesh:
    from app.backend.model import generate_trellis_mesh

    mesh = generate_trellis_mesh(image, seed=42, simplify=0.95, texture_size=1024)

    mesh = mesh.copy()
    mesh.remove_unreferenced_vertices()

    if hasattr(mesh, "remove_degenerate_faces"):
        mesh.remove_degenerate_faces()
    elif hasattr(mesh, "nondegenerate_faces"):
        mesh.update_faces(mesh.nondegenerate_faces())

    # Drop small disconnected pieces (common residual planes)
    components = mesh.split(only_watertight=False)
    if len(components) > 1:
        mesh = max(components, key=lambda m: len(m.faces))

    mesh.fix_normals()
    return mesh