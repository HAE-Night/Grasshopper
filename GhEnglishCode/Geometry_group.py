# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/11/5 16:31

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import ghpythonlib.components as ghc
import copy
import math
import socket
import time
import getpass
import base64
import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 分解几何物体
        class DestructionGeometry(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@几何物体的分解", "HAE_DestructionGeometry",
                                                                   """Decomposition of multiple geometric objects (Brep, Curve, etc.). Note that the plane output of a line is inconsistent with the curve""", "Hero",
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
                self.SetUpParam(p, "Geometry", "G", "Geometric objects, supporting multiple different geometric objects")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "ID", "ID", "Object ID")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Vertex", "V", "Points obtained after object decomposition")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edge", "E", "Edge of object after decomposition")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Face", "F", "The surface obtained after Brep decomposition, and the curve returns null")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneA", "PA", "Standard central coordinates of geometric objects")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneB", "PB", "The central coordinates of geometric objects are determined along the X-axis vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneC", "PC", "The central coordinates of geometric objects are determined along the Y axis vector")
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
                        ID = str(Geometry)
                        temp_geo = Rhino.DocObjects.ObjRef(Geometry).Geometry()
                        Vertex, Edge, Face, Plane = None, None, None, None
                        if isinstance(temp_geo, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_curve__get_plane(temp_geo)
                        elif isinstance(temp_geo, (rg.Brep, rg.Surface, rg.NurbsSurface,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_brep__get_plane(temp_geo)
                        PlaneA, PlaneB, PlaneC = Plane, self.base_rotate(Plane, 1), self.base_rotate(Plane, 2)
                        return ID, Vertex, Edge, Face, PlaneA, PlaneB, PlaneC
                    else:
                        self.message2("Geometry is null!")
                finally:
                    self.Message = 'Geometric decomposition'


        # 几何排序
        class Value_And_Sort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@几何排序", "HAE_Value_And_Sort",
                                                                   """The sorting of geometric objects can only be carried out after the sorting is completed. The sorting of area and length is supported, but the same group of data must be the same; Increase the sorting of point sequence, and input the coordinate axis to be used as reference during point sequence sorting (the default is X axis comparison)""", "Hero", "Geometry")
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
                self.SetUpParam(p, "Geometry", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Extract subscripts, do not input, and output all by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Loop", "L", "The traversal value is enabled by default, and the value from 0 to index will be taken. If f is disabled, only the index+1 value will be taken")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Sort", "S", "Select the sorting method, and enter a in descending order and ascending order by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Input during point sequence sorting, and do not input other geometric objects")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "A_Objects", "AO", "If the subscript is input, the geometric objects from 0 to index will be taken out, and the default output will be all")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "A_Values", "A", "If subscripts are entered, the values from 0 to index will be taken, and all outputs will be output by default")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Objects", "BO", "If the subscript is input, the geometric objects from the index to the end will be taken out, and the default output will be all")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Values", "B", "If the subscript is entered, the value from index to the end will be taken, and the default output will be all")
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
                            return False, 'Data types are inconsistent!!'

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
                                                                   "HAE@GH数据类型分类", "HAE_TypeClassification", """GH Geometric Data Type Classification""", "Hero", "Geometry")
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
                self.SetUpParam(p, "Geo", "G", "List of data types instantiated by Grasshopper")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Id", "ID", "Object ID (including objects of reference type)")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "Point Type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Vector Type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Segment Type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep Type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "Face Type")
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
                                self.message3("Data group not added")
                        return Id, Point, Vector, Curve, Plane, Brep, Surface
                    else:
                        self.message2("Data list is empty!")
                finally:
                    self.Message = "GH Data Type Classification"

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
