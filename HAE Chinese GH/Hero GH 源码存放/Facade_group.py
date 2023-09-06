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
                                                                   "RPP-曲面关键点", "RPP_SurfaceKeyPoints", """获取曲面板关键点，角点、中心点、线中心点""", "Scavenger", "Facade")
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
                self.SetUpParam(p, "Surface", "S", "待获取关键点的曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Center", "C", "是否需要中心点")
                bool_center = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_center))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Corner", "Co", "是否需要角点")
                bool_corner = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_corner))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Line_Center", "LC", "是否需要线中心点")
                bool_line_center = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_line_center))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Center_Pt", "CP", "曲面板的中心点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Corner_Pt", "COP", "曲面板的角点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line_Center_Pt", "LCP", "曲面板的线中心点")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJPSURBVEhLY6AL+BcXof3P2+/YVzuXBQJsbH5AIazYqn9zqtvzfxs0JhzIwiYPwu4SEkH/vHx3/nNw3/bEOUAYKMbA8NDFpfq/vdP/R6ZW/0U5OP4DhbBiw/Zt/y2u/v+v0bIPqzwIu4qJ/geZ9dPS7v82K1s3oBgDQ6KCgn6BjOy/QDHx54yMjL1AIaxY0j1pmlbTrhNS7qkzscmDMB8ra3+GlPSXeEmpj85SUhAfAIEsEINccAzMoxw8BeKPQMwF5gGBIhCDLDgF5lEGWIH4ORCDLOABCYDAqAXIYGAskABialnACMSgVPQBiDlBAgyeWx8Hm28/+1+hePZpsAAOEPEzS9vrf+EC22/J4VAhDBC99oGk6ZLjH7WmH/xmWL9LCixov/TeOvMz//8bLXt3y96+ngUsiAU4nQlZY/s/7b/+Yb9voaGhbFBhFOAx74Kv1UGgWdv//zfvOecKFlSKqHaSDq74L2jgchIsgAMYzrDz1VricFmzx6oNyAUFBQbQj88XkPDMeCfmFP9FytQZnpNBXqFWHDABMSwORnMyVjBMLZABYpAFJ8A8ysEzIAalIm4wb4uDg/lCQ5P/ZbKK54FcaVzYftYWA6/Xf0p15pw0wSYPwjZyYkrdWtpvWpVUP6cpKfEDxRgY3rq4zv3v7PH/ponlf1ZmZpBPsGKj9s3/7Z7//6/eRqBOdvX4/9/W+f9+G3sXoBgDwxo9I/e9OvqX8+TkTwPrZFB5hBXLBhVf1Ow981k2uOwyNnkQlubgOL1OU/vGck2d8z0mJrIA06wTFc2Sb4EAAAAASUVORK5CYII="
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
                    self.Message = '曲面关键点'


        # 物件粗略范围
        class SmallestRegion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-物件粗略范围", "RPP_SmallestRegion", """以中心物件为中心，寻找一组物件中粗略最小范围""", "Scavenger", "Facade")
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
                self.SetUpParam(p, "Main_Item", "M", "中心物件")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Order_Item", "O", "查找范围物件")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "范围物件的数量")
                count = 6
                p.SetPersistentData(gk.Types.GH_Integer(count))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Order_Item", "R", "取得的范围物件")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Order_Index", "i", "取得物件在原列表中的下标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Distance", "D", "取得物件的粗略距离")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQ0SURBVEhLvZUJTBxlFMenHm002CZFQwPYaLnm+Oae2dnd2UNYVERKCrI2ttjiSjZq08SW1DY1BtMjqUmNJlVbaixYYgrLvQ3UQpXWVCpIPJJSxWirtMQaCPbYIgXc5zfDGEE0FDD+kped+f/f997M7Mz7iP+NgoKChHVrn9peHCjakZOd/TKWFk44s2P16lVJD/t8b7jd7mctiSCCgYBS9HThheeCxeB/Ih8URYUUll1h2bdMMBhc4nHpPyqybNZw6HqAkGX5ToddveBx66CpKiCOB44XQBRFn7VuMhyOz3B04tAMYTKPPeJbpyoyJCUlNVNk2i+CIH5rGviki6ZIINNSgWVZXFwClmFeMM2prMEBVjxvCJNx2m17REEwPMKmSK/zPG8eEwxDlXMsAoamcAMEEs8CLwn7TXMqi3H04ujDEWsIk1FXxBVJkgRer3eX2+k4yzBMv2mwDPUSbzRIeQA4Xy5Ih3uAf6e70TT/RuL6nXsSinZOa25rHEhX9zbnUKnJEfzYQRJFoCjqVdNECD1u3AEikwEpWgTVjQDbGo2ItUMrzQQLf2looRgebefDv/fklIXvtmRiY0t0kdAUGWTD491MQmw6mZLSnpaaus/4f82ErOTkRYIg0FgglaT4+7n9Z3ej2mu/CicApLora80kC1Q1VMMcGeqwTolSKL1NPHqjRToNwB76qdKSZ4bZ0Uqh0NBF6RMAvubKBksmljWOlcc33DxuHAMQC8RwJCSfAaAPfr9L3lx2r5l0q9Cl4eVs9cA56VMApml4+6bqvrt6C4NN3zxZ3BHNzb2Haho+KHfh4u/+8Ka1ZPaQ296PRVUDXyQ0jMO5wIat4MsAcKVDVOJfXNowWonK++qs1LlDb6peGlNxOe9qhvftqO6B31QdvhKVP9+yBdbv/LBFo4tPqmrJd4IMXzIclHmzqh7sjOZY9tzxtV2KFVtGPqDrh69uCWyJryTJjyuWJ3Q8urdtM98JwNVff81KnT225mur+OaxfqkDAB3qO020Q4xlEUQ3LEGVP7fJRpPGyIFQyH+75fwz+POOcTgcHiUxDtmP3siTj42GxFO4cM11QAd6S6y0KXgJ4g7mcH+N8Q0I4ZHPtSODlGVNJz832+NyaMBxXA/fOHZexIuYysunyN3HkZXyrzAVF99Tv8YXE775zPpMmz0vL2+j3+9fZtkT+PNXBj1OO/CuzG5UG+lCFZc+tKwZce5rjeeqBstQYclWlaPGH/J6QXd5z2dlFdxnJui6zmRmZPQ6dTcIHHrF0NRt9dOm5UzQibFrWETjqUzizcYNuttr1iLsmnLCpTtBlBTA45Y1xTmAhyZpFKepVGPDAsWmHTMNh6ae9OIdjUPcW6YwDxiK/Mi4CyPwAJ14zE6nqui6/a9Neh6wLCkjhgIRb1q4Qakl/7fQdFoRxzFnNE2L+wNK5J0lyms/VAAAAABJRU5ErkJggg=="
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
                    self.Message = '粗略最小范围'


        # 沉头螺钉
        class CounterBore(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-沉头孔", "RPP_CounterBore", """输入规格自动生成沉头螺钉（包含M4、M5、M6、M8、M10、M12、M16、M20）""", "Scavenger", "Facade")
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
                self.SetUpParam(p, "Code", "C", "螺丝编号")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Deep1", "D1", "深度1")
                DEEP_LENGTH_1 = 5
                p.SetPersistentData(gk.Types.GH_Number(DEEP_LENGTH_1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Deep2", "D2", "深度2")
                DEEP_LENGTH_2 = 10
                p.SetPersistentData(gk.Types.GH_Number(DEEP_LENGTH_2))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Alum_Material", "AL", "铝料螺钉")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Iron_Material", "FE", "铁料螺钉")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGQSURBVEhL7dVLK0RhHMfxmbFh61bEwm0oCcmlRhLjMmnIrTAoZmHFhpUsZGVhZ+EFsLCRW7wNL8DCba0UQojv75yZKZc5Mw+y4VefzvM/c+Z5njPPmfO4fjO5yP8heUhFLFm4wT0e8fINd3jGKmJJwTJ0wSaCGDI0gBFcQYM04kM06gNqrco8G7hGvVXFyTp0J5/OIE7cOIS+16ATibKDW+jW25OwC/3uSXWuaEaniC5cMlphlGOsoDyBfujJy4FRzjFjNx1TiicUWpVBzjBnNx1Thf8BHPPHB5i1m46pxJcGuMC03XSMFxqgwKoMcoJLHCWgf7xeFWUwSghb0FvyAPvYi7Sj53TcxhrSETclmEKFVZklG2+2x/dJwyS0bWpfHoMPWrRidKIXYY/Ho7tSuwODUMeqtVZa7GHUoA8tkdqViVE1SABNWICfDjWYOupCiHqco56sMHSd0o2A2+1e5KjOl9CGeegz690fjMyuDjr6qCd0HkXQAmrWfvSgGhlQNEttOtoBtUE1Q5PmvMv7CqrUfBXPGH/jAAAAAElFTkSuQmCC"
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

                    re_mes = Message.RE_MES([Code], ['Code'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.deep1 = Deep1
                        self.deep2 = Deep2
                        if Code in self.al_specifications.keys():
                            order_sp_al = self.al_specifications[Code]
                            order_sp_fe = self.fe_specifications[Code]

                            Alum_Material = self.counter_bore(order_sp_al)
                            Iron_Material = self.counter_bore(order_sp_fe)
                        else:
                            Message.message1(self, '未包含此螺丝规格！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Alum_Material, Iron_Material
                finally:
                    self.Message = '沉头螺丝（孔）'

    else:
        pass
except:
    pass
