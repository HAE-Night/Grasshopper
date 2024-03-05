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

                # 若直线存在
                if sub_align:
                    self.pln = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))
                else:
                    self.pln.Origin = sub_start_pt

                offset_pt = rg.Point3d(self.pln.OriginX, self.pln.OriginY + sub_dis, self.pln.OriginZ)
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
                if s_len >= e_len:
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
                    over_trunk_list, align_trunk_list = self.Branch_Route(Overwrite)[0], self.Branch_Route(Align_Line)[
                        0]
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

                        zip_list = zip(new_sp_trunk_list, new_ep_trunk_list, dis_trunk_list, over_trunk_list,
                                       align_trunk_list, trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.run_mian, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                    iter_ungroup_data)

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
                if sub_align:
                    self.pln = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))
                else:
                    self.pln.Origin = sub_start_pt

                offset_pt = rg.Point3d(self.pln.OriginX + sub_dis, self.pln.OriginY, self.pln.OriginZ)
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
                if s_len >= e_len:
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
                    over_trunk_list, align_trunk_list = self.Branch_Route(Overwrite)[0], self.Branch_Route(Align_Line)[
                        0]
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

                        zip_list = zip(new_sp_trunk_list, new_ep_trunk_list, dis_trunk_list, over_trunk_list,
                                       align_trunk_list, trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.run_mian, zip_list))
                        Dimension, Real_Value, Show_Value = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                    iter_ungroup_data)

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
                        Text_TEN, Cells, Pln = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                       iter_ungroup_data)

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
                                args.Display.DrawText(sub_text, System.Drawing.Color.FromArgb(0, 150, 0),
                                                      sub_text.GetTextTransform(sub_text.DimensionScale,
                                                                                sub_text.DimensionStyle))
                            rec_curve = self.unrendered_rec3d[text_index][sub_index].ToNurbsCurve()
                            args.Display.DrawCurve(rec_curve, System.Drawing.Color.FromArgb(0, 150, 0), 2)
                except:
                    pass


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
                result = self.RunScript(p0, p1, p2, p3)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIvSURBVEhLYxgFgxqw8vLyCoMwlM8gKirKA6SYhYWFeY2NjVkhogwMQkJCfECKCcIjHuQyMjJeYWJiOgCkl8jLy3MA2TtZWVmNgPRhIN4HUgSk04D4LZCpBeKTAnqABs8H0rxA+h4LC0sGkD4I5NsADdwDxB/Y2dkVmZmZlwPFvwPFTUGaSAFdQI1TQAygYbuAFtQB+TuBXFugoUuA7CVA8Z1QNSCLrUFqSQGdQM2XgLgbiO9ycHDIA+lrQHEnoMH7gJZ4AOn/QBwGFDsFxA4gTTiBBwMD++ZwvyOr3FzqoUK6QFwANKCQi4tLEiLEEArEkkDDvYE0KMIDgBgUwSBawodBkmuNu8vylbYO8UA+BuC8s6j6//G6tFVQPskAaJPQk0U1/082p8+FCqEAzsszS34erU5eCOWTAwSuziz9f6o1czKUjwI4r8wq/XWoLBGr7UQCzuuzy/6faEjvhfJRAOe1ueUvDhfGvj9cl3jpeH0qSfhEc8alramB1x8tqP5/rCa1GWomCuC8MqfszeGCuAf7SmNWH65IWn24PIF4XJ28el2c76YH86v+H61LbYWaiQJAcfD7aFXyLCifHMByc27F/6M1KZ1QPgqgOJL1GBjEbg2oBdcXVv4/0Zi+FMonGYAsuL+09v/xxvQuqBACyAAt2JsT9XZzmN9MqBDJwImBQfxcbdr/7QnBPVAhBPjPwMAYCHRBNCTrkwX2AyO5iYHfuIVBSBoqNAoIAQYGAMi83N/s4LrqAAAAAElFTkSuQmCC"
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Working plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "dimension style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text")
                p.SetPersistentData(gk.Types.GH_String('Text'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Leader", "L", "lead")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                result = self.RunScript(p0, p1, p2, p3)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIdSURBVEhLYxgRgBGIvYE4C4gNQAJAYA7EgkBsC8SSIAEgcAViMQiTNMALxNeBuAiITwGxAxAvB2I7IL4NxB1AzAbE/4HYE4hJBiCX7oUwGYKBeCEQTwNiNyDeD8SbgDgKiL8BcSAQkwyQLUgE4ulAPAWIw4AYZBHIN8eAeBEQg4KRLHAGiEFBBLJIEYhnAHEcEPcCcQoQr4Pyq4GYePDv3x6jzctLbYWEeKr4+bkmycgIB5ibq2qKi/MngtgSEgKxqqoSdnJyIt7y8iJeUlKCEYe3Nfr++7lty7/Xy/ygxuAG398sf3Fsb+vfygL/h1WFAfdLc3xeFmZ4fSzL9X1Wku3zCkg/L87yfgMSB/GB9ItDW+v///9/7f/f18t2Qo3BDtwd9L17m2P/F+eGaAG5osTiNfOLNP793Nz488UyPSAfNwC66FxSjMNSKJe6QE9P3rCxIvS/goKUOlSIuiA3zXNjYZbXISiXukCIk1O6vjzkv42Fhj1UiLogJdZxclme7x0ol7qAjZnZqyzP73uQv3k4VIiqgHVKV+LbS0e7/zMzM4NKT6oD05c3Z/5fOa/gPjc3N1nFLl6QmexWd+VY939JSSFQKUl90FYbcaswyxtU9FIfqKiIKnu5Gb0EMiUgItQGXKzJDEwMSVAedUE9g7SMHTN/UwWDmGUng4QJNfFkBlkTYIUq1TqVQfZPF4P0304G6f/UxFMYZP8DAOqPyxw9e5AIAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dim, self.bbox = [], []
                self.Plane, self.DimStyle = None, None

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

            def Complete_data(self, basis_List, Need_List):  # 补全数据
                Last_Data = Need_List[-1]  # 以最后一个值补全数据
                if len(basis_List) > len(Need_List):
                    for _ in range(len(basis_List) - len(Need_List)):
                        Need_List.append(Last_Data)
                return Need_List

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
                Pts, Str = tuple
                if Pts is None:
                    leader = None
                else:
                    leader = rg.Leader.Create(Str, self.Plane, self.DimStyle, Pts)
                return leader

            def temp_Points(self, curves):
                # 解构线上的点
                Points = map(self.Get_curve_pt, curves)
                return Points

            def match_list(self, data1, data2):
                """匹配两个列表的数据"""
                zip_list = [data1, data2]
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

            def temp_Create_Leader(self, tuple):
                # 创建标注样式
                Points_List, Str_List, Path = tuple

                iter_group = self.match_list(Points_List, Str_List)  # 匹配后的数据
                match_point, math_str = iter_group  # 匹配后的点列表和字符
                zip_list = zip(match_point, math_str)

                leader_list = map(self.Create_Leader, zip_list)
                ungroup_data = self.split_tree(leader_list, Path)

                return ungroup_data

            def RunScript(self, curve, Plane, Style, Font):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Leader = gd[object]()

                    factor_bool = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]

                    re_mes = Message.RE_MES([factor_bool], ['Curve terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve, curve_Path = self.Branch_Route(curve)
                        str = self.Branch_Route(Font)[0]
                        pts = map(self.temp_Points, curve)
                        self.DimStyle = self.Find_DimStyle(Style)  # 查找标注样式
                        self.Plane = Plane if Plane else rg.Plane.WorldXY

                        complete_str = self.Complete_data(curve, str)

                        zip_list = zip(pts, complete_str, curve_Path)
                        iter_ungroup_data = map(self.temp_Create_Leader, zip_list)
                        Leader = self.format_tree(iter_ungroup_data)

                    no_rendering_line = self.Branch_Route(Leader)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Leader
                finally:
                    self.Message = 'Lead dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANOSURBVEhL1ZV7SFNRHMdvZm6aJlrQwwg3t7Q0rCTsH/OfHhBEf0QRQURCGpZoPvIxS1vLdI/r5mNLTY18pPMRiWk6pzHQEAl16t18ZFo+Kq1maJbEPZ0zz8hh8wH2Rx/4cXe+v989353nJRAAACYA09uMjX/Be01azniTzEDTMzuwtLZo8+M1fdKbcCAzPlhaW7oLbqt0achgej+W1pbuwsT/3IAqNhkADyytLWgNBnJ4gKbpU9DECcsWAQSxTmzLCc1gchXCTZ5uWLZM/7PkuhdnToN2WQxoz+F9H6ghW2cmqpJoeu4QLjGDtOMcT7FxlacxWX4iBrsAy5bprbhX1xIeALSP7/c0J4WMt90NAfqkMNAhDgejLdmNND16DJcSCUSCVar9niMSG5Zaas3KkthzgxR23JMy5307ccliKLjIfYpYNEWecIps4NN7+mNVVGd+Yk8XLxhQwggwN1mdDXN2QQThkmm3W5zO5EaikYiY7FzFBjc+fGY/3OzugLs0hyq+o9LDRabprwewZAR2aEXTnZc6M2LHqMgrYEzzoB1qu3CagNMjSl7veuIssddGxGAVyzgcRhbbxxGn/7DA4CCWzIAj2vqhNfd5V1gAeFslfgPb26FsJWawy7KsOf5ChmuVxJZzWOrk4UXac4tIRw/zfqgn0EBm2cDE1GBFETIZVsleo6kUMlhH5bYckXSjhxfKo3UgHdxDFc7eLsYXTKzUAPGpI6+BigwEn9+VybG0PLpSvkq3QgP4z7do5dETffIYWD/ui+WlWY0BYtZQe1V/6xr4MlRUg6Wl0SmhgTRqxQZo/jW8wJHBMgF8Z3b5k7xaA0THo/iUMTm6XtpvYMkyujLBqg2+jVX6a+ODwayhshpLljEZQFZ8m8KzYKu6fnFu5FX6EJYsQyn5Tb2ZaFf8OkfTP73+FuhbgT6pABiMAQ1821LDJ6lS/g/4228+vzAAjOH5m3mwTlzeevkC0JLRoIuMmA+JeVBwhPq0aIDOC9pxOlkcaAw4D9AtrJPyAEVGgh5TwHq9NA5MUHmU0WDWUM0eriWVPSWCZr2SvzjKBc26Ev5LqiSxAW7p+VDyGwaqU+oHa4X1veWwXS5Q95qiUqDufypRTw0X8n8Dfq1Qvtb5Hd0AAAAASUVORK5CYII="
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

            def match_tree(self, data_1, data_2, data_3, data_4, data_5, ):
                one_trunk, two_trunk, three_trunk, four_trunk, five_trunk = \
                    zip(*map(self.Branch_Route, [data_1, data_2, data_3, data_4, data_5]))[0]
                if len(four_trunk) == 0 and len(five_trunk) == 0 == 0:
                    Defult_LayerName = str(sc.doc.Layers.FindIndex(0))
                    four_trunk = [[Defult_LayerName]]
                zip_list = [one_trunk, two_trunk, three_trunk, four_trunk, five_trunk]
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
                Vector, Center_Point, Start_Point, End_Point, Coeff_Point, OverWrite = tuble
                # 如果输入的点有空值，直接返回空值
                if Vector is None or Center_Point is None or Start_Point is None \
                        or End_Point is None or Coeff_Point is None:
                    return None, None, None

                Dimstyle = self.dimstyle
                Plane = rg.Plane.WorldXY  # 以世界XY坐标轴作为参考平面
                rg.Plane.Origin
                Plane.Origin = Center_Point
                AngularDim = rg.AngularDimension.Create(Dimstyle, Plane, Vector, Center_Point, Start_Point, End_Point,
                                                        Coeff_Point)
                if OverWrite is not None:
                    AngularDim.RichText = str(OverWrite)  # 标注覆写
                True_Value = math.degrees(AngularDim.NumericValue)  # 角度真实值
                DisPlay_Value = AngularDim.PlainUserText  # 显示值

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
                target_Path, Ref_Vector, CP_trunk_list, new_Sp_Point, new_Ep_Point, Coeff_Point, OverWrite = tuple

                iter_group = self.match_list(Ref_Vector, CP_trunk_list, OverWrite)
                match_ReV, match_CP, match_Over = iter_group

                sub_zip_list = zip(Ref_Vector, match_CP, new_Sp_Point, new_Ep_Point, Coeff_Point, match_Over)
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
                                                                           Coefficient, OverWrite)
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
                        self.dimstyle = self.Find_DimStyle(Style)

                        self.Dihedral = Dihedral  # 反角
                        Coefficient_trunk_list = Coefficient_trunk_list

                        new_list1 = map(self.temp_get_newSPEp, zip(CP_trunk_list, SP_trunk_list, EP_trunk_list))
                        new_Sp_Point, new_Ep_Point = [result[0] for result in new_list1], [result[1] for result in
                                                                                           new_list1]

                        new_list2 = map(self.temp_get_Vector,
                                        zip(CP_trunk_list, SP_trunk_list, EP_trunk_list, Coefficient_trunk_list))
                        Ref_Vector, Coeff_Point = [result[0] for result in new_list2], [result[1] for result in
                                                                                        new_list2]

                        # 此处运行创建角度标注主方法
                        sub_zip_list = zip(target_Path, Ref_Vector, CP_trunk_list, new_Sp_Point, new_Ep_Point,
                                           Coeff_Point, OverWrite_trunk_list)
                        iter_ungroup_data = zip(*ghp.run(self.run_main, sub_zip_list))
                        AngularDim, True_Value, DisPlay_Value = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    no_rendering_line = self.Branch_Route(AngularDim)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return AngularDim, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Angle dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                self.SetUpParam(p, "Picture_Frame", "PF", "Picture frame")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALOSURBVEhL7ZZdSFNhGMefqxZ5kZVJYinVLLRQy1KGhTl3kVaEZhCBRJCVlpDWpG3NraamFn6UIeQXWn6BEk5T0kJsfkBZWua328wuMtz6JKNw79Nz3OlCSJqnmy76wx/e8z/nfX68nPc574FfkkjE26ymolTGOl35SJAQG2WjPbmpNJxfRxLkdRI/1CBjj/z4SJAYu589PV6INJxfhwBHrMYiAkyK+UiQGGvRjDzN4QDr7QmAM9nT1XV5koXICvWxMLpeJ9Rmc3Hu8JNsDhBJ9gN9lVzeYcjCjqbL+MNSgb2GTDToU9DQoFm8ad7bsdv4beoO9ndk4eBgAdJLMWxgrC9KX3OxdMZYgq+yznX36mILBtLP5i/G/enx+b3aE4XjJcqJL5Ol2NaYksbYsyhahV1hUUFxQ2VKTKJlbgJwOQXgEwPg7ai556mMqCvuaLL5wVUEkSjUXplXTKzs/ECZAlsiIry1sPJ4NnhszwQ3h30N3Pckw7J94wUXks1NaegbvOUAX9ouDjBYrsS64FA/NawI52OHlQBikRyW7h7JS1SYm9MXBtTvkvpqwHk/HzssDXg6EyDkP2BB/TsAobvoMPgsIcCfd1GTdK8P1wc54B6UAWsDHTX1jUxJfTB6i/pgIQDXaG3R0eIr4OJFE4LTwM1h36DnNbB6zVBeksr0u0aTRgaeGb6rQjnAZj4SpLaYQ9qJ1gwEJyfpXIDY44H4UtZcp7r5/U059uWqxtrVp1s71QmLdntK3ENjpW764+tivFchV9JHVAqttYpL3V3X8cXjTMRPdKJ9rX03a6kSZJu1eorN1H2etVSi8XkemkxF3LkAq8jinf4bM7kbjDVs5UKhovk6q3HuyIwnS+ZCTpERAYmz0xyg0ZuPBInZ6nXcyUjDHfaE18HwgGQ74C9XYKtP5QEh9oQXAbT0y4Fkfz4SJGbT5+D7ag4gAwD4Ce1sUa8jKyeEAAAAAElFTkSuQmCC"
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP/SURBVEhL5ZVrTFt1GMb/ZoSRGELUeCFqjKKRRLNkkiWzEUNwGuOcynTZMhcvbIlU5tzmaOd0MqDQQgdb1nFpoYVyH72NlTE2RIII6LINgQ0HLW259AIUgSx1bB98fEvPbGWHxZl980l+H85Jz+/p/+17Uvb/yEeMxZx6Y9O+AvZkPF2GB+7eo2jj1+0e1lXMYcGBuf7vMVCuGGkVClWFT7z4XiRjD3Efu/t8wyIFPZL0bkz1A5girMQYMU04cWO0B0M6tbfzgNhUtTZxx0bGnuEevXNSGHuk5Kk1R+3mOhJdJzzEMDEUgv/aQUwGmO2H/Wztwi+5GZ2GDUkH9jMWR6r7AsYlqV6XkOlpkKBP4+cInN1m3Ji/TCIn4T+BhQgt8zNCuAj/SUfhPd+C2oQ3B3cw9jSnDaZl14dtN+dPwDVUjOG2bFxUi9CTL8KvZfkY72zEwuwASSYIvjIXFty9OF8qhyppg0/Ioh7gtIE8z1hkV8Gu3+dcWjivFMM9pMSUQw33cAks7Tm4qKGyAhF6VXKMdZhwfaaPpOOEv9AJ+5l61H2ZDKP2W5Ru3WjktMFkhUW/YjVLMGVXLxaE4rqqxCTdd1tKYO2Q4lKFmMrScEmZh7H2RvyskEIj+gT1+gw012Ti6LOr6edckspXE8RzAyWLsqUFodwq81iVGL1QgHP7tkFFcoNZCtMpGarThX+ms/BYThtMs3CL2ees5JUux8xYOdpyU1Gt3A/diQw0nZajLHnzb6S7bYsiOmWp7nn3XRQM0mn7jkOf9inq6zOgI1qMMhQnvlbEOYM5yKLiruoPYdqh4Zfx4LGoYGnJQbV4O/SmbOgNEjQWf428B59L4rTBlMcJvpjtLYKHNsdFD4fCJ/czNarBhTIRtJLURflJcy60acm+r+hl5bTBNG3f1PDHuPY2OR+3CqZphVslKagqEi3Ov5nmX7ol6UdO+Y+EdUg+c1yj+fMJeRmkEQ0UwiCi+dcdWiw4Uy+B4iXBd5wzmN3s/hcu1x7EDB2ZV8aDZ1gFWyutpCgZOpq/gdDJ9yAr7GEBpw1GGbt6z80+JXzeGkzb1PTtaDt4pKH4l6G3XAxt5uc0/yw0nc2Heuc278e0jZw2mMPRMXGnt75T+JNMaHc058Bn0+Cau+qOZV4q+CFHiMrjaTCZZThXkwXFy/EqTrlsImQro183ffBWUZdMaLOHltGb+3cZzX/yShGMNH8Dyc20moo1AgU9vyKg+XeJkK98PPHk5rePdUuFVltTNnwjgbKZiQrY2/NgyN4Jff5eHIlZtZd75j8nXLri0UTj++uPdeWkWCfaD2O0IQNl7673yR+LpT+ze5twRVRMQu0qgSydRa7l7i0Txv4CN34MAJiCgl0AAAAASUVORK5CYII="
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAU8SURBVEhLrZUNUNNlHMef1JTT67y4yre88izirEjlssTzSkvJ0DjLN9LsBBNIPAWCwrcxZTA3QWPyssEYA2UDBnMwh0EnV4IvQPkCgjrYeJmAMgSkwVTg27M//xzo8qrre/e9/Z/d8/98n9/v+T//P7Ep9Y35S6SvzfVjBlQbCZnjTsiz7JBwyAsuHDJnPDv89zrq+tYys4KL4m3rE3wJWVixd1u3eNbctasImXX2G5/cNLcFEnbqKHEIGcMhzi+zw6erTr5bj3416tIjAGhRnfxdl159oNdyPh6RZOJX6uVrdsWRmYvp1FGViF9xExx/5z0eOyRhZMJH9Gfs8Ig8w6yCrnr6Gf8N5UAhMHASg+Ys4IGaBulQErjRcjVD3AW0o/vqz6iWiRpKArdLRFNcV1LApN2EzO/VCVC6c1M6b8z0DbXxofjxeZd1PKepH1SFbrlEQslE98rIbX0PzQoMdlJTOOPOYeuVXBg1yWir1NFAE7WZuhX9DWWozU0xaUOCVNekEX2w5uNOsYCpnnbhvrlShI4SIZgy1Gu8YgdMmRjqybYH2HxXAdxX4fLRIJzjcTBwv54CbrJuZoK6KnSoPBQM9OUC1jwMdpxgugAUQbPaq8AWMEbrs0oCsxLozaET7AGwUrgoFHotvUY3dQu1nvoGc60vzMBF7lYM3lM+Vr0CQ11KtBQd6iQ53p7huJICa4MU1uZ0pgp0KzFkWz1dUZ0sAqd3+KHmeDxazmpg7aqmcFurbBWYcDkpGj01CRjqdlD9YAGIasWKRfnLPtkkmDQzpKPsCAboRKtRxpRafsAf5XGBuJq9B8YLQvyWFo7zceH4XSxAW1URepouoiaVS2FZgK29I6une1ERGXDT1iJGaa8vWNx3QYSLwiCUcf1hKopBlSQM5lY52vQStNYl47ZRSq+TYSgXoIzOy/FcjmZdFG6VCtHfKAP+oPvA7iMeamDM2MNsMqNEl7e3ajyX9xrK49B8+RgKfLzpyvcz0FvXkka5vSEVhrJYVKaEoEYdidM7N6KTPjXWJhn69akArSR/padC8/HSUBZPSAAhL6l8vIstbZlor09BAwU0VhxlVv54wK2aRLTdkOBOUxru3snEOf52NOVwkLtrMwp+8EMXfVz3ksnzWPQjjT0rCDL1tGVQQBIDaL0ufhI+0rX0fNyUQLFkCeS+66CgZyZHvh8S90X3Yp2dZ7DcYe0jk92vqyLR0ZjmGObA7XRv6ktiINu6Htn5POSpedBI9iBq4qubWaxdMnePHV2XEtF+Q4xWevNIO4Lb3EFbVJUaDnnMDqjyo3Cy8BDkYb6WYEKcWaxdWr+1OX0t8ifgjvwooFGKkqgAZCaGIzebC90pIVI2rP6VRY7SuF+i/Bt7af8dAR26lraoOgF54VugVEQyAUXKKIjme+xnmXbtIpPerMnah05askOYA7fTzTWU8HE83Be5tPe2/ucKg3Fw3IseLNYuseu84AdXxLCYT6DDIKWrS3YIHWnbw3BJ9j3kB76FKu8gtD/FQhq0yfw1IU4s1q7D02a7n/rys4QyfqCxURcNiyENvfQ8PC3MTAPORAci41gY1IV8FJ84CNHCxQ6/fCPlxJ8wbZl6zaeJ5fxAg3FkGD3Rj8Jo/29fS0Q+7X8ehRcmRUD0roeI3v/Xl+wfyUk4YcbSk+tXxp+LCaw3aHmwNAyHdZrSYSwVII8XBFVsCI7Mdgth7/nPGh8zdsrS/C+84sujA+pNpYfpq4GLVG8vi3Cq6+fsnP9N40WTZ3+Y5ebB55Dn3mf/+xsR8icvktiv9W4r2wAAAABJRU5ErkJggg=="
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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

            def match_tree(self, data_1, data_2):
                one_trunk, two_trunk = zip(*map(self.Branch_Route, [data_1, data_2]))[0]
                zip_list = [one_trunk, two_trunk]
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
                plane, text = tuple
                if plane and text:
                    TextEntity = rg.TextEntity.Create(text, plane, self.DimStyle, True, 0, 0)
                    TextEntity.Justification = rg.TextJustification.MiddleCenter  # 设置对齐方式
                else:
                    TextEntity = None

                return TextEntity

            # -------------修改----------------
            def match_list(self, data1, data2):
                """匹配两个列表的数据"""
                zip_list = [data1, data2]
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
                # -------------修改----------------

            def run_main(self, tuple):
                Plane, Text, Path = tuple
                if len(Plane) == 0 or len(Text) == 0:
                    Text_List = []
                else:
                    # -------------修改----------------
                    match_Plane, match_Text = self.match_list(Plane, Text)
                    Text_List = map(self.Creat_TextEntity, zip(match_Plane, match_Text))
                    # -------------修改----------------

                ungroup_data = self.split_tree(Text_List, Path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Plane, Text, Style):
                try:
                    Text_result = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    re_mes = Message.RE_MES([Plane, Text], ['Plane', 'Text'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.DimStyle = self.Find_DimStyle(Style)  # 查找标注样式

                        max_index, iter_group, max_group = self.match_tree(Plane, Text)

                        iter_group.insert(max_index, max_group)  # 将得到的最长的列表插入到匹配后的数据中
                        target_Path = self.Branch_Route(self.Params.Input[max_index].VolatileData)[1]  # 得到最长的目标路径
                        if len(target_Path) == 0: target_Path = [[0]]  # 如果目标路径为0, 给一个默认的路径

                        Plane_trunk_list = iter_group[0]
                        Text_trunk_list = iter_group[1]

                        zip_list = zip(Plane_trunk_list, Text_trunk_list, target_Path)

                        iter_ungroup_data = map(self.run_main, zip_list)
                        Text_result = self.format_tree(iter_ungroup_data)

                    no_rendering_line = self.Branch_Route(Text_result)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Text_result
                finally:
                    self.Message = 'Text'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKeSURBVEhLY6A5kBQTcvVyNZzp62k61dfdmHrY23Sqh7P+bAY7K82mORPTSzaurFBZPz9fYfPSUlVK8fLp+Qpb11WozZmQOo3BxU67qr4iyOX//7v8/z6sDP/3Y33wv/cryMe/NwHplSH///9nm9gam8vgYKNd1dMU7ffv39bgf1+XSf17tJKTYvx6pfq/f/vce5qBFtjb6lTO7k2N+vfvqDs0WqgC/v8/5TKlPb4UbMHMyRnB5yeXpk1gkHLuhOJWBmlHEG5nkHYiFc/gU/a4Mqs6cuqE1HywBdMmpwZfmlGR1gsx0AGEu1jkqztY5HI6GWTsScWz+VRcUSyY3pMY+e/fYU+o78BgAreacxeXqgGUSzIABdHkjoQSiA96kyL+/dvsB5UDgz4uVe8uDmVLKJck8O/WRPZ//3a5T+lMLB61ACsYPhZM7aJRKgKB//9vO/S3xBeALZjeD8oHlFvQxSUv0c0o29nDIjvneFVGXu/UlDiwBVO6E8OAFoRA1YFBLYOwcz4DKykZjamHUeYKsBT4n8Ug+r+HQexzT4THUgYnYHHdWBXm/u/XRut/r5fF/P64xuv3lzVeBwvjao43Zeb/+7LS49/bZfjx740ee7Ijy6cyyPzPARruzsD3fwqD5P9eS4v/YAv62hP8QU4AluOK/36u1v73ebX2x2uz1D7em6P+79NKrZ/Pl2njw//+bdDalR7pNZlR9n820AIbBu7/sxik/nc7WD8CW9BRG4VSDpELWhnE8tsYxF/XMoh+bWcQmNVeGZHNYG+t2bh8Tl7V9ZN9JpdOdpKNr5/oMf74b4P6gZb0wEMliTHPgSGxeF7uRAZpaWGHiECrpTHhdotjwmwpxpHRdrMiYuxnREfZLwzyM18G9RytAAMDAFEHdIgDgZ+iAAAAAElFTkSuQmCC"
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI/SURBVEhL7ZXLaxNRFMa/mYm0Yk2b93umiTW6EdwpFKmiiyKabmwUKtZdWx+NpaIiaGyaZPKw0ZRqN7F1ERSlUqgPEDfJylWLoKsERP8Ck1AqLjrXe8ehuogUNOgmH/zmMpy53zl3ZjgH/0wE4OjSMDQ/YApuYxzO4SScARmOvkbB/Jgv6MVPOZYWpINZeIIJOIMpuPr/FLaf+SQF8bAMz3FEYXYkOM8kS3AfouEOpI6/hfkkdd4DSc4dRwqSXYYzG4bNqr6zBklGuyEBx4yagB4rE4XbpcUaohisNvodss0Ev1UzwaZqJthUGwnuwmtLwDUdg92ixRqii4BebRWs8iTvupoXdh0qYocnj05pka7zkDpr2GvJt3ZKD3bu8WldV8PsHwTsrKh6pLf5rLIgHrmB9iu0Xbu7ZiF279NtDwW4jsQZmEaCvGF8kDcNd3Ntj8bs3nNvY2Pjcdh7U3CrTMLSW358s1D7/LBafT9bj1qllFv9tBQtoojdjgBniECHa/RkLRC4W5QMtvAD4DHUZtPfVpTS/h8H/ynl68I7Ql4SsvasDguEkOdk7ePcNzyFTxzgjSEImKAEqHmKEoUgyOC4iFO0nFeUlR7Nd0NK9ckHQt4Qsr5UH/KarJZy62BzYBqeoQuwjZ7mTBMxOE+l4ToxAnPoLIzX7+n9Jxf7jl6mf5o67RgRmIMrmUvzlfJc4cvyTF0q5VxheWr0hVpNGNAR9FDC/Ct0tTAI+gV2T2Ot9BEdnd1bf0Xd+P8FfAfbe0sf/26VsQAAAABJRU5ErkJggg=="
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
                                                                   "RPP_PolylineAngleDim", "RPP_PolylineAngleDim", """Multi-line Angle dimension""", "Scavenger", "H-Facade")
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPMSURBVEhL3ZV7TNNXFMc7OslEtNakIp2FFNry+BVxdGpAYHVCNAhmPjFWK1HECUETNVsWomYLoKjDLaIGFZ2KjhrkoRUBFUyIiQ+s+2NRY2ZcfCHZhAJDsco9nvP73bKhgvSf/eEnOf2d8z338bu/e+6t7IMmOD46NNMcK2TGx9IzVHy+aWIe22F7vdRtiGzISroK7DTAs5MA3WTlku+2/8Zgh2+yU67zru9Ho1FZnY+PAmP2Sva8csXzltKs2vKN+8l3W33FpmJX67FMMWZnjjofHga1WrmIDzEoviU/Z7QydrYD7hYruBaEFiO5brxn4c8w8u41HvoEJ2nbXZD2gBKkDci0OGErwBl8+4ZlFOt0uvEhISHZ4eHhvmIDjsFgCEXSeShjrH4l9FTAZ8bAdVx6J0EXqnN6u5+WtajVmhQceAEOkoHmz/P9wEli0VaHhYXFTxSEyH/ay7psB9Z0YGq01OIN0i3mUwB1wJ5Vxctkw9XYMZCnBgRXNgbbxY1QjJ3uaNqxgVafaI7YztP/IpfLp9+/uQdu3yi6g+FwSfUc3Lsr5ytzXqEbICkSXvk5C2/iRrn2bls1Van0S0XtIynlGSePf5cNUA+L50aXckkm+zxSm+Vy2vDTVGymGJe9QBAEjZj0gODgEPOoUaoZjNXaf2sqAJRMpCsP7lrVgzXfior41vhNE/R6fST5Q4WqzF1V4DxhAjgH2Rkz6in2/nZtSgNO4GJO22QScIJUT1eAE+gEITSZfNZlWwcvqmHO7EkFYhLRX7RvZozVXNF+qp2g1eoWc33I0HlRKscl4b3hg3vZ9UvR13+hPFLKItIBs0NlWU4Jhl6S6hFytOTux0f2v+oqB8Ewni7AfvjsK0x/wti5h4xVjfT39/fBZQ9+7Dkmk0m8MkqK1k4BqIXCXMsfGH5MWj/8/JSpnS1H4JZj11m5XDEHN82Kp9mCpuZN+oF6BFqa0Wi0yL1HJ79sL7e1PzoM41SK+bzJ26xfndQEUIN3UaOOYpzEgIOswaqiC68PLIQpVDX47VUUX6z6fhpVzsb1XzWLDQYhorlxC7DeUw08Jnw1gUFp3CdGBAQE9110BOutrvnz9z2AN4KZSwMzK2FikXijvqhYCFA8DCvDa1JUpGXJksSxFMfERMVFT476EnU5xezp8Zn09lkrEur4EO9Fgf8Jf1Mn1nmijczVWtrD2ss6+vy2XzvdOdrYS3U/0MmdIHUfAtoA1bxtuUsv78y3OgpzrY6f8q3XduYtvU4+PpvJyC/Mszp+3LH8auIXxjze9f9EJnsNBUjR2nHS7t8AAAAASUVORK5CYII="
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

            def Create_AngularDim(self, Vector, Center_Point, Start_Point, End_Point, Coeff_Point):
                """创建角度标注"""
                # 如果输入的点有空值，直接返回空值
                if Vector is None or Center_Point is None or Start_Point is None \
                        or End_Point is None or Coeff_Point is None:
                    return None, None, None

                Dimstyle = self.dimstyle
                Plane = rg.Plane.WorldXY  # 以世界XY坐标轴作为参考平面
                Plane.Origin = Center_Point
                AngularDim = rg.AngularDimension.Create(Dimstyle, Plane, Vector, Center_Point, Start_Point, End_Point, Coeff_Point)
                True_Value = math.degrees(AngularDim.NumericValue)  # 角度真实值
                DisPlay_Value = AngularDim.PlainUserText  # 显示值

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
                curve_1, curve_2, coefficient = tuple_data
                curve_1_MP = self.Get_SP_EP_MP(curve_1)  # 获取线的中点
                curve_2_MP = self.Get_SP_EP_MP(curve_2)  # 获取线的中点

                Center_Point = self.Get_Curve_PointEnd(curve_1, curve_2)[0]  # 求两根线之间的交点
                New_SP_Point, New_END_Point = self.get_new_SpEp(Center_Point, curve_1_MP, curve_2_MP)  # 得到新的起点和终点

                Ref_Vector, Coeff_Point = self.get_Vector(Center_Point, curve_1_MP, curve_2_MP, coefficient)  # 得到参考向量和系数点

                # 得到角度标注，真实值和显示值
                AngularDim, True_Value, DisPlay_Value = self.Create_AngularDim(Ref_Vector, Center_Point, New_SP_Point, New_END_Point, Coeff_Point)

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
                curve, coefficient = tuple_data
                AngularDim, True_Value, DisPlay_Value = [], [], []
                if curve is None:  # 如果curve为空
                    return AngularDim, True_Value, DisPlay_Value
                if curve.IsClosed:  # 曲线是闭合的
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) != 1:
                        Shift_Explode_Curves = list(Explode_Curves[1:])
                        Shift_Explode_Curves.extend(list(Explode_Curves[:1]))  # 偏移一下曲线列表
                        match_coefficient = self.match_list(Shift_Explode_Curves, [coefficient])[1]
                        curve_zip_list = zip(Explode_Curves, Shift_Explode_Curves, match_coefficient)
                        AngularDim, True_Value, DisPlay_Value = zip(*map(self.Get_Curve_AngularDim, curve_zip_list))  # 得到角度标注
                else:
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) > 1:  # 线数小于1，你求个嘚的角度
                        if len(Explode_Curves) == 2:
                            # 只有两根线的情况
                            curve_zip_list = zip([Explode_Curves[0]], [Explode_Curves[1]], [coefficient])
                            AngularDim, True_Value, DisPlay_Value = zip(*map(self.Get_Curve_AngularDim, curve_zip_list))  # 得到角度标注
                        else:
                            Curves_1_List = Explode_Curves[1:]  # 去除首尾两根线段
                            Curves_2_List = Explode_Curves[:-1]

                            match_coefficient = self.match_list(Curves_1_List, [coefficient])[1]
                            curve_zip_list = zip(Curves_2_List, Curves_1_List, match_coefficient)

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

                match_curves, match_coefficient = new_list_data

                curves, coefficient = self.match_list(match_curves, match_coefficient)

                zip_list = zip(curves, coefficient)
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

                    self.dimstyle = self.Find_DimStyle(Style)
                    self.Dihedral = Dihedral if Dihedral is not None else False
                    self.Retain = Retain if Retain is not None else False
                    re_mes = Message.RE_MES([Curves], ['Curves'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        AngularDim, True_Value, DisPlay_Value = self.temp_by_match_tree(Curves, Coefficient)
                    no_rendering_line = self.Branch_Route(AngularDim)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return AngularDim, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Multi-line Angle dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                                                                   "RPP_PolylineDimension", "RPP_PolylineDimension", """Line length dimension""", "Scavenger", "H-Facade")
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPtSURBVEhLY8AFXFwMpYqyfJxzUt1d8OGCTG+XggxPJwMVCVGoVqKAkIyMcHF+tld5Wb5fXlm+Dx7sl5ca61QnIMAdA9QnAtGOBySHuAnFhNstAzIn66hJx+hpK4QTwhqqkqlA9R0hAZbzi3P9tMAG4QKVRYFdft5mIeW5vlv//9v8//+3tYTx/y3/Kwv89js66hpXFQfNgBqFCbJSXc1rSoMmMTMwBH54tvj/v39b1v/7vj6ZIP63dfGHpwv/A41wry4NacrN9LCHmIgGasuClwIp0wVT0u/++7f94/+7M/khMvjB/f3zOYCOeT+tK/EmkKtZXRo8HyKDBIpyfVKAKSLf3Ei5+P//bf//fV2dDZUiCgB9kvv/5/r/ygqisWUF/iV56d6BUCkGhsQQG9H68pAVQKbm/s21P4GuufL/PwMjRJY48P/MTNZ//zY/XD0//xWQq15bHrIISLOAJcuLAvrDg63ckqMd5v//v+v//8+rHcASJIJ/39ZGgHxvZ6VZlp/lnVqU65fEUJjp5VhbETwJKG/y+PqM//9+bVgLUU4e+Pd308W9G2p+AJmaDZWhCxla6yKKeXh4NDtqw08DU8Pv/+8WykGUkgeAceH8///O/2H+FhMSYp1CwYJ6OvIZvz+u+v/v27p6sACF4N+vjXvOH+oEJVtHEN9l7qR0YMRuew4UISlicYF/r5eZ/P+/+39ksNUTEF+wosBvDzDl/Pr3dYUpWAWF4N/nlUX/f2787+FsMIWhszHaFiimf3Br/R9gMjsHUUI++PdkoTAwLj8vnpZ5R0ZGKJChviKkqCDLJ9baXBWYwYDFz5c1yVC1ZIF/39b0//2y9r+ICE9ydUnQRAYLCxlOYKZYDZRTmjMx9T7Q9nfEFhHo4P/z5QrAIubPhNaY06ZGKtFVJUHVYIn8DE/PmtLgdiDT9fMLYCH3cx0oX5AM/n1ft/TD00X/mZiYIuvKQ6ZHRtoj6oeK4sBZjo4GVqXZ3ptAufHHm5X4y3U08O/dMj1QKVBTHLDDw80orbwoELUsi4+3V2ioCFsMZGqf3t/2H5gj90FkiAPAEmDn/ctTQWk/uKEybKaFhQUnRAYJlOT6lGSneSa6OejUgSP857qw//9nshLC/94u8wCl+4wEpyVRoTaFpfm+kVAjUYGxsTFrXUXIKiBTc+Xc3GsgTf8+rXpHCP//v+P/qb1tn4H6fIBhPxNI486wedmerkW5vtN5uNj7mqrDj/S1xO4hhLu7k3aoK0ls8HI3WlhZGAQuHvACF0e9WCCVYWakMjE01KYqKMCqGoRDwNiyBoaDAy1rQTg83K5OUV58gqysqA3EBBhgYAAAz4lKfMW9pwQAAAAASUVORK5CYII="
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

            def Create_Dim(self, sub_align, Start_Point, End_Point, Dim_Point):
                """创建标注"""
                Plane = ghc.Line_Pt(sub_align, rg.Point3d(0, 0, 0))  # 从线得到平面

                ann_type = rg.AnnotationType.Rotated  # 标注类型
                Dimension = rg.LinearDimension.Create(ann_type, self.dimstyle, Plane, Plane.XAxis, Start_Point, End_Point, Dim_Point, 0)

                True_Value = Dimension.NumericValue  # 真实值
                DisPlay_Value = Dimension.PlainUserText  # 显示值

                return Dimension, True_Value, DisPlay_Value

            def Get_Curves_Dim(self, tuple_data):
                Curve, coefficient = tuple_data
                new_offset = ghc.OffsetCurve(Curve, coefficient, None, 1)  # 线根据系数偏移

                # 获取线的中点
                Mid_length = new_offset.GetLength() / 2  # 将线的长度除2
                t = new_offset.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                Mid_Point = new_offset.PointAt(t)  # 根据t值求中心点

                Start_Point = Curve.PointAtStart  # 线起点
                End_Point = Curve.PointAtEnd  # 线终点

                Dimension, True_Value, DisPlay_Value = self.Create_Dim(new_offset, Start_Point, End_Point, Mid_Point)

                return Dimension, True_Value, DisPlay_Value

            def _run_main(self, tuple_data):
                """运行主方法"""
                curve, coefficient = tuple_data
                Dimension, True_Value, DisPlay_Value = [], [], []
                if curve is None:  # 如果curve为空
                    return Dimension, True_Value, DisPlay_Value
                if curve.IsClosed:  # 曲线是闭合的
                    Close_UnifyCurve = UnifyCurve().unify_curve(curve, rg.Plane.WorldXY)[0]
                    Explode_Curves = Close_UnifyCurve.DuplicateSegments()  # 炸开线段
                    match_coefficient = self.match_list(Explode_Curves, [coefficient])[1]
                    curve_zip_list = zip(Explode_Curves, match_coefficient)
                    Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))
                else:
                    Explode_Curves = curve.DuplicateSegments()  # 炸开线段
                    if len(Explode_Curves) == 1:  # 炸开线只有一根的情况
                        curve_zip_list = zip(Explode_Curves, [coefficient])
                        Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))
                    else:
                        control_point = [cp.Location for cp in curve.ToNurbsCurve().Points]
                        control_point.append(control_point[0])
                        New_Curve = rg.Polyline(control_point).ToNurbsCurve()
                        Close_UnifyCurve = UnifyCurve().unify_curve(New_Curve, rg.Plane.WorldXY)[0]
                        Explode_UnifyCurve = Close_UnifyCurve.DuplicateSegments()  # 炸开线段
                        New_Explode_Curves = self.compare_curves(Explode_Curves, Explode_UnifyCurve)
                        match_coefficient = self.match_list(New_Explode_Curves, [coefficient])[1]
                        curve_zip_list = zip(New_Explode_Curves, match_coefficient)
                        Dimension, True_Value, DisPlay_Value = zip(*map(self.Get_Curves_Dim, curve_zip_list))

                return Dimension, True_Value, DisPlay_Value

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_curves, match_coefficient = new_list_data

                curves, coefficient = self.match_list(match_curves, match_coefficient)

                zip_list = zip(curves, coefficient)
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

                    self.dimstyle = self.Find_DimStyle(Style)

                    re_mes = Message.RE_MES([Curves], ['Curves'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, True_Value, DisPlay_Value = self.temp_by_match_tree(Curves, Coefficient)

                    no_rendering_line = self.Branch_Route(Dimension)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dimension, True_Value, DisPlay_Value
                finally:
                    self.Message = 'Line length dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALnSURBVEhL7ZNfSFNRGMCv1eiPBdoM/8w/IWm0pswkRdtopmi1sJRlOtucK53KMGhFgVazpKmprIZajSCsfKkQQuyPFYlZ1z8ZBNVNpYceeqke0rCX4vR959zdNvKhh6AXf/Djft/ZOd85u/c73AIL/FMWgRHiE1kMysEgmjFWgTjuYwm4lIUSOH+Z+AwAFw+BYTTjOAX4BPQv0A8qWUgxgJ0slFgN9oEraeYHbjAK+jaIAcdB/w14MJmFFAt4k4USa8AXINYLIBh8DuIJkCgQC8poxsB/qGIhZT94g4USuB7rYL0AsNAw6NsZT/KMhRKDYCILKcXgNRZK4Hqsww6mUkaXt7vM/NkT+8YiI0Jmncf3jrtbrHydY88E5s1O46jbVca7YY4iKnTmUNX2V+5mC+9uO8AX7kqbViZGf3a3H+TbG00wp4zH9biuyWkcc50s4TnD7jQXIcOEkPtEp1US8vMOxGOEzN0iui2Qk0cg/v6U5GYlkZkPVyHmwQnysLeOVFpyIH4JDoIwD9bTOnTdPcKlqOKqvB6b4Gkpn4xVyOdaz5ROebtqBNepkumYKPn3zjbrO/z9isf2Zm1s2Lf6IwXvvR3VgveSXTAVaT6qk+K+er124fL5CgHn4Xqs09FqnfS0WAT6mkTw3eE7x95HokH8yP5dhF22kYUUE9jDQgnsQvzIf3QRXpoR0Ne/kSBOxHGu1rbDXmzQEH2O+iLmIngPulkoEQriQVfQzEf+zs212brkH0UFGQ3iEN5q7AZ6c63GrZaB/tOzh2v0TZgDstSU+IF18eGfjEZNvDiG4MmxnfE2/6bSnF0/MtRKHHb9BXEoAXwN4ol8hItPZDl0zpfe6w6izVifKY5xMplMDY8pEC9qAEEhwTK8pbR/y0t13Y1OE7GVbWvDfD7S0xM26PNSdWJKOVqbf7fLU02KCzPPiUPzU2PNrXjQ1/DWbNDge/5rbOaskts9xx7r8zZpxaEF/isc9wsmoAFASCWSkAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.Head_tail, self.dimstyle, self.Dihedral, self.bbox = (None for i in range(4))

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
                Offset_Line = ghc.OffsetCurve(Line, coefficient, Ref_Plane, 1)
                # 获取线的中点
                Mid_length = Offset_Line.GetLength() / 2  # 将线的长度除2
                t = Offset_Line.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                Mid_Point = Offset_Line.PointAt(t)  # 根据t值求中心点

                return Mid_Point

            def Create_Dim(self, Plane, Start_Point, End_Point, Dim_Point):
                """创建标注"""
                ann_type = rg.AnnotationType.Rotated  # 标注类型
                Dimension = rg.LinearDimension.Create(ann_type, self.dimstyle, Plane, Plane.XAxis, Start_Point, End_Point,
                                                      Dim_Point, 0)

                True_Value = Dimension.NumericValue  # 真实值

                return Dimension, True_Value

            def _run_main(self, tuple_data):
                """运行主方法"""
                One_Point, Other_Point, Baseline, coefficient, BasePlane = tuple_data
                Dim_Point = self.Offset_Line_Pt(Baseline, coefficient, BasePlane)  # 线偏移
                Dimension, True_Value = self.Create_Dim(BasePlane, One_Point, Other_Point, Dim_Point)  # 创建标注
                return Dimension, True_Value

            def _do_main(self, tuple_data):
                """匹配方法"""
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                match_Points, match_Baseline, match_coefficient = new_list_data
                Ref_Plane = ghc.Line_Pt(match_Baseline[0], rg.Point3d(0, 0, 0)) if match_Baseline[
                                                                                       0] is not None else rg.Plane.WorldXY  # 根据基线得到参考向量

                Sort_Points = self.sort_pt((match_Points, Ref_Plane))  # 将点根据参考平面进行排序
                if len(Sort_Points) == 0:
                    Dimension, True_Value = [], []
                else:

                    Points_1_List = Sort_Points[1:]  # 去除首尾两端点
                    Points_2_List = Sort_Points[:-1]

                    Points, Baseline, coefficient, BasePlane = self.match_list(Points_1_List, match_Baseline, match_coefficient,
                                                                               [Ref_Plane])  # 匹配列表数据

                    zip_list = zip(Points_2_List, Points_1_List, Baseline, coefficient, BasePlane)
                    Dimension, True_Value = zip(*map(self._run_main, zip_list))

                    if self.Head_tail:  # 是否包含首尾标注
                        Start_Point = Sort_Points[0]  # 起始点
                        End_Point = Sort_Points[-1]  # 结束点
                        Two_coefficient = coefficient[0] * 2 if coefficient[0] else 2
                        Head_tail_Dim_Point = self.Offset_Line_Pt(Baseline[0], Two_coefficient, BasePlane[0])  # 线偏移
                        Other_Dimension, Other_True_Value = self.Create_Dim(BasePlane[0], Start_Point, End_Point,
                                                                            Head_tail_Dim_Point)
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

                    self.dimstyle = self.Find_DimStyle(Style)

                    re_mes = Message.RE_MES([Point_list, Baseline], ['Points', 'Baseline'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dimension, True_Value = self.temp_by_match_tree(Point_list, Baseline, Coefficient)

                    no_rendering_line = self.Branch_Route(Dimension)[0]
                    self.dim = filter(None, list(chain(*no_rendering_line)))
                    self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                    for _ in self.dim:
                        if _:
                            self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dimension, True_Value
                finally:
                    self.Message = 'Continuous dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Style", "S", "Dimension Style")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALqSURBVEhLzdV/TIxxHAfwU13nRBcSsVo/SES2EJU2FWvsqK7S2FrRJub6Zf2QfmjNzao127UoU8qOSiOUEkWls8ZKbJa0Fv1T6Y+M5jaWj/fnjoRG7PnDe3tt3x/3PPd8v8/3+31E/0NOg7+hKGzWwy44Dk3gDIJlGWyHJ6CBQ2APgiQSagxFUTAoDEV9rMEbuC0EfMEOZhQjMAYZJEARcGZDBFyCaiiELMiAfOD2KkgES5g2LsAX8MWLwQH2Ao/gDuSCI3yLBOaDVF8TiaxACXchjht+zn5IgT3AU8Q5Bg1gw5WFMjOfBKVcU16s7G+uzdB1NKnoXl2mTlMS25cYH1BiLpW642c8eh75ZRDDD0mDs8BTchIuAscpM1nR0v/8DBHdh3p6N3iBBrrVNNJbTKS7hrYmet1bRFkpwfxASyEGymABTIbfgQmEQh03zJFI/CtL48aJWmn8jYYK86N6QgI9VNbWskB0exkbG2/z9nA+kpYYdKtLm4c/aqMr5UfHzMzEa9FftsTKYpTvMzVzQQs8v65VpTEfiB5SU23mZ88NK5LQ9suwp2RrQd6BAaJ2ulmRPIa6Kv7wzreGru/hm/DGEqXG737ET9TWkE0yqSm/7JnEVp0TMUikpRJ1dCvqvFAmMwtugIW9/aLQ4b5zND5aSe5uDif0vTPPpvbGbOpsOUUmJka8UCbDS7OSC6kJAfX89IW5kQOo/m5apo2zo7XSZZVt+NfqZPhAywNJbUXSMH2qox1+63hDCRZePalg9/RB7sTIiyLCKvHT9wgUOfB8rx7oLqCejnxCmU9UwcJrl3ehfRde0Nir82RpMY//VLCYwlWwqSyJGyJqpDCFh1rfI2D4dAxKUsrVfCyUF0QPoW6u7xEoy4H3wppn2hzdx/c15Onu9Lf74I/hlVTl5mr3mCZuU/P1dBKL9WeLYPHdF+JFCvnG6riD/s2q9LBOiUQi2OeSYxQV7qPYsnnlS5RjgT8u/xiR6AsyOQOkKw3ikwAAAABJRU5ErkJggg=="
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
                Arc, Coefficient, OverWrite = tuple
                if Arc is not None:
                    Length = Arc.Length
                    ArcDim = rg.AngularDimension(Arc, Coefficient)
                    ArcDim.DimensionStyleId = self.dimstyle.Id
                    if OverWrite is None:
                        ArcDim.RichText = str(round(Length, 2))
                    else:
                        ArcDim.RichText = OverWrite
                    True_Value = Length
                    DisPlay_Value = ArcDim.PlainUserText
                else:
                    ArcDim, True_Value, DisPlay_Value = None, None, None
                return ArcDim, True_Value, DisPlay_Value

            def _do_main(self, tuple_data):
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                match_Arc, match_Coefficient, match_OverWrite = new_list_data

                Arc, Coefficient, OverWrite = self.match_list(match_Arc, match_Coefficient, match_OverWrite)  # 将数据二次匹配列表里面的数据

                zip_list = zip(Arc, Coefficient, OverWrite)
                zip_ungroup_data = ghp.run(self.Create_Dim, zip_list)  # 传入获取主方法中

                dim, True_Value, DisPlay_Value = zip(*zip_ungroup_data)

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [dim, True_Value, DisPlay_Value])

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
                    self.dimstyle = self.Find_DimStyle(str(Style))

                    re_mes = Message.RE_MES([Arc], ['Arc'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Dim, True_Value, DisPlay_Value = self.temp_by_match_tree(Arc, Coefficient, OverWrite)
                        no_rendering_line = self.Branch_Route(Dim)[0]
                        self.dim = filter(None, list(chain(*no_rendering_line)))
                        self.bbox = rg.BoundingBox.Empty  # 覆写zoom方法
                        for _ in self.dim:
                            if _:
                                self.bbox.Union(_.GetBoundingBox(True))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Dim, True_Value, DisPlay_Value

                finally:
                    self.Message = 'Arc length dimension'

            def DrawViewportWires(self, args):
                try:
                    for sub_dim in self.dim:
                        args.Display.DrawAnnotation(sub_dim, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


    else:
        pass
except:
    pass
