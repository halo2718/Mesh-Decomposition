import numpy as np
import trimesh

src = "./assets/elephav.ply"

class Mesh:

    def __init__(self, src, convex_eta=0.3, delta=0.5) -> None:
        self.src = src
        self.mesh = trimesh.load_mesh("./assets/test.ply")
        
        self.verts = self.mesh.vertices
        self.norms = self.mesh.face_normals
        self.faces = self.mesh.faces
        
        print(self.faces)

        self.face_adj_pairs = self.mesh.face_adjacency
        self.face_adj_conve = self.mesh.face_adjacency_convex
        self.face_adj_edges = self.mesh.face_adjacency_edges
        self.face_adj_unsha = self.mesh.face_adjacency_unshared

        self.dual_graph_size = self.faces.shape[0]
        self.convex_eta      = convex_eta
        self.delta           = delta

        self.generate_dual_graph()

        
    def generate_dual_graph(self):
        angular_dist_list  = []
        geodesic_dist_list = []
        for idx, (face_idx_a, face_idx_b) in enumerate(self.face_adj_pairs):
            angular_dist = self.calc_angular_dist(idx, face_idx_a, face_idx_b)
            angular_dist_list.append(angular_dist)
            pass

    def calc_angular_dist(self, idx, face_idx_a, face_idx_b):
        norm_a, norm_b = self.norms[face_idx_a], self.norms[face_idx_b]
        convex         = self.face_adj_conve[idx]
        # Note that the TRIMESH has already forced the length of normals to be 1.
        angular_dist = self.eta * (1.0 - np.dot(norm_a, norm_b)) if convex else 1.0 - np.dot(norm_a, norm_b)
        return angular_dist

    def calc_geodesic_dist(self, idx):
        verts_on_edge = self.verts[self.face_adj_edges[idx]]
        verts_unshare = self.verts[self.face_adj_unsha[idx]]
        origin = np.array(verts_on_edge[1])
        edge_coord = np.array(verts_on_edge) - origin
        unsh_coord = np.array(verts_unshare) - origin
        axis   = np.array(verts_on_edge[0]) - origin
        axis   = axis / np.linalg.norm(axis)
        edge_a = unsh_coord[0] - edge_coord[1]
        edge_b = unsh_coord[1] - edge_coord[1]
        norm_a, norm_b = self.norms[self.face_adj_pairs[idx]]
        convex = np.dot(norm_a, edge_b) < 0
        angle = np.arccos(np.dot(norm_a, norm_b))
        angle = angle if convex else -angle
        dir_a = np.cross(axis, edge_a)
        dir_b = np.cross(axis, edge_b)
        plane_to_rotate = 0 if np.dot(dir_a, norm_a) > 0 else 1
        xn, yn, zn = axis[0], axis[1], axis[2]
        x0, y0, z0 = edge_coord[0][0], edge_coord[0][1], edge_coord[0][2]
        M = xn * x0 + yn * y0 + zn * z0
        c = np.cos(angle)
        s = np.sin(angle)
        K = 1 - c
        rot = np.array(
            [
                [xn * xn * K + c, xn * yn * K - zn * s, xn * zn * K + yn * s, (x0 - xn * M) * K + (zn * y0 - yn * z0) * s],
                [xn * yn * K + zn * s, yn * yn * K + c, yn * zn * K - xn * s, (y0 - yn * M) * K + (xn * z0 - zn * x0) * s],
                [xn * zn * K - yn * s, yn * zn * K + xn * s, zn * zn * K + c, (z0 - zn * M) * K + (yn * x0 - xn * y0) * s],
                [0, 0, 0, 1]
            ]
        )
        plane_a = [edge_coord[0], edge_coord[1], unsh_coord[0]]
        plane_b = [edge_coord[0], edge_coord[1], unsh_coord[1]]
        center_a = sum(plane_a) / len(plane_a)
        center_b = sum(plane_b) / len(plane_b)
        if plane_to_rotate == 0:
            homo_coord = np.array([center_a[0], center_a[1], center_a[2], 1.0]) 
            center_a_rot = np.dot(rot, homo_coord)[:3]
            geodesic_dist = np.linalg.norm(center_a_rot - center_b)
        else:
            homo_coord = np.array([center_b[0], center_b[1], center_b[2], 1.0]) 
            center_b_rot = np.dot(rot, homo_coord)[:3]
            geodesic_dist = np.linalg.norm(center_b_rot - center_a)
        return geodesic_dist

if __name__ == '__main__':
    mesh = Mesh("./assets/bunny.ply")
