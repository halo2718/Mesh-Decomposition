import os
import numpy as np

src = "./assets/venusv.ply"

def read(src):
    vertices = []
    faces    = []
    meta     = {}
    state    = 'header'
    cnt = 0
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

v, f, meta = read(src)
print(v)
print(f)
print(meta)