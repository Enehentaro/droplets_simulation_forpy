from typing import Tuple
import yaml
import pprint
import numpy as np

def read_setting(CaseDir:str) -> Tuple[dict, dict]:
    with open(CaseDir + '/setting.yaml', 'r', encoding="utf-8") as f:
        all_setting = yaml.safe_load(f)

    droplet_setting = all_setting["dropletSetting"]
    flow_setting = all_setting["flowFieldSetting"]

    pprint.pprint(droplet_setting)
    pprint.pprint(flow_setting)

    return droplet_setting, flow_setting

def read_dropSetPlace(CaseDir:str) -> np.ndarray:
    dropSetPlace = np.loadtxt(CaseDir + '/initial_position.txt', delimiter=",", skiprows=1, dtype='float')
    print("dropSetPlace = ", dropSetPlace)
    
    return dropSetPlace

if __name__ == '__main__':
    read_setting('case')
    read_dropSetPlace('case')