from lib.setting_reader import *
from lib.SimpleVtk import SimpleVtkUnstructuredGrid
from lib.droplet import *
from lib.unstructured_grid import *
import time

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
    cellCenter = ugrid.get_cellCenter()

    startTime = time.perf_counter()
    
    refCellId = []
    for i in dGroup["position"]:
        nearestID = nearest_search(cellCenter,i)
        refCellId.append(nearestID)
        
    endTime = time.perf_counter()
    print(endTime - startTime,"sec")
    print(len(refCellId))

if __name__ == '__main__':
    main()