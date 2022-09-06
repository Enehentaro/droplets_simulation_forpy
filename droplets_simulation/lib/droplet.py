import numpy as np
from setting_reader import read_setting, read_dropSetPlace
from SimpleVtk import SimpleVtkUnstructuredGrid

droplet_dtype = np.dtype([
    ("position", "f8", (3,)),
    ("velocity", "f8", (3,)),
    ("radius", "f8")
])
"""飛沫構造化データ型
    飛沫の変数をまとめる
    必要があれば適宜追加
"""

def get_dropletArray(droplets:int,dropIniPlace:np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        droplets (int): the number of droplets

    Returns:
        np.ndarray: ndarray of droplet
    """
    array = np.zeros(droplets, dtype = droplet_dtype)

    array["position"] = dropIniPlace
    array["radius"] = np.random.rand(droplets)

    return array

def calc_dropIniPlace(num_droplets:int,dropSetPlace:np.ndarray) -> np.ndarray:
    min_dropSetPlace = dropSetPlace[0:3] - 0.5*dropSetPlace[3:6]
    max_dropSetPlace = dropSetPlace[0:3] + 0.5*dropSetPlace[3:6]

    dropIniPlace = np.random.uniform(min_dropSetPlace, max_dropSetPlace, (num_droplets,3))

    print("min_dropSetPlace =", min_dropSetPlace)
    print("max_dropSetPlace =", max_dropSetPlace)

    return dropIniPlace

if __name__ == '__main__':
    droplet_setting, flow_setting = read_setting("../../case")
    dropSetPlace = read_dropSetPlace("../../case")
    dropIniPlace = calc_dropIniPlace(droplet_setting["num_droplets"],dropSetPlace)
    dGroup = get_dropletArray(droplet_setting["num_droplets"], dropIniPlace)
    print(dGroup)

    output = SimpleVtkUnstructuredGrid()
    cell_types = np.ones(droplet_setting["num_droplets"], dtype = int)
    offsets = np.arange(droplet_setting["num_droplets"])
    cell2node = np.arange(droplet_setting["num_droplets"])
    output.set_points(dGroup["position"])
    output.set_cells(offsets, cell2node, cell_types)
    output.make_grid()
    output.write_out("drop.vtk")
