from lib.setting_reader import *
from lib.SimpleVtk import SimpleVtkUnstructuredGrid
from lib.droplet import *

def main():
    ugrid = SimpleVtkUnstructuredGrid()

    print("please write your case directory name")
    CaseDir = input()

    droplet_setting, flow_setting = read_setting(CaseDir)
    dropSetPlace = read_dropSetPlace(CaseDir)

    dropIniPlace = calc_dropIniPlace(droplet_setting["num_droplets"],dropSetPlace)
    dropIniRadius = read_dropIniRadius(droplet_setting["num_droplets"])
    dGroup = get_dropletArray(droplet_setting["num_droplets"], dropIniPlace, dropIniRadius)
    
    output_dropVTK(droplet_setting["num_droplets"],dGroup)
    
    ugrid.read_vtk(flow_setting["path2FlowFile"])

if __name__ == '__main__':
    main()