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
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import initialization
from itertools import chain

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:
        # 点序排序
        class PointsSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点排序（参照点排序）", "RPP_PointsSort", """点序排列角点，根据参照点自动排序点阵""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b852c643-79d1-48fc-9a5a-2c674bb342fe")

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
                self.SetUpParam(p, "Ref_Point", "P", "参照点，默认为世界坐标原点（0，0，0）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Point(rg.Point3d(0, 0, 0)))
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
                try:
                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.refer = Ref_Point
                        if Ref_Curve is None:
                            self.vector = None
                        else:
                            self.vector = Ref_Curve if type(Ref_Curve) is rg.Vector3d else Ref_Curve.TangentAtStart
                        leaf_points = [list(_) for _ in Points.Branches]
                        if len(leaf_points) != 0:
                            res = map(self.close_point, leaf_points)
                            Result = ght.list_to_tree(res) if self.vector is None else ght.list_to_tree(map(self.re_built_sort, res))
                            return Result
                finally:
                    self.Message = '点排序'


        # 点序排序（分组排序）
        class PointOrderGroupingSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点序排序（分组排序）", "RPP_PointOrderSort", """点序排序，按X-Y-Z轴分组排序""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9b7d7417-b3aa-4580-bb4c-1c3193c78eeb")

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
                self.SetUpParam(p, "PTS", "P", "点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "坐标轴")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('X'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "分组的容差")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(50))
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

            def find_collinear_pts(self, points):
                copy_points = points[:]
                new_tree_list = []
                while len(copy_points) > 0:
                    single_pts = [_ for _ in copy_points if abs(eval("copy_points[0].{} - _.{}".format(self.axis, self.axis))) <= self.Tol]
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
                    re_mes = Message.RE_MES([PTS], ['PTS'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.axis = Axis
                        self.Tol = Tolerance
                        if self.axis not in ["X", "Y", "Z"]:
                            Message.message1(self, "请输入正确的坐标轴！")
                        sort_by_axis = self.find_collinear_pts(PTS)
                        result_point_sort = self.handing_sort_re(sort_by_axis)
                        return result_point_sort
                finally:
                    self.Message = "点序排序（分组排序）"


        # 删除重复的点
        class CullPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-删除重复的点", "RPP_CullPoints", """删除点列表中重复的点""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("bbfb844f-0f92-43e6-be07-6a26d8de96b7")

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
                self.SetUpParam(p, "Points", "P", "点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差度")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Output Format", "O", "输出的方式（0：只输出剔除后的数据，1：将重复的数据分组）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
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

            def remove_duplicate_points(self, points):  # 删除重复的点
                new_points = []
                index_groups = []  # 点分组后的下标
                for i, p in enumerate(points):
                    flag = False
                    for j, np in enumerate(new_points):
                        if p.DistanceTo(np) <= self.tol:  # 根据公差判断点是否重复
                            index_groups[j].append(i)
                            flag = True
                            break
                    if not flag:
                        new_points.append(p)  # 添加唯一点
                        index_groups.append([i])
                return new_points, index_groups

            def RunScript(self, Points, Tolerance, Output_Format):
                try:
                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc

                        if Output_Format > 1:
                            Message.message2(self, "请输入正确的数据类型！！")
                            return gd[object](), gd[object]()
                        self.tol = Tolerance
                        new_cull_pts, Index = self.remove_duplicate_points(Points)
                        if Output_Format:  # 判断输出方式
                            group_points = [[] for _ in range(len(Index))]
                            for i in range(len(Index)):
                                for j in Index[i]:
                                    group_points[i].append(Points[j])
                            Reuslt_Pt = ght.list_to_tree(group_points)  # 将重复点列表转化为树
                        else:
                            Reuslt_Pt = new_cull_pts
                        Index_Pt = ght.list_to_tree(Index)  # 将下标列表转化为树

                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Reuslt_Pt, Index_Pt
                finally:
                    self.Message = '删除重复点'


        # 按照参照平面排序
        class PtsSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点按XYZ轴排序", "RPP_PtsSortByXYZ", """点序列排序，将按照给定的参照平面排序，不给默认为世界XY""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4d413cd7-9c52-47a6-9af6-92502286f023")

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
                self.SetUpParam(p, "Pts", "P", "点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "轴（x，y，z）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('X'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "参照平面")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
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
                    re_mes = Message.RE_MES([Pts], ['Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        Axis = Axis.upper()
                        if Axis not in ['X', 'Y', 'Z']:
                            Message.message1(self, "请输入正确的坐标轴！")
                        else:
                            sorted_pts_axis = ghc.PlaneCoordinates(Pts, CP)[self.dict_axis[Axis]]
                            zip_list_sort = zip(sorted_pts_axis, Pts)
                            Sort_P = zip(*sorted(zip_list_sort))[1]
                            return Sort_P
                finally:
                    self.Message = '点排序'


        # 点依次排序
        class SortPt(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点依次排序", "RPP_SortPtOrder", """以初始点依次进行排序""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("599bb86f-b653-44de-b1a9-591ed5808e1f")

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
                self.SetUpParam(p, "Pts", "P", "待排列的点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "first", "f", "指定开始元素,默认为第一个")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
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

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Pts, first):
                try:
                    re_mes = Message.RE_MES([Pts], ['Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
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
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Pt_Result, Index
                finally:
                    self.Message = '点依次排序'


        # XYZ轴顺序排序
        class SortPtGroup(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点排序（输出下标）", "RPP-SortPtGroup", """将输入的点按照坐标系排序并输出下标""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("40c698a6-1657-4619-a587-a75b8ed2614d")

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
                self.SetUpParam(p, "Pts", "Pl", "输入的点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "P", "参照平面")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "XYZ", "XYZ", "按照轴顺序排序")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('x,y,z'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Sort_P", "Pr", "排序后的点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "i", "点在原列表中的序号")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPESURBVEhLtZZ/TFNXFMfvtO+9dhbkVwlBkCW2/kLsHL9azWSJIyFGJTFgNBoxYYqDNSuCGsCkoqmuKigsYrrISBSlbaQFCwJWQZNVE3+Ly0x0if/otsRNmPgLE3s9573bapVWzdwn+ead872vPX333vNuSSj+JiRySBC+YunHZ5jna0YEwfWPXD6XWR8HSsi4f3ne+EAuX/0rIfwQz1tHOC6VDf93oAD3VBC+hhC/dMdjhSJpWCbLEgfDcI+QT0fhh6DwM8wOC06NSwoJKXSYeBaK5PY1xc8/1fQlSwlMZbKP5zei4KkP+QiJYEMh0YPaMJjTbcnQefffST+xax/mhJrGzXabvdlXrDStc/sK0ZNQg7KfwPTCU0ySrNAECqg7qvekXm+kU1xVo+nWdVzOgEk2+VjlI/XV3XSys9KM9wCxoLugPJ8gfAMFEkU3DIECCXZDjupExVCcrewQLNIn6EUfWVsS3WFwx7Qb/PN9HlSDwTDHLX+oVMZhHA4tyCaFQEOeikVj0QxySOE7yOj6Yem8ywcvJJcs3g7pT5IbFgPoOkgmZm+is9cp9Gd+3KzvbRAbSuPaclH72wGatLNoFNL96IUBO/1PkLigczosiVn9e70ZPZZGQqk4lSS102TMutlMU4/X3kVTZSutTeivohMrFrphuEm8aWxw7v8CzRczQOOs/i7tWiOd3lNLNfZqaRdNcpQbUy6ZaaLDeA93B3p8W/EMuOhARzFPt1q57JMNNfq++gLMAbzvBqhMzBjKlqLp8Z3lz+JtZVeS7OUKybUXKCLb129WthbPk4wA2SBxF83oNC1Lv3aAznJve2Hw+QSwsHDQ+hScq1Ms8FozI35eoyEt+VHMDktgmyY7K/OTf9lKk05vucMlRO0Fqx/919F2mZv1gwfp5907v2fWOwkUwL0f6TGu5BbNxk6+CVI6KB0vjjFSjm28oRmso3DtYFYwOQNNs6h/5SVeFZDAxvkdpM0d6YvPPFV/+4tuS9dM9o6Kai3Jj+0t98QeXpuJeRDabvMm3WUr1brNu5mFYAF/o00A4ZevwkTtqiqeeameTvVso2pnzRT0wvJZ+ybPtMF6CldsGD9YoFUKiQcUKK6yl6pVTsMfsW2lZ1JaiuTMDoBnCgslYo6W5Mb1brgYY/u2kFkIFsBGM4F60AjCsiSCOAqD1sEPFIiGE7F6IFR3M9JA2KVv7Zj3Ac6FpQ+gCEvHBN/t8GPILdBZkPcDpXvO8xVwDQk+Hh6VC0ALP1B5ZRyXBn8aLBD/P8C5vuu+TJb5EotAN0UFAg5rAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.h_sort = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Pts, CP, XYZ):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Sort_P, Index = (gd[object]() for _ in range(2))
                    self.h_sort = [_.upper() for _ in XYZ.split(',')]
                    re_mes = Message.RE_MES([Pts], ['Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        dict_pt_data = dict()

                        from_plane = rg.Plane.WorldXY
                        to_plane = CP
                        xform = rg.Transform.PlaneToPlane(to_plane, from_plane)
                        copy_pt = [rg.Point3d(_) for _ in Pts]
                        [_.Transform(xform) for _ in copy_pt]
                        dict_pt_data['X'] = [_.X for _ in copy_pt]
                        dict_pt_data['Y'] = [_.Y for _ in copy_pt]
                        dict_pt_data['Z'] = [_.Z for _ in copy_pt]
                        total_list = []
                        for _ in self.h_sort:
                            total_list.append(dict_pt_data[_])
                        zip_list = list(zip(total_list[0], total_list[1], total_list[2]))
                        w_sort_pts = []
                        for index in range(len(zip_list)):
                            w_sort_pts.append(list(zip_list[index]) + [index])
                        Index = [_[-1] for _ in sorted(w_sort_pts)]
                        Sort_P = [Pts[_] for _ in Index]

                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Sort_P, Index
                finally:
                    self.Message = '-'.join(self.h_sort)


        # 指定点是否共面
        class FitPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点共面平面", "RPP-FitPlane", """判断指定点是否共面""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("77574345-7551-4edf-9a62-6aa7461f03f2")

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
                self.SetUpParam(p, "Pts", "Pi", "是否共面的点集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "判断在容差范围内是否为共面点")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Plane", "PL", "公差范围内的共面平面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "是否共面")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPCSURBVEhLrZRbTFt1HMePD+5F9+IlGk182IMxMfFJow8aY2KMxvlk0Ji9KXtworColUtLIeuFXmDlVtcLG0VuLe3oha5dKXQU6lbZuA1U6JgyLDFAW9rT9vRCz9fT7gSomI3EfpNPer7f/+n390tzeoiDAohHUuNVlWlr3adsVFoll8rfwt16wNIAul3yHBuXTuTCF6/gFgcZEzdMa5qfYOPSKnO18vWUteYl1u4p6Tr7Nqw/vMDahwqeM89m3TXvsPbBom6ffg+/8ZE18hahUj3KxnuiRqpOwMN/nLUFpf1fTWJBDtY+WORs+SkERcjq61fZaE+Z+fI3dm/VZHIG7hXzlPa4KtRT1hXVOaKLHMDTcLQBWCw7lrn2HSft+F6ZGuF8yMYF0f5Tn2C+GpSRT3dvaNf70gPozegxstaGpXXl0QbkFQuefCrrr6Jh44N+8vPjfBiO9e1cKtOHVWMrtwXw/apAT1wH3ZYGuk01tNtd6IeheEBi9JuPU1bOB6wtEu1982l6siJCW+t3rYHOru6wank4+xOGUj3oCmlwMaxG7+YF9G7tY6H79gcUHtHFasDWAKiaip4WA7OtMaH5yLsmD0wE2zGc08GU1GJgW4l+hvznf2FHz4EBS+UvY56D3GXuLv3Mt4/lM3tU/eJQQt3Yn9asWHAJ+qQGvZFOGEIdBfQPwYHu4p+IHjz9Gumoe9eSUp40x5VmE6nMeKHB3RUx3Gvnod9phzFcjIlhMNqJwVjHoTMXsxRbTRBGSnmim75Yoc8pp0ehhpspNiaV+P1OLWCuwJZTAGOsDcMRBcwHMEVb4VsT4/qqpHB98GwcWhD2RMurrnTnkD3RSv29KcNqQAZLVAHrznmYyFbM3WPeTbZK/DklxOX4/dzGYo4pMBqSIDtZARhqMb7egmFSsXc+wSxJjESbO2bQh+sRETD+JTBQh4m/5LAlmmGPNeNKVA5fUAxnRM76fWxkC8YiYqSnvgaGau9/L75/7sMFEM6YVPozfoRnR4SE7yxIBw/ukAyOuBRXY1I4SRnsCTnjZQX/b/K5f0OAX+4JD91zA8wfzU02SW+iA66EFN6wGBPMRq6EBG7y6DiTzCKU9FA+zfQS10iRdBZt8MTFGEs2MYgL16Ug30t4KaF0AQp4k8KSk+8lpiiBbAkt8FHnSk6+l/BTjdJlyHEj1Vhy8r3EzQz/zB+QYTrNLzl3IAExS9c+P5flUcs4h5kMl4FXArhMuQCzGd524TUxk67+LEA3UkGIsA7h/2aD6QnkGqJz2br3/wHxdyir9PYT6wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            def _fit_plane(self, pts_list):
                Rhino.RhinoApp.Wait()
                if len(pts_list) == 1:
                    return [ghc.XYPlane(pts_list[0])], [False]
                else:
                    bool_res, plane_res = rg.Plane.FitPlaneToPoints(pts_list)
                    if bool_res == rg.PlaneFitResult.Success:
                        return [plane_res], [rg.Point3d.ArePointsCoplanar(pts_list, self.tol)]
                    else:
                        return [None], [False]

            def RunScript(self, Pts, Tolerance):
                try:
                    re_mes = Message.RE_MES([Pts], ['Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        Plane, Result = (gd[object]() for _ in range(2))
                        self.tol = Tolerance

                        pts_trunk_list = self.Branch_Route(Pts)[0]
                        if pts_trunk_list:
                            temp_res = zip(*ghp.run(self._fit_plane, pts_trunk_list))
                            Plane = self.Restore_Tree(temp_res[0], Pts)
                            Result = self.Restore_Tree(temp_res[1], Pts)
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Plane, Result
                finally:
                    self.Message = '点集是否共面'


        # 点集根据与曲线距离分组
        class CurveDistanceGrouping(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点与曲线分组", "RPP-CurveDistanceGrouping", """选出在Distance公差范围内的点""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("46d778e1-7959-4851-aae1-2d983a231676")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "与点相关的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "Pi", "待分组的点集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "与曲线距离小于此值的点")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Pts1", "P1", "满足要求点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Pts2", "P2", "未满足要求点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Indexes1", "I1", "满足要求点的下标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Indexes2", "I2", "未满足要求点的下标")
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
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUZSURBVEhLrZQNTBNnGMdvmdMsED8RdeLcBlipKFVE2utdr3dXEKZMTXAEpc5FBXFzy9T5MYSKUKhyqChhouKcYhgiU5QvB1rZdbMGhKIzBuecqQpoP+j3B+jdruttC1qXjfBLntz//7/3zeW5980DvIhoz7XQsOTcL/0CAyex0fCCF/9azdtwjB41drKCjYYXyY5enLMo7xwjZ3oTRizNm8BdLnubtT7h0mdGIrTSP4q6PmGBvTMo2tUeitCPeABf+8WbuC4zSmLMRsRPcxchLtli9BmRHEMdTUNMxTtx0+k9oLype8r8ZW6eMqdG/OzcJdharYIsNe2QrfYOZGv8HbQ3d4P2KzpwgHwkpNp7wYEOs8DZ4YCpR3YA6dkRjhtkNsyw24zq5AbUkP8QGyBaMWdJB9J3qBPtO3kNzL+knxy5zMVTZn8nfn6+FLZUFcLWml1Ca91myH4pVWi9vAK2tywBT13uDE7fbp5RWYDxnTdC+FTXVAChZSNirLJAiVExJo4qGrWo1jRu1qqiLSMBLpftHuAmysYHJ2VMY+0rgTNJ/TRQSjMywpv4IL7M9AmY1Uz7Twn7mY3+M1FbquOmx65LZ+Tr3sQHCScMsyLSSi+PeZe3ho1eQpjTUvTOwg2djAz2+PDVhe8H8RNDPHpIRG+9eDAITqlhLSDa1dYxHU7z/ArO5w0Uh7+1jvYL5Ki9b18A6ZONlRh3SSW6HCmqy2NqjxQzFqYgxiIpYiyWxpoq0xHiOj1VsILmHE7bjbjPSoXXvt/HO3GgkblFUlzbkb+AOEsHp2yycJP2tk7+YKkCom5JBW6NFKK6pUDsY9lMXC/TYn1ZdyWu3HbcTNxD9YVasb5IKzYWa8X2krvglW80vDL5ddjw7QORtVILO6vuIFSdRmit1QodDb8JHLU38fauh/Okx+kpSYk0SHVqBS6NlvmAlu0DAKA8zQzOcvlXAOA3aETEf/1EGLGx5MY4ftRaNvLJciXtH756f1pAmCiUjQYTc+j+Gd56ZkT4BQ4aEfFHdVujt12g/SaG/H0GQwLdZhTNTMivYmSYN/kHDlaQyDzGep2XOIWeP3vdIfVIIGAxG/kG75W9h+uzSMy8sxGz5jbg9n0/oLpCErEQdWJHSTXqPlaPUmXnUEd5E9xXTsKmChJ2VZJYS5uTl3KEDlqbRMPPVSRou0IK7Cqm1CTf3kryne0kMypIIKZHFogbsvLxp9kEppcXoE8VBGokCLGqqmsecYCOOL+5GTEdJxDjSQI2nSZgSwXBHDIhelifw0nOypjbcjgbfv4jAdqVTKmYUhN8ZytTHQRMPSaAyLbUN9hmBoHnP6jgfkh47nqqNxkiaE/GxwvdCiNukl/ALIo1qLFguiePDrdOCsEy1zNytMcPmbjuHRMl1pxk3JxXgZn2PsYs+x2o+eBtdKBIvoQqn51Kt/ns8C9kND1CkFF/Oki0UsXYAG/6al5DTUQkajmYiVlL1KjtiA11nOqdf7i0PHT7Zx/FUjUvzZvNPZQftPsqPU286t+nqC8QujQgXnMzF8pqoacmLKEhU7kTcdd0iRwXi2FnfSzy5Iy/Z93c6KNz3pqTnPDnpv/Lyo3U6Hmfnrw6IUSYy+89Phtxnd8ucl78CXY2WGFXUx/sUjbDtGp1IkVNZLcMD3xT43jI3rwUcinLILfqvtCtdgr7W++BA5pSgevW4ki6aQy7dHiAXGou1N+6CezvVIL9v5ihZ1pbdP/t9D8AtxNhaL+vceIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def format_tree(self, result_tree):
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            for sub_index in range(len(item)):
                                stock_tree.Insert(item[sub_index], path, sub_index)
                        else:
                            stock_tree.Insert(item, path, index)
                return stock_tree

            def rewrite_list_to_tree(self, input, none_and_holes, source):
                """
                重写列表转树的方法
                """
                # 初始化目标树
                target_tree = gd[object]()

                # 嫁接至空树
                def proc(input, empty_tree, track):
                    path = gk.Data.GH_Path(System.Array[int](track))
                    if len(input) == 0 and none_and_holes:
                        empty_tree.EnsurePath(path)
                        return
                    else:
                        for i, item in enumerate(input):
                            if hasattr(item, '__iter__'):
                                track.append(i)
                                proc(item, empty_tree, track)
                                track.pop()
                            else:
                                if none_and_holes:
                                    empty_tree.Insert(item, path, i)
                                elif item:
                                    empty_tree.Add(item, path)

                if input:
                    proc(input, target_tree, source)
                    return target_tree
                else:
                    return target_tree

            def split_tree(self, tree_data, tree_path):
                new_tree = self.rewrite_list_to_tree(tree_data, True, tree_path)
                result_data, result_path = self.Branch_Route(new_tree)
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def on_curve_pts(self, tuple_data):
                curve_list, pt_list, origin_path = tuple_data
                count = 0
                index_list = []
                while len(curve_list) > count:
                    sub_curve = curve_list[count]
                    for sub_index, sub_pt in enumerate(pt_list):
                        res_bool = sub_curve.ClosestPoint(sub_pt, self.dis)[0]
                        if res_bool and (sub_index not in index_list):
                            index_list.append(sub_index)
                    count += 1
                without_index = [_ for _ in range(len(pt_list)) if _ not in index_list]
                res_pts, without_pts = [pt_list[_] for _ in index_list], [pt_list[_] for _ in without_index]

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_pts, without_pts, index_list, without_index])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curves, Pts, Distance):
                try:
                    Pts1, Pts2, Indexs1, Indexs2 = (gd[object]() for _ in range(4))
                    re_mes = Message.RE_MES([Curves, Pts], ['Curves', 'Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        self.dis = Distance

                        curve_trunk_list, tree_path = self.Branch_Route(Curves)
                        pts_trunk_list = self.Branch_Route(Pts)[0]
                        c_len, p_len = len(curve_trunk_list), len(pts_trunk_list)
                        if c_len > p_len:
                            new_pts_trunk_list = pts_trunk_list + [pts_trunk_list[-1]] * abs(c_len - p_len)
                        else:
                            new_pts_trunk_list = pts_trunk_list
                        distance_zip_list = zip(curve_trunk_list, new_pts_trunk_list, tree_path)
                        iter_ungroup_data = zip(*ghp.run(self.on_curve_pts, distance_zip_list))

                        Pts1, Pts2, Indexs1, Indexs2 = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Pts1, Pts2, Indexs1, Indexs2
                finally:
                    self.Message = '与曲线在指定范围的点'


        # 点集根据距离分组
        class PointGroup(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点由距离分组", "RPP-Point Group By Dis", """点按指定距离分组""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ffb381c9-9d67-40af-9c68-c57301c1a1a3")

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
                self.SetUpParam(p, "Points", "Pts", "待分组的点集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "指定的距离")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point_Group", "Pr", "分组后的点集")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "分组后的点集在原列表中的下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO/SURBVEhLzVVpaBRJGK3unp57kkyOmcxkJpNEY7yNoiKIEkGIsIKKJxFdlAUVwQMFRQTRKIKKiheoEQNBlP0hKC7iriSKGMQL9M+y7rpBPBB3Xe9b/HyvupMYCSGiLD54VE3Vq/r6e/VVjfqeYbgt4XHbb4b9YBoMYufDg2z/TfS3cQJIgCOdbvcxEZzldDVGgHbMNE80xdMimT5Sn1cotlLrMV4JrqPoSzAarHa6bZiwNzcub4t7yalYSqSkjyyJRAXjfZ3pr8RA29v4Kt1LLhdmZFYoS94j0J/JUsk3rN2upEvMBGeAP4E1HADorel0VXJZJPpGMr3lWbpcHqZ6yku0UlwhU4LhFszDra5R5DIOloJc8DOYDRITjxUUySNsfAkZvMbXL4U9fyfLZHs0Rpv6ObLOkQSXgxvAURxwEQN1aWaZ5pqb2OwsDni2tqdC6nDId4p6yK84D0imU9cZyitt392jBUk5Hy+WBZEcivc4U+0Y6PHW30/10NZw03/R8rDJq8gopMxlkK0CWcrtKPPYjfew4Hcc1prsPJHSvlKXW8ggzKYNVb7AL0/g+X/uxk/Rf4D+Y7S0qdSyN0E2DozqBS7612bno6Z7y/VEiRzKTzgHhyALwjqTYeAi0PwhEG58gTlWEXXUH4BFa7H+Jcb6ebz7uGEHoDzmnYMtryF4nCrXX8avYQYtaBOW5whkP4LG+EC4icHfQcOPOlGQkr+guYpAzKTTAHHDqv0D1rDs6CnTvYHfi1EdLL+5oewHrlSN8QdO0haeATOhlnyDgDz8Msve6krbYCcsawsvChfSWy5kSxs+IABvLXR8IlSl19dwH2dFOzj/D3T8qOdYcw1ZhE2TB9wBSy2lmlnTtIaZzIfvXMhFkqnQzwF0vIAqahi1tO0MynQH6p62MgAzcHWtl7MNKbCmIS+h7bhVVKYPjXZdRNCmWFquoIVmvlYrNfU0xi5gbFduewCu3eZctAGOrCNCc0JZjyiit/waklWyKadA31hodAZAZmVW7jtW3KcW0cqaUOQ25iNgQCs/RZ5h7eMdaF1E8jngRjudLxvqKJUa7vU10z7Oc3Nm24LM05a1GdOTwRVa+BlKJgXCr5gFFzAAS5a/x/qDfMS8IB89PhvTtKUIzozZrsblxPhgMMfVdYrZvFisJi4iN8IijM91ptVCkBdOlVh2M8+GmuN4/MKGcZDj3UFNf9vbMg+Bqv3BF/jNf6pWMAuf01WFOYb5W5Uv+BBV2IDffme4ewiCQ8Bi/atrdHhz/kco9RESr7nIkzHaUwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.distance = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def split_tree(self, tree_data, tree_path):
                """操作树单枝的代码"""
                new_tree = ght.list_to_tree(tree_data, True, tree_path)  # 此处可替换复写的Tree_To_List（源码参照Vector组-点集根据与曲线距离分组）
                result_data, result_path = self.Branch_Route(new_tree)
                if list(chain(*result_data)):
                    return result_data, result_path
                else:
                    return [[]], result_path

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            if item:
                                for sub_index in range(len(item)):
                                    stock_tree.Insert(item[sub_index], path, sub_index)
                            else:
                                stock_tree.AddRange(item, path)
                        else:
                            stock_tree.Insert(item, path, index)
                return stock_tree

            def group_pts(self, tuple_data):
                origin_pts, origin_path = tuple_data
                origin_pt_length = len(origin_pts)

                point_list, group_list = [], []

                for pt_index in range(origin_pt_length):
                    for sce_pt_index in range(pt_index + 1, origin_pt_length):
                        if origin_pts[pt_index].DistanceTo(origin_pts[sce_pt_index]) <= self.distance:
                            current_pair_list = [origin_pts[pt_index], origin_pts[sce_pt_index]]

                            for pair in current_pair_list:
                                if not pair in point_list:
                                    point_list.append(pair)
                                    group_list.append(pt_index * sce_pt_index)
                                else:
                                    index = point_list.index(pair)
                                    old_group = group_list[index]

                                    for k in range(len(group_list)):
                                        if group_list[k] == old_group:
                                            group_list[k] = sce_pt_index * sce_pt_index

                dup_list = [i for n, i in enumerate(group_list) if i not in group_list[:n]]
                res_pt_list, res_pt_indexes = [], []
                for dup_index in dup_list:
                    sub_pt_list, sub_pt_indexes = [], []
                    for group_index, group_item in enumerate(group_list):
                        if dup_index == group_item:
                            sub_pt_list.append(point_list[group_index])
                            sub_pt_indexes.append(origin_pts.index(point_list[group_index]))
                    res_pt_list.append(sub_pt_list)
                    res_pt_indexes.append(sub_pt_indexes)

                for rest_index in range(origin_pt_length):
                    if rest_index not in chain(*res_pt_indexes):
                        res_pt_list.insert(rest_index, [origin_pts[rest_index]])
                        res_pt_indexes.insert(rest_index, [rest_index])

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_pt_list, res_pt_indexes])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Points, Distance):
                try:
                    Point_Group, Index = (gd[object]() for _ in range(2))
                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        self.distance = Distance

                        pt_trunk_list, pt_path_list = self.Branch_Route(Points)
                        iter_ungroup_data = zip(*ghp.run(self.group_pts, zip(pt_trunk_list, pt_path_list)))

                        Point_Group, Index = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Point_Group, Index
                finally:
                    self.Message = 'Point Group'


        # 点排序（右手定则）
        class SortPointByRightHand(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-右手定则排序", "RPP_SortPointByRightHand", """将点按平面Z向量逆时针排序，多点与原点共线按照距原点远近排序""", "Scavenger", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c37bf920-19b2-4d86-9ee4-18cfcddc05db")

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
                self.SetUpParam(p, "Points", "Pi", "点列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "FirstIndex", "F", "指定开始的元素下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "排序用平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Points_Result", "P", "排序后的点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "index", "I", "输出点在原列表中的顺序")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAL/SURBVEhL7VJdSFNxFBcqKIOIiCgiQjJFyZltLnfv3Z0u0CyioA99iEIh+qKXHnopFayIwnrxqfDFTA2/PwK1UFJDYzmbliESay4CPzbd5py6ef+/zl2XYoSkMqKHfvDj/s/hnN/5uCfin0J6q2sLV+8+opjhh7bJc2J/jdeq7sM6xRVeaJ/abiTVzizoizp3Ka7wYm0x0+x75nyrmOEDm9DvYExrfNBbcp2rGh1hc1rjsCXTiGnDZiVk9bDbUzZIbv4ToMXHscvI6TBhxs7hzEkR7c26DiVs9ZCmuBLAAHiT0PftInI6TbAOa7B1Www+WwQwP5+nhK4czMdlBcW7iFc5mNuvILvuHWBKgaUnmYpyQECAf1zglZTlg/nSdgfmRLd/WIBXZQTiRHRlXsOponfw7RSB4jRASiEKkDyczTGi3aSkLg8DPWJ3dpaIkYEUTD45CEeGGk0lF3Cs0gzbo0TMH6cCNh6YpyIQIU1zlUrqn8ECQqF9SETkxli8fyMLcPCNJ8LiycX5rpdkJ4PdpKneCrQiHTBLq6Iiiw5driKxNPwTggGLekguDt1tGgRcJGCmlbw2QGpLg/tFOtCUCpZ1CI5+AWfP8ejvphjwYD7eNz/JxSpSv0O+a2mG/yoXgFvuilYAHbznDHBuS4NrrwHeGD0mtqfCmc/hi1WH9ZFxqC3XUJwcT425OTNweo0iGQppiq8JXg11L1+I66sAc6+IyW4tbM/VsNdoMFpN3wY1FpwHKUaHuvIDmBqlNc7SFG55EprUoXuoSP6Cf4y7FBT3kHiwew6lj3lERanhcf6wQ0jiPwTpLYvLq5Rt+XSZHgEnn6lI009lRhVj4rw8Ivz042TSu7VBi8MZ8ZC8tCpG9C+TlMsk/QRjR3cGC/Q1qjpHetUYbFFhsDXxJweIpkYVPryS/Ssg6VhNapjqE0qDBUpv7RlquBODivzoEFYWRKOqMNS3XDbfi0VZXnRLsEBFwT5V9d04ffnteCFcrL+foC8rjF36ZP/jLyEi4jtfFZxJXHP09QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):  # 报错红
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):  # 警告黄
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):  # 提示白
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def split_tree(self, tree_data, tree_path):
                """操作树单枝的代码"""
                new_tree = ght.list_to_tree(tree_data, True, tree_path)  # 此处可替换复写的Tree_To_List（源码参照Vector组-点集根据与曲线距离分组）
                result_data, result_path = self.Branch_Route(new_tree)
                if list(chain(*result_data)):
                    return result_data, result_path
                else:
                    return [[]], result_path

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            if item:
                                for sub_index in range(len(item)):
                                    stock_tree.Insert(item[sub_index], path, sub_index)
                            else:
                                stock_tree.AddRange(item, path)
                        else:
                            stock_tree.Insert(item, path, index)
                return stock_tree

            def is_nan(self, angle):
                # 判断是否为失效值
                nan_bool = (not float('-inf')) < angle < float('inf')
                return not nan_bool

            def right_hand_rule(self, pts, center_pt, vec, pl):
                # 右手定则；共线的点将按点到源点的距离排序
                angle_list, collinear_list, coll_index_list, no_collinear_list, no_coll_index_list, null_index = ([] for _ in range(6))
                for pt_index, pt_item in enumerate(pts):
                    if pt_item:
                        pt_vector = rg.Vector3d(pt_item - center_pt)
                        angle = rg.Vector3d.VectorAngle(pt_vector, vec, pl)
                        # 是否共线筛选
                        if angle == 0 or self.is_nan(angle):
                            collinear_list.append(pt_item)
                            coll_index_list.append(pt_index)
                        else:
                            no_collinear_list.append(pt_item)
                            no_coll_index_list.append(pt_index)
                            angle_list.append(angle)
                    else:
                        null_index.append(pt_index)

                if coll_index_list:
                    collinear_indexes = [zip_coll_pt[1] for zip_coll_pt in zip(*self.sortbydistance(center_pt, zip(collinear_list, coll_index_list)))[1]]  # 共线点按距离排序
                else:
                    collinear_indexes = []
                no_collinear_indexes = [zip_no_coll_pt[2] for zip_no_coll_pt in sorted(zip(angle_list, no_collinear_list, no_coll_index_list), reverse=True)]  # 不共线点以逆时针排序
                res_index_list = null_index + collinear_indexes + no_collinear_indexes
                return res_index_list

            def sortbydistance(self, xyz, zip_coll):
                coll_pts, coll_indexes = zip(*zip_coll)
                distance_list = [xyz.DistanceTo(single_pt) for single_pt in coll_pts]
                sort_zip_list = sorted(zip(distance_list, zip_coll))
                return sort_zip_list

            def RunScript(self, Points, FirstIndex, Plane):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Points_Result, index = (gd[object]() for _ in range(2))
                    Plane = Plane if Plane else rg.Plane.WorldXY
                    base_pt, ref_vector = Plane.Origin, Plane.XAxis

                    if Points:
                        # 平面投影
                        projected_point_set = [Plane.ClosestPoint(_) if _ else None for _ in Points]
                        # 投影点重排序并输出下标
                        temp_index = self.right_hand_rule(projected_point_set, base_pt, ref_vector, Plane)

                        if FirstIndex is not None:
                            if 0 <= FirstIndex < len(temp_index):
                                split_index = temp_index.index(FirstIndex)
                                a_temp_list, b_temp_list = temp_index[split_index:], temp_index[:split_index]
                                index = a_temp_list + b_temp_list
                                Points_Result = [Points[single_index] for single_index in index]
                            else:
                                self.message1('索引下标不在区间范围内！')
                        else:
                            Points_Result = [Points[single_index] for single_index in temp_index]
                            index = temp_index

                    else:
                        self.message2('P端不能为空！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Points_Result, index
                finally:
                    self.Message = '点以右手定则排序'

    else:
        pass
except:
    pass

import GhPython
import System
