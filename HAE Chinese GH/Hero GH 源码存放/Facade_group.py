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
from Grasshopper.Kernel.Data import GH_Path
from itertools import chain
import initialization
import Geometry_group
import copy
import math
import clr
import os
import sys
import Object_group

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:
        # 获取曲面板关键点
        class SurfaceKeyPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SurfaceKeyPoints", "F1",
                                                                   """Obtain the key points, corner points, center points, line center points of the surface plate""",
                                                                   "Scavenger", "H-Facade")
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
                if brep_list:
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

                    ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                       [corner_list, center_list, line_center_pt])
                else:
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                       [[corner_list], [center_list], [line_center_pt]])
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
                        Corner_Pt, Center_Pt, Line_Center_Pt = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

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
                                                                   "RPP_SmallestRegion", "F3",
                                                                   """Centered on the central object，find a rough minimum range in a set of objects""",
                                                                   "Scavenger", "H-Facade")
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
                        #                main_pt = Geometry_group.GeoCenter().center_box(obj_item)
                        main_pt = Geometry_group.GeoCenter().center_box(obj_item)
                        #                other_pts = map(Geometry_group.GeoCenter().center_box, new_object[obj_index])
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

                        main_trunk_list, temp_path_1 = self.Branch_Route(Main_Item)
                        order_trunk_list, temp_path_2 = self.Branch_Route(structure_tree)
                        # 匹配数据
                        m_len, o_len = len(main_trunk_list), len(order_trunk_list)
                        if m_len < o_len:
                            main_trunk_list = main_trunk_list + [main_trunk_list[-1]] * (o_len - m_len)
                            target_path = temp_path_2
                        elif m_len > o_len:
                            order_trunk_list = order_trunk_list + [order_trunk_list[-1]] * (m_len - o_len)
                            target_path = temp_path_1
                        else:
                            main_trunk_list = main_trunk_list
                            order_trunk_list = order_trunk_list
                            target_path = temp_path_1
                        zip_list = zip(main_trunk_list, order_trunk_list, target_path)
                        iter_ungroup_data = zip(*ghp.run(self.closest_object, zip_list))
                        Res_Order_Item, Order_Index, Distance = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

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
                                                                   "RPP_CounterBore", "F2",
                                                                   """Input specifications automatically generate countersunk screws (including M4, M5, M6, M8, M10, M12, M16, M20)""",
                                                                   "Scavenger", "H-Facade")
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
                self.al_specifications = {'M4': (4.5, 9.6), 'M5': (5.5, 11.6), 'M6': (6.5, 13.6), 'M8': (8.5, 17.8),
                                          'M10': (11.0, 22.0), 'M12': (13.0, 26.0), 'M16': (17.0, 32.0),
                                          'M20': (21.0, 38.0)}
                self.fe_specifications = {'M4': (6.0, 9.6), 'M5': (7.0, 11.6), 'M6': (8.0, 13.6), 'M8': (10.0, 17.8),
                                          'M10': (12.0, 22.0), 'M12': (14.0, 26.0), 'M16': (18.0, 32.0),
                                          'M20': (22.0, 38.0)}
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
                loft_brep = \
                    rg.Brep.CreateFromLoft([big_circle, small_circle_one, small_circle_two], origin_pln.Origin, unset_pt,
                                           rg.LoftType.Straight, False)[0]
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
                                                                   "RPP_Surface_flanging", "F12",
                                                                   """Panel folding, suitable for regular aluminum plate, special plate need semi-manual work""",
                                                                   "Scavenger", "H-Facade")
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
                self.SetUpParam(p, "Edge_Tree", "EL",
                                "Curve list, enter the edges that need to be defined,if no input,make folding uniformly")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Size_Tree", "SL",
                                "folding width list, control the list of curve value, quantity must be consistent with curve list")
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
                                ver_zip = list(zip(fold_vector_count,
                                                   self.data_polishing_list(ght.tree_to_list(Edge_Tree),
                                                                            [ght.tree_to_list(Size_Tree)])))
                            else:
                                ver_zip = list(zip(fold_vector_count,
                                                   self.data_polishing_list([data_ for data_ in Edge_Tree.Branches],
                                                                            [data_ for data_ in Size_Tree.Branches])))
                            fold_size_count = ghp.run(self.ver_lenght, ver_zip)
                            fold = list(zip(fold_surface, fold_size_count))

                        Fill_Brep, Folded_Surface = zip(*ghp.run(self.add_fillet_to_edges, fold))

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Fill_Brep, Folded_Surface
                finally:
                    self.Message = 'HAE surface folding'


        # 平面的X轴标注（水平标注）
        class HorizontalAnnotation(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_HorizontalAnnotation", "F4",
                                                                   """X-axis dimension of the plane (horizontal dimension)""",
                                                                   "Scavenger", "H-Facade")
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "End_Pt", "EP", "Dimension ending point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "The referenced plane,default is world XY")
                PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.Hidden = True  # 隐藏输入端预览
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Mark the offset distance")
                DISTANCE = 1
                p.SetPersistentData(gk.Types.GH_Number(DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Align_Line", "L", "Align the dimension to line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Overwrite", "W", "Dimension data overwrite")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                self.Message = 'Horizontal Dimension'
                Dimension, Real_Value, Show_Value = (gd[object]() for _ in range(3))
                if self.RunCount == 1:
                    def temp_by_match_tree(*args):
                        # 参数化匹配数据
                        value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                        len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                        max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                        self.max_index = max_index
                        max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                        ref_trunk_path = trunk_paths[max_index]
                        other_list = [
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [
                                [None]]
                            for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                        matchzip = zip([max_trunk] * len(other_list), other_list)

                        def sub_match(tuple_data):
                            # 子树匹配
                            target_tree, other_tree = tuple_data
                            t_len, o_len = len(target_tree), len(other_tree)
                            if o_len == 0:
                                new_tree = [other_tree] * len(target_tree)
                            else:
                                new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                            return new_tree

                        # 打包数据结构
                        other_zip_trunk = zip(*map(sub_match, matchzip))

                        zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                        # 多进程函数运行
                        iter_ungroup_data = zip(*map(self._do_main, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                    iter_ungroup_data)
                        return Dimension, Real_Value, Show_Value

                    Start_Pt = self.Params.Input[0].VolatileData
                    End_Pt = self.Params.Input[1].VolatileData
                    Plane = self.Params.Input[2].VolatileData
                    Distance = self.Params.Input[3].VolatileData
                    Align_Line = self.Params.Input[4].VolatileData
                    Style = self.Params.Input[5].VolatileData
                    Overwrite = self.Params.Input[6].VolatileData

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    j_list_1 = any([len(_i) for _i in self.Branch_Route(Start_Pt)[0]])
                    j_list_2 = any([len(_i) for _i in self.Branch_Route(End_Pt)[0]])
                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['SP terminal', 'EP terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, Real_Value, Show_Value = temp_by_match_tree(Start_Pt, End_Pt, Plane, Distance, Align_Line,
                                                                               Style, Overwrite)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                DA.SetDataTree(0, Dimension)  # 返回值
                DA.SetDataTree(1, Real_Value)  # 返回值
                DA.SetDataTree(2, Show_Value)  # 返回值

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPVSURBVEhLvZR/bFNVFMe3ti8ODE4UF2FGdI6J79537+u2rl27rHFsS0exydgPliBGUrexiXQjRBKzxTiHiwQWS8QsoyAQCKjtSIjK4hJ/hB+bMYiGMMRfMWrwRxxzGpgG3PV7X9829gP8p/hJvrnnnHfeOfee29ckSZ6eqdaufrTUcBJNuT+XnuvfNnrlz5jYuS34ohlOHMHHvT5xJSaEGBBv7Q29bYYTiq1lU3lka/ua82VlLMuMJZwSaEfcvDWUQ91x89YgG+yKm0mu1NRUu2mPY4HugRZAd0Jp0DzoeuaAlXKNu1ORDcLQbaFGv3DnZT1vRE3wYrrNZjtrtVq/S05O/lVRbF8qivVl8/E4t9evLRErfDlbTH8KsnP7qsrC0P6u9WOw7zCi01AUy1o0+Fma8chUWjet3PXa9tq/Yd4Vj0xSBr3T29NyMbw1eKmggDe73Wyj2601u1ykyeGiz2jaQ08h52k0OLdo0d0BQjKDqppRr6oPTIiSxXu/OvMqTpE7/XRJhTabdeSnL7rF2OUjQoz0iLHfY1BU/DMcFWL0qBj8ZIewWpMPIvd023M1l8VYr7g29OYU/fXLIXxPx0RXZ+0PyJMjz5DFJSXY2ccn3m0b3bOzYWh9bekbjcGS6LhC9cujq6sKosjpgD73FfF9LZsrT27eEDhxvTY2+geHf9wvmtb5j6BmDMo2qgN5yR0b6nzdr3Q8ORIPzcRisVSjwW+mO4NlXq3lcKRJwFSh16GJX+MqqAu6d3v7E6LQQ0JGdBopKSmLFUWpNt0ZhBqWX1xTU/iB6fZAEw3krIqk8fCS9LbMjIWzNvgPlKVLFu6ZO1fhpi/HNP17Sij/YwOv12tzOp3M48lz+f3++eOxQCAwr6qqyurxeO43Ek2Ki4tT8/Pz5d/FzZhsYNe0ZTpnlxijfTrnXzuduRWMsQc516IOB9d1nV+12+01RjJgTBuklHxkujdisgGlj1RzzvqlraqqDwW+z87OLqJU7c3h3KNRehWxD+XzXF33cqYJQsh70r8JUSh+4YyRCux2wHAACp7lnNdjjWH7xVh7KaX9DoeDcI3slnEpM/1GHIOoYWmaVokGx6Wdz1gajv8tGvhR9CjWUjw/wAhpwKhOy9FgQysoIX3Gy7MQCdd1Xji/+1rPvub4KVGoHHfwh8ORs0Vn7AxV1VbEljJNOyUbYbfvu1yuOXZdFyjcifuhiH1qvDwTy0Bf+7AQn4mhbyLyq5YjYmkaIc9ipy9gto/JWE5W1gL4ATRIxyr/bZNwigrY90HzYRt5s/FSa826gVPhC5FwXee/PztAyjSROysAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.bbox, self.dim = (None for _ in range(2))

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                elif ref_obj is not None:
                    test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def _get_dim(self, pt_tuple_data):
                sub_start_pt, sub_end_pt, sub_plane, sub_dis, sub_align, sub_style, sub_over_data = pt_tuple_data

                if sub_start_pt is not None and sub_end_pt is not None:
                    # 若直线存在
                    if sub_align:
                        sub_plane = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))
                    else:
                        sub_plane.Origin = sub_start_pt

                    style = self.Find_DimStyle(sub_style)
                    offset_pt = rg.Point3d(sub_plane.OriginX, sub_plane.OriginY + sub_dis, sub_plane.OriginZ)
                    ann_type = rg.AnnotationType.Rotated

                    sub_dim = rg.LinearDimension.Create(ann_type, style, sub_plane, sub_plane.XAxis, sub_start_pt, sub_end_pt,
                                                        offset_pt, 0)
                    if sub_over_data:
                        sub_dim.RichText = sub_over_data
                    real_dim_value = sub_dim.NumericValue
                    show_dim_value = sub_dim.PlainUserText

                    sub_dim = initialization.HAE_LinearDim(sub_dim)  # 调用至自定义类

                else:
                    sub_dim, real_dim_value, show_dim_value = (None for i in range(3))

                return sub_dim, real_dim_value, show_dim_value

            def _do_main(self, tuple_data):
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_SP, match_EP, match_Plane, match_Distance, match_line, match_style, match_OverWrite = new_list_data

                start_pt_list, end_pt_list, plane_list, dis_list, align_line_list, style_list, over_data_list = self.match_list(
                    match_SP, match_EP, match_Plane, match_Distance, match_line, match_style, match_OverWrite)  # 将数据二次匹配列表里面的数据

                start_pt_list = map(self._trun_object, start_pt_list)  # 将引用物体转换为Rhino内置物体
                end_pt_list = map(self._trun_object, end_pt_list)
                plane_list = map(self._trun_object, plane_list)
                dis_list = map(self._trun_object, dis_list)
                align_line_list = map(self._trun_object, align_line_list)
                style_list = map(self._trun_object, style_list)
                over_data_list = map(self._trun_object, over_data_list)

                sub_zip_list = zip(start_pt_list, end_pt_list, plane_list, dis_list, align_line_list, style_list,
                                   over_data_list)

                res_dim_list, real_v_list, show_v_list = zip(*map(self._get_dim, sub_zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_dim_list, real_v_list, show_v_list])

                Rhino.RhinoApp.Wait()
                return ungroup_data


        # 平面的Y轴标注（垂直标注）
        class VerticalDimension(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_VerticalDimension", "F5",
                                                                   """Y-axis dimension of the plane（Vertical Dimension）""",
                                                                   "Scavenger", "H-Facade")
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "End_Pt", "EP", "Dimension ending point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "The referenced plane,default is world XY")
                PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.Hidden = True  # 隐藏输入端预览
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Make dimension for the offset distance")
                DISTANCE = 1
                p.SetPersistentData(gk.Types.GH_Number(DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Align_Line", "L", "Align the dimension to the line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Overwrite", "W", "Dimension data overwrite")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                self.Message = 'Horizontal Dimension'
                Dimension, Real_Value, Show_Value = (gd[object]() for _ in range(3))
                if self.RunCount == 1:
                    def temp_by_match_tree(*args):
                        # 参数化匹配数据
                        value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                        len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                        max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                        self.max_index = max_index
                        max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                        ref_trunk_path = trunk_paths[max_index]
                        other_list = [
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [
                                [None]]
                            for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                        matchzip = zip([max_trunk] * len(other_list), other_list)

                        def sub_match(tuple_data):
                            # 子树匹配
                            target_tree, other_tree = tuple_data
                            t_len, o_len = len(target_tree), len(other_tree)
                            if o_len == 0:
                                new_tree = [other_tree] * len(target_tree)
                            else:
                                new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                            return new_tree

                        # 打包数据结构
                        other_zip_trunk = zip(*map(sub_match, matchzip))

                        zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                        # 多进程函数运行
                        iter_ungroup_data = zip(*map(self._do_main, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                    iter_ungroup_data)
                        return Dimension, Real_Value, Show_Value

                    Start_Pt = self.Params.Input[0].VolatileData
                    End_Pt = self.Params.Input[1].VolatileData
                    Plane = self.Params.Input[2].VolatileData
                    Distance = self.Params.Input[3].VolatileData
                    Align_Line = self.Params.Input[4].VolatileData
                    Style = self.Params.Input[5].VolatileData
                    Overwrite = self.Params.Input[6].VolatileData

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    j_list_1 = any([len(_i) for _i in self.Branch_Route(Start_Pt)[0]])
                    j_list_2 = any([len(_i) for _i in self.Branch_Route(End_Pt)[0]])
                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['SP terminal', 'EP terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, Real_Value, Show_Value = temp_by_match_tree(Start_Pt, End_Pt, Plane, Distance, Align_Line,
                                                                               Style, Overwrite)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                DA.SetDataTree(0, Dimension)  # 返回值
                DA.SetDataTree(1, Real_Value)  # 返回值
                DA.SetDataTree(2, Show_Value)  # 返回值

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP/SURBVEhLrZV9TBNnHMdbjlKtsmUixhkGAYsNvdfeXTtCDyuIxOnmdLSZZsqy7MVtycIYLWZg2iU4ZQRYiFt0g0hC2CYosTDnWxxZohtG3XtIZhxDZfGPOeZeHIbNcPs+15uzwFVI9km+eX7P75677z3P87vnTASPYHc++0RRqdb5v9mwVmYGBxpvjv3Ro4ary1qRegRaN40eghQoA5qC2+1e5hKEN3me38NxXLmeNpme3uxbrY71qKp6Rt0V3jiCVNskvQs1Qh0pluQbVqvlQ8QpUBySy1XJc9z3oiBUCTx/kaXpFv2SKXl3w1N10f3buvx+T7aei+Ph1Z7Stj0V56981zoxPLhX3d30/PBy7x1vCURRqGIY5gCJi4sVJ8eyow6HI1W7mACqwOM4uTOyWW3Y8eTQ55/Uj3/zaeOtN+rKR95q3qquXMGdwxhtNmQGMIiS2O8vXQCDq3a7PZ30E0FlZ6b70S6DbN37Kq8f6Xr1FuL7ITo3Z/FWtHMgkyyKIRj0ITRLLn4bw9BfkJhcmymphzqDvx07WDuBeEks9R+yLG/E2l/hOPY4y7KnsdGMfmnG3HOHwZRKCgQClNfrzfR4BKeeSshiyAFlQkshO5QW7Qz+eqxnegOCoijpePEjCC2xjAEURdVDg2az+QZFJV1GfBZpur83fO3U0ToV8QPawEkoipyDzR3MysrS9sUQMl2fL2uO2Wz60WKxbAkEnKRSUusjm6427Sj/E/GUPSAUFnqyYfDlXQ3+BSXwA5qyWM9EavoSNATNI4nJzN7ArBkEYj3TfdAYNApNa1BUVLAUBsMZGRlz9VRiYDCM5rbByuXM9RWKkxwncQ8gSypJkiU/P3+uwLKb9FxKJBJJ0gYYgU2+hka7AaR9HN3+90fdNT8jtsVSMUSRD+EcGoLJvaRfUlKyxOUSLtM0/aI2wAirlSq12WzkqyWk9b0XGu9urySmcQYunt8liaKKA66C9D2yGJElScWXHdYGzBBDA4HjGrD2/Xhgv8/nmy/w3AByp9Gv04fMCEMDLM/bOBqCLMvsx0z6WJbuxOH3GmbUpA8xhIJul1xvZ2i8q73yJ71L0KqJZ9kOrHdQkoQ1D7rdZGl8MNiJA+8dbVQCFqFyRmqqHjuhFORVYwY3P2it+GVVMV9dEyw7lS/nfo0xZkEQ1rB5eYVYnmS8dS25EYYFMFpF4kQked25G4Ivrfv28IEadeL3g6qKX+uJvrAaqnh0QOJyyC/UiLv+C+JYlDZ/fejl9QN48KWFC+aRaiElaYUWTtbe5mdaLl5o/+tQxyvH0Z8VhVAv9D50GDo6nU5Gt+Mf/5U6OtRGDsZZkwyRw89Qr9c+/sKZz1outLU81/wPyCM84+zSN5gAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.bbox, self.dim = (None for _ in range(2))

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                elif ref_obj is not None:
                    test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def _get_dim(self, pt_tuple_data):
                sub_start_pt, sub_end_pt, sub_plane, sub_dis, sub_align, sub_style, sub_over_data = pt_tuple_data

                new_plane = copy.copy(sub_plane)
                new_plane.Rotate(math.radians(90), new_plane.ZAxis)  # 垂直标注

                if sub_start_pt is not None and sub_end_pt is not None:
                    # 若直线存在
                    if sub_align:
                        new_plane = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))
                    else:
                        new_plane.Origin = sub_start_pt

                    style = self.Find_DimStyle(sub_style)
                    offset_pt = rg.Point3d(new_plane.OriginX + sub_dis, new_plane.OriginY, new_plane.OriginZ)
                    ann_type = rg.AnnotationType.Rotated

                    sub_dim = rg.LinearDimension.Create(ann_type, style, new_plane, new_plane.XAxis, sub_start_pt, sub_end_pt,
                                                        offset_pt, 0)
                    if sub_over_data:
                        sub_dim.RichText = sub_over_data
                    real_dim_value = sub_dim.NumericValue
                    show_dim_value = sub_dim.PlainUserText

                    sub_dim = initialization.HAE_LinearDim(sub_dim)  # 调用自定义类

                else:
                    sub_dim, real_dim_value, show_dim_value = (None for i in range(3))

                return sub_dim, real_dim_value, show_dim_value

            def _do_main(self, tuple_data):
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_SP, match_EP, match_Plane, match_Distance, match_line, match_style, match_OverWrite = new_list_data

                start_pt_list, end_pt_list, plane_list, dis_list, align_line_list, style_list, over_data_list = self.match_list(match_SP, match_EP, match_Plane, match_Distance, match_line, match_style, match_OverWrite)  # 将数据二次匹配列表里面的数据

                start_pt_list = map(self._trun_object, start_pt_list)  # 将引用物体转换为Rhino内置物体
                end_pt_list = map(self._trun_object, end_pt_list)
                plane_list = map(self._trun_object, plane_list)
                dis_list = map(self._trun_object, dis_list)
                align_line_list = map(self._trun_object, align_line_list)
                style_list = map(self._trun_object, style_list)
                over_data_list = map(self._trun_object, over_data_list)

                sub_zip_list = zip(start_pt_list, end_pt_list, plane_list, dis_list, align_line_list, style_list,
                                   over_data_list)

                res_dim_list, real_v_list, show_v_list = zip(*map(self._get_dim, sub_zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_dim_list, real_v_list, show_v_list])

                Rhino.RhinoApp.Wait()
                return ungroup_data


        # 在犀牛空间中创建表格
        class Table(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Table", "F11",
                                                                   """Create a table in the Rhino space""", "Scavenger",
                                                                   "H-Facade")
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
                p.Hidden = True  # 隐藏输入端预览
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
                p.Hidden = True  # 隐藏输出端预览
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALXSURBVEhLtZVrSFNhGMcPc/PsltNZtihRLDU1dU6dly1nXuZ0S53YZZhCaMPUeVlt5CzDvCWERXQxCTSJFMENU9JKDbJmIgwGI/DLCII+JoRdoNjTc47Q5z68Hvjxcv7Pef7PeznPORReKYhlF6HsIXsEoM45ChpVIhSfSGE5jveqrHhQZ8f/G7Wo6wpToUhzDLU4VmPjyjgoRK2sOA1Ki+RsLuMnFvOBKWDR5CYAwAqszF6FXHyY4bPvPmpzAD9mAH45AX46of5cPhTkJcFgtwljL3ZiDLAATx40sQVqqlUAW1OozUNW+pGdAvnqRBRWYRkLpCZFsXz5+BC1RYDfswABLPTnOVSUpkNC3EHo7KjA2NJOjAEnN9xXCzFREaBUHAb4No3aS8jOiGULtErDxGDA5JM6BZTjyGAoUYBem/afKHD2cnb7GJhcgy4dQiVCtsBpZGXXCJMIesfuNQZck7aAc8JKDJfTEWhvLA1QNM1trizL8JqqVd4zxhximEx53pzMWC8lFtMXcR89RoPSU6nPJIbRmO2RJ0d7qAP7Jb0TI03genYZZiasxHA5u6CpXssechufz9sUCulNoYAg6MenuZuUSCTon5+yw8bbIVhf6iPGxvowDF43sSuwBgVxPnG5QcRhfCmZLGzA9fQSLM91w2tXFzGWcRXWZj3ga8q7kJwY6ZanRLvx1Mkhj3FHHgp3UxKJqMNiLvHb28r9NouBGHZblb+kINVP7ZWGXMMP1fboXfP2yO0GYow+atmuO5v3nRLSPHOoRPRBEiIkC3rygjhuSq2MH3Qv3oC1V73wfrGHGGtrt+B8jQYoDodzRSgI3sLG2MIGIQf6BQdzvzJ90Df5uBXcbwbg3UIPMdyrQ3BnoI5ttOpwqXhaFhE6LdsnIQf6SdEX+4BusZh1PoetytdprSSGw3HKZ9QrfZRAQN8c7q+F8dEWwB8PMcbH2qG5QQt/AV41JveCu0G4AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.ref_h_scale, self.w_s, self.layer_index, self.factor, self.unrendered_rec3d, self.unrendered_text = (
                    None for _ in range(6))

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

                sub_rec = rg.Rectangle3d(pln, rg.Interval(0, max(x_dir_list)),
                                         rg.Interval(0, self.ref_h_scale * -height_text))

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
                        new_text_list.append(initialization.HAE_Text(sub_text))  # 将文本传入自定义文本类
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
                        gh_obj.BakeGeometry(sc.doc, attr, None)  # 调用自定义文本类中的Bake方法
                        # sc.doc.Objects.Add(gh_obj, attr)

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
                        Text_TEN, Cells, Pln = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                       iter_ungroup_data)

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Text_TEN, Cells, Pln
                finally:
                    self.Message = 'Table frame'


        # 创建标注样式
        class DimStyle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DimStyle", "F14", """Create dimension style""",
                                                                   "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d38e2624-642d-429e-9c82-0255e65d8533")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Proportion", "P", "Proportion")
                p.SetPersistentData(gk.Types.GH_Number(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Character height", "CH", "Character height")
                p.SetPersistentData(gk.Types.GH_Number(2.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Typeface", "F", "Typeface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Roundoff", "R", "Round length units.")
                p.SetPersistentData(gk.Types.GH_Number(0.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "ZeroSuppression", "ZS",
                                "Zero elimination for length units and angle units(0: None；1: SuppressLeading；2: 	SuppressTrailing；3: SuppressLeadingAndTrailing)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.SetPersistentData(gk.Types.GH_Number(2))
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Name", "N", "Name")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                result = self.RunScript(p0, p1, p2, p3, p4, p5)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJVSURBVEhL5ZZdSFNhHMYt5rpYBksnDaNmx4V9mJx0YYnIMl2FFLhdpEhrNI2VBZG26GPowD5oIggOk/KijChBxbQkCjLsepHdRkRUFBRBUCHa0/Pf1o0VnTPv6gc/zsv7Hs5zzvt50kgpbZnjQWqkejDTNhqeY1rHvrpyRKMBRDv86DrvxVKzaYb1S6RRB/Z1+csRe3wRsYlziMW60NTggjSEh/ubATykd4BvQ1Bs2e9YnyGNOlhVUmSfAW4D00N81gNEwvWJgGs9h4DvI8Cnm/j65ipsK7JSCnCoygw+DwAfbzBgFO2n9/wnAQuS17+hO2ARtdCTNECLaDHdQo9TIYcGE0X9Ael0Da2lsiYOUz910UGaTd20lwopBeRTj9xEDtD9dHfyejR5lVBBd4C8tZWGaCOVLiqjVcmyfFkJ3UWFlAdZ0LJt6Ap4z3oZZEHe1J4o/oJK5YsEGwNmNQXkrrS8Zr3ZWbb2wtnWOlSWr79f7dp4eWel2ru9YkPPjorCqFjlLJgMBT2wK1bpQusmVZnWFJBjNb/IyswYf/msmzfKHjX2B0fpBCbvtsJoNNwqVpUPGrvI8spkSi9o9FaMjQycQHNT9fNTzTVPQi01T9uCnqnWoJt6pkJB99t7I2fgrS2/bjCklTrUvC96xmChNJIIldnyO2QdxPd8skzzGCRnkd7zQJnPNNXCvNaBFv7lgOH+Y6z4eSYP8ky2pBSw2bF6FhiPPxx4hM52bzwg0rB3K/quHEFfdwCXOv3INC9O5a8ij4sTvnonfPxL8fm2oagwFz8AR6AKmXAF0KwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def create_style(self, name, Proportion, TextHeight, font, Roundoff, Suppression):
                """创建或修改标注样式"""
                if sc.doc.DimStyles.FindName(name) is None:
                    # 判断标注样式是否存在
                    Rhino.RhinoDoc.ActiveDoc.DimStyles.Add(name)
                dim = sc.doc.DimStyles.FindName(name)
                dim.DimensionScale = Proportion  # 标注比例
                dim.TextHeight = TextHeight  # 字高
                dim.Font = Rhino.DocObjects.Font(font)  # 字体
                ZeroSuppress = Rhino.DocObjects.DimensionStyle.ZeroSuppression(Suppression)
                dim.ZeroSuppress = ZeroSuppress  # 长度单位消零
                dim.AngleZeroSuppress = ZeroSuppress  # 角度单位消零
                dim.Roundoff = Roundoff  # 长度单位取整

                sc.doc.DimStyles.Modify(dim, dim.Id, True)  # 将设置的样式进行修改

            def RunScript(self, Name, Proportion, Character_height, Typeface, Roundoff, ZeroSuppression):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([Name], ['Name end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.create_style(Name, Proportion, Character_height, Typeface, Roundoff, ZeroSuppression)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Name

                finally:
                    self.Message = 'Create dimension style'


        # 引线标注
        class LeaderDim(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_LeaderDim", "F13", """Lead labeling""",
                                                                   "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c322bb68-2927-40e4-b7ef-270a1c0afba1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "lead")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Working plane")
                REF_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(REF_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.Hidden = True  # 隐藏输入端预览
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text")
                p.SetPersistentData(gk.Types.GH_String('Text'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Leader", "L", "lead")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Lead dimension'
                Leader = gd[object]()
                if self.RunCount == 1:
                    def temp_by_match_tree(*args):
                        # 参数化匹配数据
                        value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                        len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                        max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                        self.max_index = max_index
                        max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                        ref_trunk_path = trunk_paths[max_index]
                        other_list = [
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
                            for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                        matchzip = zip([max_trunk] * len(other_list), other_list)

                        def sub_match(tuple_data):
                            # 子树匹配
                            target_tree, other_tree = tuple_data
                            t_len, o_len = len(target_tree), len(other_tree)
                            if o_len == 0:
                                new_tree = [other_tree] * len(target_tree)
                            else:
                                new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                            return new_tree

                        # 打包数据结构
                        other_zip_trunk = zip(*map(sub_match, matchzip))

                        zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                        # 多进程函数运行
                        iter_ungroup_data = map(self._do_main, zip_list)

                        Leader = self.format_tree(iter_ungroup_data)

                        return Leader

                    Curve = self.Params.Input[0].VolatileData
                    Plane = self.Params.Input[1].VolatileData
                    Style = self.Params.Input[2].VolatileData
                    Text = self.Params.Input[3].VolatileData

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    j_list = any([len(_i) for _i in self.Branch_Route(Curve)[0]])
                    re_mes = Message.RE_MES([j_list], ['Curve terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Leader = temp_by_match_tree(Curve, Plane, Style, Text)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                DA.SetDataTree(0, Leader)  # 返回值

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKgSURBVEhLxdRtSFNRGAfwba6VJLmlNleOWUa+NJGVq4RS0FRYq5yoOJeSNFOxF2orKqyVYrlWUuYX3YTeFUxhpkUUEVoRfQpfPoREXwqNoCCnZlRP/3PviogYsW70hx97zjn3nnt37rlX9D+SCpVQBnLQQQZkActayObL4GKBdZAG1VAEpXAFWJqhhi+DSyEshblggwLI8ddW2AdGCDr5UAXsLlPABJuBLV09sCUyQNAJhRUQzrVEonkg48sfSYI4vvw32atftWw2VRfXj3oHLOF6/zDV2RnaoTzjmqGthtXDeQb9cN6m1BETY9SP5oMxVzf+5G49zX7opts9R6imIncyKT7mJs4th4AXk2Wla1/Tl14iuhfYTA/R+w7Ut+AB0XQ3uS9UknJR+FfMw3baQm7GX2Lu6zjAndTeXEmnT1jIebyEnI4SanSY6dQxM508WkwNtcX08lkzjrtD42NtdKl1F20rTn+VotW4Q0NlWzCPCiTcjD9Hl6x5Sh97aeSRi9BsgpXAHiiT6JcAjZbC9WQtz5lQKRUX0Wa7LAwCZkOLczvuapAqyjKn0I7ku38bPbAX8vtOCxgFhCxWKbp8b67R2xduki+Y7+GHBIhMJrWpYyJHa22mGaIBqjtcMI3u5fyoAJFKJXa25T75btAU/oE2QT2G7ngQcwcIENvIYxfRZy/Wv5/O1FlILBazBxfCD/997EODTkx+n7ydBylWHdWOvjn8kDCxTzxvpa7LNsKauPx9wiUqIuxQVflGtu/38z0CRyIROfDTAuxFUUK0wEQOdUzERHKyZlKbqPYJRhvrU0XLfewC9VfxLSHqI3rXKRx8z5oaytjSi+q819kHboDbpsJ5SG3nKrgLnLWWZpLHs5vc53cKxuPZQ0WmNPoGX37toVJqzMYAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dim, self.bbox = [], []

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                elif ref_obj is not None:
                    test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def Create_Leader(self, tuple):
                """创建引线标注"""
                Pts, Plane, Style, Text = tuple
                if Pts is None:
                    leader = None
                else:
                    DimStyle = self.Find_DimStyle(Style)
                    leader = rg.Leader.Create(Text, Plane, DimStyle, Pts)
                    leader = initialization.HAE_Leader(leader)
                return leader

            def Get_curve_pt(self, curve):
                """获取线上面的点列表"""
                if curve is None:
                    return None
                pts = []
                if ('ToNurbsCurve' in dir(curve)):
                    curve = curve.ToNurbsCurve()
                # 判断输入的线是否闭合
                if curve.IsClosed:
                    Message.message2(self, "Closed curves do not support this operation!")
                else:
                    if ('Points' in dir(curve)):
                        # 得到线的控制点，并返回在线上的控制点
                        for cp in curve.Points:
                            Pt = rg.Point3d(cp.Location)
                            t = curve.ClosestPoint(Pt)[1]
                            test_pt = curve.PointAt(t)
                            distance = test_pt.DistanceTo(Pt)
                            if distance < 0.001:
                                pts.append(Pt)
                    else:
                        # 将线均分为若干点，得到点列表
                        for t in curve.DivideByCount(100, True):
                            pts.append(curve.PointAt(t))
                Points = System.Array[rg.Point3d](pts)
                return Points

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_curve, match_plane, match_style, match_text = new_list_data
                curve, plane, style, text = self.match_list(match_curve, match_plane, match_style, match_text)

                curve = map(self._trun_object, curve)
                plane = map(self._trun_object, plane)
                style = map(self._trun_object, style)
                text = map(self._trun_object, text)

                pts = map(self.Get_curve_pt, curve)
                Leader = ghp.run(self.Create_Leader, zip(pts, plane, style, text))

                ungroup_data = self.split_tree(Leader, origin_path)

                return ungroup_data


        # 角度标注
        class AngularDim(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_AngularDim", "F15", """Angle dimension""",
                                                                   "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("89cd24a1-2f2d-4276-889d-055eb72dc1d8")

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
                self.SetUpParam(p, "Center_Point", "C", "Central point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Start_Point", "SP", "Starting point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "End_Point", "EP", "End point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Coefficient", "F", "coefficient")
                TOL = 1
                p.SetPersistentData(gk.Types.GH_Number(TOL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "OverWrite", "W", "Manually specify the Angle")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Dihedral", "D", "Inverse or not")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Angle dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "True_Value", "RV", "True value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Display_Value", "SV", "Display value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN/SURBVEhL3ZZZbExRHMbPi9jaqlmq7nRMNaXVJrUVI9pIxVqhFAki9mkV04ililQRaTu2TtEyM6q6oFqaKKXiQYREPHkhsYvUNqV6S2vvfP7n3okud8YSnnzJl0zO/7vnd8495/4zjBRONnmwP/mfyDxpXBSs1iRYsxbBunspQoIDQOORcvnvZcrJnAfgGrmGfBlxsREcwHf2T2TauiGRJj4PV8NJoOUMYoxh/wfAIJf/XgrAmFEDOWCyXPauTKb1cf/8qToCmk/TIUciIizoG9WukJeQ/XiwvXJY35jdTJdqYbp495BXdQS8q8A4Aty5sQe3bubCnBIPrcavjnIZZJX0BCmbCUtzmM5ITrYwta972KMUgNjR4RJAvrqX4Hx8BDsy5kLt3/MZ5RdWsJCYg8wQn8MEG+0kbRcTUixMmC5Pp5TiDIzRoa3DBvdHfq4JzkdHJAj/Pp7ePYxZ00by86mx0iuys+BJWTRxHgvtSjtJtzC9YGPDu8jTtkkBiB0d9pXGE8g7ArR+dRvWJLhBl4HWamxeP5ND7LksMLGAGYzZLMhMO5mQzXQ7CRLNJ20vBcB9TfVyWTrgdbq+KvFs+UbKXZCcmjyZZxxlzBC3hwlSlgCDPZ2HN0DnD20A+XZV2XrKXoSruRJDooJdNPbLnvW7AC59L9/uDS/u2Shfi2s1mTx3XS55158AuFavWTGF8tQYv1VjYlwUz46VS571p4AeapVvfdPTInrmAmor03m2Si55ljdAiFz2qPyqkrX0TK2UjwzXfaKxQLmkVFJnQPTQEA4wktVePJ9/D85XpXj95gTWrpzK81s6Zbg1ZGbemjarDUC9aE6CEf0NAe+C+wWIBr1W7BekEfU6tRgkqEV+XYXA3o2BffwROUiPCHJYqACVv49Lq/EVNWofUa2S3a1rlyYJkLlxtgRopdVwf3GW4TOt7tPLUnx8UYIP5JbnxWh5VozmumN4X1eExieFqL9vg5NuVP0DO948dOAttZSGRw7pdwMt1r0zZt6e3hGAxnJAPKV0U3tXtJn6l8LUXjLo1UuAvTsX0ABvbOd+bpc3V8umNvLDuIpttHAOSJsyfgis1NisWQuRl70I+y2LcXDXEhTQP4xDe5fh8L7lsFHdbjXBkZeEwv3JOHpgBYryU1BckIKSQytRZluF4/bVOOkwo7wwFacrN2HG1BH4DqNEGyW/VsxMAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dimstyle, self.Dihedral, self.bbox = (None for i in range(3))

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def match_tree(self, data_1, data_2, data_3, data_4, data_5, data_6):
                one_trunk, two_trunk, three_trunk, four_trunk, five_trunk, six_trunk = \
                    zip(*map(self.Branch_Route, [data_1, data_2, data_3, data_4, data_5, data_6]))[0]
                zip_list = [one_trunk, two_trunk, three_trunk, four_trunk, five_trunk, six_trunk]
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_trunk = zip_list[max_index]
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                return max_index, map(sub_match, matchzip), max_trunk

            def data_packet(self, data_list):
                # 将两组数据拆开
                data1 = [[_d1[0]] for _d1 in data_list]
                data2 = [[_d2[1]] for _d2 in data_list]

                return data1, data2

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def get_new_SpEp(self, tuple):
                """获取新的起点终点"""
                Center_point, Start_point, End_Point = tuple
                # 如果输入的点有空值，直接返回空值
                if Center_point is None or Start_point is None or End_Point is None:
                    return None, None
                Cp_to_Sp = rg.Vector3d(Start_point - Center_point)
                Cp_to_Ep = rg.Vector3d(End_Point - Center_point)

                Cp_to_Sp.Unitize()  # 单位化向量
                Cp_to_Ep.Unitize()  # 单位化向量
                new_Cp_to_Sp = Cp_to_Sp * 2  # 修改向量的长度
                new_Cp_to_Ep = Cp_to_Ep * 2

                new_Sp_Point = Center_point + new_Cp_to_Sp  # 新起点
                new_Ep_Point = Center_point + new_Cp_to_Ep  # 新终点

                return new_Sp_Point, new_Ep_Point

            def get_Vector(self, tuple):
                """ 根据中点，起点，终点得到两个向量，
                并得到标注的系数点，和中点至系数点的向量"""

                Center_point, Start_point, End_Point, Coefficient = tuple
                # 如果输入的点有空值，直接返回空值
                if Center_point is None or Start_point is None or End_Point is None:
                    return None, None

                # 中点至起点的向量为起点-终点
                new_length = -(abs(Coefficient) + 2) if self.Dihedral else (abs(Coefficient) + 2)  # 根据长度设置反角
                Cp_to_Sp = rg.Vector3d(Start_point - Center_point)
                Cp_to_Ep = rg.Vector3d(End_Point - Center_point)

                Ref_Vector = Cp_to_Sp

                Cp_to_Sp.Unitize()  # 单位化向量
                Cp_to_Ep.Unitize()  # 单位化向量
                new_Cp_to_Sp = Cp_to_Sp * new_length  # 修改向量的长度
                new_Cp_to_Ep = Cp_to_Ep * new_length

                new_Sp_Point = Center_point + new_Cp_to_Sp  # 新起点
                new_Ep_Point = Center_point + new_Cp_to_Ep  # 新终点

                Coeff_Point = rg.Line(new_Sp_Point, new_Ep_Point).PointAt(0.5)

                return Ref_Vector, Coeff_Point

            def Create_AngularDim(self, tuble):
                """创建角度标注"""
                Vector, Center_Point, Start_Point, End_Point, Coeff_Point, OverWrite, Style = tuble
                # 如果输入的点有空值，直接返回空值
                if Vector is None or Center_Point is None or Start_Point is None \
                        or End_Point is None or Coeff_Point is None:
                    return None, None, None

                Dimstyle = self.Find_DimStyle(Style)
                Plane = rg.Plane.WorldXY  # 以世界XY坐标轴作为参考平面

                Plane.Origin = Center_Point
                AngularDim = rg.AngularDimension.Create(Dimstyle, Plane, Vector, Center_Point, Start_Point, End_Point,
                                                        Coeff_Point)
                if OverWrite is not None:
                    AngularDim.RichText = str(OverWrite)  # 标注覆写
                True_Value = math.degrees(AngularDim.NumericValue)  # 角度真实值
                DisPlay_Value = AngularDim.PlainUserText  # 显示值

                AngularDim = initialization.HAE_AngularDim(AngularDim)  # 调用自定义类

                return AngularDim, True_Value, DisPlay_Value

            def match_list(self, *args):
                """匹配两个列表的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def temp_get_newSPEp(self, tuple):
                # 运行中间商
                CP_list, SP_list, EP_list = tuple

                iter_group = self.match_list(CP_list, SP_list, EP_list)
                match_CP, match_SP, match_EP = iter_group
                zip_list = zip(match_CP, match_SP, match_EP)

                Point_List = map(self.get_new_SpEp, zip_list)

                new_SP_List, new_EP_List = zip(*Point_List)
                return list(new_SP_List), list(new_EP_List)

            def temp_get_Vector(self, tuple):
                # 运行中间商
                Center_Point, Start_Point, End_Point, Coefficient = tuple

                iter_group = self.match_list(Center_Point, Start_Point, End_Point, Coefficient)
                match_CP, match_SP, match_EP, match_Coeff = iter_group
                zip_list = zip(match_CP, match_SP, match_EP, match_Coeff)

                vector_Pt = map(self.get_Vector, zip_list)

                Ref_Vector, Coeff_Point = zip(*vector_Pt)
                return list(Ref_Vector), list(Coeff_Point)

            def run_main(self, tuple):
                # 创建标注主方法，还原数据结构
                target_Path, Ref_Vector, CP_trunk_list, new_Sp_Point, new_Ep_Point, Coeff_Point, OverWrite, Style = tuple

                iter_group = self.match_list(Ref_Vector, CP_trunk_list, OverWrite, Style)
                match_ReV, match_CP, match_Over, match_Style = iter_group

                sub_zip_list = zip(Ref_Vector, match_CP, new_Sp_Point, new_Ep_Point, Coeff_Point, match_Over,
                                   match_Style)
                # 创建角度标注

                AngularDim, True_Value, DisPlay_Value = zip(*map(self.Create_AngularDim, sub_zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, target_Path), [AngularDim, True_Value, DisPlay_Value])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Center_Point, Start_Point, End_Point, Coefficient, Style, OverWrite, Dihedral):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    AngularDim, True_Value, DisPlay_Value = (gd[object]() for _ in range(3))
                    CP_factor = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    SP_factor = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
                    EP_factor = self.parameter_judgment(self.Params.Input[2].VolatileData)[0]
                    re_mes = Message.RE_MES([CP_factor, SP_factor, EP_factor],
                                            ['Center_Point terminal', 'Start_Point terminal', 'End_Point terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 匹配树形
                        max_index, iter_group, max_group = self.match_tree(Center_Point, Start_Point, End_Point,
                                                                           Coefficient, OverWrite, Style)
                        iter_group.insert(max_index, max_group)  # 将得到的最长的列表插入到匹配后的数据中
                        target_Path = self.Branch_Route(self.Params.Input[max_index].VolatileData)[1]  # 得到最长的目标路径
                        if len(target_Path) == 0: target_Path = [[0]]  # 如果目标路径为0, 给一个默认的路径

                        # 将匹配后的数据赋值
                        CP_trunk_list = iter_group[0]
                        SP_trunk_list = iter_group[1]
                        EP_trunk_list = iter_group[2]
                        Coefficient_trunk_list = iter_group[3]
                        OverWrite_trunk_list = iter_group[4]
                        OverWrite_trunk_list = OverWrite_trunk_list if OverWrite_trunk_list else [[None] for i in range(
                            len(CP_trunk_list))]  # 覆写没有值默认为None
                        Style_trunk_list = iter_group[5] if iter_group[5] else [[None] for i in range(len(CP_trunk_list))]

                        self.Dihedral = Dihedral  # 反角

                        new_list1 = map(self.temp_get_newSPEp, zip(CP_trunk_list, SP_trunk_list, EP_trunk_list))
                        new_Sp_Point, new_Ep_Point = [result[0] for result in new_list1], [result[1] for result in
                                                                                           new_list1]

                        new_list2 = map(self.temp_get_Vector,
                                        zip(CP_trunk_list, SP_trunk_list, EP_trunk_list, Coefficient_trunk_list))
                        Ref_Vector, Coeff_Point = [result[0] for result in new_list2], [result[1] for result in
                                                                                        new_list2]

                        # 此处运行创建角度标注主方法
                        sub_zip_list = zip(target_Path, Ref_Vector, CP_trunk_list, new_Sp_Point, new_Ep_Point,
                                           Coeff_Point, OverWrite_trunk_list, Style_trunk_list)
                        iter_ungroup_data = zip(*ghp.run(self.run_main, sub_zip_list))
                        AngularDim, True_Value, DisPlay_Value = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return AngularDim, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Angle dimension'


        # 增加绘图框
        class Add_Drawing_Frame(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Add_Drawing_Frame", "F22", """Add frame""",
                                                                   "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a36621e6-f373-46c9-a291-2802b4e876f3")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Rectangle()
                self.SetUpParam(p, "Frame_List", "B", "Box list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Frame_Scale", "S", "Frame scale")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Drawing_area_width", "DW", "Plot width")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Drawing_area_height", "DH", "Plot height")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Frame_width", "FW", "Frame width")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Frame_height", "FH", "Frame height")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Base_Point", "P", "Vector base point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Drawing_Frame", "DF", "Drawing frame")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Picture_Frame", "FL", "Picture frame")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Frame_Scale", "FS", "Frame scale")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJoSURBVEhL7dZdSFNhGAfwly5Kbbtw2V2IdBN9WFd9YHUxK7UMLDGTzMK12QzZKtrC1vwgzY/UbLRKlijO0mgZc86mW2rNAi2TpAspsst2ESuyTKHt6f+e01UXyTnX/uHH2fMezvOwM3jfsX+i+kspVBITG8vWpGxbZ9qSnGhCGSOuikkCfW15XtjlKg/n5+yaRL1dKoUipuzLRwcF+ysItQ42AlsGR6FzuNdKv+Z9VKJNm0XdIsPg9FgT9TjP8wE1oGFxcSvSqyy5ocbakwvt9mK632qk2w2nqK7imGT1lfnU2VJCbejTfF03m75n80OmUsXmULibiF6CD7zgh2GZngDvM0E1ZXkjTKFYntVqK4p4XKXRvm4zeR9cJE+XKdrXZfotFZ6LeNGD9/H0WqNHsnYM4DWxlZAPz9vtenoz2UK6E6nvUa+VoXjEU0aOG0X8N2iDPBCyE7xvg3X4akG6WV84JS5LS0KCMnP+s5NeD1/lAxpgn3ADSQXfeKAKAwLUWHX8nbgsLSqVIvvrp1Z64avkA5phv3ADWRogZGnAolkasGj+NyAFvFPCVjEqe6uIj1ceWAg5aULcKq6Bmq+vgkIYvWsrorFxO2kL1B9Qb5DB4H9soTtNWj6gA3QseX2imW/RAbeVBh5dglIaxNXfI90g8Od5n4D/CllN2T+Yevcmq3hAPAMcNhE3rgMwJMNT8AA/tF7xgVGWlLi6wGw4OHPuTOa3Ww0a6nAYqdqSGzHqM75LZTidMcePS97HdOFw6FDm1mm8JiH8X4F9yH2Zfs71k16zdwH1WRnuzUzahBMNn6sZY2l/AAwq0nZ7CWt1AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def Judge_Frame_Scale(self, Frame_List, Frame_Scale):
                """判断图框比例和图框对象是否匹配"""
                new_Scale = []
                if len(Frame_List) == len(Frame_Scale):
                    for index, Scale in enumerate(Frame_Scale):
                        if len(Scale) != len(Frame_List[index]):
                            scale_data = Scale[-1]
                            s = []  # 根据图框对象放入比例大小
                            for _i in Frame_List[index]:
                                Scale = scale_data if scale_data else 0
                                s.append(Scale)
                            new_Scale.append(s)
                else:
                    if len(Frame_Scale) == 1:  # 如果输入的是一个列表
                        if len(Frame_Scale[0]) == len(Frame_List):
                            for index, Scale in enumerate(Frame_Scale[0]):
                                s = []  # 根据图框对象放入比例大小
                                for _i in Frame_List[index]:
                                    Scale = Scale if Scale else 0
                                    s.append(Scale)
                                new_Scale.append(s)
                        else:  # 若输入的是单个值
                            for index in range(len(Frame_List)):
                                s = []  # 根据图框对象放入比例大小
                                for _i in Frame_List[index]:
                                    ns = Frame_Scale[0][-1] if Frame_Scale[0][-1] else 0
                                    s.append(ns)  # 以最后一个值作为整体比例
                                new_Scale.append(s)
                    else:
                        Message.message2(self, "Frame scale does not match！")
                new_Scale = Frame_Scale if len(new_Scale) == 0 else new_Scale

                return new_Scale

            def Get_Draw_Area(self, tuple):
                """获取绘图框"""
                Frame_list, Frame_scale, Frame_Path = tuple
                Draw_Frame = []
                Lower_left_Point = []
                for index, Frame in enumerate(Frame_list):
                    Plane = rg.Plane.WorldXY
                    Center = Frame.Center
                    Plane.Origin = Center
                    width_domain = self.Drawing_area_width * Frame_scale[index] / 2.0
                    height_domain = self.Drawing_area_height * Frame_scale[index] / 2.0
                    # 根据区间创建Rectangle
                    width = rg.Interval(-(width_domain), width_domain)
                    height = rg.Interval(-(height_domain), height_domain)

                    new_Rectangle = rg.Rectangle3d(Plane, width, height)
                    Draw_Frame.append(new_Rectangle)
                    Lower_left_Point.append(new_Rectangle.Corner(0))

                ungroup_data = self.split_tree(Draw_Frame, Frame_Path)

                Rhino.RhinoApp.Wait()
                return ungroup_data, Lower_left_Point

            def Get_Frame(self, tuple):
                """获取图框"""
                Drawing_left_Point, Frame_scale, Frame_Path = tuple
                Frame = []
                for index, Dl_pt in enumerate(Drawing_left_Point):
                    move_vector = self.Base_Point * Frame_scale[index]
                    new_corner_point = Dl_pt + -(move_vector)
                    Plane = rg.Plane.WorldXY
                    Plane.Origin = new_corner_point
                    # 根据宽高创建Rectangle
                    width = self.Frame_width * Frame_scale[index]
                    height = self.Frame_height * Frame_scale[index]

                    new_Rectangle = rg.Rectangle3d(Plane, width, height)

                    Frame.append(new_Rectangle)

                ungroup_data = self.split_tree(Frame, Frame_Path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_data(self, tuple):
                """还原图框比例的树形结构"""
                Scale, Path = tuple
                ungroup_data = self.split_tree(Scale, Path)

                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Frame_List, Frame_scale, Drawing_area_width, Drawing_area_height, Frame_width,
                          Frame_height, Base_Point):
                try:
                    Drawing_Frame, Picture_Frame, New_Frame_scale = (gd[object]() for i in range(3))
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([Frame_List, Frame_scale], ['Frame_List', 'Frame_scale'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Frame, Frame_Path = self.Branch_Route(Frame_List)
                        Scale = self.Branch_Route(Frame_scale)[0]

                        self.Drawing_area_width = Drawing_area_width if Drawing_area_width else 283  # 初始化绘图区宽
                        self.Drawing_area_height = Drawing_area_height if Drawing_area_height else 161  # 初始化绘图区高
                        self.Frame_width = Frame_width if Frame_width else 297  # 初始化图框宽
                        self.Frame_height = Frame_height if Frame_height else 210  # 初始化图框高
                        self.Base_Point = Base_Point if Base_Point else rg.Vector3d(10.5, 45.5, 0)  # 初始化基点向量

                        New_Scale = self.Judge_Frame_Scale(Frame, Scale)  # 判断图框比例和图框对象是否匹配

                        zip_data1 = zip(Frame, New_Scale, Frame_Path)
                        iter_ungroup_data_Draw, pt = zip(*map(self.Get_Draw_Area, zip_data1))
                        zip_list2 = zip(pt, New_Scale, Frame_Path)
                        iter_ungroup_data_Frame = map(self.Get_Frame, zip_list2)
                        iter_ungroup_data_Scale = map(self.temp_data, zip(New_Scale, Frame_Path))

                        Drawing_Frame = self.format_tree(iter_ungroup_data_Draw)
                        Picture_Frame = self.format_tree(iter_ungroup_data_Frame)
                        New_Frame_scale = self.format_tree(iter_ungroup_data_Scale)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Drawing_Frame, Picture_Frame, New_Frame_scale

                finally:

                    self.Message = 'Add frame'


        # 获取块
        class Get_block_By_Name(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Get_block_By_Name", "F24", """Get block""",
                                                                   "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3bf8ff3c-a3a2-4a7d-91b0-a4658f5759c6")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Block_Name", "N", "Block_Name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Update", "U", "Update")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Block", "B", "Block")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPOSURBVEhLzZV7TNVlGMeZkhwRdR0VJwqHGBhylQAxNakUo3bEG8KAOZS8RTacAdp0q7wsEmtIS5iIECBXL9xUXGQWM52Ymzidf4hr2IwVhRgMUo/fvs/vVY8Hz8FL/tF3++z8zjm/9/s87/M+7/va/R9kT1JIBHGQH56nJpKfVidFICF2JkbpnVr5/WsyhziS/6TYCS76zurydABHgbt1aL+Sh9K9KYhdNA1jnUe28Z09xEhGyICn0Qqdwws49d02mp8ATLXAzUrg7yr1TDp+yceBklQsiQvHeBf9dY4pIouIXgwGlIOD/bmE6OkIf80Xxshg5O5cibZLOcCdGs6EASSQBJRgnNmNa4Wor9qAlctm4yWD8x+0qCQJZLz49ZdnaJCHCTjCLPeiaPcaxMfMQGiwJ4xvhyA7MwmtLV8Bt6o18wfBtOD83r0fx6o3Qf+iE+h1RllaKn3LxhiW5jBwo0INRB062wpQVbwOifGvY0qIJyIjgpC5bQku/5wF9B3S3pExVy/uQhRn/bKXiwT4Qllaqrml6XMOOghTR+kDtGCSNY26rxehhou/PHEWwkK9EPFGAL7MWIrSgrVwnzAaxXkfII6NQK8wZWmWl7+Pq+muTPmvMosAD4PO8nvB6tH7ewkaWJKlXGz7wYNw4fQOmPi/0zCdtPRgZWvWuk82RGsD+5vaQguGb1FbmoboqDA+n0R+9irJPlNZWqqppWn7I+V5HLK4c1n3ktz3GaARb70ZKAGmKEuzDP4+brdUecqtGlkDXRX4szUPAb5uuPlrITqu5mGYo+4K/R4pT/KmDxcwg8NWjWwhXVack6zNQDblN7uSJfssZWmpxubGrcA/h6wa2ULWS2q/O2sFn49j3jshEmCmsjRrnLfXuN47smCkv4ktpHW7uD8C/AwszR50XSvAyBGOckYNUbZmJaWuMT59eW7XoIq9HzkrkGO/R0V+imSfqywtVX+yYbPW2/1NBkLKE88zK/uzRD6fQMyCVyWA3BsWcjO4jlE7lecPeg8OuMnuI6Xs4Y6e7O+O3y7noKe9mPfF8Hb6DVW2ZgXqdEPOzpjqjYxPE3D+1A51gDE72Q+2WlZmW7svFeHTJ2nlqS9Lk+wLlKV1+ZF00hQc5HH7448Wo/mHDK3PtWDsrocbQNZLjodsnkFSHuOcVyTAXDF6EslVuZYcnxxg6NuYtlC7fOSM0YLxHuhlSST7i5xxzPypYl5InunO9iDvkQZfH7ee1JQonP5xO45UroeHuzMmTXTp43+r5cXnIVfyLqkb7jS0m5+XSAixITu7fwGUqPnwTQWg8AAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.InsDefblock = []
                self.InsTanblock = []
                self.block_objects = []
                self.Brep, self.Point, self.Curve, self.Dim = ([] for i in range(4))

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def Find_Block_by_name(self, tuple):
                """根据图块名查找图块"""
                Name, Path = tuple
                Geo = []
                for n in Name:
                    if n == '' or n is None:  # 判断n值是否为空值或者empty
                        block = None
                    else:
                        find_block = sc.doc.InstanceDefinitions.Find(n)
                        if find_block is None:
                            block = None
                        else:
                            self.InsDefblock.append(find_block)
                            block = find_block.GetReferences(1)[0].Geometry
                            self.InsTanblock.append(block)
                    Geo.append(block)
                if None in Geo:
                    Geo = []
                ungroup_data = self.split_tree(Geo, Path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def Graft_List(self, List, Path):
                """列表升树"""
                Tree = gd[object]()
                Path = GH_Path(tuple(Path))
                if len(List) == 0:
                    Tree.AddRange(List, Path)
                else:
                    if len(List) == 1:
                        Tree.Add(List[0], Path)
                    else:
                        for index, n in enumerate(List):
                            New_Path = Path.AppendElement(index)
                            Tree.Add(n, New_Path)
                return Tree

            def Get_BlockObj(self):
                # 获取到块里面的物体
                if len(self.InsDefblock) == len(self.InsTanblock):
                    for _index in range(len(self.InsDefblock)):
                        xf = self.InsTanblock[_index].Xform
                        for obj in self.InsDefblock[_index].GetObjects():
                            Geo = obj.Geometry
                            Geo.Transform(xf)  # 移动变换
                            self.block_objects.append(Geo)
                else:
                    print("An undescribable error occurred in the program！")

            def Draw_object(self):
                # 将需要显示的物体分类
                for block in self.block_objects:
                    block = block.ToBrep() if 'ToBrep' in dir(block) else block  # 将块物件转为Brep
                    block = block.ToNurbsCurve() if 'ToNurbsCurve' in dir(block) else block  # 将块物件转为NurbsCurve
                    str_type = str(type(block))
                    if 'Brep' in str_type:
                        self.Brep.append(block)
                    elif 'Point' in str_type:
                        self.Point.append(rg.Point3d(block.Location))
                    elif 'NurbsCurve' in str_type:
                        self.Curve.append(block)
                    elif 'Text' in str_type or 'Dim' in str_type:
                        self.Dim.append(block)
                    else:
                        pass

            def RunScript(self, Block_Name, Update):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Data_Tree, Block = gd[object](), gd[object]()
                    # 判断输入
                    factor_bool = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    re_mes = Message.RE_MES([factor_bool], ['Block_Name end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Tree, Tree_Path = self.Branch_Route(Block_Name)
                        for index, G in enumerate(Tree):
                            Data_Tree.MergeTree(self.Graft_List(G, Tree_Path[index]))

                        Name, Name_Path = self.Branch_Route(Data_Tree)

                        zip_list = zip(Name, Name_Path)
                        iter_ungroup_data = ghp.run(self.Find_Block_by_name, zip_list)
                        Block = self.format_tree(iter_ungroup_data)
                        self.Get_BlockObj()
                        self.Draw_object()

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Block
                finally:
                    self.Message = 'Get block'

            def DrawViewportWires(self, args):
                try:
                    for brep in self.Brep:  # 重绘Brep
                        args.Display.DrawBrepWires(brep, System.Drawing.Color.FromArgb(0, 150, 0))

                    for Point in self.Point:  # 重绘Point
                        args.Display.DrawPoint(Point, System.Drawing.Color.FromArgb(0, 150, 0))

                    for Curve in self.Curve:  # 重绘Curve
                        args.Display.DrawCurve(Curve, System.Drawing.Color.FromArgb(0, 150, 0))

                    for Dim in self.Dim:  # 重绘Dim
                        args.Display.DrawAnnotation(Dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except Exception as e:
                    print(e)


        # 解构块
        class Deconstruct_Block(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Deconstruct_Block", "F25",
                                                                   """Destructor block""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("40337116-88d7-4247-9bea-9d79661319de")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Block", "B", "Block")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Name", "N", "Name")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Plane", "P", "Plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Geometric objects in a block")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASpSURBVEhLtZZ7UJRVGMY/dpdl7xeWRWBZFsF1FzKdUUiZwAuWohBgKTiIJUI3ktEupCNqUBoZSRcdJZi8YICIRIH0B6JGTkzolE0OMiWRQ9CQmRcuCQL79J5vYRNZZqSZnpnffOfbPec573nPe84ud4+UI8//TbHEx4SUf7PLMvIclYFQ2ZuTl1rIcTZ6NhPziAyim5hKmIi9RCPx31cqcXE5kKvRI1QsQbibFEXuXhC7uHRESeQ9VlcxqEuSvefkJSDciXeeV2hw1286OgyBgH8QCmmSRJkSKoHgNn0fwjo/oBYQwfYmx/kTvyWQUcMUI+Bn4XlT7YGlEjkylFrMdHUDRTFM/S4RecQyYgoxKi2RZm9yUUQfYeXfRpQ4100y1Gc0o80nANFSOTYoNeild/hbUUwrcRcK8fSahSj/NBMZ6dHw9Xa/SeMqiGRi6zSRK0QcV0Yp7jeLXG8xU4foi22UChtMVj4lOoEQb2k8cMrTiBZPEwxyKc6d2QWgnjhJ1OGHxjz4SSRIEsthIvMltFq1QID3tHo87CpuI9sg5i0jimgzsZqM42UKfpO7aA+q9QYsp3cvjmMbjMyNsbjYtAe4fZwmqCG+QnZOEnYIZPxKW7ynoobGbFPr+InYGDaBB7GWWEKEEZdZRPGcAJUKPd6VarAgJgS5u1Ow+eU4xEWHIiZqDl7fFIfPK7Pw1KpwpEsUgCmIsGDAOB07aIJpIr7qWJmP01UPuQQ5eamICDFDQlE0NeRStGfsqfm7Es3n87FvTyoSVoRBTpE+S3tVrPNGrd4Xc2n1eVTqaQo1vITCrhFPh4L9/fSDP154n8zq0fXrJ1j82Cz88v2HQE8Fhq+XwvZXKd/GcDX1qUP5sUxYXETIUrrzabno7c+nK4D2xGxfxRhl7929jh84/GcJ0HsCw2Q40HWUN78foBYvpi/HSlrlC1IVsig113wC8apCy4zvECztDgmkUrefOpv3241HTW4eo6jLxhjzn/edQEtTPvRaBZ6kVMkMWuRK1QhTKSGSiaGhKiRPdr4cevSJqNnAUDVs95k5w0aV1PrdB7hyaR9uXD0ItVrODiLWr1sMnU71DfkVEOzAOVRQfnAjYKtxajgOlkK+XE8hZ8sqREY8hM2vxCN7y0oWeYrdknMbeXIyvU71R3f7IX6QU0Mn2G5Q6rqPI3R2IC6c3okh+sxq9uklP1b6Y7QiNXkRRXPSqdFEYKAKp6uyEBFmpbH1OFu9nUVfbrccq6pztdnA4BdOjSaCVdEzq+cjL2cNtRuQnBDOJoi2W/6rAKNBh97OI/wAvr57K5xWzr3gVjl6Og5j1gwTrrUWouf3I9BqFJ3k58j7qMxisag4yGJoS1m7CGWHNqH98gGg/zM+Zeiv4kt13ARUbUcLXsLSyJnUrxGlhRtY9B/ZLZ2Lzczuou0qlfTryIUz7rz9RhLOn83FIDNklxtbHTvF7DTbqhG3LAR1lVvR3noYwRZfNsEcZvSgYr/D7BIsCQ4ytj+3/nFUlryGriuFNNmXuN5ahHl0VxXkp8FTp/iZ+o2p+cmKXenziZ0eOtW3sTGP3E2k00upZVHvJyb4p8Fx/wAq6HDUOYq6dQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def Graft_List(self, List, Path):
                """列表升树"""
                Tree = gd[object]()
                Path = GH_Path(tuple(Path))
                if len(List) == 0:
                    Tree.AddRange(List, Path)
                else:
                    if len(List) == 1:
                        Tree.Add(List[0], Path)
                    else:
                        for index, n in enumerate(List):
                            New_Path = Path.AppendElement(index)
                            Tree.Add(n, New_Path)
                return Tree

            def Get_Block_Attr(self, tuple):
                block_list, block_Path = tuple
                block_name, block_Plane, block_objects = [], [], []
                for block in block_list:
                    xf = block.Xform  # 获取这个块的变换矩阵
                    # Base_Point = rg.Point3d(xf.M03, xf.M13, xf.M23) # 获取基准点
                    InsDef = sc.doc.InstanceDefinitions.FindId(block.ParentIdefId)  # 转为InstanceDefinitionGeometry对象
                    block_name.append(InsDef.Name)  # 获取图块名
                    for _ in InsDef.GetObjects():  # 获取图块的物体
                        Geo = _.Geometry
                        Geo.Transform(xf)
                        block_objects.append(Geo)
                    Plane = rg.Plane.WorldXY
                    Plane.Transform(xf)  # 转换平面
                    block_Plane.append(Plane)
                ungroup_data = map(lambda x: self.split_tree(x, block_Path), [block_name, block_Plane, block_objects])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Block):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Data_Tree, Name, Plane, Geometry = (gd[object]() for i in range(4))
                    # 判断输入
                    re_mes = Message.RE_MES([Block], ['Block end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Tree, Tree_Path = self.Branch_Route(Block)  # 解构树形
                        for index, G in enumerate(Tree):
                            Data_Tree.MergeTree(self.Graft_List(G, Tree_Path[index]))
                        Block_data, Block_Path = self.Branch_Route(Data_Tree)
                        zip_list = zip(Block_data, Block_Path)
                        iter_ungroup_data = ghp.run(self.Get_Block_Attr, zip_list)

                        Name, Plane, Geometry = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                        zip(*iter_ungroup_data))
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Name, Plane, Geometry
                finally:
                    self.Message = 'Deconstruct Block'


        # 在犀牛空间创建一个文本注解
        class Create_Text(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CreateText", "F31", """Create a text annotation in the Rhino space""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("07661e79-4bdc-4b45-8902-98e761c26c90")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Text", "T", "Text")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOxSURBVEhL7VRrUIxRGF62EUVWbUQNchlhxtZ22QyxtVrLZqUQK1G7pGTDjC5Ik1q6oSZtl3UZsVFobbuVMhq3kRnlOi4Nk5lMJlSMLFptr/fUt9If0/jjB8/MM9953/eZ85zvnPcc2n/8G7BDsn7Dicg/h99it9R7N9Oh4Voq1NWkwFX1XrhdnQx3aw9CQ91hCFzGUVPSP8PyJR4pD29lwr3radD8WAHQUwmtjUp4eucIND5SwEoRp5ySDgoMhgWL7Twl2sbGyp1K0ZhIF6Rz4DJPHTHwX+quwdgTyUYykIOG11ynhI5XJ8FP4JpFpfoh3bDoOBh1EBK0MJdKmQv5zsn7E8U3ZJHCcjqd7os5CwcH6xX4JYsyYaaZmZkXft09XKcVwqcLsMrfs4LJtArqK1OQhvCKiMFGMVeB4VBZuOARieG7FgBqQX1mVzfmg3MzJZCbEdaJ42FIZt4hqV6ZHQ5sluPn1qYT0N1RCt3tJfDmWQFgvR8mA2mwz0Fzc7pvZ8tpqNbsa/OZNyt222aBpgdXFiDiHAlaMTetBycYP46xjTt/VgbAFdizM0A3c4Z9dF7W5maiK1ZGt6Ulih9QU/fBZIAHKxfy2cnQeRHsJ1grsURHsq5eSoCi/Kg6HE++UZFkyMsK/6opjfv+vD6brNQbSXOZPSmJbBHfm5VH4gEwGQh4rMwICb/IqC+DmrK93ypL4w1V5+O7jN8ugapQ1k60gSLPAtCrgeglwd663gkQIoGrHDovQKjYO59K9cNkwOfOORy1SVBi/KKGqvO7v2qLY/SEpefiP2L+MSXnNd3PATBowYM9NZXKEYMDxGDjWm4BleqHySBQxDkQ4MeRG94Ww0iL4QlYskRaIIcQHYEkxEerb1XBRzyLU4rID5gi7U7zF7qlEoN1qxccJfEAmAzWr1kod3BgSuBzGcTJll/H0hiknZ3t6ABHx7GLcMxuvJsNR9PDXq9f7fUEDOXg5jwlhczhNc8pAXBrwzfwyF0a+MxEhC1WAVyDLaF8ckkm12r2YXtWQvnZWMMVPOC3r0+Tp6N+R4RQS/bfabr9JtRxWl8cg4qSOD2OrSwtzXktT/PhPXbgKcXWgW261NdFWaVLwg6Y0/t7rNmT9hTkRDaXqWI+KHMiXu7a7q+yZoxMT09aZ0iMWdmEkhFEFyrm1pwplHXZ2lhFYjhUGuJz+3KV3IgN8Y7UfwXZihnIX5+H4chRyJ/7j3BE2vQNe2GGJK+ydW/UFxMNObv/+Kug0X4ArtS9wxpMbcUAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def Creat_TextEntity(self, tuple):
                """创建文本标注"""
                plane, text, style = tuple
                if plane and text:
                    DimStyle = self.Find_DimStyle(style)
                    TextEntity = rg.TextEntity.Create(text, plane, DimStyle, True, 0, 0)
                    TextEntity.Justification = rg.TextJustification.MiddleCenter  # 设置对齐方式
                    TextEntity = initialization.HAE_Text(TextEntity)  # 传入自定义文本类
                else:
                    TextEntity = None

                return TextEntity

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def run_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                Plane, Text, Style = new_list_data

                if len(Plane) == 0 or len(Text) == 0:
                    Text_List = []
                else:
                    match_Plane, match_Text, match_Style = self.match_list(Plane, Text, Style)

                    Text_List = map(self.Creat_TextEntity, zip(match_Plane, match_Text, match_Style))

                ungroup_data = self.split_tree(Text_List, origin_path)

                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [
                    map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
                    for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))

                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = map(self.run_main, zip_list)
                Text = self.format_tree(iter_ungroup_data)

                return Text

            def RunScript(self, Plane, Text, Style):
                try:
                    Text_result = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    re_mes = Message.RE_MES([Plane, Text], ['Plane', 'Text'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # self.DimStyle = self.Find_DimStyle(Style)  # 查找标注样式
                        Text_result = self.temp_by_match_tree(Plane, Text, Style)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Text_result
                finally:
                    self.Message = 'Text'


        class ViewMake2D(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ViewMake2D", "F111", """Create 2D Views of an Object from Multiple Angles""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4bdbdb2c-b060-41f7-8636-1b04ec504717")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Obj", "G", "Object for Make2D")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Main View Plane for Make2D")
                p.SetPersistentData(gk.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "X Spacing", "X", "Spacing between Views in X Direction")
                p.SetPersistentData(gk.Types.GH_Number(100))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Y Spacing", "Y", "Spacing between Views in Y Direction")
                p.SetPersistentData(gk.Types.GH_Number(100))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "3D Scale", "3D S", "Scaling Ratio of 3D View")
                p.SetPersistentData(gk.Types.GH_Number(0.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "3D X", "3D X", "Distance of 3D View in X Direction")
                p.SetPersistentData(gk.Types.GH_Number(300))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "3D Y", "3D Y", "Distance of 3D View in Y Direction")
                p.SetPersistentData(gk.Types.GH_Number(300))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Visible Curve", "Vi", "Visible Lines of Views")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Hidden Curve", "Hi", "Hidden Lines of Views")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Rectangle()
                self.SetUpParam(p, "Single Frame", "S", "Bounding Box of Single View Frame")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Rectangle()
                self.SetUpParam(p, "Frame List", "B", "Overall Bounding Box Frame")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Three-View Drawing'
                # 初始化输出端数据内容
                Visible_Curve, Hidden_Curve, Singe_View, View_Outline = [gd[object]() for _ in range(4)]
                if self.RunCount == 1:
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    p3 = self.Params.Input[3].VolatileData
                    p4 = self.Params.Input[4].VolatileData
                    p5 = self.Params.Input[5].VolatileData
                    p6 = self.Params.Input[6].VolatileData
                    # 判断是否为空
                    j_bool_f1, obj_trunk, obj_path = self.parameter_judgment(p0)
                    pln_trunk = self.parameter_judgment(p1)[1]
                    x_spac_trunk = self.parameter_judgment(p2)[1]
                    y_spac_trunk = self.parameter_judgment(p3)[1]
                    _3d_scal_trunk = self.parameter_judgment(p4)[1]
                    _3d_x_spac_trunk = self.parameter_judgment(p5)[1]
                    _3d_y_spac_trunk = self.parameter_judgment(p6)[1]
                    re_mes = Message.RE_MES([j_bool_f1], ['O end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        self.bbox = rg.BoundingBox.Unset
                    else:
                        # 获取右击菜单的设置值
                        self.meun_list_num = []
                        for _ in ['A', 'B', 'C', 'D', 'E', 'F']:
                            self.meun_list_num.append(self.settings.GetValue(str(self.InstanceGuid) + _, 0))

                        if self.meun_list_num[2] == 0:
                            self.meun_list_num[2] = 1
                        else:
                            self.meun_list_num[2] = 0

                        if self.meun_list_num[4] == 0:
                            self.meun_list_num[4] = 1
                        else:
                            self.meun_list_num[4] = 0

                        if self.meun_list_num[5] == 0:
                            self.meun_list_num[5] = 1
                        else:
                            self.meun_list_num[5] = 0

                        # 生成原始zip列表
                        iter_group, max_i = self.match_tree(obj_trunk, pln_trunk, x_spac_trunk, y_spac_trunk, _3d_scal_trunk, _3d_x_spac_trunk, _3d_y_spac_trunk)
                        obj_trunk, pln_trunk, x_spac_trunk, y_spac_trunk, _3d_scal_trunk, _3d_x_spac_trunk, _3d_y_spac_trunk = iter_group
                        zip_list = zip(obj_trunk, pln_trunk, x_spac_trunk, y_spac_trunk, _3d_scal_trunk, _3d_x_spac_trunk, _3d_y_spac_trunk, obj_path)
                        # 多进程函数运行
                        iter_ungroup_data = zip(*ghp.run(self._do_main, zip_list))

                        Visible_Curve, Hidden_Curve, Singe_View, View_Outline = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                        self.bbox = rg.BoundingBox.Unset
                        view_list_box = [_.BoundingBox for _ in list(chain(*(zip(*zip(*iter_ungroup_data[-1])[0])[0])))]
                        for _ in view_list_box:
                            self.bbox.Union(_)

                DA.SetDataTree(0, Visible_Curve)
                DA.SetDataTree(1, Hidden_Curve)
                DA.SetDataTree(2, Singe_View)
                DA.SetDataTree(3, View_Outline)

            def get_ClippingBox(self):
                return self.bbox

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQRSURBVEhLrZV/TJVlFMfhgiDmvQjcixAKiGmMQpGx2szSEHVgisuZ/BC6zKWwnEJNK5loSS5cIPKjS4VXowIVrSXOUkhC+EObUQjhFhO8VPbD0pDSsKvfvueBF5rV9eY622fv8573Oec8zznPc14XijcJv0MCiA8J+xf8iUuaq6srPDzc/4an56h/1AtubjrQtpzk0t6u0+nsHNu1sTz5XkVc0iPCg2DrKIftTBl6viglJTjfVoqfz72Jb758DT2flwzpB7HZdiMzI04CWMjmxIQYdHVZETrRhA1rF3FcDXPybPleLQHSoqeHAgPvA9feA349AFw9qJ6rzXHoPFkI3Dw0qNfAMWx8Zom2g03m5Eeoa8TUyYHY8XI6x6ewfs1j8v0dFSAqMgT4ZR9waS9u/FQN9O1D/9d7ZALqqtfT4EOHAVY8MYu6jzAlLAAFW1I4bkJ2ZrzjAFd6d8PbMAbW0tXo/up1nGvdOUx39y7ubu7IDlJm0+kJ3HtPIEpeMXPciufXLXYUYD8u9+yC0U8Pd3c3eN5SYE+PUX8t8qaF82fg+McFMPrqkbR0Jmpq8rAgdpqDAFf2s8CV0I8djcqdq9D+WTHamguGaT9TjozUOcMBDHovtdvx/t7wNxlgNOoxxsvDcYAfu96AFyedrN/KLbMGUngNNCD32ZEaJD0+E32X96Kfab16oQp2+6Hb1KC/Ft+dtUCnc0XT4c3qhIleAzisjqMWIHWZFPmIqp3ywwXlZCWMBIiZETa4SplEYzkR4Iqm3x+C3vYyvtcP6TWaseW5pcMBJF3AJ6RuiBN4ITtxOMDKoEAfFG1LRxHPcGF+mqKIbMxZgldfWqHGml59K3oKsQ/fJw6sJF8WWFaaidKCDEVZWRYenRUh3w9KgHnk+B2yjphJM2kijaSBHCVHSDb5X8WNjCOTyIMknjgtU4jsNoXIyraRSvIBaSGd5ALpJ5IeIYM4JYvJNaIM5bLJ08SLGBE+AQ89MBUpbG5xcyIhnXlo3jLilCwi9gBeotp3N6ClPh9Bgb5IjI8ZbJDq5DXhos2K6Gmh/9n5QvLHeJM3Oj4tpqMGrHpyrrofVRVP463KtepU5eUuR3CQn+Z8uRg6Iwnkur/RgPZTbNlsx29bspSTcd53qfRMZnv29RmrORaSiFMi1b/u72dAm/wPeHluXKpB33kruk4X4/uzFbj52wHYOi2IjAjWnEvxnZIFZEBy3nl6B50fHew/Kt9yi4+p3XzLXiX9n3OFVDF0RuaT30MmGtHavB12/lx6+Rtta9mOxro81O7JgaVwJV7MS8akYJPmPE0MnRHJuTKacLcvoqPCIPn3Gq3a7q0MkB9IOnFK4shFIkYdRK699JEKspWsIXI6YkkUCSEGchtxcfkTSFRBFEkY0KUAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.settings = Grasshopper.Instances.Settings

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def sub_match(self, tuple_data):
                # 子树匹配
                target_tree, other_tree = tuple_data
                t_len, o_len = len(target_tree), len(other_tree)
                if o_len == 0:
                    new_tree = [other_tree] * len(target_tree)
                else:
                    new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                return new_tree

            def match_tree(self, *args):
                # 参数化匹配数据
                len_list = map(lambda x: len(x), args)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = args[max_index]
                other_list = [args[_] for _ in range(len(args)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                # 插入最大列表，获得最新列表
                reslut_list = map(self.sub_match, matchzip)
                reslut_list.insert(max_index, max_trunk)
                return reslut_list, max_index

            def AppendAdditionalMenuItems(self, items):
                try:  # always everything inside try
                    # context menu item 1
                    component.AppendAdditionalMenuItems(self, items)
                    image = None

                    self.item_1 = items.Items.Add("Front View", image, self.OnClicked1)
                    enabled_a = self.settings.GetValue(str(self.InstanceGuid) + 'A', 0)
                    if enabled_a == 0:
                        self.item_1.Checked = True
                    else:
                        self.item_1.Checked = False

                    self.item_2 = items.Items.Add("Left View", image, self.OnClicked2)
                    enabled_b = self.settings.GetValue(str(self.InstanceGuid) + 'B', 0)
                    if enabled_b == 0:
                        self.item_2.Checked = True
                    else:
                        self.item_2.Checked = False

                    self.item_3 = items.Items.Add("Right View", image, self.OnClicked3)
                    self.item_3.Checked = False
                    enabled_c = self.settings.GetValue(str(self.InstanceGuid) + 'C', 0)
                    if enabled_c == 1:
                        self.item_3.Checked = True
                    else:
                        self.item_3.Checked = False

                    self.item_4 = items.Items.Add("Top View", image, self.OnClicked4)
                    enabled_d = self.settings.GetValue(str(self.InstanceGuid) + 'D', 0)
                    if enabled_d == 0:
                        self.item_4.Checked = True
                    else:
                        self.item_4.Checked = False

                    self.item_5 = items.Items.Add("Bottom View", image, self.OnClicked5)
                    self.item_5.Checked = False
                    enabled_e = self.settings.GetValue(str(self.InstanceGuid) + 'E', 0)
                    if enabled_e == 1:
                        self.item_5.Checked = True
                    else:
                        self.item_5.Checked = False

                    self.item_6 = items.Items.Add("3D Perspective", image, self.OnClicked6)
                    self.item_6.Checked = False
                    enabled_f = self.settings.GetValue(str(self.InstanceGuid) + 'F', 0)
                    if enabled_f == 1:
                        self.item_6.Checked = True
                    else:
                        self.item_6.Checked = False

                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked1(self, sender, none_e):
                try:
                    tool_button_1 = self.item_1.Checked
                    if tool_button_1 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'A', 1)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'A', 0)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked2(self, index, value):
                try:
                    tool_button_2 = self.item_2.Checked
                    if tool_button_2 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'B', 1)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'B', 0)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked3(self, index, value):
                try:
                    tool_button_3 = self.item_3.Checked
                    if tool_button_3 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'C', 0)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'C', 1)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked4(self, index, value):
                try:
                    tool_button_4 = self.item_4.Checked
                    if tool_button_4 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'D', 1)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'D', 0)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked5(self, index, value):
                try:
                    tool_button_5 = self.item_5.Checked
                    if tool_button_5 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'E', 0)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'E', 1)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def OnClicked6(self, index, value):
                try:
                    tool_button_6 = self.item_6.Checked
                    if tool_button_6 is True:
                        self.settings.SetValue(str(self.InstanceGuid) + 'F', 0)
                    else:
                        self.settings.SetValue(str(self.InstanceGuid) + 'F', 1)
                    self.ExpireSolution(True)
                except Exception, ex:
                    System.Windows.Forms.MessageBox.Show(str(ex))

            def get_xy_point(self, pt):
                new_pt = copy.copy(pt)
                new_pt.Z = 0
                return new_pt

            def get_xy_min_max_pt(self, curves):
                mid_pts = []
                for crv in curves:
                    crv.Domain = rg.Interval(0, 1)
                    mid_pts.append(crv.PointAt(0.5))
                # X轴方向最大最小的点
                x_sorted_point = sorted([(_[0], _) for _ in mid_pts])
                x_max_point = x_sorted_point[-1][1]
                x_min_point = x_sorted_point[0][1]

                # y轴方向最大最小的点
                y_sorted_point = sorted([(_[1], _) for _ in mid_pts])
                y_max_point = y_sorted_point[-1][1]
                y_min_point = y_sorted_point[0][1]

                return x_max_point, x_min_point, y_max_point, y_min_point

            def get_new_view_plane_x(self, origin_pt, dis_1, dis_2):
                view_pt = copy.copy(origin_pt)
                view_pt.X += dis_1
                view_pt.X += dis_2
                return view_pt

            def get_new_view_plane_y(self, origin_pt, dis_1, dis_2):
                view_pt = copy.copy(origin_pt)
                view_pt.Y += dis_1
                view_pt.Y += dis_2
                return view_pt

            def get_bbox(self, geo_list):
                unset_bbox = rg.BoundingBox.Unset
                for _ in geo_list:
                    unset_bbox.Union(_.GetBoundingBox(True))
                return unset_bbox

            def get_thickness_box(self, u_bbox):
                u_box = rg.Box(u_bbox)
                if u_box.Z == rg.Interval(0, 0):
                    u_box.Z = rg.Interval(-50, 50)
                else:
                    u_box = u_box
                return u_box

            def new_make_2d(self, view_geo_list):
                visible_curve, hidden_curve = [], []
                # 单一视窗
                bbox_list = map(self.get_bbox, view_geo_list)
                # 定义视图参数
                parameters = rg.HiddenLineDrawingParameters()
                parameters.AbsoluteTolerance = sc.doc.ModelAbsoluteTolerance
                parameters.Flatten = True
                parameters.IncludeHiddenCurves = True
                parameters.IncludeTangentEdges = True
                parameters.IncludeTangentSeams = True
                # 整体视窗
                view_bbox = rg.BoundingBox.Unset
                for b in bbox_list:
                    view_bbox.Union(b)

                chain_view_geo_list = chain(*view_geo_list)
                for view_index, view_g in enumerate(chain_view_geo_list):
                    # 添加物体
                    parameters.AddGeometry(view_g, '')

                # 设置视图方位
                point_list = list(view_bbox.GetCorners())
                rot_pt = (point_list[0] + point_list[6]) / 2
                ht = point_list[4].Z - point_list[0].Z
                z_vec = Rhino.Geometry.Vector3d.ZAxis
                __view = Rhino.Display.RhinoViewport()
                __view.ChangeToParallelProjection(True)
                __view.SetCameraTarget(rot_pt - (z_vec * ht), False)
                __view.SetCameraLocation(rot_pt + z_vec * ht, False)
                # 设置视图
                parameters.SetViewport(__view)
                # 生成视图
                hld = rg.HiddenLineDrawing.Compute(parameters, True)

                for hld_curve in hld.Segments:
                    cur = hld_curve.CurveGeometry.DuplicateCurve()
                    if cur.IsValid and cur.GetLength() != 0:
                        # 区分可见线与不可见线
                        if hld_curve.SegmentVisibility == Rhino.Geometry.HiddenLineDrawingSegment.Visibility.Visible:
                            visible_curve.append(cur)
                        elif hld_curve.SegmentVisibility == Rhino.Geometry.HiddenLineDrawingSegment.Visibility.Hidden:
                            hidden_curve.append(cur)
                        else:
                            pass
                # 可见线与不可见线视框
                visible_bbox, hidden_bbox = rg.BoundingBox.Unset, rg.BoundingBox.Unset
                for c1 in visible_curve:
                    c1_bbox = c1.GetBoundingBox(True)
                    visible_bbox.Union(c1_bbox)
                for c2 in hidden_curve:
                    c2_bbox = c2.GetBoundingBox(True)
                    hidden_bbox.Union(c2_bbox)
                # 将物体位置置于水平面
                tg_box_point = view_bbox.Center
                tg_box_point.Z = 0
                visible_point = visible_bbox.Center
                hidden_point = visible_bbox.Center

                target_plane = ghc.XYPlane(tg_box_point)
                visible_plane = ghc.XYPlane(visible_point)
                hidden_plane = ghc.XYPlane(hidden_point)

                xform_visible = rg.Transform.PlaneToPlane(visible_plane, target_plane)

                xform_hidden = rg.Transform.PlaneToPlane(hidden_plane, target_plane)

                [_.Transform(xform_visible) for _ in visible_curve]
                [_.Transform(xform_hidden) for _ in hidden_curve]

                # 闭包算法分割每个视窗线位置
                def get_view_point(con_curve):
                    sub_visible_list, sub_hidden_list = [], []
                    for v_ in visible_curve:
                        if con_curve.Contains(v_.PointAt(v_.DivideByCount(2, False)[0])) != rg.PointContainment.Outside:
                            sub_visible_list.append(v_)

                    for h_ in hidden_curve:
                        if con_curve.Contains(h_.PointAt(h_.DivideByCount(2, False)[0])) != rg.PointContainment.Outside:
                            sub_hidden_list.append(h_)
                    return sub_visible_list, sub_hidden_list

                curve_list = map(self.get_curve_list, bbox_list)
                res_visible_curve, res_hidden_curve = zip(*map(get_view_point, curve_list))
                # 整体View线框返回
                total_box = rg.BoundingBox.Unset
                for view_c in bbox_list:
                    total_box.Union(view_c)

                def flatten_box(need_box):
                    need_box = rg.Box(need_box)
                    need_box.Z = rg.Interval(0, 0)
                    return need_box

                box_list = map(flatten_box, bbox_list)
                total_box = flatten_box(total_box)

                return res_visible_curve, res_hidden_curve, box_list, total_box

            def get_curve_list(self, sub_bbox):
                temp_pts = sub_bbox.GetCorners()
                pts = [temp_pts[0], temp_pts[1], temp_pts[2], temp_pts[3], temp_pts[0]]
                cur = rg.PolylineCurve(pts)
                return cur

            def get_obj_list_bbox(self, obj_list, data_list):
                # 获取集合内数据
                pln, x_spac, y_spac, _3d_scal, _3d_x_spac, _3d_y_spac = data_list
                # 初始化集合数据
                x_spac, y_spac, _3d_scal, _3d_x_spac, _3d_y_spac = float(x_spac.Value), float(y_spac.Value), float(_3d_scal.Value), float(_3d_x_spac.Value), float(_3d_y_spac.Value)
                pln = pln.Value
                # 初始化物体列表包围框
                obj_group_bbox = rg.BoundingBox.Unset
                for o in obj_list:
                    obj_group_bbox.Union(o.Boundingbox)
                # 物体中心点
                obj_group_bbox_center = obj_group_bbox.Center
                obj_group_bbox_center_xy = self.get_xy_point(obj_group_bbox_center)
                center_pln, center_pt_xy = rg.Plane(obj_group_bbox_center, rg.Vector3d(0, 0, 1)), rg.Plane(obj_group_bbox_center_xy, rg.Vector3d(0, 0, 1))

                orient_obj_list = ghc.Orient(obj_list, center_pln, center_pt_xy)['geometry']
                orient_obj_list = orient_obj_list if type(orient_obj_list) is list else [orient_obj_list]

                # 获取映射物体的外包围框和中心点
                orient_obj_list_bbox = rg.BoundingBox.Unset
                [orient_obj_list_bbox.Union(_.GetBoundingBox(True)) for _ in orient_obj_list]

                orient_obj_list_center = obj_group_bbox_center_xy

                pln.Origin = orient_obj_list_center
                orient_obj_list = ghc.Orient(orient_obj_list, pln, center_pt_xy)['geometry']
                orient_obj_list = orient_obj_list if type(orient_obj_list) is list else [orient_obj_list]

                # 获得最底下的面
                orient_obj_list_bbox = self.get_thickness_box(orient_obj_list_bbox)
                orient_obj_surface = orient_obj_list_bbox.ToBrep().Faces[4].ToNurbsSurface()
                brep_ = orient_obj_surface.ToBrep()
                box_pts = [_.PointAt(_.DivideByCount(2, False)[0]) for _ in brep_.Edges]
                box_distances = [_.DistanceTo(orient_obj_list_center) for _ in box_pts]

                # 主视图平面
                front_plane = rg.Plane(orient_obj_list_center, rg.Vector3d(0, 0, 1))
                # 获得四个方向的视图
                right_pt = self.get_new_view_plane_x(orient_obj_list_center, -1 * box_distances[0], -1 * x_spac)
                right_plane = rg.Plane(right_pt, front_plane.ZAxis, front_plane.YAxis)

                left_pt = self.get_new_view_plane_x(orient_obj_list_center, box_distances[2], x_spac)
                left_plane = rg.Plane(left_pt, front_plane.ZAxis * -1, front_plane.YAxis)

                bottom_pt = self.get_new_view_plane_y(orient_obj_list_center, -1 * box_distances[1], -1 * y_spac)
                bottom_plane = rg.Plane(bottom_pt, front_plane.XAxis, front_plane.ZAxis)

                top_pt = self.get_new_view_plane_y(orient_obj_list_center, box_distances[3], y_spac)
                top_plane = rg.Plane(top_pt, front_plane.XAxis, front_plane.ZAxis * -1)
                # 获取3D视图平面
                _3d_point = bottom_pt
                _3d_point.X -= _3d_x_spac
                _3d_point.Y -= _3d_y_spac
                _3d_plane = rg.Plane(_3d_point, rg.Vector3d(0, 0, 1))
                _3d_plane.Rotate(math.radians(-55), _3d_plane.XAxis)
                _3d_plane.Rotate(math.radians(-45), _3d_plane.ZAxis)
                # 判断有多少个选择项
                pln_list = [front_plane, left_plane, right_plane, bottom_plane, top_plane, _3d_plane]
                need_obj_list = []
                for index, meun_item in enumerate(self.meun_list_num):
                    if meun_item == 0:
                        new_geo_list = ghc.Orient(orient_obj_list, front_plane, pln_list[index])['geometry']
                        new_geo_list = new_geo_list if type(new_geo_list) is list else [new_geo_list]
                        need_obj_list.append(new_geo_list)

                v_curve_list, h_curve_list, single_outline, total_outline = self.new_make_2d(need_obj_list)

                return v_curve_list, h_curve_list, single_outline, total_outline

            def _do_main(self, tuple_data):
                # 分解集合数据
                obj_list, pln_list, x_spac_list, y_spac_list, _3d_scal_list, _3d_x_spac_list, _3d_y_spac_list, origin_path = tuple_data

                # 获得最新列表
                map_list = self.match_tree(pln_list, x_spac_list, y_spac_list, _3d_scal_list, _3d_x_spac_list, _3d_y_spac_list)[0]
                sub_zip_list = zip(*map_list)
                # 返回列表物体的包围盒
                reslut_list = []
                for set_data in sub_zip_list:
                    reslut_list.append(self.get_obj_list_bbox(obj_list, set_data))
                # 多进程批量处理
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), zip(*reslut_list))
                Rhino.RhinoApp.Wait()
                return ungroup_data


        # 获取CAD图框信息
        clr.AddReference("Interop.AutoCAD")
        from AutoCAD.AcadApplication import ActiveDocument
        from AutoCAD import AcadApplicationClass


        class Get_CAD_Attribute(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Get_CAD_Attribute", "F23",
                                                                   """Gets the CAD frame properties""", "Scavenger",
                                                                   "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("63938b6a-0fe7-4979-a107-e2ce5cca45d2")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Frame_Path", "F", "Frame Dwg file path")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Get", "G", "Gets the frame properties if True")
                Default_Bool = False
                p.SetPersistentData(gk.Types.GH_Boolean(Default_Bool))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attribute_labels", "L", "Frame properties label")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attribute_value", "V", "Frame property value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Drawing_width", "DW", "Drawing width")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Drawing_height", "DH", "Drawing height")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Frame_width", "FW", "The frame width")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Frame_height", "FH", "The frame area is high")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Base_Point", "P",
                                "The frame area is a vector between base points at the bottom left of the drawing area")
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
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)
                        self.marshal.SetOutput(result[4], DA, 4, True)
                        self.marshal.SetOutput(result[5], DA, 5, True)
                        self.marshal.SetOutput(result[6], DA, 6, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHmSURBVEhL7dVPSBRhGAbwSRGUrQVdx0oNdXbXFrq4Mop07CAeAm8KHhb2YEqZqx4qMgQ7qZtBEVTQzYMkKigIYSF4EFEPoUSi5dr6jy5RBm4G8ozPuzoiC6ssjrd94cd+37vD+/DNwIzCukmPqPMcyFzlBRk2W/o3Ndu+YQnVvpGRkbYkcyWg11OcGwZCvcD3ZmDRAqFmw1jtynFc+iwBPQXX1G2fr3KA64BVGhpuD2U7Lq5yrfTQOslxrLRDy6QE83Mdv+vqbskJHh6Sh/OL5MLZw15C/P6qwaxMW4hrJVihu/8ZRviObI6VpEvAq+guwQJW2lza5R+yDuolWgT41BL956BSaYUk4J00Ei3Oa9cK1GRA/EoGnFrJgNhKo2qqoUxpAB+fWBWg0hzJtSJMbmA+YFXAczKHm4aBL/e1QjX6uj5rwCTFBiwBHzoYIDPiBpiv635pnFDdFBvwHvjadHSC8lJtF5i4K5tj9ZTeUG10d3KN0H/ao2myAwtNrqKcNa6VZzeu520BM2+ByRY5CcMCwLIfCPv4sOoPevFM3ZPfsYEHo8N9rePYHXrM4Y3A9Osrqn1BAl6mpFwwPJ78n7rXGZHbJcpKtB2T2YunzKv9rdBdW7RZ7nX+0UudEbf7Kj/DirEPMGPhbMpTHOwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.acad = None

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

            def sort_points(self, list_point):
                """点排序"""
                total_list = [[_.X, _.Y, list_point.index(_)] for _ in list_point]
                Index = [_[-1] for _ in sorted(total_list)]
                Sort_P = [list_point[_] for _ in Index]
                return Sort_P

            def Get_AcDbPolyline_Points(self, Polyline):
                """将CAD图框内置的两个线框转换为点列表"""
                Polyline_Points = []
                for line in Polyline:
                    point_list = line.Coordinates
                    points = [rg.Point3d(point_list[i], point_list[i + 1], 0) for i in range(0, len(point_list), 2)]
                    Polyline_Points.append(points)
                list_box_info = self.Get_Box_info(Polyline_Points)  # 调用Get_Box_info方法
                return list_box_info

            def Get_Box_info(self, Points):
                """获取绘图区和图框区信息"""
                list_box_info = []
                for pt in Points:
                    sort_corners = self.sort_points(pt)  # 将点进行排序
                    pt_left_lower = sort_corners[0]  # 取出左下点
                    # 取出两个区域的长和宽
                    height = pt_left_lower.DistanceTo(sort_corners[1])
                    width = pt_left_lower.DistanceTo(sort_corners[2])
                    info = (float('%.4f' % width), float('%.4f' % height), pt_left_lower)
                    list_box_info.append(info)
                return list_box_info

            def RunScript(self, Frame_Path, Get):
                try:
                    Attribute_labels, Attribute_value, Drawing_width, Drawing_height, Frame_width, Frame_height, Base_Point = (
                        gd[object]() for i in range(7))
                    re_mes = Message.RE_MES([Frame_Path], ['Frame_Path'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    elif not os.path.exists(Frame_Path):
                        Message.message2(self, "The path of the frame template does not exist！")
                    else:
                        if Get:
                            # 获取cad块中属性值
                            try:
                                self.acad = System.Runtime.InteropServices.Marshal.GetActiveObject(
                                    "AutoCAD.Application")
                            except:
                                self.acad = AcadApplicationClass()
                                self.acad.Visible = False
                            doc = self.acad.Documents.Open(Frame_Path)
                            for entity in doc.ModelSpace:
                                # 如果对象是一个块引用，获取其属性
                                if entity.EntityName == 'AcDbBlockReference':
                                    block_reference = entity
                                    break

                            Attribute_labels = [_.TagString for _ in block_reference.GetAttributes()]  # 属性标签
                            Attribute_value = [_.TextString for _ in block_reference.GetAttributes()]  # 属性值

                            Polyline = [entity for entity in doc.ModelSpace if
                                        entity.EntityName == 'AcDbPolyline']  # 获取线框

                            if len(Polyline) == 2:
                                # 排序判断获取绘画框和图框获取
                                s_list_box_info = sorted(self.Get_AcDbPolyline_Points(Polyline))

                                Drawing_width = s_list_box_info[0][0]  # 绘图区框
                                Drawing_height = s_list_box_info[0][1]  # 绘图区高
                                Drawing_pt_left_lower = s_list_box_info[0][2]

                                Frame_width = s_list_box_info[1][0]  # 图框区宽
                                Frame_height = s_list_box_info[1][1]  # 图框区高
                                Frame_pt_left_lower = s_list_box_info[1][2]  # 图框基点

                                # 获取基点间向量
                                Base_Point = rg.Vector3d(Drawing_pt_left_lower - Frame_pt_left_lower)
                            else:
                                Message.message2(self, 'Must contain a drawing line and frame line！')

                            doc.Close()

                    return Attribute_labels, Attribute_value, Drawing_width, Drawing_height, Frame_width, Frame_height, Base_Point
                finally:
                    self.Message = 'Gets the CAD frame properties'


        # 导出CAD并套图框
        clr.AddReference("Interop.AutoCAD")
        # from AutoCAD.AcadApplication import ActiveDocument
        from AutoCAD import AcadApplicationClass
        from AutoCAD import AcadApplication
        from AutoCAD import AcadApplication


        class Export_to_CAD(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Export_to_CAD", "F21",
                                                                   """Export CAD and frame""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("77586548-8aa5-4be3-9f04-1c0e4a9a586e")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Frame_Path", "F", "Path of the frame template (suffix required)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Storage_Path", "SP", "Save path (Please do not enter a suffix)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Attribute_labels", "L", "Attribute label to be modified")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Attribute_value", "V", "Attribute value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Rectangle()
                self.SetUpParam(p, "Frame_List", "FL", "Frame list")
                p.DataMapping = Grasshopper.Kernel.GH_DataMapping.Flatten
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Object_List", "O", "List of objects after Bake (enter Guid)")
                p.DataMapping = Grasshopper.Kernel.GH_DataMapping.Flatten
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Frame_Scale", "FS", "Frame scale")
                p.DataMapping = Grasshopper.Kernel.GH_DataMapping.Flatten
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Export", "E", "Export button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFlSURBVEhL7Za/SwJhGMcdQghqbGiJBmlsMvH0Oi4kCETyTsvkEvyVg1CLtuRBmU2RS5MErSHUYA5JYUKbEDQG/QdtDQ1S8fDtOQnjFoU4m/zCB77vOzyfF97hfW0cH3PIlIaAMddWZjBEuiaj7DOqhewxXcHRT3EZCwszz5gExl1YGZEZCfpmJBiYkWBgRoKB+X+B11hYGCdjEsQYh4VEmK7AeDexoXooFlmkxrVO25kVKuQUat0c0FrQTXpepWJhneLaEvlkJ4leF3kEN4miSLIskyRJJAgCeT0ukqUFioQlniWSSVC/2MXrSwXAA9p3JeCtyr2J53YZ+Kxxb6HVOEOn0+HeP0+P97i9zBvDfwV8ehwXNdBXHdXzHTRrOj7er6DnFJyUNlE5zSC75Uc45IcSXEU0GkUikUA6nUYymYSmaVAVBSE1gFQ8gGxquScw/SrmHNOYnBiH3T6G2Zmp3v7fsOEbA/wow72a5+gAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.acad, self.Attribute_labels, self.model_space, self.Frame_Path = (None for i in range(4))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def Get_Attribute_dict(self, Attribute_value):
                """将属性值以字典的形式存储"""
                if len(self.Attribute_labels) == len(Attribute_value):
                    Attribute_dict = {k: v for k, v in zip(self.Attribute_labels, Attribute_value)}
                else:
                    Message.message2(self, "The attribute tag and attribute value do not match well！")

                return Attribute_dict

            def export_objects_to_cad(self, Object_List, Storage_Path):
                """将物体导出到CAD中"""
                rs.UnselectAllObjects()  # 取消Rhino中选中的物体

                rs.SelectObjects(Object_List)  # 根据Guid选中物体

                new_path = Storage_Path + '.dwg' if '.dwg' not in Storage_Path else Storage_Path
                command = '_-Export "{}" _Enter'.format(new_path)
                rs.Command(command)
                rs.UnselectAllObjects()  # 取消Rhino中选中的物体

            def add_attributes_to_cad(self, block_reference, attributes_data):
                """将属性值写入到图框中"""
                for attribute in block_reference.GetAttributes():
                    tag = attribute.TagString  # 获取图框的属性标签
                    if tag in attributes_data:
                        data = attributes_data[tag] if attributes_data[tag] else '-'
                        attribute.TextString = data

                block_reference.Update()

            def Get_Insert_Point(self, Rectangle):
                """获取到图框插入点"""
                Rec_point = Rectangle.Center  # 获取矩形的中心点
                point = System.Array.CreateInstance(System.Double, 3)
                point.SetValue(Rec_point[0], 0)  # X坐标
                point.SetValue(Rec_point[1], 1)  # Y坐标
                point.SetValue(Rec_point[2], 2)  # Z坐标

                return point

            def Get_Polyline_CenterPt(self, Poly_list):
                """得到最长的Poly的中心点"""
                max_length = -1
                longest_curve = None
                Box = None

                for curve in Poly_list:  # 得到最长的线
                    length = curve.GetLength()
                    if length > max_length:
                        max_length = length
                        longest_curve = curve

                if longest_curve:  # 求中心点
                    Box = longest_curve.GetBoundingBox(True)
                return Box

            def Set_Frame(self, Array_Point, Frame_Scale):
                """套图框操作"""
                block_reference = None
                AcDbBlock, PolyCurve = [], []
                Array_Block = self.model_space.InsertBlock(Array_Point, self.Frame_Path, Frame_Scale, Frame_Scale,
                                                           Frame_Scale, 0)
                Explode_Array_Block = Array_Block.Explode()  # 将插入的图框炸开
                for block in Explode_Array_Block:
                    if block.ObjectName != "AcDbBlockReference":
                        if block.EntityName == 'AcDbPolyline':
                            point_list = block.Coordinates
                            points = [rg.Point3d(point_list[i], point_list[i + 1], 0) for i in
                                      range(0, len(point_list), 2)]
                            points.append(points[0])
                            curve = rg.PolylineCurve(points)
                            PolyCurve.append(curve)
                        block.Delete()  # 删除里面不属于图框的块
                    else:
                        AcDbBlock.append(block)

                Array_Block.Update()
                Array_Block.Delete()  # 删除导入整合的块

                Box = self.Get_Polyline_CenterPt(PolyCurve)  # 得到图框的中心点

                length_AcDbBlock = len(AcDbBlock)

                if length_AcDbBlock != 0:
                    block_reference = AcDbBlock[0]
                    for _ in range(1, length_AcDbBlock):
                        AcDbBlock[_].Delete()
                    if Box:
                        block_reference.Move(self.Get_Insert_Point(Box), Array_Point)  # 将图框移动到中心点

                    return block_reference
                else:
                    Message.message2(self, "The frame path inside the kerosene matches the frame！")

            def run_main(self, tuple):
                Point, Attribute, Frame_Scale = tuple

                block_reference = self.Set_Frame(Point, Frame_Scale)  # 套图框操作

                self.add_attributes_to_cad(block_reference, Attribute)  # 改变图框属性

            def RunScript(self, Frame_Path, Storage_Path, Attribute_labels, Attribute_value, Frame_List, Object_List,
                          Frame_Scale, Export):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    re_mes = Message.RE_MES([Frame_Path, Storage_Path, Attribute_labels, \
                                             Attribute_value, Frame_List, Object_List, Frame_Scale], \
                                            ['FP', 'SP', 'A-label', 'A-value', 'F-List', 'Obj-List', 'Frame_Scale'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    elif not os.path.exists(Frame_Path):
                        Message.message2(self, "The path of the frame template does not exist！")
                    else:
                        if Export:
                            self.Attribute_labels = filter(None, Attribute_labels)  # 将输入的属性标签定义为类对象
                            Cut_None_FrameList = filter(None, Frame_List)
                            trunk_Attribute_value = filter(None, self.Branch_Route(Attribute_value)[0])
                            Frame_Scale = filter(None, Frame_Scale)

                            if len(Cut_None_FrameList) == len(trunk_Attribute_value) == len(
                                    Frame_Scale):  # 判断属性值和图框列表是否匹配
                                try:
                                    self.acad = System.Runtime.InteropServices.Marshal.GetActiveObject(
                                        "AutoCAD.Application")
                                except:
                                    self.acad = AcadApplicationClass()
                                    self.acad.Visible = False
                                Attribute_dict = ghp.run(self.Get_Attribute_dict,
                                                         trunk_Attribute_value)  # 将属性值和属性标签写入字典中
                                ArrayPoint = ghp.run(self.Get_Insert_Point, Frame_List)  # 获取到点列表
                                self.export_objects_to_cad(Object_List, Storage_Path)  # 将物体列表导出到CAD
                                Storage_doc = self.acad.Documents.Open(Storage_Path)  # 打开导出的CAD文件
                                self.model_space = Storage_doc.ModelSpace
                                self.Frame_Path = Frame_Path
                                zip_list = zip(ArrayPoint, Attribute_dict, Frame_Scale)
                                map(self.run_main, zip_list)
                                Storage_doc.Save()
                            else:
                                Message.message2(self, "The data don't quite match！")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                finally:
                    self.Message = 'Export CAD and frame'


        #
        class PolylineAngleDim(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PolylineAngleDim", "F34", """Multi-line Angle dimension""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7c5be027-0008-4280-a928-57afb4f6e117")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "polyline")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Coefficient", "F", "coefficient")
                p.SetPersistentData(gk.Types.GH_Number(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "90?", "90?", "If False, 0, 90, 180, 270 are no dimension")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Dihedral", "D", "Perigonal Angle or not")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "True_Value", "V", "True Value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Display_Value", "S", "Display Value")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQZSURBVEhL3ZV7UJRVGMZ3WXZZcLntLgsICTpdSCIdFWrNBEmGNBZUwGZWrZwsR0ciTaPLKBTeaLzkoIOO4wUFDMxILhFqV5sma6wZs6wpR5w0MgrxQiKXfXrOy9oQA7H90x89M7/Z/c73fc973nPe836a/7UcZB1Z6yGriIF4pAhyIyUxDlkz7chMS8AcZyJGRtnAcSEtdRxmZ09CpiMBWbMmwhxkUuPLiUc6mPxgLIA6wFXD32O4cqEUAf6+KMp3YlxcNLLS75NxoEF+y0oWqwBtJEQc/kEP+xoNOPvVFvfLDWj5aS+iIq1ItMfwuhFN35bA6KPHzEficfNKlfu5OtgT7lRBSnptBpYP+TEvNx3XLlfiy+NFWFc4F4EmIyaMHYWrl8qAaweB7sM4/fkmhIcGITLcjK2bF6Dp3G4cbyhQgXvocY+4DaBCguFhwfDz84Fer0MEDQpezEbX5TeAPw6hp6VcQOfbaLtYiqVL0mA1+0PvrUPUbVYYjXqVRaO49dNdpJNg5YpZ+OSj9fjh5OtwtdIYtUBbZa/5bxW9qCBX1fLUooOZnWS2e7kPfr4GKQIyjfxNx+Y7k7Bo/lTExkRyc2na8RbAmf9lOgjqGbXRq1ZkShZPzZuiAnxDdOJMOU3DjGg5uxPdfNib6W5ePU9m199sINBRjRNHV8vMP67PB9oPIcwWpK4XK/NwrVb7y5b1j0slAO/gpWUzEDncjB4ugav1wICmfVHZpk8bj6RJo90e9dhdvBD0bVEBcizcpM5bFcLZfPHeGnh5aXHh620y1t+wL/j9AGf8JqJHhKCowCnmam+6fi1HiCVAZaGxabWaixtYjnLzZjU+bXwVOp0Xfma9DxVAge4aJD0w2n346MEsdrB0mcElFUApW5XluVPFvPk+nl00HaOiQ+HizDxaoq7DqN63TPag+cx2dLHyQqwy+6fF3a13H2XfaWsul1NauSuXwT6Ueu8t0UHMeU9lDRxBavIYci/ynnEo81NEK85u3c5l6RgbOwLmYBPKdixByaYFqK/MQ3vzPjm9fY1dau17anCdh+2zI4VorMtHxc4c7p2XZEJSxLWfVMuF1eIPG9tARIRFTqZKt7bqBVnbvuZbNzyJ4KBhMBi84W/yRagtUEqcHvXiNoD05PuFTzwkBmAjU41ueY6kjKrSpRJE8dorc2Rs49rHcP677WhnMVTvf05tbDfHY8igmqqO+5kTG2VZcJ2lyw665uXZYth0ehvOs3zV//1sDcBR4AZPPPfKHi/dtFiZDKWKyao1qyxugQ8wlx+Y8WNGInlyLGZMnyBjMgm2iT08WHyvlVjEYQiFkfbEiXcjnT3fwa9XBms8JSlOZq6wx9+BjIz75Z6DX7zAAD81nks8VipZ+S94nniT/1IazZ+rPaF8jnr+egAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dimstyle, self.Dihedral, self.bbox = (None for i in range(3))

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def get_new_SpEp(self, Center_point, Start_point, End_Point):
                """获取新的起点终点"""
                # 如果输入的点有空值，直接返回空值
                if Center_point is None or Start_point is None or End_Point is None:
                    return None, None
                Cp_to_Sp = rg.Vector3d(Start_point - Center_point)
                Cp_to_Ep = rg.Vector3d(End_Point - Center_point)

                Cp_to_Sp.Unitize()  # 单位化向量
                Cp_to_Ep.Unitize()  # 单位化向量
                new_Cp_to_Sp = Cp_to_Sp * 2  # 修改向量的长度
                new_Cp_to_Ep = Cp_to_Ep * 2

                new_Sp_Point = Center_point + new_Cp_to_Sp  # 新起点
                new_Ep_Point = Center_point + new_Cp_to_Ep  # 新终点

                return new_Sp_Point, new_Ep_Point

            def get_Vector(self, Center_point, Start_point, End_Point, Coefficient):
                """ 根据中点，起点，终点得到两个向量，
                并得到标注的系数点，和中点至系数点的向量"""

                # 如果输入的点有空值，直接返回空值
                if Center_point is None or Start_point is None or End_Point is None:
                    return None, None

                # 中点至起点的向量为起点-终点
                new_length = -(abs(Coefficient) + 2) if self.Dihedral else (abs(Coefficient) + 2)  # 根据长度设置反角
                Cp_to_Sp = rg.Vector3d(Start_point - Center_point)
                Cp_to_Ep = rg.Vector3d(End_Point - Center_point)

                Ref_Vector = Cp_to_Sp

                Cp_to_Sp.Unitize()  # 单位化向量
                Cp_to_Ep.Unitize()  # 单位化向量
                new_Cp_to_Sp = Cp_to_Sp * new_length  # 修改向量的长度
                new_Cp_to_Ep = Cp_to_Ep * new_length

                new_Sp_Point = Center_point + new_Cp_to_Sp  # 新起点
                new_Ep_Point = Center_point + new_Cp_to_Ep  # 新终点

                Coeff_Point = rg.Line(new_Sp_Point, new_Ep_Point).PointAt(0.5)

                return Ref_Vector, Coeff_Point

            def Create_AngularDim(self, Vector, Center_Point, Start_Point, End_Point, Coeff_Point, style):
                """创建角度标注"""
                # 如果输入的点有空值，直接返回空值
                if Vector is None or Center_Point is None or Start_Point is None \
                        or End_Point is None or Coeff_Point is None:
                    return None, None, None

                Dimstyle = self.Find_DimStyle(style)
                Plane = rg.Plane.WorldXY  # 以世界XY坐标轴作为参考平面
                Plane.Origin = Center_Point
                AngularDim = rg.AngularDimension.Create(Dimstyle, Plane, Vector, Center_Point, Start_Point, End_Point, Coeff_Point)
                True_Value = math.degrees(AngularDim.NumericValue)  # 角度真实值
                DisPlay_Value = AngularDim.PlainUserText  # 显示值

                AngularDim = initialization.HAE_AngularDim(AngularDim)  # 调用自定义类

                return AngularDim, True_Value, DisPlay_Value

            def Get_Curve_PointEnd(self, curve, other_curve):
                """判断线的两端点是否为交点"""
                Point_List = [curve.PointAtStart, curve.PointAtEnd]

                O_Point_List = []
                for pt in Point_List:
                    t = other_curve.ClosestPoint(pt, False)[1]
                    closest_point = other_curve.PointAt(t)
                    if closest_point.DistanceTo(pt) < 1e-6:
                        O_Point_List.append(pt)
                Rhino.RhinoApp.Wait()
                return O_Point_List

            def Get_SP_EP_MP(self, curve):
                # 获取线的中点
                Mid_length = curve.GetLength() / 2  # 将线的长度除2
                t = curve.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                Mid_Point = curve.PointAt(t)  # 根据t值求中心点

                return Mid_Point

            def Get_Curve_AngularDim(self, tuple_data):
                # 得到线的角度标注
                curve_1, curve_2, coefficient, style = tuple_data
                curve_1_MP = self.Get_SP_EP_MP(curve_1)  # 获取线的中点
                curve_2_MP = self.Get_SP_EP_MP(curve_2)  # 获取线的中点

                Center_Point = self.Get_Curve_PointEnd(curve_1, curve_2)[0]  # 求两根线之间的交点
                New_SP_Point, New_END_Point = self.get_new_SpEp(Center_Point, curve_1_MP, curve_2_MP)  # 得到新的起点和终点

                Ref_Vector, Coeff_Point = self.get_Vector(Center_Point, curve_1_MP, curve_2_MP, coefficient)  # 得到参考向量和系数点

                # 得到角度标注，真实值和显示值
                AngularDim, True_Value, DisPlay_Value = self.Create_AngularDim(Ref_Vector, Center_Point, New_SP_Point, New_END_Point, Coeff_Point, style)

                if not self.Retain:  # 如果为False则0, 90, 180, 270不标注
                    if True_Value in [0, 90, 180, 270]:
                        AngularDim, True_Value, DisPlay_Value = None, None, None
                return AngularDim, True_Value, DisPlay_Value

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def _run_main(self, tuple_data):
                """运行主方法"""
                curve, coefficient, style = tuple_data
                AngularDim, True_Value, DisPlay_Value = [], [], []
                if curve is None:  # 如果curve为空
                    return AngularDim, True_Value, DisPlay_Value
                if curve.IsClosed:  # 曲线是闭合的
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) != 1:
                        Shift_Explode_Curves = list(Explode_Curves[1:])
                        Shift_Explode_Curves.extend(list(Explode_Curves[:1]))  # 偏移一下曲线列表
                        match_coefficient = self.match_list(Shift_Explode_Curves, [coefficient])[1]
                        match_style = self.match_list(match_coefficient, [style])[1]
                        curve_zip_list = zip(Explode_Curves, Shift_Explode_Curves, match_coefficient, match_style)
                        AngularDim, True_Value, DisPlay_Value = zip(*map(self.Get_Curve_AngularDim, curve_zip_list))  # 得到角度标注
                else:
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) > 1:  # 线数小于1，你求个嘚的角度
                        if len(Explode_Curves) == 2:
                            # 只有两根线的情况
                            curve_zip_list = zip([Explode_Curves[0]], [Explode_Curves[1]], [coefficient], [style])
                            AngularDim, True_Value, DisPlay_Value = zip(*map(self.Get_Curve_AngularDim, curve_zip_list))  # 得到角度标注
                        else:
                            Curves_1_List = Explode_Curves[1:]  # 去除首尾两根线段
                            Curves_2_List = Explode_Curves[:-1]

                            match_coefficient = self.match_list(Curves_1_List, [coefficient])[1]
                            match_style = self.match_list(match_coefficient, [style])[1]
                            curve_zip_list = zip(Curves_2_List, Curves_1_List, match_coefficient, match_style)

                            AngularDim, True_Value, DisPlay_Value = zip(*map(self.Get_Curve_AngularDim, curve_zip_list))  # 得到角度标注

                AngularDim = list(filter(None, AngularDim))
                True_Value = list(filter(None, True_Value))
                DisPlay_Value = list(filter(None, DisPlay_Value))

                return AngularDim, True_Value, DisPlay_Value

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_curves, match_coefficient, match_Style = new_list_data

                curves, coefficient, Style = self.match_list(match_curves, match_coefficient, match_Style)

                zip_list = zip(curves, coefficient, Style)
                AngularDim, True_Value, DisPlay_Value = zip(*ghp.run(self._run_main, zip_list))

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [AngularDim, True_Value, DisPlay_Value])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [
                    map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
                    for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))

                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = zip(*map(self._do_main, zip_list))
                AngularDim, True_Value, DisPlay_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                return AngularDim, True_Value, DisPlay_Value

            def RunScript(self, Curves, Style, Coefficient, Retain, Dihedral):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    AngularDim, True_Value, DisPlay_Value = (gd[object]() for _ in range(3))

                    # self.dimstyle = self.Find_DimStyle(Style)
                    self.Dihedral = Dihedral if Dihedral is not None else False
                    self.Retain = Retain if Retain is not None else False
                    re_mes = Message.RE_MES([Curves], ['Curves'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        AngularDim, True_Value, DisPlay_Value = self.temp_by_match_tree(Curves, Coefficient, Style)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return AngularDim, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Multi-line Angle dimension'


        # 线长标注
        class UnifyCurve:
            def __init__(self):
                self.plane = rg.Plane.WorldXY

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

            def is_curve_closed(self, curve):
                # 使用Curve.IsClosed方法来检查曲线是否闭合
                # "---------------------"
                if curve:
                    return curve.IsClosed
                else:
                    return None
                # "---------------------"

            def unify_curve(self, curve, plane):
                flag = str(curve.ClosedCurveOrientation(plane))
                if flag == 'Clockwise':
                    curve_f = curve
                    curve_f.Reverse()
                    bool = True
                else:
                    curve_f = curve
                    bool = False
                return curve_f, bool

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if ref_obj is None:
                    return None
                elif 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj.Value
                return test_pt

            def match_list(self, *args):
                """匹配子树"""
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group


        class PolylineDimension(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PolylineDimension", "F35", """Line length dimension""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f03a809e-fc41-4c83-adbf-d27fee280129")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "polyline")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension Style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Coefficient", "F", "Coefficient")
                p.SetPersistentData(gk.Types.GH_Number(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "True_Value", "V", "True Value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Display_Value", "S", "Display Value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAK/SURBVEhLtdVdSFNhHAZwt0zXZiVmZBnmRxZ2U2gRZKBU9AVFRYQUGBhY0UU3hkEf2E1JIkSZlqIkkV8tldRpN1IRIREYWnaR0BLL0LRMTU23p+d/xqGTnrPNix74MZG9z//d2XvOAgwSSDbPn/8nydRDhZRCJjKKhXbQXWohM/nMBYLGW8qlrBnu0EfSvjeafKaVlAW2EAts1mBYSX3Vkv9ZgudrBxwhrwmjEYKjJht9zlL0vis09OV9EXo+FCNxfYw64BZ5zR5CZvo2AM3AqJ0eGhshONBaf1Ed8FpKvOVp+JKFGHSWscAO17cKn9yDFYDrMfbtSpQB4xSpNOnkOKHs5knuqgmugQe6hXowWYeutnwEzjPLEDl9sxJK/cmb1wITdXAPVekWeSObOnNipwyYpnVSqk2R2WxC+7NcYKqeu9cv8QZjdvR3lyB0sVWGNHlqPdlEOJu523NpdBb7hZdU1uflHJUBYruUy534KmbVUgz3liunQnexnzBcjQm+JqyJlAHtMmA/4cbVdE5/Ale//1+sLuVTtOB2Xob6KZQbqztpQyx+f6+C+0e1/kI/uaWDx3srDwt7nTJAotxc1y6lcbpjTsfzH8ruG3Gv4JS6+zQpV1NrXRAEZ0cBMF6rX+ADftZg9Ot9rFwRJuVtntq/iaKxA3s3Au4G3p2VuiWGlN07cOX8YXX38siflWxCY+U5vrlhTpcKvx7hMx98ITaLlNuVNp3IL1lnXPQyjMui4RrdspncJOc/41iqlE9SnJQZ5SDhctYhLuLTlKfCJ17SN89zYTKZZEC+0uIlETQRFBSIjhfX4eKRm+K9YWSa39XYUCVStiSo1z5JSnylk5RnSjzvyPjYCGOrlyPKc2qE/FCFk8+Uk7pIDFA9lWg0UB9p39dFfuU0faJikkeJ3O16WUSplEMvqZQ0CQj4AxtlJxdqDIoRAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dimstyle, self.Dihedral, self.bbox = (None for i in range(3))

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def compare_curves(self, A_Curve_List, B_Curve_List):
                """对两组线进行比较"""
                result_curves = []
                for acurve in A_Curve_List:
                    new_acurve = acurve.ToNurbsCurve()
                    new_acurve.Domain = rg.Interval(0, 1)
                    Tangent = new_acurve.TangentAt(0.5)  # 指导曲线切向量
                    for bcurve in B_Curve_List:
                        save_curve = bcurve.ToNurbsCurve()
                        new_bcurve = bcurve.ToNurbsCurve()
                        Parallel = Tangent.IsParallelTo(new_bcurve.TangentAt(0.5), 99.0001)
                        if Parallel != 1:
                            new_bcurve.Reverse()
                        new_bcurve.Domain = rg.Interval(0, 1)
                        if rg.NurbsCurve.IsDuplicate(new_acurve, new_bcurve, True, 0.1):
                            result_curves.append(save_curve)
                return result_curves

            def Create_Dim(self, sub_align, Start_Point, End_Point, Dim_Point, style):
                """创建标注"""
                Plane = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))  # 从线得到平面
                dimstyle = self.Find_DimStyle(style)
                ann_type = rg.AnnotationType.Rotated  # 标注类型
                Dimension = rg.LinearDimension.Create(ann_type, dimstyle, Plane, Plane.XAxis, Start_Point, End_Point, Dim_Point, 0)

                True_Value = Dimension.NumericValue  # 真实值
                DisPlay_Value = Dimension.PlainUserText  # 显示值

                Dimension = initialization.HAE_LinearDim(Dimension)  # 调用自定义类

                return Dimension, True_Value, DisPlay_Value

            def Get_Curves_Dim(self, tuple_data):
                Curve, coefficient, style = tuple_data
                new_offset = ghc.OffsetCurve(Curve, coefficient, None, 1)  # 线根据系数偏移

                # 获取线的中点
                Mid_length = new_offset.GetLength() / 2  # 将线的长度除2
                t = new_offset.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                Mid_Point = new_offset.PointAt(t)  # 根据t值求中心点

                Start_Point = Curve.PointAtStart  # 线起点
                End_Point = Curve.PointAtEnd  # 线终点

                Dimension, True_Value, DisPlay_Value = self.Create_Dim(new_offset, Start_Point, End_Point, Mid_Point, style)

                return Dimension, True_Value, DisPlay_Value

            def _run_main(self, tuple_data):
                """运行主方法"""
                curve, coefficient, style = tuple_data
                Dimension, True_Value, DisPlay_Value = [], [], []
                if curve is None:  # 如果curve为空
                    return Dimension, True_Value, DisPlay_Value
                if curve.IsClosed:  # 曲线是闭合的
                    Close_UnifyCurve = UnifyCurve().unify_curve(curve, rg.Plane.WorldXY)[0]
                    Explode_Curves = Close_UnifyCurve.DuplicateSegments()  # 炸开线段
                    match_coefficient = self.match_list(Explode_Curves, [coefficient])[1]
                    match_style = self.match_list(match_coefficient, [style])[1]
                    curve_zip_list = zip(Explode_Curves, match_coefficient, match_style)
                    Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))
                else:
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) == 1:  # 炸开线只有一根的情况
                        curve_zip_list = zip(Explode_Curves, [coefficient], [style])
                        Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))
                    else:
                        control_point = [cp.Location for cp in curve.ToNurbsCurve().Points]
                        control_point.append(control_point[0])
                        New_Curve = rg.Polyline(control_point).ToNurbsCurve()
                        Close_UnifyCurve = UnifyCurve().unify_curve(New_Curve, rg.Plane.WorldXY)[0]
                        Explode_UnifyCurve = Close_UnifyCurve.DuplicateSegments()  # 炸开线段
                        New_Explode_Curves = self.compare_curves(Explode_Curves, Explode_UnifyCurve)
                        match_coefficient = self.match_list(New_Explode_Curves, [coefficient])[1]
                        match_style = self.match_list(match_coefficient, [style])[1]
                        curve_zip_list = zip(New_Explode_Curves, match_coefficient, match_style)
                        Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))

                return Dimension, True_Value, DisPlay_Value

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_curves, match_coefficient, match_style = new_list_data

                curves, coefficient, style = self.match_list(match_curves, match_coefficient, match_style)

                zip_list = zip(curves, coefficient, style)
                Dimension, True_Value, DisPlay_Value = zip(*ghp.run(self._run_main, zip_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Dimension, True_Value, DisPlay_Value])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [
                    map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
                    for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))

                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = zip(*map(self._do_main, zip_list))
                Dimension, True_Value, DisPlay_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                return Dimension, True_Value, DisPlay_Value

            def RunScript(self, Curves, Style, Coefficient):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Dimension, True_Value, DisPlay_Value = (gd[object]() for _ in range(3))

                    re_mes = Message.RE_MES([Curves], ['Curves'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, True_Value, DisPlay_Value = self.temp_by_match_tree(Curves, Coefficient, Style)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dimension, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Line length dimension'


        # 连续标注
        class ContinueDimension(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ContinueDimension", "F33",
                                                                   """ContinueDimension""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("fbb690e2-f44f-4ecf-b988-18e60478b894")

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
                self.SetUpParam(p, "Point_list", "Pts", "Point set")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Baseline", "L", "Base line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension Style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Coefficient", "f", "Coefficient")
                TOL = 0
                p.SetPersistentData(gk.Types.GH_Number(TOL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Head_tail", "H", "Whether start and end dimension are included")
                p.SetPersistentData(gk.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "True_Value", "V", "True Value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJkSURBVEhL7dRdSNNhFMfxkzYca2DbINPShYMWURpJZJlFodCkdBcatAoqqY0iNGItsJdBFDEryFUYtFlEBUokiFYrRiC9XFiK2EVXRa9008Wgujz9zuG/i4Zsu6iLwAPfi8+zZzx/2LM/zczM/NUpRDvQPuSQBcwWJK5UETWjCGpSEdUh8S4V0Qok9qsyxox+IUY1soAZR+KdKqLrSBxVER1F4kcqot1I/Fo1zXxEsmGRiugJEntUROeQ+JSKaC8S31YRbUXi9IE6btSGfOg7kg1BY+2N4YuGhw0PGo4bfmH4kuEpwxKdiPX4OXG/ix12q3zIV8+3cyJxhquWVqi7jnjhbvY2rVJv89bCF/hAe6O6vtYNR/hYZ4u6epkTPs23eg+KKfjt7TVmfsgLy+y64f1EFH7ODRuWq0f6Q/A4hzqa1eFQKzzJsahf7Wutg1/x0N2gunFjFTzKqQ99Yjo5ljzLqU83uLRkrm4YHQlzKnWP1612q/uuBOBhDuxpUHcGPPADjoR96hZPDTzEsZ796vo1S+ABnnrWLSZP+QJHvNI572ZBwawfsqGsxDbocpXGTabCr2K7zZoUWyxF+ptYLeZJcXGx5aXYbDa9E9ttc56KTabZX1yu+fGKcof8Rn9M5i16jMSbVUSXkVjuukxetyg9Regzkg3VsoDRJ0J6GzCbkNyw9SqiQ0g+H1ARbUfipCpj8jkgczL/aFkPkH/yTyQbVsoCJtcB8iAdKP3qyHqACfWifuSUBUyuAzIn6wHTzf9/wASSL6Tfprkm/TYdU+Ux8uSH0WJV7lmL7qDjqn8/RL8Bi34VSvKRl1kAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.Head_tail, self.Dihedral = (None for i in range(2))

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

            def sort_pt(self, set_data):
                # 获取片段集合中所有点和平面
                pts, pl = set_data
                origin_pts = filter(None, pts)
                if len(origin_pts):
                    pts = map(self._trun_object, origin_pts)
                    pl = self._trun_object(pl)
                    # 新建字典
                    dict_pt_data = dict()
                    from_plane = rg.Plane.WorldXY
                    # 获取转换过程
                    xform = rg.Transform.PlaneToPlane(pl, from_plane)
                    # 复制点列表
                    copy_pt = [rg.Point3d(_) for _ in pts]
                    # 将转换过程映射至点集合副本中
                    [_.Transform(xform) for _ in copy_pt]
                    dict_pt_data['X'] = [_.X for _ in copy_pt]
                    dict_pt_data['Y'] = [_.Y for _ in copy_pt]
                    dict_pt_data['Z'] = [_.Z for _ in copy_pt]
                    # 按轴排序，最后结果映射只源点列表中
                    zip_list_sort = zip(dict_pt_data['X'], origin_pts)
                    res_origin_pt = zip(*sorted(zip_list_sort))[1]
                else:
                    res_origin_pt = []
                return res_origin_pt

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def match_list(self, *args):
                """匹配子树"""
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def Offset_Line_Pt(self, Line, coefficient, Ref_Plane):
                """将线根据系数进行偏移，得到偏移之后线的中心点"""
                if Line is None:
                    Message.message2(self, "Baseline is empty")
                    Mid_Point = rg.Point3d(0, 0, 0)
                else:
                    Offset_Line = ghc.OffsetCurve(Line, coefficient, Ref_Plane, 1)
                    # 获取线的中点
                    Mid_length = Offset_Line.GetLength() / 2  # 将线的长度除2
                    t = Offset_Line.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                    Mid_Point = Offset_Line.PointAt(t)  # 根据t值求中心点
                return Mid_Point

            def Create_Dim(self, Plane, Start_Point, End_Point, Dim_Point, dimstyle):
                """创建标注"""
                ann_type = rg.AnnotationType.Rotated  # 标注类型
                Dimension = rg.LinearDimension.Create(ann_type, dimstyle, Plane, Plane.XAxis, Start_Point, End_Point,
                                                      Dim_Point, 0)

                True_Value = Dimension.NumericValue  # 真实值

                Dimension = initialization.HAE_LinearDim(Dimension)  # 调用自定义类
                return Dimension, True_Value

            def _run_main(self, tuple_data):
                """运行主方法"""
                One_Point, Other_Point, Baseline, coefficient, BasePlane, Style = tuple_data
                Dim_Point = self.Offset_Line_Pt(Baseline, coefficient, BasePlane)  # 线偏移
                dimstyle = self.Find_DimStyle(Style)
                Dimension, True_Value = self.Create_Dim(BasePlane, One_Point, Other_Point, Dim_Point, dimstyle)  # 创建标注

                return Dimension, True_Value

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_Points, match_Baseline, match_coefficient, match_style = new_list_data
                Ref_Plane = ghc.Line_Pt(match_Baseline[0], rg.Point3d(0, 0, 0)) if match_Baseline[
                                                                                       0] is not None else rg.Plane.WorldXY  # 根据基线得到参考向量

                Sort_Points = self.sort_pt((match_Points, Ref_Plane))  # 将点根据参考平面进行排序
                if len(Sort_Points) == 0:
                    Dimension, True_Value = [], []
                else:

                    Points_1_List = Sort_Points[1:]  # 去除首尾两端点
                    Points_2_List = Sort_Points[:-1]

                    Points, Baseline, coefficient, BasePlane, Style = self.match_list(Points_1_List, match_Baseline, match_coefficient,
                                                                                      [Ref_Plane], match_style)  # 匹配列表数据

                    zip_list = zip(Points_2_List, Points_1_List, Baseline, coefficient, BasePlane, Style)
                    Dimension, True_Value = zip(*map(self._run_main, zip_list))

                    if self.Head_tail:  # 是否包含首尾标注
                        dimstyle = self.Find_DimStyle(Style[0])
                        Start_Point = Sort_Points[0]  # 起始点
                        End_Point = Sort_Points[-1]  # 结束点
                        DimensionScale = dimstyle.DimensionScale * 3  # 查找标注样式的比例
                        Two_coefficient = coefficient[0] * 2 + DimensionScale if coefficient[0] else 2 + DimensionScale  # 设置二次偏移的系数点
                        vector = ghc.Amplitude(ghc.Vector2Pt(Start_Point, BasePlane[0], False)['vector'], Two_coefficient)
                        Head_tail_Dim_Point = ghc.CurveMiddle(ghc.Move(Baseline[0], vector)['geometry'])
                        Other_Dimension, Other_True_Value = self.Create_Dim(BasePlane[0], Start_Point, End_Point, Head_tail_Dim_Point, dimstyle)
                        Dimension, True_Value = list(Dimension), list(True_Value)
                        Dimension.append(Other_Dimension)
                        True_Value.append(Other_True_Value)
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Dimension, True_Value])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [
                    map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
                    for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))

                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = zip(*map(self._do_main, zip_list))
                Dimension, True_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                return Dimension, True_Value

            def RunScript(self, Point_list, Baseline, Style, Coefficient, Head_tail):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    Dimension, True_Value = (gd[object]() for _ in range(2))

                    self.Head_tail = Head_tail

                    re_mes = Message.RE_MES([Point_list, Baseline], ['Points', 'Baseline'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, True_Value = self.temp_by_match_tree(Point_list, Baseline, Coefficient, Style)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dimension, True_Value
                finally:
                    self.Message = 'Continuous dimension'


        # 弧长标注
        class ArcAnnotation(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ArcAnnotation", "F32", """Arc length dimension""", "Scavenger", "H-Facade")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9701e95d-c56b-44b3-abd5-c2469dbca47d")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Arc()
                self.SetUpParam(p, "Arc", "A", "Arc")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Coefficient", "f", "Coefficient")
                p.SetPersistentData(gk.Types.GH_Number(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension Style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "OverWrite", "W", "OverWrite")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Dimension", "D", "Dimension")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "True_Value", "V", "True Value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Display_Value", "SV", "Display Value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALJSURBVEhLxZRbSFRRFIZnyBSKiCjKnqpRo+yh8lZhmPUigQ9aRNhLGRRZkiJihD5GhI9iUGGmNeM4zuSoGRZCGOFbkFj0UnQhCRod81pzPX//2mdmGhs0aib64ePsfc4+6z97rXW24X/rADHpw3+j08RO1qhZAnWUZJC1pILUhMYJ0U5SRe6SE6SBbCIrSFxKIZnkFCkksotikkuMoWstaSE9IW6RapJHltQ2cpacJyfJBSIm+0LzUYLk5CSkm1KRl52OXGLasgFJScsgz8gIkXQuJzGSwKX60FBGsokEHyAo3J+JtpuVeDfaDN+4BZizK7wuC96MNKHlegUK8reHjV6QfLJA4lpHdpMSIgXuY17Q1FgOBHoB9APzDuBrJzBp1ZGx3JNnXiecnXVI27xeTAKknCyQFPEKkS+XPMPWWsWXH6lAwYmOJVGGNHKPteNYyV4YjUYxkjaP0RGCq/XHVXAtKkiA6RHCOwjfCz8XZLf93EkK68U4PhUxSsnkfc4uE/C9G5iy/XxZAjMN8Peoud9l0eDhmmCfMlNGbl5n7SguypLgr0mBBI2WFBgDXZcA7QGDRgX39SAwaX3idXWUeT7fy/SMtW/1u62Hg1O2Vm26i0VnLaZtatcvhxvbGGeViviL+jPSNiIoxQvlXaXE34uA2zoYWhMj/7i1MDDTNR2cc3gDE5aY4oa1krgqzxSpYoVTo03SaMbu9Xxqlc5aVPMfW3I0V4d04aLaQXCn+ZyenpCBSs0X85C+JD7Jn4vHjssqJREDSC0sTfqS+HSIYNBZH+mUiIE7MQZZBJ23L6rWixiwNQMu8zN9SXyS8362obaUX/0wYqCxt/HtPnwuc0xP/42G9+Sk6z+Pz6n3P8eap3va7zLL0R23auQMcbRV4/nTa9zJoJyaQ9pvWvRPtI5MEaSuX423r27I4Zdw1ZMP5KCaxSWD4Qf7rzA0rZoIlAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dimstyle, self.bbox = None, None
                self.dim = []

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

            def Find_DimStyle(self, dimstyle):
                """获取标注样式"""
                Style = sc.doc.DimStyles.FindName(str(dimstyle))
                if dimstyle is None:
                    # 输入为空时，给默认值
                    Style = sc.doc.DimStyles.FindIndex(0)

                if Style is None:
                    # 若标注样式不存在，根据索引0返回第一个标注样式
                    Message.message2(self, "DimStyle: {} non-existent".format(dimstyle))
                    Style = sc.doc.DimStyles.FindIndex(0)
                return Style

            def match_list(self, *args):
                """匹配子树"""
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def Create_Dim(self, tuple):
                """创建标注"""
                Arc, Coefficient, OverWrite, Style = tuple
                if Arc is not None:
                    dimstyle = self.Find_DimStyle(Style)
                    Length = Arc.Length
                    ArcDim = rg.AngularDimension(Arc, Coefficient)
                    ArcDim.DimensionStyleId = dimstyle.Id
                    if OverWrite is None:
                        ArcDim.RichText = str(round(Length, 2))
                    else:
                        ArcDim.RichText = OverWrite
                    True_Value = Length
                    DisPlay_Value = ArcDim.PlainUserText
                    ArcDim = initialization.HAE_AngularDim(ArcDim)  # 调用自定义类
                else:
                    ArcDim, True_Value, DisPlay_Value = None, None, None
                return ArcDim, True_Value, DisPlay_Value

            def _do_main(self, tuple_data):
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                match_Arc, match_Coefficient, match_OverWrite, match_Style = new_list_data

                Arc, Coefficient, OverWrite, Style = self.match_list(match_Arc, match_Coefficient, match_OverWrite, match_Style)  # 将数据二次匹配列表里面的数据

                zip_list = zip(Arc, Coefficient, OverWrite, Style)
                zip_ungroup_data = ghp.run(self.Create_Dim, zip_list)  # 传入获取主方法中

                Dim, True_Value, DisPlay_Value = zip(*zip_ungroup_data)

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Dim, True_Value, DisPlay_Value])

                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [
                    map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [
                        [None]]
                    for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))

                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = zip(*ghp.run(self._do_main, zip_list))
                Dim, True_Value, DisPlay_Value = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                return Dim, True_Value, DisPlay_Value

            def RunScript(self, Arc, Coefficient, Style, OverWrite):
                try:
                    Dim, True_Value, DisPlay_Value = (gd[object]() for i in range(3))
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    # self.dimstyle = self.Find_DimStyle(str(Style))

                    re_mes = Message.RE_MES([Arc], ['Arc'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dim, True_Value, DisPlay_Value = self.temp_by_match_tree(Arc, Coefficient, OverWrite, Style)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dim, True_Value, DisPlay_Value

                finally:
                    self.Message = 'Arc length dimension'


    else:
        pass
except:
    pass
