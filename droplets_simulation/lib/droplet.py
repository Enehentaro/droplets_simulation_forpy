import numpy as np
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support

droplet_dt = np.dtype([
    ("position", "f8", (3,)),
    ("velocity", "f8", (3,)),
    ("radius", "f8")
])
"""飛沫構造型
    飛沫の変数をまとめる
    必要があれば適宜追加
"""

if __name__ == '__main__':
    droplets = 10
    a = np.zeros(droplets, dtype = droplet_dt)

    a["position"] = np.random.rand(droplets,3)
    a["radius"] = np.random.rand(droplets)

    print(a)
