import vtkmodules.all as vtk
from vtkmodules.util import numpy_support as ns
import numpy as np

class OutPutError(Exception):
    '''vtkライブラリ使用時の出力に関するエラー'''


celltypes_def_dict = {"tetra": vtk.VTK_TETRA, 
                      "prism":vtk.VTK_WEDGE, 
                      "hexa":vtk.VTK_HEXAHEDRON, 
                      "pyramid":vtk.VTK_PYRAMID, 
                      "point":vtk.VTK_POINTS}

class SimpleVtkUnstructuredGrid():
    '''
    Description
    -----------
    A class for a simple vtk library wrapper.
    - read/write Legacy VTK files.

    '''

    def __init__(self) -> None:
        self.grid = vtk.vtkUnstructuredGrid()
        self.cells =vtk.vtkCellArray()
        self.points = vtk.vtkPoints()
        self.celltypelist = []

#読み込み系のメソッド
    def read_vtk(self, filename):
        '''
        read vtk unstructured grid file.
        '''
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        reader.Update()
        self.grid = reader.GetOutput()   

    def get_points(self):
        """
        return point array.

            array[d1,d2] : point coordinates. 

            `d1`:pointId, `d2`:coordinates(`1`:x, `2`:y, `3`:z)
        """
        return ns.vtk_to_numpy(self.grid.GetPoints().GetData()) 
        

    def get_cells(self):
        '''
        returns tuple of `(connectivity array, offsets array)`
        
        types of these arrays are`np.int64`.

        Note
        -----
        Cited from https://vtk.org/doc/nightly/html/classvtkCellArray.html#aed9b6605b0a86217b972773628c8c518 

        Internally, the connectivity table is represented as two arrays: Offsets and Connectivity.

        Offsets is an array of [numCells+1] values indicating the index in the Connectivity array where each cell's points start. The last value is always the length of the Connectivity array.

        The Connectivity array stores the lists of point ids for each cell.

        Thus, for a dataset consisting of 2 triangles, a quad, and a line, the internal arrays will appear as follows:
        
        ```
            Topology:
            ---------
            Cell 0: Triangle | point ids: {0, 1, 2}
            Cell 1: Triangle | point ids: {5, 7, 2}
            Cell 2: Quad     | point ids: {3, 4, 6, 7}
            Cell 4: Line     | point ids: {5, 8}
            
            vtkCellArray (current):
            -----------------------
            Offsets:      {0, 3, 6, 10, 12}
            Connectivity: {0, 1, 2, 5, 7, 2, 3, 4, 6, 7, 5, 8}
        ```

        Usage
        -----
        To get connectivity of a cell `cell`, then

            >>> connectivity[offsets[cell]:offsets[cell+1]]
            [0 1 2]


        '''
        return ns.vtk_to_numpy(self.grid.GetCells().GetConnectivityArray()), ns.vtk_to_numpy(self.grid.GetCells().GetOffsetsArray())

    def get_celltypes(self):
        """
        return array of cell types.
        """
        return ns.vtk_to_numpy(self.grid.GetCellTypesArray())

    def get_number_of_cells(self):
        """
        return number of cells.
        """
        return self.grid.GetNumberOfCells()

    def get_number_of_points(self):
        """
        return number of points.
        """
        return self.grid.GetPoints().GetNumberOfPoints()

    def get_field_data(self, array_name:str):
        """
        get field data named as `array_name`
        """
        celldata = self.grid.GetCellData()
        if celldata.HasArray(array_name):
            return ns.vtk_to_numpy(celldata.GetAbstractArray(array_name))
        else:
            raise OutPutError("{0} does not exist in current grid.".format(array_name))

#ここから書き込み系のメソッド
    def set_points(self, point_array):
        '''
        set point coordinates.

        point_array[d1,d2] : point coordinates. 
        
        `d1`:pointId, `d2`:coordinates(`1`:x, `2`:y, `3`:z)
        '''
        self.points.SetData(ns.numpy_to_vtk(point_array))

    def set_cells(self, element_data, celltype_list:list):
        '''
        setting CellArray using ImportLegacyFormat.

        Arguments
        ---------
        - element_data : 1d array data with the legacy layout;
        { n0, p0_0, p0_1, ..., p0_n, n1, p1_0, p1_1, ..., p1_n, ... }
        where n0 is the number of points in cell 0, and pX_Y is the Y'th point in cell X.
        - celltype_list : 1d array. components must be "VTK_***".
        '''
        self.cells.ImportLegacyFormat(ns.numpy_to_vtkIdTypeArray(element_data))
        self.celltypelist = celltype_list

    def set_cells(self, offsets:np.ndarray, connectivities:np.ndarray, celltype_list:list):
        '''
        Sets the internal arrays to the supplied offsets and connectivity arrays.
        '''
        self.cells.SetData(ns.numpy_to_vtkIdTypeArray(offsets), ns.numpy_to_vtkIdTypeArray(connectivities))
        self.celltypelist = celltype_list

    def add_field_cell_data(self, data_name, data_array, attribute=None):
        '''
        set cell data

        attributes: attribute of given cell data. choose 'scalar', 'vector' or 'tensor'.
        '''
        _array = ns.numpy_to_vtk(data_array)
        _array.SetName(data_name)

        if attribute is None:
            self.grid.GetCellData().AddArray(_array)
        elif attribute == "scalar":
            self.grid.GetCellData().SetScalars(_array)
        elif attribute == "vector":
            self.grid.GetCellData().SetVectors(_array)
        elif attribute == "tensor":
            self.grid.GetCellData().SetTensors(_array)
        else:
            raise OutPutError("3rd arguments 'attribute' must be 'scalar', 'vector', 'tensor' or ''.")


    def make_grid(self):
        '''
        Making `vtkUnstructuredGrid` object after setting cells and points.
        '''
        self.grid.SetPoints(self.points)
        self.grid.SetCells(list(self.celltypelist), self.cells)

    def write_out(self, filename, binary = False, old_version=False):
        '''
        write out grid as legacy vtk format.

        '''
        writer = vtk.vtkUnstructuredGridWriter()
        
        writeout_core_(self.grid, writer, filename, binary, old_version)


def writeout_core_(grid_,writer_,filename,binary,oldversion):
    '''
    Note
    ----
    From vtkDataReader.h;
    "Currently VTK can write out two different versions of file format: files
    of VTK reader version 4.2 and previous; and VTK reader version 5.1 and
    later. This will likely change in the future. (Note: the major
    difference in the two formats is the way cell arrays are written out.)
    By default, Version 5.1 files are written out."
    '''
    writer_.SetInputData(grid_)
    writer_.SetFileName(filename)

    if binary :
        writer_.SetFileTypeToBinary()
    else:
        writer_.SetFileTypeToASCII()
        
    if oldversion:
        # https://vtk.org/doc/nightly/html/vtkDataWriter_8h_source.html
        # SetFileVersionはvtk9.1.0以降対応. 
        if vtk.VTK_MAJOR_VERSION >= 9 and vtk.VTK_MINOR_VERSION >= 1:
            writer_.SetFileVersion(writer_.VTK_LEGACY_READER_VERSION_4_2)
        else:
            raise OutPutError("VTK version error :: Current version is {0}.{1}".format(vtk.VTK_MAJOR_VERSION, vtk.VTK_MINOR_VERSION))

    writer_.Write()


if __name__ == "__main__":
    ugrid = SimpleVtkUnstructuredGrid()
    ugrid.read_vtk("./vtk/sax_flow.vtk") #ここ環境に合わせて変えて

    print(ugrid.get_number_of_cells())
    print(ugrid.get_number_of_points())

    points = ugrid.get_points()
    print(points[0,:])

    cell2node, offsets = ugrid.get_cells()
    cellId = 0
    print(cell2node[offsets[cellId]:offsets[cellId+1]])

    data_s1 = ugrid.get_field_data("pressure")
    print(data_s1)

    output = SimpleVtkUnstructuredGrid()
    output.set_points(points)
    output.set_cells(offsets, cell2node, ugrid.get_celltypes())
    output.add_field_cell_data("pres", data_s1, "scalar")
    output.make_grid()
    output.write_out("test.vtk")
    