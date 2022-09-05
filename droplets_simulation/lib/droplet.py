import numpy as np
import pprint
from setting_reader import read_setting, read_dropIniPlace

droplet_dtype = np.dtype([
    ("position", "f8", (3,)),
    ("velocity", "f8", (3,)),
    ("radius", "f8")
])
"""飛沫構造化データ型
    飛沫の変数をまとめる
    必要があれば適宜追加
"""

def get_dropletArray(droplets:int) -> np.ndarray:
    """_summary_

    Args:
        droplets (int): the number of droplets

    Returns:
        np.ndarray: ndarray of droplet
    """
    array = np.zeros(droplets, dtype = droplet_dtype)

    array["position"] = np.random.rand(droplets,3)
    array["radius"] = np.random.rand(droplets)

    return array

def calc_dropIniPlace(num_droplets:int,dropSetPlace:np.ndarray):
    min_dropSetPlace = dropSetPlace[0:3] - 0.5*dropSetPlace[3:6]
    max_dropSetPlace = dropSetPlace[0:3] + 0.5*dropSetPlace[3:6]
    
    num_dropOnEdge = 1
    while((num_dropOnEdge+1)**3 <= num_droplets):
        num_dropOnEdge += 1

    drop_xEdge = np.linspace(min_dropSetPlace[0],max_dropSetPlace[0],num_dropOnEdge)
    drop_yEdge = np.linspace(min_dropSetPlace[1],max_dropSetPlace[1],num_dropOnEdge)
    drop_zEdge = np.linspace(min_dropSetPlace[2],max_dropSetPlace[2],num_dropOnEdge)

    drop_xEdge, drop_yEdge, drop_zEdge = np.meshgrid(drop_xEdge, drop_yEdge, drop_zEdge)
    dropIniPlace = np.c_[drop_xEdge.flatten(), drop_yEdge.flatten(), drop_zEdge.flatten()]

    print("min_dropSetPlace = ", min_dropSetPlace)
    print("min_dropSetPlace = ", max_dropSetPlace)
    print("num_dropOnEdge = ", num_dropOnEdge)
    print("dropIniPlace = ", dropIniPlace)

    return

if __name__ == '__main__':
    droplet_setting, flow_setting = read_setting("../../case")
    dropSetPlace = read_dropIniPlace("../../case")
    calc_dropIniPlace(droplet_setting["num_droplets"],dropSetPlace)
    dGroup = get_dropletArray(droplet_setting["num_droplets"])
    print(dGroup)
