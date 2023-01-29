# -*- ecoding: utf-8 -*-
# @ModuleName: Vector_group
# @Author: invincible
# @Time: 2022/7/8 11:10
# coding=utf-8

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import Curve_group
from itertools import chain

Result = Curve_group.decryption()
try:
    if Result is True:

        """
            切割 -- primary
        """
        # 点依次排序
        class SortPt(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点排序", "RPP_SortPt",
                                                                   """以初始点依次进行排序""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("599bb86f-b653-44de-b1a9-591ed5808e1f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "P", "待排列的点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "first", "f", "指定开始元素,默认为第一个")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pt_Result", "Pi", "排序后的点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "排序后的下标")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGdSURBVEhLrdY9KEVhHMfx6yXykkJKycJEBvIyUTZZyGAzCDFREmVkYsVglEXJYlFKGYjBoAwMohhEZFKE8P2d7tHjnHPPea57fvWp+5z7PM//vDznuTeRZlowhSEU6kCcGce34QyViCVV+IBZQJYRSzrgnVx2EUsqcA9vgRf0IpYswJz8EFfJz4vIwr9Ti0fcYBBdUEqxDbdgDdJOLk6hSdp0ICDT0PcPWMMO5lCAyKxCgyecVur0Q/1M+wjNANRx02mFZxLeApIyddDa14Ms0oGIrMC6QD7OoQ6NOmCRTrzDnPwNgdGDUodRp2WfDWjcJy7QDV9GoE7rTss+2biGbqmWtVbfb7TXLGEPqn6CPx0s0gqd2LzTMlIO9410ad0XI53obdZY3zMbgzm5axi20TZxm+TbMmYRVGAGttGS1hjtV77U4wvm5GprUFTKoDd4C3pnGhCYHlziFVpefYhKE3RL3JPS2GakTB6qkeO0wqP7fADzquUYWq4ZR7vkM7wF9ANUgoyjKziCt4CWdyxXoOgvzB3cyZ/QDiOJxA8jXI+HhRHZIAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Pts, first):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    first = 0 if first is None else first
                    if Pts:
                        Pt_Result, Index = [], [first]

                        def ptsort(pts, tag_ind):
                            pt_list = []
                            for _ in range(len(pts)):
                                if _ not in Index:
                                    dis = rg.Point3d.DistanceTo(pts[tag_ind], pts[_])
                                    pt_list.append((dis, _))
                            pt_list.sort()
                            Index.append(pt_list[0][1])
                            if len(Index) == len(pts):
                                for j in Index:
                                    Pt_Result.append(pts[j])
                                return Index, pt_list
                            else:
                                return ptsort(pts, Index[-1])

                        ptsort(Pts, first)
                        return Pt_Result, Index
                    else:
                        self.message2("点列表为空！")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = '点依次排序'


        # 点序排序
        class PointsSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点排序", "RPP_PointsSort",
                                                                   """点序排列角点，根据参照点自动排序点阵""",
                                                                   "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b852c643-79d1-48fc-9a5a-2c674bb342fe")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Ref_Point", "P", "参照点，默认为世界坐标原点（0，0，0）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Ref_Curve", "V", "参照向量；当数据组出现不同类型的矩阵，可以统一点序的初始方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Points", "Pts", "点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Result", "R", "成功排序的点序")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH4SURBVEhLxdW5Sx1RFMfxh8GQRDAS7WIKQUUbJVZWaicoFgkknbFwKUQFiyxamaVIE40W/gMxkEYkpDG9SBL3DdzAJVZxCaJgqd/fM3e4c2Z4pNH3gw/65tw76My55yXSkZu4cflrbG79+xmXlHsz8QFbWMcr+KnCBH5jHCVw0d5+uL0vEclHnBudUApxBr+2g7tQBuHXpANB7uAQdtEClOewNamHcgRbm0eQ29iHXTQDpRu2JrVQDmBr0wjlDeyiJigPYP/KFWRBeQe/Js8QSQ/0r/1Cmy54Kcc3LOMz8uGnF25vqy6kJQVoRwvydMGkAV2oSX4Kx+1tRq4u2KjPj+GeodqwGIoOzxf4z/g9XKrh791GEYLoBmpJ/wYyBuUxbE30XpRF2NoogmTjBHbRGpQ+2Jo8gXIKW1tFkAz8gF00AqUOtialUNQ5tvYJoTyE5oxbsAS/FYfh3+AFXCqwB1fTI7uPSO7hEdQtOt02lXiKsuSncNQ5bm+qiXt1cSNXLbYJnWo/6v1J6FF8h3v+ivYOQHs3YEd9MnEjV4dKiRvXu8iBMgS/JpFxHTdy3bjWC7U1ceP6L2wtMq7/wC7633EdN+qnEMpr2EVuXKtd7ReSpqob12/h16QRkejlzOIn7MhVa36FzocOoO1zNcUctFfD8jqSSFwAmoPvaxdGlE0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            refer, vector, switch = None, None, False

            def close_point(self, points_list):
                new_points = [self.refer]

                while len(points_list) > 0:
                    ref_point = new_points[-1]
                    all_len = [rg.Point3d.DistanceTo(_, ref_point) for _ in points_list]
                    min_len = min(all_len)
                    min_index = all_len.index(min_len)
                    new_points.append(points_list[min_index])
                    points_list.pop(min_index)
                return new_points[1:]

            def re_built_sort(self, point_data):
                vector_all = [rg.Vector3d(_) - rg.Vector3d(point_data[0]) for _ in point_data[1:]]
                min_vector_ang, min_index = rg.Vector3d.VectorAngle(vector_all[0], self.vector), 0
                for vec_num in range(len(vector_all)):
                    vector_ang = rg.Vector3d.VectorAngle(vector_all[vec_num], self.vector)
                    if min_vector_ang > vector_ang:
                        min_index = vec_num

                if min_index != 0:
                    min_index_of_po = min_index + 1
                    first_two = [point_data[0], point_data[min_index_of_po]]
                    rest_point = [_ for _ in point_data if _ not in first_two]
                    re_place = first_two + rest_point
                    first = re_place[0]
                    self.refer = re_place[1:][0]
                    final_points = self.close_point(re_place[1:])
                    final_points.insert(0, first)
                    return final_points
                else:
                    return point_data

            def RunScript(self, Ref_Point, Ref_Curve, Points):
                self.refer = rg.Point3d(0, 0, 0) if Ref_Point is None else Ref_Point
                if Ref_Curve is None:
                    self.vector = None
                else:
                    self.vector = Ref_Curve if type(Ref_Curve) is rg.Vector3d else Ref_Curve.TangentAtStart
                leaf_points = [list(_) for _ in Points.Branches]
                if len(leaf_points) != 0:
                    res = map(self.close_point, leaf_points)
                    Result = ght.list_to_tree(res) if self.vector is None else ght.list_to_tree(
                        map(self.re_built_sort, res))
                    return Result


        # 点序排序（分组排序）
        class PointOrderGroupingSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点序排序（分组排序）", "RPP_PointOrderSort",
                                                                   """点序排序，按X-Y-Z轴分组排序""", "Scavenger",
                                                                   "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9b7d7417-b3aa-4580-bb4c-1c3193c78eeb")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "PTS", "P", "点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "坐标轴")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "分组的容差")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Result", "R", "排序后结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGcSURBVEhLtZXJSgQxFEXLlRM4bUScFk6gf6Sggi4UdKkiqAgudCMuHED8ERWHpdor8Yu8J1Sa9KMqCd164WQglUq91M1LUWpBXIjrCuZFTEuiat65mBHFovgRe2JVrBnGhNeAGC5rrwlh5/CeA/EtiivBy2PqEmfiVTyLN3EkUjqhuBUrNCIaEl9iVPSJKfEpekVMmxTsF2HFNCKeBJGgbkG/3/XqtUWRs8CgaAi+nGhmBRGlInAL3Ih1GhHx5ez5i+DL+Rf7IqVtinuxQSNDPYJ/QJ2jHQp8HlrxLzVe1k2x19bnodoe9z7H3/j8XYQ+73TcrRz6fFJ8CO8SO27PAeP0a88JYVmfPwrv89Q5YD7P+3Fe3HJO2DPrc/uFsXPAfPp+fK7sNyNgZfYszDWhz9sZr8xvrBjzeVvj5HNS7n9omuJBuKyXIfY6dg6sdinIRalkxx77+wB3sMctPq9Rdja19wHnJOc+yF6go/vgTizTiCh1Durk/u2lOKQRkfU5deoeR/w3l665/Y8FIVnClFt1HxBV1bzToigavznUYxXIUCEIAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.axis = None
                self.Tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def find_collinear_pts(self, points):
                copy_points = points[:]
                new_tree_list = []
                while len(copy_points) > 0:
                    single_pts = [_ for _ in copy_points if
                                  abs(eval("copy_points[0].{} - _.{}".format(self.axis, self.axis))) <= self.Tol]
                    new_tree_list.append(single_pts)
                    for _ in single_pts:
                        copy_points.remove(_)
                nn_points_list = map(lambda x: ghc.SortPoints(x)["points"][::-1], new_tree_list)
                start_points = sorted(map(lambda start: start[0], nn_points_list))[::-1]
                res_points = []
                for s_index in start_points:
                    for _ in range(len(nn_points_list)):
                        if s_index in nn_points_list[_]:
                            res_points.append(nn_points_list[_])
                return res_points

            def handing_sort_re(self, data):
                rebuild_sort = []
                length_origin = len(data[0])
                copy_data = [data[_][::-1] for _ in range(1, len(data))]
                copy_data.insert(0, data[0])
                for single_data in copy_data:
                    count = 0
                    while length_origin > count:
                        rebuild_sort.append(single_data[count])
                        count += 1
                one_dim = list(chain(*copy_data))
                rest_data = [_ for _ in one_dim if _ not in rebuild_sort]
                rebuild_sort = rebuild_sort + rest_data
                return rebuild_sort

            def RunScript(self, PTS, Axis, Tolerance):
                try:
                    if len(PTS) != 0:
                        self.axis = "X" if Axis is None else Axis.upper()
                        self.Tol = Tolerance if Tolerance is not None else 50.0
                        if self.axis not in ["X", "Y", "Z"]:
                            self.message1("请输入正确的坐标轴！")
                        sort_by_axis = self.find_collinear_pts(PTS)
                        result_point_sort = self.handing_sort_re(sort_by_axis)
                        return result_point_sort
                    else:
                        self.message2("点序不能空！")
                finally:
                    self.Message = "点序排序（分组排序）"


        # 按照参照平面排序
        class PtsSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点排序", "RPP_PtsSortByXYZ",
                                                                   """点序列排序，将按照给定的参照平面排序，不给默认为世界XY""",
                                                                   "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4d413cd7-9c52-47a6-9af6-92502286f023")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "P", "点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "轴（x，y，z）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "参照平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Sort_Pts", "P", "排序后的点序列")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGhSURBVEhLpda9LwRBHMbxxXl/Lby1/AFeOoVCJP4TCgWFRBQiQkEiJCKRKDQ6GhGKqzQaodARBUpEI4iEhPB95naTdTezt3Oe5JPbmdvZ397O7N4GltRjFouYQTXSpAejuc3kdOAn9I0mpMkpNKbPtBLShldo5yc0oliGEJ3UgTqSUkqBc9xhDRrXC2d8C0RnP4YyfCALZ3wL6Oxvc5smE9DYftOyxKdAdPYXWMYKtsI+51z4FDiB9nsLP+Ur1rbORdoC0dlPozlPN5xzkaZAJS7xjCp1WKIbVccoSJoCutu1LMdNy54WXOc2/ybtJaoIP5Ni3cdnkkuKb4FWhxpY41NgEtovTsv0Bbo3MiiITwE9ouexEJrDPjR2B3p0FOS/c3CGezSYliXl0E9UgUd1eCR6mo6YVizD2MAS1vEJ7fiOVahf3w/ClQFozLZp5aUT0T+SyzG0OmzRna0n6gPq1GGLZvwQtoPvIinOS5MfW5FiB48uzaZppYiKHEGD9tSREK2UG2i1daE9pBeHWjijV5UpaEUlRa818V8bdxUEQeYXu2uXtVyxgvoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_axis = {'X': 'x_coordinate', 'Y': 'y_coordinate', 'Z': 'z_coordinate'}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mergesort(self, arr_list):
                if len(arr_list) <= 1:
                    return arr_list
                middle = int(len(arr_list) / 2)
                l_list, r_list = self.mergesort(arr_list[:middle]), self.mergesort(arr_list[middle:])
                result = []
                l_hand, r_hand = 0, 0
                while l_hand < len(l_list) and r_hand < len(r_list):
                    if r_list[r_hand] < l_list[l_hand]:
                        result.append(r_list[r_hand])
                        r_hand += 1
                    else:
                        result.append(l_list[l_hand])
                        l_hand += 1
                result += l_list[l_hand:] + r_list[r_hand:]
                return result

            def RunScript(self, Pts, Axis, CP):
                try:
                    CP = CP if CP is not None else ghc.XYPlane(rg.Point3d(0, 0, 0))
                    Axis = 'X' if Axis is None else Axis
                    Axis = Axis.upper()
                    if len(Pts) != 0:
                        if Axis not in ['X', 'Y', 'Z']:
                            self.message1("请输入正确的坐标轴！")
                        else:
                            sorted_pts_axis = ghc.PlaneCoordinates(Pts, CP)[self.dict_axis[Axis]]
                            zip_list_sort = zip(sorted_pts_axis, Pts)
                            Sort_P = zip(*sorted(zip_list_sort))[1]
                            return Sort_P
                    else:
                        self.message2("点序列不能为空！")
                finally:
                    self.Message = '点排序'


        """
            切割 -- secondary
        """
        # 删除重复的点
        class CullPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-删除重复的点", "RPP_CullPoints",
                                                                   """删除点列表中重复的点""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("bbfb844f-0f92-43e6-be07-6a26d8de96b7")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Points", "P", "点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Output Format", "O", "输出的方式（0：只输出剔除后的数据，1：将重复的数据分组）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Reuslt_Pt", "R", "结果列表")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index_Pt", "I", "重合点的下标组")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVMSURBVEhLxVV3TJRnHH7LaLW1pzVGrSYtggQJgpooqHB4OLCuGFmKGA3GSRARNY4Yt1UwGqPRugVFRG0ZKioyHamDKUMtyNZyUMq+ffj0ueO0tSL1vz7Jk3vv/X7v7/mt73vF/4KLEolz8uDBy/YJ0du01S0uWFiMTe7ff3m4EF+btj6OKHPzqXmBgW3KM2eQKZNl7RbiW9OjLhFjZuZXGBam0dy4gTQ3t4wN3QUVaW7umR0Q0K6Lj4f29m1orl5Fhrt7zsGPiESbmc0tDg3VQS4HFAro7t1DirNz5iohJCaTv3FJIvHM8fdvU0dFofnIEbQcPw7N9evQxcV1KXLe0nJeUUiIDhUV0D5/Dk1BAd7U1kKbkYE7zs4ZB4ToazJlWT7/3P6xl1e74tAhNGzdisZ9+9B69CjaWSb9zZswZJQuleZGCDHQYB9jaelXGBysBx3rsrOhefwY6qwsqLjuoKA+NRV3XFziafqZwV6c79nTpWTpUrTu2YP60FA07tyJ1gMHoDhxAipmhORk6BMSkOrufj9KiKC8oCAdnj6F/sEDaDIzob57FypSSWoogvx8pE+cmP9OAFxcs7P7sXr1arTu3o3GDRvQsncvFIcPQ80stNHRAKNqi4lB6bp1wMOH6EhL6+wTqSKVt25BlZ6ODoo+8fVtutijh5vR+T8RZ2sbXr1mDRTh4WjesgXt+/dDdewYtOfOoePSJYBOcP8+3iQlQZeYCC2pJpXMTsUp6khJwRMfn6YzQkwwufwQcTY24TVhYVCzRG3bt0N58CA0bLg+MtIo8ubKFeg5XTpSExsLJfcVp05Bd/kyHnl7N0cK4W5y9XH8YmMT8WrtWmjYdAX7oaKIlk3Xnz4N/dmz0J48CTXLp2A52zdtgpoZP5o5s/vI/w1msrMsNFSt5EQpduyAir/qiAio2BslM1Ns3oz29evRsmsXsry8Ks5aWEhNRz8Na4Xony6TyVvpsI3ZtG3caIzWwDaylXvtHIZa7v9sZXXBdOzTwJdkcIZMlmN8J1atQuPKlWgKCUEzB8DAJk5bY3Aw/uRoNzGLUq4T7Oz46foEHBFiEJ3nNzHK+kWLIJ8/H/WBgWigs4blyzvJ9R+LF6Nu4ULU+vigMSgIlQwiYdgwfu+6wU+MPNPDI6+BUb6aPRs106fjNR3Uzp0LeUCAUazO3x9yspY0PKuhXdXkyZAvWIByCl9zcOg6E46X0bl8xQqUT5iAl66uqODBqmnTUDNrFmpmzEDdkiWoZ+0NgtX8X0VWenqiXCZD6ejRqKZdGbO95uj4vsgpiaRvmlSa9TtTfjFyJJ4NH44SZ2ejSBnFyqVS1LFcBTycIpPV1fJzYhAoc3PDS7LExQUvRo1Csa2tUewls0tydNxsci9E7IABHpV0XjJmDPIHDkSRvT2eOToaD/02YgReeXujnNGzxttOCPFdmkyWW8/GllH4uZOTkcU8U2Bjg7w+fSD39UX6lClVdN35LbrYu/c3Ka6u6dWscRGjyB80CIVDh6JwyBBUTp1qTDvR3n6v0Zg4zk83RzivdtkyvGAABVZWeErb3H79UMqsi9mb6w4Oq03mnTBcj6lSaUYNm1lA4xyJxJh+KTNLdHB45/wtjNPm4ZH7mqUrtLZGdq9eKBk3DsXsT7yd3TqT2fvYxpvIKEKjqkmTUDpvHm44Oe0xPf4A53g/cDByXvv5oZL2RYw83t6+a+dvsYY3UdL48XdzvbyaYztHzpz8gvyyC5rxDra66eb2a/acOS3RdnZbuPef+Iq0nS6EC38HkN+T1t3QcMtZ/yDEWNPakjRBiL8At09pA8gJgyQAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None
                self.copy_pts = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def cull_point(self, pts):
                count = 0
                base_pt = pts[0]
                group_data = []
                while len(pts) > count:
                    if base_pt.DistanceTo(pts[count]) < self.tol:
                        group_data.append(pts[count])
                    count += 1
                for _ in group_data:
                    pts.remove(_)
                return group_data, pts

            def test(self, data):
                return [self.copy_pts.index(_) for _ in data]

            def RunScript(self, Points, Tolerance, Output_Format):
                try:
                    Output_Format = 0 if Output_Format is None else Output_Format
                    if Output_Format > 1:
                        self.message2("请输入正确的数据类型！！")

                    self.tol = 0.01 if Tolerance is None else Tolerance
                    if len(Points) == 0:
                        self.message2("点序列表不能为空！！")
                    else:
                        self.copy_pts = Points[:]
                        tree_data_pts = []
                        while True:
                            if len(Points) <= 0:
                                break
                            else:
                                new_cull_pts, Points = self.cull_point(Points)
                                tree_data_pts.append(new_cull_pts)
                        tree_data_indexes = map(self.test, tree_data_pts)
                        if Output_Format == 0:
                            Reuslt_Pt, Index_Pt = map(lambda x: min(x), tree_data_pts), ght.list_to_tree(
                                tree_data_indexes)
                        else:
                            Reuslt_Pt, Index_Pt = ght.list_to_tree(tree_data_pts), ght.list_to_tree(tree_data_indexes)
                        return Reuslt_Pt, Index_Pt
                finally:
                    self.Message = '删除重复点'


        """
            切割 -- tertiary
        """
        # 多重向量偏移
        class Skewing(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-多向量偏移", "RPP_Skewing", """多向量位移""",
                                                                   "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3e8b5fff-1d6e-49d1-b6be-f5c5b36bc816")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Object", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Ref_Plane", "P", "参考向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "XVector", "X", "X轴的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "YVector", "Y", "Y轴的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "ZVector", "Z", "Z轴的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Objcet", "G", "位移后的物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Transform", "T", "偏移后的总量")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                result = self.RunScript(p0, p1, p2, p3, p4)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHYSURBVEhL5dU9SJVRHMfxpyxUMigRpBwKERqqKSqEojCCEGppFDGQSkKJIiJpKqWUSgqlIV16UfAFGlpNFEtRo0HDHKSht0GMRHNp8vt9zhXiUnCH50794MM9z3Ovzznn/5xzjP6r3EFZaCafo/iNx9jgjaSzGzdwHFnpwNShKDSzk4vIWgfbcA/H4quEk4NevEA3fA8lf7ELj3AKm5BxtuIVOvEM91GPhjTn8RWTKETG2Y4HeIkB2OG/4uidccbJhxvsMOwo0VjHZhyJrxLOBbTAF5p4rOFnfEDiZTHWvRIuvUSPBVdH+grIxcbQjNt5oRnHXe1gjL/xO3+jzX/ci3MTlmQa1r0fE3iD03iNMQzDk9Ul6/VTnIB/Owrv92AKPmsE0SGsoBTX8AnzKIcjcYcuwBPVldWEJThjr6vxEVtSnNktvEMxoit4a4P4kEX4QEfyEAfgS+9CK9wTc5jFWZzET/ShDeYSnHUcT8mZ0Iz24Ae+4DZqsQ924OxqsJ4qrOIJxrEf6//xLmMoNEMJltGIQThyS7QXZgd+oSC+iqIz8AGW5hva8R0Oxk7NdbwPzRB3qw+2vr55p+gyNdb6aurTWBJP1ueowE7cRQfcnOYgzoVmVhNFaxZkV0zB5eR1AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                dict_data = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def judgment_type(self, obj):
                return False if type(obj) is rg.LinearDimension else True

            def normal_move(self, plane, vector_iter):
                origin_vector = [plane.XAxis, plane.YAxis, plane.ZAxis]
                zip_list = list(zip(origin_vector, vector_iter))
                offset_total_vector = map(lambda total: ghc.Amplitude(total[0], total[1]), zip_list)
                offset_vector = reduce(lambda n1, n2: n1 + n2, offset_total_vector)
                return offset_vector

            def RunScript(self, Object, Ref_Plane, XVector, YVector, ZVector):
                try:
                    Ref_Plane = ghc.XYPlane(rg.Point3d(0, 0, 0)) if Ref_Plane is None else Ref_Plane
                    XVector = [0] if len(XVector) == 0 else XVector
                    YVector = [0] if len(YVector) == 0 else YVector
                    ZVector = [0] if len(ZVector) == 0 else ZVector
                    total_offset_x, total_offset_y, total_offset_z = sum(XVector), sum(YVector), sum(ZVector)
                    zip_vector = (total_offset_x, total_offset_y, total_offset_z)
                    Transform = self.normal_move(Ref_Plane, zip_vector)

                    if Object:
                        if isinstance(Object, (rg.Point3d, rg.Point)) is True:
                            Object = rg.Point(Object)
                        elif isinstance(Object, (rg.Line, rg.LineCurve)) is True:
                            Object = Object.ToNurbsCurve()

                        if self.judgment_type(Object) is True:
                            Object.Translate(Transform)
                            New_Objcet = Object
                            return New_Objcet, Transform
                        else:
                            return None, Transform
                    else:
                        self.message2("物体为空！！")
                        return None, Transform
                finally:
                    self.Message = "多向量位移"

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Vector_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("54d72071-40fa-4946-a45c-3d10d6d6ad0e")
