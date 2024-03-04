# -*- ecoding: utf-8 -*-
# @ModuleName: Line_group
# @Author: invincible
# @Time: 2022/7/8 11:04
# coding=utf-8

import initialization

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
import ghpythonlib.components as ghc
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
import ghpythonlib.treehelpers as ght
import re
import clr
import System.Collections.Generic.IEnumerable as IEnumerable
from Grasshopper.Kernel.Data import GH_Path
import math

clr.AddReference("System.Management")
import System.Management
from itertools import chain
import math
import copy
from System import Array

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:
        # 点向式绘制直线
        class VectorLineTaking(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_VectorLineTaking", "W1",
                                                                   """Point-oriented drawing line.""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("69142382-49fc-4abe-8502-b1c7b585b980")

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
                self.SetUpParam(p, "Point", "P", "start of line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Direction", "D", "the length and direction of line\ndefault vector is length 10 in Z direction")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Vector(rg.Vector3d(0, 0, 10)))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Whole", "W", "direction in both side（open in default，True），close input False")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line", "L", "output line")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAF4SURBVEhLYxhywNj4DKuHxy12KJf6wNbjTLSz752dTt7X7ji6n9eGClMP2PucEbHzOLMbaMFze7czAVBh6gBn55PC9h6nj9m5n/KzczuRZu9+2gEqRTlwcTnDb+9x5iTQ0BSoEPWAq+sFbqDhR4FBkwUVoh6wt9/PAXT1QXuPs4VQIeoBUJK0cz+zB+j6CqgQ9UBo6CpmO4/T24HBUg8VogIQ3sAroXY2VkzxsCvQ8EVA3AaVoQbYz+Efcf74lp3///dO+fLfxP7EUqgEtcAa+frWh/9B4Ofv//+tnE+vhEpQB4jr7eR28z/3ePbCT//L6x7/1jE7Qb1cqhV6hQ2U/a2cTmcw8BywZWDbogmVohyAUgswne8E4lqoEHUBMKVscfA40wzlUhfYu59dZ+dxtgvKpS4AloorgXgilEtdAIxQYCY6NQPKpS6wdz8zB2jBPCiXegBYKrIADZ4OTC1LoELUBQ7uZ9yBJeNiKJf6AJSZoEwqAgYGAFDLiEMQByWiAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def create_line(self, start, vector):
                if self.factor is False:
                    line = rg.Line(start, vector)
                else:
                    line = rg.Line(rg.Line.PointAt(rg.Line(start, vector), 1), -vector * 2)
                return line

            def RunScript(self, Point, Direction, Whole):
                try:

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        Message.message2(self, 'The Point-terminal cannot be empty！')
                        return gd[object]()

                    re_mes = Message.RE_MES([Point], ['Point'])
                    if len(re_mes) > 0:
                        return None
                    else:
                        self.factor = Whole
                        Line = self.create_line(Point, Direction)
                        return Line
                finally:
                    self.Message = 'P+V=L'


        # 曲线修剪（简化控制点）
        class CurveTrim_S(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CurveExtendTrim", "W5",
                                                                   """trim curve，if input negative,trim curve,if input positive,extend curve.""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e96b5a92-6ac1-4a01-9e26-b341f34d39c8")

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
                self.SetUpParam(p, "Curve", "C", "curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "curve extend type，0=Line，1=Arc，2=Smooth")
                LINE_TYPE = 0
                p.SetPersistentData(gk.Types.GH_Integer(LINE_TYPE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "L0", "L0", "the extend length from the begin point，default is 10")
                START_DISTANCE = 10
                p.SetPersistentData(gk.Types.GH_Number(START_DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "L1", "L1", "extend length of end point,by default is 10")
                END_DISTANCE = 10
                p.SetPersistentData(gk.Types.GH_Number(END_DISTANCE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "C", "the result of curve")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMOSURBVEhL7ZVdSFRBFMeXepGstKcgWrb82F01SwgCRXfu3a879151bd2FogLpIQ0JCoWCwiu6UoFBVMSG9BZEUigE0UvUSybt190PDVZT+7AStSwLQ2Kmc7fpYRHBdn3sB8O9zJw5Z+bM/8zo/pMRVDHk016DebD1+I5Kp3rOKscvIhw6A+0ojyNOXg7tR0JkF8bJrWzK2qBK6WbiM18lPtMU6TaMjbfbpkX3eyp4vlLR85mKjbNUOPiB2usnKC/FqAUHFyFoEuHwEySGbyEcPY3kOGe3v85jLtMhivEO8ZUMUaW4grRtz11Sygua3I+kKiHWgoTQBYsQvAYO7yEh+Azh4Ci0eU5UqcM1STEE1xbhbHhHOSk6B0Fv2O3B9ECku1DPftdEbW1wk9MV11vlxAGE1UNIjHTCAvrB+Q/RMw87DPQx0/UDibEGTopNi41agKCfdWdHtRzbxmP1JCdG44L7I6TsDYVd3F+Ron+FFyJlvBS9Ao5nxcY5yP9bCv9DkKoGZpIZVinCw0EOWOURKnm+gKLimuMHFjHsYCaZYbG/KAZ5PnS4pkCyc+A0MoNE9RIvRE3MJHNqHMO7weGsJkNeVINIih72evs3suHs4YSAjN0zVEsLJ4bvwsprrThRmvVB/gWhpzlQWH5Ojv/E7k+pFNnrx0EtoW8cDgfgYG+DRFv4upEyNiUzbHKswColmmAHfpDiMARYsNUlWSXPp3YIBTaAXJF8NiU7qupfbbGI0XKtwOA+8kH7rl0ZCAdOMZP1AaHJHJBuFy+P/rLVjdFq/BKxoezgpZBBkypceouSd4HycmKhxjl0hA1nThGfLOTlWB84Xk4VmwzFJql9lfxzAzP5AzlfqCdKUerhIG17c6mi25AaWAV6tiCP9Oibm72DxOZZBsmqS5Cam9U4XMpM0iEdxlZoAeozNcE3pD06bCiNlN3lkijpMk+QLkOg59j1jgr7VDs8MjuZyeqkHPv3UaIUS6xrBVQxmknvHgftMZpZ19qgivkE6TQlSbf5MVFMg9SrW7/y1+l0vwFWvne7DtJTWAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_factor = {'-': ['Trim', None], '+': ['Extend', 'rg.CurveExtensionStyle.{}']}
                self._style = {0: 'Line', 1: 'Arc', 2: 'Smooth'}
                self.first_factor, self.first_line_length, self.first_type_of_line = (None for _ in range(3))
                self.second_factor, self.second_line_length, self.second_type_of_line = (None for _ in range(3))
                self._curve_style = None
                self.curves, self.pts = None, None

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

            def trim_extension_curve(self, curve):

                sim_curve = curve.Simplify(rg.CurveSimplifyOptions.All, sc.doc.ModelAbsoluteTolerance,
                                           sc.doc.ModelAngleToleranceDegrees)
                curve = sim_curve if sim_curve else curve
                curve = curve.ToNurbsCurve()
                after_shear = eval('curve.{}(rg.CurveEnd.Start,self.first_line_length)'.format(
                    self.first_factor[0])) if self.first_type_of_line is None else eval(
                    'curve.{}(rg.CurveEnd.Start,self.first_line_length,{})'.format(self.first_factor[0],
                                                                                   self.first_type_of_line))
                if after_shear is None:
                    result_line = curve
                else:
                    result_line = eval('after_shear.{}(rg.CurveEnd.End,self.second_line_length)'.format(
                        self.second_factor[0])) if self.second_type_of_line is None else eval(
                        'after_shear.{}(rg.CurveEnd.End,self.second_line_length,{})'.format(self.second_factor[0],
                                                                                            self.second_type_of_line))
                return result_line

            def temp(self, tuple_data):
                curve_list, origin_path = tuple_data
                new_line_list = map(self.trim_extension_curve, curve_list)
                ungroup_data = self.split_tree(new_line_list, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def str_handle(self, str_data):
                if str_data is not None:
                    symbol = '+' if str_data[0].isdigit() is True else '-'
                    num = abs(float(str_data))
                else:
                    symbol = '+'
                    num = 0
                return symbol, num

            def parameter_handling(self, par):
                par_factor = self.dict_factor[par[0]]
                line_length = par[1]
                type_of_line = par_factor[1].format(self._curve_style) if par_factor[1] is not None else None
                return par_factor, line_length, type_of_line

            def get_se_pt(self, no_red_line):
                render_points = []
                for single_line in no_red_line:
                    start_pt = single_line.PointAtStart
                    end_pt = single_line.PointAtEnd
                    sub_pt_list = [start_pt, end_pt]
                    render_points.append(sub_pt_list)
                return render_points

            def RunScript(self, Curve, Type, L0, L1):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result_Curve = gd[object]()
                    self._curve_style = self._style[Type]

                    trunk_curve, trunk_path = self.Branch_Route(Curve)
                    trunk_curve = map(lambda x: filter(None, x), trunk_curve)

                    len_c = len(trunk_curve)
                    first = self.str_handle(str(L0))
                    second = self.str_handle(str(L1))

                    self.first_factor, self.first_line_length, self.first_type_of_line = self.parameter_handling(first)
                    self.second_factor, self.second_line_length, self.second_type_of_line = self.parameter_handling(second)
                    if len_c:
                        zip_list = zip(trunk_curve, trunk_path)
                        iter_ungroup_data = ghp.run(self.temp, zip_list)

                        Result_Curve = self.format_tree(iter_ungroup_data)
                    else:
                        self.message2("terminal C can not be empty!")
                    no_rendering_line = self.Branch_Route(Result_Curve)[0]
                    pt_array = map(self.get_se_pt, no_rendering_line)

                    self.curves = no_rendering_line
                    self.pts = pt_array

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Result_Curve
                finally:
                    self.Message = 'Extend Trim Curve'

            def DrawViewportWires(self, args):
                try:
                    for _f in self.curves:
                        for _s in _f:
                            args.Display.DrawCurve(_s, System.Drawing.Color.Green, 2)
                    for sub_pts in self.pts:
                        for _pf in sub_pts:
                            for _ps_index in range(len(_pf)):
                                args.Display.DrawDot(_pf[_ps_index], str(_ps_index), System.Drawing.Color.FromArgb(248, 141, 30), System.Drawing.Color.FromArgb(255, 255, 255))
                except:
                    pass


        # 多折线按线段序号偏移
        class OffsetBySerial(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_OffsetBySerial", "W13",
                                                                   """polyline offset by assigned number""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f86b09ae-745e-4577-90b9-f5c72b7d6fe1")

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
                self.SetUpParam(p, "Curve", "C", "polyline")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Indexs", "I", "numnber of polyline")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "offset 10 by default")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "R", "multiple broken line after offset")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI6SURBVEhLYxgFww+ISbqlAXEUlEtdICsboW1uv/m/vun0/0AuK0SUSsDO7bSjvef5Lxq6zZv0zWY9d/S62gOVwgTKGsVzNXSb1hjZrdSFCuEFQIMTnX1v/Xf0ulwD4ruFPjS2dNj+T0zGOxqsAAYsnI5J27gdnWNivfy/ntn0XzYuhz46el+9Zu95ocXJ46weVBkKAMk5+978b+9+LhIqBAYaeo2XLB13/mcQEDXTF5N093fwutjm5H39q5PPjeOaBu0uQDVCrr4PFIGuKgXi0w5el784eF266eh9rUVFu8JHXNKz0sb54Eqgyz/bup2yghiLAHJKybVqunVHGWxcj063ct7739Ru3VVn39v+UHkM4Ox9ScnR60KJo+flE/pmM/7buZ/8r2sy5Y5X0D15qBLsQEO3PkVJPX8RlEsUkJLzc1FQzZoNZApARGgP2GRkQuyhbJIBE5TGCpwC7poZmM+5Z2a3/j8w7qqgwsQBNZ26ej2TqW8MLOZ3eATekoEKw4Gj95VaYLz9sXDcNkVZq6zS3vPcf3uPUzFQaZyATULWzwSYmnZb2G/5oK5Tv8HCccd5J5+bX5y8r63QNploBQwOM0evK8eAyfO1vdtZD6g+BlPbdfGmNqv+y6tmoSRZFCCnkpJsarvmP1DxVt+Iz+JQYQZ79/MOQBdvMbSY99/Yaul/C4ft6228DwtCpWGAXcuw64KiWmYRlI8JRGUDlOVVMjOgXAwgq5hgK6eSngzljoJRQHPAwAAAp3S7mE1UKsAAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.curves, self.pts = None, None

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

            def _offset_line(self, tuple_data):
                curve, sub_index_list, sub_dis_list = tuple_data

                line_list = [_ for _ in curve.DuplicateSegments()]
                test_is_linear = [_.IsLinear() for _ in line_list]
                colse_factor = curve.IsClosed

                if not all(test_is_linear):
                    return False
                elif len(line_list) < len(sub_index_list):
                    return 1
                else:
                    curve_planar = curve.TryGetPlane()[1]
                    offset_line_list = []
                    count = 0
                    for c_index, c_item in enumerate(line_list):
                        if c_index in sub_index_list:
                            count += 1
                            if sub_dis_list[count - 1]:
                                new_item = c_item.Offset(curve_planar, sub_dis_list[count - 1],
                                                         sc.doc.ModelAbsoluteTolerance, rg.CurveOffsetCornerStyle.
                                                         None)[0]
                            else:
                                new_item = c_item
                            offset_line_list.append(new_item)
                        else:
                            offset_line_list.append(c_item)
                    return self._find_closest_pt(offset_line_list, colse_factor)

            def _find_closest_pt(self, lines, res_bool):
                origin_zip_list = list(zip(lines, lines[1:] + lines[:1]))
                zip_one_by_one = origin_zip_list if res_bool else origin_zip_list[0: -1]
                _pt_list = []
                for zip_items in zip_one_by_one:
                    single_pt = rs.LineLineIntersection(zip_items[0], zip_items[1])[0]
                    _pt_list.append(single_pt)
                if not res_bool:
                    _pt_list.insert(0, lines[0].PointAtStart)
                    _pt_list.append(lines[-1].PointAtEnd)
                else:
                    _pt_list.insert(0, _pt_list[-1])
                res_line = rg.PolylineCurve(_pt_list)
                return res_line

            def temp(self, temp_data):
                if temp_data:
                    curve_list, index_list, dis_list = temp_data
                    sub_cur_len = len(curve_list)
                    index_list = [index_list] * sub_cur_len
                    dis_list = [dis_list] * sub_cur_len
                    sub_zip_list = zip(curve_list, index_list, dis_list)
                    res_line_list = map(self._offset_line, sub_zip_list)
                    return res_line_list
                else:
                    return None

            def _get_mid_pt(self, no_red_line):
                render_points = []
                for single_line in no_red_line:
                    de_curves = [_ for _ in single_line.DuplicateSegments()]
                    sub_mid_pt = []
                    for _ in de_curves:
                        _.Domain = rg.Interval(0, 1)
                        _mid_pt = _.PointAt(0.5)
                        sub_mid_pt.append(_mid_pt)
                    render_points.append(sub_mid_pt)
                return render_points

            def RunScript(self, Curve, Indexs, Distance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result_Curve = gd[object]()
                    no_rendering_line = []

                    trunk_list_curve, trunk_list_index, trunk_list_dis = self.Branch_Route(Curve)[0], \
                        self.Branch_Route(Indexs)[0], \
                        self.Branch_Route(Distance)[0]
                    trunk_list_curve = map(lambda x: filter(None, x), trunk_list_curve)

                    curve_len, index_len, dis_len = len(trunk_list_curve), len(trunk_list_index), len(trunk_list_dis)
                    re_mes = Message.RE_MES([Curve, Indexs], ['Curve', 'Indexs'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        new_trunk_dis = trunk_list_dis if trunk_list_dis else [[10]]

                        new_trunk_index = trunk_list_index + [trunk_list_index[-1]] * abs(
                            curve_len - index_len) if curve_len > index_len else trunk_list_index
                        new_trunk_dis = new_trunk_dis + [new_trunk_dis[-1]] * abs(
                            curve_len - len(new_trunk_dis)) if curve_len > dis_len else new_trunk_dis
                        z_zip_list = zip(trunk_list_curve, new_trunk_index, new_trunk_dis)
                        zip_list = []
                        for _ in range(len(z_zip_list)):
                            if len(z_zip_list[_][1]) != len(z_zip_list[_][2]):
                                Message.message1(self,
                                                 "{} broken line failed to offset,reason：the subscript is not equal with offset distance list！".format(
                                                     _ + 1))
                                zip_list.append(None)
                            else:
                                zip_list.append(z_zip_list[_])
                        temp_res_lines = ghp.run(self.temp, zip_list)
                        for _ in range(len(temp_res_lines)):
                            if not temp_res_lines[_]:
                                no_rendering_line.append(trunk_list_curve[_])
                            else:
                                sub_res_line = []
                                for sub_index in range(len(temp_res_lines[_])):
                                    if temp_res_lines[_][sub_index] is False:
                                        Message.message2(self,
                                                         "in {} group the {} broken line failed to offset；reason：the broken line be offseted must be straight line！".format(
                                                             _ + 1, sub_index + 1))
                                        sub_res_line.append(trunk_list_curve[_][sub_index])
                                    elif temp_res_lines[_][sub_index] is 1:
                                        Message.message2(self,
                                                         "in {} group the {} broken line failed to offset；reason：input subscript is greater than the number of broken lines！".format(
                                                             _ + 1, sub_index + 1))
                                        sub_res_line.append(trunk_list_curve[_][sub_index])
                                    else:
                                        sub_res_line.append(temp_res_lines[_][sub_index])
                                no_rendering_line.append(sub_res_line)
                        Result_Curve = self.Restore_Tree(no_rendering_line, Curve)

                    _pt_array = map(self._get_mid_pt, no_rendering_line)
                    self.curves = no_rendering_line
                    self.pts = _pt_array

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result_Curve
                finally:
                    self.Message = 'polyline offset by number'

            def DrawViewportWires(self, args):
                try:
                    for _f in self.curves:
                        for _s in _f:
                            args.Display.DrawCurve(_s, System.Drawing.Color.Pink, 2)
                    for sub_pts in self.pts:
                        for _pf in sub_pts:
                            for _ps_index in range(len(_pf)):
                                args.Display.DrawDot(_pf[_ps_index], str(_ps_index),
                                                     System.Drawing.Color.FromArgb(248, 141, 30),
                                                     System.Drawing.Color.FromArgb(255, 255, 255))
                except:
                    pass


        # 偏移多边曲线
        class PlineOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PlineOffset", "W15",
                                                                   """broken line offset by segment，3 different type offset mode""", "Scavenger",
                                                                   "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4121d1e6-b3a6-4e53-a4e6-c2346dbb6703")

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
                self.SetUpParam(p, "Curve", "C", "original curve broken line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "the distance of offset，the number of input offset distance equals with the number of folding")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Simply", "S", "terminal is closed by default，after open（True）is normal offset")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Double", "DU", "terminal is closed by default，after open（t）Line the first and last polyline")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Rescur_list", "R", "final broken line")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHnSURBVEhLYxiywM7jlKG9++lIKJe6wN71lI6d++nzdm6nHaFC1AOO7ie17d3PnLNzP2sJFaIeCFHYqw4y3MbztDVUiETw/z8jw7bvbgapd12cnU96OLifcbf1OO3mZHfcVbHpdYxc9YPbrg7kGg4C9f+Z+Ca9umgUf2ufk9PJbnuP0xPsPc5OcHI6NVE/5+l0hm0/46EqyQfeBof17d1Ob4RyaQPs3M9UAVNJP5RLGwCMzF0OHmedoVzqAzuvs5r2HmeOubpe4IYKUR8AI7nQzuPMdCiXNgBoyRZ7tzM+UC6R4PAHQfFFz4nyurHLGX57t1M7pzBM4YEKEQYsyz6v1c5/dsjJ8eQKYIpZbu95dgkwKOYBw3wGMN1PtPM42wXETfbu5yrtXU5n2Pid3yva9uQiw4V/hB1l739ewDLg3D6juFvKNjaHRG3dLss6up9St/O4YOjged4alHPtPc8EAAuyKGBpmeLgcibfOuhyPvOij40MZ/5zQY3BDew8Tjc5uZwuh3KpC+y9TkoAg+SAq+tO2iQ9O/dTfbbuZ7KhXOoCe/fzCsAkt8/Y+AwrVIi6AJRC7DzPxUG51AU+xkc1gBbsAhb4jFAhKoKV/zj1Eq9sAObGAKgIlcHqL4ZMi97vhvKoDBgYAPSXr1lTGqsuAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = False

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def offset_curve(self, tuple_data):
                single_data, dis = tuple_data
                new_offset = ghc.OffsetCurve(single_data, dis, None, 1)
                return new_offset

            def find_closest_pt(self, data_list):
                count = 0
                colse_pts = []
                while len(data_list) > count:
                    one_index, two_index = count, count + 1
                    if two_index < len(data_list):
                        single_pt = rs.LineLineIntersection(data_list[one_index], data_list[two_index])
                        if abs(single_pt[0].DistanceTo(single_pt[1])) < 0.001:
                            colse_pts.append(single_pt[0])
                    else:
                        if self.factor is True:
                            two_index = len(data_list) - two_index
                            single_pt = rs.LineLineIntersection(data_list[one_index], data_list[two_index])
                            if abs(single_pt[0].DistanceTo(single_pt[1])) < 0.001:
                                colse_pts.insert(0, single_pt[0])
                    count += 1
                return colse_pts

            def double_line(self, origin_line, offset_line):
                start_pts = ghc.Discontinuity(offset_line, 1)["points"]
                end_pts = ghc.Discontinuity(origin_line, 1)["points"][::-1]
                set_of_poly_list = start_pts + end_pts
                return ghc.PolyLine(set_of_poly_list, True)

            def RunScript(self, Curve, Distance, Simply, Double):
                try:
                    res_poly_line = None

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        Message.message2(self, 'The p-terminal cannot be empty！')
                        return gd[object]()

                    re_mes = Message.RE_MES([Curve, Distance], ['Curve', 'Distance'])
                    if len(re_mes) > 0:
                        # "--------------------------"
                        return None
                        # "--------------------------"
                    else:
                        self.factor = Curve.IsClosed
                        if Simply == False:
                            explode_curves = ghc.Explode(Curve, True)["segments"]
                            explode_curves = explode_curves if isinstance(explode_curves, (list)) is True else [
                                explode_curves]
                            if len(Distance) == len(explode_curves):
                                zip_offset_curve = zip(explode_curves, Distance)
                                offset_list = ghp.run(self.offset_curve, zip_offset_curve)
                                closest_pt = self.find_closest_pt(offset_list)
                                if len(closest_pt) < len(offset_list):
                                    closest_pt.insert(0, offset_list[0].PointAtStart)
                                    closest_pt.append(offset_list[-1].PointAtEnd)
                                res_poly_line = ghc.PolyLine(closest_pt, self.factor)
                            else:
                                Message.message1(self, "distance data list must be equal with the number of polyline！")
                        else:
                            res_poly_line = ghc.OffsetCurve(Curve, Distance[0], None, 1)
                        Double = False
                        Rescur_list = self.double_line(Curve, res_poly_line) if Double == 'T' else res_poly_line
                        return Rescur_list
                finally:
                    self.Message = 'offset broken line'


        # 圆弧拾取
        class ArcPick(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ArcPick", "W42",
                                                                   """simple curve pick up plug-in，modify by parameter，rebuild a new curve""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c81a3c2c-9d6c-4833-9ad0-2fe541933635")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "curve data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "filter curve accuracy")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "designate the specific radius of curve（select circle by radius）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(2.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result", "RC", "get final result curve")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQbSURBVEhLzZVdTBxVFIBHbNQYleiDoVaTaoBlt6W2sVWLu3NnZufn3tnlp2xrNManqjHxxRfTaKCjaEIxauKLDz7oe5PGxCgqJmorUHZm9g8WlKKWamNxqWCCrdKmcz1nuKWlXfD3wS+ZzO45Z86599xzzpX+V2ipyQ0kNaoTmt9N2Oj2hDWxXqj+Ofel379RTZWfUljxMDheNNq+42bHDzzZeowrrHBWYaXPVFZ6UphLhHx+kyTxa8TftYlrR7Yo9ui4tetHTjt/AodFLlveCZl6ZXifVO3RUG7uOom6oTg9ukW2XJ9Y7uPCxerI1N2msrG50LFdrBC70CXbuWhsT/k61MNKb5BZqZmw4ivg/Ber8xQEd+fV1PgFQt2+0MlqEJbbjk7xI3gPtOi5O4SqKhCsDlL1UTI9yY324xx2+K5QCRynBles2IUeWE1WYfnzmGtCcwPSnoPXCquqwGof0dumXPg+l2yd4sn01zxhZSckh9cIE0lSqP+Y2fE9RM7PQm6ntdR4eJAJOrJXmKzKrTsXNmvpY29DARwilt8Pizqnt37DZcNlwkSSEpa3Xm2fasHTh+19gAFgy3l4FiH3W4VZVXivtFH8DJFNfz/LzGIxvCdEl9hpDN0u09x5Qr2AWEc3YrrA8C2hvoqgO/J08Gp0MdjfuI87ZB3KZOY1J1snMcCpiwWxTMIY0TD3sIvj+B8Ob11L2+DNoRIInossHzY4fYb3Rjl/bRMPXoyc4U6sDuX305FbiOXNaakJrpr5e0Pji4DiUax5iP6lEIVwR6oBh3uDvugcrDoTOI1P8N4Y530xHvRETgfdjTuEaQicRd7sOAFn6JlCtMSlAO6gEIXwA/fUBk6kwl/fxPlLTUtP6Lypwl9ouOqMZOqXjfZpLrO8IURLQAAlTJHlTjuXlxkQdNVvA4ezYVoOhM5ngq5Is1AvgynFhtPS1VJkZ+sI9RdVeyzArhXiZYJ9EOTlprPw/Bw8Xx8T4hUozHtIh36AIHNLc+kKYBeHKZRZwsxWbfegu+GBoKth5couQ7ay77Ddp6FJvUNCtBLZ8h/GplNZcSFhuncJ8V+CGEObVbt8Tm/7lieYrwnxlUCzWa6HQ46w/HA97b9eKNZE1/1awgrjNFOB9GQ/EeLqyHouCl18BisKZv4R6I+7hQocfVoL8+YgDkQhkuI0H4OmLFidMzi2Zwkt3SlUqxO3hnU47AWWgXyywq/QfD3oFGaOr6W/+h2KIQ4Dbgc4fAOe32hnhYN9BWXCxZ/TYgxuVeyxD+FG47h11S5x7FBI4QI04zzOLCwIrHm82WT9iwbx6d9DtseicC2+ieWHTiEAjvILsPJ5uPH64Z0Rpv8OvOzV1MQMBiK08Kxplm8Tqv+OB7XhDXDIA3AmHwvRGkjSHyZFFajLbW89AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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

            def _judge_curve(self, index_curve, curves):
                for _ in curves:
                    if isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Line, rg.LineCurve, rg.ArcCurve)) is False:
                        return index_curve

            def filter_by_line(self, wait_curves):
                wait_curves = wait_curves if isinstance(wait_curves, (list)) is True else [wait_curves]
                count = 0
                fit_curve_list = []
                while len(wait_curves) > count:
                    start_pt, end_pt, mid_pt = wait_curves[count].PointAtStart, wait_curves[
                        count].PointAtEnd, ghc.CurveMiddle(wait_curves[count])
                    new_line = rg.Line(start_pt, end_pt)
                    ref_mid_pt = ghc.CurveMiddle(new_line)
                    curvature = abs(mid_pt.DistanceTo(ref_mid_pt))
                    if self.tol < curvature:
                        fit_curve_list.append(wait_curves[count])
                    count += 1
                return fit_curve_list

            def rebuild_circle(self, arc_curve):
                base_pts = map(lambda arc_line: ghc.DivideCurve(arc_line, 3, False)['points'][0:3], arc_curve)
                new_circle = map(lambda pts: rg.Circle(pts[0], pts[1], pts[2]), base_pts)
                filter_cir = [_ for _ in new_circle if _.Radius > self.r]
                if len(filter_cir) != 0:
                    min_cir = filter_cir[0]
                    for other_cir in filter_cir:
                        if other_cir.Radius < min_cir.Radius:
                            min_cir = other_cir
                    return [min_cir]

            def _join_handle(self, zip_list):
                data_tree = gd[object]()
                curve_list, path = zip_list
                if len(curve_list) == 0:
                    rebu_cir = []
                    data_tree.AddRange(rebu_cir, GH_Path(tuple(path)))
                else:
                    temp_line = [_ for _ in rg.Curve.JoinCurves(curve_list, 0.001, False)]
                    false_fun = map(lambda x: None if x.IsClosed is False else x, temp_line)
                    temp_line = filter(None, false_fun) if filter(None, false_fun) else [temp_line[0]]

                    explode_line = map(lambda line_single: ghc.Explode(line_single, True)['segments'], temp_line)
                    filtered_curve = map(self.filter_by_line, explode_line)
                    rebu_cir = map(self.rebuild_circle, filtered_curve)
                    for _ in rebu_cir:
                        if _:
                            data_tree.AddRange(_, GH_Path(tuple(path)))

                return data_tree

            def RunScript(self, Curve, Tolerance, Radius):
                try:
                    Result = gd[object]()
                    self.tol = Tolerance
                    self.r = Radius
                    tree_leaf = [list(_) for _ in Curve.Branches]
                    tree_Path = self.Branch_Route(Curve)[1]
                    tree_leaf = map(lambda x: filter(None, x), tree_leaf)

                    re_mes = Message.RE_MES([tree_leaf], ['C terminal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        filter_list = []
                        for _ in range(len(tree_leaf)):
                            if self._judge_curve(_, tree_leaf[_]) is not None and len(tree_leaf[_]) == 0:
                                Message.message1(self, "{} curve data group has wrong data！！".format(_ + 1))
                            else:
                                filter_list.append(tree_leaf[_])
                        zip_list = zip(tree_leaf, tree_Path)
                        for _data in ghp.run(self._join_handle, zip_list):
                            Result.MergeTree(_data)
                        return Result
                finally:
                    self.Message = 'pick up curve'


        # 线段点线转换
        class Dotted_Line_Conversion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_StartToStrat,EndToEnd", "W45",
                                                                   """starting point is connected to the starting point, and the end point is connected to the end point""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8f4035c7-a253-4efb-8a12-c39d503bf27d")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "multiple curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Start_Curve", "S", "start line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "End_Curve", "E", "end line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "A", "all lines assembly")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Tree_Result", "T", "output line by data tree")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAS6SURBVEhLvZVrbBRVFMdHiCI+CGqQSGqh6bJboBW1D9qmu7O73Zm5++hLWh5B09pgY2IwRJBQrd2WpsWqTROpDRgNShA/iNEP2EoEoyHS3Z2d7buU0kJaCxGEik2qUdN7PPf2unXsJxPj70v3/P/33vOYOx3pf4VWW1bQphQVyqTFQvpvoXWWs9D+GNDatdVCMkGDFpUesO2BoHSXkOLQYEoqNK4rRm+RkBZCa606tCVhAmuDkOLcDmY/SOusv0D7eqANj5YLmUMbEpNovXUG3k6F32pSW4W8kGdLPj35+nMnYEvhKYeQ4rhJqHaiZitA8wY4VHHgPSFzaNCWAQdXA7y1Eob3amNCXkiWp78j2z8FGWp/rpA4hHQsyVFik8XFBlRu+Qay1b7TwuJYHWOZ71Q20y9374TtRaduWbJuLhOWGVmLnvEUXgbZa2QIiePUdL9SdBly1J4fsrULsw5NDwmLYyex/dn+G5CuXsHkvbMef2ytsMzgxnOegkvgUkMbhcRB/WOt5Co4iN7k0CIzsqb3CYuD/hl34AJggdPsr10xFoyYI5NoOD8wDA6fsU5IUhYJLUN9WibGtINEMvH3LB40KGxJLupejt6MQwuPY+LjWsk1sJPwDmGbwYWGOzAEed6wVUiSg0RLyFPXASv/hGAyl6+XVRpPYCe6yg7F7o5hgue9pVOARewXthk8rN/l68cWQ0lCwvYjx72lt8CuRrYqyul7Xb4+UwI8+A1f6U/gJHq5w6sr3s0/smRtwjYjE32IVegJDCSyOBCI3oNVTTm9PX/Icvdyt7tr5VwCfT6Bpnd7Csd4US6/ka4WT2KCyOfCNoMbR5zebmwxlMBipxbV+Ey1yNdzftcalgA7HeAxrsOYYpeTPFajKfkFIzhO8y2Lg62P4XOAXI+xisckepjN1K5FX2Cxi+jJLv8A66CXxU4S3eHdfJON7AMW5xYaq5zeGMbGqCTBHUwzgQfyBHkktoItwFav4TOhsta9hvl5+WGr2z/EDozx9Zr+EcGZyySyjcfywH2oTaM/lY7jZZoJNEdZAmY6SCxTLf4e2w3H23VpERu75ziCrrIyWIyjucGej13TH2F+MAiLsMgJ9GdzlO8e5pv+Ds522OnrAUJGluDCZnY78GbsEfZ8AhL9yqnom9TiCXZ9zwmbw57P3EWY69oEdtCHFYGsGhbceMntH8Tf5y3CjifAEXzB3mofu/Na5GVhc9CL/PNljYPXNJSnxSBX6XnJUzjK7v55YXFYYladXTP6cQwXeTeeLtNB2Pm3bK+shB8X0jyblL5Oxd+LbUcn3EXs7TSqhMXxBKKJmcrA77naAOT4cDxq2BBWnDT3SGeWbwps8rjpHyanouSzd6/WFsDgvm3g8XZNp/nHHxAW5/6Unx9qerrl9tArbjhS1Qap+RdfFFaco5XVZ0/urofGZ1pkIc0zulepgEMWgNYnoXr74SYhx6lKP3Inflavw5sJAPU26Ni1i7+Qf0FrLE/QxtUUWhOABpNPCHke2iIt/fW11GNX9mkfBsuP3i1kE7Qu+X1oTQNM1Alg/v7i99oG9SkAbegHbe1C/vfQlg0bIbh+wYefAa9a8+jBlJ20JWGpJEnSnytwY1SaJ/chAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def get_points(self, origin_curves):
                """
                分解线段，使得线段集的起点和起点连接，终点和终点连接
                """
                origin_curves = [_ for _ in origin_curves if _ is not None]
                if len(origin_curves) == 0:
                    start_lines, end_lines, all_lines, tree = [], [], [], []
                else:
                    start_points = [s_point.PointAtStart for s_point in origin_curves]
                    end_points = [e_point.PointAtEnd for e_point in origin_curves]
                    format_start_points = list(zip(start_points, start_points[1:] + start_points[:1])[0:-1])
                    format_end_points = list(zip(end_points, end_points[1:] + end_points[:1])[0:-1])
                    start_lines = [rg.LineCurve(s[0], s[1]) for s in format_start_points]
                    end_lines = [rg.LineCurve(e[0], e[1]) for e in format_end_points]
                    all_lines = start_lines + end_lines
                    tree_branch = [start_lines] + [end_lines]
                    tree = Grasshopper.DataTree[rg.LineCurve]()
                    for sub, leaf in enumerate(tree_branch):
                        tree.AddRange(leaf, Grasshopper.Kernel.Data.GH_Path(sub))
                return start_lines, end_lines, all_lines, tree

            def RunScript(self, Curves):
                try:
                    # 判断输入的列表是否都为空
                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]  # 获取所有数据
                    j_list = filter(None, list(chain(*temp_geo_list)))

                    re_mes = Message.RE_MES([j_list], ['Curves'])

                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object](), gd[object]()
                    else:
                        Start_Curve, End_Curve, Result_Curve, Tree_Result = self.get_points(Curves)
                        return Start_Curve, End_Curve, Result_Curve, Tree_Result
                finally:
                    self.Message = 'convert point to line or convert line to point'


        # 合并曲线
        class CurveJoin(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Curve_Join", "W2",
                                                                   """curve combination（multiprocess）""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3aaa7084-475b-40dc-a140-0b7c6d8d7d65")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "a set of assembly line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerace")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "New_Curve", "C", "combine broken lines")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIsSURBVEhLY6AlkJQJDIQyqQ/UdGrnuwU8/A/lUheo69ZP8wh+9d/QbM4tqBD1gLpO7RzPkDf/jSwXXANyJSCiVAJqOvUTQC43slwMcrk0RJRKQE27eiY4WCwXPwRylSCiVAJK6oWzoYbfAXJlIKLkA0Ytg45DmvrtC0AcFa3SiR5BL/8bWix4BOQqgsQoAjxC2poOnhf+6xpN3CqvmtHoHvjsv45R/2uglDpEBYVAVikh3tHr4n913cbnjt5XgBG65ApQmOJggQMRMacqB8/z/519b4FSyw9hcccJ8krJQUApVogK8gEziODgkLIytV3z3z3oxX8791P/Xfzu/DezW/+fjU1YA6yKFCCrEBembzZru7HVsmumtqvv6ppMPszOLu0gKuEUomM0aZq2Uc88Ve2qRmiZQ7oPVDRLF9p7nP1vbLX0r6P35f9eoR/+K2sU3YBKUwUwArG1mk7dVUevS/9BkatrMukpUIwNLEsFwK+mW3fAK+Tdf2XN0vNmdhv+GlktPQWVoxhwA7P/CVAO1TWeuIKLS87H1f/hf3W95j6oPEWAHZhb94HCXNug5yBIQFzcUkxdr3G2hISXJlgFBYBL26h3m1foR2AO7QMZzgsRpg5g0zbsPgByua7J1P1APjdEmDqABWj4VojhU3YB+ewQYeoADi2D9vVeIe//65tOPwzk80CEqQNYtA16N4LCXM9kKijMuSDC1APcwOLgHRAfA7L5IELUAgwMAG2XtZzil6uYAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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

            def _join_curve(self, tuple_data):
                curve_list, origin_path = tuple_data
                curves = [_ for _ in rg.Curve.JoinCurves(curve_list, self.tol, False)]
                ungroup_data = self.split_tree(curves, origin_path)
                return ungroup_data

            def RunScript(self, Curve, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = Tolerance
                    New_Curve = gd[object]()

                    curve_tree, curve_path = self.Branch_Route(Curve)
                    re_mes = Message.RE_MES([Curve], ['C'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        zip_list = zip(curve_tree, curve_path)
                        bole = ghp.run(self._join_curve, zip_list)
                        New_Curve = self.format_tree(bole)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return New_Curve
                finally:
                    self.Message = 'combine curve'


        # 最近点连线
        class PCLINE(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PCLINE", "W3",
                                                                   """refer geometry shape to the closest line""", "Scavenger",
                                                                   "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7f05f3bb-8ff1-4a7d-8c6e-315f0bb6bf69")

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
                self.SetUpParam(p, "Geo", "G", "a geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "RefCurve", "C", "curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Line", "L", "The line of a geometric object to the nearest point to this line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Close_Point", "P", "Closest Point")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH5SURBVEhL1ZJNSBRhHIeXajbcD3WbzdaBMlI0JVzdmcXdmXfcrf3QvQmdFQIVOkidIoKo6BDlsUOHPsCDWmueu0iWZW2xsIFHjxJJSrGFJkT8/Q3zDyw6yVvQAw/zznP5McPr+a/QtIHkkebhERy9bpGL0tVzbyVdeEehkGFyk4o/Zk6tpQsVUtVkhptU/Lo5uZrqL1Odqqe5SeVfDEx9TPW/pfqwkeImlaBhTq/19mGgPmZzk0pQt6bXe/veUCDUKbhJpVa3HmKghIGoxW0nxUBr99Jg+PCzXX+ebj1at/OvKBg8keT0kyv7BoeX5soVorsTnylqrpxE1OFtOAqH4AN+noY3oHNTBqDTz8Ix3KItO7+IgeMJvO9k3H/p2vJ3Ap+qRIns+/OIZ+APWIL34SachEVI8A68Cp0+Byux5ATZuZcYaO/B+6+cKpTPXb+5+mFkbLkUObrYxDkA97pHz35+Oqjw934Av6hq55wv+MOAy7ifD7uhzhDFqsi9oJra1jg3qagY+CJyCxg4ZnCTStgQM19FdoF8vmbngkinIS5mNkT2OQaaurlJ5VDcfrxhZecxoP2VgYhhz25amXlSfFoXN6lE4mL2m5V5SopyMMpNKo0Y2HIHGjq5SaUxkX5Cdv41eb1aGzep7GnpuHC5pePiLZwVN3k82/Q+nY1ZhBAvAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __get_line_point(self, curve, point):
                self._switch = False
                recent_par = curve.ClosestPoint(point)[1]
                nearest_point = curve.PointAt(recent_par)
                return nearest_point

            def __get_line_curve(self, cur_one, cur_two):
                self._switch = True
                line_data = [cur_one.ClosestPoints(cur_two)[1], cur_one.ClosestPoints(cur_two)[2]]
                return line_data

            def RunScript(self, Geo, RefCurve):
                try:

                    structure_tree, structure_tree1 = self.Params.Input[0].VolatileData, self.Params.Input[
                        1].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    temp_geo_list1 = [list(i) for i in structure_tree1.Branches]
                    if len(temp_geo_list) < 1 or len(temp_geo_list1) < 1:
                        Message.message2(self, 'The Geo or RefCurve cannot be empty！')
                        return gd[object](), gd[object]()

                    re_mes = Message.RE_MES([Geo, RefCurve], ['Geo', 'RefCurve'])
                    if len(re_mes) > 0:
                        # "--------------------------"
                        return None, None
                        # "--------------------------"
                    else:
                        new_point = None
                        if isinstance(Geo, (
                                rg.Line, rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve)) is True:
                            new_point = self.__get_line_curve(Geo, RefCurve)
                        elif isinstance(Geo, (rg.Point3d)) is True:
                            new_point = self.__get_line_point(RefCurve, rg.Point(Geo).Location)
                        elif isinstance(Geo, (rg.Point)) is True:
                            new_point = self.__get_line_point(RefCurve, Geo.Location)
                            Line = rg.Line(new_point[0], new_point[1]) if self._switch is True else rg.Line(new_point,
                                                                                                            Geo.Location)
                            Point = new_point
                            return Line, Point
                        else:
                            Message.message1(self, 'The battery does not support this geometry type！')
                            return gd[object](), gd[object]()
                        Line = rg.Line(new_point[0], new_point[1]) if self._switch is True else rg.Line(new_point, rg.Point(Geo).Location)
                        Point = new_point
                        return Line, Point

                finally:
                    self.Message = 'line the nearest point'


        # 求线长度
        class LineLength(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GetLineLength", "W32",
                                                                   """Find the length of the line and keep the specified decimal place""", "Scavenger",
                                                                   "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c683174a-8426-4e49-9fa3-0d986603bb70")

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
                self.SetUpParam(p, "line", "C", "Find the length of the line list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "decimals", "N", "keep*decimals.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Length", "L", "length of segment.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMtSURBVEhL3ZRNaBNBFICjWBRR0JM3f1Dwag1WbJKd3SS7O5tNmqS1VUEPBQ+KCOpFD0KwIghKi0UU8VIPgiLiRQSpWmzVNtk0yaap9if2V6m2/hS0anvw+WY7rYRY+2NPfjDszHtv35v35s3Y/g8IaVgmqMYtyZdpEGm8odgbswabCzi8Ja8bCI2Xc/P5Y7fHC9DRRznUD5LeATTcCYGKbnDj3OPHddkwEBo9xc3njxVANfokPQOFjhaof/IBbt8dgm3FLeg4DpgBfo3j3Hz+TAUQtTZweA0YHvkB56t7rGCLGsAhp2H3fhO+jk3Avso0FJHY4gbYQVJwuioLn0fH8RwSWP9WENT5B4hEYCkh99bw5e8AdlcKrlwfwAAT0JUdg+rLfbDdGZ1TAOzEFaK/3SNqqRpRS76S9PZRQTEkSzl9Br4MaLjz4J4UlB8wgYYS4FL+noHgT+8SdbMWHfd6At1Wx6mlQ+AJdAJRWqllxAIQNf5JCQ2A6OsEgXZYQ8K5Fw1p2Qg7i5w2lXzJCtGXbnT7XwItfQ9K+A2IWuI77r7erbcdK1ZjW7kpI7KUKFEq+dpKBTWWN7yBbKlLTm1ili45Koia+VwO9liOWWvj7p+6tfQhrz+z3nK3UESaOOvW29HxO+YUszVvuPVkEVcvHLv9WgGmfkcJDYIc7GeOH0t62s7V/wqWj7beV8NvrYPDLCJckQelD5ZjqWQsYa0n0PUIW9zFVTODZ1BnOcc3iajGQS7OYae7eZ2km2cws6yXd1Jg7zg2ilHFTf6MoEZPsJKwNnWpsSNcnAPRWislX3pYDQ8B28hkJ5kPCU0dLS55tpqb5eNSjCLsqp+s7oTGLnFxDkQxzsnBXlBCrEWTgyJNnpR87Ru4embYrcS6d7ILg2m22GywhKummcqOBSBaqs6pN63lqtnBn2sm0zW/EeXFFi6exqkZDtau1sWkiatcPDfwxjrZz2x3LrUlr+5+f3wlPitZKzvVaOLiuYMliesVX/AdiTVyUQ7YSRcnL5o5RtTmjVw8d3BXFzyBbFKixmYuygEfvZvsiSBK82EuWlwIyawSaKqQL2fBZvsF0I7e31s7rqUAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def RunScript(self, Curve, Number):
                if Number:
                    Number = math.fabs(Number)
                digit = ".%uF" % Number if Number else ".0F"
                Length = gd[object]()
                List_Length = []
                struct_tree = self.Params.Input[0].VolatileData

                temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                length_list = [len(list(filter(None, _))) for _ in temp_geo_list]
                Abool_factor = any(length_list)
                re_mes = Message.RE_MES([Abool_factor], ['C end'])
                if len(re_mes) > 0:
                    for mes_i in re_mes:
                        Message.message2(self, mes_i)
                else:
                    Curve_path = self.Branch_Route(struct_tree)[1][self.RunCount - 1]
                    for crv in Curve:
                        if crv is None:
                            List_Length.append(None)
                        else:
                            List_Length.append(format(float(crv.GetLength()), digit))
                    Length.AddRange(List_Length, GH_Path(tuple(Curve_path)))
                    # return outputs if you have them; here I try it for you:
                return Length


        # 根据线长排序
        class LenghtSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_LenghtSort", "W35",
                                                                   """Sort the Curve according to length, from smallest to largest""", "Scavenger",
                                                                   "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e93bc482-0f62-42b6-bf53-97caa94435bc")

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
                self.SetUpParam(p, "Curve", "C", "Line need to be sorted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "line after sort")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Length", "L", "length after sort")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAK9SURBVEhL7Y9rSFNxGMaPUASlkjcUPGeXlIwo6EtBWByXbO7utqYkLTU3BC0yxKRiEAR9EKm++CGhL0WRic0rXsowuxzbdOpUXPM2nTrMSxZJS6W9/d3+gWbEWq5P/eDh8D7P+38fDvEfnxn7Usp2rJQeBijfjq2tpXtR/3oebsKLKX06tjxI1F2nZSpzLh79x/ThitEJJdAyXqzFlgexstMmUhpdePQfZv4SY4fr0GQvysaWB5HSZEQF03j0n/bZC4wN9NAQqILn7/OZQbgKtSMFgSlodOqYHiiEKlt+YArqp88yJrgIldYAFdROapkOKIAHVt3GAkWnSaTomMSj/zxBBa/gPNwb0GZhywMq6JKetHyVqS3F0rTeIkXGu0KxyszGse9UjGuYVrcO7vbmnMKWBx6v77Y8zTonTH37TaQwrsrUAyti5RsJjn2nYkLT1bCkgUqHxmqYznxmcGY+bfmU11zlyL4ll9eE0HRZMJ9/f5dUWr4TP/kzHo2eqa5b0LkNM9lQM5cFhlkNNLu08HA0ox+vbGJfsjEiTjGWezDvYxi2fo/bHRwFQES63UQE+oYh7cbRL4naXxbMktiAk2p37lFN6Q9oP0fj6GcgiBTO0qG8VUH4CRc/nLckCOe5kJYEMZIFcVy6QxGn2iyubEhLpvQss6RDwFFMAVs2PM9VTpYkZC1y8GEv9LW2bZTIssBRzgFb7gB26kZx1gvlP8SWTwAl7EOyIPUCSzyIdtaKRla58pHHXFmH949oum0bye+cYUntQIkGgUKL67X2cJPQ3pq8x71iSYbRcQeQAvMimfzyzl66LtJTgAgijxuOxCY2JUUnVvus2KP1alLQvcyWjaPD6G8E5gmK13455tCNKHz374gXDoVSwn6gUnpsZFLruYiEnBAcbQ2sYw1hsXSjOp4gdmDrX0MQ3wEezYpPK8Qy/wAAAABJRU5ErkJggg=="
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

            # 排序
            def CurveLen(self, Curve):
                Length = [i.GetLength() for i in Curve]
                CL = zip(Curve, Length)
                AREAS = sorted(CL, key=lambda x: x[1], reverse=False)
                return [_i[0] for _i in AREAS], [_i[1] for _i in AREAS]

            def RunScript(self, Curve):
                try:
                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)
                    re_mes = Message.RE_MES([Abool_factor], ['Curve'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        if len(Curve) == 0:
                            return [], []
                        else:
                            Curve, Length = self.CurveLen(filter(None, Curve))
                            return Curve, Length
                except Exception as e:
                    Message.message1(self, "run error：\n{}".format(str(e)))
                finally:
                    self.Message = 'Length Sorting'


        # 曲线取值
        class DTS_Get_Vale(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DTS_Get_Vale", "W44",
                                                                   """Decomposed line，and the subscript value（S is the edge, V is the point）""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("50fd4090-ae7a-4e99-8ef2-075c8be0ac09")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve to be decomposed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "The subscript of a decomposed edge or point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "S_V", "B", "select edge or point，not to select edge by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "data1", "D1", "First set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "data2", "D2", "Second set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "data3", "D3", "Third set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "data4", "D4", "Fourth set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "data5", "D5", "Fifth set of data")
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
                        self.marshal.SetOutput(result[4], DA, 4, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM4SURBVEhL7VRdSBRRFLYesh5Ksz+EXkohs5+XSFbbnXvnZ2fuzOyu7mI/IJGEEEGBLz4EglSPPRQFPRW9GWhEPVRKDyXors7O7uzOrqar/dHaD1GRVkgg07mz00amub5ED34w3DlnvnvuOWe+e4qW8f+Al5N7asjgOsfMwyWGy5CSbMZK8iaWkwOsYnZj1WyqJPeLHcriQJLWJta/tBCJpd2quZ76eH5oA5bN81gxZ6TgGwtJ0a/wZBiiT5PQOwsrqSwmRpMdYAHw6sgx+wU2DguBZ1buEN1NfQyJjsuNHy3I+gEjx70IPVptc2FlpFiIVdMjcuMHOCgZ9pCoWH0wvYp+57jIFpYkjkMCo/4jMxb10QPapWDWguzGaUtyPu2oR9Y5mzA/ViKSOM2qqc9SCCok+hQjRbPQQovaUPkEJvFcBRS8L7WftsUxC8Y+4WEJkpMt0M4uLCd64YBLLDFE+LQix/hXQGRwq8sVXuOYedCqONk8Bdn1wU99D+skZNvpUWKMQ1kcWNQOC/7xb5jEUm4S30R9qN4oxUqiA3oMKnpNFZZliHYH/lcvlo1Zp893kThQZQeZB5zvyQn7BUn6Yy8oSApOWlQh1Iel2AX10LTFyskeJBnYJjpAPn0jVHOO949ZQmAClBa/7CaRvYKgl9SR/gpE4idBfRnfLxXpbVTrkNkUS6IV1OdWte28z6y1CQsAieFKuHSd3vrnFn3gIIv3Z+xEWSU1BnGbHSq9FKZQJ/XvcMwlAYl6FaemWlklfZGVzTNYTh1wPhUOQjLFUvBFOax/jJOC4BJ7ymq9A5sdMw+qaejnbWjfNO8bpW2cBa33eHJaLwwciVdDkLeckv4EN9JFfW6iIVYdjuTmTmKGkbRuUNBZWK+BVH/Oo3usNLTLDjIHjBLZyQcmunIG0Tqo7KgcMdGv5HxRnfNnviBitCJklNpEB3WB/rVIMdpBhpYXZhiSjeuMOMgir7YbEgjBnlv2bGt4lZ9FmJKFwFMg6w3U55Gi5TDYfgs8Fx5v3za4dDd42EuDUSWJMNNgAH6HO3KVqsyhAlkM1yASsSfpUkGnAFLTjZxvpAWpw8LcipfxFxQV/QB4Loa50TfLBgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            @staticmethod
            def get_v_s(array_list):
                c_list = [i for i in array_list]
                point = []
                for i in c_list:
                    point.append(i.PointAtStart)
                    point.append(i.PointAtEnd)
                p_list = list(set(point))
                p_list.sort(key=point.index)
                p_list += [p_list[-1]]
                return c_list, p_list

            @staticmethod
            def subscript_value(mod_list, list_data):
                new_list = []
                for index, i in enumerate(list_data):
                    new_list.append(mod_list[i])
                return new_list

            @staticmethod
            def index_erreor(P_Slist):
                if len(P_Slist) < 5:
                    P_Slist = P_Slist + [None] * (5 - len(P_Slist))
                    return P_Slist
                else:
                    return P_Slist

            def RunScript(self, Curve, index, S_V):
                try:
                    data1, data2, data3, data4, data5 = (gd[object]() for _ in range(5))
                    re_mes = Message.RE_MES([Curve], ['Curve'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve = Curve.DuplicateSegments()
                        C_List, P_List = self.get_v_s(curve)
                        I_List = [list(map(int, re.split(r"[.。!！?？；;，,\s+]", i))) for i in index]
                        New_C_List = self.index_erreor(
                            [self.subscript_value(C_List, I_List[i]) for i in range(len(I_List))])
                        New_P_List = self.index_erreor(
                            [self.subscript_value(P_List, I_List[i]) for i in range(len(I_List))])
                        if S_V == 'S' or S_V == 's' or S_V is None:
                            data1, data2, data3, data4, data5 = New_C_List
                        elif S_V == 'V' or S_V == 'v':
                            data1, data2, data3, data4, data5 = New_P_List
                    return data1, data2, data3, data4, data5
                finally:
                    self.Message = 'decompose curve'


        # 曲线筛选
        class FilterCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FilterCurve", "W31",
                                                                   """select curve by curvature""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("0bf1b87f-be62-4681-95cc-a2cacce8a98c")

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
                self.SetUpParam(p, "Curve", "C", "curve list data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "curvature tolerance")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_Result", "CR", "curvature greater than the curve（result curve）")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Line_Result", "LR", "curvature less than the curve（result line）")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAXnSURBVEhLbVZ5bBRVGJ8gR+RoRSkQkLZQ2tJikaR0e+3um9ljrm63pQcoRkVEE5CYSEgQhW4pPWgBC3jgQTyimIjR/zSaRs6yy+5Ou7RdurS0GqCCXEVEAgKd5/e9nS5F+SWTnfmO9/ve+463HO8MFjrdfYutUsDNS5pkEQMFFkWz8bLfzt7loIg6fF6r2LfynZWNtctKflgmyEEV7Yd1D3scxX1lnEXSlpOSSHJ2tjbGIh6exSudTYLSEeLVE52C0rXL6jiUSsjB0QXuyKRLG/Leou/n0lPrnbaFcm9CoaMl0eOho1D3sIeIbXM5q6QtwQUg2lm82tmjVAxSm6ubCkVhqlRcxd9zguSfzwF0T+oauiOD6h9yKQvsPfvsxacvmp1HclH3MBCiTeF4sa3c5dLGA4FXKb9CrbL2qSB1pBPRO5fIbTulsj8okbQedNA3z15Dt8+n+i4uZT7fv1ouvwQBdN8slHw8W/E/yHcem8pFz1hbIi0ewIUOGboYiBT8HoknmG4JtGnccroNCDyzF6DOKvnXiuBnK4rcsTp9CnMYAUZApBBP5OB7LHoxuMzQxYAByGWXaJL1Qg1tGmUQpDECBBF9q5wlZ+BYI9Qq+coMMQMjgEUFImtfSGUXKC5m6GIgin+RWHqOppCBnfrWca/Qpkyq12SwnAzDIvtfdLj7qaP4NLWI3ucM8X0COPcqTKhVPF5l6GIwQ4RqxTU6zTK4hjaOeZURbEzNMNQxwHEtsRf3UGfJb9QieVeijLggyUTRXEQNLYQKugcJu0pEbR7zAGBlCWrXOYe7j3JZ+pN63ZQ3aGMmpRvSYjYjYXX43Lai7iGx9CyFnKyW5d5xrEyZUvS/rVRcoURp/xuiabbKwSZeDl3G6C3i8V1oQz3p1Uhwa0vi7Bx7WC6UfWaUj4RV9DkFV/dtdiJK8AVGYJJ746LKQBVE/A8mXCnHHuiCxLVtY54AfVNaLW1Io5GNQnqOs+s6HgeRAs8b6hisUqvF7u7/zgzTgBHkid7HDR1nlo8k2NSIwLtO2onqn26IGfSq9AbakEFvfDBhapatt8LuOkWxAGD36w2TB5Dt0OIZgbmoc7Ih47Kh6eyurhy7qzvfbvc/YYgZgKARCfQtGUn4jcdhKzp5AxsOm5IZjUC0ioDA4eiPRwGc/euCGr4ml12kcvllPKK7UARbmTUA6n87rc+g1JOZaIi4AmfrQvA5i7kicvs3mZn7xxqq+wT4wbIOC/PKiSGYhHvh2c3L7YPoCMTvog3soJnWwQ5qU2fi9zDYkFQ729XK6+h/OMfewnaea/NNA4KA26z400BxE1r+pkUMmpgXoNChJYLjGaf7V8o9TZP12ml1tA76oI5LMExiMJl+jCNK6KcoSUc3TtICd+skDme/VQquxcqBctxh2McAzbcCJ+wMy+V1+taJHr1mztDul2tNBVLER+TAOsPMgGcUUdo+L37mDuxa+5aJWCeLgT0sUYpWyoQjQJyBp7AcU/kzn+h1k+v1zcn3PM/uMeVJXXcxTzBm/heUTQ0vB6JFJvl4XJRACm6LjurACsMmBjPceNLi8zSFH2jWG+IbaA0kOcyNzbJHsiC5AyxHcuhrvFMMlxhyyMHpeKNJMB5Ksb0hmlZDFwPs7jM8oscK/irR6+Oa6OZ5ME0zWd/kC8eSeLWjw0juAbP5aKzcEdFxLQcr8vK8j0KzHMVdEKltr9kemGMr8s6E92psJCi/32FQjIYL52NanQ5lmvSYsQY0U0s8LN7CSNSOsMV5eLahihLAQFuaWRkeK6gsmj7cMo4IXgnBlTkI7yf/xMsfHfRN876CeQQ7mMtGyzAqK/c/wivtX0btw+et9mM5KGdlSuRQJWtpAEZjUzs9QOQVlE4Nzrg5X/iFdS1Cr07Zp1elDtGPuPGG6AFALhswX3Cn38Zyxz8ScCO1vSS4I+m4HQcj8sC/hNZJ7B0iIyQ80Sy3J6D+4pv5B2hNLvUs3ZOM3yMfHCtO588TYArX4zUKR7/K4Y7M+BfSUhTIJ1pA7QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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

            def find_curvature(self, o_curve):
                if o_curve:
                    start_pt, end_pt, mid_pt = o_curve.PointAtStart, o_curve.PointAtEnd, ghc.CurveMiddle(o_curve)
                    ref_line = rg.Line(start_pt, end_pt)
                    ref_mid = ghc.CurveMiddle(ref_line)
                    curvature = abs(mid_pt.DistanceTo(ref_mid))
                    return o_curve if curvature >= self.tol else None

            def RunScript(self, Curve, Tolerance):
                try:
                    Curve_Result, Line_Result = (gd[object]() for _ in range(2))
                    self.tol = Tolerance

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        Message.message2(self, 'The C-terminal cannot be empty！')
                        return gd[object](), gd[object]()
                    re_mes = Message.RE_MES([Curve], ['Curve'])
                    if len(re_mes) > 0:
                        return [], []
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_curve = self.Branch_Route(structure_tree)[0][self.RunCount - 1]

                        result_cur = ghp.run(self.find_curvature, Curve)
                        index_fit_cur, index_line_cur = [], []
                        for index_c in range(len(result_cur)):
                            if result_cur[index_c] is None:
                                index_line_cur.append(origin_curve[index_c])
                            else:
                                index_fit_cur.append(origin_curve[index_c])
                        #                index_fit_cur.AddRange(List_Length,GH_Path(tuple(Curve_path)))
                        Curve_Result, Line_Result = index_fit_cur, index_line_cur
                    return Curve_Result, Line_Result
                finally:
                    self.Message = 'filter curve（curvature）'


        # 曲线按照参照平面排序
        class LineSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_LineSortByXYZ", "W25",
                                                                   """sort Curve-list，when the axis input is null,sort as length of line,inputs x, y, z will be sorted by its axis coordinates，CP specifies plane""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def __init__(self):
                self.bool_factor = False
                pass

            def get_ComponentGuid(self):
                return System.Guid("ff552258-2c50-4fe8-b032-9ec25ef804b5")

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
                self.SetUpParam(p, "Curve", "C", "curve list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Axis")
                AXIS = 'X'
                p.SetPersistentData(gk.Types.GH_String(AXIS))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "XY Sort by axis XYZ, world XY by default")
                PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Sort_Curve", "C", "Sorted list of curves")
                self.Params.Output.Add(p)

            def sort_cur(self, set_data):
                # 获取片段集合中所有点和平面
                origin_curs, pl = set_data
                curs = map(self._trun_object, origin_curs)
                pl = self._trun_object(pl)
                if len(curs):
                    # 新建字典
                    dict_pt_data = dict()
                    from_plane = rg.Plane.WorldXY
                    # 获取转换过程
                    xform = rg.Transform.PlaneToPlane(pl, from_plane)
                    # 取线的中心点
                    pts = [rs.CurveMidPoint(cur) for cur in curs]
                    # 复制点列表
                    copy_pt = [rg.Point3d(_) for _ in pts]
                    # 将转换过程映射至点集合副本中
                    [_.Transform(xform) for _ in copy_pt]
                    dict_pt_data['X'] = [_.X for _ in copy_pt]
                    dict_pt_data['Y'] = [_.Y for _ in copy_pt]
                    dict_pt_data['Z'] = [_.Z for _ in copy_pt]
                    # 按轴排序，最后结果映射只源点列表中
                    zip_list_sort = zip(dict_pt_data[self.axis], origin_curs)
                    res_origin_curs = zip(*sorted(zip_list_sort))[1]
                else:
                    res_origin_curs = []
                return res_origin_curs

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Sort Curve'
                # 初始化输出端数据内容
                Sort_Cur = gd[object]()
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    # 确定不变全局参数
                    self.axis = str(p1[0][0]).upper()
                    self.j_bool_f1 = self.parameter_judgment(p0)[0]
                    re_mes = Message.RE_MES([self.j_bool_f1], ['C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 多进程方法
                        def temp(tuple_data):
                            # 解包元组元素
                            origin_cur_list, origin_pl_list, origin_path = tuple_data
                            # 若平面有多个，重新赋值
                            o_pl_len = len(origin_pl_list)
                            if o_pl_len == 1:
                                origin_cur_list = [origin_cur_list]
                            else:
                                origin_cur_list = [origin_cur_list[:] for _ in range(o_pl_len)]
                            # 每个单元切片进行主方法排序
                            sub_zip_list = zip(origin_cur_list, origin_pl_list)
                            res_cur_list = map(self.sort_cur, sub_zip_list)
                            # 每个单元切片是否有数据输出
                            if res_cur_list:
                                ungroup_data = self.split_tree(res_cur_list, origin_path)
                            else:
                                ungroup_data = self.split_tree([[]], origin_path)
                            return ungroup_data

                        # 数据匹配
                        cur_trunk, cur_path_trunk = self.Branch_Route(p0)
                        pl_trunk, pl_path_trunk = self.Branch_Route(p2)
                        cur_len, pl_len = len(cur_trunk), len(pl_trunk)
                        if cur_len > pl_len:
                            new_cur_trunk = cur_trunk
                            new_pl_trunk = pl_trunk + [pl_trunk[-1]] * (cur_len - pl_len)
                            path_trunk = cur_path_trunk
                        elif cur_len < pl_len:
                            new_cur_trunk = cur_trunk + [cur_trunk[-1]] * (pl_len - cur_len)
                            new_pl_trunk = pl_trunk
                            path_trunk = pl_path_trunk
                        else:
                            new_cur_trunk = cur_trunk
                            new_pl_trunk = pl_trunk
                            path_trunk = cur_path_trunk
                        zip_list = zip(new_cur_trunk, new_pl_trunk, path_trunk)
                        # 获得结果树列表
                        iter_ungroup_data = ghp.run(temp, zip_list)
                        Sort_Cur = self.format_tree(iter_ungroup_data)

                # 将结果添加进输出端
                DA.SetDataTree(0, Sort_Cur)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANlSURBVEhLvZVbSBRRGMfXygiLHqKQCFKIkAy6sHjJdefM7O7MmZm92IV9KKhAy4cIesmnHjZ6LCjooadehAhLMNDoQkJBXnZ3ZnZX3TRvmYkvFhhCEBaevjN9LW7tFGb0Axnnf/Z8l/N93xnXf4eEzK2CmmyMxdgalP4tomzUqEfnmFc1FJRswGmVqKZi0Wh2PUp/h9ttFotaek6gZjtKNoJq3tWjH5kUtNwo/UxRDX1c7orF/py5QJM3CbU+LY9W1Kz7yuEZ5lWSdSjlAQF55YYpJlKTouQMOIj4Q6+ZEOjfjZKLqGabcvgdg2ctSnkI1Lgm6UPjsPcWSs6ImuHxh0cZkRMHUAIHxj0eIdTiIEo5eEOAgwGBpq7Dc5SQ5+twqTBeOd7iC75i9WpqG0q/dUCoIRI1tSjqA11Qv0VCkwFc+hVZzmwE4/OQ6lOUbMBBm6MDxTgPNbvM/4dmiMHeC/ZCIcB7q9wwzQTd2oOSDUTZIUfeOGSQFuXwZBMYPyeHx5ocMyA0FdCOvWeC0n8JpRxwtl3cAdHTubr8oBK6LRSaLeHZ86fDrLAiiHJY1AZGUMiDULNTjkzCHKT2o7QyIM1y3jmCkjiBUh6CanQFwuNQ+HglSitDoskKf3jMcVBW7YCfIwzRgkDjd1DKg2hm56occCDKq/yYvNTYjlIOQbWe8Aw9NLEXpRy1St8WXzBbXR+29tXRngpeT1zKx+frL7WvCGrd4O+SauyyFwC4a7r9kIGkW2UwqRv8oZEWX3iw1F7TDBkC6xX1oWlo4/FolK21NxUCinwbWnJe0FKafV2oVivXeRf5gsNLnpC5E9YfRI5/hZmwmu1NCMxBFgbuJL4WxqsY1VJwiEHLngHjH/hcwOB0QAY9YOALGO+mR2aZqKWmfMG+HbgNjCevwBE/xFdnCO0vh/SZV7cE3llwQ86gQcjGYAEYNkkbXPDQl7laSIrl5kFJWuYUOKpyrAEHotADkQkmKd8H6pDUWwbDl7EN64MwaNklmHTZ/jEiqsZpf2TiBQTzDNq8nRDmfJt6aeIRnPfc8iu3Wo1vJlqmW254C5/SeBPKOUQ1SXz8DtLSZ6EujbB3Ey7lw6PmXy2Yh4so5eCf0kIXHYd3jbuZFbubTfvP8Yj4tMJZfnaHzBKUVonL9Q2mpZtIkFobPgAAAABJRU5ErkJggg=="
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

            # def RunScript(self, Curve, Axis, CP):
            #     try:
            #         Sort_Curve = gd[object]()
            #         # 判断输入的列表是否都为空
            #         structure_tree = self.Params.Input[0].VolatileData
            #         temp_geo_list, geo_path = self.Branch_Route(structure_tree)
            #         length_list = [len(filter(None, _)) for _ in temp_geo_list]
            #
            #         bool_factor = any(length_list)
            #         re_mes = Message.RE_MES([bool_factor], ['Curve'])
            #         Sort_Curve = gd[object]()
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             # "---------------------------"
            #             origin_curve = filter(None, self.Branch_Route(structure_tree)[0][self.RunCount - 1])
            #             # "---------------------------"
            #             origin_path = self.Branch_Route(structure_tree)[1][self.RunCount - 1]
            #             if len(origin_curve) == 0:
            #                 Sort_Curve.AddRange([], GH_Path(tuple(origin_path)))
            #             else:
            #                 Axis = Axis.upper()
            #                 index_list = self._sort_by_xyz(filter(None, Curve), Axis, CP)
            #                 Sort_Curve.AddRange([origin_curve[_] for _ in index_list], GH_Path(tuple(origin_path)))
            #         return Sort_Curve
            #     finally:
            #         self.Message = "Sort Curve"


        # 均分曲线
        class Equipartition_Curve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Equipartition Curve", "W43",
                                                                   """equally divide curve""",
                                                                   "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("49378bcc-dac0-4845-a0dc-f934d8eeb669")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "please input a curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Espacement", "E", "Espacement（300 by default）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(300))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "HT_Length", "HT", "the distance from the last point to the curve is more than（by default 20）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(20))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Offset", "O", "The position of the offset starting point on the curve（0 by default）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Style", "S", "style of equally divide default：2（0：from the start point，1：from the end point，2：from the center point）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(2))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "PointAtCurve", "P", "Points on the curve")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Parameter", "t", "The length on the curve")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANTSURBVEhL3ZRpSFRRFMdfiy0KpUa0oknjLE6OhahlzTjN5oxLZjUpmRE1pVYqoWngOM8FR7MFVAijxDYKopIsiigCC0yTnOZDRFrkCpmSaR+syHO693UhqXQM/NQPHu/+zzn3nnvuO/dx/y9QKAtDPmAWkxMCNkkS8P4qJl2D18wzyKQHUCJayEwTAjZxFfBiC5Ouwf3BbmRSPfAB3sw0IST2OK2CSdfgGSHBrUkn4KUnyBElMjk5wCq+jjw3nckJgXySwCqKYdI1I3mBOiiT9X63BaQz07gM5io0UCZ9D7z8Ttfh5XOZeXxEEW/SnNk7EU8tRSzRoN70tJK5BEhn+UCx2I+O3UK/BtUdOPJViC0Pw+Qt95/7hrxbLAT+DWVkU9z6mA+Yk1gLoyVeHTV7rf0b44dxg6GpmIXQD5pLzttKxyE6x+P4eCcO5ik676VZXqniBlFpcrSu3db4ZyVabfMCdZRzQBP7FjXGZjPYvU/LNnbKVaaX/fq4TlTqmzQ0DnhZDtjnpXIK8DNs7kC/iO6HIwX+x97xErVc034+2jyEKkPzJWHRsagMT6upc62+5TjVYJPW03eYrjUqMr4XI4yODnJA06BoWSaUc7tWqHrsUds+oue6oWgo8yiE0vlkAzhTbXrRZtzSh0pD46+21ZpeiLUxr0BtcvQtCe51x1pujtCmFaLZ1K+MbL4QbR5GH2VXPpziknqObuAV2tfdaqNjmCw6A4p8K0gnRQuxhsZQ3aZ2JJUPcn6wiNo4mfrtFf3Wz6iMfHaQajzq4yUkSP+ZICLO4ak2Od8rdF2jjZnbb99MOeQMjvqEKuOzauonl+wsuclGOqaE61pIdQOYlVBTx122ZK/md9dgbExDm9F4V1gQ7NIFZMIjeuGEGQSZ6qXJktCAI4Wh+KVoDaaY63FFeI+E+oCXXBybgGzR7UnGjm6sXIXcKC8tx2oxfsuX3Wde0orB7mRX6b9ftBv7UjPQLiEtKcW7qZZcZiYJRAFYGujFpAAUL76K54KQZrdi1SoEfqVQritI4jPkOcnkuCDv6wnl8q0cZCk8oFQeNOnfgk2SBwWyZCanHigQF//Tr/lfId1VQo51D5NTD7mAFeSYUpicerBQYiYVhDP538NxPwBu3IAJ5JI8FgAAAABJRU5ErkJggg=="
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

            # 根据树分支和路径还原树形
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [i for i in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 处理操作
            def Curve_Offset(self, Curve_Data):
                Curve = Curve_Data[0]
                Espacement, HT_Length, Offset, Style = Curve_Data[1]
                # 可以添加一个选择方式，从中间、头尾开始位置
                C_Length = Curve.GetLength()  # 曲线总长
                if Style == 0:  # 从曲线 开始点(Left) + 间隔 + 起始点偏移 开始
                    Left = HT_Length + Offset
                    Right = -1
                elif Style == 1:  # 从曲线 结束点(Right) - 间隔 - 结束点偏移 开始
                    Left = C_Length + 1
                    Right = C_Length - HT_Length - Offset
                else:  # 从曲线中心点(C_Center) 开始
                    C_Center = C_Length / 2 - Offset
                    Left = C_Center
                    Right = C_Center - Espacement

                # 定位点长度位置
                Parameter = []
                # 定位点在曲线的位置
                PointAtCurve = []

                if Espacement != 0:
                    # 根据长度去判断每次偏移 Espacement
                    while Left <= C_Length - HT_Length or Right >= 0 + HT_Length:
                        # ± HT_Length 确保数据不在指定边缘范围内
                        if 0 + HT_Length <= Left <= C_Length - HT_Length:
                            Parameter.append(Left / C_Length)
                        if 0 + HT_Length <= Right <= C_Length - HT_Length:
                            Parameter.append(Right / C_Length)
                        Left += Espacement
                        Right -= Espacement

                    if Style != 0 and Style != 1:
                        Parameter.sort()

                    # 得到在线上的这个长度
                    for i in Parameter:
                        PointAtCurve.append(Curve.PointAtLength(i * C_Length))
                else:
                    PointAtCurve, Parameter = ([None] for _ in range(2))
                return PointAtCurve, Parameter

            # 数据匹配
            def Data_Matching(self, Data, Matching_Data):
                return Matching_Data * len(Data)

            # Curve 多进程
            def Curve_Multiprocess(self, Combined_Data):
                Curve_list = list(Combined_Data[0])
                # 确保有数据
                if not Curve_list == []:
                    #            return [[], []], [[], []]

                    Data = [Combined_Data[1]]
                    Data = self.Data_Matching(Curve_list, Data)

                    PointAtCurve, Parameter = list(zip(*ghp.run(self.Curve_Offset, zip(Curve_list, Data))))
                    # （值，None）
                    PointAtCurve = self.split_tree(PointAtCurve, Combined_Data[2])
                    Parameter = self.split_tree(Parameter, Combined_Data[2])
                else:
                    PointAtCurve = self.split_tree([[]], Combined_Data[2])
                    Parameter = self.split_tree([[]], Combined_Data[2])
                return PointAtCurve, Parameter

            # 处理操作
            def Processing_Operations(self, Curve, tree_path, Espacement, HT_Length, Offset, Style):
                # 数据匹配
                Curve_Tree = [list(i) for i in Curve.Branches]
                Curve_Tree = map(lambda x: filter(None, x), Curve_Tree)
                Data = [(Espacement, HT_Length, Offset, Style)]
                Data = self.Data_Matching(Curve_Tree, Data)
                # 进入多进程
                PointAtCurve, Parameter = zip(*ghp.run(self.Curve_Multiprocess, zip(Curve_Tree, Data, tree_path)))
                PointAtCurve = self.format_tree(PointAtCurve)
                Parameter = self.format_tree(Parameter)
                return PointAtCurve, Parameter

            def RunScript(self, Curve, Espacement, HT_Length, Offset, Style):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    PointAtCurve, Parameter = (gd[object]() for _ in range(2))
                    re_mes = Message.RE_MES([Curve], ['Curve'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve_path = self.Branch_Route(Curve)[1]
                        PointAtCurve, Parameter = self.Processing_Operations(Curve, curve_path, abs(Espacement),
                                                                             HT_Length, Offset, Style)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    # 还原树形结构

                    #            PointAtCurve = self.format_tree(PointAtCurve)
                    #            Parameter = self.format_tree(Parameter)
                    return PointAtCurve, Parameter
                finally:
                    self.Message = 'curve divide equally'


        # 统一曲线方向
        class Filp_Curve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Filp Curve", "W33", """Unify the direction of the curve。
                           if input curve,then keeps all curves in the same direction
                           input truth value means that the curve with the highest center point is the uniform direction
                           or else the curve with the lowest center point""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3159660c-6476-4c5f-9c05-e5cd4924ace1")

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
                self.SetUpParam(p, "Curves", "C", "List of curves that need to be reversed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Direction", "G", "The true value is the curve with the highest center point, and the false value is opposite（ture by default）\
                                   If it is a curve, use the curve to unify the direction\
                                   ")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "The curve after reversal")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Flag", "F", "flip or not")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANZSURBVEhL3ZVLaBNRFIZbbFVEFB+LIqLgAzWZpGI0Wm3mzp1MZu7MJH0aC4qPhW5072MpRRduFFe6EAUXiguXKqLUB2mbyeTRJK1aH1Xro5ZKLSKihV7PhIO0JrZYXflByMx/zj333nPOvVP2f+Lz+Srdbvc6j8fjg98KlMfBy4NmdoVspv0BLVFPjexRoiWOM9Y7Cx0mB4K3eAThy3qvN+4VhGMoI7yc6PYB2ew5S1iylzV94ErkGXf+A6rVgk6TAxNcFNzuO7CTxWWcl6OMwASkba7zRDVrjWw+aRSZPaA1vuNEs64XXKZCcLliXo/nnSAI9/1+/zyUSxIIxeRg+DGXjK4RSU+NBYPxRWgqDeR8Aaz+W3V1tQo7mI/yb5H0zCNI1ZAYbPdIZn4vUe0wmkoDE2yA/KcJIbNR+i2QmlYjOgKpSex33hm7MSug23JNKCZQllhZcPoVCFzBi/I+EWLEq2Dlp43twxA8OSHvPp9dSfXMV5j0KkpTQ4x8lcS6goRljkosfZsaOeiaQQ6TXHa5rs1EtwKSajXrzUNOwXejVBpnIBTuIDW6ErLZzZ0uCdW/dIIOg3YVAijoOgFRi3eC/XM4bM9BqRhRubdaNvJ5fftHJ+BboqfOUb1rJ410u6PR/IQVj6dWeUBY8yAnavwESsWoavtCana/ViJPOdVTe6LRazPQNCl+dmMe7LQPxn6qNbMLUC5GVDuvsKYBHlBiGkpTQpi9hRr5nDNOVDrqUC6GmJagNrzhAa3jAkolIZH8KpGlG+FgnZJYKqs1vuVyuGc0oLbvQpfSiJp1Sal7zrcpD5eh9JMatW0tXGpnJCPT7/g4RQ9GeuEEZ55JRu5kDb27HF1LQ8L2YmrmR0Wt8yZKPwlonYecmoTqX0HR0xasvFUysiY1uicPOh5RTdDChaXbDc6FhjLcNR37Ct1kZmMyS3pR/nMI6ZtN9PjGWpZyicyKONpWJbkkGO79DqvN+HznKwuOf4sL+pywRFJkiSNEs88rdS/GCGtbiuaCHR+nj3OJaU3voTMecajJfTFkRYieC4ta8jDsbhO6TR8SsgRq5jgcee5cE2pDP3RLNi5q9g742FSg298hqlYyVN8Hk2RvUZZWUf53UCO5XDKebMbXaVJW9gPecWAFuAsO8AAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            # 根据树分支和路径还原树形
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

            # 曲线高度排序
            def Curve_Height(self, Curve_Bool):

                Curve_list = Curve_Bool[0]
                Curve_Height = [Curve.PointAtLength(Curve.GetLength()) for Curve in Curve_list]  # 曲线方法
                Max_Value = 0  # 第一个最大值下标
                Min_Value = 0  # 第一个最大值下标
                for Value in range(1, len(Curve_Height)):
                    if Curve_Height[Max_Value].Z < Curve_Height[Value].Z:
                        Max_Value = Value
                    if Curve_Height[Min_Value].Z > Curve_Height[Value].Z:
                        Min_Value = Value
                return Curve_list[Max_Value] if Curve_Bool[1] else Curve_list[Min_Value]

            # 曲线反转
            def Curve_Flip(self, Curve_FlipCurve):
                Curve_list = Curve_FlipCurve[0]  # 曲线数据
                Tangent = Curve_FlipCurve[1].TangentAt(0.5)  # 指导曲线切向量
                Flag = []  # 是否反转
                # 循环判断向量是否一致，不一致互换
                for i in range(len(Curve_list)):
                    # 99.0001度之内的都算平行
                    Parallel = Tangent.IsParallelTo(Curve_list[i].TangentAt(0.5), 99.0001)
                    # Parallel 1向量是平行的，0向量不平行或至少有一个向量为零，-1向量是反并行的。
                    if Parallel != 1:
                        Flag.append(True)
                        Curve_list[i].Reverse()
                    else:
                        Flag.append(False)
                return Curve_list, Flag

            def do_main(self, tuple_data):
                curve_list, guide_list, origin_path = tuple_data
                if len(curve_list) != 0:
                    ref_bool = tuple_data[1][0]
                    if type(ref_bool) is bool:
                        temp_curve = self.Curve_Height(tuple_data[0: 2])
                        res_curve_list, bool_list = zip(*ghp.run(self.Curve_Flip, zip([curve_list], [temp_curve])))
                    else:
                        new_curve_list = [copy.deepcopy(curve_list) for _ in range(len(guide_list))]
                        temp_curve_list, temp_bool_list = zip(
                            *ghp.run(self.Curve_Flip, zip(new_curve_list, guide_list)))
                        res_curve_list = list(chain(*temp_curve_list))
                        bool_list = list(chain(*temp_bool_list))
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_curve_list, bool_list])
                else:
                    # "---------------------------"
                    res_curve_list, bool_list = [[]], [[]]
                    # "---------------------------"
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_curve_list, bool_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curve, Guide):
                try:
                    Curve_Tree, Flag_Tree = gd[object](), gd[object]()
                    re_mes = Message.RE_MES([Curve], ['C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve_trunk, curve_path = self.Branch_Route(Curve)
                        curve_trunk = map(lambda x: filter(None, x), curve_trunk)
                        #                curve_trunk = [_ for _ in curve_trunk if len(_)<0]

                        guide_trunk, guide_path = self.Branch_Route(Guide)

                        len_c, len_g = len(curve_trunk), len(guide_trunk)

                        if len_c > len_g:
                            new_curve_trunk = curve_trunk
                            new_guide_trunk = guide_trunk + [guide_trunk[-1]] * abs(len_c - len_g)
                            curve_path = curve_path
                        elif len_c < len_g:
                            new_curve_trunk = curve_trunk + [curve_trunk[-1]] * abs(len_g - len_c)
                            new_guide_trunk = guide_trunk
                            curve_path = guide_path
                        else:
                            new_curve_trunk = curve_trunk
                            new_guide_trunk = guide_trunk
                            curve_path = curve_path

                        zip_list = zip(new_curve_trunk, new_guide_trunk, curve_path)
                        #                print curve_trunk
                        #                if len(curve_trunk)>0:
                        iter_ungroup_data = zip(*ghp.run(self.do_main, zip_list))
                        Curve_Tree, Flag_Tree = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                        iter_ungroup_data)
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                    return Curve_Tree, Flag_Tree
                finally:
                    self.Message = 'Uniform curve direction'


        # 获取多折线角平分线
        class AngularBisector(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_AngularBisector", "W51",
                                                                   """The Angle bisector is calculated from the Angle of polyline""", "Scavenger",
                                                                   "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("93af8e00-3e7d-4bbe-ae91-ad43f6f3e73f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Polyline", "POL", "polyline（No radians）；curve（radians）、lines and arcs are not allowed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "number of angular bisector；the number is（Count - 1）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(2))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Angular_Bisector", "BC", "Output angular bisector")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN4SURBVEhLvZVrSBRRFMeXggqioiKKMFNzd8vKClLK2pnVcXbu7Lqru1oJvVCKoMiM+qS4a2lqb6OkF0ViDysqiApJkKQ+5M5u9jCs6CWVZlZiUZjYPZ27XpTo5Ub0g8vM/Ofcc+65c+4Z3X9nzpzTo/jtv8ekaKvk5KZ3Jos3jkv/FoH49tsWfgTR4s3gUtBQt7GYug1nwTNxCJf6EIm2j6S2gVn1L+JSUECePh/2TQcM0AUlESO43AfLgLjeAG5RKpf6Dc0zZsGuaUC3TP5CPXqBy98jKNoh4moFDOTkUr+guYalsH0qQPEUoDmRdi7/iKj4jhDXaxAUr4NLf4Q5ZI5ZABaIyz8HAxxTXC2A1WTj0m+huXqBFk7uCmwNbhGXfw2u/LjibAGzclvh0i+BHP1MdN4Be9C52+Dh8u/Bb3BKcTaDoGoyl34KzY2cRAuMLbAXKybPUMrlPyMovrOK8xWIiXWzufQDsDFqHN1kfNxTjsZyLvcPUfGfl5OfQ7x6Lx9LdQKXe6GeyOHovB7KooF6DBe53H8Eol2Q7A+BZRFvvfvZrN4ucDhuDGPv6FoymOYbawPO2dUTNSgwKRjwJF+Skh7gOdCqROLvtqa9h7nK/SdxiX4H3RRyGspwWzADlgmfEhwYoIpt0Xy1zsCGiTRciCVNUJ2VBbBzPNCikHr2Dbh58ODKq+XkZ5Bg0WK5pKtf76yFnaHwYbME2WlH13H578AMahIdTyBGbpjJnqk7Ig92hEFnvr4z03Wle5bc1D4vyRcaMP4bMECtZH8MuqF0LC0YkxE4oYXGrk+F4bETTS9LbAvaQbDcrODmwYMH7Xp04nNas2bZNigOw+YVxVpAoHlJUvVos/VOR7z13leTfDM8MCFYZkmNN3KWnAQoMgLdGtJJiwZ+1/QEi9dtZVkQrYhLwWGzXfNB4QzsjOOhenXGmZFxHXNNRLOIFj9Bp1aReLOlpEbArWzGkSYS3wIs53Qz8S3GQ7rUTLTlAvFmJiQ9WCGQWzHcbR9mte7y1Q0lcHhlKcSor0BOacZDx0YLsC5rSXkBkv0RsFJmPyaSykYbqIHxtnfY0zux5WttHg8M4K57iMPqmSG3Vk6Xnp5jfQlXWIkrPYHGFXhfjj+io5jJYVHRDuLzAVx1GXbgvWhTija78boD329LsDUWi6ovRafT6b4B/23A/eqzbv4AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.eq_part_num = None
                self.tol = sc.doc.ModelAbsoluteTolerance

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def split_tree(self, tree_data, tree_path):
                new_tree = ght.list_to_tree(tree_data, True, tree_path)
                result_data, result_path = self.Branch_Route(new_tree)
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

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

            def _angular_bisector(self, double_curves):
                first_curve, sce_curve = double_curves

                re_sorted = double_curves[::-1] if first_curve.GetLength() < sce_curve.GetLength() else double_curves
                new_first_curve, new_sce_cuvre = re_sorted
                first_line_start_pt, sce_line_strat_pt = [_.PointAtStart for _ in re_sorted]
                intersection_pt = \
                    rg.Intersect.Intersection.CurveCurve(new_first_curve, new_sce_cuvre, self.tol, self.tol)[0].PointA
                if first_line_start_pt.DistanceTo(intersection_pt) >= self.tol:
                    new_first_curve.Reverse()

                if sce_line_strat_pt.DistanceTo(intersection_pt) >= self.tol:
                    new_sce_cuvre.Reverse()

                new_first_line = rg.Line(new_first_curve.PointAtStart, new_first_curve.PointAtEnd)
                new_first_vec = new_first_line.Direction

                new_sce_line = rg.Line(new_sce_cuvre.PointAtStart, new_sce_cuvre.PointAtEnd)
                new_sce_vec = new_sce_line.Direction

                base_plane = rg.Plane(intersection_pt, new_first_vec, new_sce_vec)
                angle = rg.Vector3d.VectorAngle(new_first_vec, new_sce_vec, base_plane)

                base_arc = rg.Arc(base_plane, base_plane.Origin, new_sce_cuvre.GetLength(), angle)
                base_curve = base_arc.ToNurbsCurve()
                base_curve.Domain = rg.Interval(0, 1)

                t_list = [_ for _ in base_curve.DivideByCount(self.eq_part_num, True)][1: -1]
                bisector_list = [rg.Line(intersection_pt, base_curve.PointAt(_)) for _ in t_list]

                base_line_format = rg.Line(new_first_line.To, new_sce_line.To)

                intersection_pt_array = []
                for single_bis in bisector_list:
                    intersection_format_t = rg.Intersect.Intersection.LineLine(single_bis, base_line_format)[-1]
                    intersection_pt_array.append(base_line_format.PointAt(intersection_format_t))

                bisector_list_format = [rg.Line(intersection_pt, _) for _ in intersection_pt_array]
                return bisector_list_format

            def _get_result(self, tuple_data):
                cur_list, origin_path = tuple_data
                temp_res_lines = []
                for single_cur in cur_list:
                    single_cur.Domain = rg.Interval(0, 1)
                    single_curvature = [_ for _ in single_cur.CurvatureAt(self.tol)]
                    if sum(single_curvature) == 0:
                        sin_crv_list = single_cur.DuplicateSegments()
                        temp_ensemble = zip(sin_crv_list, sin_crv_list[1:] + sin_crv_list[:1])
                        ensemble_curves = temp_ensemble if single_cur.IsClosed else temp_ensemble[0: -1]
                        temp_res_lines.append(map(self._angular_bisector, ensemble_curves))
                    else:
                        temp_res_lines.append([[None]])
                ungroup_data = self.split_tree(temp_res_lines, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Polyline, Count):
                try:
                    Count = Count if Count != 0 else 1

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Angular_Bisector = gd[object]()
                    self.eq_part_num = abs(Count)
                    poly_trunk_list, poly_trunk_path = self.Branch_Route(Polyline)
                    poly_trunk_list = map(lambda x: filter(None, x), poly_trunk_list)

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        Message.message2(self, 'The Polyline-terminal cannot be empty！')
                        return gd[object]()

                    re_mes = Message.RE_MES([Polyline], ['Polyline'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return []
                    else:
                        iter_ungroup_data = ghp.run(self._get_result, zip(poly_trunk_list, poly_trunk_path))
                        Angular_Bisector = self.format_tree(iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Angular_Bisector
                finally:
                    self.Message = 'Polyline angular bisector'


        # 点与封闭曲线的关系
        class PtsCurveRelationship(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PtsCurveRelationship", "W4", """Determines the relationship between the selected point and the closed curve""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d0656632-dda1-41b1-8213-69b8fc78e6d1")

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
                self.SetUpParam(p, "Points", "P", "The selected set of points")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Closed curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tol", "T", "Accuracy (distance from point to curve)")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Relationship", "R", "Relation between points and closed curves（0 = outside，1=On the curve，2=internal）")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "In_Curve_Index", "ICI", "subscript of the point on the closed curve in the original list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Outside_Curve_Index", "OCI", "subscript of the point outside the closed curve in the original list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Inside_Curve_Index", "ISCI", "subscript of the point inside the closed curve in the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQRSURBVEhLtZR7bFNVHMcvOmc3OoooKI5/iFLMxCVb2atr72lvH/ferXs4N/GRyB8mIDISnJY/dGESjdkiyiBDZLoNFSIao5s6N7KUdqDdo7fcMvfIxsYWcDGAj4H4KMRz+Z3LsVq2diTET3LS8/39zv2dnt/5/Q7zf4AntZvwT0t34r8YPTUxjKIwOhgLqLwl8LSmBf+q/RuHmTXXDb8x6cpF7Qw49qkGClqvaBCajBrnx1NXXf05saCmZn9yxA7r6CcRMGZS6BTEZSYDz6Rcxmc17xPNCv1ZFnGgG4khH8sHIiPfIftamjbMHPNuUF5wv+PPRkM+VpC81oKTPosodyGn/0E14FxAeu6CcRuZQ7DD8JE7z/HdsugRWib3ZlonBvVVdXU196ehQW1a2qeJCHnvQUKwAQmBnWqw+cjjQoeM9mAxlTGxiMHHONdIa0XFYKKZD2wEvYu64lP2xNcfCMXHHyXzbORdQfKsOm4A8cFXba6xsK20727EB55DgvQWdcUG0nSfp7PsohwwbIO6WuwomVJYvn8Pdc/CaGxVL9NoC1Xl2eX5N4DbX9Le9uSZo0dsVaDu5FxDjazQp54mHiWPd20pXddZR2V8WKG3JYsbmDfof/F0ODo6vyocittL+BKD4AQrs9BwE1REOTVHcDhCC63iwN65fO2txZ+0flbmj7kBBF6lXNUp+BemJ4Mbasy3h8qoKwJXKKfai04piJeaqClCvl2uNDnlN6gk8ZLo9Dqwsw6f03wBTfeSgR1pNDlm/0uCme9ebnBJyWQO9a+BfmHhN8HslLaaHLLaB9CwzfiC9kf8J7OS6FlAox1EolSKkJKABPkwdOvz1BUF6ww8U/IUVsxiL2cWAuvNfPCfDdrw+ZQr8NitVhfeCNmAFYJFueX+JIsYCoP+iLqiICnjikZfzHX6l6QbxzdlmMbeJHbIRiKk6F510VyoJ6AXmS18s8hgkO5QHXGo3l77yraX6xuojM+anIkDesN0CZURTMKJpXa7pKMyiuMey7D3CDdKZWxImdXXuzua39tYSU0qpEShesLwJHQTTTazuUZ3WQuDBqI/bH52z7v7Kj8m87jABlpflz3c4zV+SU0q5MJZXnobUrdF1YJkKqy4BCXb7yb6IcOZykdyJ2vJfF52vPZ62+7dW5+mMiZJK35PpVMo3/7NsHk9lfFJz5s4sJad2m4S+/QmMRQ1smzD+urq2ofHv19dHTiWk5NpHXuArGOFE82Qwps7AeQ3DZ6EDkvBSQ88yVEDnhFPlXvvt1JPuQJ3dXotGvFYCgY8UM6fZ5qnltMQ/wI5Xww1u4jKmwZfYXJJ91OpAjoB/6BpJ51MikU14lFdA55O/oNcrmq4BUhzKedSFHx64QWIdzvDMMw1hDbSu8rKyGEAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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

            def relationship_point_curve(self, pts, curve):
                relat_list, in_curve_index, outside_curve_index, inside_curve_index = ([] for _ in range(4))
                for pt_index, pt in enumerate(pts):
                    if pt is not None:
                        t = curve.ClosestPoint(pt)[1]
                        test_pt = curve.PointAt(t)
                        distance = test_pt.DistanceTo(pt)
                        if distance < self.tol:
                            in_curve_index.append(pt_index)
                            relat_list.append(1)
                        else:
                            # "--------------------------------"
                            cfactor, c_Plane = curve.TryGetPlane()
                            c_Plane = c_Plane if cfactor else rg.Plane.WorldXY
                            if curve.Contains(pt, c_Plane) == rg.PointContainment.Inside:
                                # "--------------------------------"
                                inside_curve_index.append(pt_index)
                                relat_list.append(2)
                            else:
                                outside_curve_index.append(pt_index)
                                relat_list.append(0)
                    else:
                        relat_list.append(None)

                return relat_list, in_curve_index, outside_curve_index, inside_curve_index

            def RunScript(self, Points, Curve, Tol):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index = (gd[object]() for _ in range(4))
                    self.tol = Tol

                    structure_tree, structure_tree1 = self.Params.Input[0].VolatileData, self.Params.Input[1].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    temp_geo_list1 = [list(i) for i in structure_tree1.Branches]
                    if len(temp_geo_list) < 1 or len(temp_geo_list1) < 1:
                        Message.message2(self, 'The P or C-terminal cannot be empty！')
                        return gd[object](), gd[object](), gd[object](), gd[object]()
                    re_mes = Message.RE_MES([Points, Curve], ['Points', 'Curve'])
                    if len(re_mes) > 0:
                        Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index = [], [], [], []
                    else:
                        Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index = self.relationship_point_curve(
                            Points, Curve)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index
                finally:
                    self.Message = 'Points and Closed Curves'


        # 线与指定向量的关系
        class CurveVectorParallel(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CurveVectorParallel", "W24", """Determine if the line is parallel to the top vector（include of antiparallel）""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6edc63ab-a243-4a98-a24e-f057b0888cff")

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
                self.SetUpParam(p, "Curve", "C", "The set of curves to be judged")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Specified vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "Angle（Degrees）tolerance")
                Tolerance = sc.doc.ModelAngleToleranceDegrees
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve1", "C1", "A set of line segments parallel to a vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve2", "C2", "Set of line not parallel to a vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index1", "I1", "The subscript of a line parallel to a vector in the original set")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index2", "I2", "The subscript of a line not parallel to a vector in the original set")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMgSURBVEhL1ZRdSBRRFMenB6EgsB6EohIqdcc1zbTIj925s+u2c2d1sxTDpyAEw5IoFcXSVVcr7QNT6cEIQ7EQJJ8ifAjURNPd2dldv9KVJZDEqA1MAiNtbmfzhvRhge6LPzjcvWfO+Z9z7sxdZlOgVLBxSmHofroNPIpF9UqpVS8o18IOUldggQkySGM0UarZSaU0LIS6A4tSFv6C3DtEFCvrJiUHQql7la9VMceV2shLSoVqHRaeD1O0k5pIQmrVMIlqjlSpsghhtlB5hlm2sJ2k5Qjxj/pfa/qL3VITUh5BiEW18ttfqCJsL5VnGF8Re/rd1ei2uQL1P81XrG77WMz+ZpGtC6XR3cQKwjdYslgZtTh9Oa6I5MYHUfmNs1SXWU8aov3is3Je4jHqDgxfmhtZcjeJLFlVH0byE1nqDhzKndgWUh86rzQxEdT1Kxr8MkSXNmFEopTGCY4MhG3ZnNF+lsdyjlawXUTYcYXDjhIk2Ms5LFUjLNVxgr0e9vfB/6Asu2E579Sjt0dPjLcazN4urdGWSaVX4IThMylmjwcSJsDGOcHmRoIkwzoMxYZh7QfBXg7busGeIWx/CvsOiHkIzxoj9DPFar23kDNKFoPZUw0xZr15MkaDh9S0xPpISBjcphOcUbzoyOSwbOGx4wlMN8iL8kyKefoTNH6bhq6NwSAF64xDhyExCwmOSk6UOuFYnCA2h7C8gETZB0c4BWs3CNfz2JXDi85krWDfzTBk9aL9BBlt5yCoCYmOXujsDYjM/xDC8iwk2kCoHYmuUp3gPsmZRiMRGttOU9dGKwyd15s9HdCZFYQJL7oGoEMrb5LTNVhWG7K8wTR0fWix3ZhinmrjTa4REPd3Os1j53P4iqr9X1ayQfrzz2u9QMchfKpL0GHXdSjWh0SnDwougb2HqXqgYA0nyqI+dXAPTdkY8blSkB47YnR4JBcmfIyw0wvFvoHBUcozYF1wdwq0JjlJk9q/k6ZtDGQa28WJbhGK3AQbgBf/WZ/22v/uFLiIo1pj3z4aGhgQ6tmKTM5Y3jR6AS5fM0p37qCPNj0M8x3X08+ThSAtrQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.angle = None

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

            def unified_direction(self, tuple_data):
                curve, origin_curv, guide_vector, origin_path = tuple_data
                guide_vector = guide_vector[0]
                curve_parallel, curve_not_parallel, parallel_index, not_parallel_index = ([] for _ in range(4))
                if curve:
                    for curve_index, single_curve in enumerate(curve):
                        if not single_curve:
                            continue
                        else:
                            single_curve = single_curve.ToNurbsCurve()
                            single_vector = single_curve.TangentAtStart
                            radian = rg.Vector3d.VectorAngle(single_vector, guide_vector)
                            if radian > math.pi / 2:
                                single_curve.Reverse()
                            factor_radian = rg.Vector3d.VectorAngle(single_curve.TangentAtStart, guide_vector)
                            factor_angle = math.degrees(factor_radian)
                            if factor_angle < self.angle:
                                curve_parallel.append(origin_curv[curve_index])
                                parallel_index.append(curve_index)
                            else:
                                curve_not_parallel.append(origin_curv[curve_index])
                                not_parallel_index.append(curve_index)
                ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                   [curve_parallel, curve_not_parallel, parallel_index, not_parallel_index])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curve, Vector, Angle):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.angle = Angle
                    Curve1, Curve2, Index1, Index2 = (gd[object]() for _ in range(4))

                    re_mes = Message.RE_MES([Curve, Vector, Angle], ['Curve', 'Vector', 'Angle'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        tree_of_curve, curve_tree_path = self.Branch_Route(Curve)
                        tree_of_vector = self.Branch_Route(Vector)[0]

                        structure_tree = self.Params.Input[0].VolatileData
                        origin_pts = self.Branch_Route(structure_tree)[0]

                        c_len, v_len = len(tree_of_curve), len(tree_of_vector)
                        if c_len > v_len:
                            tree_of_vector = tree_of_vector + [tree_of_vector[-1]] * abs(c_len - v_len)
                        zip_list = zip(tree_of_curve, origin_pts, tree_of_vector, curve_tree_path)
                        iter_ungroup_data = zip(*ghp.run(self.unified_direction, zip_list))
                        Curve1, Curve2, Index1, Index2 = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                 iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Curve1, Curve2, Index1, Index2
                finally:
                    self.Message = 'Relationship between line and specified vector'


        # 创建中间线
        class TweenCurves(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TweenCurves", "W11", """Create multiple intermediate lines between the two curves""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1de545c0-4f66-4579-9992-9c45fdc9ef01")

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
                self.SetUpParam(p, "Curve1", "C1", "First curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve2", "C2", "Second curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Number", "N", "Number")
                Count = 1
                p.SetPersistentData(gk.Types.GH_Integer(Count))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "Intermediate line")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKjSURBVEhLzZVfSFNRHMelKFN0kiu1tGTEoDbZde7u3rt773b3N7VkFQW9WNhbD4VFSET0IFk9BIWIgSWJZKsgNUuD2T//FiEIQUQPVkT0UERUlIUmt++5niDn2q7mQx/4sP2+57Dfzj07Zyn/BS7/3cNysH+MV7qiDilSazIf5OjQwlDENW4VvD0tvHJrVArcV32bn6qccrM3Pd2SR6csIBmrVjBc0z5P6eMpwXv7GZK06YEFJj9/u00pG1GL+eazNNJFMayAJq1Kgo1tOCKHBtWcHH8ujZIyBFXqS3gOeuHfSBV9veN24WI9rZNihvthBL6Bv5sNwBI4C4Y/XyuHBlSDoSCbRrpZBHl4AZImU7AMxrA8Sww8+MG6r3fQYF744Df4Fa4hwZ9sYE5UBsNjKufpupKXt6mQxnNmCyQruaxVMViYU1VSoO+LiHPCeW48YeWONla+dpwO62YYkiazVkEx2NjGnfjgZs7dOSKFhl7QXDfbIGlwVKv04vJFPQ4xspfhm6tszoZSo1FcTYdiWQY/wVdapRd3aLhVCvZPCkr3hOi/o8rBAdXuukTOwOLpGTNogGQVbq2aAxkwM3ftDhMjtNQEKp6rNq4p3iZZIWkQ1ar5Yhda63lvz3e8XTqdzKAdkiaVWjUfTNZDTinYpxaaq8n9FAvZo/eQNKmG8R5lYsjRx+arDNu4h0axMJDcV6QJ+Tkeg+Tkk0etD2z6B4d0tYmW8ciCdfAjJI2I4/AhLIWJcXrao7zS/ZqWiSDfuhyeho/gZ3gAJsZqP7OL3DHrLDVhGukllb4mZYnT3TnoLR9VWVekbn3RSVeBeXe+oWBjtsFgyTYaw5l03j+RVuJqq8P/71vclj+d7o5J3tM1ISg9U6L/3ju5bHQlnReHlJRfaUG7tHobhpIAAAAASUVORK5CYII="
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

            def Tween_Cruve(self, c1, c2, n):
                curve = rg.Curve.CreateTweenCurves(c1, c2, n)
                return curve

            def RunScript(self, C1, C2, n):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    structure_tree, structure_tree1 = self.Params.Input[0].VolatileData, self.Params.Input[1].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    temp_geo_list1 = [list(i) for i in structure_tree1.Branches]
                    if len(temp_geo_list) < 1 or len(temp_geo_list1) < 1:
                        Message.message2(self, 'The Curve1 or Curve2-terminal cannot be empty！')
                        return gd[object]()

                    re_mes = Message.RE_MES([C1, C2], ['C1', 'C2'])
                    if len(re_mes) > 0:
                        return []
                    else:
                        return self.Tween_Cruve(C1, C2, n)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'create Intermediate line'


        # 平面修剪曲线
        class PlaneTrimCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PlaneTrimCurve", "W14", """Remove the curved section on one side of the plane""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("2b209d3f-f0ad-473d-aab5-bfb7856934bd")

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
                self.SetUpParam(p, "Curve", "C", "Curves to be trimmed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "trimming the flat")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Flip", "F", "flip the curve or not")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Trim_List", "T", "List of trimmed curves")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Parameters", "t", "Parameter values at points where the plane and curve intersect")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Intersected", "I", "if the plane trims curve，it is True，or else False")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMdSURBVEhLxZXtS1NRHMdPaYtpJfVGIQmiXplZsJ7Q3H2Yurt772Y+7EU6MqKMCiqR6Em5reyFaIFZ2IMQIT5N1DG3dGkucyq650cjemPQq/6Hu86Zh4XU5k2QPnDhfH/nnPs95/5+51zwX9GbQJowAfZgmZJbTrATN6VjMullHVaqEMukPJnPlbdPFvBYSsdkEmRD5raTWCbFYhEy+q0t5VhKBxn0mY2SDPrGHuqwlE4sBrYM2YRjWCZlwwZ1dY6crp42Esuk/JMBxYWO0FzkGakJTqt4z2fDpUkPwYTNNBsx4CF/8DeDPL1JplC4t2EJAMEEcmk2/I7mlhcoPnqHUvsO1dT07n7+tl2lZEJaio+MUFxkluaCFXhKAmQw8N6oxRKQmsA1UuOdJdhwzmpA7eJINviFZkP38/RhWTwIgTnYOmptVmAJSCaiItnIR2hkVXGREhyO029r4pXqaCXcvZNiwxaC8+fjLrj60qV8omz+IJYJUBUN2O4WfReB/KsItqMYSrxav3gemnyg2KCDYHy9pbqlvvqb4/5C+pv1ROGK9HJ1OIR0s6+6NiDuKHfixyPKdT9FcBz1o1VSbKiSrXKd7bY2tq6IoBQuhpiLyc8silkVc2IWHX9RKkatwlHcTMnop9tatFO7mJ3pjoEMFEM63pmMasPM/vbO1+teAfEkW1oSSUYUq3ycQvEjbrQGml7Ihkl6jL6vivfO1NZPumGZTsPkPaW1wQI8bA3IoN8mxBeC5pOsb4xQuywK3r3WgGT91+HLAzQXbVNqAocbGgblPcMtp04z3jxYpk0w7lTx0SGSC6nxlASoTJVly/WwRKME62nC4VWKePc+UuOzkRq/nWJCB3AYVow+bdhijCcUQRBCOsVFz8HdjFNceJrQ+F4Qat+DEp375eVGe7i4LDqIzg8e/huCcV0hGe8jLBOkuuxoJlhAsqGr8OQbueqlGx1vOi/iLulIvU0RI1PNGtyUzqZf18hAyg/nFTQYHGvdiIFe1mWrLMIyKW12Q2b3xIUqLKUjCET6vSn5XiyTIpiArMWxa90f0yYAwC+VQFNkpV7euwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.flip = None
                self.factor = None

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

            def RunScript(self, Curve, Plane, Flip):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Trim_List, Parameters, Intersected = (gd[object]() for _ in range(3))
                    self.flip = Flip
                    self.factor = sc.doc.ModelAbsoluteTolerance

                    # "--------------------------------"
                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Curve_Abool_factor = any(length_list)
                    temp_geo_list = self.Branch_Route(self.Params.Input[1].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Plane_Abool_factor = any(length_list)
                    re_mes = Message.RE_MES([Curve_Abool_factor, Plane_Abool_factor], ['Curve', 'Plane'])

                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object]()
                    else:
                        if Curve and Plane:
                            curve_event = rg.Intersect.Intersection.CurvePlane(Curve, Plane, self.factor)
                            if not curve_event:
                                Intersected = False
                                Trim_List = Curve
                                Message.message2(self, 'The plane does not intersect the curve!')
                            else:
                                if self.flip:
                                    Curve.Reverse()
                                curve_event = curve_event[0]
                                Intersected = True
                                origin_dim = Curve.Domain
                                cut_off_point = curve_event.PointA
                                point_t = Curve.ClosestPoint(cut_off_point)[1]
                                Trim_List = Curve.Trim(rg.Interval(origin_dim[0], point_t)) if self.flip else Curve.Trim(rg.Interval(point_t, origin_dim[1]))
                                Parameters = point_t
                        else:
                            Trim_List, Parameters, Intersected = None, None, None
                    # "--------------------------------"

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Trim_List, Parameters, Intersected
                finally:
                    self.Message = 'Plane Trim Curve'


        # 统一曲线方向为逆时针
        class UnifyCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_UnifyCurve", "W34", """The uniform curve direction is counterclockwise""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("70c2cbf0-a13b-4813-8464-749781207056")

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
                self.SetUpParam(p, "Curve", "C", "Curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Reference plane")
                Origin_Plane = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(Origin_Plane))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Bool", "B", "True reversal，False unreversed")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                Curve, Bool = (gd[object]() for _ in range(2))
                self.Message = 'Uniform curve direction(anticlockwise)'
                if self.RunCount == 1:
                    def run_main(tuple):
                        curve, plane = tuple
                        if self.is_curve_closed(curve) is None:
                            Curve, Bool = None, None
                        elif self.is_curve_closed(curve):
                            Curve, Bool = self.unify_curve(curve, plane)
                        else:
                            Curve, Bool = None, None
                            Message.message2(self, "Curve required to be close!")
                        return Curve, Bool

                    def _do_main(tuple_data):
                        a_part_trunk, b_part_trunk, origin_path = tuple_data
                        new_list_data = list(b_part_trunk)
                        new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                        match_Curve, match_Plane = new_list_data

                        Curve, Plane = self.match_list(match_Curve, match_Plane)  # 将数据二次匹配列表里面的数据

                        trun_Curve = ghp.run(self._trun_object, Curve)  # 将引用数据转为Rhino内置数据
                        trun_Plane = ghp.run(self._trun_object, Plane)

                        zip_list = zip(trun_Curve, trun_Plane)
                        zip_ungroup_data = ghp.run(run_main, zip_list)  # 传入获取主方法中

                        Curve, Bool = zip(*zip_ungroup_data)

                        ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Curve, Bool])

                        Rhino.RhinoApp.Wait()
                        return ungroup_data

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
                        iter_ungroup_data = zip(*ghp.run(_do_main, zip_list))
                        Curve, Bool = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                        return Curve, Bool

                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData

                    j_list_1 = any([len(_i) for _i in self.Branch_Route(p0)[0]])
                    j_list_2 = any([len(_i) for _i in self.Branch_Route(p1)[0]])

                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['Curve', 'Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Curve, Bool = temp_by_match_tree(p0, p1)

                DA.SetDataTree(0, Curve)
                DA.SetDataTree(1, Bool)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQQSURBVEhL7ZV/bFNVFMefGsFFIhiDf0Dbh6/vVwtME2VgDNNs7cZ+w0Ib/UeMSzaD1kCy4Lr29XUt2wDdTzcToiwS/LWEZP5BTIxmkWAgMmZihEHnj23MZEHll8j66717PPftWrcMNRr+Mn6Sm/Z+7+k595x77i33P7eFVJMqm+2uWDoq15GAuJTJt4ebTdJGM65ehTfyAXrXg9mifmdElcDPAfE+ZvLvmX1FKkTnv0LnOjBDcrepyYeh3QXQlw9mTJkxWpRmEhRXMvN/RrJJ8pBWVxK684HsXb6LyVxalx7BLAYgrgL0Y1Yx9Vo2qrTP6m4HM/l7UnukCqNVzUKnC6b3FMS54iua6P+patNuksdMuJSuytkWtZfE1BQtH4kpabNF6UuFFYWZ3JpUUKo1W10EOtaC0SxaO1/lGR0Stl8HvurClLN2un9N9bmNljEyG3La0XEbZnXNyggzw/nb6aC6jpn8QTooPQ3tboBX0XlIaGAyxxd/9rijIgGOyu9hTc0PIJQdL2JLOX7BszCiahAzmYIuPLOIfOXSTvcytozOm5XnYT86P7AWICw8x+QcNu/IGF81iVlMwkNbE11MXkRGU16wui2iDIGPu2tODMkv0k4hbeoNIyQ9QzVHxfmP+LKzccsAsT81XLO68NMye/Gp95z+NAg1iXfY0gLMsDxMM0iGxBIm0QBSgEY1muXjdH6/58xye8nIqOBLgr1sLBfkd2yeLw5bQbZ9+2H9QbibyRztJDOmEizPjxM7+HuYzHH0dqJ4iWDnYGQn1UQxsNReMnpM8KXAUT7WbRnOw150sp9uQKj55pNNuy9a3WVoysvQT8sjH7SM5pPVpE7abqYmRZlEudNRMjJId2uvSLzFtByri04cELbfAL56zHJIItLntNRZTS62DOaTDsr5sM8NRJMnwOebOxyG3XvqkIBBHJXj73Mc3MFkC5vn9McrS8+TwZfqCkhMMPC2z4DuXsKWF2KGpdNzOxC9TMph85zsoSXhK8ePiVvGcw8eX/rl0TzPRPrrRk8n9CqQDSv9bGkxeNgN0LcejaQPmLQAm/dEKy2JozzxlaP8Qp1jy7kOfttlWOE5e5REVw1DhxvQRyEzX8z1JvUB0qLcxIcseVXnVzB5IRum/Hme6YllpTNwr/ci4TZfHuht8D9M9jmTpqZMn6l/NNdVtwRr+K51UcJynOhSQUaTNtNDwyaowHkt2b+kerLxscahnTuODAe2DhD9wV0kyg9CD81c7mFu/pyMJj4Jr+FtxrfI+sQzoRcHenBgYHgdRy8+2V0CQLeI3+kaaq0uyGjyBubmrzHCUjC7Vx0kEeUIXvk3sXX7MP1OU5fbjIisgy43EfzTMXSpHsezRszlzwTlJ9jP/1Nw3G/kbAy8W3WYlQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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


        # 删除重合曲线
        class RemoveOverlapCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RemoveOverlapCurve", "W12", """Delete overlapping lines and curves，Adjustable tolerances to delete similar overlapping curves""", "Scavenger", "B-Curve")
                return instance

            def __init__(self):
                pass

            def get_ComponentGuid(self):
                return System.Guid("3ec4ebc8-1395-44e4-a0d7-9085a1695575")

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
                self.SetUpParam(p, "Curve", "C", "Curve set to be deleted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Curves in the range will be treated as overlap curves")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "curve set after delete")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Delete overlap curve'
                Res_Curve = gd[object]()
                if self.RunCount == 1:
                    def do_main(tuple):  # 覆写主方法
                        orgin_path, orgin_curves = tuple
                        curves = filter(None, orgin_curves)
                        if len(curves) != 0:
                            _trun_curves = ghp.run(self._trun_object, curves)  # 将引用数据转为Rhino内置数据
                            curve_list = self.unify_curve_direction(_trun_curves[0], _trun_curves)  # 统一曲线方法
                            Res_Curve = self.remove_duplicate_lines(curve_list, self.tol)  # 得到结果线
                        else:
                            Res_Curve = []

                        ungroup_data = self.split_tree(Res_Curve, orgin_path)
                        return ungroup_data

                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.marshal.GetInput(DA, 1)
                    self.tol = p1

                    j_list = any([len(_i) for _i in self.Branch_Route(p0)[0]])

                    re_mes = Message.RE_MES([j_list], ['C'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        tunk_curves, tunk_path = self.Branch_Route(p0)
                        zip_list = zip(tunk_path, tunk_curves)
                        iter_ungroup_data = map(do_main, zip_list)
                        Res_Curve = self.format_tree(iter_ungroup_data)

                DA.SetDataTree(0, Res_Curve)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARxSURBVEhL3ZV7TFtVHMd5LD7GEJW4kfmHoobEGMxCYLb0vtrbe2/fLXMwnIvGTaMTQ2Jm4n8mJs74StQIapa5aXRO949xI6W3LS2P0ZYW+uBVpIwycStzmxgmloHt8XfuNZGVFv/3k3zSnn7vub/0nt85t+h/x9PgbrJp4fkDXOCtQdIdtRPiATn6b0guwBPswEP/DDdQAi6BV5S8b9K2ZwH1sEHkJV2/uVhXpXRFfrTgB83NZ25j9NFVtWE0qVD47pSjjbSDaPsObV+j7eJym9aHxjQh5CDEj+Q4L6+DCHzV2Jo+aGxeQhTv75CSPGwB58CUUtMzQJmm0Cnas9pLONNdtLdKumIjd4CT4BpYxZoSTt72MyKFUB0O8/EyiKrut32jtCRvtrPnUzG1H3WrxDY5zgsN4n9x/OCR7AO8bR5RQvCclORhJ5gpLt5ylrJcGDcKoWteyp0VCfF7OS6IF8RFytWGMTuINObRHVKShxQYoAzjLlY3ku4ixYyLcHrkqCC4A3EBnanlj+eEPSlECyFGSnIoBRfBQcI0OWgUhrO9TD9yko7TtfpYLWuMM4xh4gma9z0iXf0v9SAucNjyVLZVB11IC0HcYRtQgKi84lER1uBaGxdAEbofnaR7jtbrR1b0T15FQlMKac0JpBYij8lTJAwgLtDK2y53sOZpKBB5UEpy+AHMPN7w2QhlnUVfqvtRH+FIhwn7fQ3CkKAxTbxE66KvMbowboZiaYbMCRBVVNapWXPiOixyTP75VhpAVLbt4aTKnFh6hg+hiGYIuUnxWJFu+nardfFurXa4QsH77qUNQ1WsdabWuP/3e2BOBZgGPRrz9CHD3kXcpi/CeAP9YGaX8qsEaZlBx+iejJ9wr3xI9SqVupEUZ5mVHo3WcgFx1iTS772OONu8E+YcAVFRSUmr1poMqPWxG42WeDm+4XqkXr6rojZGWpPL+zn/r0F49iLRfaqoGZXSutBRxjD2BSWEPoXvH8Pn+xpT/G2VtrcF5l0Cf2rUnCfx+lDC0Cf4hrmcAdd2KU64leapbCftmQgxA8hBOnbLcUFwK+LFfcG8L/2K0HQZqflwo5SsAx8RV8AIY5wIUrqRhW5SvOQgHDNSujn4nMIFdmots8fVhnHEcdHtUrKOrSBeJDdtmYnyfGjeTYh/wu7tktLN+RbEBUo1xngnXiM4tqulZB243fAhN0nqo/2sPpw+RzpXRMIRktLNeRfEBapNLVdteOELdRDu40xtfUcXAf3fyXjSPqpn1UE7cndsLmoQF3gPDxj96DK8F5I07cWP/RbwwqBt5TUhlWVu8VnOnwnDKWonur+T44LgF9UUeBMs4yzxdvxOIAX/mzjMZQCETjo5RUCvf057VyLqALKrxCY5LogJxP/iNB4w+tg4Z52Ddh0m8Xg90jm0taz6ImlJrBmF4I0+yvOXSDjjcrwpZ0FchNLv+6UGNmKW0g3n3Q9vgId4W/JwnT78zo8qu0IkRUqONgW35tcgPlWLCNZVw7JDlX8DMHzplecfzsMAAAAASUVORK5CYII="
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

            def unify_curve_direction(self, reference_curve, curve_list):  # 统一曲线方向
                reference_start_point = reference_curve.PointAtStart
                reference_end_point = reference_curve.PointAtEnd

                # 计算参考曲线的方向向量
                reference_curve_vector = rg.Vector3d(reference_end_point - reference_start_point)

                # 创建一个存储处理后的曲线的列表
                unified_curves = []

                for curve in curve_list:
                    # 判断曲线是否闭合
                    if curve.IsClosed:
                        unified_curves.append(curve)
                    else:
                        # 获取曲线的起点和终点
                        start_point = curve.PointAtStart
                        end_point = curve.PointAtEnd

                        # 计算曲线的方向向量
                        curve_vector = rg.Vector3d(end_point - start_point)

                        # 判断曲线方向是否需要反转
                        if not curve_vector.IsTiny() and curve_vector * reference_curve_vector < 0:
                            curve.Reverse()

                        unified_curves.append(curve)

                return unified_curves

            def remove_duplicate_lines(self, lines, tolerance):
                unique_lines = []
                for line in lines:
                    is_duplicate = False
                    for unique_line in unique_lines:
                        if rs.Distance(line.PointAtStart, unique_line.PointAtStart) < tolerance and \
                                rs.Distance(line.PointAtEnd, unique_line.PointAtEnd) < tolerance:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        unique_lines.append(line)
                return unique_lines


        # 曲线相交位置打断曲线
        class IntersectionBreak(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_IntersectionBreak", "W23", """breaks the curve at the intersection position""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("822cddd6-919d-4ff4-b3f8-5a5f1e52a3cc")

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
                self.SetUpParam(p, "Curve", "C", "A set of intersecting curves")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance")
                Tolerance = 0.0001
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Res_Curve", "C", "breaks the curve at intersection position ")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPWSURBVEhL5ZR/TFtVFMcrmZvGTLP4Ky7OGKNu8kNsaCn99W7h/bj3vVeKcTAZZJlBN5Yt2XDg1CiBzKlLppPNhCUmSLLoFjf1jy0z4kiEMQdt33ttKaYWAoFkilGnGSpKWbmesksIGXQV//ST3PR+T+87995zzzmm/zc8778b4aCHyeWBpEADhwNHmVyAE/d6ipUodePgA8z073FIoXGOBI4xuQCH7+JqjujTcIvNzLQ0othxh+CLrXWp/WuKyi/dbjLRLJ+vM1v29tG84th6tuwGrELkfG7J8AkmlwYR7V2+dHAGkWCCI9ofFiF6JVZPxieb7JQoPf12KdwLJ+3gsHYaYa0N1rXk8UPNB7e8c8FoIL/VbzpeWSDElWJF55ASeiq7YmAlc30dh3BxLa/GPB4cUhEJV9qkgW2f1u6++sMrzhBRulucUrgdNvgcNuhERO+D0ETz+cGRD55vHP17/wZaVXZuqkjsTyDZoPAu03DgIuZ6cSoqTq0sFL+9dr/z5/RZUkBvFeW+CZsY3q2qPWsQiTzoUgOPIPT1CrZicSAzauGUfz1KBlcx05LYJQNCFzjLZGZAel5A2H+GybS4cWAXvMvETU89RyHpuxPinOSwfxMzpcUl+x/3KBEK6WxmpvSY+ehGjhgzgqDdxUw34xZIgJ/gFq8ynZ5Sb/dJF9a6mcwIp6i35pfEDSZvBEma1y6PXd5ZfiI+9ca66ZPb9v6SLwyeT6Wmh+jtELIjcMIDHAm+jGR9B8LGZiRrXvjfYxX6LaVqZ11jdWuyp25jznpHbDVzOw/CvQ9b8djePRUffTjWiOi5XTWnn+Rjn4DjLyGnL4HzCBTgEMy/h3EF5r/D7xSMpFn4ju6vPjpDj5jo2Z07Ehby4yQU4ovM9UKgguucUmScyUVpaqJZkDG3pZLBLobvy5GG1rVvb9rQ9sJL0TJvZ/cTeNKdqgm2fCE2MTLqEvW3mcwIQr5YBQV3jyD72w5tfWu49pmPFTuJb3cR41625Dr7Kg/nPPt0F7UWRzjIoIdSPQViLbiJVu2RjXoO64cgNMdnexLRQhCeUQjdr6lQ5fPx5LHnmpOpMDVXt04USMMjSPwmd9axA+t2GxkJDu8TL9M3c6iqdv0Jze0afAjNT08grF+FOcReH4Be1AXzU7DB+1Dpr8GogYdXzELM0lrzuvnAlsOJqrIzVbOO50BiINeKR99r2XpwOtYgdpX7vlKht9g4ofex1DVJBu1ijrySoaBDMj5jch4KxWIRBpIrbNTFTMsCetIeGB1MzpMN3dMtBQshR7KYadlk3JP+OybTP+zDpjL28cxWAAAAAElFTkSuQmCC"
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

            def temp(self, tuple):
                curve, points, origin_path = tuple
                sub_zip_list = zip(curve, points)
                res_list = map(self.split_curve, sub_zip_list)
                ungroup_data = self.split_tree(res_list, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def Get_Curve_PointEnd(self, curve, other_curve):  # 判断线的两端点是否为交点
                Point_List = [curve.PointAtStart, curve.PointAtEnd]

                O_Point_List = []
                for pt in Point_List:
                    t = other_curve.ClosestPoint(pt, False)[1]
                    closest_point = other_curve.PointAt(t)
                    if closest_point.DistanceTo(pt) < 1e-6:
                        O_Point_List.append(pt)

                Rhino.RhinoApp.Wait()
                return O_Point_List

            def split_curve(self, tuple_data):
                curve, points = tuple_data
                t = []
                for p in points:
                    t.append(curve.ClosestPoint(p)[1])
                return curve.Split(t)

            def Find_Intersections(self, curves):
                intersection_points_list = []  # 交点列表
                for curve in curves:
                    pts = []
                    for other_curve in curves:
                        if curve == other_curve:  # 判断是否同一根线
                            continue
                        # 找线的交点
                        curve_intersections = rg.Intersect.Intersection.CurveCurve(curve, other_curve, self.tol,
                                                                                   self.tol)

                        for i in curve_intersections:
                            if i.IsPoint:
                                pts.append(i.PointA)
                            else:
                                for j in self.Get_Curve_PointEnd(other_curve, curve):
                                    if all(j not in sublist for sublist in intersection_points_list):
                                        pts.append(j)
                    intersection_points_list.append(pts)  # 将交点添加到列表中

                Rhino.RhinoApp.Wait()

                return intersection_points_list

            def RunScript(self, curve, tol):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = tol if tol else self.tol
                    Broken_curve = gd[object]()

                    curve_trunk_list, trunk_path = self.Branch_Route(curve)
                    curve_trunk_list = map(lambda x: filter(None, x), curve_trunk_list)
                    c_len = len(curve_trunk_list)
                    if c_len:
                        intersection_points_list = ghp.run(self.Find_Intersections, curve_trunk_list)
                        zip_list = zip(curve_trunk_list, intersection_points_list, trunk_path)
                        iter_ungroup_data = ghp.run(self.temp, zip_list)

                        Broken_curve = self.format_tree(iter_ungroup_data)
                    else:
                        self.message2('Data on end C is empty！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Broken_curve
                finally:
                    self.Message = 'break curves at intersecting positions'


        # 原始曲线延伸至目标曲线
        class ExtendTargetCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ExtendTargetCurve", "W21", """Extend the original curve to the target curve""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("fef369f5-5b8a-498c-930d-aaca3bef1d64")

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
                self.SetUpParam(p, "Curve", "C", "Original curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Target_Curve", "TC", "Target curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "Extension way：0=Line, 1=Arc, 2=Smooth")
                default_type = 0
                p.SetPersistentData(gk.Types.GH_Integer(default_type))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Res_Curve", "C", "The extended curve")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Res_Bool", "B", "if the original curve can be extended to the target curve，then True、or else False")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Extend_Type", "E", "If both sides of the original curve extend to the target curve,it is BothExtend；If only the starting position is extended, it is StartExtend；If extended only by the end position，it is EndExtend ；If neither side can extend, it is NoneExtend")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMzSURBVEhLrZRbSBRhFMfHiK70YJQVFaEEmga96So78+2sOzPfzKyr7roYBD0EJb3kSxBEIQS99BhJBb4EQYGRXcjwocJWTffiruu6aphl6301xNRyw/k6M3wV4W29/GAe5n++OWfO+c45zGbCq9GzSPCepK+bx3Fcv90iB2qLTs8ThP3PqLw5mHH9/oLCqEcomSK80jnMir5cato4vNSUyYrRHteZXoKdbYFctjWdmjYOJzWxrBSNq+6vZDKWSbQE85aaNg7CbW6r2pUQiuPEqjQ/0H4xnYQwRJtlTPTI+uEkb6WtqI+IpYPEggO3dE37yVwzAswwd4xD64UDh2LJILE5+ggn+SupzGgTzAkaYBShzzuonDwIVW1FcvtD7BonemmgFd3U9Je6p2WNd+9Vk5y8PieVksNs9qQiHHwjl03qbRjnpFaWmv7jaPZUBSsnYA7anlBpdcyFngyL3NGplH0jFiXcmy82Z1HTIljJd8gihxJIDsyY1XAqlZeHFVtyeSU8LINzhENN+UJDGjUtCzRAA3aOEVb0llNpaTjpg4NXInOyK04scrAWwyqgphXhsPeCXkpO8j2i0mIg1YpCey+RSof1TrlN5aTglcAxyHoBMombTC07qfwPsxi4IThiRHD0Ew77rlB5TYDzkFDcD3fmy6OSQQonhWuQMk4KCvsnd+3TZKqvGT1r/d6gTJcMwSRG9prFYL1YMkaa3pWR2MCRL5rGXNTmmVPGgTUC93BOdk0QJPnuGwIMzWV7OYGS+HsWphm/PpF/Hm065ZXD9T4vO5tsMw4nAZLabVLpkB7ghSGwQijdVvzp6oGM72ngdAvsFUWbY6phgX2MBFRitccg3dAAkoM10OcupEQOGh8uAyv4ROwc1UtUR6WlgWApSAyeR7g7ZLVHid5+knMEZiIwD5PdCM9NXu1wINGfZVY9qYIQ2s0KremwAF8arYr9VdTV6vBFXTkw0ZUwE68tuH1aLIkRfbql0hF9N8Hfemeh6yYtcjvR9xVM87hVbTlMP18bIjQFUsM2Xg5fh7I9B6fdkNUUBP4BJRyCAX2MVlgp66LA0b1HVQdS3e7km2GTYJjfKbuH310UeOsAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = sc.doc.ModelAbsoluteTolerance
                self.type_dict = {0: 'Line', 1: 'Arc', 2: 'Smooth'}

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

            def intersection_curve(self, extend_curve, target_crv):
                curve_pts = ghc.CurveXCurve(extend_curve, target_crv)['points']
                if curve_pts:
                    if not isinstance(curve_pts, rg.Point3d):
                        par_list = []
                        sort_list = []
                        for single_pt in curve_pts:
                            single_par = extend_curve.ClosestPoint(single_pt)[1]
                            par_list.append(single_par)
                            sort_list.append(abs(single_par))
                        target_par = min(zip(sort_list, par_list))[1]
                    else:
                        target_par = extend_curve.ClosestPoint(curve_pts)[1]
                    return target_par
                else:
                    return False

            def RunScript(self, Curve, Target_Curve, Type):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Curve, Res_Bool, Extend_Type = (gd[object]() for _ in range(3))

                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    if len(temp_geo_list) < 1:
                        Message.message2(self, 'The Curve-terminal cannot be empty！')
                        return Res_Curve, Res_Bool, Extend_Type

                    re_mes = Message.RE_MES([Curve, Target_Curve], ['Curve', 'Target_Curve'])
                    if len(re_mes) > 0:
                        # "-------------------------"
                        return None, None, None
                        # "-------------------------"
                    else:
                        start_curve = Curve.Extend(rg.CurveEnd.Start, 100000, eval('rg.CurveExtensionStyle.{}'.format(self.type_dict[Type])))
                        end_curve = Curve.Extend(rg.CurveEnd.End, 100000, eval('rg.CurveExtensionStyle.{}'.format(self.type_dict[Type])))

                        start_par = self.intersection_curve(start_curve, Target_Curve)
                        end_par = self.intersection_curve(end_curve, Target_Curve)
                        if start_par and end_par:
                            origin_domain = start_curve.Domain
                            start_need_domain = rg.Interval(start_par, origin_domain[1])
                            start_trim_curve = start_curve.Trim(start_need_domain)

                            start_origin_domain = start_trim_curve.Domain
                            orinig_par = start_trim_curve.ClosestPoint(Curve.PointAtStart)[1]
                            trim_start_curve = start_trim_curve.Trim(start_origin_domain[0], orinig_par)

                            end_need_domain = rg.Interval(origin_domain[0], end_par)
                            end_trim_curve = end_curve.Trim(end_need_domain)

                            temp_curve_list = [trim_start_curve, end_trim_curve]
                            Res_Curve = rg.Curve.JoinCurves(temp_curve_list, self.tol)[0]
                            Res_Bool = True
                            Extend_Type = 'BothExtend'
                        elif start_par and (not end_par):
                            origin_domain = start_curve.Domain
                            start_need_domain = rg.Interval(start_par, origin_domain[1])
                            start_trim_curve = start_curve.Trim(start_need_domain)
                            Res_Curve = start_trim_curve
                            Res_Bool = True
                            Extend_Type = 'StartExtend'
                        elif (not start_par) and end_par:
                            origin_domain = end_curve.Domain
                            end_need_domain = rg.Interval(origin_domain[0], end_par)
                            end_trim_curve = end_curve.Trim(end_need_domain)
                            Res_Curve = end_trim_curve
                            Res_Bool = True
                            Extend_Type = 'EndExtend'
                        else:
                            Res_Curve = Curve
                            Res_Bool = False
                            Extend_Type = 'NoneExtend'

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Curve, Res_Bool, Extend_Type
                finally:
                    self.Message = 'The curve extends to the target curve'


        # 物体确定曲线方向
        class CurveDirGroupByGeo(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CurveDirGroupByGeo", "W22", """Take the end of the object closest to the curve as the start or end of the curve""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1e6b916b-ce90-4429-a503-f0e18f0a8578")

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
                self.SetUpParam(p, "Curve", "C", "orientation of Curve to be determined")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "A set of objects A that affect the direction of a curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                default_bool_x = False
                p.SetPersistentData(gk.Types.GH_Boolean(default_bool_x))
                self.SetUpParam(p, "Reverse", "R", "The end of true near the object is the end，The end of False near the object is begin")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "The curve's direction is determined")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQPSURBVEhLrVZ9bBNlGH8To1EwksxkgkaMERQ/ioQNqPvo27u217tradfe3bp1ZYYZN6cu+BU/khkjJmqmRvzDxc0/GOsd4HAIIwb9ww80opBeW7ZqBBeGMWwDGQwmDNl4X5/eXgakmhBzv+SX6z3P+z6/ey73/p4iO0ApuoH9/G/E4986nnyO9DasO38fC10zpk4hjpxFbfQMWsJChVCqNgRbnp2kj7WQn1ioAOPjqIicR/fTSeQlf6FHga9A4ffIBOqALig5g3azpYVQ1Y2B2ppttPkZSp94nrTmY7DRQy6iNijSSSZRN3ATmULthKD1wGagDHwIeBfwDeCtweDRORh/c7NV9ErEFD0cr+mhsdovaKTmZyIIn90JG+4GroCnmw+8ni0FUChA7pm3kPAPlA43BqN7OvnA/l1OPvcjljLHOXngNCeYJWzxDKqrDaUuvoNGoklaznXRSt5YuXjZqHfJ8rHGEtehtjLPwPZKIZ3G/tRxt5ShvtBhKkZHqaSepEJkjHpCw9Sz+hDFYmaak/t/4/yZB1npGWhasjZRlxfYAsW7jrmE7z6S1XEqQwFJGaP+yFEocBAKmBeAv2MxtdctpbdgKf02FtPNnJiWucDAw1jOzWclr0a1atQn6naCwFZa4emecPm+XO2W+tvdkvmW2282YTkruqQDDp8vW6xp9Dq27doBHTRcEqj0GBdW8RtuYyl7oKrJpkRdHxPQz3m9m29nKXugafpTiUQfrYp+Qit4fcLn6y5mKXugqsa6ywLGKafwcRFL2QNF0V9IJHaBQE++gz9FMXkLS9kDTTNetgQiPbSc10eW+rrnspQ9UBTj1RmBbSBg/IHxxhtZyh6oqv76GhAIWwL6UElJxxXWYAMUJfmmJVD1aV5gkIXtA3TQdkmgjE9mXYH0Yi5w8HGXmIq4/OYjWMgtcgp7i/7XKc4DvqL318BBC1X10nJ311fgNb2h2mnL0HzhIcoFchSEzkL8CHjRPuAOLJkfYr/Z6hLNBiybIu8/sNwbTC3E2rFCu4aT3DkrwCd/wHJmGR/IvQNGthW4pxT/ajr5gRG3lKXe0CCY3zCY4AlmhicsM8zH807rFjMnOak/UyFl72XlrVf0Yn3icxDYDnZt7GfhWcDQKR0dvKMJzSXFDueoYyX3i1Ah9K+1OpDMduhs50xnqSPgspNg2VMuMb2CbUcoGOyYA456OKrupmWc/j0LW4DRWA+jcoRMoxYYQItg+BS+gqtA4ROn89jNZcRjeliLfQ0d6PtYyAI5jdaSv9EQjND1INYB3WyCq35xwrp2AN8FtsJIbYIHCANXAf/djb1Ssg/cdDO7ncX0GHqJwNBntwgK3ARFF4CoA8iTcygGwk9D7DWY4x/AP4xGhBD6BwF3I4wXPtnvAAAAAElFTkSuQmCC"
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

            def get_boundingbox(self, obj):
                if type(obj) == rg.Point3d:
                    obj = rg.Point(obj)
                obj_box = obj.GetBoundingBox(True)
                return obj_box

            def get_closestPoints(self, curve, geo_list):
                new_pt_list = [rg.Point(_) if type(_) is rg.Point3d else _ for _ in geo_list]
                point = curve.ClosestPoints(new_pt_list)[2]  # 得到物件距离最近的那个点
                if point.IsValid:
                    return point
                else:
                    box_0 = rg.BoundingBox.Empty
                    box_list = map(self.get_boundingbox, new_pt_list)
                    for _ in box_list:
                        box_0.Union(_)
                    return box_0.Center

            def get_curve_extreme_point(self, Curve):
                # 获取曲线的两个端点
                return Curve.PointAtStart, Curve.PointAtEnd

            def compare_distance(self, curve, geo_list):
                geo_point = self.get_closestPoints(curve, geo_list)
                curve_PS, curve_PE = self.get_curve_extreme_point(curve)
                curve_point = []
                if curve_PS.DistanceTo(geo_point) < curve_PE.DistanceTo(geo_point):  # 比较两点之间的距离
                    curve_point.append(curve_PS)
                    curve_point.append(curve_PE)
                else:
                    curve_point.append(curve_PE)
                    curve_point.append(curve_PS)
                return curve_point

            def get_vector(self, points, curve):
                vector = points[1] - points[0]
                curve_PS, curve_PE = self.get_curve_extreme_point(curve)
                cvector = curve_PE - curve_PS
                rcurve = curve
                if vector != cvector:
                    rcurve.Reverse()
                return rcurve

            def temp_vector(self, tuple):
                Points, Curve = tuple
                new_Point = Points[::-1] if self.Reverse else Points  # 判断点列表是否反转

                rcurve = self.get_vector(new_Point, Curve)  # 根据点列表判断是否反转

                return rcurve

            def temp(self, tuple):
                Curve, Geometry, Path = tuple

                Cut_None_Geometry = filter(None, Geometry)
                Cut_None_Curve = filter(None, Curve)

                if len(Cut_None_Curve) == 0:
                    r_curve = []
                else:
                    Curve_Point = map(lambda one_curve: self.compare_distance(one_curve, Cut_None_Geometry), Cut_None_Curve)  # 将单根线和一组物体传入主方法中
                    zip_list = zip(Curve_Point, Curve)
                    r_curve = map(self.temp_vector, zip_list)

                iter_group_data = self.split_tree(r_curve, Path)

                return iter_group_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_trunk = value_list[max_index]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [value_list[_] for _ in range(len(value_list)) if _ != max_index]  # 剩下的树
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

                iter_group = map(sub_match, matchzip)
                iter_group.insert(max_index, max_trunk)

                return iter_group, ref_trunk_path

            def RunScript(self, Curve, Geomertry, Reverse):
                try:
                    rcurve = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    structure_tree, structure_tree1 = self.Params.Input[0].VolatileData, self.Params.Input[1].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]
                    temp_geo_list1 = [list(i) for i in structure_tree1.Branches]
                    if len(temp_geo_list) < 1 or len(temp_geo_list1) < 1:
                        Message.message2(self, 'The Curve or Geomertry-terminal cannot be empty！')
                        return gd[object]()

                    re_mes = Message.RE_MES([Curve, Geomertry], ['Curve', 'Geomertry'])
                    if len(re_mes) > 0:
                        return None
                    else:
                        self.Reverse = Reverse
                        iter_group, target_Path = self.temp_by_match_tree(Curve, Geomertry)
                        trunk_Curve, trunk_Geometry = iter_group

                        zip_list = zip(trunk_Curve, trunk_Geometry, target_Path)
                        ungroup_data = map(self.temp, zip_list)
                        rcurve = self.format_tree(ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return rcurve

                finally:
                    self.Message = 'The object determines the direction of the curve'


        # 边界矩形
        class BoundingRectangle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-BoundingRectangle", "W41", """Creates a boundary rectangle for a set of geometric objects""", "Scavenger", "B-Curve")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def get_ComponentGuid(self):
                return System.Guid("ce6e9b19-3d20-4985-b63e-645dae646330")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Object", "O", "A set of geometric objects")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "Pl", "Original plane")
                ORIGIN_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(ORIGIN_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Rectangle()
                self.SetUpParam(p, "Bounding", "B", "resulting boundary rectangle")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Dim-X", "X", "X dimension of the rectangular plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Dim-Y", "Y", "Y dimension of the rectangular plane")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQsSURBVEhLrVZvaBxFFD+qIvW/aPtJoV9FqbaBNjW7O7t7tzsze3e5S5N8FkEUUeM/sJoK0aIE0VKEgogfBBVEKv3QDy1a9bA2udzt7eV2k7vUJmk11obWXhqCgqLt+N7e3JrLhfY++IPH7cy8eb958968dzHNdq145sxbhJb+d0G7MZ16B/jAkqB95wX+rhW2+4KwMmdFondOWL1nBO+vr6u3Vmjfr+FvDJnQOGGlrzXm7tV4aVij3isqLT5DmPu0Rt13CSvXEr3zwkxWBYxHQ72mgD7YeA2+94CNVzVaHG6slXJoNyRwBpeFxovPx1aBONOPGNx/H2TRcPyrRrLqIqlcvi5029vLBy43CPhAXajInsg/QBz/Pd0JLtrZc0J3/GXDqRzUncpOua8FXV1HbgGdfXCIGcInL+m8sqDzye9JZvIuQt3XoytC92Hij3j6tDCcKaFz/zDhlRRjp2+WttrQPTC+0UhOu3b2F9hb+gau5SONe4eA5LiSDO5uIcDTgsES4f4TCitvkjauCY2WPsd9Ki+ZcqoFxPbejgjwrlRWfEGuRXi0d+Z2q29x88iI2CCnQhC7+LgDezQrPySn2tCwGxEsCYy8XIspytFNOg8+gav6BzOH8HJdZ+Vj4PabkFkHMTt0Xj4s1UP02BMP68x9TA7bCVS4M1zYSXJbzNTMAsYDUvIAGHwRyD8Gg7MgVw0n+AsC+0FX14c3hZYA+A3xOA96Z+XUOh5w92WMvpmsLZqpU8u7rLGHpG6EwUFxg/xsAXj6KT4s1XZ3yKl2AsK9Zw1aeDCenp1TzBNbpV4L7MzU/WY62ArebtdYcRu8HW7w4BimuWKPPyfVQrR7sCoGa6EkTsThoVWxXISSngWB0pH5SZhO9TIGXapG6JhAscdSmOtwxzU49ZMqLVBIQWawwCGs1o2PTaq2oCMCQvNb4ukf/zac6ZOrg9oJOiNg7piZnLlCSO5eOdWCRGL+TiM5BekZEC3pqxqrbLOsyq24Rqj3xhqCwp5w1ypAmg71WHkuhxFUOr4dvPoSsucKlplmbFj/b3jQfaij0QK0gXqToA5p6o2Gu6+JkQ1gdNTOLkDNClagjO8n9kRW524PlA7VTM1x8GAzpiskxe+YBCEBniKeOoX16DNpqQ3xeO0eKGQ+678Ixv39O9jRO+RSC+A6b4OKegE9gpRvEFjZn6HhuB5OgOtHCBm5UepHIGziPiNVzWlWMS2n1gV4mIODrEDjORQ1HIwBPJ6nMAXp7kXsXN92d3+xUe7pGPAe3sGWSlhewfj913CgozWrqUZP7kqk51egZPyA7oY7OwAcMGn3nYP6VXgJxxCTYT4oCdAViP7xRj92hzS78BXWFri27zB9O5RZ6Hx/hn0Z7OjNnrzevwpsJFgO8Lqac9cTfO2YLLz/Ujhu/KtYEv8C/ZUN1pUdzyQAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.ref_plane = None

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
                new_tree = ght.list_to_tree(tree_data, True,
                                            tree_path)  # 此处可替换复写的Tree_To_List（源码参照Vector组-点集根据与曲线距离分组）
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

            def _get_vertex(self, data_list, pln):
                pts_list = []
                for item_data in data_list:
                    if type(item_data) is rg.Point3d:
                        pts_list.append([item_data])
                    elif isinstance(item_data, (rg.Curve)):
                        pts_list.append(rg.Box(pln, item_data.ToNurbsCurve()).GetCorners())
                    elif type(item_data) is rg.Brep:
                        pts_list.append(item_data.GetBoundingBox(True).GetCorners())
                    elif type(item_data) is rg.Rectangle3d:
                        box_line = item_data.ToNurbsCurve()
                        pts_list.append(rg.Box(pln, box_line.ToNurbsCurve()).GetCorners())
                return pts_list

            def get_boxegde(self, obj, pln):
                pts_list = self._get_vertex(obj, pln)
                box_egde = rg.Box(pln, list(chain(*pts_list)))
                return box_egde

            def get_sub_box(self, box, pln):
                turn_box = box.ToBrep()
                if turn_box:
                    face_list = [_ for _ in box.ToBrep().Faces]
                    face_pln_list = []
                    for face in face_list:
                        set_data = face.TryGetPlane()
                        if set_data[0]:
                            face_pln_list.append(set_data[1])
                        else:
                            face_pln_list.append(rg.Plane.WorldXY)

                    ref_vector = pln.Normal
                    vector_is_parallel = [_.Normal.IsParallelTo(ref_vector) for _ in face_pln_list]
                    sub_index = vector_is_parallel.index(-1)
                    sub_suface = face_list[sub_index]

                    new_sub_box = rg.Box(pln, sub_suface)
                    work_pln = face_pln_list[sub_index]
                    work_pln.Flip()
                else:
                    new_sub_box = box
                    work_pln = pln
                corners = list(set(new_sub_box.GetCorners()))
                pt_1, pt_2 = self.get_two_pt(corners)
                sub_box = rg.Rectangle3d(work_pln, pt_1, pt_2)
                return sub_box

            def get_two_pt(self, pts):
                pt_one = pts[0]
                max_values = []
                for pt in pts:
                    max_values.append(pt_one.DistanceTo(pt))
                pt_two = pts[max_values.index(max(max_values))]
                return pt_one, pt_two

            def _do_main(self, tuple_data):
                objs, Plane = tuple_data

                objs = list(objs[0]) if 'List[object]' in str(objs) else objs
                objs = [_ for _ in objs if _ is not None]
                if len(objs) == 0:
                    New_BoundingBox, X_Dir, Y_Dir = [], [], []
                else:
                    new_box = self.get_boxegde(objs, Plane)
                    if type(new_box) == rg.Box:
                        New_BoundingBox = new_box
                        X_Dir = New_BoundingBox.X
                        Y_Dir = New_BoundingBox.Y
                    else:
                        New_BoundingBox = self.get_sub_box(new_box, Plane)
                        X_Dir = New_BoundingBox.Width
                        Y_Dir = New_BoundingBox.Height
                return New_BoundingBox, X_Dir, Y_Dir

            def temp(self, tuple_data):
                # 解包元组元素
                origin_object_list, origin_pl_list, origin_path = tuple_data
                # 若平面有多个，重新赋值
                o_pl_len = len(origin_pl_list)
                if o_pl_len == 1:
                    origin_object_list = [origin_object_list]
                else:
                    origin_object_list = [origin_object_list[:] for _ in range(o_pl_len)]
                # 每个单元切片进行主方法排序
                sub_zip_list = zip(origin_object_list, origin_pl_list)
                res_object_list = map(self._do_main, sub_zip_list)

                New_BoundingBox, X_Dir, Y_Dir = zip(*res_object_list)
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [[New_BoundingBox], [X_Dir], [Y_Dir]])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Object, Plane):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Bounding, X, Y = (gd[object]() for _ in range(3))

                    trunk_object, trunk_path = self.Branch_Route(Object)
                    o_len = len(list(filter(None, (chain(*trunk_object)))))
                    if o_len:
                        # 数据匹配
                        object_trunk, pt_path_trunk = self.Branch_Route(Object)
                        pl_trunk, pl_path_trunk = self.Branch_Route(Plane)
                        pt_len, pl_len = len(object_trunk), len(pl_trunk)
                        if pt_len > pl_len:
                            new_object_trunk = object_trunk
                            new_pl_trunk = pl_trunk + [pl_trunk[-1]] * (pt_len - pl_len)
                            path_trunk = pt_path_trunk
                        elif pt_len < pl_len:
                            new_object_trunk = object_trunk + [object_trunk[-1]] * (pl_len - pt_len)
                            new_pl_trunk = pl_trunk
                            path_trunk = pl_path_trunk
                        else:
                            new_object_trunk = object_trunk
                            new_pl_trunk = pl_trunk
                            path_trunk = pt_path_trunk
                        zip_list = zip(new_object_trunk, new_pl_trunk, path_trunk)
                        # 获得结果树列表
                        iter_ungroup_data = zip(*ghp.run(self.temp, zip_list))
                        Bounding, X, Y = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                 iter_ungroup_data)
                    else:
                        self.message2("The O terminal is empty！")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Bounding, X, Y
                finally:
                    self.Message = 'Boundary rectangle'


        # 获取一组曲线集的轮廓曲线
        class PlanarCurveContour(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PlanarCurveContour", "W52", """Gets the contour curve of a set of curves""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("67a4091c-f26f-4d39-980e-fdae9e01df4e")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_List", "C", "Curve set")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane")
                NORMAL_PLN = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(NORMAL_PLN))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance")
                NUM_TOL = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(NUM_TOL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Res_Curve", "R", "Result curve")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAS3SURBVEhLxZV5bBRVHMeH4hZLbWnrVW3pgT1Q0FqRXrQ7u9vdndmj2wOQSIJXQKrEmHjGqG2kRo3BEGOkwahERAP6hyhGKYFUiPa+thQWW9qipYootnSDIGif3+/bWYsNHv/5ST7J+/3ezHszb97vjfJ/MRO2wadkdAmsmj9bdfVUq3r3dourK6C6Ok9ZXD0nre6+3SWOr8zGZX/LDPg6FHAlE8Ts8t9cWnb0WZv7UMDuOyps3oDA4MNmvWOnqre9ana21VtcvUMO35Cw6F2qcds/Uh81O2Uyz7KrTqsY3e8oHxZWt1+UaK17KlZOeh94UcQb111EbQSuCahae5eRuDSeO4L2xCTfB4nJPuGsPC5yC7aIxCSvMJnm8K2+ga/AG3ntdMxayxMWV7co8n0ZY6SmyFc/T8M67vUsnxCJyeUiIsIUiI7J6kHXr7AKLoNb4FnIyd6AUfBPVK1tldXTJ1S9JdlIhVhibywo9X4dtHkCY1rliGfGzFnbkW6F18ATsBmGmQNrICfxw2uhBMuz2uo+KFR3a6KRwmvZv8jExwmWlvW3FzoaOCD5EAZCTWUB5GD7ZDTFEsi364WXM2HW22pVvf28qjbKGNRGWNwH/cX2AyIlZc11RpK8B7nei2SkKA7ISbbKaIpCyPxbDDD4DrPePsy2RNU67tGqvhcJVxc3IuQah3kX8ka6jQlwF2T8goymeA4yn2nzHunCJB/LLMGa9+XkbWanCz4E06EHXoBc34ch+0sheRoyXiejEPzQ4yZT3G7Uymk89OMyqzo75rNo0jOqNyNcCu+Ea+A5yEE6IBmFH4WaknrI/koZhdgUl3CbcPgGsYP8BTLDLcWKXLVu8kqZCMEP2wk3wnEmANtnoElGIT6BnITfgKxIy6wWdt/gjw5HQ7TMoMxrsK3O63r/LJlQFL4Jb0qC4fWOgE6jvRCGiYR8Q9bE9TBrUdE2TDDwGdoh8LXXm7U2LgfhunOQR2WkKD7IOBVy37O9Gl5MAvwW9sfG36Jb3b04n/oekT2kRGtfy6IwQnbsDDUlWZB94XVmsb0faipcY9YAuQEGr0q0Bx3lxyatzpacUBqY9a7FPP2SUpe9ifAdyEHD8NjmNwjvew4+AudBTsxtHCYje2HNmRJnczA1VQ0XmKLctLwv0uoJnFiQu+EnhMchb3wbcquSl+Ek5DbMhez/GfbDyyC5Ha7HuTUWHZPB/tdkNkyJ1vK8s2L0l5z8jWkIH4MsfV64AfKNhmAT5AR8S1bpg5DFNQiFKTJOzJ13t7giNpv9vPcZGCJPb4nFCTpR6j2yx0jxnH8J8sIJ2ACD8Dd4Gv4O2ccH2TE7JvU+q8s/4awc3YuY1EH23ysjYnY0u/SqH4TF3cvjNwy36ibIiubgHIAboQIuhhJ96cl9dt/QeIlz/1wjRVg3f91xWKq1nMSG/4HqbMow0oTnOuuD25lHx61QcZYfK8K5M1JaNnCu2HEgn7l/xexoKrN5D4/bywawn7u3WvVu5/1PCtaAEhWTmR8Vnd6dlLKiG8W0S6v8Dv/lQz2FauN8efN/pbj403j8vOuwXKfw6oJ/J7PeedbmOTyG/8UFHAX4N/f2qy7/9KKbhqL8AUkUrA5Nwo8/AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol, self.pln = (None for _ in range(2))

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

            def _planr_curve_box(self, curve_list):
                init_box = rg.BoundingBox.Empty
                cur_box = [_.GetBoundingBox(True) for _ in curve_list]
                for single_box in cur_box:
                    init_box.Union(single_box)
                return init_box

            def _curve_stitching(self, origin_curves, rest_curve):
                origin_curves = list(origin_curves)
                single_curve = rest_curve[0]

                for origin_c in origin_curves:
                    _event = rg.Intersect.Intersection.CurveCurve(origin_c, single_curve, self.tol, self.tol)
                    _list_event = list(_event)
                    if _list_event:
                        new_origin_c = rg.Curve.JoinCurves([origin_c, single_curve])[0]
                        origin_curves.remove(origin_c)
                        origin_curves.append(new_origin_c)

                rest_curve.remove(single_curve)
                if rest_curve:
                    return self._curve_stitching(origin_curves, rest_curve)
                else:
                    return origin_curves

            def connect_start_end(self, single_cuvre):
                start_pt = single_cuvre.PointAtStart
                end_pt = single_cuvre.PointAtEnd
                line_curve = rg.Line(start_pt, end_pt).ToNurbsCurve()
                single_region = rg.Curve.JoinCurves([single_cuvre, line_curve])[0]
                return single_cuvre if not single_region.IsClosed else single_region

            def intersect_curve(self, region_curve, disjoint_list):
                region_curve = region_curve if type(region_curve) is list else [region_curve]
                region_curve = rg.Curve.CreateBooleanUnion(region_curve, self.tol)[0]

                intersect_pts = []
                others_region_list = map(self.connect_start_end, disjoint_list)
                a_part = [_ for _ in others_region_list if _.IsClosed]

                b_part = [_ for _ in others_region_list if _ not in a_part]

                if b_part:
                    for curve in b_part:
                        pts, cur_list = [], []
                        curve_intersections = rg.Intersect.Intersection.CurveCurve(region_curve, curve, self.tol, self.tol)
                        if list(curve_intersections):
                            for i in curve_intersections:
                                if i.IsPoint:
                                    pts.append(i.PointA)
                            intersect_pts.append(pts)
                    intersect_pts = list(chain(*intersect_pts))
                    if intersect_pts:

                        import Point_group
                        sorted_indexes = Point_group.SortPointByRightHand().right_hand_rule(intersect_pts, rg.PointCloud(intersect_pts).GetBoundingBox(True).Center, self.pln.XAxis, self.pln)

                        sorted_pts = [intersect_pts[_] for _ in sorted_indexes]
                        sorted_pts.append(sorted_pts[0])
                        poly_line_curve = rg.PolylineCurve(sorted_pts)
                        poly_line_curve = poly_line_curve if poly_line_curve.IsClosed else None
                    else:
                        poly_line_curve = None
                else:
                    poly_line_curve = None
                temp_curve = rg.Curve.CreateBooleanUnion([region_curve, poly_line_curve] + a_part, self.tol)
                if temp_curve:
                    interval_curve = temp_curve
                else:
                    interval_curve = [region_curve]
                return interval_curve

            def _curved_profile(self, tuple_data):
                curves, origin_path = tuple_data
                curves = [_ for _ in curves if _ is not None]
                if not curves:
                    ungroup_data = self.split_tree([], origin_path)
                else:
                    curves = list(rg.Curve.JoinCurves(curves))
                    if all(not (curve.ToNurbsCurve().IsClosed) for curve in curves):
                        ungroup_data = self.NOClose_Curve(tuple_data)
                    else:
                        nur_cur_list = [_.ToNurbsCurve() for _ in curves]
                        res_box = self._planr_curve_box(nur_cur_list)
                        frame_curve = rg.Curve.JoinCurves([_.ToNurbsCurve() for _ in res_box.GetEdges() if _.IsValid is True])[0]

                        new_nur_list = []
                        disjoint_line = []
                        for _ in nur_cur_list:
                            curve_event = rg.Intersect.Intersection.CurveCurve(frame_curve, _, self.tol, self.tol)
                            turn_list_curve = list(curve_event)
                            if turn_list_curve:
                                new_nur_list.append(_)
                            else:
                                disjoint_line.append(_)
                        join_curve_arr = rg.Curve.JoinCurves(new_nur_list)

                        factor_closed = [_.IsClosed for _ in join_curve_arr]
                        if any(factor_closed):
                            first_closed = [_ for _ in join_curve_arr if _.IsClosed]
                            closed_curve = [_ for _ in disjoint_line if _.IsClosed]
                            if closed_curve:
                                temp_curve = rg.Curve.CreateBooleanUnion(first_closed + closed_curve, self.tol)[0]
                                res_curve = self.intersect_curve(temp_curve, disjoint_line + [_ for _ in new_nur_list if
                                                                                              _.IsClosed is False])
                            else:
                                no_join_curves = [_ for _ in nur_cur_list if _.IsClosed is False]
                                res_curve = self.intersect_curve(first_closed, no_join_curves)
                        else:
                            interface_curve = join_curve_arr
                            disjoint_join_line = rg.Curve.JoinCurves(disjoint_line)
                            # "-----------------------"
                            if len(disjoint_join_line) > 1:
                                repair_line = list(chain(*[_.DuplicateSegments() for _ in disjoint_join_line]))
                                repair_line = [_ for _ in repair_line if _.IsValid]
                                stitching_curve = self._curve_stitching([interface_curve[0]], repair_line + list(interface_curve[1:]))
                                res_curve = rg.Curve.JoinCurves(stitching_curve, self.tol)
                            else:
                                res_curve = disjoint_join_line
                            # "-----------------------"
                        ungroup_data = self.split_tree(res_curve, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def NOClose_Curve(self, tuple_data):  # 没有封闭的曲线
                curves, origin_path = tuple_data
                if len(curves) != 1:
                    curves = filter(None, curves)
                    curves = [_.ToNurbsCurve() for _ in curves]
                    split_breps = []
                    bounding_box = rg.BoundingBox.Empty
                    for curve in curves:
                        bounding_box.Union(curve.GetBoundingBox(True))
                    polygon_curve = rg.PolylineCurve(bounding_box.GetCorners())  # 将bounding_box转换为PolylineCurve
                    try:
                        Surface = rg.Brep.CreatePlanarBreps(polygon_curve)[0]
                    except:
                        return self.split_tree(curves, origin_path)
                    nurbs_curves = [crv_ for crv_ in curves]  # 将曲线转换为NURBS曲线列表
                    split_breps = Surface.Split.Overloads[IEnumerable[Rhino.Geometry.Curve], System.Double](
                        nurbs_curves, 0.01)

                    # 判断Brep的边线是否在给定的线附近的函数
                    def find_edges_on_curves(Brep, Curves):
                        result = 0
                        pt_length = []
                        for edge in Brep.Edges:
                            edge_curve = edge.ToNurbsCurve()
                            for pttt in edge.DivideByCount(100, True):
                                pt = edge.PointAt(pttt)
                                pt_length.append(pt)
                                for curve in Curves:
                                    t = curve.ClosestPoint(pt)[1]
                                    test_pt = curve.PointAt(t)
                                    distance = test_pt.DistanceTo(pt)
                                    if distance < 0.001:
                                        result += 1
                        return result >= len(pt_length)

                    def brep_unnion(Breps):  # Brep Union
                        Brep = rg.Brep.CreateBooleanUnion(Breps, 0.1)
                        Brep[0].MergeCoplanarFaces(0.1)
                        curve_list = Brep[0].Edges
                        curves = [_ for _ in rg.Curve.JoinCurves(curve_list, 0.1, False)]
                        return curves

                    surface = [brep for brep in split_breps if find_edges_on_curves(brep, curves)]
                    if len(surface) == 0:
                        ungroup_data = self.split_tree(curves, origin_path)
                    else:
                        res_curve = brep_unnion(surface)
                        ungroup_data = self.split_tree(res_curve, origin_path)
                else:
                    ungroup_data = self.split_tree(curves, origin_path)
                Rhino.RhinoApp.Wait()

                return ungroup_data

            def RunScript(self, Curve_List, Plane, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = Tolerance
                    self.pln = Plane
                    Res_Curve = gd[object]()

                    re_mes = Message.RE_MES([Curve_List], ['C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve_trunk, curve_trunk_path = self.Branch_Route(Curve_List)
                        zip_list = zip(curve_trunk, curve_trunk_path)
                        iter_ungroup_data = ghp.run(self._curved_profile, zip_list)
                        if filter(None, list(iter_ungroup_data)):
                            Res_Curve = self.format_tree(iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Curve
                finally:
                    self.Message = 'Curve plane profile'


        # 竖直线、水平线
        class VHLine(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_VHLine", "W54", """The line is divided into two kinds: partial vertical and partial horizontal""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6f6b0933-33aa-480e-b2f5-a8e02315adc7")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Straight line，Non-straight lines will be combined by starting and ending lines")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Reference plane，The level corresponds to the X-axis of the plane、The vertical aligns with the Y-axis of the plane")
                NORMALPLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(NORMALPLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "Tolerance Angle")
                ANGLETOL = 45
                p.SetPersistentData(gk.Types.GH_Number(ANGLETOL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "HorizontalLine", "H", "Horizontal line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "VerticalStraightLine", "V", "Vertical line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "OtherStraightLines", "OL", "Other types of lines")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "HorizontalDeviationLine", "HD", "A horizontal line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "SlantedVerticalLine", "SV", "A vertical line")
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
                        self.marshal.SetOutput(result[4], DA, 4, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOkSURBVEhLrVVra1xFGN5qqdJWLZVCW0oRb2goUVIpNN1z5pzZ3XPmXBIv7RLIB8Ev2lZKUSgVhIZYiqWBImirFap+8ULALxpTFLTFJJvsuewtZ2+JtgYq/eJ/iM/MzsbdNmm2sQ8MM+8773memXfemRNjbO4h1fT6qVvsIeTq5qQb7Y6zsDt2v5BMBo8RM/hFt0vzhAVzmlW4Raz8P5pdGCIsn9aN3Au9/dVHZPjakU5HGxJW4VnCwiliFcYgNg6homblq5qVy2EcoH2PBZwmTj5NnMKeVKqwSX7eOVTmB4qZ6UH/uWr5KfJyfgtEj4H8FY3lTmFX30EkC+F5+P7QWN6HPYrxMPqDlEVde91go6RrB08XiG8YRrRVNYNrqhn29zL/KWL6czKkDXGW20adogKxtyFwAWLjGE9DKKPZxZ/A8bEMbYBY4UuENcjQ/66ysC/O02b6QZx5hPbVRlTTH8EizqH/UGXeB4h5XzX8kwrLvoe4Yfgvqiy4ojuVBfQ1QdwEMbw3EDDBx1CfbBHwFDMwqVP7AuQrNsRdRsFcwvgT2lc/D+FBQdwEVv0RAi7L8VSLQF0E/F+A6Ges/LgYLwlkIRB4xPDPUKdyGndliwheC0BUxrZ0MW7dAfNDYnpJ6lR/RVugTjTSm5zcKT7qFLwikP+/FNPfwe1WAfirIgjQrNkDOMAfdLdyk9qVS2py+hk5dXfgYsXlqa9r2G1nUInFFoW/CcpK3UjZ12h/6271W2JHL8qp5YGSOwrS36S5qkATCaf0pO5En4odudUx6pQVOdUO7OAzXsPS7FigCWJnt+tO+Syvf5zTNYxtOdUA0nNVM/23pHnPAk3wF5m65cMJtxaB8xvpXlwHkrpieL3SsWYBDt2p9iPlb6JgeoSDsJldvIISiezjwgGsRQDlewjpyVG3PkeswJVukKHGsZ1ImgL3IkCd0quoJp+6tTpyfwSuBxozEng134XAFWkKdCJA2WwfqieLVc/rdnSMkKH1cqoduMFf4bd5XpoCdwr8B90p2SDNoCz/BPE7XV2jG+TU8kCJTuGJeF2aArcJlNPp0QcVljdAPIF2XbfLJwj58mEZvjJQVuvxvM4vnbhEqwDmAzUZPo8LNa07NZ7jzkGM8GmQLexjM49KlwB8GS6w3wie4zvgC8CTMKga0ymc2Wso6QHFWrnhzRrgf0QIBC4IipJ3CYR5ISciZv4J7OBHxBzGT2QC6cxw8dWaZhUzxAzG/wWq0i7/1hq2PQAAAABJRU5ErkJggg=="
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

            def RunScript(self, Curve, Plane, Angle):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    if self.RunCount == 1:
                        self.j_bool_f1, self.origin_curve, self.curve_path = self.parameter_judgment(self.Params.Input[0].VolatileData)
                    HorizontalLine, VerticalStraightLine, OtherStraightLines, HorizontalDeviationLine, SlantedVerticalLine = (gd[object]() for _ in range(5))
                    re_mes = Message.RE_MES([self.j_bool_f1], ['C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        curve_list = self.origin_curve[self.RunCount - 1]
                        if filter(None, curve_list):
                            gh_curve = list(map(self._trun_object, curve_list))
                            h_list, v_list, os_list, hd_list, sv_list = ([] for _ in range(5))
                            for i in range(len(gh_curve)):
                                # 判断是否为直线 不是的话取首尾点连接成直线
                                if str(type(gh_curve[i])) != "<type 'PolylineCurve'>":
                                    gh_curve[i] == rg.PolylineCurve([gh_curve[i].PointAtStart, gh_curve[i].PointAtEnd])
                                # 向量对比是否平行
                                if gh_curve[i].TangentAtEnd.IsParallelTo(Plane.XAxis):
                                    h_list.append(curve_list[i])
                                elif gh_curve[i].TangentAtEnd.IsParallelTo(Plane.YAxis):
                                    v_list.append(curve_list[i])
                                else:
                                    os_list.append(curve_list[i])
                            for i in range(len(gh_curve)):
                                # 向量对比是否在规定的偏向平行的度数之内
                                if gh_curve[i].TangentAtEnd.IsParallelTo(Plane.XAxis, math.radians(Angle)):
                                    hd_list.append(curve_list[i])
                                elif gh_curve[i].TangentAtEnd.IsParallelTo(Plane.YAxis, math.radians(Angle)):
                                    sv_list.append(curve_list[i])
                            HorizontalLine, VerticalStraightLine, OtherStraightLines, HorizontalDeviationLine, SlantedVerticalLine = h_list, v_list, os_list, hd_list, sv_list
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return HorizontalLine, VerticalStraightLine, OtherStraightLines, HorizontalDeviationLine, SlantedVerticalLine
                finally:
                    self.Message = 'Vertical line、Horizontal line'


        # 根据点所在的位置对曲线进行偏移
        class OffsetByPoint(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_OffsetByPoint", "W111", """The curve is offset according to the position of the point""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3f3152cb-0b25-4da8-953f-0479f1c5a5c7")

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
                self.SetUpParam(p, "Curve_input", "C", "The curve to be offset")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "An indication of the offset direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distances", "D", "Offset distance")
                DIS = 10
                p.SetPersistentData(gk.Types.GH_Number(DIS))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Normal", "N", "Offset normal")
                NORMAL = rg.Vector3d(0, 0, 1)
                p.SetPersistentData(gk.Types.GH_Vector(NORMAL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Corner", "C", "Chamfer type none -0 sharp -1 round - 2 smooth-3 chamfer - 4")
                INTER_NUM = 1
                p.SetPersistentData(gk.Types.GH_Integer(INTER_NUM))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_Output", "C", "The offset curve")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                result = self.RunScript(p0, p1, p2, p3, p4)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN8SURBVEhLrZVdaBRXFMe3xkatGnywaDTuJpDsJvEj2qSrbjNzZnZ3Zu6dmWQ3uiOiffDF2lootFXxqaGiqPSlUCl9EATRl+iDqPgifoAkmp3Zz2yiSf02aUQjFJGClHJ773ifSicbk/zgsjP/ezhzz86c//G1ms5Hkp5NiKjYBWoGSSgLgpoLg5FeI3Tk68C8txShkXm+6SIoGVHrGifaFrq6xojaNUrU5FOiJB6RWMcIkfUiAeS8AZR5CDhzE3D2N3qgvYAKm8AqLeJpvGn9wvlQ1BwB8IBJE1mgObskzfmaXh8E7Byj9ycB2ZdF5OToQyaixqB7ELYknP9L0ovnAOdNnm5mWBapELShatEoCBLOfi/h3NWoUSJ460si6aW8oNyJ8tDZw+omlaDf3SfrA29ZVe1K37d8a2Z0W1alGoOvRLFtL7sX1PQqWS/dxlsniKD27XSDZkJMEk5HJSCRyGfkk7bwDaYB9CyS9cEHsjH0ph1lP3YDp8vm1tCzDetbyOrVa8jatS1kQySyguntWl+cvRPQ7B/dwOlQv3OiKhQ58Ly5qYk0hoIkGAxeB4C5fNsnaun7dI11d5M5XJo69ehKVSDxuFCDh8cbmoT9oQb/N+FwfRXfdgEtfcztI5wPcqkMhHzAftZ9nl8Y6HxU8BvDf64ULzW4e/8DqE6SNS6tYguXJqcumQsHzOELAeP3WzT5i5XiWc/kDND716vJJ8wB9nFpcmr1/JG61GtSmxgjNfI1kcuegHa7NtYxzB5wnH5aN+YKmp2QjUEdzGKjoowv5HEuzRap9OvFV7XJ58SPh0b9yp0U3/IE9NJy1uHUWk74aPJqZmisQZTOh0x8K6GcLeHC0TgutlWrvY01Wu6cX+lNhSLHF/MckxLtKC6TjQH6DuxfXaEdZdbJuLRDQplD1OAuUp/5g/2H7wytcDUBp5a4gVOEHfpdBfYJLv0H+tXIarYFUO5nNTnKXPPulKyZI+u9gZh5j1XwE5e8AbV/N069IpJm7+FSWWQtHYp3PiDU4n/gkjemO/EK/9DWP8Olsogo/SkbXLSC77jkzaZU3wIR2X/T05znUllkI9OqJp/Rd5DeziVv4vHMiqg5xMr9hUtlsayeCmrZYdoC87nkjaCzmT3G3PFLLs0udCbvN7a9ppPK3sil2QVwfxsd6oebm3squfQe+Hz/AnYSc+/XD7PfAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.corner_dict = {0: "None", 1: "Sharp", 2: "Round", 3: "Smooth", 4: "Chamfer"}
                self.j_bool_f1 = False
                self.j_bool_f2 = False

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

            def RunScript(self, Curve_input, Point, Distances, Normal, Corner):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Curve_Output = gd[object]()
                    # 插件默认值参数
                    if self.RunCount == 1:
                        self.j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                        self.j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
                    else:
                        pass

                    # 插件默认值参数
                    Style = eval("rg.CurveOffsetCornerStyle.{}".format(self.corner_dict[Corner]))
                    # 插件默认值参数
                    tol = sc.doc.ModelAbsoluteTolerance
                    re_mes = Message.RE_MES([self.j_bool_f1, self.j_bool_f2], ['C end', 'P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Curve_input and Point:
                            temp_arr_cur = Curve_input.Offset(Point, Normal, Distances, tol, Style)
                            if temp_arr_cur:
                                Curve_Output = temp_arr_cur[0]
                            else:
                                Curve_Output = Curve_input
                                Message.message2(self, "Curve offset failure！")
                        else:
                            Curve_Output = None

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Curve_Output
                finally:
                    self.Message = 'The curve shifts toward the point'


        # 判断曲线集合B和闭合曲线A的位置关系
        class CurvePosition(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CurvePosition", "W53", """Determine the position relationship between curve set B and closed curve A""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("11fac9d6-fe1b-4772-a0c2-23ced196ff1d")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_A", "CA", "Closed curve A")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_B", "CB", "Curve set B")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Reference plane")
                DEFAULT_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(DEFAULT_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Express", "E", "Explain the relationship between the two")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Value", "V", "0：Within the curve，1：Intersect a curve，2：Off the curve，1000：The two are not compatible")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Inside", "C1", "The line inside the closed curve A")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Intersect", "C2", "The line that intersects the closed curve A")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Outside", "C3", "The line outside the closed curve A")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Non Coplanar", "C4", "A line not collinear with the closed curve A")
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
                        self.marshal.SetOutput(result[4], DA, 4, True)
                        self.marshal.SetOutput(result[5], DA, 5, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARkSURBVEhLpVZdTBxVFD5q1AYxttqgSNUHK00NxqptFSkzswO7M7MsUIhJ0ybWJkoaSYyP9sWsjS998cFgCtVq+wDM7JZdYGmxVIq0KQjMLruEtWpjhKQ0pFVL2dlfShjPvTNLYYCWxC/5Muece+d89+fcuQMmCpC5Qs1kvr16YgcrhXb+X/Kuq28y5aHtRnqAAPKQVHvrWHnVnzojBNMWpliHmmQENbVKW5oRgyvinHN8HvtPGekBepCHxdqbjZwz3M1XhAsIhdJL+QFw53wMLZtK3o++uL8wsHkCPthQ+fYvz2b7EPvDLeefzvpZslK4DgVmjPQA3cg6oWb6BCuqHiNk4lzmIwjMd0BH+gI+uyCQPmK2GIgs5IEvcdT0FsHYRypZQb1tuoaAWDvdxIrBNiOEULQz4Eueg/a7HMjJFzDRLvAnf8D4IHj1XNpH1vaBEiPvLwMjhGrvL6DE6kGO/URtK2StCZR4A7VbZ49hXze1l2BtAUHNCvRgIo7aVrQmnkfxYWqTWcqxamovwXoELmKindS2ouXOJkw8AEH9URxEP3jubDVbFrGOJdJw6lojta1QtE9w1K1wamIDyLNXcD8eM1sW8WCBUzMbcXQR8KW+AO/tp4wYJvSn6lBgApqTL+GzCPfiAm2z4MECBC2xzZiwGfyZAWhL9IIvfQV9BeR0IW1X4k4cRDu1LVifQBY+LQ/OZnaAN/4cnPy3yIwCeDQel6qP2qSMO+f34/7sJq5VgJRjPTnJqwpkQTa3M53BAiihvvdmLgpcxAPYB97EAB5GnJ32G4wtbHHsGRQNAbf7Yez6LVJy7L1+8r4Ccuwb6Jq7ikk6zQiK4IHr0d+CgJ5DfTl2GvruVle93m+jAnZ75IlSx1A3WxEpYoRhIuCjHa2QZwtx5JPQMPUMJgniAaswW5ZDjstwaYF3vXG5bHGJbFKUZ8XQEO/6/RoGv6dBKxTNhzS+Oa2x91AkRG0rlFgvjC+8LBQPC0v3AMqkSGFZ5R/TnBhaWRUe7TVMOAmBG8YyECiaCh4UWoqOv5/E5RsEXX+E55d/7CgYYeh4edVfGWw4wbI/Gx8zAjnWiSM7bHoGziTfxbgKbp3soQFl9h0s3V5i4h1Rs0IA19+LS4UMHuGcY6NCqVoNI+ltEJiLY5X04EzOo1CPQe0sdOk6xg6Yr+NAtE+R9PRby5QC7wIfESE2I47u4u3hjuID16KFn02fzmn85yD0p2xweY6FH1MC+OMu6F2w4TK9Sl8mkOPNyEPEXEMg2EZouhR2W4iRbGNfC2Xj7aJtrKGiZPTgvlf6t+sAD5ld7sGPZ8GToh++tQRwBpYbzQQpZ971q8RJ0S9tzjEFl7CLk8I+Voo0IT/fszdal3/0+vHsnlhvNAoy+qV38j0OFhTbB/LIxm8Vux/H50abMLKNEyIC5xytZ8XRrzgx4rHbgm28Q9292p1MgSX63Rp/FRaqhAlGVGdwlLdw1jfIHwS2TaOfIH2Mvwp16j8XgsLTXWysIwAAAABJRU5ErkJggg=="

                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pln, self.ref_pln, self.tol = (None for _ in range(3))

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

            def xform_curve(self, cuvre_data):
                res_curve = ghc.Orient(cuvre_data, self.pln, self.ref_pln)['geometry']
                return res_curve

            def positional_relationship(self, sub_data):
                # 获取引用曲线
                origin_a_curve, origin_b_curve = sub_data
                temp_v, temp_c1, temp_c2, temp_c3, temp_c4, temp_e = ([] for _ in range(6))
                # 转gh内置物体
                a_curve = origin_a_curve
                b_curve = map(self._trun_object, origin_b_curve)
                # 获取转换过程
                a_curve = self.xform_curve(a_curve)
                b_curve = map(self.xform_curve, b_curve)
                # 判断两个曲线间的关系
                for index_curve, item_curve in enumerate(b_curve):
                    if rg.Curve.PlanarCurveCollision(a_curve, item_curve, self.ref_pln, self.tol):
                        temp_c2.append(origin_b_curve[index_curve])
                        temp_v.append(1)
                        temp_e.append('intersect')
                    else:
                        # 得到线的长度
                        curve_len = int(item_curve.GetLength())
                        # 根据长度取20个点
                        for par in range(0, curve_len, curve_len // 20):
                            # 判断是否在统一平面
                            par_pt = item_curve.PointAt(par)
                            if par_pt.Z > 0:
                                temp_e.append("They're not on the same plane")
                                temp_v.append(100)
                                temp_c4.append(origin_b_curve[index_curve])
                                break
                            else:
                                # 判断曲线中的点是否在封闭线内部
                                if a_curve.Contains(par_pt, self.ref_pln, self.tol) == rg.PointContainment.Inside:
                                    temp_c1.append(origin_b_curve[index_curve])
                                    temp_v.append(0)
                                    temp_e.append('in')
                                    break
                                else:
                                    temp_c3.append(origin_b_curve[index_curve])
                                    temp_v.append(2)
                                    temp_e.append('out')
                                    break
                return temp_v, temp_c1, temp_c2, temp_c3, temp_c4, temp_e

            def temp(self, tuple_data):
                a_list, b_list, origin_path = tuple_data
                a_list, b_list = filter(None, a_list), filter(None, b_list)
                # 子数据匹配
                if a_list and b_list:
                    new_b_list = [b_list[:] for _ in range(len(a_list))]
                    sub_zip_list = zip(a_list, new_b_list)
                    v, c1, c2, c3, c4, e = zip(*map(self.positional_relationship, sub_zip_list))
                else:
                    v, c1, c2, c3, c4, e = ([[]] for _ in range(6))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [v, c1, c2, c3, c4, e])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curve_A, Curve_B, Plane):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Express, Value, Inside, Intersect, Outside, Non_Coplanar = (gd[object]() for _ in range(6))
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_f2, curve_trunk, curve_path = self.parameter_judgment(self.Params.Input[1].VolatileData)
                    # 默认值参数
                    self.pln = Plane
                    self.ref_pln = rg.Plane.WorldXY
                    self.tol = sc.doc.ModelAbsoluteTolerance
                    # 默认值参数
                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['CA end', 'CB end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        a_trunk, a_path = self.Branch_Route(Curve_A)
                        # 数据匹配
                        a_len, b_len = len(a_trunk), len(curve_trunk)
                        if a_len > b_len:
                            new_a_trunk = a_trunk
                            new_b_trunk = curve_trunk + [curve_trunk[-1]] * (a_len - b_len)
                            new_path = a_path
                        elif a_len < b_len:
                            new_a_trunk = a_trunk + [a_trunk[-1]] * (b_len - a_len)
                            new_b_trunk = curve_trunk
                            new_path = curve_path
                        else:
                            new_a_trunk = a_trunk
                            new_b_trunk = curve_trunk
                            new_path = a_path
                        # 打包多进程运行
                        zip_list = zip(new_a_trunk, new_b_trunk, new_path)
                        iter_ungroup_data = zip(*ghp.run(self.temp, zip_list))
                        Value, Inside, Intersect, Outside, Non_Coplanar, Express = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Express, Value, Inside, Intersect, Outside, Non_Coplanar
                finally:
                    self.Message = 'Curve position relation'


        # Curve Divide
        class Equipartition_Curve_2(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Equipartition_Curve", "W113", """Curve Divide""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e925f200-887f-43ed-a802-767a7f1677a0")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curves", "C", "curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Espacement", "E", "Spacing of points")
                p.SetPersistentData(gk.Types.GH_Number(300))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Espacement_Endpoint", "EP", "Distance from edge point")
                p.SetPersistentData(gk.Types.GH_Number(300))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "Equalizing point")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Parameter", "t", "Points on the curve parameters")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPqSURBVEhL3ZVdbBRVFMfXSKK8GCB+QnkwFGxpt4V2u98zd+7szJ27M7Nf/ZilSESNxiYmKgaixgQfGoNSoy8+8KAxRh9MjUaiRo1ibSxYdlu2+8HStA2wTfkoVkAE/Iocz2wnRqOkIPrCL5nknv/9z567e8656/onWOp0M42NywIrrnSk/4aw3LfW523ZK7G3IdpxDiLmOEjRsTeIDnc6lismzPZx2Sx/7IQul8CyXtnMn29t2wDuZqtPMqY2Ez7yHu84DZT3z/l87rhjXRCBfZNWE0fxcPmL84I6eLdsHjobMScvUn02WBUdJH3KaPMmvmvzdQHVy0878mWh+ufbePspkI3ylJ8N1LrCRmGppOdLaqICmEh0fH9hxYramrDy6aBhXQBJL+wW2ODfaqPELywPBrvfDwkdIGnDXwfUvbdXN0QtE+cdp0BQhnqqwmUAgBukaK5PS50AapR/ldRdOwThQVFkh6jIR3fKxsTPsv4l1NcHX0X7ovm3EL9/32IxmnU74YKILEcj5sT+UCgNvuADwDvOAEvO4M+Xz0jGtObYrp3bbnGtWu95vJ3GDltiNH/FB/yD5wZgkagX6wnPd0p8bDs1Jl8LCY986PFqn5Bo7nVqzmyNxOcUWf7iDueVhRG08l3UnNoYDqf6vYH7vlUT06C1nwQ1cQRkcxI83p4fG90qdloBlPgR3DsBavIkiPIrsx5P4weitqc9bFSWOh83DyEDNxMt+xB20h7ZOAh65w/gDW6DhsbwfuzjHSRaSFIt10DM8Vv9nZcW2w9j08sIG6nD4saoefR5r39LpnmdDrz9GNai+AvR8++QaNHkfOImF2XDzQxbFBP8ZG/g6Sy96+onl6Qu1ch66X6c/M9wpvCgZ4Dw7GFXV1f/jdQ40EwSuSWO95qx7zCql7aIPLvTkf5nBJZZKccmVIFnmcBzLBLZzAXlJU3g5WpM+RAjJMUF9V2Mi/jYviKj6lYmqC//ScuhbxP6djFqVliYH1hbTYBf5SPDOg/2lGqpCvj9FILiszhE5zCeAxbPQFurG0T1LdS+R+04FvQ4BIMmBIQnUDuL2ixoyUnweQMQkl4AM/2bXYNj1QRUy9+jxMYtITqatotc18A3rPdtx/W4RfWcJWpfWatXt3b7hDdRO4jxCOoFq75e3bSupWej7RPRR/URq66OdHt8L6aV5Iwl6VlfNcH1Cw7hEomPPoW93SvyUq8oPdbrDz+M60KvrZHo2DOMlZY59qsnhEMYwaFR8VpQEzPgD9wLLZ4UKHiF2FeFEpsE+5/Qsf87gsrQchIr1dJkZVVT05NrmpoeXWOvbY3w4RrHdt3icv0OJT+5reclx+0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.Espacement, self.Endpoint = (None for _ in range(2))

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

            def Get_Curve_Length(self, Curve):
                """获取线的长度"""
                Length_List = []
                for _ in Curve:
                    if _ is not None:
                        Length_List.append(round(_.GetLength(), 4))
                    else:
                        Length_List.append(None)
                return Length_List

            def trim_curve(self, curve, curve_length):
                if curve.IsClosed:  # 判断线是否闭合
                    return curve  # 闭合线暂不采取操作
                else:
                    curve_length = math.fabs(curve_length)
                    r = curve.Trim(rg.CurveEnd.Start, curve_length)  # 切割线
                    #            result = r.Trim(rg.CurveEnd.End, curve_length-0.001)
                    return r

            def Get_Curve_Middle(self, Curve, Curve_Length):
                """求线的中心点"""
                Mid_length = Curve_Length / 2  # 将线的长度除2
                t = Curve.DivideByLength(Mid_length, False)[0]  # 得到线中心的t值(False是不包括首尾点)
                center_Point = Curve.PointAt(t)  # 根据t值求中心点

                return center_Point

            def Espace_Judge(self, tuple):
                """线的间距判断"""
                Curve, Length, origin_path = tuple
                Points = []
                if len(Curve) == 0:
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [[], []])  # 返回空树
                else:
                    for Lindex in range(len(Length)):
                        if (Length[Lindex] - (self.Endpoint * 2)) > 0:  # 判断线是否有点
                            temp_n = (Length[Lindex] - (self.Endpoint * 2)) / self.Espacement  # 创建一个中间变量
                            temp_d = -((temp_n - math.floor(temp_n)) * self.Espacement / 2) - self.Endpoint
                            if Length[Lindex] <= -(temp_d * 2):
                                mid_pt = self.Get_Curve_Middle(Curve[Lindex], Length[Lindex])
                                t = [Curve[Lindex].ClosestPoint(mid_pt)[1]]
                            else:
                                curve = self.trim_curve(Curve[Lindex], temp_d)
                                t = curve.DivideByLength(self.Espacement, True)
                            Points = map(lambda x: Curve[Lindex].PointAt(x), t)
                            ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Points, t])
                        else:  # 没点的线
                            ungroup_data = map(lambda x: self.split_tree(x, origin_path), [[], []])  # 返回空树

                Rhino.RhinoApp.Wait()
                return ungroup_data

            def Graft_List(self, List, Path):
                Tree = gd[object]()
                Path = GH_Path(tuple(Path))
                if len(List) == 0:
                    Tree.AddRange(List, Path.AppendElement(0))
                else:
                    if len(List) == 1:
                        Tree.Add(List[0], Path)
                    else:
                        for index, n in enumerate(List):
                            New_Path = Path.AppendElement(index)
                            Tree.Add(n, New_Path)
                return Tree

            def RunScript(self, Curves, Espacement, Espacement_Endpoint):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Data_Tree, Res_Point, Parameter = gd[object](), gd[object](), gd[object]()
                    '--------------------'
                    # 设置两个端口的默认值
                    self.Espacement = Espacement
                    self.Endpoint = Espacement_Endpoint
                    '--------------------'

                    re_mes = Message.RE_MES([Curves], ['Curves end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:

                        Tree, Tree_Path = self.Branch_Route(Curves)
                        for index, G in enumerate(Tree):
                            Data_Tree.MergeTree(self.Graft_List(G, Tree_Path[index]))

                        tunk, tunk_Path = self.Branch_Route(Data_Tree)
                        GH_Curve = map(lambda x: filter(None, x), tunk)  # 去除None值
                        Curve_Length = map(self.Get_Curve_Length, GH_Curve)
                        zip_list = zip(GH_Curve, Curve_Length, tunk_Path)
                        iter_ungroup_data = zip(*map(self.Espace_Judge, zip_list))
                        Res_Point, Parameter = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Point, Parameter
                finally:
                    self.Message = 'Curve Divide'


        class OffsetBySurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_OffsetBySurface", "W55", """The Curve is offset by the surface""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f48f06e7-1c78-4867-9da9-9e934c00ce2c")

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
                self.SetUpParam(p, "Curve", "C", "Curve to be offset")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Offset distance")
                p.SetPersistentData(gk.Types.GH_Number(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "Offset surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Curve", "R", "The result after offset")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                if isinstance(p2, Rhino.Geometry.Brep) and p2.Faces.Count == 1: p2 = p2.Faces[0].DuplicateSurface()
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARDSURBVEhLrZULTFtVGMevryyZ0UzjnBrkWRlQKOUxUCncdgx6C2UPEJaJE5sFppARhxinM5LFYbZpdJmPsIEjPra4mjkTI05UKq/20t6OPijQ1gmMwRiPSi2sW4f9PPf2MEAq4OOXnOR89zvf/zv3O9+5l/BHGsVsk2Tpg7C5JPcGnL9/fVzjI9hcGShBL0kx+dj0y0O8hrU8gfbgphzLFVFm52CooP1B7FoektJ3pFH6HGwu4vF0plAsMw2996ETBgZvgvKcGyLi6VaCUN6BlyyEomyr5PKh1XI5szoBDZSAEcv029k5+4z1EQTcxq6NTdYeS5JY4fyPLpjP4aNOiErU1HKC8yG3dK4hKR0tlhntqCw2dqASudGzYTTQXGeXZHXZxJTuRLhQfeLg2w4o3tML6o5JLD3H1h0DEMpvfhFLY6rg9vRsUygpN0WQmYxvSPUmsYwpm7Uzcgwh4cLW+r37riIZL1S8aoPGpgmfKsJscUHJnm4o3WuHp3baIZjfJMXq/iGlOhrtPAubRHBkS3LBs9aZSecfnOCRo/1Q+ZoN2ulJqNxvA2rbBaitv8z5eqwz8OQm428BYSoeDl8MKWW0pIzZik0iKkFtbmh0cwIsY+MeKKvohcJdXfDB8Usw4fBgj4/GphuwgWQs6wSGu7HEQlCCC2KZNo+dJ5MaRbyoF46f9O1wpRw4NA3CJzpQZ/khTcq0pWXqJATx9T0Zm42jdZ+MQkl5Nw5dGkvPdXjljRFIzzb0pEr1B7DkQjZu1KwjSdWdMckd359Ssu3ohc0FBtB3/u5T+QtW+zR89sUwlFYMQUqGcTwkii4jCOYuLOcfnkBdv6tsGLwIVuSb78YgXa6H08or0NTsgDNnR6Cq+iIU7bZA/k6jdwNphXiRXhWbrAnGEv4JCjq3JjpJd1bxwmXUej0oAbdJjp9bHVD+ci+6B91cF31UOwgGk9NbVT0GiamMkiDy/d/kWR5dr84RpjD2mpNOmJ6egacVZhi5egPLL4Z9uzNfTUFkguYnFM7d9EWIsk33SbLMuYmp+m+fKf4FNFr3rbIUlXT5vbGzdJquobLohh4OVz2A5RYjouioJLEB6j6d6/NZDr/bD9VH+rA1B5ueTby9qA9CBG1cOy9JRFxrrqJ0AFxTWAHTP+DmDlbV4uAul9HsgvdrLsFzu7tAkm1Hu6cbscTyBPKbXy97aRg8nhnf9wDDdkxeoZEbO9CZvHnoV9RRE5CV13WTH6eJxOErIyS67dRb74yxZ7AgCVsSB/4csOdTuX8UwqJbKnDYyuHxGlZFJtDa0186bx30fDweL+yrGofHYtvqcMg/hxejCogXMSPt9DSW9XGxzwPF5cPAE7TX4KX/nkB+U4ok2zjTN3AdXC4v1H8+BegXORkarX4eL/nvRMW1KwqKBiG3sPtauFD3cWDMD6HY9f8Rk0RvWRum/vsfx7IQxJ//TJMpdPgJpgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.j_bool_f1 = False
                self.j_bool_f2 = False

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

            def RunScript(self, Curve, Distance, Surface):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Curve = gd[object]()
                    # 组件只运行一次提取输入端方法
                    if self.RunCount == 1:
                        self.j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                        self.j_bool_f2 = self.parameter_judgment(self.Params.Input[2].VolatileData)[0]
                    else:
                        pass
                    # 偏移的精准度
                    tol = sc.doc.ModelAbsoluteTolerance
                    re_mes = Message.RE_MES([self.j_bool_f1, self.j_bool_f2], ['C end', 'S end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 判空
                        if Curve and Surface:
                            # 偏移主方法
                            temp_curve = Curve.OffsetOnSurface(Surface, Distance, tol)
                            if temp_curve:
                                Res_Curve = temp_curve
                            else:
                                Res_Curve = [Curve]
                        else:
                            Res_Curve = [None]
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Curve
                finally:
                    self.Message = 'Curve offset By Surface'


        # 将线段集合围合部分生成闭合曲线
        class MeshLines(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_MeshLines", "W112", """The closed curve is generated by enclosing part of the line set""", "Scavenger", "B-Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9972dae6-659c-4bbb-a138-c8e6400a5375")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                p.DataMapping = gk.GH_DataMapping.Flatten
                self.SetUpParam(p, "Lines", "L", "Line set, default flatten")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Max", "M", "Maximum number of sides for enclosed part")
                p.SetPersistentData(gk.Types.GH_Integer(3))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Res_Curve", "C", "Generate the curve of the enclosed part")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARFSURBVEhLrZV9UBRlHMdXGgnMmEqSZtKmaYiXAFEQ6DjYvd2724PjTocZqCY0GCtGGZw0IxyGYnyZJsJmEjWYyon4AzQNCRtiKtEiiLeDO+485VReCo69A0EMjrOc+fasrCUKosZn5vljn9v9fPf3e557lrpfFFpjDJPUGipdLiSpD8k05l1KnW2MTmx7VZpcGALoxqgYtbEl+eURrFW2/yBNLwgeAUzbe1yS+e8jO53o/diOLRt7EEi3VhRQBR7SPQ9GUHxTRBjb2bQ1YxBdhQJcJU6MH3JC2C9g+yY7ghVtJ/0Tah+Wbr8/yBvmKbRdf32V48DYQQeuHHLATsTiGCXXIwcE5GUO4QWFoT4w9tdHpcfmJ4RtDg9lOxuy0gdg/FDAVKkTjmIBQ0R8c4ghlw9MB+/ZIiCUNbRGMqd9JcXcyPiOnbr1Fncl6bX4lmI7RNmt8ltDRkjI1U8dKNoqIIzrsITE/7xSUs2E4duDFIkms2LdANJeOoeuD36Hu3QYl0nIXAE3h7PYgQkScnCbgNVc56WguF8CJC1Fq84Es1qzjYrXGmgSUMQmtG6KS7QiRtuBvekWXCgcgIsEiZK7BTlJCydLHDj8joAIldEuhqi0hmBWd9at0JoOS3nTKLnmz9a+IcAnpwcqnQFlm8/BQSQTZAeJu2e2AHGI6+QiIcfzBLCazmFa0+VgtaZ8SfsfDHPaS8W1nV9ROI5F5VfwdIYVaXoD6nIukn5Pb9PZAsQKxQ1h3DMIbVI3aLX1Oiszx0ramSjpxjWcpuv60s+vgqq9Bu+iIQSmmLAjxYiOXf032nb7+riIvCHfDpXSDL+ybXi2IhcKnekax5lSJO1MeFnDjri0AXgc+RNUzRSoYxPwye9HjL4D+16zoLdo8N/1EeU/5g6CVnZieflb8O6LhudgOCJ3V4Gjzzol5Z3w8qa60LdHQJ2YBPX1BKhvp+BRPg7f7AukDQZUZnff+AOefPcPyPhW+B7dDO/+aCy5KEPwgWJwausoqzbQku5OOO4nPzVrGH7qozFQ1S5QlaQaUokYtLhkBCtftyJdZ4WS68Kymgx4OlZhiU2OsH1fQB3Xa2fl5nBJNTd8XKOOXW+D15fjoL4hlYghR0lIrRvP5DoRrT+FqA21iMqswvK6DVhVWAZe3ndJRXc8LynmRyNrKI5+UwB1nIjFUT0J/2wBDJH7nknFI93xCN77CTTqQVLNeQvDNK+QHr03IiPbF/PxLabn3h8F9Z0LQeSQo5O/x7KGZHiRni+1MojYfQwqha2FYdrnP5NmQ8O2hDB6i3tNej9kG6vweLOeyKPgY+Qh234Kmhf762PXVd/7qTobCro1K1HTgyfrX4GnfTUea0+CPKsRfExfjX/C/gf7LtyOUm49EVkwXUF8Zosor6BALZJ+/v/wvOUJVmMaUqZ2Q0XbSqXphYVRGhI43urm9L/5SVN3gaL+ARl//is3r7FsAAAAAElFTkSuQmCC"
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
                    j_list = any(ghp.run(lambda x: len(list(x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def _get_mesh_pt(self, single_mash_face):
                # 判断各个Mash面为三角形还是四边形
                corner_str = ['A', 'B', 'C', 'D']
                # 循环获取角点的下标
                corner_index = []
                for _ in corner_str:
                    corner_index.append(eval("single_mash_face.{}".format(_)))
                return corner_index

            def outline_box(self, ptf_list):
                # 3f点转变为3d点
                pt_list = map(lambda x: rg.Point3d(x.X, x.Y, x.Z), ptf_list)
                # 转变为曲面
                nurbs = rg.NurbsSurface.CreateFromCorners(pt_list[0], pt_list[1], pt_list[2], pt_list[3])
                # 转为曲折线
                temp_curve = rg.Curve.JoinCurves(nurbs.ToBrep().Edges)
                if temp_curve:
                    ply_line = temp_curve[0]
                    ply_line.MakeClosed(sc.doc.ModelAbsoluteTolerance)
                else:
                    ply_line = None
                return ply_line

            def RunScript(self, Lines, Max):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Curve = gd[object]()
                    # -------------默认值-------------
                    Max = Max
                    # -------------默认值-------------
                    # 判空
                    if self.RunCount == 1:
                        self.j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    re_mes = Message.RE_MES([self.j_bool_f1], ['L end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将曲线成数组
                        Lines = filter(None, Lines)
                        if Lines:
                            # 确定线集合组合后是否都是闭合
                            curves = rg.Curve.JoinCurves(Lines, sc.doc.ModelAbsoluteTolerance)
                            isva = all([_.IsValid for _ in curves])
                            isclose = all([_.IsClosed for _ in curves])
                            if not (isva and isclose):
                                curve_arry = Array[rg.Curve](Lines)
                                # 生成新网格
                                mesh = rg.Mesh.CreateFromLines(curve_arry, Max, sc.doc.ModelAbsoluteTolerance)
                                if mesh:
                                    # 获取Mesh的所有面和顶点
                                    mesh_faces = [_ for _ in mesh.Faces]
                                    mesh_pt = [_ for _ in mesh.Vertices]
                                    # 判断各个Mesh面是生成三角形还是四边形
                                    pt_indexes_list = ghp.run(self._get_mesh_pt, mesh_faces)
                                    # 获取个体面的四点或三点
                                    res_pt = []
                                    for pt_indexes in pt_indexes_list:
                                        sub_pt = [mesh_pt[_] for _ in pt_indexes]
                                        res_pt.append(sub_pt)
                                    # 得到闭合曲线
                                    close_curve = ghp.run(self.outline_box, res_pt)
                                    Res_Curve = close_curve
                                else:
                                    Message.message2(self, 'Failed to generate, please adjust the Max input')
                            else:
                                Res_Curve = curves
                        else:
                            Res_Curve = [None]
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Curve
                finally:
                    self.Message = 'Generated closed curve'

    else:
        pass
except:
    pass

import GhPython
import System
