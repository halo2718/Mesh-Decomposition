import os
import numpy as np

src = "./assets/venusv.obj"

def read(src):
    vertices = []
    normals  = []
    faces    = []
    with open(src, 'r') as F:
        line = F.readline()
        while line:
            content = line.split(" ")
            if content[0] == 'v':
                print(content)
                vertices.append([float(content[2]), float(content[3]), float(content[4])])
            elif content[0] == 'vn':
                normals.append([float(content[2]), float(content[3]), float(content[4])])
            elif content[0] == 'f':
                v_c = [int(item.split("//")[0]) for item in content if item != "f"]
                v_n = [int(item.split("//")[1]) for item in content if item != "f"]
                faces.append([v_c, v_n])
            else:
                pass
            line = F.readline()
            
    return vertices, normals, faces

v, n, f = read(src)
print(v)
print(n)
print(f)