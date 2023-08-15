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
import Grasshopper.Kernel as gk
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper.Kernel.Data import GH_Path
import copy
import math
import Curve_group
from itertools import chain

Result = Curve_group.Result
Message = Curve_group.message()
try:
    if Result is True:
        """
            切割 -- primary
        """
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
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
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

            # 求边界框的中心点
            def center_box(self, Box):
                type_str = str(type(Box))
                if 'List[object]' in type_str:
                    bbox = rg.BoundingBox.Empty
                    for brep in Box:
                        bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))  # 获取几何边界
                    center = bbox.Center
                else:
                    center = Box.GetBoundingBox(True).Center if "Box" and "Plane" not in type_str else Box.Origin if "Plane" in type_str else Box.Center
                return center

            def GeoCenter(self, tuple_data):
                # 集合结构，待处理数据以及原树形分支
                Geo, origin_path = tuple_data
                center = [_ for _ in ghp.run(self.center_box, Geo)]
                ungroup_data = self.split_tree(center, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Geometry):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc

                        Geolist, geo_path = self.Branch_Route(Geometry)
                        iter_ungroup_data = map(self.GeoCenter, zip(Geolist, geo_path))  # 树形集合解组数据
                        Cenpt = self.format_tree(iter_ungroup_data)  # 匹配树路径

                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Cenpt
                finally:
                    self.Message = '中心点'


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
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "提取下标，不输入默认全部输出")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Loop", "L", "遍历取值，默认开启，会取0到index的值，Float关闭，此时只会取第index+1个的值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Sort", "S", "选择排序方式，默认降序，升序选择Float")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "在点序排序时输入，其他几何物体的排序不用输入")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('X'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "A_Objects", "AO", "若输入下标则取出0到index的几何物体，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "A_Values", "A", "若输入下标则取出0到index的值，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "B_Objects", "BO", "若输入下标则取出index到末端的几何物体，不输入默认全部输出")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
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
                if sorting == True:
                    return objects, values
                elif sorting == False:
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
                    if loop == True:
                        a_list_data, b_list_data = array_data[0:index], array_data[index:len(array_data)]
                    elif loop == False:
                        a_list_data, b_list_data = array_data[index], array_data[index]
                    return a_list_data, b_list_data

            def RunScript(self, Geometry, Index, Loop, Sort, Axis):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        self.axis = Axis.upper()
                        g_bool, g_type = self.is_sametype(Geometry)
                        objs, vals = None, None
                        if g_bool is True:
                            objs, vals = self.get_value_sort(Geometry, g_type, Sort)
                        A_Objects, B_Objects = self.switch_handing(objs, Index, Loop)
                        A_Values, B_Values = self.switch_handing(vals, Index, Loop)
                        return A_Objects, A_Values, B_Objects, B_Values
                finally:
                    self.Message = '几何排序'


        # 几何体的中心平面
        class GeoCenterPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-几何物体中心平面", "RPP_GeometryPlane",
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
                p = Grasshopper.Kernel.Parameters.Param_Plane()
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
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        sc.doc.Views.Redraw()
                        Plane = self.Object_Operations(Geometry)
                        Plane = self.Restore_Tree(Plane, Geometry)
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Plane
                finally:
                    self.Message = '几何中心平面'


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
                    re_mes = Message.RE_MES([Breps, Planes], ['Breps', 'Planes'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
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
            切割 -- secondary
        """
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
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object](), gd[object](), gd[object](), gd[object]()
                    else:
                        temp_geo = Geometry
                        Vertex, Edge, Face, Plane = None, None, None, None
                        if isinstance(temp_geo, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_curve__get_plane(temp_geo)
                        elif isinstance(temp_geo, (rg.Brep, rg.Surface, rg.NurbsSurface,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_brep__get_plane(temp_geo)
                        PlaneA, PlaneB, PlaneC = Plane, self.base_rotate(Plane, 1), self.base_rotate(Plane, 2)
                        return Vertex, Edge, Face, PlaneA, PlaneB, PlaneC
                finally:
                    self.Message = '几何分解'


        """
            切割 -- tertiary
        """
        # 数据类型分类
        class TypeClassification(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-GH数据类型分类", "RPP_TypeClassification", """GH几何数据类型分类""", "Scavenger", "Geometry")
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
                                Message.message3(self, "数据组未添加")
                        return Id, Point, Vector, Curve, Plane, Brep, Surface
                    else:
                        Message.message2(self, "数据列表为空！")
                finally:
                    self.Message = "GH数据类型分类"
            # 物体跟随线排序


        # 物体跟随线排序
        class GeoSortedByCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-物体随曲线排序", "RPP_ObjectSortedByCurve", """通过曲线的方向确定一组杂乱几何物体集合的排序""", "Scavenger", "Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("54118195-e4ce-423a-b238-3c92d46e8759")

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
                self.SetUpParam(p, "Geo", "G", "需要排序的物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "指引的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Result", "R", "排序后的物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "i", "排序后物体在原列表中的下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJqSURBVEhLtZRtSFNRGMdvRJJQYPbiK2lpjs3VUGuNa6ZJgmE0o0b28iGi+iLUoPo4o4kxg5CK1hsVjYZeIxrSF7EPK8TRsOaHxJJSaJWglpl7sbGdp+fcewYh6Obd/MEP/s95LvdcDuc+3BKyAt0lxQTxTzRkh7wHdayMUo+apZgAf30nNOTPvlHirQmT6ZNb2DLlPpovRZmEA0cMJFg7A1+0EHCVwueeqmesVYFapCgDQg6nRvz1ZgjWgFsoAc8TJThai77amrdVs0duoVulKIPglD4fxqsg7NaA06qER00KZ2sjn83aZegNKSbAty5V25CghvZm1R2DoXM5W6bcROkmiVGZl7fysUldx8ooWpRusGQ8QNVSTD56tEWKi4C8zzpP+nJTWTkfq9BOdL1YLURouNoY8e22kunyU7PDJYdgJAeIJ8PG2vNxFW2Q4gLMvjmuIqO1BKACIFAJkfHyKTKw6QJ8ygLXw3Q79JfR+TKX/ehtKcYg5DKYYEYP8EsHru6dEPquCwJ8SPn4NE3vsa8DMpjZDf3iEIuiQB1omljFggwcbQp768A3sh3gNw9kkg/5vdpcsTeWswd+4HG9zWgTH+a4TLQLjf/W+N0HLIMdO0BoKYBX95Tw2lY8NjHEr2ZtjvRuOAOTG/dipJvSl9OZEz/Ou6XHHNeK3tmvFP58YVGA1VhwlrX+h86YlygvVnIQrqvSO8zFGgBuGVuK0og+RwvFKokoUXpV6QhOoQvJgt6Oyyid89FRnBTon3kOpcdBj2XuUclmLWpEBfQSGt/9joPNqAltR+mXr0GTykX0NBprqC0SjvsHd+zhvsW1w2kAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
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

            def center_box(self, Box):
                type_str = str(type(Box))
                if 'List[object]' in type_str:
                    bbox = rg.BoundingBox.Empty
                    for brep in Box:
                        bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))  # 获取几何边界
                    center = bbox.Center
                else:
                    center = Box.GetBoundingBox(True).Center if "Box" and "Plane" not in type_str else Box.Origin if "Plane" in type_str else Box.Center
                return center

            def sort_points_on_curve(self, points, curve):
                param_list = []
                for point in points:
                    param_list.append(curve.ClosestPoint(point)[1])
                sorted_params, sorted_indexes = zip(*sorted(zip(param_list, range(len(param_list)))))
                return sorted_indexes

            def RunScript(self, Geo, Curve):
                try:
                    re_mes = Message.RE_MES([Geo, Curve], ['Geo', 'Curve'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        center_pt_list = list(ghp.run(self.center_box, Geo))
                        self.sort_points_on_curve(center_pt_list, Curve)
                        sorted_indexes = self.sort_points_on_curve(center_pt_list, Curve)
                        Result = [Geo[_] for _ in sorted_indexes]
                        Index = sorted_indexes
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Result, Index
                finally:
                    self.Message = '物体跟随曲线排序'

    else:
        pass
except:
    pass

import GhPython
import System
