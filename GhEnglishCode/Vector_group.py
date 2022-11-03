# -*- ecoding: utf-8 -*-
# @ModuleName: Vector_group
# @Author: invincible
# @Time: 2022/7/8 11:10
# coding=utf-8

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import copy
import Line_group
from itertools import chain

Result = Line_group.decryption()
try:
    if Result is True:
        # 多重向量偏移
        class Skewing(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@多向量偏移", "Niko_Skewing", """多向量位移""", "Hero", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3e8b5fff-1d6e-49d1-b6be-f5c5b36bc816")

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


        # 向量多次偏移取值
        class VectorAccumulation(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@多向量偏移取值", "Niko_VectorAccumulation",
                                                                   """多向量取值，向量累加，将几何多次偏移得到每次偏移的几何物体""", "Hero",
                                                                   "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ea2fff51-938d-495f-8f56-874bfa8110ce")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "原始的几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector1", "V1", "第一组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector2", "V2", "第二组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector3", "V3", "第三组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector4", "V4", "第四组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector5", "V5", "第五组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Vector6", "V6", "第六组向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "GetSingle", "S", "是否单个取值，输入't'则不会累加向量数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry1", "G1", "第一次偏移的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry2", "G2", "第二次偏移的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry3", "G3", "第三次偏移的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry4", "G4", "第四次偏移的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry5", "G5", "第五次偏移的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry6", "G6", "第六次偏移的几何物体")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                p7 = self.marshal.GetInput(DA, 7)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)
                        self.marshal.SetOutput(result[4], DA, 4, True)
                        self.marshal.SetOutput(result[5], DA, 5, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGQSURBVEhL1dXNK0VBHMbxQ9wQeUmxkJKysBFLyYodSYmdd2vZSdn7J6wVEgsveYm8FJGUbJC/QCnFhuL7zL1T4zaZe7glT33q/M6Z6XfnnjnnRH+VaoxhAuOohS/10HWNG0UlMsocPhzz8GUR7rgZeJOHdnSiAxtwJx5D53XdUn0Bd9wK7Lg25MJkEO7AbOmFSStu8ApduMdtmjuP9DEP0PwXXKMZX7KHd5QhJ8XG1t/R5lCDNXizCzUoNlUyQ2hJHgajXaQGq6byxF2Bol+lCcumCie4AtugCHWYhCZcYQAFULQ7ujCCYWiVNdAPCzZ4Sx5Gm9BgVz+UJqRfW4Aa6zi4Aj0X2ron0IRH6NlogFKBJRyk7KMPhciogb0HJdCEdVOFk/E9KDVVFOVD56ZMFU4VYjWIG7uCbVN58tsGCRxh2lSe/LZBMP+/gX0XaXv+JLoH55g1lSc7UAP7SoibcmgXbZnKid6Wh3iGBuhLdYqzGDT+Epr/BD3hjTDRB14Xss2+u8xf0gOdyJbuKIoSnwcwttkd71lBAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def sum_vector(self, single_vector):
                result_vector = rg.Vector3d(0, 0, 0)
                for i in single_vector:
                    result_vector += i
                return result_vector

            def list_handling(self, objects, list_data):
                origin_vector = [v if v is not None else rg.Vector3d(0, 0, 0) for v in list_data]
                result_list = [self.sum_vector(origin_vector[0:_]) for _ in range(1, len(origin_vector) + 1)]
                return result_list

            def move_object(self, objects, vector_list):
                d1 = copy.copy(objects)
                d2 = copy.copy(objects)
                d3 = copy.copy(objects)
                d4 = copy.copy(objects)
                d5 = copy.copy(objects)
                d6 = copy.copy(objects)

                d1.Translate(vector_list[0][0], vector_list[0][1], vector_list[0][2])
                d2.Translate(vector_list[1][0], vector_list[1][1], vector_list[1][2])
                d3.Translate(vector_list[2][0], vector_list[2][1], vector_list[2][2])
                d4.Translate(vector_list[3][0], vector_list[3][1], vector_list[3][2])
                d5.Translate(vector_list[4][0], vector_list[4][1], vector_list[4][2])
                d6.Translate(vector_list[5][0], vector_list[5][1], vector_list[5][2])
                return d1, d2, d3, d4, d5, d6

            def RunScript(self, Geometry, Vector1, Vector2, Vector3, Vector4, Vector5, Vector6, GetSingle):
                GetSingle = 'F' if GetSingle is None or GetSingle.upper() == 'F' else 'T'
                if Geometry:
                    vector_list = [Vector1, Vector2, Vector3, Vector4, Vector5, Vector6]
                    new_vector_list = self.list_handling(Geometry, vector_list) if GetSingle == 'F' else [
                        v if v is not None else rg.Vector3d(0, 0, 0) for v in vector_list]
                    Geometry1, Geometry2, Geometry3, Geometry4, Geometry5, Geometry6 = self.move_object(Geometry,
                                                                                                        new_vector_list)
                    return Geometry1, Geometry2, Geometry3, Geometry4, Geometry5, Geometry6
                else:
                    pass


        # 点序排序
        class PointsSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@点排序", "Niko_PointsSort", """点序排列角点，根据参照点自动排序点阵""", "Hero", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b852c643-79d1-48fc-9a5a-2c674bb342fe")

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
                    Result = ght.list_to_tree(res) if self.vector is None else ght.list_to_tree(map(self.re_built_sort, res))
                    return Result


        # 点序排序（分组排序）
        class PointOrderGroupingSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@点序排序（分组排序）", "Niko-PointOrderSort", """点序排序，按X-Y-Z轴分组排序""", "Hero", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9b7d7417-b3aa-4580-bb4c-1c3193c78eeb")

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
                    signle_pts = [_ for _ in copy_points if abs(eval("copy_points[0].{} - _.{}".format(self.axis, self.axis))) <= self.Tol]
                    new_tree_list.append(signle_pts)
                    for _ in signle_pts:
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

        # 删除重复的点
        class CullPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@删除重复的点", "Niko_CullPoints", """删除点列表中重复的点""", "Hero", "Vector")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("bbfb844f-0f92-43e6-be07-6a26d8de96b7")

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
                        tree_data_indexs = map(self.test, tree_data_pts)
                        if Output_Format == 0:
                            Reuslt_Pt, Index_Pt = map(lambda x: min(x), tree_data_pts), ght.list_to_tree(tree_data_indexs)
                        else:
                            Reuslt_Pt, Index_Pt = ght.list_to_tree(tree_data_pts), ght.list_to_tree(tree_data_indexs)
                        return Reuslt_Pt, Index_Pt
                finally:
                    self.Message = '删除重复点'

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
