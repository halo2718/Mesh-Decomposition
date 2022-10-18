import os
import numpy as np

src = "./assets/elephav.ply"

class Mesh:

    def __init__(self, src) -> None:
        self.src = src
        self.vertices, self.faces, self.meta = self.read_ply(src)
        self.dual_graph = self.generate_dual_graph()

    def read_ply(self, src):
        vertices = []
        faces    = []
        meta     = {}
        state    = 'header'
        with open(src, 'r') as F:
            line = F.readline()
            while line:
                if state == 'header':
                    content = line.strip("\n").split(" ")
                    if content[0] == 'element':
                        meta[content[1]] = int(content[2])
                    elif content[0] == 'end_header':
                        state = 'main'
                    else:
                        pass
                elif state == 'main':
                    for i in range(meta['vertex']):
                        content = line.strip("\n").split(" ")
                        vertices.append([float(content[0]), float(content[1]), float(content[2])])
                        line = F.readline()
                    for i in range(meta['face']):
                        content = line.strip("\n").split(" ")
                        faces.append([int(content[1]), int(content[2]), int(content[3])])
                        line = F.readline()
                    break
                line = F.readline()
        return vertices, faces, meta
    
    def generate_dual_graph(self):
        dual_graph = []
        for i in range(self.meta['face']):
            cur_face = self.faces[i]
            edge_1 = (cur_face[0], cur_face[1])
            edge_2 = (cur_face[1], cur_face[2])
            edge_3 = (cur_face[2], cur_face[0])
            cur_connection = []
            for j in range(self.meta['face']):
                if i == j:
                    continue
                else:
                    ref_face = self.faces[j]
                    cond1 = edge_1[0] in ref_face and edge_1[1] in ref_face
                    cond2 = edge_2[0] in ref_face and edge_2[1] in ref_face
                    cond3 = edge_3[0] in ref_face and edge_3[1] in ref_face
                    if cond1 or cond2 or cond3:
                        cur_connection.append(j)
            dual_graph.append(cur_connection)
        return dual_graph


if __name__ == '__main__':
    mesh = Mesh("./assets/bunny.ply")
