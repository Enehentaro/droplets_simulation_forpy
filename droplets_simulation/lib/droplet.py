import numpy as np
import random

droplet_dtype = np.dtype([
    ("position", "f8", (3,)),
    ("velocity", "f8", (3,)),
    ("radius", "f8")
])
"""飛沫構造化データ型
    飛沫の変数をまとめる
    必要があれば適宜追加
"""

def get_dropletArray(droplets:int,dropIniPlace:np.ndarray,dropIniRad:np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        droplets (int): the number of droplets

    Returns:
        np.ndarray: ndarray of droplet
    """
    array = np.zeros(droplets, dtype = droplet_dtype)

    array["position"] = dropIniPlace
    array["radius"] = dropIniRad

    return array

def calc_dropIniPlace(num_droplets:int,dropSetPlace:np.ndarray) -> np.ndarray:
    min_dropSetPlace = dropSetPlace[0:3] - 0.5*dropSetPlace[3:6]
    max_dropSetPlace = dropSetPlace[0:3] + 0.5*dropSetPlace[3:6]

    dropIniPlace = np.random.uniform(min_dropSetPlace, max_dropSetPlace, (num_droplets,3))

    print("min_dropSetPlace =", min_dropSetPlace)
    print("max_dropSetPlace =", max_dropSetPlace)

    return dropIniPlace

    
def read_dropIniRadius(num_droplets:int) -> np.ndarray:
    IniRad_ratio = np.loadtxt('../data/initialRadius_coughing.txt', delimiter=",", skiprows=1, dtype='float')
    IniRad = IniRad_ratio[:,0]*1.e-6
    ratio = IniRad_ratio[:,1]
    random.seed(0)
    dropIniRad = random.choices(IniRad, k = num_droplets, weights = ratio)

    print("initialRadius_Distribution")
    for i in IniRad:
        print('%e [m] :' % i, dropIniRad.count(i))

    return np.array(dropIniRad)

def output_dropVTK(num_droplets:int,dGroup:np.ndarray):
    from lib.SimpleVtk import SimpleVtkUnstructuredGrid
    output = SimpleVtkUnstructuredGrid()
    cell_types = np.ones(num_droplets, dtype = np.int64)
    offsets = np.arange(num_droplets, dtype = np.int64)
    cell2node = np.arange(num_droplets, dtype = np.int64)
    output.set_points(dGroup["position"])
    output.set_cells(offsets, cell2node, cell_types)
    output.add_field_cell_data("radius", dGroup["radius"], "scalar")
    output.make_grid()
    output.write_out("../vtk/drop.vtk")

if __name__ == '__main__':
    from setting_reader import read_setting, read_dropSetPlace
    droplet_setting, flow_setting = read_setting("../../case")
    dropSetPlace = read_dropSetPlace("../../case")
    dropIniRadius = read_dropIniRadius(droplet_setting["num_droplets"])
    dropIniPlace = calc_dropIniPlace(droplet_setting["num_droplets"],dropSetPlace)
    dGroup = get_dropletArray(droplet_setting["num_droplets"], dropIniPlace, dropIniRadius)

    output_dropVTK(droplet_setting["num_droplets"],dGroup)
