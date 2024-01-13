# -*- ecoding: utf-8 -*-
# @ModuleName: Vector_group
# @Author: invincible
# @Time: 2022/7/8 11:10
# coding=utf-8

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import initialization
from itertools import chain
from Grasshopper.Kernel.Data import GH_Path

Result = initialization.Result
Message = initialization.message()
TreeFun = initialization.TreeOperation()
try:
    if Result is True:
        # 点序排序
        class PointsSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PointsSort", "Q13", """Point sequence permutation，sort the dot matrix automaticly by reference point""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b852c643-79d1-48fc-9a5a-2c674bb342fe")

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
                self.SetUpParam(p, "Ref_Point", "P", "Reference point，default is the original world coordinates（0，0，0）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Point(rg.Point3d(0, 0, 0)))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Ref_Curve", "V", "Reference vector；When data sets have different types of matrices，initial direction of the point order can be unified")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Points", "Pts", "point order")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Result", "R", "successful sorting point order")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOsSURBVEhLzVVJbJVVFL7/OXf4+96jIJCGoQwCWoYWSSGk2PJeKVMRO1AItUEjoqBYwlQNilUWGCFxIQkbgkqI7tzgTllIAokGCERiSyAlwUTTNSEsgI3X79z/f/QRMClpF37Jeeee77/33OEMT40CxnI1t0NPTMxRBi3Sh+zurOfWeEBZNS+lRxUzuSUeMPuyXm+O71CN2ZHyjyHmenuK2+Or/Kq7CLkUZL07H+y2uI9b3R/c4q7xK+46+H7oa7zOXYG+wE1uwLyd8WZX1ouOqvXX8OkS1wnKdVvs7Uc5b3uyiexPdU+RE10iH5QITm/ewQayyR7cZGPs4XNq4joFz+a1lLcHOW++4II5Cn0YcoRXuK8gx7jRnoR8xwV7Gvp7Xo0br7Lf8lp7kpaan8zrZf+EG2zLeKrVPXAZJZ5Hjom8yvXJyc1bcF6t96f8sFEBeew9gRrIc2E0TuXNljKPG3iap/cE7qmoUHW0wp6LXjJfwtJC0Wzq1O3xXQSxX5WpKYGr0b3ikFfa2yqjJgunJqMOxqqmMP4v8HJ72R3MebO1zGNyo3BUby7YTxDE7qynStoS5hVsv/sU87ZnvBrPa4QbFniJ/sa+jwxY7x6qMapKOHqR3tAd8X2c9paK1fTAvUBdus0N0svmZ5hjhBsuHE3HKTNqcWoXUQnJJsNHMKkuRQxZB9kMmSPESBBiVILaqIJuIn29bnae5uoH4HqTT6XIqQJ+QzBTZHmxPkUFe7b4bDyLO1DRg9RgzsHMQWI4/ysUGnpSqIW96E1LjRRbh6wJiGrNcalEFNBgMTtoJr1pdmLBgRwW2B8CJ8nQiyC/hyBP08tBrUQdJM5lE5F3Ex2VR7/ImgBusrdCdmzFwpyqD+Qkndeb4pAxtFB/JhTN1z2mC2m62v6NbJNa6NYbMAcJ8mgDkZ3YYApdlzUB/DxvRBO7gWw6DXOosCaoRppGnRhRQgRIoRX7fzM32NCDSp2Hg2aiM+mcEUHjKX7Tr6GaZRN5KtyGqrTEYFkyZQhP/CvRLOriZeYEEnVBSklCyhPOTYyACoT6DKr8AS8xPppEN8FtSD6lQGrtxXvfowZ7HmZ5IK2qQqGFNs55+7tQiEG3Rt/RLe4+jlMb5g1hBmQ+5Mk6QZD/DEFGu0WQJTskEnN0Kzb4EFdusL8KRXXmR/sx5iEdkWXbw7zhACc7oDvjh/hPuARzXMICldyMFP4cIzkdHkPX8RrXhz51FtaEwD0DxMnT2sD/FUr9C+6U9SlB3IOYAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = False

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

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
                if len(point_data):
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
                else:
                    return point_data

            def RunScript(self, Ref_Point, Ref_Curve, Points):
                try:
                    Result = gd[object]()
                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        # "------------------------------------------"
                        LenRef_Points = len(self.Branch_Route(self.Params.Input[0].VolatileData)[0])
                        if LenRef_Points == len(self.Branch_Route(Points)[0]):
                            self.factor = True
                            Re_Point = filter(None, self.Branch_Route(self.Params.Input[0].VolatileData)[0][
                                self.RunCount - 1])
                            self.refer = Re_Point[0].Value if len(Re_Point) else rg.Point3d(0, 0, 0)
                        else:
                            self.refer = Ref_Point
                        if Ref_Curve is None:
                            self.vector = None
                        else:
                            Len_RefVector = len(self.Branch_Route(self.Params.Input[1].VolatileData)[0])
                            if LenRef_Points != Len_RefVector:
                                Message.message2(self, 'P. V data mismatch !')
                            self.vector = Ref_Curve if type(Ref_Curve) is rg.Vector3d else Ref_Curve.TangentAtStart
                        # "------------------------------------------"

                        leaf_points = [list(_) for _ in Points.Branches]
                        Point_Path = self.Branch_Route(Points)[1]
                        leaf_points = map(lambda x: filter(None, x), leaf_points)
                        if len(leaf_points) != 0:
                            res = map(self.close_point, leaf_points)
                            # "------------------------------------------"
                            if self.factor:
                                res_Point = res[self.RunCount - 1]
                                res_Point_Path = Point_Path[self.RunCount - 1]
                                if self.vector is None:
                                    Result.AddRange(res_Point, GH_Path(tuple(res_Point_Path)))
                                else:
                                    Result.AddRange(self.re_built_sort(res_Point), GH_Path(tuple(res_Point_Path)))
                            else:
                                Result = ght.list_to_tree(res) if self.vector is None else ght.list_to_tree(
                                    map(self.re_built_sort, res))
                            # "------------------------------------------"
                            return Result
                finally:
                    self.Message = 'point order'


        # 点序排序（分组排序）
        class PointOrderGroupingSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PointOrderSort", "Q11", """sort point order，Sort by X-Y-Z axis groups""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9b7d7417-b3aa-4580-bb4c-1c3193c78eeb")

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
                self.SetUpParam(p, "PTS", "P", "Sequence of points")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Axis")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('X'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance for grouping")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(50))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Result", "R", "Sorted result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANCSURBVEhL7VVLSFRRGD7P67zMwmaS0KFMcdDSpphozFeaUYalYi/t5aNErXxUq8JFUBAUtiqCaFW0qaRNu1zVrnUQ0jppEQS1KBe377/3nNEZbRMtWvTBx5z5vjv/+c893znD/uNvQ4DSH/4ZanmZfMCL+A2M1/iSQT47IdL6g6jVc6xADBjVYhevUi95pXqBccqXcqHZZlnvLOgLYVefC7kioV5Dtd2WykbH1Zcirp6MuLIlz4VW7lusWKb1Nz2O342FXblDf4EW9a2liIgRPRhy9TA4kSmy1jfZdnUw4OpxTIBCqitAnu20WR0Jul5jFzNe0reyUSHrnO/6PB7ERLxCvYJG79wD3yAfqc6AV4BvlE8h2dWFxBb9TvejsT6svFK+gRbwrUVwkIqlUegej/LrGFP3DphnPslvAptBKq5B8hQYw75MsnwxhnGh8YgZ0DvrBw+AabAe7AVpMy1Pgi3gbvC40Szpex1IDVANqkWNLEONKBFXscAe8z0bDutGp4MYZScMqxBFYkpsRYpWiWGj5UCxlGxwftAmq2NBlxfLO8YhcF4qH6sebCbeNQrNQYv5Fsy4vKvPhFyHAoANZ4ViyFiL4Ov4tB7FBg9hsxBHWas/GYsQl3vzvHTpUfinQy7e8FHjMVGj3nsRRrwpZbxcPjHWEuSzdtUe8LqgB3mZeG4cQlgk1UeKoZ5A1lsRYb0kijExTgnTI1gBGqFaxslBgPWKajXDS/htfCvwxQyqeELNiKSeZUF22GiLkKxDxNUURg2+kA0b01xQHC1zsdTL/e0yjWJ6FqSEnAJPmzFplhS9brAL7ANpIy3pWVoVeRRZ0lrBFbEatK+HVka0aENvnfikg0ewPmcRNoATfgvjRjJWhIiJa3KP81m2OPMsKi4bmSB5uXhG8VW9QXsdhH0L1eNymnRKIaUNzordJ1UboojbkuilgbEy32LVlDDvsqMLDRNBsydViJSez8QUlx6dC+NlIeUVQQy9CfZ7EyR8i0XlTv3VOwcU0yaHPHtd00V4n86GNzmaREzpulgOvl5Oy315C1jmT/zp3DSyRQMiPCu26bfYgQ6jWTg4vVd4Qj7EHh0y2m+xCSz1h/88GPsFpM/CDb7qytQAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.axis = None
                self.Tol = None

            def find_collinear_pts(self, points):
                copy_points = points[:]
                new_tree_list = []
                while len(copy_points) > 0:
                    single_pts = [_ for _ in copy_points if abs(eval("copy_points[0].{} - _.{}".format(self.axis, self.axis))) <= self.Tol]
                    new_tree_list.append(single_pts)
                    for _ in single_pts:
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
                    re_mes = Message.RE_MES([PTS], ['PTS'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.axis = Axis
                        self.Tol = Tolerance
                        if self.axis not in ["X", "Y", "Z"]:
                            Message.message1(self, "Please input the correct axis！")
                        sort_by_axis = self.find_collinear_pts(PTS)
                        result_point_sort = self.handing_sort_re(sort_by_axis)
                        return result_point_sort
                finally:
                    self.Message = "sort point（Grouping sort）"


        # 删除重复的点
        class CullPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CullPoints", "Q1", """Delete duplicate points in the point list""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("bbfb844f-0f92-43e6-be07-6a26d8de96b7")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Points", "P", "Point list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Output Format", "O", "Mode of output（0：Only input deleted data，1：Group duplicate data）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Reuslt_Pt", "R", "Result list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index_Pt", "I", "Subscript group of overlapping points")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALpSURBVEhLxVVLbExRGL7nNe9hYlSrHp1pqSn1atIOaUu6aiJFaMQrDerVUqysbMTKQmJnJRE2VmyRNJogIRIWSDRBLCwEDSEioqnr+8+5dzpze+fOdOVLvvTMf77/+8/5zzm31v9EAmwww6pQC9aYYWUIluWjvFV+wjhjQoFI8ZwY583iFcZzTCgArJ7fUoMxW52O2yjyFqHFZsYXSdYknqjhuK2GYjbGjxCLmykfsDpxUx2A+QkkHDN/+Uo5jqk6oyhBjGXFQ62DueZRFMnwMcxFjGQaEVYvrquBqDE/AjHxOIjV8RXiJTTzjVQjDKP7WkPGrn4YPIwiWX4PmpSREqQ1IndGbHUG5hAUEohUZAhFmsVzKPX22VJ+V+vIsFhLsVPwwEKxv0ukdZFmjfyO7r03iUirRCGsbIzV8tvqEH5T3706WgzIW8QzeC4x1tMIswY+WjD0JlPsIEht9JvX7YR5TryAV9pYzkSMZcQDOixfEzpQMvLGtTna2CJew4PeRCASuG6PC7fDa+ale9tWyTfIXWQsKiPFl4uneidk4GdMdHbK1+j3MpuXr5HAG/isTvocpkvMiXb1C9plJmU2SLGLsj8y6dtzl5iTe6NTbKG45mRVibkw34XbMhKwepf0MHGz2AJ2w8mugCS7gJWXN6e+F/+mx4VWyf0oUsOuOi5lEOPn5I4y5u7VJZYrsg9F5rErjpsHSX5Wboc5PfXiZCIZIo4D/cZXy4/64L23yy2yG0XS7LLj6kBZg7KvzLeISOadod9Q5sFG3qa+6F367QRaKmJF2XntraGsVr5Ovit8pouT8H9BdIf+QNVrxBrrebv6qndbXITGKCzyagIf7G5HW0ADtv++ZPtkvjk0hbmtRlKCDhh9LxQpaiPm2oxkJpr4WvlBF0G7RE/YRqzfTPmiU2xUP2khejF59QMxamMgcqJDTYhebb7HhALRIzaF/oqu0CTGXSZUGRvAATOsCtvALWbowrL+AVSqihre6oZOAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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

            def __init__(self):
                self.tol, self.format_put = None, None

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

            def remove_duplicate_points(self, tuple_data):  # 删除重复的点
                points, origin_pt_list, origin_path = tuple_data
                if points:
                    new_points = []
                    index_groups = []  # 点分组后的下标
                    for i, p in enumerate(points):
                        flag = False
                        for j, np in enumerate(new_points):
                            if np:
                                if p.DistanceTo(np) <= self.tol:  # 根据公差判断点是否重复
                                    index_groups[j].append(i)
                                    flag = True
                                    break
                        if not flag:
                            new_points.append(p)  # 添加唯一点
                            index_groups.append([i])

                    # 判断依据，0只输出每组唯一一个点；1输出删除点和保留点
                    if self.format_put == 1:
                        index_groups = index_groups
                    elif self.format_put == 0:
                        index_groups = [_[0] for _ in index_groups]
                    else:
                        index_groups = index_groups
                        self.message2("Please input the correct data type！！")
                    # 判断需要的点列表
                    if type(index_groups[0]) is list:
                        new_ref_points = map(lambda x: [origin_pt_list[_] for _ in x], index_groups)
                    else:
                        new_ref_points = [origin_pt_list[_] for _ in index_groups]
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [new_ref_points, index_groups])
                    Rhino.RhinoApp.Wait()
                else:
                    new_ref_points, index_groups = [], []
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [new_ref_points, index_groups])
                return ungroup_data

            def RunScript(self, Points, Tolerance, Output_Format):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    List_Output_Format = [0, 1]
                    self.format_put = Output_Format
                    self.tol = Tolerance
                    Reuslt_Pt, Index_Pt = (gd[object]() for _ in range(2))

                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        pt_trunk, pt_trunk_path = self.Branch_Route(Points)
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_pts = self.Branch_Route(structure_tree)[0]
                        origin_pts = map(lambda x: filter(None, x), origin_pts)
                        gh_origin_pts = map(lambda x: map(self._trun_object, x), origin_pts)
                        zip_list = zip(gh_origin_pts, origin_pts, pt_trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.remove_duplicate_points, zip_list))
                        Reuslt_Pt, Index_Pt = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                      iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Reuslt_Pt, Index_Pt
                finally:
                    self.Message = 'Remove duplicate points'


        # 按照参照平面排序
        class PtsSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PtsSortByXYZ", "Q12", """Sort point order，sorted according to the given reference plane，default is world XY""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4d413cd7-9c52-47a6-9af6-92502286f023")

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
                self.SetUpParam(p, "Pts", "P", "set of point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Axis（x，y，z）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('X'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "Reference plane")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Sort_Pts", "P", "set of point after sort")
                self.Params.Output.Add(p)

            def sort_pt(self, set_data):
                # 获取片段集合中所有点和平面
                origin_pts, pl = set_data
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
                    zip_list_sort = zip(dict_pt_data[self.axis], origin_pts)
                    res_origin_pt = zip(*sorted(zip_list_sort))[1]
                else:
                    res_origin_pt = []
                return res_origin_pt

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Sort Point'
                # 初始化输出端数据内容
                Sort_Pt = gd[object]()
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    # 确定不变全局参数
                    self.axis = str(p1[0][0]).upper()
                    self.j_bool_f1 = self.parameter_judgment(p0)[0]
                    re_mes = Message.RE_MES([self.j_bool_f1], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 多进程方法
                        def temp(tuple_data):
                            # 解包元组元素
                            origin_pt_list, origin_pl_list, origin_path = tuple_data
                            # 若平面有多个，重新赋值
                            o_pl_len = len(origin_pl_list)
                            if o_pl_len == 1:
                                origin_pt_list = [origin_pt_list]
                            else:
                                origin_pt_list = [origin_pt_list[:] for _ in range(o_pl_len)]
                            # 每个单元切片进行主方法排序
                            sub_zip_list = zip(origin_pt_list, origin_pl_list)
                            res_pt_list = map(self.sort_pt, sub_zip_list)
                            # 每个单元切片是否有数据输出
                            if res_pt_list:
                                ungroup_data = self.split_tree(res_pt_list, origin_path)
                            else:
                                ungroup_data = self.split_tree([[]], origin_path)
                            return ungroup_data

                        # 数据匹配
                        pt_trunk, pt_path_trunk = self.Branch_Route(p0)
                        pl_trunk, pl_path_trunk = self.Branch_Route(p2)
                        pt_len, pl_len = len(pt_trunk), len(pl_trunk)
                        if pt_len > pl_len:
                            new_pt_trunk = pt_trunk
                            new_pl_trunk = pl_trunk + [pl_trunk[-1]] * (pt_len - pl_len)
                            path_trunk = pt_path_trunk
                        elif pt_len < pl_len:
                            new_pt_trunk = pt_trunk + [pt_trunk[-1]] * (pl_len - pt_len)
                            new_pl_trunk = pl_trunk
                            path_trunk = pl_path_trunk
                        else:
                            new_pt_trunk = pt_trunk
                            new_pl_trunk = pl_trunk
                            path_trunk = pt_path_trunk
                        zip_list = zip(new_pt_trunk, new_pl_trunk, path_trunk)
                        # 获得结果树列表
                        iter_ungroup_data = ghp.run(temp, zip_list)
                        Sort_Pt = self.format_tree(iter_ungroup_data)
                    # 将结果添加进输出端
                DA.SetDataTree(0, Sort_Pt)


            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKrSURBVEhLrZVLaBNBGMcHd2d2ZyZRsQcPCoKoiIpUPXjxIHrz5KEBg0LM7mRjk9YXiiBqrY/4rqFFRHoRj6IUqkItBS8Fbx706lk96UFQRCT+Z/NV8mhNAvuDYXf+3+z3n9l5sQXEUGozG1i+iqoJMsw8N1TPeEnXeFF/dvP+Hookg2P0Pn4cyQuqxk/gGcoZCjFm5Fo+JEe90NtASu9wo7fyY0g+jOSnUzBQ4xRiwqgRcTFd40aNkbQ4uRUrWahXU60dYeQAH9IzPFITLOhLkwxzWRFnYGpUlaRFQXweI//KcswnqTvw0fXYIFT3SGoDyftdI9+5oXzPjZ8luTswghs0grsktQHzKuZv2i3ISbSfJbk78MGt+gjkbZKawS9B7BMfVG/cSL6A2W9WlGso2hkY3CGDmyQ1wQO9DbHXVGWuUc+dUB2gamfsv48NAlkhqQlxNL0R+yeLdjmUPBZKFr9zF4U7g8Zj9TmQ10hqJsMcFjHFjjAdF/seMU7RzqBX92ODgrxKUrLAYJxGMEpSsuAXTdAkXyYpWTCCB9YAh+ElkpIFBg9jg0BdIKkZTCgP1A67ckQ5vckP/HUUWQKsgsZG2P6PGg3cvNztFvWpeLVYyuk+JJ/DIpjlg/qPG8jJWF8KNJ7CqfoLG+Y81avirJ0DZXiot/Oi+iHOpWpOoPfHHxAikAexEL7JTrsYjSr8JI5tFPTmMYyeChzjeE4h9iU+zo18xUosRZ8wmxQd+O6E3l6S/g96HaKnP4U1spdQiGLvi7iO5I0bCUYw/4g2b3lJ9YsI12432IlzI/UhvoSsSXzjtSQHIi+24A6Zh8k0L6s5x8grFOqCDHoXySeinvxla3KLl/fW87I+ZO8BXvQP93TQLYCe7cRjWb3Wwgj0DBP/Si/nUDIw9heQCbZf5May/wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

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

            # def RunScript(self, Pts, Axis, CP):
            #     try:
            #         Sort_P = gd[object]()
            #
            #         "----------------------------"
            #         # 添加列表判空操作，如有空值就删掉，如有空树枝就返回
            #         temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
            #         length_list = [len(filter(None, _)) for _ in temp_geo_list]
            #         Abool_factor = any(length_list)
            #
            #         re_mes = Message.RE_MES([Abool_factor], ['Pts'])
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             structure_tree = self.Params.Input[0].VolatileData
            #             origin_pts = filter(None, TreeFun.Branch_Route(structure_tree)[0][self.RunCount - 1])
            #
            #             "----------------------------"
            #             gh_origin_pts = map(TreeFun._trun_object, origin_pts)
            #             if len(origin_pts) <= 1:
            #                 Sort_P = origin_pts
            #             else:
            #                 Axis = Axis.upper()
            #                 dict_pt_data = dict()
            #                 from_plane = rg.Plane.WorldXY
            #                 to_plane = CP
            #                 xform = rg.Transform.PlaneToPlane(to_plane, from_plane)
            #                 copy_pt = [rg.Point3d(_) for _ in gh_origin_pts]
            #                 [_.Transform(xform) for _ in copy_pt]
            #                 dict_pt_data['X'] = [_.X for _ in copy_pt]
            #                 dict_pt_data['Y'] = [_.Y for _ in copy_pt]
            #                 dict_pt_data['Z'] = [_.Z for _ in copy_pt]
            #                 zip_list_sort = zip(dict_pt_data[Axis], origin_pts)
            #                 Sort_P = zip(*sorted(zip_list_sort))[1]
            #
            #         return Sort_P
            #     finally:
            #         self.Message = 'Sort Point'


        # 点依次排序
        class SortPt(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SortPtOrder", "Q5", """Sort by initial point""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("599bb86f-b653-44de-b1a9-591ed5808e1f")

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
                self.SetUpParam(p, "Pts", "P", "A list of points to be arranged")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "first", "f", "Specify start element,default is the first one")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pt_Result", "Pi", "Sorted points")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "The sorted subscript")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJMSURBVEhLrZXPaxNBFMdfsjObndm0VVtssUG0IP5AVFDBk14FRShUWkpVSDabhNjE1qvai968KIIV1IsK+g+Igoqi4KVQ/IXVqhfxHygIxYPrd2aHYNvNmqz9wIe8eW+zk32ZnaFEFNxeGiJhRqsL80WZV+UC8+W87We3mfSq0EcpusjGRMBPuwE/mw1YRV4wtf9iK7wO5+ANNipu8zomKMvFVM76htwmmIgD8AH8CK/AAahhfvagXbK3IKzCH3CNysciqmIDPhg8DB/Bd/A87IFxXIbvofpuBD5xlhf3+Lj7kw0688RpBtkKdHS9Ne7Dp2G4DF5wd+HmqqeB7m1N7jWldnkB74Th3+Spg3tyxj7jBqwoP9FE5zpTaRcbqrZO6dESumlfesCao3rXv/+sOPopl97JAnbMnjSZBp1wFnbpUULQ5mn1fnB0A10pmnSD1/BQGCaDV+RLfXM1iSfU6lqCWgm1MExGej8bZyNigZfEQ+GJnEk3OAdvhmFi1EoaDsOVHIXPwzARu+FnaOlRBGpPeQszetQ+01BtKU1RM6uVtEOP2kP9qC9wux7F8Bg27WEMo/BVGMZzFV4Kw7Z4Br0wjGco1Zt+QhMtHod+tsc6Yg8iegNdnWvKFKVZQdxSpxX2pA90UvSbSiQZL7MZx+Z3GxukNSxaaE/ZXa93VOUk3sS8M2IqkWAXHtPXqetL8jed6Og2pSYcJwtPcJfX9BN8dXxno6lEc0r2saKYxRP/4gV5jQKc2K3A63IP+Wtb2/RwWGXqmZgzmegPX552tJxMRjEAAAAASUVORK5CYII="
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

            def RunScript(self, Pts, first):
                try:
                    Origin_RPt, Index = gd[object](), gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)

                    re_mes = Message.RE_MES([Abool_factor], ['Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_pts = self.Branch_Route(structure_tree)[0][self.RunCount - 1]
                        gh_origin_pts = list(map(TreeFun._trun_object, origin_pts))

                        "----------------------------"
                        if len(gh_origin_pts) == 0:
                            # 如果有空分支直接return空列表
                            return [], []

                        first = first if first else 0
                        first = len(filter(None, Pts)) + first if first < 0 else first

                        if first > len(filter(None, Pts)):  # 判断first是否越界！
                            Message.message2(self, "Index out of bounds!")

                        else:
                            Pt_Result, Index = [], [first]

                            None_indexList = []

                            def ptsort(pts, tag_ind):
                                if len(pts) == 0:  # 如果输入的是空列表直接return
                                    return [], []
                                else:
                                    pt_list = []
                                    for _ in range(len(pts)):
                                        if not pts[_]:
                                            pt_list.append((0, _))
                                        else:
                                            if _ not in Index:
                                                dis = rg.Point3d.DistanceTo(pts[tag_ind], pts[_])
                                                pt_list.append((dis, _))

                                    pt_list.sort()
                                    Index.append(pt_list[0][1])
                                    if len(Index) == len(pts):
                                        for j in Index:
                                            Pt_Result.append(pts[j])
                                        return Index, pt_list
                                    else:
                                        return ptsort(pts, Index[-1])

                            # 判断列表中是否包含了空的数据
                            if None in gh_origin_pts:
                                Origin_RPt = []
                                for index, value in enumerate(gh_origin_pts):
                                    if value is None:
                                        None_indexList.append(index)
                                gh_origin_pts = filter(None, gh_origin_pts)
                                cut_origin_pts = filter(None, origin_pts)
                                ptsort(gh_origin_pts, first)

                                new_index = []
                                if len(cut_origin_pts) == len(Index):
                                    Origin_RPt = [cut_origin_pts[_] for _ in Index]
                                    for _psort in Origin_RPt:
                                        Y_index = origin_pts.index(_psort)  # 排完序之后获取到在原列表中的下标
                                        new_index.append(Y_index)
                                        del origin_pts[Y_index]
                                new_index.extend(None_indexList)
                                for _i in range(len(None_indexList)):  # 有几个空值就返回多少个
                                    Origin_RPt.append(None)
                                Index = new_index
                            else:
                                ptsort(gh_origin_pts, first)
                                Origin_RPt = [origin_pts[_] for _ in Index]
                        "----------------------------"

                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Origin_RPt, Index
                finally:
                    self.Message = 'sort point successively'


        # XYZ轴顺序排序
        class SortPtGroup(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SortPtGroup", "Q14", """Sort the input points according to the coordinate system and output subscripts""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("40c698a6-1657-4619-a587-a75b8ed2614d")

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
                self.SetUpParam(p, "Pts", "Pl", "Enter a list of points")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "P", "Reference plane")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "XYZ", "XYZ", "Sort by axis")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('x,y,z'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Sort_P", "Pr", "Sorted points")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "i", "The sequence number of the point in the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPESURBVEhLtZZ/TFNXFMfvtO+9dhbkVwlBkCW2/kLsHL9azWSJIyFGJTFgNBoxYYqDNSuCGsCkoqmuKigsYrrISBSlbaQFCwJWQZNVE3+Ly0x0if/otsRNmPgLE3s9573bapVWzdwn+ead872vPX333vNuSSj+JiRySBC+YunHZ5jna0YEwfWPXD6XWR8HSsi4f3ne+EAuX/0rIfwQz1tHOC6VDf93oAD3VBC+hhC/dMdjhSJpWCbLEgfDcI+QT0fhh6DwM8wOC06NSwoJKXSYeBaK5PY1xc8/1fQlSwlMZbKP5zei4KkP+QiJYEMh0YPaMJjTbcnQefffST+xax/mhJrGzXabvdlXrDStc/sK0ZNQg7KfwPTCU0ySrNAECqg7qvekXm+kU1xVo+nWdVzOgEk2+VjlI/XV3XSys9KM9wCxoLugPJ8gfAMFEkU3DIECCXZDjupExVCcrewQLNIn6EUfWVsS3WFwx7Qb/PN9HlSDwTDHLX+oVMZhHA4tyCaFQEOeikVj0QxySOE7yOj6Yem8ywcvJJcs3g7pT5IbFgPoOkgmZm+is9cp9Gd+3KzvbRAbSuPaclH72wGatLNoFNL96IUBO/1PkLigczosiVn9e70ZPZZGQqk4lSS102TMutlMU4/X3kVTZSutTeivohMrFrphuEm8aWxw7v8CzRczQOOs/i7tWiOd3lNLNfZqaRdNcpQbUy6ZaaLDeA93B3p8W/EMuOhARzFPt1q57JMNNfq++gLMAbzvBqhMzBjKlqLp8Z3lz+JtZVeS7OUKybUXKCLb129WthbPk4wA2SBxF83oNC1Lv3aAznJve2Hw+QSwsHDQ+hScq1Ms8FozI35eoyEt+VHMDktgmyY7K/OTf9lKk05vucMlRO0Fqx/919F2mZv1gwfp5907v2fWOwkUwL0f6TGu5BbNxk6+CVI6KB0vjjFSjm28oRmso3DtYFYwOQNNs6h/5SVeFZDAxvkdpM0d6YvPPFV/+4tuS9dM9o6Kai3Jj+0t98QeXpuJeRDabvMm3WUr1brNu5mFYAF/o00A4ZevwkTtqiqeeameTvVso2pnzRT0wvJZ+ybPtMF6CldsGD9YoFUKiQcUKK6yl6pVTsMfsW2lZ1JaiuTMDoBnCgslYo6W5Mb1brgYY/u2kFkIFsBGM4F60AjCsiSCOAqD1sEPFIiGE7F6IFR3M9JA2KVv7Zj3Ac6FpQ+gCEvHBN/t8GPILdBZkPcDpXvO8xVwDQk+Hh6VC0ALP1B5ZRyXBn8aLBD/P8C5vuu+TJb5EotAN0UFAg5rAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.h_sort = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Pts, CP, XYZ):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Sort_P, Index = (gd[object]() for _ in range(2))
                    self.h_sort = [_.upper() for _ in XYZ.split(',')]
                    re_mes = Message.RE_MES([Pts], ['Pts'])

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()

                    if len(re_mes) > 0:
                        Sort_P, Index = [], []
                    else:
                        dict_pt_data = dict()

                        from_plane = rg.Plane.WorldXY
                        "----------------------------"
                        to_plane = CP if CP else rg.Plane.WorldXY
                        xform = rg.Transform.PlaneToPlane(to_plane, from_plane)

                        # 判断输入是否包含空值，如有直接返回空值
                        copy_pt = [rg.Point3d(_) if _ else _ for _ in Pts]
                        [_.Transform(xform) if _ else _ for _ in copy_pt]
                        dict_pt_data['X'] = [_.X if _ else _ for _ in copy_pt]
                        dict_pt_data['Y'] = [_.Y if _ else _ for _ in copy_pt]
                        dict_pt_data['Z'] = [_.Z if _ else _ for _ in copy_pt]
                        "----------------------------"

                        total_list = []
                        for _ in self.h_sort:
                            total_list.append(dict_pt_data[_])
                        zip_list = list(zip(total_list[0], total_list[1], total_list[2]))
                        w_sort_pts = []
                        for index in range(len(zip_list)):
                            w_sort_pts.append(list(zip_list[index]) + [index])
                        Index = [_[-1] for _ in sorted(w_sort_pts)]
                        Sort_P = [Pts[_] for _ in Index]

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Sort_P, Index
                finally:
                    self.Message = '-'.join(self.h_sort)


        # 指定点是否共面
        class FitPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FitPlane", "Q2", """Determines whether the specified point is coplanar""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("77574345-7551-4edf-9a62-6aa7461f03f2")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "Pi", "Whether a set of points is coplanar or not")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Determine whether it is a coplanar point in the tolerance range")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Plane", "PL", "Coplanar plane within tolerance")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Coplanar or not")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJ4SURBVEhLzZXfa9NQFMdPknvz46aurg5EmK7aKUOU6qbdhhsFER/24IMy3Zxjtkm6dTrmD1B0DhXEIYj4IIKvPuofqd97e0vTNk068MEPfMn5ngROcu85N/RfwkMRWHVxU9vhsQLvHau5C9oOxHruX+ev/AvadtPMjzqBM6ldNyzKVd2Ge0pbyQQ0bc3at6nIqjLWOgedj3mpMmRYIYqH4gviTOahPTJpxajwA3PcfAS/0qN70BJ0FwqgLYhBBpRJA5JfkArbzy3qUPIEyrfCbGpQif6QwQKvSWuFkVY6RpUYC8QL2sgf1ZkQ6n8uDo/8i2zXm0W4Ck3KAjz012ibcuqBQfwiyyhaH6jijetMMnbk3eK74iHCO1ByNyTx44Qwr7DffIlf0pkMRswtvPOUdl3w0DuQX6ptB4dkI7SXKx3jMv/G5lRr9qFauUFCGfS9XcvJllUO8nhTzLBILXMKAm1n01m1B3XvIwUjBX2nCx6JaTsQ+9rKApxvuquYBbnMqWxAag/wNldpBwuQzTY02gqzeQCVWmGMZbJQ2tWuF1kgeQ9Y6D/jdbGuLZknzZc00d8RLHQXscnvte1lcAG5UU7NOaMtGWXrM5th17TtsIydac8Elo3VxZvYjERQ+qDFSF6iOG+JWZF/QxVFMxgl65M772YeL21kF5Qo8I/TU/JaqRRkgSnrq7PQWYUs6lDBfixeY7KHnE51Fg192LWP42KfHDrNKmyOxjAnnbwctj1oUIclch+Sp6r8mo4cCjHp36lg7sTycoNlwWx4TZT5ZvYkJtIgrroRV53pRxXAj13bw9HIjeH/8ZPWjxzTmX8Mukm9vbwS0V8tu1oLnoBJZQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            def _fit_plane(self, pts_list):
                Rhino.RhinoApp.Wait()
                if len(pts_list) == 1:
                    return [ghc.XYPlane(pts_list[0])], [False]
                else:
                    bool_res, plane_res = rg.Plane.FitPlaneToPoints(pts_list)
                    if bool_res == rg.PlaneFitResult.Success:
                        return [plane_res], [rg.Point3d.ArePointsCoplanar(pts_list, self.tol)]
                    else:
                        return [None], [False]

            def RunScript(self, Pts, Tolerance):
                try:
                    pts_trunk_list = self.Branch_Route(Pts)[0]
                    if not pts_trunk_list:
                        Message.message2(self, "The point set is empty!")
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        Plane, Result = (gd[object]() for _ in range(2))
                        self.tol = Tolerance

                        pts_trunk_list = self.Branch_Route(Pts)[0]

                        pts_trunk_list = map(lambda x: filter(None, x), pts_trunk_list)

                        if pts_trunk_list:
                            temp_res = zip(*ghp.run(self._fit_plane, pts_trunk_list))
                            Plane = self.Restore_Tree(temp_res[0], Pts)
                            Result = self.Restore_Tree(temp_res[1], Pts)
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Plane, Result
                finally:
                    self.Message = 'Whether the point set is coplanar'


        # 点集根据与曲线距离分组
        class CurveDistanceGrouping(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CurveDistanceGrouping", "Q15", """Select the point within the Distance tolerance""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("46d778e1-7959-4851-aae1-2d983a231676")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "Curves associated with points")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "Pi", "Set of points to be grouped")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "The point whose distance from the curve is less than this value")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Pts1", "P1", "point meeting requirement")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Pts2", "P2", "point not meeting requirement")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Indexes1", "I1", "subscript of point meeting requirement")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Indexes2", "I2", "subscript of point not meeting requirement")
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
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUZSURBVEhLrZQNTBNnGMdvmdMsED8RdeLcBlipKFVE2utdr3dXEKZMTXAEpc5FBXFzy9T5MYSKUKhyqChhouKcYhgiU5QvB1rZdbMGhKIzBuecqQpoP+j3B+jdruttC1qXjfBLntz//7/3zeW5980DvIhoz7XQsOTcL/0CAyex0fCCF/9azdtwjB41drKCjYYXyY5enLMo7xwjZ3oTRizNm8BdLnubtT7h0mdGIrTSP4q6PmGBvTMo2tUeitCPeABf+8WbuC4zSmLMRsRPcxchLtli9BmRHEMdTUNMxTtx0+k9oLype8r8ZW6eMqdG/OzcJdharYIsNe2QrfYOZGv8HbQ3d4P2KzpwgHwkpNp7wYEOs8DZ4YCpR3YA6dkRjhtkNsyw24zq5AbUkP8QGyBaMWdJB9J3qBPtO3kNzL+knxy5zMVTZn8nfn6+FLZUFcLWml1Ca91myH4pVWi9vAK2tywBT13uDE7fbp5RWYDxnTdC+FTXVAChZSNirLJAiVExJo4qGrWo1jRu1qqiLSMBLpftHuAmysYHJ2VMY+0rgTNJ/TRQSjMywpv4IL7M9AmY1Uz7Twn7mY3+M1FbquOmx65LZ+Tr3sQHCScMsyLSSi+PeZe3ho1eQpjTUvTOwg2djAz2+PDVhe8H8RNDPHpIRG+9eDAITqlhLSDa1dYxHU7z/ArO5w0Uh7+1jvYL5Ki9b18A6ZONlRh3SSW6HCmqy2NqjxQzFqYgxiIpYiyWxpoq0xHiOj1VsILmHE7bjbjPSoXXvt/HO3GgkblFUlzbkb+AOEsHp2yycJP2tk7+YKkCom5JBW6NFKK6pUDsY9lMXC/TYn1ZdyWu3HbcTNxD9YVasb5IKzYWa8X2krvglW80vDL5ddjw7QORtVILO6vuIFSdRmit1QodDb8JHLU38fauh/Okx+kpSYk0SHVqBS6NlvmAlu0DAKA8zQzOcvlXAOA3aETEf/1EGLGx5MY4ftRaNvLJciXtH756f1pAmCiUjQYTc+j+Gd56ZkT4BQ4aEfFHdVujt12g/SaG/H0GQwLdZhTNTMivYmSYN/kHDlaQyDzGep2XOIWeP3vdIfVIIGAxG/kG75W9h+uzSMy8sxGz5jbg9n0/oLpCErEQdWJHSTXqPlaPUmXnUEd5E9xXTsKmChJ2VZJYS5uTl3KEDlqbRMPPVSRou0IK7Cqm1CTf3kryne0kMypIIKZHFogbsvLxp9kEppcXoE8VBGokCLGqqmsecYCOOL+5GTEdJxDjSQI2nSZgSwXBHDIhelifw0nOypjbcjgbfv4jAdqVTKmYUhN8ZytTHQRMPSaAyLbUN9hmBoHnP6jgfkh47nqqNxkiaE/GxwvdCiNukl/ALIo1qLFguiePDrdOCsEy1zNytMcPmbjuHRMl1pxk3JxXgZn2PsYs+x2o+eBtdKBIvoQqn51Kt/ns8C9kND1CkFF/Oki0UsXYAG/6al5DTUQkajmYiVlL1KjtiA11nOqdf7i0PHT7Zx/FUjUvzZvNPZQftPsqPU286t+nqC8QujQgXnMzF8pqoacmLKEhU7kTcdd0iRwXi2FnfSzy5Iy/Z93c6KNz3pqTnPDnpv/Lyo3U6Hmfnrw6IUSYy+89Phtxnd8ucl78CXY2WGFXUx/sUjbDtGp1IkVNZLcMD3xT43jI3rwUcinLILfqvtCtdgr7W++BA5pSgevW4ki6aQy7dHiAXGou1N+6CezvVIL9v5ihZ1pbdP/t9D8AtxNhaL+vceIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dis = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def format_tree(self, result_tree):
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

            def rewrite_list_to_tree(self, input, none_and_holes, source):
                """
                重写列表转树的方法
                """
                # 初始化目标树
                target_tree = gd[object]()

                # 嫁接至空树
                def proc(input, empty_tree, track):
                    path = gk.Data.GH_Path(System.Array[int](track))
                    if len(input) == 0 and none_and_holes:
                        empty_tree.EnsurePath(path)
                        return
                    else:
                        for i, item in enumerate(input):
                            if hasattr(item, '__iter__'):
                                track.append(i)
                                proc(item, empty_tree, track)
                                track.pop()
                            else:
                                if none_and_holes:
                                    empty_tree.Insert(item, path, i)
                                elif item:
                                    empty_tree.Add(item, path)

                if input:
                    proc(input, target_tree, source)
                    return target_tree
                else:
                    return target_tree

            def split_tree(self, tree_data, tree_path):
                new_tree = self.rewrite_list_to_tree(tree_data, True, tree_path)
                result_data, result_path = self.Branch_Route(new_tree)
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def on_curve_pts(self, tuple_data):
                curve_list, pt_list, origin_pt_list, origin_path = tuple_data
                count = 0
                index_list = []
                while len(curve_list) > count:
                    sub_curve = curve_list[count]
                    for sub_index, sub_pt in enumerate(pt_list):
                        if sub_pt:
                            res_bool = sub_curve.ClosestPoint(sub_pt, self.dis)[0]
                            if res_bool and (sub_index not in index_list):
                                index_list.append(sub_index)
                    count += 1
                without_index = [_ for _ in range(len(pt_list)) if _ not in index_list]
                res_pts, without_pts = [origin_pt_list[_] for _ in index_list], [origin_pt_list[_] for _ in
                                                                                 without_index]

                ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                   [res_pts, without_pts, index_list, without_index])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curves, Pts, Distance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.dis = abs(Distance)
                    Pts1, Pts2, Indexs1, Indexs2 = (gd[object]() for _ in range(4))
                    re_mes = Message.RE_MES([Curves, Pts], ['Curves', 'Pts'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve_trunk_list, tree_path = self.Branch_Route(Curves)
                        pts_trunk_list = self.Branch_Route(Pts)[0]

                        pts_trunk_list = map(lambda x: filter(None, x), pts_trunk_list)

                        structure_tree = self.Params.Input[1].VolatileData
                        origin_pts = self.Branch_Route(structure_tree)[0]

                        origin_pts = map(lambda x: filter(None, x), origin_pts)
                        c_len, p_len = len(curve_trunk_list), len(pts_trunk_list)
                        if c_len > p_len:
                            new_pts_trunk_list = pts_trunk_list + [pts_trunk_list[-1]] * abs(c_len - p_len)
                            new_origin_pts = origin_pts + [origin_pts[-1]] * abs(c_len - p_len)
                        else:
                            new_pts_trunk_list = pts_trunk_list
                            new_origin_pts = origin_pts
                        distance_zip_list = zip(curve_trunk_list, new_pts_trunk_list, new_origin_pts, tree_path)
                        iter_ungroup_data = zip(*ghp.run(self.on_curve_pts, distance_zip_list))

                        Pts1, Pts2, Indexs1, Indexs2 = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                               iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Pts1, Pts2, Indexs1, Indexs2
                finally:
                    self.Message = 'Points in the specified range with curves'


        # 点集根据距离分组
        class PointGroup(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Point Group By Dis", "Q3", """group the point by the specified distance""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ffb381c9-9d67-40af-9c68-c57301c1a1a3")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Points", "Pts", "Set of points to be grouped")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Specified distance")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point_Group", "Pr", "The set of points after grouping")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Subscript of the grouped points set in the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM3SURBVEhL3VVNS5RRFL5zzz13nHH6tDLKtMakMhQ1JylrMrHI6dNsMvtAS63UUsOkZf+gRVCtJGjRrk07WwYtqoUFgZuEIHDjqk0kpLfn3HlzoWNgGUEPPLzz3vPcez7uOe+ofw0KnkuKA1RpnlKSx6jeftSVPKKiqj2w/SHy9KA5EnbmRI7jSxFnmvG8levMhYgLFetnUJiM8HdgVMI0hh334cBzEcdtUccX8ezCsyfXcXvU6Xx9J1AvHqHNdI+7cdj1gD1RR/XIJp3jqCHs7GDM6RozCulKMOE3ZX6nwFL/phSD4czPOQiV0EOJ1qRRmvNgC6K/AkdXsdaU4wyyoaT9AOkG8DhYTqXmE7dCW2u/a1ZdWKsCm8AsWKZSUntzGjyLTXDkSwPKHRgcFIrT/UCtaCuNW5STU8juBjQHww7LSTF5QTagTMNSa76JDWdwwYhanMm7LjMTkOSJDtF2sqz3w8Ep6DqwpxeaQj0i9l9jtW7TFWZUl/EM7bPfdLV5j8gfwDKUEcBBXL+wOJDRcXJfBnflg0naKZjzM6qFsZs26TemGg7i9EUrNbdzIpTgCd9tRxH9ZUQvWUuDIBvYW8HDXpkF5Zyw03YA0R1Cba9FncVl06rQY9jgy3dNgdlvpxh1Z9i5E8TMMBqDcVfaqNvQ7AXng9bRsEXX+I2ySWqLTRaXr626C0kLWGjq7LSvP7pLApFOksuW2dER1ecPywbaQa98beVg6SBxhu6Q37TTjAeyfIO7mc0gaGXuBTGg0gCBbh6aUPMxKwfLxhSik4lGB/FAzDGGDZrtYIh28Wfv4GTQQVImaWdkCnuDHJYNZbQi9MhKROJEOkRSl9rKQSgHNPUi1EX6uZVph1OfgTiQ1q6xX2GOimYhlJg9dsbX9+cnQxxIJqg17JKBjFKaMZAszSCHS4mgpQJ6AmvdrC4bcJlDFu1nxYlkgna0iI4K6SXMIbAWjOkies3dgV2+uDV2BuvbAq4HF4bWqh9zMOlLcwyfjmJ6h+V4xqqawRi4kbbQW/m8UxVP4l06bFFYCzaCUnf5SmaDZFQBrvFvfxGSUQcoA5aWhaWG/NNJ3SPgcln4X6DUDx2VEoag8PxwAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.distance = None

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

            def group_pts(self, tuple_data):
                # 解构参数
                ref_origin_pts, origin_path = tuple_data
                gh_pts = map(self._trun_object, ref_origin_pts)
                origin_pt_length = len(gh_pts)

                total, count, group_sub_list = 0, 0, []
                # 循环分组点下标
                while origin_pt_length > total:
                    if not gh_pts[count]:
                        total += 1
                        continue
                    flatten_list = list(chain(*group_sub_list))

                    if count not in flatten_list:
                        sub_index = []
                        # 第count个点与所有点循环比较距离
                        for _ in range(len(gh_pts)):
                            if gh_pts[count].DistanceTo(gh_pts[_]) <= self.distance:
                                if _ not in flatten_list:
                                    sub_index.append(_)
                        group_sub_list.append(sub_index)
                        # 条件长度增加
                        total += len(sub_index)

                    count += 1
                res_pts = map(lambda x: [ref_origin_pts[_] for _ in x], group_sub_list)

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_pts, group_sub_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Points, Distance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.distance = abs(Distance)
                    Point_Group, Index = (gd[object]() for _ in range(2))
                    re_mes = Message.RE_MES([Points], ['Points'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        pt_trunk_list, pt_path_list = self.Branch_Route(Points)

                        # 构造输入端参数
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_pts, path_trunk = self.Branch_Route(structure_tree)
                        origin_pts = map(lambda x: filter(None, x), origin_pts)
                        zip_list = zip(origin_pts, path_trunk)
                        # 多进程
                        ghp.run(self.group_pts, zip_list)
                        iter_ungroup_data = zip(*ghp.run(self.group_pts, zip_list))
                        # 匹配树形
                        Point_Group, Index = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                     iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Point_Group, Index
                finally:
                    self.Message = 'Point Group'


        # 点排序（右手定则）
        class SortPointByRightHand(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SortPointByRightHand", "Q4", """Sort points counterclockwise by the plane Z vector,multiple points and origin are collinear,rank according to distance from the origin""", "Scavenger", "A-Point")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c37bf920-19b2-4d86-9ee4-18cfcddc05db")

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
                self.SetUpParam(p, "Points", "Pi", "Point List ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "FirstIndex", "F", "Specifies the starting element subscript")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Sorting plane")
                NORMAL_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(NORMAL_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Points_Result", "P", "Sorted points")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "index", "I", "The order of the output points in the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO7SURBVEhL3ZVdTFtlGMdJFqZ3Nq2MFkrbwMZHWzinn6fnq6ftwsfYEpxaN5PBmCOZMGDD2CVopBuVAi1QWZBAIMs0cZnsQpQbvZjG7GIzSp0mM8bMCyVR78wuvZh/n9O+ZEuoXhgujL/kl5P37Tn/97zPec5p2X+O2iNf2eydmx1suPs4OvNdto78B2y4+9g7vx6vab/7oCy+todN7S62Q/lbjq5f4GjLc2xqd7G137lQ0/ndTbv2mZlN7S6Ow39y1tZ7OTb81+wxOAw95oC538yTXvOAboXXNGBRh962xq7fqfQZhozuymELbzln5Mwj5uC+EUuocqhapLHdGGI5f0szN8BBm1GhTEhQ0iQdw1Ne+F89jaaTi/CNc5i/JWHzdwGtcxLElAx1UkY0p6HhSMMyyymNYb+hXw/0jSvwJosXKmSQFuATp+HsXUQo7UFi3Y+F2260zYrwjNHvtEhsRkPjIecqiyqN7aDtfTkbxuynMmY/l9AyLsH/poRTcwG0XuhDbc8ihAyH5qSE+tdFBC9JOHNVwYsrMsSkChvvGGNRJSmvP97wkzan4aP7PN77wY3EhIIfV1qBtRg2xgfQ07eMeysCvl06iKXLUUQzEr7/w4f1LR/4QRFPGY1HWVZJOO8wj3BWRTQdhDoRRFtSxBztYmPaj66zffAdW8X5iy6MJkPAux0YnAnj+RUPjq0G0NLteUgZB4pRJTA5TWcVKoded/3BCeTgWxoSlyMYzcl4ZfpZjCT7Mbwg4+pSDD/PR3GYFucuypAzGpzPuLYo5oliWgkc7fYb0Vy40DUS88MpBfmMitvpML6clrGZCeJuJowNupGjYwL8dI7eaZGshgOx+k9YVEn2Np1o3IpQqwXowcn6TujiwKUQmkZD6H0nhM3fBMRXBbhfC4FLiQiwFpYn6dyUihrOnmVZOykvL+e95z3QqP7xBQXhNG1bv5j0Ubu+fE3Ax/cb0H0lAD+VpBDMVGhnYkLE01WVL7C4nVRwFYNe6udzNyQ8gB8j6wI8bxSD9BJIKSpDKlg4br982wuEZxR4XvI+3EtFYHE72d9Vu67mIogvi8jedCG+FIRILapO0cvGlCYfjZVt6e4j8xrczzX/SjFPFtNKYA1bv+HPtKDxhBN1x11o7HbB3euE+ySpHwvqc8xTj+T7eTiUui9YVGkMtYa1atkKi2ApWBV6TLGqYLX0mLJuNaykLVIDU53pnz8RxD5Sr6GLdJMtpP7H4iF9ZIAUSP1rKZEqqZERMkZWkf8rysr+AkBB1/doXf1qAAAAAElFTkSuQmCC"
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

            def is_nan(self, angle):
                # 判断是否为失效值
                nan_bool = (not float('-inf')) < angle < float('inf')
                return not nan_bool

            def right_hand_rule(self, pts, center_pt, vec, pl):
                # 右手定则；共线的点将按点到源点的距离排序
                angle_list, collinear_list, coll_index_list, no_collinear_list, no_coll_index_list, null_index = ([] for _ in range(6))
                for pt_index, pt_item in enumerate(pts):
                    if pt_item:
                        pt_vector = rg.Vector3d(pt_item - center_pt)
                        angle = rg.Vector3d.VectorAngle(pt_vector, vec, pl)
                        # 是否共线筛选
                        if angle == 0 or self.is_nan(angle):
                            collinear_list.append(pt_item)
                            coll_index_list.append(pt_index)
                        else:
                            no_collinear_list.append(pt_item)
                            no_coll_index_list.append(pt_index)
                            angle_list.append(angle)
                    else:
                        null_index.append(pt_index)

                if coll_index_list:
                    collinear_indexes = [zip_coll_pt[1] for zip_coll_pt in zip(*self.sortbydistance(center_pt, zip(collinear_list, coll_index_list)))[1]]  # 共线点按距离排序
                else:
                    collinear_indexes = []
                no_collinear_indexes = [zip_no_coll_pt[2] for zip_no_coll_pt in sorted(zip(angle_list, no_collinear_list, no_coll_index_list), reverse=True)]  # 不共线点以逆时针排序
                res_index_list = null_index + collinear_indexes + no_collinear_indexes
                return res_index_list

            def sortbydistance(self, xyz, zip_coll):
                coll_pts, coll_indexes = zip(*zip_coll)
                distance_list = [xyz.DistanceTo(single_pt) for single_pt in coll_pts]
                sort_zip_list = sorted(zip(distance_list, zip_coll))
                return sort_zip_list

            def temp(self, tuple_data):
                # 解包数据
                pt_list, origin_pt_list, _index, ref_pln, origin_path = tuple_data
                if pt_list:
                    _index = _index[0]
                    ref_pln = ref_pln[0]
                    # 得到平面基础数据
                    base_pt, ref_vector = ref_pln.Origin, ref_pln.XAxis
                    # 平面投影
                    xform = rg.Transform.PlaneToPlane(ref_pln, rg.Plane.WorldXY)
                    projected_point_set = [rg.Point3d(_) for _ in pt_list]
                    # 投影点重排序并输出下标
                    temp_index = self.right_hand_rule(projected_point_set, base_pt, ref_vector, ref_pln)
                    # 判断F端是否为失效值
                    if _index is not None:
                        # 判断F端是否为负数
                        if _index < 0:
                            _index += len(temp_index)
                        # 若F端在正常范围内
                        elif 0 <= _index < len(temp_index):
                            pass
                        else:
                            _index = len(temp_index)
                            Message.message2(self, 'The index subscript is not in the range！')
                        split_index = temp_index.index(_index)
                        a_temp_list, b_temp_list = temp_index[split_index:], temp_index[:split_index]
                        res_indexes = a_temp_list + b_temp_list
                        res_pts = [origin_pt_list[single_index] for single_index in res_indexes]
                    # 若F端未输入数据
                    else:
                        res_pts = [origin_pt_list[single_index] for single_index in temp_index]
                        res_indexes = temp_index
                else:
                    res_pts, res_indexes = [], []
                # 解包数据
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_pts, res_indexes])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Points, FirstIndex, Plane):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Points_Result, index = (gd[object]() for _ in range(2))
                    # 获取输入端数据
                    j_bool_f1, origin_pts, _path = self.parameter_judgment(self.Params.Input[0].VolatileData)
                    re_mes = Message.RE_MES([j_bool_f1], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 数据匹配
                        pt_trunk, pt_path = self.Branch_Route(Points)
                        index_trunk, index_path = self.Branch_Route(FirstIndex)
                        pl_trunk, pl_path = self.Branch_Route(Plane)
                        pt_len, index_len, pl_len = len(pt_trunk), len(index_trunk), len(pl_trunk)
                        if pt_len > pl_len:
                            new_pt_trunk = pt_trunk
                            new_pl_trunk = pl_trunk + [pl_trunk[-1]] * (pt_len - pl_len)
                        else:
                            new_pt_trunk = pt_trunk
                            new_pl_trunk = pl_trunk

                        # 输入失效值时的F端数据结构
                        if not index_trunk:
                            index_trunk = [[None]]

                        if len(new_pt_trunk) > index_len:
                            new_index_trunk = index_trunk + [index_trunk[-1]] * (len(new_pt_trunk) - index_len)
                        else:
                            new_index_trunk = index_trunk
                        zip_list = zip(new_pt_trunk, origin_pts, new_index_trunk, new_pl_trunk, pt_path)
                        # 多进程处理数据
                        iter_ungroup_data = zip(*ghp.run(self.temp, zip_list))
                        # 匹配树形并分配输出端
                        Points_Result, index = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Points_Result, index
                finally:
                    self.Message = 'Points are sorted by the right hand rule'


        # 在指定平面内找出共面点
        class CopPoints(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CopPoints", "Q21", """Find coplanar points in the specified plane""", "Scavenger", "A-Point")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def get_ComponentGuid(self):
                return System.Guid("dc315fbd-b47a-442e-8b6e-e9db4b621900")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "P", "Set of points")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "Pl", "Specified plane")
                NORMAL_PL = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(NORMAL_PL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "The distance from the point to the plane")
                NUM = 0.0
                p.SetPersistentData(gk.Types.GH_Number(NUM))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Coplanar_Pt", "P", "A point in the specified plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Non_Coplanar_Pt", "N", "A point that is not in the specified plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index1", "I1", "Subscript of the point in the specific plane at the origin set")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index2", "I2", "The subscript of a point in a nonspecified plane in the origin set")
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
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPSSURBVEhLzVVLaFVHGJ56Z+acmbk38UUXxSLWV33gworWhRRBaBXEKoiPKMk9c07uI4kxQUQ3LbSUQhZtF3bTquAD0a0oqOBCV6JSFAQ1Ii1FcaEuBFF84PX7/zMmBnJFIQs/GM6Zf+b/55v/NeKd6BRKVd1GVXNb8G+DdIzQIyKVmjOq1zXUdgxvL4i6KIbVD0OcxFNVxR6XdfeP9HYnyWQWf6O6YTi1+djmGtqbdaxAaBMturc0O8xGor84WawXOp/8KCQMXGKW9ZytTs3aKIumqy7MKzDeidHjGoXELScV+sJtd1TNvlKZPSc6YZCwRTiZ2WOqah/Jqr1FJOHn4mRmSEYCU5mav2m/SsyvMPISCq/goj0QfQJmBenNdToQxhuqr0ju+5324/a7eB4IydT+SzcYx77ugwK5hJh6s5oUCLpSmqk7i1+GKe3X2P8Qh5LhBsUIBx6hJSLGMSOidHNvn7GO2FqahFP/hEtOqsS15cLmgBt2c0zIWMU+kUm8lOX4Yv7ircSgW78HcMvwN4SCt6tkt+vT5eLcIGKA/Vfwws9wXxJEzRH5aIaquNOqbgeVNwPk/7A0BoAxsLnAVyV/I0bwcVdYbQrs+ZpuIDNTH0kIVSvaRRxmgooKBzzlYA1n16GwynGTvaWlYv2E1iDJa4fIYG8gtI8XEIx25O1tjP9lYnpYCCDNjqp+bKaUxEB9rGF52SyB6+5x1lXsf8q7Bfl+s5+ND2fRc6FTPYvzto5Roy9OTswiUqD+ozLzi+5C8fh4A8sAKJ4fMkQZ480pksvU9XO6k3G6sTeDlA3fMUPaTHnNivEmttQEYHqF2dN+0sWBvID+xbeo2QfwxlUcsFiI9tbxCMhNDiaN1N4VVfcpKzQBuQpd9gXXQdU+LWRuRVjK0ds6PvwFJOYz9JYBbP4tKkdfBOk7gYKcD0JtOtGjN7yPAqpsveqy5+DPw3FH/HkQD6OB5jcayMW+ZWKYjQ6dmO85gNSy89hcftPjdVKajUw5i8y7qb39gRUC0Ah/gqsfYTxAkLtzKU6E4A9ZcwdlR7yMRCNymtoyUs+kZgr1Jaxd5fSktM6bWpl0CmW7kklRmlLB1Vwjfxq9vcj5SwYr9mWURtPo0Rkygi+K7gZX++bWCXzo2+9HZv7KScX9eV1AHlIeV3Lz6CRmOdTf4/zZ9Ha3rNlrSMkT2hfnkCy8HyeYUHBhIbXf0hI3x8w+ZqJ0UIaUzxmZ+7yZ2OL7RqEpeia2qMwNUIVTrIKUoTrsQll1B2TV7NUdeiYLcbVl8NlFsB3Eo7GDhWMCIV4DUCZZvLJ5OWoAAAAASUVORK5CYII="
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

            def coplanar_pts(self, sub_tuple_data):
                pts, plane, origin_pts = sub_tuple_data
                xform = rg.Transform.PlaneToPlane(plane, self.ref_plane)
                copy_pt = [rg.Point3d(_) for _ in pts]
                [_.Transform(xform) for _ in copy_pt]

                z_list = [abs(_) for _ in zip(*copy_pt)[-1]]
                need_data_index = []
                no_data_index = []
                for z_index, z_item in enumerate(z_list):
                    if z_item <= self.tol:
                        need_data_index.append(z_index)
                    else:
                        no_data_index.append(z_index)

                need_data = [origin_pts[_] for _ in need_data_index]
                no_data = [origin_pts[_] for _ in no_data_index]
                return need_data_index, no_data_index, need_data, no_data

            def _coplanar(self, pts, origin_pts, pln):
                "----------------------------"
                # 如果pln为空，则pln的值为世界XY坐标轴
                pln = pln if pln else rg.Plane.WorldXY
                "----------------------------"
                copy_pln = rg.Plane(pln)
                coplar_pt, need_index = [], []
                pts = list(filter(None, pts))

                if pts:
                    copy_pln.Origin = pts[0]
                    xform = rg.Transform.PlaneToPlane(copy_pln, self.ref_plane)
                    copy_pt = [rg.Point3d(_) for _ in pts]
                    [_.Transform(xform) for _ in copy_pt]
                    z_list = [int(_.Z) for _ in copy_pt]

                    total, count = 0, 0
                    while len(z_list) > total:
                        flatten_list = list(chain(*need_index))
                        if count not in flatten_list:
                            sub_index = []
                            for _ in range(len(z_list)):
                                if abs(z_list[count] - z_list[_]) <= self.tol:
                                    if _ not in flatten_list:
                                        sub_index.append(_)
                            need_index.append(sub_index)
                            total += len(sub_index)
                        count += 1

                coplar_pt = map(lambda x: [origin_pts[_] for _ in x], need_index)
                return coplar_pt, need_index

            def _do_main(self, tuple_data):
                pts_list, plane_list, origin_pts_list, origin_path = tuple_data
                if len(plane_list) == 1:
                    need_list, need_indexes = self._coplanar(pts_list, origin_pts_list, plane_list[0])
                    no_indexes, no_list = [], []
                else:
                    set_pts_list = [pts_list] * len(plane_list)
                    set_origin_list = [origin_pts_list] * len(plane_list)
                    sub_zip_list = zip(set_pts_list, plane_list, set_origin_list)
                    need_indexes, no_indexes, need_list, no_list = zip(*map(self.coplanar_pts, sub_zip_list))
                # "--------------------------------"
                need_list = [[]] if len(need_list) == 0 else need_list
                need_indexes = [[]] if len(need_indexes) == 0 else need_indexes
                # "--------------------------------"
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [need_indexes, no_indexes, need_list, no_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Pts, Plane, Tolerance):
                try:
                    self.ref_plane = rg.Plane.WorldXY
                    self.tol = abs(Tolerance)
                    Index1, Index2, Coplanar_Pt, Non_Coplanar_Pt = (gd[object]() for _ in range(4))

                    pts_trunk, pst_trunk_path = self.Branch_Route(Pts)
                    re_mes = Message.RE_MES([Pts, Plane], ['P', 'Pl'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)

                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_pts_trunk = self.Branch_Route(structure_tree)[0]
                        origin_pts_trunk = map(lambda x: filter(None, x), origin_pts_trunk)
                        plane_trunk, plane_trunk_path = self.Branch_Route(Plane)

                        pts_len, plane_len = len(pts_trunk), len(plane_trunk)
                        if pts_len > plane_len:
                            new_pts_trunk = pts_trunk
                            new_origin_pts_trunk = origin_pts_trunk
                            new_plane_trunk = plane_trunk + [plane_trunk[-1]] * (pts_len - plane_len)
                            target_trunk_path = pst_trunk_path
                        elif pts_len < plane_len:
                            new_origin_pts_trunk = origin_pts_trunk + [origin_pts_trunk[-1]] * (plane_len - pts_len)
                            new_pts_trunk = pts_trunk + [pts_trunk[-1]] * (plane_len - pts_len)
                            new_plane_trunk = plane_trunk
                            target_trunk_path = plane_trunk_path
                        else:
                            new_pts_trunk = pts_trunk
                            new_origin_pts_trunk = origin_pts_trunk
                            new_plane_trunk = plane_trunk
                            target_trunk_path = pst_trunk_path

                        zip_list = zip(new_pts_trunk, new_plane_trunk, new_origin_pts_trunk, target_trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self._do_main, zip_list))
                        Index1, Index2, Coplanar_Pt, Non_Coplanar_Pt = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Coplanar_Pt, Non_Coplanar_Pt, Index1, Index2
                finally:
                    self.Message = 'Grouping of coplanar points'


    else:
        pass
except:
    pass

import GhPython
import System
