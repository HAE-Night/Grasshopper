# -*- ecoding: utf-8 -*-
# @ModuleName: Geometry_group
# @Author: invincible
# @Time: 2022/7/8 11:21

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import copy
import math
import Curve_group

Result = Curve_group.decryption()
try:
    if Result is True:
        # 分解几何物体
        class DestructionGeometry(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-几何物体的分解", "RPP_DestructionGeometry",
                                                                   """多个几何物体的分解（Brep，Curve等），注意直线的平面输出与曲线不一致""", "Scavenger",
                                                                   "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ed705333-be7c-459f-a18f-25152869e1c1")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "几何物体，支持多个不同的几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Vertex", "V", "物体分解后得到的点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edge", "E", "物体分解后得到的边")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Face", "F", "Brep分解后得到的面，曲线返回空")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneA", "PA", "几何物体的标准中心坐标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneB", "PB", "几何物体中心坐标沿X轴向量确定坐标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneC", "PC", "几何物体中心坐标沿Y轴向量确定坐标")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKASURBVEhLzdXZr41nGIbxXYoOplZbpaZqzdQ8lNKiaMyzA0FFHNSBiAhJK06JA+mf3OuHj+yuhGzZEndyJWuv9X3PcD/P++6xD02fxrKY+/yvSZKgi2N9rIzVsTG2hGSfxIQ1JRaFIGtjeSyNP+LP+CKmh4TbY1MsjKnxRs2KNbEjtsX3sScuxtP4N47F3jgTC+KzUMxPsTNWxMwYkaq9dCS0PicEuBLXY3ecf/n5cdyMH0MwM5kR38UvcTpGrNPyruDxb+FBVX0eX8W6kPznOBEHY3ZIILCOt4aihsTjpAMPzQ8/zgsz2B/aZp+AfGfF76EY7yjE74PMzHKMEy95K4gAqlH9l6F6FpnNt7E5JJfMe2TIZ0Ng348kOBonwyZciKthHW3RtBCIbZdDsmFjeM/Cf+KAL5JZijFOS8Iaysxrwz0cp8KLLPg4/EZW1Yp6RsC7wVa6EX+/+PhafL8Whi3RnWDVqpd/CwjWkMGywsY9ieMxyFm59+LjaxnWXyGBXdeBM+BFSayieTgnHwUZvq6GoQ+6Hd5/JRuk+vvBb0EfxqHYFx7Wod3eEEMCZ8UhtAyKsT2kwFsxWPa8zUchsw6sHR89KIHuzAZ+GxL4/kGYkXkoUrGW5Vm8Wl2bYPU8xALVOg8OlRNr0IbLc5tFrGGpLq2oDqy4qq2zzRqRygRQmYF+Hc6GhE6uK8KKkkOma/cVKVIBbt2RM/B/GSivDc5NyWvngm0/BBt0PFTJe4UpaEJSvQ0SwG3KJokHSawAZ2jCMuxfw8sSsMYwz4XTbUVdIax5Jxmi+0gSCb4J/3Ss8qVQ/aRI8OHm1IUEky4Xne2wsjbsvemt/3PHa2zsP4tgPuzdUnpeAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def explode_curve__get_plane(self, curve):
                origin_list = curve.DuplicateSegments()
                length_point = len(origin_list)
                if length_point == 1:
                    c_list = [curve]
                    curve_plane = self.get_normal_plane(curve)
                    points = [curve.PointAtStart, curve.PointAtEnd]
                    return points, c_list, None, curve_plane
                elif length_point > 1:
                    c_list = [_ for _ in origin_list]
                    point = []
                    for line in c_list:
                        point.append(line.PointAtStart)
                        point.append(line.PointAtEnd)
                    p_list = [point[i] for i in range(len(point)) if i % 2 != 0]
                    p_list.insert(0, point[0])
                    if curve.IsClosed is True:
                        curve_plane = self.get_polygon_plane(p_list) if length_point != 3 else ghc.XYPlane(ghc.Area(curve)['centroid'])
                    else:
                        curve_plane = self.get_normal_plane(curve)
                    return p_list, c_list, None, curve_plane

            def explode_brep__get_plane(self, brep):
                V, E, F = brep.Vertices, brep.Edges, brep.Faces
                length_brep = len([_ for _ in E])
                vertex_list = [i.Location for i in V]
                brep_plane = self.get_polygon_plane(vertex_list) if length_brep != 3 else ghc.XYPlane(ghc.Area(brep)['centroid'])
                return V, E, F, brep_plane

            def get_polygon_plane(self, points_list):
                x, y, z = 0, 0, 0
                for point in points_list:
                    x += point[0] / len(points_list)
                    y += point[1] / len(points_list)
                    z += point[2] / len(points_list)
                center_point = rg.Point3d(x, y, z)
                single_vertex = list(zip(points_list, points_list[1:] + points_list[:1]))
                vector_list = [i - j for i, j in single_vertex]
                axis_list = vector_list[2:]
                object_plane = rg.Plane(center_point, axis_list[0], axis_list[1])
                return object_plane

            def get_normal_plane(self, single_data):
                point = single_data.PointAtStart
                start_vector = single_data.TangentAtStart
                end_vector = single_data.TangentAtEnd
                if start_vector == end_vector:
                    origin_plane = rg.Plane(point, end_vector)
                    normal_plane = copy.copy(origin_plane)
                    normal_plane.Rotate(math.radians(90), -1 * normal_plane[2])
                else:
                    normal_plane = rg.Plane(point, start_vector, end_vector)
                return normal_plane

            def base_rotate(self, plane, axis):
                dict_axis = {1: 'XAxis', 2: 'YAxis', 3: 'ZAxis'}
                rot_plane = copy.copy(plane)
                angle = math.radians(90)
                rot_plane.Rotate(angle, eval('rot_plane.{}'.format(dict_axis[axis])))
                return rot_plane

            def RunScript(self, Geometry):
                try:
                    if Geometry:
                        temp_geo = Geometry
                        Vertex, Edge, Face, Plane = None, None, None, None
                        if isinstance(temp_geo, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_curve__get_plane(temp_geo)
                        elif isinstance(temp_geo, (rg.Brep, rg.Surface, rg.NurbsSurface,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_brep__get_plane(temp_geo)
                        PlaneA, PlaneB, PlaneC = Plane, self.base_rotate(Plane, 1), self.base_rotate(Plane, 2)
                        return Vertex, Edge, Face, PlaneA, PlaneB, PlaneC
                    else:
                        self.message2("Geometry为空！")
                finally:
                    self.Message = '几何分解'


        # 几何排序
        class Value_And_Sort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-几何排序", "RPP_Value_And_Sort",
                                                                   """几何物体的排序，排序完成进行才会进行取值，支持面积和长度的排序，但是同一组数据必须是一样的；增加点序的排序，在点序排序时输入要作为参考的坐标轴（默认为X轴对比）""", "Scavenger",
                                                                   "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a2cd7d1d-1260-43f9-8164-1f356db3927d")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "提取下标，不输入默认全部输出")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Loop", "L", "遍历取值，默认开启，会取0到index的值，关闭输入f，此时只会取第index+1个的值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Sort", "S", "选择排序方式，默认降序，升序输入a")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "在点序排序时输入，其他几何物体的排序不用输入")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "A_Objects", "AO", "若输入下标则取出0到index的几何物体，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "A_Values", "A", "若输入下标则取出0到index的值，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Objects", "BO", "若输入下标则取出index到末端的几何物体，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Values", "B", "若输入下标则取出index到末端的值，不输入默认全部输出")
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
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADBSURBVEhLzdOxCgJBDATQxU8QBL9GS+0sLCy0VEtbSy0trP1dnRwMeGfW3WSDOPCKg70J2ePSv2UHD9h0T8G5wfPNFcIyLA8dkiunC7hTKifXJrXlZBpiLaeq6/KWU3aTEbSWkzpkCdphrzn0MgH5Uw+wbyDvb2EMv80UjnAKIFvIjfSyAO0uvWbwEfn62mGrM2TTOuRrOSN/pPZySVU5Y93EVM7UDnGVM6XraipncpuElDPDTULLmTXcYdU9FZPSC6yo6H2TptWGAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.axis = None

            def get_value_sort(self, object_list, data_type, sorting):
                origin_data = None
                if data_type == rg.Brep:
                    origin_data = [o.GetArea() for o in object_list]
                elif data_type == rg.Curve:
                    origin_data = [o.GetLength() for o in object_list]
                elif data_type == rg.Point3d:
                    origin_data = eval('[o.{} for o in object_list]'.format(self.axis))
                values = sorted(origin_data)
                temp_list = sorted(enumerate(origin_data), key=lambda x: x[1])
                index_list = [t[0] for t in temp_list]
                objects = [object_list[index] for index in index_list]
                if sorting is None:
                    return objects, values
                else:
                    if sorting.upper() == "D":
                        return objects, values
                    elif sorting.upper() == "A":
                        values = values[::-1]
                        objects = objects[::-1]
                        return objects, values

            def is_sametype(self, list_data):
                Curve = [rg.PolyCurve, rg.LineCurve, rg.Curve, rg.ArcCurve, rg.PolylineCurve, rg.Polyline, rg.Line, rg.NurbsCurve]
                temp1 = [type(t) for t in list_data]
                temp1 = set(temp1)
                for x in temp1:
                    if x in Curve:
                        return True, rg.Curve
                    else:
                        copy_list = copy.copy(list_data)
                        for i in range(len(list_data)):
                            copy_list[i] = type(list_data[i])
                        temp2 = set(copy_list)
                        if len(temp2) == 1:
                            return True, type(list_data[0])
                        else:
                            return False, '数据类型不一致！！'

            def switch_handing(self, array_data, index, loop):
                if index is None:
                    return array_data, array_data
                else:
                    a_list_data = b_list_data = None
                    if loop is None or loop == 'T' or loop == 't':
                        a_list_data, b_list_data = array_data[0:index], array_data[index:len(array_data)]
                    elif loop == 'F' or loop == 'f':
                        a_list_data, b_list_data = array_data[index], array_data[index]
                    return a_list_data, b_list_data

            def RunScript(self, Geometry, Index, Loop, Sort, Axis):
                self.axis = Axis.upper() if Axis is not None else 'X'
                if Geometry:
                    g_bool, g_type = self.is_sametype(Geometry)
                    objs, vals = None, None
                    if g_bool is True:
                        objs, vals = self.get_value_sort(Geometry, g_type, Sort)
                    A_Objects, B_Objects = self.switch_handing(objs, Index, Loop)
                    A_Values, B_Values = self.switch_handing(vals, Index, Loop)
                    return A_Objects, A_Values, B_Objects, B_Values
                else:
                    pass


        # 数据类型分类
        class TypeClassification(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-GH数据类型分类", "RPP_TypeClassification", """GH几何数据类型分类""", "Scavenger", "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("871bc32c-c64a-454c-b2af-b20ed09c766f")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "Grasshopper实例化的数据类型列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Id", "ID", "物体ID（包含引用类型的物体）")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "点类型")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "向量类型")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "线段类型")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "平面类型")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep类型")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "面类型")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

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
                        self.marshal.SetOutput(result[6], DA, 6, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANtSURBVEhLlVZZaxRBEB7B238RXyQeD+qDyYsaxEQMwYgvxpMkBkNEYyCSA4lgVPRP5UEIQkQjLAoJEghustNz7By7OXa7u6yqmdkjO5ujoOid6qqvu6q+7l5jP6LD8Jz2wj7teZPKyc+CF0xIL7yvg63W2OXgohcXT+mw+EoH4Q/tBQAK6gW/dd4HHRQW0G9kdX7+RBy6t5SF6FZhcZmBNrcBnDwoy2lQssNWid3Q/4827ZsxRHORpj0JJcmBStipwA0qcLHtMsfInBiLoRpFmuYEbwdT3zd4ouiPveFwmc2NxpBVKZtmF5Rx5wReG2i7oFwvGvdh50UwEy3cqzG0YUA2e1Ja9mpdWXDUfgC6uAEqJ6IRg3ezJ3FULsRb1ktLx3gBKeyXlFrFiRRB5Moq+K9nwLn1AILx9yBXs6ALxVS78uoz51IJZ9DA8ZA0rQxsbVcdMG3aGYGI021gXeoC0dIGweRH3IUCf+wdf1fsEx9Ab2xiXM0CmAVueMHQtt1Kda+jItUW06cdEojd3oNjJ+TvDYFaF+D2PAXrcmy/2MnfHFeDAVF/lCEt6yEdmgo4aZwBpS9arjCIOHsN3DsDoLI5cG4/AnH+emTH+WD6c5RBDYZGhbICQ9r2NNWrdpIVG0e1DSY/8c7d3n7wR2c4A//FFLh3B9D+DMK3X0D+Wwe1k32ooAEMJSwsbMoCpsW74rl1E9RaLhppjkbMhBYjYSah/04MEszAnaIfOycrLMKGUo2pLP7ININ6Q+PgdD9me/BmNpVFpJwB1qqvWQ8qLMKGUs3d3sGoBwguLnTsyqJKD8CyzmjsOHc9WSCNRdhQZhHaD8AiGZ0DYf3iU5wsUMcizCBhCzaUzgGVpcKuJiyCEp0D51t0ki1nmPuAt2LFKWERps+1RhBiiw4LjfZsPYu4PCjadp/wArCychwn/sanL3KkERuX7IzH5JZtZo/j6LrHzf6G73CEFyApr1sdVCa6DdkxUWpc2oOTZidwPwQobkLJNNtj6KrgYzHKudXejvvVBBypKddyz2PIRsGbdZSfSSpXGlCKcs2xLLqwofHiHI6hmks5Z99QQTHD2dBTiJQjkAZQojfNo+hw42dpba36yOwlkMkclUFxCP81zKu8V6ZDQ+lHaKj4jfYSsuqr9gv9MDd3OA6tEcP4D2UTuWPeloOlAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Geo):
                try:
                    eliminate_list = [_ for _ in Geo if _ is not None]
                    if len(eliminate_list) != 0:
                        Id = []
                        Point = []
                        Vector = []
                        Curve = []
                        Plane = []
                        Brep = []
                        Surface = []
                        for _ in eliminate_list:
                            if isinstance(_, (System.Guid)) is True:
                                Id.append(_)
                            elif isinstance(_, (rg.Point, rg.Point3d, rg.PointCloud)) is True:
                                Point.append(_)
                            elif isinstance(_, (rg.Vector3d, rg.Vector2d, rg.Vector2f, rg.Vector3f)) is True:
                                Vector.append(_)
                            elif isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Arc, rg.ArcCurve, rg.Circle, rg.Line, rg.LineCurve, rg.NurbsCurve)) is True:
                                Curve.append(_)
                            elif isinstance(_, (rg.Plane)) is True:
                                Plane.append(_)
                            elif isinstance(_, (rg.Brep)) is True:
                                Brep.append(_)
                            elif isinstance(_, (rg.Surface, rg.SumSurface, rg.NurbsSurface)) is True:
                                Surface.append(_)
                            else:
                                self.message3("数据组未添加")
                        return Id, Point, Vector, Curve, Plane, Brep, Surface
                    else:
                        self.message2("数据列表为空！")
                finally:
                    self.Message = "GH数据类型分类"


        # 几何体中心点
        class GeoCenter(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-中心点",
                                                                   "RPP_GeoCenter",
                                                                   """求几何物体的中心点""",
                                                                   "Scavenger",
                                                                   "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("5a71f66c-d43d-4631-9a69-7c04cafb71a1")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Center", "C", "中心点")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALdSURBVEhLtZbrS6JBFMb79/ZfCLp8q7b7/Uq2S6VCgqTsVhARtETQBwvBTHclotuHtutuuUooZJFblEWQlj77nvMe653MChZ/MDjPmdd53pk5Z7Qok8l8AGApVCMDh9YpGEVaI6eC8S6D29tb7O3tYWlpCSsrKzg6OpKRt3nV4PT0FENDQ2hsbERvby8sFgvMZjM6OjpQX1+P6elpeTI/eQ18Ph/KysowMTGB4+NjPDw8yAi4HwwG0d/fj8rKSn6RfLxo4PV6efJQKCSR/CwuLqK0tBRnZ2cSUckxiEajKCkp4U8j5+fn2NjYwPb2NtLptER1aLUNDQ2iVHIM+vr64HK5ROmMjIygpqYGg4Nm7SxMvC3Ly8syqjMwMACPxyPqCcXg5OQEdXV1SKVSEgHsdjt6enp4BVlo/8vLy7G2tiYRIBKJoL29XdQTioHb7cbw8LAo4PDwENXVH5FMJlnf/fJrzcd9mpBe5v7+njXR1dWFWCwmSkcxGB0dxdzcnChwBk1NfeP+Xew3rj02btQnKIt2dna4T9hsNqyurorSUQycTif8fr8owOFw4PuPAJBJIeG24Mb1Cdeuz7hyW7XRNJxfvirPP/8+oRiMj49jfn5eFLiQsitIXseR8NpxpbXUzV+OdXd3KyuwWq2vr4DcjWdAh04Zk93nu8hPJKNb3N/c3ERtba2SEM3NzVyURhSDy8tLzmdj1c7OznKKBoN/WKcyVFx6lW9t6WYE3VWtra2inlAMCErLmZkZUToLCwucMTQBvSXdRcatIWiMqvo5OQaJRIJznHLdCKVqOBzm9DSmJjE5OYnOzk5RKjkGxP7+PoqLi7G+vi6R/IyNjaGqqgoXFxcSUXnRgKCLrqKigq+A3d3dx2Ij6Kyy9w9d48Yqf05eA4K2gs6jra0NLS0tnJZUrU1NTTCZTAgEAkpCvMSrBlm0322+AmjrDg4OEI/HZeRt3mXwPxT4XwXwD/Z9PBDIsPB/AAAAAElFTkSuQmCC"
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

            # 求边界框的中心点
            def center_box(self, Box):
                return Box.Center

            def GeoCenter(self, Geo):
                box = [g.GetBoundingBox(True) for g in Geo]  # 获取几何边界
                center = map(self.center_box, box)
                return center

            def RunScript(self, Geometry):
                try:
                    if len(Geometry) > 0:
                        Cenpt = self.GeoCenter(Geometry)
                        return Cenpt
                    else:
                        self.message2("无几何体输入")
                finally:
                    self.Message = 'HAE 中心点'

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Geometry_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "Niko_ZiYe"

    def get_Id(self):
        return System.Guid("694c7cf1-cae1-4ff6-9dbd-4cb38d949a4e")
