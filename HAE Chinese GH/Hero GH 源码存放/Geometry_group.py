# -*- ecoding: utf-8 -*-
# @ModuleName: Geometry_group
# @Author: invincible
# @Time: 2022/7/8 11:21

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Grasshopper.DataTree as gd
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper.Kernel.Data import GH_Path
import copy
import math
import Curve_group

Result = Curve_group.decryption()

try:
    if Result is True:
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

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP9SURBVEhL7VRdTNtVFG+cLuo0i9Fo5mJiNHvRRB+IZjNuDxMlpvhgpRAKBQoSIHw8FEKAYGFUKGkYDaQLLSEQIEGiDDcEFkpWxz74XisjtF2FIkMIdBa69WtQ6PV3mste1i34kfjiLzn5/8/vfNx7zzn3Cv7HvwKxWHy4oKAgNiMj4+vMzMxUoVD4figUeo6b/z6Kiorei4mJac7OznY1Njaynp4e1t3dzWpra1lqauqd5ORkFWPsTe6+fyDoQHp6ujwlJcU/Pj7OVlZWtoPB4HXsWgc5t729fclut+/SgjjVal9f31c8dH+Qy+VniouL2ebmJkPCs5DXuekhwB2FlE5PT7PCwkI2MTFRyE1PBhIfR52DGxsbu0gg4bQgISHhjfz8fGlpaalkYWHhMKdpIeHY2Ji/srKS4WQfcDoyUJqnUNcps9lMO08kDt/XoqOjz+bm5t7X6/Wsvr6epaWlOevq6pTkz31EHR0drKuraxbcM8RFRGtr66cqlYoFAoFrnBLIZLKBtrY25nK5aFELZMpqtW2oamoo4Xd7i5hMpt6WlhbyEYYDIwG1Vw8NDZFTuGlVVVUiOvrOzo4DXKLf9KM1cPO8Gf8xDodjQlOvYR6PJ1xGcJ/QArOzs3rSI6KkpOQqFgjCOdxUlKWLL1jht1/vf3BZy3zDDSGfY2oa3BcY3dDIyIiRfKEfQtkCBoNhbu9UjwC7tQ8MDNyDw0HSFQrF7QsXf1oIbbkT2Q098/V9y7wXUfoxKoXvuOJM1e3+/v7VcDBQXV29jPg/HtsHtVpt6+3tDWA3L5KOHZpx7FXoJ7furVkDPzcx7+VzId/dxXYkeSknJ+f3yclJRzgYKC8vXzMajb9x9VF0dnYaIMgXOkY66qnTaDTM7XZngXvZbzUOPfj1hplsKKesBo3GQHxPOuyvgtudn58fJz0i0DhFc3Mz83q9aaQj6N3h4WGGp+JuXl7eaUpyxxf6EJNVgFvuWV9fx0HYx+SrVCqlTU1N1K860iMCxnfa29uZTqejRh3gnHxmZoZholhSUpI1Pj7e0tDQwJxOJyVTkg98n42LizPNzc0Rd4q4xwLvznl6zAYHB9WcokU+h1zF8T2Li4v38W+AfEk2JH8a71YL7hDDe3UFeuQJ2gMCj9psttWysjK6td9wOgwEPw/7w2ea/kUikRbTw3w+3zr0t7npyYDjR8vLyy661SjJJTRPXFFR8QI3C6Kiol6JjY2VIfkvdMuRfAsxp7l5f0DAMez4yujoKNNqtSwrK8spkUhuSqXSWxhPN5VkaWmJaj4KOcHD/joQ/BnkB/RmzWKxMPSBYXroblzABsTUA+76z4BEB5H0CL5v4XuI0/81BII/AYxC1ZsWbaMIAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            # 数据转换成树和原树路径
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            def Get_different_Center(self, brep, type_str):  # 不同的物体求中心点
                if "Plane" in type_str:
                    center = brep.Origin
                elif "Circle" in type_str or "Box" in type_str or 'Rectangle' in type_str:
                    center = brep.Center
                elif "Point" in type_str:
                    center = brep
                elif "Line" in type_str:
                    center = brep.BoundingBox.Center
                elif "Arc" in type_str:
                    brep = brep.ToNurbsCurve()
                    center = brep.GetBoundingBox(True).Center
                else:
                    center = brep.GetBoundingBox(True).Center
                return center

            # 求边界框的中心点
            def center_box(self, Box):
                if not Box: return
                type_str = str(type(Box))

                # 群组物体判断
                if 'List[object]' in type_str:
                    bbox = rg.BoundingBox.Empty  # 获取边界框
                    Pt = []
                    for brep in Box:
                        type_str = str(type(brep))
                        if "Circle" in type_str or 'Rectangle' in type_str or "Box" in type_str:
                            bbox.Union(brep.BoundingBox)  # 获取几何边界
                        elif "Plane" in type_str or 'Point' in type_str or 'Arc' in type_str:
                            Pt.append(self.Get_different_Center(brep, type_str))
                            bbox = rg.BoundingBox(Pt)
                        else:
                            bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))

                    center = bbox.Center
                else:  # 不是群组
                    center = self.Get_different_Center(Box, type_str)
                return center

            def GeoCenter(self, Geo):
                center = ghp.run(self.center_box, Geo)
                return center

            def RunScript(self, Geometry):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    Geolist = [list(Branch) for Branch in Geometry.Branches]  # 将树转化为列表
                    Cenpt = ghp.run(self.GeoCenter, Geolist)  # 主方法运行
                    Cenp = self.Restore_Tree(Cenpt, Geometry)  # 还原树分支
                    return Cenp
                finally:
                    # 预知代码Bug之前（抛异常）可用
                    # self.mes_box("开发组测试", 1 | 32, "标题")
                    self.Message = 'HAE中心点'



        # 几何排序
        class Value_And_Sort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-几何排序", "RPP_Value_And_Sort",
                                                                   """几何物体的排序，排序完成进行才会进行取值，支持面积和长度的排序，但是同一组数据必须是一样的；增加点序的排序，在点序排序时输入要作为参考的坐标轴（默认为X轴对比）""",
                                                                   "Scavenger",
                                                                   "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a2cd7d1d-1260-43f9-8164-1f356db3927d")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                self.SetUpParam(p, "Loop", "L",
                                "遍历取值，默认开启，会取0到index的值，关闭输入f，此时只会取第index+1个的值")
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
                Curve = [rg.PolyCurve, rg.LineCurve, rg.Curve, rg.ArcCurve, rg.PolylineCurve, rg.Polyline, rg.Line,
                         rg.NurbsCurve]
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


        # 几何体的中心平面
        class GeoCenterPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-GeometryPlane", "RPP-几何物体中心平面",
                                                                   """求几何物体的中心平面""",
                                                                   "Scavenger", "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("718640f5-8562-4c71-9690-9d6d8f72ebca")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Plane", "P", "几何物体平面（曲线在起始点、面在中心、几何体在最大面的中心点）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM6SURBVEhL7ZNrSFNhGMfnZTqmVEODmFpTtMT60BevOHTMSxrmBZW0KZIT04lOsSwT85a2TN3CzbykZ5t5yXmBFPM257XCDCk1L6SEVBpiKmkfRufpPboPUoSmBH3oDw/n5bzv8/+d53nOS/qvvy4A0COeOI6bLqzh9svLy4e2Ng4iZKqNDI3EQ7it4sVaQ6Z8+MndKmxJ8KgVRmaW3TXH9i7CcAnAcHAWTy3r/izOkav6ciseLopKEtRtdX4w2WoD6yoyCMUx3zky3FKTtrtwfMOheXiuMkfa9TJLXLBQXpkAysbzMNNmDhs9ZIAhxB5GMYjiGQlEEp7aswQYmvTdhdrgKFbIYLWPDjCqDfAcGRGmhGEfCtWOQO9Fkji1Txlurkn/VagVR+Lj41N9fX3z/P39BWFRCfIIri9en04CRYY2fO3Q2QbsNN4rAJlTkHGTm5vbvKenp5zFYmEBwWGd/sFeIIjRhWuh+hDCpsCmSgug/yfzPQKo1tbWE0KhsKizszNZJpPZYy3KhNzC6zBXS4G5RgPwsjeASUx3u+/7AOiYmpp2x8XFRUgkEm4Y55IyT1jZmn4nUT0lJ8N0AwWCWVQYJwBooPsB6JqZmSnDw8M5aWlpl5lODp94iRmvMvL43yalZBiv0YNAFypMHARAp9N7eDxeMp/P92G5MJtEpXW9aXlX1RMYGWYa9CHIVQPYZ4vIJiYmHWjQTikpKcfPubMbo6Jj318IDsGvBFnCtMIQIr314U3VwWag5HA4yUlJSRGRkZHcLEFhE5cfAzW3DGC0UgsuuurBu2p0lLgPfwpAl8qAwWAMoK/3KS0ttc3Pzz+jUg0EVLd2j+UUFy1mFN5YdbCzgnYJA9b7qdu/KlEJMt5a76ECGpPJfO3s7HzT2NjYCs3jJINBP1UsvMfOLZB6h8YXJp61c91MFbf0CrDajw+kmfBY6gcjChtY6Tq8Nfjikmi1+/3fAAhhGObBZrOVFhYWCtSuejSTOhqNJjMyomGnbaybY6O5UUQrUbUn2mdxR9HT9ZSKjum32eW1UxJpNtyuqoausRVnjd3BhWAUBDtKVD/yAfdoGfkSOD8/f0yz/V//hEikH9g9dLOaG7vaAAAAAElFTkSuQmCC"
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

            # 根据树分支和路径还原树形
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [i for i in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 曲线类的平面
            def Curve_Plane(self, Curve):
                NurbsCurve = Curve.ToNurbsCurve()
                if len(NurbsCurve.Points) - 1 >= 2:
                    # NurbCurve 不是直线使用三点确定平面
                    NurbP = NurbsCurve.Points[1]
                    U = rg.Point3d(NurbP.X, NurbP.Y, NurbP.Z)
                    V = Curve.PointAtEnd
                else:
                    # Curve 是直线使用 UV 方向去得到平面
                    U = rg.Vector3d(Curve.PointAtEnd - Curve.PointAtStart)
                    V = rg.Vector3d.CrossProduct(U, rg.Vector3d(0, 0, 1))
                    if V.Length < 0.01:
                        V = rg.Vector3d.CrossProduct(U, rg.Vector3d(0, 1, 0))
                Plane = rg.Plane(Curve.PointAtStart, U, -V)

                return Plane

            # Brep最大面下标
            def BrepFaces_Max(self, Brep):
                # rg.AreaMassProperties.Compute(face).Area 方法是得到 Brep 各个面的面积
                BrepFaces = [rg.AreaMassProperties.Compute(face).Area for face in Brep.Faces]
                return BrepFaces.index(max(BrepFaces))  # 第一个最大值下标

            # 根据中心点求面 -- U,V与原生不符，却与SEG相符
            def Brep_Plane(self, Brep):
                # Surface
                if Brep.Faces.Count <= 1:
                    Box = Brep.GetBoundingBox(False)
                    Center = Box.Center
                    Normal = Brep.Faces[0].NormalAt(0.5, 0.5)
                else:  # Brep
                    # self.BrepFaces_Max()  求 Brep 立体的最大面的下标
                    BrepFaces = Brep.Faces[self.BrepFaces_Max(Brep)]
                    Box = BrepFaces.GetBoundingBox(False)
                    Center = Box.Center
                    Normal = BrepFaces.NormalAt(0.5, 0.5)
                # 计算法向量并给面的 Z 轴
                Plane = rg.Plane(Center, Normal)
                return Plane

            # 类型对应
            def Type_Correspondence(self, Geometry):
                if 'Point' in str(Geometry):
                    # Geometry 是 Point 类型不属于 Point3d 也转换不了 Point3d
                    #            return rg.Plane(Geometry, rg.Vector3d.XAxis, rg.Vector3d.YAxis)
                    return None
                elif 'Curve' in str(Geometry):
                    return self.Curve_Plane(Geometry)
                elif 'Brep' in str(Geometry):
                    return self.Brep_Plane(Geometry)

            # 对象多进程
            def Object_Multiprocess(self, Geometry_List):
                return ghp.run(self.Type_Correspondence, Geometry_List)

            # 物体操作：
            def Object_Operations(self, Geometry):
                Geometry_Tree = [list(i) for i in Geometry.Branches]
                return ghp.run(self.Object_Multiprocess, Geometry_Tree)

            def RunScript(self, Geometry):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    if 'empty tree' in str(Geometry):
                        self.message2('请输入几何物体')
                        return gd[object]()
                    else:
                        Plane = self.Object_Operations(Geometry)
                        Plane = self.Restore_Tree(Plane, Geometry)
                        return Plane
                finally:
                    # 预知代码Bug之前（抛异常）可用
                    # self.mes_box("开发组测试", 1 | 32, "标题")
                    self.Message = 'HAE开发组'


        """
            切割 -- secondary
        """


        # 分解几何物体
        class DestructionGeometry(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-几何物体的分解", "RPP_DestructionGeometry",
                                                                   """多个几何物体的分解（Brep，Curve等），注意直线的平面输出与曲线不一致""",
                                                                   "Scavenger",
                                                                   "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ed705333-be7c-459f-a18f-25152869e1c1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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
                        curve_plane = self.get_polygon_plane(p_list) if length_point != 3 else ghc.XYPlane(
                            ghc.Area(curve)['centroid'])
                    else:
                        curve_plane = self.get_normal_plane(curve)
                    return p_list, c_list, None, curve_plane

            def explode_brep__get_plane(self, brep):
                V, E, F = brep.Vertices, brep.Edges, brep.Faces
                length_brep = len([_ for _ in E])
                vertex_list = [i.Location for i in V]
                brep_plane = self.get_polygon_plane(vertex_list) if length_brep != 3 else ghc.XYPlane(
                    ghc.Area(brep)['centroid'])
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
                        if isinstance(temp_geo,
                                      (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_curve__get_plane(temp_geo)
                        elif isinstance(temp_geo, (rg.Brep, rg.Surface, rg.NurbsSurface,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_brep__get_plane(temp_geo)
                        PlaneA, PlaneB, PlaneC = Plane, self.base_rotate(Plane, 1), self.base_rotate(Plane, 2)
                        return Vertex, Edge, Face, PlaneA, PlaneB, PlaneC
                    else:
                        self.message2("Geometry为空！")
                finally:
                    self.Message = '几何分解'


        # Geo|Plane分隔
        class Brep_PLane_Group(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Geo|Plane分组", "Geo_PLane_Group",
                                                                   """根据Plane对几何体进行分组，所有Z轴方向需要跟第一个Plane一样，并且第一个plane必须Z轴朝外""",
                                                                   "Scavenger", "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3bab47c8-1132-4f8a-bf91-5373b81fc90b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PLane", "P", "分隔平面-第一个分隔平面的Z轴朝外")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Brep", "G", "分隔后的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "a", "I", "几何体原下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMASURBVEhLYxgFBEH9/v0szjWnDBm0/vNAhagDQv6JhnQcM2NISzvD2tJf8HTFkvCn1RPqVgc3rs7gzvqnDVVGAvjPplj82jSubUlJ8+TKbWuWB71rnlh+GyTBvHa+173/Vxj+/z/J9f/ZPvX/25Y6/586M/VKYU//dI/6/TIQA7ADz4qtahUTuxfPmRN/78Bq+/9vDyoCzWH7//8yw//FcyMvApX8Z142J+Du/1NACw4C8WEgPg7E5xj+39pj9d84b48rxCjswKZgccjLQ3r//58F6jkG1Q8yB2jevNlxF4BKkCw4gISPMvy/uVXrv3H+bgeIUdiBXdECv2e7ga4+gqafGAuub9H5b5S7wxFkUFpaGquZmRkfiI0MbAvm+T/ZpUy+BcYlx6yVBAX5dXV1qzQ0NOK1tLRSdXR0EvX09IIMVFREHarWuFNkgUXLUyNpMSELoKGWCbGx4SGBgU5Ay5T09fUdVRUU0uxzp4dQZIFl+ytDKTExZ3c/P3Vvd/eL/r6+taCgAQFZMTF/68SO5Mc7KbGg8a6pnIREsLy8PIevt/fU5IgIcYjxDAzyUlIR9vnzAyjygVnhHkcFKfEwUCR7e3oeDvbzy4sMCcny8vIykJUS83Oq3ehKvgWbdf6bZiz3UZCSiAe5ODc1VTkqPDwqwMfnBDCouuQkJa1dGvfZU+QD6/qLFqry8l7AFFSgqakZoKqlZebq6qpjZGQUrSwpaexUu8ORIgtMCvfZg1wPtEAYmDR1gCnIBYgjTUxMwoHCTPZFC30osoCYnExzC56SZAGooAIpBhZej/bpEVHYLQh5f0T1//8zUH0g/egWrJrvc/f/RYjg3+NC/2/t0P+/ZqHPl6ZJlYfdKvdrQIzCDuxL1hu0Tq08DFJ/c4cBWD/YsUDzFs+JusBgb/+fpW9yyvt96xz+T56Rcrmgp2uqY83eIGCNJA01gzgAVA/SB9I/ZUbq5b3rnP53TS54yDDzzBnWoLo14eIZn3WgSqkCxPN+6oQ1rQ+AcmkFGBgAn3YUpEfP2DsAAAAASUVORK5CYII="
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

            # 数据转换成树和原树路径
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # Geo 分隔
            def split(self, _brep_dict, _pln_s):
                _A_brep = []
                brep_negative = []
                for brep in range(len(_brep_dict)):
                    if type(_brep_dict[brep][0]) == rg.Point3d:
                        brep_centroid = _brep_dict[brep][0]
                    else:
                        brep_centroid = _brep_dict[brep][0].GetBoundingBox(True).Center  # 获取Brep物体的中心点
                    projection = _pln_s.ClosestPoint(brep_centroid)  # 生成中心点在PLN的投影点，并生成两点向量
                    normal = brep_centroid - projection

                    # 判断法线向量是否与Plane法线向量同向
                    if normal * _pln_s.Normal > 0:
                        _A_brep.append(_brep_dict[brep])
                    else:
                        brep_negative.append(_brep_dict[brep])
                return _A_brep, brep_negative

            # 主函数
            def Brep_Plane_split(self, BPSdatas):
                _brep_list = BPSdatas[0]
                _brep_dict = zip(_brep_list, range(0, len(_brep_list)))
                _plane_list = BPSdatas[1]

                brep_positive, brep_positive_index = [], []  # 返回值保存
                end_brep = []  # 保存剩余数据

                """
                可替换成for循环，针对不同的情况替换调用参数和接收返回值
                """
                if len(_plane_list) == 1:
                    brep_p, brep_nega = self.split(_brep_dict, _plane_list[0])
                    brep_positive.append(brep_p)
                    brep_positive.append(brep_nega)
                else:
                    for _pln in range(len(_plane_list)):
                        if _pln == 0:  # 参数全部brep 第一个pln
                            brep_p, brep_nega = self.split(_brep_dict, _plane_list[_pln])
                            brep_positive.append(brep_p)
                            end_brep.append(brep_nega)
                        elif _pln + 1 == len(_plane_list):  # 参数：最后剩余的brep
                            brep_p, brep_nega = self.split(end_brep[-1], _plane_list[_pln])
                            brep_positive.append(brep_p)
                            brep_positive.append(brep_nega)
                        elif _pln < len(_plane_list):
                            brep_p, brep_nega = self.split(end_brep[-1], _plane_list[_pln])
                            brep_positive.append(brep_p)
                            end_brep.append(brep_nega)
                        else:
                            continue
                return brep_positive

            # 数据整合
            def data_settle(self, __data1, __data2):
                if len(__data1) == len(__data2):
                    return zip(__data1, __data2)
                elif len(__data1) > len(__data2):
                    for i in range(len(__data1) - len(__data2)):
                        __data2.append(__data2[-1])
                    return zip(__data1, __data2)
                elif len(__data1) < len(__data2):
                    for i in range(len(__data1) - len(__data2)):
                        __data1.append(__data1[-1])
                    return zip(__data1, __data2)

            def RunScript(self, Breps, Planes):
                try:
                    if 'empty tree' in str(Breps) or 'empty tree' in str(Planes):
                        self.message3("缺少必要参数")
                        return gd[object](), gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    # 属性取值
                    breps_list = [list(_i) for _i in Breps.Branches]
                    paths_list = [_i for _i in Breps.Paths]
                    Planes_list = [list(_i) for _i in Planes.Branches]
                    # 数据处理
                    new_data = self.data_settle(breps_list, Planes_list)
                    BPSdatas = ghp.run(self.Brep_Plane_split, new_data)

                    Geo_Dtree = gd[object]()
                    index_Dtree = gd[object]()

                    # 树形数据结果匹配
                    for _1 in range(len(BPSdatas)):
                        for _2 in range(len(BPSdatas[_1])):
                            GH_PATH = paths_list[_1].AppendElement(_2)
                            BPSdatas_list = list(zip(*BPSdatas[_1][_2]))
                            if BPSdatas_list:
                                Geo_Dtree.AddRange(BPSdatas_list[0], GH_Path(GH_PATH))
                                index_Dtree.AddRange(BPSdatas_list[1], GH_Path(GH_PATH))
                            else:
                                Geo_Dtree.AddRange("", GH_Path(GH_PATH))
                                index_Dtree.AddRange("", GH_Path(GH_PATH))
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    Rhino.RhinoApp.Wait()
                    return Geo_Dtree, index_Dtree
                finally:
                    self.Message = 'Geo|Plane分组'


        """
            切割 -- tertiary
        """


        # 数据类型分类
        class TypeClassification(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-GH数据类型分类", "RPP_TypeClassification",
                                                                   """GH几何数据类型分类""", "Scavenger", "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("871bc32c-c64a-454c-b2af-b20ed09c766f")

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
                            elif isinstance(_, (
                                    rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Arc, rg.ArcCurve,
                                    rg.Circle,
                                    rg.Line, rg.LineCurve, rg.NurbsCurve)) is True:
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


        # 区分是否带孔Brep
        class BrepHole(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-BrepHole", "区分Brep是否带孔", """区分Brep是否带孔""",
                                                                   "Scavenger",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("db89262c-b474-413c-8cc2-91b6ff1bbb6f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "请输入Brep参数")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "BrepHole", "H", "Brep中带圆孔的Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "BrepNoHole", "B", "Brep中不带圆孔的Brep")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKHSURBVEhLtVbZb4xRFPe/EN6IqKVePEl4UCKUB8TSiq2oXaPxoLEkQjQeWjGmbZpUU6MtpqPLVKeiTCo6qCb1YJmI2BJpbHOX7/s5d+F7cFszdH7Jyf3uOWd+v3vOXTJTfN9fTFaVL1MC55FHKIEq+/0b3psByOFGyJEmsquQo9fhpfvhve4LLJ0gf8TEVR7le2+TliGAU0B070GmZhpY/QJkwrPB6uZBRLdAdO6EuL3djNHN5J9r4iqvZirEncOWIYBTgMf3gV0rAjJjkI9DmkB07YboPQQRP2DGrjLyz4dMXQLYGOUvh+g7ahkCuCsgEta8BP7HYYjkWbCGhW6BhkKIB2d0HmteSgIVliGAW6CnHJnaGVT+HNMCJdBRSq3ZRS3aYcaOEvJTa67MQiY0k/KnZ1+B/+EpvJc9kEO1kM/b9Yb671Pw3z0KjOZemjb7VdzYi074n0YsQwCngIbMQD4JE9GQdfwb3AK+Rxv8GaK/Uq9Oz5V5IjA1zwLuPbh3AjyyUp8M3rYG/NZGY23FYC3LwNWJuXvcZk8MpwCPbTUn5P5p8Pa1+phqi6wg3ymwxkXg0U02e2K4BeiE/CKQz5rAwgX6UsmH1don4vvBb27Q33/D+BXUFZgL11JkVk8VqbvBiZzVF/5fBbo1qvetq8FvrNOCPFZKq15PvlVkxbRPf/zMCafA+PDtmD2cAt5oK2TyHPX8IuRgNb03l8nJbTQ3OAUUuYiWmCchRq9n70HamC82mhvcArRyTa4etu5yiMQxEvhqo7nBLTB4gVa+jcj3klAZvfNHJrmCVEi3RSQqibwCYuAkHa3vNpobnAKQjFb8zZAKNf6wgdzhFphEKIE8/qsAfgJdGFoFNH4/8QAAAABJRU5ErkJggg=="
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

            # 根据树分支和路径还原树形
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 判断圆弧是否闭合
            def CurveIsRound(self, Curve):
                # 先判断是否为弧形、在判断是否闭合
                return Curve.MakeClosed(0.0001)

            # 是否为带弧度的曲线
            def IsHole(self, Curve):
                # 判断原曲线 和 曲线头尾线 两条线的中心点距离为多少
                Curve = Curve[0].ToNurbsCurve()
                Start, End, Mid = Curve.PointAtStart, Curve.PointAtEnd, ghc.CurveMiddle(Curve)
                Line = rg.Line(Start, End)
                Mid_Mid = ghc.CurveMiddle(Line)
                Curvature = abs(Mid.DistanceTo(Mid_Mid))
                return Curve if Curvature > 0.01 else None

            # 是否为闭合的 圆弧 多进程
            def IsHole_Multiprocess(self, Curve_list):
                Bool_list = list(ghp.run(self.CurveIsRound, Curve_list))  # 得到列表是否为闭合的圆弧
                return Bool_list

            # 得到合并曲线
            def Get_Curve(self, Brep):
                Curves = list(ghp.run(self.IsHole, zip(Brep.Edges)))
                return list(rg.Curve.JoinCurves(list(Curves)))

            # 去除多余的真假值
            def Remove_Excess(self, Bool):
                if True in Bool:
                    return True
                return False

            # 有无圆弧的Brep分开
            def HoleInBrep_Bool(self, Brep_Bool):
                Brep, Brep_Bool = Brep_Bool  # 两组列表
                if Brep_Bool:
                    return Brep, None
                return None, Brep

            # Brep 炸开成曲线,判断曲线是否是圆弧
            # 分类是否带圆弧的 Brep
            def Brep_Multiprocess(self, Brep_list):
                Curve_list = list(ghp.run(self.Get_Curve, Brep_list))  # 得到所有的合并曲线,查看是否是孔得到判断结果
                Brep_Bool_list = list(map(self.IsHole_Multiprocess, Curve_list))  # 判断是否带孔的数据 真假值
                Brep_Bool_list = list(
                    ghp.run(self.Remove_Excess, Brep_Bool_list))  # 简化[[False, False--]] 变为 [[False]]去重 有真则为真
                return zip(*ghp.run(self.HoleInBrep_Bool, zip(Brep_list, Brep_Bool_list)))

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    # 带孔Brep，不带孔Brep
                    BrepHole, BrepNoHole = gd[object](), gd[object]()
                    if 'empty tree' == str(Brep):
                        self.message2('请输入参数')
                    else:
                        Brep_Tree = [i for i in Brep.Branches]  # 拿到数据 二维列表
                        res = map(self.Brep_Multiprocess, Brep_Tree)  # 得到物体是否有圆的真假值
                        BrepHole, BrepNoHole = zip(*res)
                        BrepHole = self.Restore_Tree(BrepHole, Brep)
                        BrepNoHole = self.Restore_Tree(BrepNoHole, Brep)
                    return BrepHole, BrepNoHole
                finally:
                    # 预知代码Bug之前（抛异常）可用
                    # self.mes_box("开发组测试", 1 | 32, "标题")
                    self.Message = 'HAE开发组'
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
