# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Facade_group
# @Time : 2023/8/9 13:12


from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rd
import scriptcontext as sc
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
import ghpythonlib.components as ghc
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from itertools import chain
import initialization
import Geometry_group
import copy
import math
import Object_group

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:
        # 获取曲面板关键点
        class SurfaceKeyPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SurfaceKeyPoints", "F1", """Obtain the key points, corner points, center points, line center points of the surface plate""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("24ee2a86-1b41-4058-bec9-d94b8fc0fa93")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "The surface of the key point to be obtained")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Center", "C", "Whether a central point is needed")
                bool_center = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_center))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Corner", "Co", "Whether corner points are needed")
                bool_corner = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_corner))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Line_Center", "LC", "Whether a line center point is required")
                bool_line_center = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_line_center))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Center_Pt", "CP", "The center point of the curved plate")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Corner_Pt", "COP", "Corner point of a curved plate")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line_Center_Pt", "LCP", "The line center point of the curved plate")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                result = self.RunScript(p0, p1, p2, p3)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMzSURBVEhLzVV/TIxhHH/5o5l/zB+2/sA14VBkiaZdnLk1K0RFibbYUX7VLHYYa7RhO3O5kz/0G0fXVchFfszK/BgnNq5xpRYtP8ZFPxyd7v34Pu8bC9fVa/7ou3327H2e7/v5PN/v8zzfLzfcbfoCRWDa9i2Rxfs1cVWaHdHm+NiwQz4+PpG0NgaJ6yeJbkM0PiZGxkcsjZ8yalR4+taoymuV+9xdb08DrouAuxLovQR0lKL+mQHV6uXve2aEurhelWo1r1xSx48PCezjGdAaZAEGp18Q7h3dDKBKJP1sAu84B/fHc+AJaD9Pa5eBRydQowoH9zg4ZGebIhwHw0MqiMNfpPrLxs0KlG0o3rumxXYkBXwb7bqzVCD1iA9GIRrbk+NgP4/MPZLc1NlZDotJ06PNWvdgizqiKClhgVadtMiQuTvuemnRjvZ3jacAnnbspnR8LhFIPJL3Ac5y2K06QYDLzUm1A9ViDll4XyuEHaK7TEwDT3NdZo9EA4EJvHh4TIwgT7+pAbD8WuQdlEeWS8LPOanoLzDiT4H/AekCHwidJrhdFeLIvj359UG6AJ0J35gP3nQAsOeBZ7fIi8hvAvn6FDpkLwLs1rQWA6uiAf85cEZF4ltLIfgOisSTP0GSAP/FjG9WPeyTZ6Jp6kzUTpgGx/1sIinz6M8gTYBulZterHVPEs7Ip6NmVyK+fyoB7+WWSUsRgZGh2wzn6yJh9EbOIFlAAHsfQu0Z/H38m4AE9BfgCgwpL4alANpLqG6Vi/WK1TBWs1hvYHWM5p/XZYsCufpNQxNguae7LxCQPzuPp3e1uHg2o8t4atsbc2G6o8aSiY/NebR+BS9va0WBbJ26nlXTwUqwUASbC+F4VYD8nM2tCXFhWvpdSfAljCaMJQQGz/ZXG9NiHiF2JTiXUrWwIyLiK+7qKbwLHonBiHEVqDwEKBbjpGIea05jCANaGcfJrAFB9ZwtNDTZJpvReyF1RW8P3W8hdJZP1htYg2GtkfpDzc0s6JYpbtVOlD+84Tt1bh/P0Ewjl/vRMC1SNTvz8MG1d4wF6e8spt3OcmNGR45uoy05SXmS1ucLzpKM434Av7PL/RH3tGgAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.center, self.corner, self.line_center = None, None, None

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

            def get_pt(self, tuple_data):
                # 获得曲面关键点（角点、中点、线中心点）
                brep_list, origin_path = tuple_data
                corner_list, center_list, line_center_pt = ([] for _ in range(3))
                for brep in brep_list:
                    if brep:
                        sub_corner = [_.Location for _ in brep.Vertices] if self.corner else []
                        sub_center = [brep.GetBoundingBox(True).Center] if self.center else []
                        sub_line_center = map(self.line_pt, [_ for _ in brep.Edges]) if self.line_center else []
                        corner_list.append(sub_corner)
                        center_list.append(sub_center)
                        line_center_pt.append(sub_line_center)
                    else:
                        corner_list.append([])
                        center_list.append([])
                        line_center_pt.append([])

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [corner_list, center_list, line_center_pt])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def line_pt(self, line):
                # 线的中心点
                total_length = line.GetLength()
                mid_len = total_length / 2
                line_cen_pt = line.PointAtLength(mid_len)
                return line_cen_pt

            def RunScript(self, Surface, Center, Corner, Line_Center):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Center_Pt, Corner_Pt, Line_Center_Pt = (gd[object]() for _ in range(3))
                    re_mes = Message.RE_MES([Surface], ['Surface'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.center, self.corner, self.line_center = Center, Corner, Line_Center

                        brep_trunk_list, brep_path_list = self.Branch_Route(Surface)
                        iter_ungroup_data = zip(*ghp.run(self.get_pt, zip(brep_trunk_list, brep_path_list)))
                        Corner_Pt, Center_Pt, Line_Center_Pt = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Center_Pt, Corner_Pt, Line_Center_Pt
                finally:
                    self.Message = 'Surface key point'


        # 物件粗略范围
        class SmallestRegion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SmallestRegion", "F3", """Centered on the central object，find a rough minimum range in a set of objects""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("cabdbfb0-527b-49bf-b295-655680a87363")

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
                self.SetUpParam(p, "Main_Item", "M", "Central object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Order_Item", "O", "Find range object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "The number of objects in Range ")
                count = 6
                p.SetPersistentData(gk.Types.GH_Integer(count))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Order_Item", "R", "Gets the object in Range")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Order_Index", "i", "Gets the subscript of the object in the original list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Distance", "D", "Gets the rough distance of the object")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQ7SURBVEhLvZULTFtlFMcvDzcjNZhhMpQFdKna9d62dAI6hdUNXEqCS7aIWyqEFFCBCRvKkDEHGY/BEGKh8hDksZVuK48xKk6JQDsmWKDsEVcYTjayIDj3opN0LCM9nu/2QjIfS53TX3Jy7/f/n+87ud8997vU/0b0ltd2t7cVHT7ZpTrU31VwSN+SUfv2JtFqznYWN0VMjL9CoVzJjRfx0FVvm7XfaAPrr71gsw7CHVsfDPTW3s3dm5jF5/OXcnlPYGzAIIXDMFwwWN5UhIvMw5rTs1Yj3LjWNd/TU95OeXqSfBYfy3eFc/BbIwx8lQVfHtkNJzryYHSgHI41Ztzx8vJ6nCSlvR9hsJxVw9dNGXBuoATCw/wz2dkUtdRkUo0B9IKpMwfOm0oAoB+6O4sqOZ96+uJQyRzcbAQzJvR9kwenjPvhJ3MZ1JS+dxl9d5KUkxmJixhx8nGAeT1sjggqI3pC9FopzOhgfLgMcCh7d+uaj2HuKJwbVF8hPpWavHGd/WojwHQd9OqzwfRtAZh7CuECFqj+9J1JTFlC8tzdqZdbG1KtAN2QnhxxFqVlRA958dmgyTNlcNvaDtV1uR8YjOoqAAN0HMn8hfjUhymbmFPG/AtwUwvD3YUwNljKxsxEA7Q0pPazSRwr/ZYrE5Rho3i7wqGwLCnNieqyzzTj05nY7Zk6XwNJsfJ9nM+yrKJIuU+VH2M6pk2/XPFJ/M916oSJpLjQRM6nxGKxx6oXVnXibYBDuQfPwl1v1bfVb59qrd8xEhe1vgg1N4f1Z0jXPIbxHIY3EQhSqdRPIhaP43UtJ1ESicQH4xluSCDznAMXChCLRHdFIhFpSRYxw6iEQiG79/6oY0HAJwtmzQdBRNN7GZpuZxhmORnj4jXkuwgMDPRGTc8IhRkoL34PDwQu9DoWOU75+j7lgwVRENA03YHF1nMp/x6+QCArCgkpvy1/Y6gy8JU2P4FgDWc9PH4IDi6AV2VgWB3UwkkPD9ym8pdoeotOKNwYilchw9RERkb+bRs6TXZ2tquIYSpwzxfOHRbspmQseoDPly8chE7hiuHBxaOkv7FNp3ChLGL+ESySgv5VzKM56f4EB/kKB4350xZL9bS2dqfB29s3Chdowpb04lLuQSaT8bCIFls5npMW+Mt8SqPZuR3gNJ4lJ6D54EcjKD3icO7PwrvI26MI/77/i8FLl7pnzObaBpQc8+Uy0QqNVpV07frJWwBDYLtyGPakb01nTScpLU5Mu4U/G4AfMcZgcqIJAsR8KfFczfpdA2RhADPAbCvUqbeRY3bxb+QEvBGLZh5gAuz2Prg+qYODVTusPB7vSWJ6jPfm2cDWBBfPfAaVxfEzEtpvHTvNedyONud+PjGKx71hP+g1aZAYK0/jPMqlvjhGq6tKGo2PDlXh+HmH/I9xSVHKMiqKY3WJSnkcp/3XUNTv1/bgR7VU1H4AAAAASUVORK5CYII="
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

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

            def closest_object(self, tuple_data):
                main_object, origin_object, origin_path = tuple_data
                other_object = map(self._trun_object, origin_object)
                new_object = [other_object[:] for _ in range(len(main_object))]
                origin_new_object = [origin_object[:] for _ in range(len(main_object))]

                total_object, total_index, total_dis = [], [], []
                for obj_index, obj_item in enumerate(main_object):
                    if obj_item:
                        main_pt = Geometry_group.GeoCenter().center_box(obj_item)
                        other_pts = map(Geometry_group.GeoCenter().center_box, new_object[obj_index])
                        sub_tuple_list, sub_distance = [], []
                        for pt_index, pt in enumerate(other_pts):
                            if pt:
                                dis = main_pt.DistanceTo(pt)
                                sub_distance.append(dis)
                                sub_tuple_list.append((dis, pt_index))
                        sort_split_list = sorted(sub_tuple_list)[:self.count]
                        sort_index_list = [_[1] for _ in sort_split_list]
                        sort_object_list = [origin_new_object[obj_index][_] for _ in sort_index_list]
                        sort_dis_list = [sub_distance[_] for _ in sort_index_list]
                        total_object.append(sort_object_list)
                        total_index.append(sort_index_list)
                        total_dis.append(sort_dis_list)
                    else:
                        total_object.append([])
                        total_index.append([])
                        total_dis.append([])

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [total_object, total_index, total_dis])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Main_Item, Order_Item, Count):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Order_Item, Order_Index, Distance = (gd[object]() for _ in range(3))
                    re_mes = Message.RE_MES([Main_Item, Order_Item], ['M end', 'O end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.count = Count
                        structure_tree = self.Params.Input[1].VolatileData

                        main_trunk_list, main_path_list = self.Branch_Route(Main_Item)
                        order_trunk_list = self.Branch_Route(structure_tree)[0]
                        zip_list = zip(main_trunk_list, order_trunk_list, main_path_list)
                        iter_ungroup_data = zip(*ghp.run(self.closest_object, zip_list))
                        Res_Order_Item, Order_Index, Distance = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Order_Item, Order_Index, Distance
                finally:
                    self.Message = 'Rough minimum range'


        # 沉头螺钉
        class CounterBore(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CounterBore", "F2", """Input specifications automatically generate countersunk screws (including M4, M5, M6, M8, M10, M12, M16, M20)""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("cd1d9326-a9eb-4e6e-8c7b-b299cc87f168")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Code", "C", "Screw number")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Deep1", "D1", "Depth 1")
                DEEP_LENGTH_1 = 5
                p.SetPersistentData(gk.Types.GH_Number(DEEP_LENGTH_1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Deep2", "D2", "Depth 2")
                DEEP_LENGTH_2 = 10
                p.SetPersistentData(gk.Types.GH_Number(DEEP_LENGTH_2))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Alum_Material", "AL", "Aluminum screw")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Iron_Material", "FE", "Iron screw")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN0SURBVEhL7ZZrbExBFMcvRcRuQkO9H6lI2Tt35j732rVsPeqLFKW79KGsNqSKCBIVr6JtImmi4pFNxCf1aCtU4pUQkfhSJBKJRPggfPEKVYIEXT3O3DttVUW3X3zyS/7ZmXPOzJkz596blf450NiYAgD9o5KUIkzJ0k/8/p01c8LFq8Mzt6WnpeWujc17eDy+/k5t5Yrm2uqinqosaj52eG3zvu2Rh17v4N1ii16hqIWoAbH8zBNfW85iQbcA2i/h7+VfxOfXUdegfNOiux6PZ5SzujfGpqbOGO7xFOBKp+SsMDn47FEcEh8b4fubU51qw8QfXtdBSeHsGxg2mMf2Ct80NjNYNo/4jj6oqfEIszR/FmloaiiHC3Vb4fzJLY6amnZCaSzrObqT2/wXxqGWukOXyCL/LvjQANDaAO0tZxwBXIGjB1bfFyF9YjJquTt0ycsNVjkJ3tfDj3dnHPE+YKPvipA+kXSCg1VFd0RIn/ifoFcmoSLu0KUgggk+nQPAdwFa613BVThUvbJvCQCkfmZ6uj3c6y0VJoel2f7ajgoSb0+j3Aoqd0SfiJDk2Zubk79qbngr7tD5sRs/elhmTrZ/+/Kc6euiSwKbly32b4xEgpuoPCEmQpJDUZQNMiGPKaWvNI09s20bP6pdZGSQsmnTyG3UxaEjJprCLAWDll9V2WlJMgfyuW1bcdxjm+PsAA2rDF0HpihVPp8viyrKCcZYnXBLus62MKoA+kox9giqRrgkwzAKVcaAjwO2vUfXNCCEzHacnIqKiv4KIa9USm8KUw8oIacYpS/EtBumaUaJLLeGQoESvjkeYplwuaiqOo6fwLKMMmHqAVYznTH6Tde1p4FAoFCYHTBBjspoQlNVkGW5XJi7wICJPAHeebEw/RHsEcNKrxq6BpqmxoXZSYBXmkC1Y0y1MHeBWQdhiZ8xsF6Y/gojpIQfCO9+DJ+bphbFxJ+wymJux/50e48csCn7LdOEYDC4OxwOzbct47BpGCeFW/L7zX2hUKhgwYIsn21ZcdywDQ80lPssS8/D/jhNppQcEEmm8nkn0Wg0BRt5BMv8gsEJ1HMqy52PKfr4wjYu9L3Eq1giXPgUsWxc1yLLmV4+p1S5hwe+6Dh/B081RNO0NDHthqZNScNryOBXKkwOzuEoTcVhxz+LFIwbKUmS9BOlob6a9irK0QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.al_specifications = {'M4': (4.5, 9.6), 'M5': (5.5, 11.6), 'M6': (6.5, 13.6), 'M8': (8.5, 17.8), 'M10': (11.0, 22.0), 'M12': (13.0, 26.0), 'M16': (17.0, 32.0), 'M20': (21.0, 38.0)}
                self.fe_specifications = {'M4': (6.0, 9.6), 'M5': (7.0, 11.6), 'M6': (8.0, 13.6), 'M8': (10.0, 17.8), 'M10': (12.0, 22.0), 'M12': (14.0, 26.0), 'M16': (18.0, 32.0), 'M20': (22.0, 38.0)}
                self.deep1, self.deep2 = 0, 0

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

            def counter_bore(self, tuple_radius):
                origin_pln = rg.Plane.WorldXY
                normal = origin_pln.Normal
                small_radius, big_radius = tuple_radius
                big_circle = rg.Circle(origin_pln, big_radius).ToNurbsCurve()
                small_circle = rg.Circle(origin_pln, small_radius).ToNurbsCurve()

                deep_vector_one = normal * (0 - self.deep1)
                deep_vector_two = normal * (0 - self.deep2) + deep_vector_one

                copy_one, copy_two = (copy.copy(small_circle) for _ in range(2))
                copy_one.Translate(deep_vector_one)
                small_circle_one = copy_one
                copy_two.Translate(deep_vector_two)
                small_circle_two = copy_two

                # start_pt = big_circle.PointAtStart
                # end_pt = small_circle_two.PointAtEnd
                unset_pt = rg.Point3d.Unset
                loft_brep = rg.Brep.CreateFromLoft([big_circle, small_circle_one, small_circle_two], origin_pln.Origin, unset_pt, rg.LoftType.Straight, False)[0]
                res_brep = loft_brep.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance)
                return res_brep

            def RunScript(self, Code, Deep1, Deep2):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Alum_Material, Iron_Material = (gd[object]() for _ in range(2))
                    self.deep1 = Deep1
                    self.deep2 = Deep2
                    if Code:
                        if Code in self.al_specifications.keys():
                            order_sp_al = self.al_specifications[Code]
                            order_sp_fe = self.fe_specifications[Code]

                            Alum_Material = self.counter_bore(order_sp_al)
                            Iron_Material = self.counter_bore(order_sp_fe)
                        else:
                            Message.message1(self, 'This screw specification is not included！')
                    else:
                        Message.message2(self, 'Screw specifications are not inputted！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Alum_Material, Iron_Material
                finally:
                    self.Message = 'Countersunk head screw（hole）'


        # 面板折边（规整铝板）
        class Surface_flanging(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Surface_flanging", "F12", """Panel folding, suitable for regular aluminum plate, special plate need semi-manual work""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4ffb7d64-abfe-46ec-95af-f2de4fb17088")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "fold_surface", "S", "original surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "fold_size", "S", "Universal folding width")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(20))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edge_Tree", "EL", "Curve list, enter the edges that need to be defined,if no input,make folding uniformly")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Size_Tree", "SL", "folding width list, control the list of curve value, quantity must be consistent with curve list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Fill_Brep", "R", "Combine face after offset folding")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Folded_Surface", "S", "edge after offset make up of face偏移的边写组成的面")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                result = self.RunScript(p0, p1, p2, p3)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPXSURBVEhLrVV7TJVlHH6otC06CB5u5/u+Q8y20+xCF3Jmf7g2WvFHLsulrXCDwpBzCjcxMMdF8nIucvEcGXpwbsIoKJAQYmPMZltauWjNamtrmuZ/bqIgGsrt6fedXtqRvg6s9WzPztl3zvv8fu/ze973w0JQC0ey+bkPxor90LMiD/9P7IX2cx308gosORtEOg/A+KYBRoUUzlZ/+e/wQX+mCRksQyqLX1jJ4mUuupHID4V1SGMI+o+yq4DsbnU1Hl6sli0cXmjNTXAwX8/k2I0ODg9/xIG+Su5yr+E7Lhc3S6FqLGG9FAtCP98AZ6OsWRNG9iIl8e/ww24LQB8ug43e99aS/Jwc+YSc6JHvfbw23MYvBmvoL13HokeXcxOS6IOd+6CfURKx4Ye+sRlObpQOz3zlJW91c/rKx3+T1zrI259Fio2NtPPUaR/3bFnLN+IS+/fDKKsG7lFS1vBBO1mLFBaveJyT412cGW6/o0A0eVWK8QR7Ot7ntohl+pciEfeXkgVqobkkKdNuxPNIXWHEnrmi0TSLT90+Rs+qp8SiZLHKeFFJWcMLfXczDObFp/HCrwfJsU5L4Vma9n132s+34pLYAO23mPaEgUXi/4WdkpDyV58jZ45zxkI0muYOfSWvsErsqYVeo6SssRdG7kHJfgHuZ3/ndnLquKXoLM1kXb3cwgItU8TTpgJwPqikrCE57myUE1vwwDKOXmmLpGWuaDQ53cvutlJ6JM4yt0ElY409SE2THP9RKt0Htq6bf7hCTvdwa+6zMtilMmBtvZKyhlwNJYcl+3l3JXLo6wA5fmf255I3u/jL2SDzFydLNLXL1XDcp6SsIen5ISAx86x6klO3jsXMvklzh6GqN7kdCVLACCoZa/jhfDok3W+W7B8NFcniPkvRWZqH6+ZoOwtdD8lwU7kb2hNKyhrSfVMYOvMS0nnpfHj+7E/2cLC3gkXSfcN8988BaHbJ/kSVZH/HhhzpvtdSNJrmf3a8niOdJ1EuxSIlZQ0vMpLkgmp9W4b7rXmxcUD8txY2ae7u93OHmG9ziPeO63Uwliqp2HjpXntLsOw1Dn1fz5mJ7sgceP3TfxaQ50fqN7FUsi/DbVHL54e8Dgsr5bi7707htpyVbA17ePHi4YgdpufmoTOTNTneyeLsLMl9Cr3yNlPLF4S4QzAek2Hv3IXEn0qkQ09KBmvycznQX8nREbP7Exw65eO74r0M9xxjXcuxYC48iszVIaQ3fgDbJbfsbMsjy9nsF2vynh+rQMLJejhjn9yFohVZ8S1wvhyAvb0cthuFsHWpn2IA+BNdH1pgtsWiXQAAAABJRU5ErkJggg=="
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

            # 重新定义向量的长度
            def ver_lenght(self, vec_size):
                vector, size = vec_size
                unit_vector = vector / vector.Length  # 将原向量单位化
                new_vector = []
                if "float" in str(type(size)):
                    new_vector.append(unit_vector * size)  # 创建新的向量，长度为new_length

                elif len(size) >= 1:
                    for i_vce_ in size:
                        if i_vce_ != 0:
                            new_vector.append(unit_vector * i_vce_)
                        else:
                            new_vector.append(0)
                return new_vector

            # 数据自动补齐
            def data_polishing_list(self, data_a, data_b):
                fill_count = len(data_a) - len(data_b)
                # 补齐列表
                if fill_count > 0:
                    data_b += [data_b[-1]] * fill_count
                return data_b

            def add_fillet_to_edges(self, fillet):
                brep_surface, fillet_vector = fillet
                # 获取曲面的边界

                edges = [cur for cur in brep_surface.DuplicateEdgeCurves()]
                one_surface = [brep_surface]
                one_surface2 = []
                if len(fillet_vector) == 1:
                    for edge_g in edges:
                        one_surface.append(rg.Surface.CreateExtrusion(edge_g, fillet_vector[0]).ToBrep())
                        one_surface2.append(rg.Surface.CreateExtrusion(edge_g, fillet_vector[0]).ToBrep())
                else:
                    if len(edges) == len(fillet_vector):
                        for i_num_ in range(len(edges)):
                            if fillet_vector[i_num_] != 0:
                                extrusion = rg.Surface.CreateExtrusion(edges[i_num_], fillet_vector[i_num_]).ToBrep()
                                one_surface.append(extrusion)
                                one_surface2.append(extrusion)
                    else:
                        for i_num_ in range(len(fillet_vector)):
                            extrusion = rg.Surface.CreateExtrusion(edges[i_num_], fillet_vector[i_num_]).ToBrep()
                            one_surface.append(extrusion)
                            one_surface2.append(extrusion)
                Brep = rg.Brep.CreateBooleanUnion(one_surface, 0.01)[0]
                Brep2 = rg.Brep.CreateBooleanUnion(one_surface2, 0.01)[0] if one_surface2 else None
                return Brep, Brep2

            def RunScript(self, fold_surface, fold_size, Edge_Tree, Size_Tree):
                try:
                    # 传参判断
                    re_mes = Message.RE_MES([fold_surface], ['fold_surface'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc

                        # 参数定义处理
                        fold_vector_count = []
                        for surface in fold_surface:  # 面法线获取
                            fold_vector_count.append(-(surface.Faces[0].NormalAt(0.5, 0.5)))

                        # 根据参数输入进行向量生成
                        if (Edge_Tree.DataCount == 0) or (Edge_Tree.BranchCount >= 0 and Size_Tree.DataCount == 0):
                            ver_zip = list(zip(fold_vector_count, self.data_polishing_list(fold_surface, fold_size)))
                            fold_size_count = ghp.run(self.ver_lenght, ver_zip)
                            fold = list(zip(fold_surface, fold_size_count))
                        elif Edge_Tree.BranchCount >= 0 and Size_Tree.DataCount > 0:
                            if Size_Tree.BranchCount == 1:
                                ver_zip = list(zip(fold_vector_count, self.data_polishing_list(ght.tree_to_list(Edge_Tree), [ght.tree_to_list(Size_Tree)])))
                            else:
                                ver_zip = list(zip(fold_vector_count, self.data_polishing_list([data_ for data_ in Edge_Tree.Branches], [data_ for data_ in Size_Tree.Branches])))
                            fold_size_count = ghp.run(self.ver_lenght, ver_zip)
                            fold = list(zip(fold_surface, fold_size_count))

                        Fill_Brep, Folded_Surface = zip(*ghp.run(self.add_fillet_to_edges, fold))

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Fill_Brep, Folded_Surface
                finally:
                    self.Message = 'HAE surface folding'


        """----------待翻译插件-----------"""


        # 平面的X轴标注（水平标注）
        class HorizontalAnnotation(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_HorizontalAnnotation", "F4", """X-axis dimension of the plane (horizontal dimension)""", "Scavenger", "H-Facade")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def get_ComponentGuid(self):
                return System.Guid("98d10c28-3162-479a-932b-2c790a1af1cc")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Start_Pt", "SP", "Dimension starting point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "End_Pt", "EP", "Dimension ending point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "The referenced plane,default is world XY")
                PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Mark the offset distance")
                DISTANCE = 1
                p.SetPersistentData(gk.Types.GH_Number(DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Align_Line", "L", "Align the dimension to line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Overwrite", "W", "Dimension data overwrite")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension set")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Real_Value", "RV", "Real value of dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Show_Value", "SV", "Dimension display value")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPVSURBVEhLvZR/bFNVFMe3ti8ODE4UF2FGdI6J79537+u2rl27rHFsS0exydgPliBGUrexiXQjRBKzxTiHiwQWS8QsoyAQCKjtSIjK4hJ/hB+bMYiGMMRfMWrwRxxzGpgG3PV7X9829gP8p/hJvrnnnHfeOfee29ckSZ6eqdaufrTUcBJNuT+XnuvfNnrlz5jYuS34ohlOHMHHvT5xJSaEGBBv7Q29bYYTiq1lU3lka/ua82VlLMuMJZwSaEfcvDWUQ91x89YgG+yKm0mu1NRUu2mPY4HugRZAd0Jp0DzoeuaAlXKNu1ORDcLQbaFGv3DnZT1vRE3wYrrNZjtrtVq/S05O/lVRbF8qivVl8/E4t9evLRErfDlbTH8KsnP7qsrC0P6u9WOw7zCi01AUy1o0+Fma8chUWjet3PXa9tq/Yd4Vj0xSBr3T29NyMbw1eKmggDe73Wyj2601u1ykyeGiz2jaQ08h52k0OLdo0d0BQjKDqppRr6oPTIiSxXu/OvMqTpE7/XRJhTabdeSnL7rF2OUjQoz0iLHfY1BU/DMcFWL0qBj8ZIewWpMPIvd023M1l8VYr7g29OYU/fXLIXxPx0RXZ+0PyJMjz5DFJSXY2ccn3m0b3bOzYWh9bekbjcGS6LhC9cujq6sKosjpgD73FfF9LZsrT27eEDhxvTY2+geHf9wvmtb5j6BmDMo2qgN5yR0b6nzdr3Q8ORIPzcRisVSjwW+mO4NlXq3lcKRJwFSh16GJX+MqqAu6d3v7E6LQQ0JGdBopKSmLFUWpNt0ZhBqWX1xTU/iB6fZAEw3krIqk8fCS9LbMjIWzNvgPlKVLFu6ZO1fhpi/HNP17Sij/YwOv12tzOp3M48lz+f3++eOxQCAwr6qqyurxeO43Ek2Ki4tT8/Pz5d/FzZhsYNe0ZTpnlxijfTrnXzuduRWMsQc516IOB9d1nV+12+01RjJgTBuklHxkujdisgGlj1RzzvqlraqqDwW+z87OLqJU7c3h3KNRehWxD+XzXF33cqYJQsh70r8JUSh+4YyRCux2wHAACp7lnNdjjWH7xVh7KaX9DoeDcI3slnEpM/1GHIOoYWmaVokGx6Wdz1gajv8tGvhR9CjWUjw/wAhpwKhOy9FgQysoIX3Gy7MQCdd1Xji/+1rPvub4KVGoHHfwh8ORs0Vn7AxV1VbEljJNOyUbYbfvu1yuOXZdFyjcifuhiH1qvDwTy0Bf+7AQn4mhbyLyq5YjYmkaIc9ipy9gto/JWE5W1gL4ATRIxyr/bZNwigrY90HzYRt5s/FSa826gVPhC5FwXee/PztAyjSROysAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pln, self.style, self.dim = (None for _ in range(3))

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

            def _get_dim(self, pt_tuple_data):
                sub_start_pt, sub_end_pt, sub_dis, sub_over_data, sub_align = pt_tuple_data
                self.pln.Origin = sub_start_pt
                if sub_align:
                    above_pt = sub_align.ClosestPoint(sub_start_pt, True)
                    offset_dis = above_pt.DistanceTo(sub_start_pt)
                else:
                    offset_dis = 0

                offset_pt = rg.Point3d(self.pln.OriginX, self.pln.OriginY + sub_dis + offset_dis, self.pln.OriginZ)
                ann_type = rg.AnnotationType.Rotated

                sub_dim = rg.LinearDimension.Create(ann_type, self.style, self.pln, self.pln.XAxis, sub_start_pt, sub_end_pt, offset_pt, 0)
                if sub_over_data:
                    sub_dim.RichText = sub_over_data
                real_dim_value = sub_dim.NumericValue
                show_dim_value = sub_dim.PlainUserText
                return sub_dim, real_dim_value, show_dim_value

            def get_uv(self, pt):
                res_bool, u_vaule, v_value = self.pln.ClosestParameter(pt)
                pt_2d = rg.Point2d(u_vaule, v_value)
                return pt_2d

            def run_mian(self, tuple_data):
                start_pt_list, end_pt_list, dis_list, over_data_list, align_line_list, origin_path = tuple_data
                s_len, e_len = len(start_pt_list), len(end_pt_list)
                if s_len > e_len:
                    start_pt_list = start_pt_list
                    end_pt_list = end_pt_list * s_len
                    dis_list = dis_list * s_len
                    over_data_list = over_data_list * s_len
                    align_line_list = align_line_list * s_len
                elif s_len < e_len:
                    start_pt_list = start_pt_list * e_len
                    end_pt_list = end_pt_list
                    dis_list = dis_list * e_len
                    over_data_list = over_data_list * e_len
                    align_line_list = align_line_list * e_len
                else:
                    start_pt_list = start_pt_list
                    end_pt_list = end_pt_list
                    dis_list = dis_list
                    over_data_list = over_data_list
                    align_line_list = align_line_list
                sub_zip_list = zip(start_pt_list, end_pt_list, dis_list, over_data_list, align_line_list)

                res_dim_list, real_v_list, show_v_list = zip(*map(self._get_dim, sub_zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_dim_list, real_v_list, show_v_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Start_Pt, End_Pt, Plane, Distance, Align_Line, Style, Overwrite):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.pln = Plane
                    self.style = Rhino.RhinoDoc.ActiveDoc.DimStyles.Find(Style, True)
                    if not self.style:
                        self.style = Rhino.RhinoDoc.ActiveDoc.DimStyles.FindIndex(0)
                        if Style:
                            Message.message2(self, "The dimension style for the '{}' type does not exist".format(Style))

                    Dimension, Real_Value, Show_Value = (gd[object]() for _ in range(3))

                    sp_trunk_list, sp_path_trunk = self.Branch_Route(Start_Pt)
                    ep_trunk_list, ep_path_trunk = self.Branch_Route(End_Pt)
                    dis_trunk_list = self.Branch_Route(Distance)[0]
                    over_trunk_list, align_trunk_list = self.Branch_Route(Overwrite)[0], self.Branch_Route(Align_Line)[0]
                    over_trunk_list = over_trunk_list if over_trunk_list else [[None]]
                    align_trunk_list = align_trunk_list if align_trunk_list else [[None]]

                    sp_len, ep_len = len(sp_trunk_list), len(ep_trunk_list)

                    re_mes = Message.RE_MES([Start_Pt, End_Pt], ['SP terminal', 'EP terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if sp_len > ep_len:
                            trunk_path = sp_path_trunk
                            new_sp_trunk_list = sp_trunk_list
                            new_ep_trunk_list = ep_trunk_list + ep_trunk_list * (sp_len - ep_len)
                            dis_trunk_list = dis_trunk_list * sp_len
                            over_trunk_list = over_trunk_list * sp_len
                            align_trunk_list = align_trunk_list * sp_len
                        elif sp_len < ep_len:
                            trunk_path = ep_path_trunk
                            new_sp_trunk_list = sp_trunk_list + sp_trunk_list * (ep_len - sp_len)
                            new_ep_trunk_list = ep_trunk_list
                            dis_trunk_list = dis_trunk_list * ep_len
                            over_trunk_list = over_trunk_list * ep_len
                            align_trunk_list = align_trunk_list * ep_len
                        else:
                            trunk_path = sp_path_trunk
                            new_sp_trunk_list = sp_trunk_list
                            new_ep_trunk_list = ep_trunk_list
                            dis_trunk_list = dis_trunk_list * sp_len
                            over_trunk_list = over_trunk_list * sp_len
                            align_trunk_list = align_trunk_list * sp_len

                        zip_list = zip(new_sp_trunk_list, new_ep_trunk_list, dis_trunk_list, over_trunk_list, align_trunk_list, trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.run_mian, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    no_rendering_line = self.Branch_Route(Dimension)[0]
                    self.dim = list(chain(*no_rendering_line))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Dimension, Real_Value, Show_Value
                finally:
                    self.Message = 'Horizontal Dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass


        # 平面的Y轴标注（垂直标注）
        class VerticalDimension(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_VerticalDimension", "F5", """Y-axis dimension of the plane（Vertical Dimension）""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("220a1e09-0934-4da6-8a0f-4214161c86f7")

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
                self.SetUpParam(p, "Start_Pt", "SP", "Dimension starting point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "End_Pt", "EP", "Dimension ending point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "The referenced plane,default is world XY")
                PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Make dimension for the offset distance")
                DISTANCE = 1
                p.SetPersistentData(gk.Types.GH_Number(DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Align_Line", "L", "Align the dimension to the line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Overwrite", "W", "Dimension data overwrite")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension set")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Real_Value", "RV", "Dimension true values")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Show_Value", "SV", "Dimension display value")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP/SURBVEhLrZV9TBNnHMdbjlKtsmUixhkGAYsNvdfeXTtCDyuIxOnmdLSZZsqy7MVtycIYLWZg2iU4ZQRYiFt0g0hC2CYosTDnWxxZohtG3XtIZhxDZfGPOeZeHIbNcPs+15uzwFVI9km+eX7P75677z3P87vnTASPYHc++0RRqdb5v9mwVmYGBxpvjv3Ro4ary1qRegRaN40eghQoA5qC2+1e5hKEN3me38NxXLmeNpme3uxbrY71qKp6Rt0V3jiCVNskvQs1Qh0pluQbVqvlQ8QpUBySy1XJc9z3oiBUCTx/kaXpFv2SKXl3w1N10f3buvx+T7aei+Ph1Z7Stj0V56981zoxPLhX3d30/PBy7x1vCURRqGIY5gCJi4sVJ8eyow6HI1W7mACqwOM4uTOyWW3Y8eTQ55/Uj3/zaeOtN+rKR95q3qquXMGdwxhtNmQGMIiS2O8vXQCDq3a7PZ30E0FlZ6b70S6DbN37Kq8f6Xr1FuL7ITo3Z/FWtHMgkyyKIRj0ITRLLn4bw9BfkJhcmymphzqDvx07WDuBeEks9R+yLG/E2l/hOPY4y7KnsdGMfmnG3HOHwZRKCgQClNfrzfR4BKeeSshiyAFlQkshO5QW7Qz+eqxnegOCoijpePEjCC2xjAEURdVDg2az+QZFJV1GfBZpur83fO3U0ToV8QPawEkoipyDzR3MysrS9sUQMl2fL2uO2Wz60WKxbAkEnKRSUusjm6427Sj/E/GUPSAUFnqyYfDlXQ3+BSXwA5qyWM9EavoSNATNI4nJzN7ArBkEYj3TfdAYNApNa1BUVLAUBsMZGRlz9VRiYDCM5rbByuXM9RWKkxwncQ8gSypJkiU/P3+uwLKb9FxKJBJJ0gYYgU2+hka7AaR9HN3+90fdNT8jtsVSMUSRD+EcGoLJvaRfUlKyxOUSLtM0/aI2wAirlSq12WzkqyWk9b0XGu9urySmcQYunt8liaKKA66C9D2yGJElScWXHdYGzBBDA4HjGrD2/Xhgv8/nmy/w3AByp9Gv04fMCEMDLM/bOBqCLMvsx0z6WJbuxOH3GmbUpA8xhIJul1xvZ2i8q73yJ71L0KqJZ9kOrHdQkoQ1D7rdZGl8MNiJA+8dbVQCFqFyRmqqHjuhFORVYwY3P2it+GVVMV9dEyw7lS/nfo0xZkEQ1rB5eYVYnmS8dS25EYYFMFpF4kQked25G4Ivrfv28IEadeL3g6qKX+uJvrAaqnh0QOJyyC/UiLv+C+JYlDZ/fejl9QN48KWFC+aRaiElaYUWTtbe5mdaLl5o/+tQxyvH0Z8VhVAv9D50GDo6nU5Gt+Mf/5U6OtRGDsZZkwyRw89Qr9c+/sKZz1outLU81/wPyCM84+zSN5gAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pln, self.style, self.dim = (None for _ in range(3))

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

            def _get_dim(self, pt_tuple_data):
                sub_start_pt, sub_end_pt, sub_dis, sub_over_data, sub_align = pt_tuple_data
                self.pln.Origin = sub_start_pt
                if sub_align:
                    above_pt = sub_align.ClosestPoint(sub_start_pt, True)
                    offset_dis = above_pt.DistanceTo(sub_start_pt)
                else:
                    offset_dis = 0

                offset_pt = rg.Point3d(self.pln.OriginX + sub_dis + offset_dis, self.pln.OriginY, self.pln.OriginZ)
                ann_type = rg.AnnotationType.Rotated

                sub_dim = rg.LinearDimension.Create(ann_type, self.style, self.pln, self.pln.XAxis, sub_start_pt, sub_end_pt, offset_pt, 0)
                if sub_over_data:
                    sub_dim.RichText = sub_over_data
                real_dim_value = sub_dim.NumericValue
                show_dim_value = sub_dim.PlainUserText
                return sub_dim, real_dim_value, show_dim_value

            def get_uv(self, pt):
                res_bool, u_vaule, v_value = self.pln.ClosestParameter(pt)
                pt_2d = rg.Point2d(u_vaule, v_value)
                return pt_2d

            def run_mian(self, tuple_data):
                start_pt_list, end_pt_list, dis_list, over_data_list, align_line_list, origin_path = tuple_data
                s_len, e_len = len(start_pt_list), len(end_pt_list)
                if s_len > e_len:
                    start_pt_list = start_pt_list
                    end_pt_list = end_pt_list * s_len
                    dis_list = dis_list * s_len
                    over_data_list = over_data_list * s_len
                    align_line_list = align_line_list * s_len
                elif s_len < e_len:
                    start_pt_list = start_pt_list * e_len
                    end_pt_list = end_pt_list
                    dis_list = dis_list * e_len
                    over_data_list = over_data_list * e_len
                    align_line_list = align_line_list * e_len
                else:
                    start_pt_list = start_pt_list
                    end_pt_list = end_pt_list
                    dis_list = dis_list
                    over_data_list = over_data_list
                    align_line_list = align_line_list
                sub_zip_list = zip(start_pt_list, end_pt_list, dis_list, over_data_list, align_line_list)

                res_dim_list, real_v_list, show_v_list = zip(*map(self._get_dim, sub_zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_dim_list, real_v_list, show_v_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Start_Pt, End_Pt, Plane, Distance, Align_Line, Style, Overwrite):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Plane.Rotate(math.radians(90), Plane.ZAxis)
                    self.pln = Plane
                    self.style = Rhino.RhinoDoc.ActiveDoc.DimStyles.Find(Style, True)
                    if not self.style:
                        self.style = Rhino.RhinoDoc.ActiveDoc.DimStyles.FindIndex(0)
                        if Style:
                            Message.message2(self, "The dimension style for the '{}' type does not exist".format(Style))

                    Dimension, Real_Value, Show_Value = (gd[object]() for _ in range(3))

                    sp_trunk_list, sp_path_trunk = self.Branch_Route(Start_Pt)
                    ep_trunk_list, ep_path_trunk = self.Branch_Route(End_Pt)
                    dis_trunk_list = self.Branch_Route(Distance)[0]
                    over_trunk_list, align_trunk_list = self.Branch_Route(Overwrite)[0], self.Branch_Route(Align_Line)[0]
                    over_trunk_list = over_trunk_list if over_trunk_list else [[None]]
                    align_trunk_list = align_trunk_list if align_trunk_list else [[None]]

                    sp_len, ep_len = len(sp_trunk_list), len(ep_trunk_list)

                    re_mes = Message.RE_MES([Start_Pt, End_Pt], ['SP terminal', 'EP terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if sp_len > ep_len:
                            trunk_path = sp_path_trunk
                            new_sp_trunk_list = sp_trunk_list
                            new_ep_trunk_list = ep_trunk_list + ep_trunk_list * (sp_len - ep_len)
                            dis_trunk_list = dis_trunk_list * sp_len
                            over_trunk_list = over_trunk_list * sp_len
                            align_trunk_list = align_trunk_list * sp_len
                        elif sp_len < ep_len:
                            trunk_path = ep_path_trunk
                            new_sp_trunk_list = sp_trunk_list + sp_trunk_list * (ep_len - sp_len)
                            new_ep_trunk_list = ep_trunk_list
                            dis_trunk_list = dis_trunk_list * ep_len
                            over_trunk_list = over_trunk_list * ep_len
                            align_trunk_list = align_trunk_list * ep_len
                        else:
                            trunk_path = sp_path_trunk
                            new_sp_trunk_list = sp_trunk_list
                            new_ep_trunk_list = ep_trunk_list
                            dis_trunk_list = dis_trunk_list * sp_len
                            over_trunk_list = over_trunk_list * sp_len
                            align_trunk_list = align_trunk_list * sp_len

                        zip_list = zip(new_sp_trunk_list, new_ep_trunk_list, dis_trunk_list, over_trunk_list, align_trunk_list, trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.run_mian, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    no_rendering_line = self.Branch_Route(Dimension)[0]
                    self.dim = list(chain(*no_rendering_line))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Dimension, Real_Value, Show_Value
                finally:
                    self.Message = 'Vertical Dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass


        # 在犀牛空间中创建表格
        class Table(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Table", "F11", """Create a table in the Rhino space""", "Scavenger", "H-Facade")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def get_ComponentGuid(self):
                return System.Guid("55e00e4a-5a71-4aef-827f-293687d08b2a")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Str", "S", "Text list（separated by Comma）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Table location")
                DEFAULT_PL = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(DEFAULT_PL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Height", "H", "Text height")
                TEXT_HEIGHT = 1.5
                p.SetPersistentData(gk.Types.GH_Number(TEXT_HEIGHT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Height_Scale", "SC1", "Table height scaling")
                HEIGHT_SC = 2.0
                p.SetPersistentData(gk.Types.GH_Number(HEIGHT_SC))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Width_Scale", "SC2", "Table width scaling")
                WIDTH_SC = 1.5
                p.SetPersistentData(gk.Types.GH_Number(WIDTH_SC))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Layer", "L", "Table layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Bake", "B", "Bake button")
                BAKE_FACTOR = False
                p.SetPersistentData(gk.Types.GH_Boolean(BAKE_FACTOR))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Text_TEN", "T", "Literal solid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Cells", "C", "Text table box")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Pln", "Pl", "Position of table text")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARsSURBVEhLbVVLbxtVGB2JCkVVoKXQUtEiIR79EQgJ8QcQCzYI8Uu6YIEptAtYdMNjw6NRW1UJcZzWcfz2zPj9Gns8fsYeP+KoxGnFglcR9+N815nmOmFxJN9zzszc+53vftZeO3Xq3Y9PP3+V8QnwzrNLVz84vSzXHyng9dvQPvwfjTnWVN77rb2/tPz1P5ev0N+X3yJ69QqtvHiRhq+8Tk+w/kPBv9B+OneRHl56Q3o9/i/g8aU36YdzL9MTeDzee157T3vGZ529QNYLF6gF0xdLyxQ58xLVsK4ocKBdW3qOEmfOS6/HV4H82fP0GZ5TeX6+BF4L3v3Ut377Jt369oa49c0NsfqjT9z+/ku5XlHA619+/hza9RPaynfXhX/l2gLHHv+dm6T9uR/y9d0BmQWLjFyNBj1DFKslMvMWpcF5MPJzrVCpkFlc1DKlKrk7ulA5k/3DAWm/je/6JuM02dWQsMshMWlviHYtKOxKSDTAeeD1pLMhWrUtwV5Vc6pbYtL1L3Ds38V7tceje75BP0+lQlSUclExcDZFrbwtSvmoKIPzwOtBc1NYpbBgr6pVihHhtgILHPvdQZ60fXfV12xYlEwZlEiY1MRuMukkJZMGpcB5SCShWVsibaakV9V0XacWTq1ySfhbjjUv0d6uIQ0tKyim3XXRa9xHKYKyVB54Pe2ti6794ITWqT8Qe9BUjj17U2N+Ase2sEODYnGTHNQvbSZxGt7FEWI4nWOFhGmkpFfVUimdmshG5WQ1UBmZgdvPUbkQmdcNda5XtlHHiKgo4LqzViuHT2jVYlgMkYHKcQ7DQQ4fGN/zjdwscXhsHMHIXcHrmoIqMGoHZIcc1+poihG6T+XYMx5mSXvYX/U1anWKxtMUiWaogd3rhk7RWBolO0IkBq26LVK6Ib2qFj8sn8pF4XfqdYS8Ow+5XV8MWYYFzoMXcg8hH9dkyDsIWeHYI0M+QMjddpnSaE0OsAuxmI8RB83t6sFEe3btoCjk4tKrarlMgnhTKsft3OuU8YERPtApUQYmfmkXu0HYMCUoC84Dv5RbtJiLSa+q5bNx2mlsCpXnj/S6pfk92J1wDbcQLq53xy86eBEHzRfLg9QwDjo4IXtVTZYPpVV59k93zXnINkKOIJgwQrbREXwzIwiZw/QQRmg2GoBvKXtVTfY8Xqrysik4ZG7T8TBD3Gq10rYYo93YzGsVPJ9Y410e1xpyEPpP8JNR5nDY7WDYoe6o7+GwCxMGn+Q8SE0Ou8gCz+CL5TYDMrunQFYuhujTURHHcOL+5dqZCJt7mwech1gCGnrdQKexV9V4VHAOKh+HX46K33EPZvsJ4qvOu5gN1uRxh62NBfA4nrlrYoz/hOMa3+KZu4rfAYUPiINZYn6CTquMPk+Soaeog51wr5sG9/IReOfcQflsQnpVLYuW7tn35ck9Tt4p3C/t0Wjtq9mvfXKcKjVQqhlatod74TSq1ATnoYHjztB2/BB7Va3drNCjqb7AO/Af7PfpP3YH/bFQZXVQAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.ref_h_scale, self.w_s, self.layer_index, self.factor, self.unrendered_rec3d, self.unrendered_text = (None for _ in range(6))

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

            def new_text(self, new_tuple_data):
                word_list, pln, height_text = new_tuple_data
                text_list, x_dir_list = [], []

                def create_text(text, plane):
                    style = Rhino.RhinoDoc.ActiveDoc.DimStyles.FindIndex(0)
                    text = rg.TextEntity.Create(text, plane, style, True, 0, 0)
                    text.Justification = rg.TextJustification.MiddleCenter
                    text.TextHeight = height_text

                    copt_text = text.Duplicate()
                    box = rg.Box(copt_text.GetBoundingBox(True))
                    rect = rg.Rectangle3d(plane, box.X, box.Y)
                    X_Dir = rect.Width * self.w_s
                    return text, X_Dir

                for word in word_list:
                    if word:
                        temp_text, x_dir = create_text(word, pln)
                        x_dir_list.append(x_dir)
                        text_list.append(temp_text)
                    else:
                        text_list.append(None)

                sub_rec = rg.Rectangle3d(pln, rg.Interval(0, max(x_dir_list)), rg.Interval(0, self.ref_h_scale * -height_text))

                return sub_rec, max(x_dir_list), len(word_list), text_list

            def num_count_add(self, num_list):
                final_data = []
                for index in range(1, len(num_list) + 1):
                    final_data.append(sum(num_list[:index]))
                return final_data

            def iter_offset(self, tuple_num):
                rec_obj, sub_x, len_num, height_dub = tuple_num

                obj_center = rec_obj.Corner(0)
                obj_pln = rg.Plane.WorldXY
                obj_pln.Origin = obj_center
                ref_sub_y = self.num_count_add([self.ref_h_scale * -height_dub] * len_num)[0: -1]

                rec_curve = ghc.Move(rec_obj, rg.Vector3d(sub_x, 0, 0))['geometry']
                new_rec_list = [rec_curve]
                for item in ref_sub_y:
                    copy_rec_cur = ghc.Move(rec_curve, rg.Vector3d(0, item, 0))['geometry']
                    new_rec_list.append(copy_rec_cur)

                return new_rec_list

            def text_translate(self, text_tuple):
                new_text_list, pln_list = [], []
                ref_pln = rg.Plane.WorldXY
                text, rectangle = text_tuple
                for sub_index, sub_text in enumerate(text):
                    if sub_text:
                        ref_pln.Origin = rectangle[sub_index].Center
                        sub_text.Plane = ref_pln
                        new_text_list.append(sub_text)
                        pln_list.append(sub_text.Plane)
                    else:
                        new_text_list.append(None)
                        pln_list.append(None)
                return new_text_list, pln_list

            def _bake_group(self, obj_list, color):
                attr = sc.doc.CreateDefaultAttributes()
                attr.LayerIndex = self.layer_index
                attr.ObjectColor = color
                attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject

                for gh_obj in obj_list:
                    if type(gh_obj) is rg.Rectangle3d:
                        sc.doc.Objects.AddRectangle(gh_obj, attr)
                    else:
                        sc.doc.Objects.Add(gh_obj, attr)

            def _do_main(self, tuple_data):

                str_list, origin_path, height, pln = tuple_data
                str_list = map(lambda x: x.split(','), str_list)
                str_len = map(lambda y: len(y), str_list)
                max_len = max(str_len)
                new_str_list = []
                for sub_str in str_list:
                    if len(sub_str) < max_len:
                        sub_str = sub_str + [None] * (max_len - len(sub_str))
                        new_str_list.append(sub_str)
                    else:
                        new_str_list.append(sub_str)
                str_zip_list = zip(*new_str_list)
                pln_list = pln * len(str_zip_list)
                height_list = height * len(str_zip_list)
                str_pln_zip = zip(str_zip_list, pln_list, height_list)

                one_rec_list, x_list, word_len, text_array = zip(*map(self.new_text, str_pln_zip))

                x_list = list(x_list)
                x_list.insert(0, 0)
                x_dir_list = self.num_count_add(x_list)
                new_zip_list = zip(one_rec_list, x_dir_list, word_len, height_list)

                rec_list = map(self.iter_offset, new_zip_list)
                text_replace, pln_array = zip(*map(self.text_translate, zip(text_array, rec_list)))

                bake_text = filter(None, list(chain(*text_replace)))
                bake_rec = filter(None, list(chain(*rec_list)))
                text_color = System.Drawing.Color.Yellow
                rec_color = System.Drawing.Color.Red

                if self.factor:
                    self._bake_group(bake_text, text_color)
                    self._bake_group(bake_rec, rec_color)

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [text_replace, rec_list, pln_array])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Str, Plane, Height, Height_Scale, Width_Scale, Layer, Bake):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Text_TEN, Cells, Pln = (gd[object]() for _ in range(3))

                    Layer = Layer if Layer else 'Table'
                    self.w_s = Width_Scale
                    self.ref_h_scale = Height_Scale
                    self.factor = Bake

                    re_mes = Message.RE_MES([Str], ['Str'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if self.factor:
                            Object_group.BakeGeometry().create_layer(Layer)
                            self.layer_index = sc.doc.Layers.FindByFullPath(Layer, True)

                        str_trunk, str_trunk_path = self.Branch_Route(Str)
                        pln_trunk = self.Branch_Route(Plane)[0]
                        h_text_trunk = self.Branch_Route(Height)[0]
                        s_len, h_len = len(str_trunk), len(h_text_trunk)
                        if s_len > h_len:
                            h_text_trunk = h_text_trunk + [h_text_trunk[-1]] * (s_len - h_len)

                        zip_list = zip(str_trunk, str_trunk_path, h_text_trunk, pln_trunk)
                        iter_ungroup_data = zip(*map(self._do_main, zip_list))
                        self.unrendered_rec3d = list(chain(*zip(*iter_ungroup_data[1])[0]))
                        self.unrendered_text = list(chain(*zip(*iter_ungroup_data[0])[0]))
                        Text_TEN, Cells, Pln = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Text_TEN, Cells, Pln
                finally:
                    self.Message = 'Table frame'

            def DrawViewportWires(self, args):
                try:
                    for text_index, text_item in enumerate(self.unrendered_text):
                        for sub_index, sub_text in enumerate(text_item):
                            if sub_text:
                                args.Display.DrawText(sub_text, System.Drawing.Color.FromArgb(0, 150, 0), sub_text.GetTextTransform(sub_text.DimensionScale, sub_text.DimensionStyle))
                            rec_curve = self.unrendered_rec3d[text_index][sub_index].ToNurbsCurve()
                            args.Display.DrawCurve(rec_curve, System.Drawing.Color.FromArgb(0, 150, 0), 2)
                except:
                    pass

    else:
        pass
except:
    pass
