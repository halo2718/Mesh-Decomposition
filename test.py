from concurrent.futures import process
import trimesh

mesh = trimesh.load_mesh("./assets/bunny.ply")
print(mesh.vertices)
print(mesh.faces)
print(mesh.face_normals)

print(mesh.face_adjacency)