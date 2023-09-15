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
import scriptcontext as sc
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from itertools import chain
import initialization
import Geometry_group
import copy

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

            def closest_object(self, tuple_data):
                main_object, other_object, origin_path = tuple_data
                new_object = [other_object[:] for _ in range(len(main_object))]
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
                        sort_object_list = [new_object[obj_index][_] for _ in sort_index_list]
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
                    re_mes = Message.RE_MES([Main_Item], ['Main_Item'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.count = Count

                        main_trunk_list, main_path_list = self.Branch_Route(Main_Item)
                        order_trunk_list = self.Branch_Route(Order_Item)[0]
                        iter_ungroup_data = zip(*ghp.run(self.closest_object, zip(main_trunk_list, order_trunk_list, main_path_list)))
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

    else:
        pass
except:
    pass
