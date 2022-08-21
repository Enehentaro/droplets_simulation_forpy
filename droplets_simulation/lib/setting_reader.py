from typing import Tuple
import yaml
import pprint

def read_setting(CaseDir:str) -> Tuple[dict, dict]:
    with open(CaseDir + '/setting.yaml', 'r', encoding="utf-8") as f:
        all_setting = yaml.safe_load(f)

    droplet_setting = all_setting["dropletSetting"]
    flow_setting = all_setting["flowFieldSetting"]

    pprint.pprint(droplet_setting)
    pprint.pprint(flow_setting)

    return droplet_setting, flow_setting