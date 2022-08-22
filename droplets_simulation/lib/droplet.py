import numpy as np

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

if __name__ == '__main__':
    dGroup = get_dropletArray(10)
    print(dGroup)
