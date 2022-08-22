from lib.setting_reader import read_setting
from lib.SimpleVtk import SimpleVtkUnstructuredGrid

def main():
    print("please write your case directory name")
    CaseDir = input()
    droplet_setting, flow_setting = read_setting(CaseDir)
    ugrid = SimpleVtkUnstructuredGrid()
    ugrid.read_vtk(flow_setting["path2FlowFile"])

if __name__ == '__main__':
    main()