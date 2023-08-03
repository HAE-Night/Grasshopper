# -*- ecoding: utf-8 -*-
# @ModuleName: Line_group
# @Author: invincible
# @Time: 2022/7/8 11:04
# coding=utf-8

import init__

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
import time
import getpass
import base64
import clr

clr.AddReference("System.Management")
import System.Management
from itertools import chain
import math

Mac_Array = []


def _get_macaddress(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    Mac_Array.append(ipconfig_list['MACAddress'])


def decryption():
    select = "SELECT * FROM WIN32_NetworkAdapterConfiguration"
    arrInfo = System.Management.ManagementObjectSearcher(select)
    prop_list = [strInfo.Properties for strInfo in arrInfo.Get()]
    map(_get_macaddress, prop_list)
    Mac_Address = filter(None, Mac_Array)

    designer_names = init__.designer_database
    origin_data_list = []
    now_time = int(time.time())
    for name in designer_names:
        try:
            with open(r'C:\Users\%s\AppData\Roaming\Grasshopper\Libraries\{0}-KEY.licence'.format(
                    name) % getpass.getuser(), 'r') as f:
                data = f.read()
                origin_data_list.append(data)
        except:
            pass
    if len(origin_data_list) == 1:
        data_list = [i for i in origin_data_list[0]]
        re_reversed_list1 = data_list[0:10]
        re_reversed_list1.reverse()
        re_reversed_list2 = data_list[10:]
        re_reversed_list2.reverse()
        result_list = re_reversed_list1 + re_reversed_list2
        result = ''.join(result_list)
        try:
            origin_data = str(base64.b64decode(result))
            origin_list = origin_data.split('-')
        except TypeError:
            return False
        if origin_list[1] in Mac_Address and int(origin_list[-1]) > now_time:
            return True
        else:
            return False
    elif len(origin_data_list) > 1 or len(origin_data_list) == 0:
        return False


Result = decryption()
try:
    if Result is True:
        """
            切割 -- primary
        """


        # 点向式绘制直线
        class VectorLineTaking(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-PDWL", "RPP_VectorLineTaking",
                                                                   """点向式绘制直线.""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Point", "P", "直线起点")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Direction", "D", "直线大小和方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Whole", "W", "双端方向（默认开启，t），关闭输入f")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line", "L", "生成的直线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAD7SURBVEhL1ZU7SwNBFEY/gmm0CEGCTRobIf9TRRBSCAkEhLSiWSJ28RekThHxRR4QsLOxznruZALLYjd3Cw8cdu4Ul9mP2b1yoo33OI5meIs36EILz/Ear/AS82gl9HCGm1A5Y/F8or3Vi214Ys0X2AyVtI5PF6z5Eo9DJdXxe7dMp9zcqKHdpGT2sRSbu/HXyd2ovLl/LFvpjM6TQ+md0v/kd9KUbz8nl9O45Up2JL0+S51Yu/K/r2LyyW1Y2J+vjFssD2hDosgI3WJ5wu5uGXDP/BFt3BmV3BZreoF9/MAGujLEH5zjiW3AQXy6YAPapv8XvuEqOsBEpF9kxj9B98/3mgAAAABJRU5ErkJggg=="
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
                Direction = rg.Vector3d(0, 0, 1) if Direction is None else Direction
                Whole = 't' if Whole is None or 'T' == Whole.upper() else 'f'
                if Point:
                    self.factor = True if Whole == 't' else False
                    Line = self.create_line(Point, Direction)
                    return Line
                else:
                    pass


        # 曲线修剪（简化控制点）
        class CurveTrim_S(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Ext_Simplify", "RPP_CurveExtendTrim",
                                                                   """修剪曲线，输入负数时修剪曲线，输入正数时延长曲线.""",
                                                                   "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "一条曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "曲线延伸类型，默认为Line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "L0", "L0", "起点延长的长度，默认为延长10")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "L1", "L1", "终点延长的长度，默认为延长10")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "C", "曲线结果")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOCSURBVEhLtZbvT1NXGMf7hv8A3rm37k9Qs2xZg8h0Sxa14By4jCGblbZshkJFDDHIBqyACHOim7ODroTabbgG3CjCOoHSFHS2QoOM8UNlsACh8IIfgc/OvbsYCqVGjJ/kJvc+zz3ne5/ne85pVTU1NbS0tDy9mpqawp5fNKZyu928TFSSynZYXV1V7qKzLYHW1lYyMj4h/aN0vF6vEo2MSurb86LXG6ird1BSfoHE/QdwOp1KZjPbqsB0+gy1Njv3+oLc7uji/ZQUlpaWlGw42xTIo04I/N7VTWBgkLT04/wzPq5kw3khgT88Xjy99/gwLY2FhQUlG84zBRwOB1qtFm93txKB3FyT3CLvn/f5xlJLcXHx1i2KZvL09DTHM05Qdekq7x48iNFo5MmTxxQWnuf7Hxq4HxzgRKaOD44dk3Opqam4XC5l9P9ErcDn83EqO1e0wseDwSHKLlajSUpCrY7HecuFy32H2Lg4SktK6OjyYL5Qyf633wmrNqpAb08PmbpPabvThc//gD4h0tlzV0x0kavXLBQUFmHQ6xkcGmLXnj2czi+gqMRMdVWVMsMGgYmJCebn55UnCIVmSU4+wnVrPcGhYfxixfT99TcDI2O0d3ZxUuyHBrudz7KziYuNxXGzmY+1mdjtDcoMEQSGh4eZnJxkeXlZjjU3N7Nr926KyyqoqP4KrU7P0ZRUyiuruHS5ht5AH3v3JaIznOJWq5t9iW/xrxi/RkSTJZHR0VHZZInHjx5hNpu5Ik5eqW0pQqDOdoNzRZ+L3VzBj84m7D872ZuYiNVqlcessaUH0mEWDAYZFxtorZrFxUUMhiyMuXlY6+2UiSrU6jc5qdOJqlKwWCzye+uJarKEJOT3+5mamiJd7Fjpy60NN7j87TVh6JfYbDZmZqYJzc4qI8KJKNDf34/H46FbLLe5uTk5VldbS8G5Im42/cqOV3ZwpuA8OXn54quvy/mt2CQQCoWIiYlBpVLJV2lpqVxF/tmzYvLfOCDW+c6dr9LW4UNz5D06OzuUkZHZZPLMzAxp4mxJSEiQhTQajeyBMScH+0+/cDgpmUqxsyu/vsKhw4ee+rMVmypY/0s1MjKi3EFjYyOvvf6G6P13fGEuRx0fTyAQYGxsLOy9jTzT5PW0t7eRlZWFyWRi8OFDObaysiL7JC1taZVt5LkEoiFVvr76NV7yvwr4D6Ki6GWRgrKXAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.curve_type = {0: "Line", 1: "Arc", 2: "Smooth"}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Curve, Type, L0, L1):
                try:
                    if Curve:
                        L0 = 10 if L0 is None else L0
                        L1 = 10 if L1 is None else L1
                        Type = 0 if Type is None else Type

                        curve_l = eval("rg.CurveExtensionStyle.{}".format(self.curve_type[Type]))
                        if L0 * -1 > Curve.GetLength() and L1 > 0:
                            Curve = Curve.Extend(rg.CurveEnd.End, L1, curve_l)
                            Curve = Curve.Trim(rg.CurveEnd.Start, -L0)
                            Result_Curve = Curve.Simplify(rg.CurveSimplifyOptions.All, 0.1, 0.1)
                            return Result_Curve

                        if L0 > 0:
                            Curve = Curve.Extend(rg.CurveEnd.Start, L0, curve_l)
                        elif L0 < 0:
                            L0 = -L0
                            Curve = Curve.Trim(rg.CurveEnd.Start, L0)
                        if L1 > 0:
                            Curve = Curve.Extend(rg.CurveEnd.End, L1, curve_l)
                        elif L1 < 0:
                            L1 = -L1
                            Curve = Curve.Trim(rg.CurveEnd.End, L1)
                        Result_Curve = Curve.Simplify(rg.CurveSimplifyOptions.All, 0.1, 0.1)
                        return Result_Curve
                    else:
                        self.message2("C端不能为空！")
                finally:
                    self.Message = '曲线修剪（S）'


        # 多折线按线段序号偏移
        class OffsetBySerial(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-多折线偏移（按线段序号）", "RPP_OffsetBySerial",
                                                                   """多折线按指定序号进行偏移""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "多折线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Indexs", "I", "多折线序号")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移距离，默认偏移10")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "R", "偏移后的多折线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGZSURBVEhL1dQ9KEZRHMfxx7vyMlAmUmSwkSQWKZOJQSIlKdlsGEwWpWQwSCkGT7FYWIjJIIVBkTJh8VImJRn4/q576uQ59+ne2zX41aeec+5z7j3n3Hv+qT9KCXpR57USTh6O8IVXdSQdzf4TeoBESicW0O613FmBbvyEHXWETQU+oMFvKMLvLEPXZ1GmjigZhVm2rKIcJktQ/5zXipAczECDL7GLbb/9AG3Dmd+eR+h04ARX0OAN2NvShnvompwjdDTrC5jBW3DF3ja93MAUoAbFGMYtzEDpgyu5mMA0StXhShW0vHeYJWuv+6EZBt08dAZgz1btRFOLO+jm6+pIIBm1qBKtPz+zph5j0KSCErsW6VA9QgO1YvuQ2Yldi3pgBkkDXHHWonGsodlrZUZflGb1ghvoBvsohB1nLeqCmdUzRtCEFmxiD7p2jGroEA75fYcwpzuwFnXDPCDIAXSo7AxC166hkqLfgbVoEmloNY3QlpzCPECrckXbav4TqRYp+nQXMYV8dTiid2cekLUWxU2oWvSfk0p9A8GZfDm6ge+4AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.curves, self.pts = None, None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

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
                            if sub_dis_list[count]:
                                new_item = c_item.Offset(curve_planar, sub_dis_list[count], sc.doc.ModelAbsoluteTolerance, rg.CurveOffsetCornerStyle.
                                None)[0]
                            else:
                                new_item = c_item
                            offset_line_list.append(new_item)
                        else:
                            offset_line_list.append(c_item)
                        count += 1
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

                    trunk_list_curve, trunk_list_index, trunk_list_dis = self.Branch_Route(Curve)[0], self.Branch_Route(Indexs)[0], self.Branch_Route(Distance)[0]
                    curve_len, index_len, dis_len = len(trunk_list_curve), len(trunk_list_index), len(trunk_list_dis)
                    if not (curve_len and index_len):
                        self.message2("C端、I端不能为空！")
                    elif not curve_len:
                        self.message2("C端不能为空！")
                    elif not index_len:
                        self.message2("I端不能为空！")
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
                                self.message1("第{}组折线偏移失败；原因：下标与偏移距离列表不相等！".format(_ + 1))
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
                                        self.message2(
                                            "第{}组第{}根折线偏移失败；原因：被偏移的折线必须为直线！".format(_ + 1, sub_index + 1))
                                        sub_res_line.append(trunk_list_curve[_][sub_index])
                                    elif temp_res_lines[_][sub_index] is 1:
                                        self.message2(
                                            "第{}组第{}根折线偏移失败；原因：输入下标大于折线段数！".format(_ + 1, sub_index + 1))
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
                    self.Message = '多折线按序号偏移'

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
                                                                   "RPP-折线偏移", "RPP_PlineOffset",
                                                                   """折线段分段偏移，三种不同的偏移模式""", "Scavenger",
                                                                   "Curve")
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
                self.SetUpParam(p, "Curve", "C", "原曲折线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移的距离，有几个折边输入几个偏移距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Simply", "S", "端口默认关闭，开启（t）后是普通的偏移")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Double", "DU", "端口默认关闭，开启（t）后将偏移前以及偏移后的折线首尾连线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Rescur_list", "R", "最终折线")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIOSURBVEhLtZa9a5NRGMUDikUtQgtiV9sUIZA0398lXZ0stQl0cXF1URQk4KLoJDiIpdX/QeoqCnZooYXODg5FoYMlVSndCsbfKccMmpY3cj3wcN97bp7zPPfc9yaJ/Q+kUqnzlUplNp/Pj5sKh2azeSqXy72vVqtdxm+mj0ehUBgrFov30un0VVMnAtFz2Wz2kJyuipjuD3ezXqvVukogcdpLxwJbFkulUpfGvpL72nR/JBKJM4h2lECikrTtN4ytcrk86o/1wGdf1et1NfKAhi6YPhkIXkNwh6R9YolCuxygCv5UMeIG8YL5OkUl3nZqdCDQVHImk4nbthlZwdgRrx2qKOJvnTIYZIfsQeCpqSM0Go3TFHquw9Q5/bk+EEheIz572kM8Hh+iyEN28ziy7/2AwC3ZgdgVU2FBd5flNbu4ayo82MUnCmx5Gh6IP9KFYyeXTP0b8Pk6Yi1Pe+BNSut15GtjwdTgwIbbElHw/IyOpxAe063WOoW/MN9inDhKGBSILuswZcXvS6Q7AH+A6EfG7+IZtyk67LToQKTt7je5uXOM88R94iWxpoIKnmXVRadFA52dxf8OyR9M/QXWnlBgg/Gmqeig4zv+oSiaCgddebz+gUWrpsICa9o6PAqUTIVBMpkcwZJ3Ft80HQ6ItuS7XkWe9/SPwEthwKs2yQ72VIQCK/pB8VIAxGK/ADVGu47UwxZAAAAAAElFTkSuQmCC"
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
                    if Curve is not None:
                        Simply = 'F' if Simply is None else Simply.upper()
                        self.factor = Curve.IsClosed
                        if Simply not in ['T', 'F']:
                            self.message1("请在S端输入正确的字母！！")

                        if Simply == 'F':
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
                                self.message1("距离数据列表必须和多线段数目相等！")
                        else:
                            res_poly_line = ghc.OffsetCurve(Curve, Distance[0], None, 1)
                        Double = 'F' if Double is None else Double.upper()
                        Rescur_list = self.double_line(Curve, res_poly_line) if Double == 'T' else res_poly_line
                        return Rescur_list
                    else:
                        self.message2("请输入一个折边")
                finally:
                    self.Message = '折线段偏移'


        # 圆弧拾取
        class ArcPick(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-圆弧拾取", "RPP_ArcPick",
                                                                   """简单圆弧拾取插件，通过参数修改，重建一个新的圆弧""",
                                                                   "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "曲线数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "筛选曲率的精度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "指定该圆弧的规范半径（通过半径筛选圆）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result", "RC", "最后得到的圆弧线段")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHKSURBVEhLxdVPKGVhHMbxGyJp/G1iFjaSLCxmwSgWRNlIRMrKjmQzCwtTYkbkz1YjaxssbJSsbChZiCwQio1iwUKmZmQz833ee97rHe657j2uPPXpnt8573nfe95z3nNC751JTKPYVG+QZfzFHWZRjqSmERrAukcRlHZ8Dm8GSwdO4A5wjkxkOftWUYWEMgrbwYWz/RVKDjRlV7DHBhBXvkEnaDp0FSVe/Rt5cJONYdhBfiBmaqCGD6jXDi+7mAtvRk0T/kDndmqHX3agRn2mekwu0sKbvtFN17nXUPtnqYMa7JsqWBahPgZN9SS6aTrYY6pgqYD6OEaKdrjZgw6Wmip4DvCsnwzc4BZ6zl8TOxPNpvLyAb9wiZdupl/GoPWzBA3QgkjUqTrXs65FFCTzUMfWGv57ZLehA7WmSjx6R2kW3EEkkl6M45OpgsV9xZyhG0mN7uUGprztqNEVbOEIh96vFl8hkhLdA3cOZQV6RftFi2oBI0jVjlj5ArfzU6TDL5XYhNpqLRUgZvTxcAcQTdME2qArbEA/9LGxbfQmKMOLsQPoX7V6v7aTaPSvv0Nvg7iSjxl8NFU41RiCVuk6tIh+ogtq75NQ6B8itYJa+UxZQQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _judge_curve(self, index_curve, curves):
                for _ in curves:
                    if isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Line, rg.LineCurve,
                                      rg.ArcCurve)) is False:
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

            def _join_handle(self, curve_list):
                temp_line = [_ for _ in rg.Curve.JoinCurves(curve_list, 0.001, False)]
                false_fun = map(lambda x: None if x.IsClosed is False else x, temp_line)
                temp_line = filter(None, false_fun) if filter(None, false_fun) else [temp_line[0]]

                explode_line = map(lambda line_single: ghc.Explode(line_single, True)['segments'], temp_line)
                filtered_curve = map(self.filter_by_line, explode_line)
                rebu_cir = map(self.rebuild_circle, filtered_curve)
                return rebu_cir

            def RunScript(self, Curve, Tolerance, Radius):
                try:
                    self.tol = 0.001 if Tolerance is None else Tolerance
                    self.r = 5 if Radius is None else Radius
                    tree_leaf = [list(_) for _ in Curve.Branches]
                    if len(tree_leaf) == 0:
                        self.message2("曲线数据不能为空！")
                    else:
                        filter_list = []
                        for _ in range(len(tree_leaf)):
                            if len(tree_leaf[_]) == 0:
                                self.message2("第{}个曲线数据为空".format(_ + 1))
                            elif self._judge_curve(_, tree_leaf[_]) is not None:
                                self.message1("第{}个曲线数据模块有错误数据！！".format(_ + 1))
                            else:
                                filter_list.append(tree_leaf[_])
                        join_curve = [_ for _ in ghp.run(self._join_handle, filter_list)]
                        return ght.list_to_tree(join_curve)
                finally:
                    self.Message = '圆弧拾取'


        # 线段点线转换
        class Dotted_Line_Conversion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点线转换", "RPP_StartToStrat,EndToEnd",
                                                                   """曲线集的起点和起点连接，终点和终点连接""",
                                                                   "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "多条曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Start_Curve", "S", "起点的线段")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "End_Curve", "E", "终点的线段")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "A", "所有的线段集")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Tree_Result", "T", "线段以树形结构输出")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKRSURBVEhL7ZVdSxRRGMcn7YXuoigtKbtQdua8zKys2gqFppvRi0ZQmIEKBQUR4VWQXvgJuugTdNvMOTOzb5Rd+QW67CbBnT0zs7rr2ht+gOmc5RCoa6640U0/+F88589zDnPO8zyj/GdfdL1fPoYI6wWO32/kNvpV20fSag7Q9vugHcxCNxiCueqQRtgcMP2T0j44qh0kdVK4JENFNYu3dOL14Gx5BNjBcD1ppDiiZ6rD2GIJZSFqkan1Uc1wQCfB7wMgKd7Gpo9Rutorrq6esLuagNlqn+awO4gUX6BMuU2m7wRYYRxS/yWww3Gcro5DyuaNt94Jae8JdMPz0PKeDS4sHZZL24iiFsNdu6jRoDueW++Opdk56TQMsv27iHqqDJsPpmEKu/w99guw2GW8uPkQmmxCz3+bQmRFl9YWAA2eqE54SoaNIxJRtqqizEobypYHAPEnpVVDbAoIm4GEjcql3dFI2ANIOMOrY0pf/DktSlDcbfK1f1z4hvmlAzvBDeTwquM+zG1M8+J4rNpesrbBn9AoSyHiPxIPDKzPRxOfoiOKZbWKL9BzX5Fh+h3YLV3hTfngvhW1Cn9wKdqlarbRZS6fBjZ7KsMt1JpwcXOCN9c9/OHHJO9yKK3G0XiTQepdlWHzge8KBuLjQYYNA6zSBZwOY0Ki2eTyTsQ0BdR/HudXJZf2BFheu+h46K6NwSwX9eb1j2tnpL0TjRY6ocVmNerdBPnvcT5djXriG8eBG8Y1Pgx5BV2X6Qo/bCzGp4EM69P1hv8XeAnCbGVU1HVdOUKVUfHvQDa7JlNrB2j51U4ZHhzVLp5FNHiF0+UUzpdTkHhzIF9pl3YTiKJD0FnV9PR6jxCipb836P4BivILbfdLrpUGntoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def get_points(self, origin_curves):
                """
                分解线段，使得线段集的起点和起点连接，终点和终点连接
                """
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
                if Curves:
                    Start_Curve, End_Curve, Result_Curve, Tree_Result = self.get_points(Curves)
                    return Start_Curve, End_Curve, Result_Curve, Tree_Result
                else:
                    pass


        # 合并曲线
        class CurveJoin(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-合并曲线", "RPP_Curve_Join",
                                                                   """曲线合并操作（多进程）""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "一组集合线段")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容忍度")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "New_Curve", "C", "合并的折线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFzSURBVEhL7ZS9S8NAGIcTtYIWQglCodSCDn6BLQhWoZ3UTUHBxcHFVSfFRUQ6uyhtKc010qYpYglFUKE4BpGKg6Iu3Ryk/0Ln+HvPDOJ65yD4wEPud29IjvtS/jon/lM6A/ASWjxJQvWfo/ABHvIkim3bQcs0k35cgm9wnSdRTNMMX1Qqi57n9SPuwCcYp5ow1VJprFGvp/DxXsRTeAt1qglRq9W0smHM3DWbcV3XNXRdQYMXRcFo1TJj++/t9jgiLeYj3KOaEIyxABykHzDHiQ2FwxvofobL/AVRzvL5iMXYAbU3FSWBib5Hc4KyMKVsNnperaY7nc5wIhjcPQqFVj+iUTpI4piFwuS146QxNX2IuYCq3sxrmvhO8RdztuW604ghSFswRzVhMplMj1UsJrvdbgRxCtLh2aaabNbgK1zgSTJ0UbXgCE8SoWNvwwaUs1O+QXPuwmOeJDMHX+AWT5JZgXSHp3j6BWj0sa/mPz9RlE+HX2apIbtNQAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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
                    if curve_tree:
                        zip_list = zip(curve_tree, curve_path)
                        bole = ghp.run(self._join_curve, zip_list)
                        New_Curve = self.format_tree(bole)
                    else:
                        self.message2('C端数据不能为空！')

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return New_Curve
                finally:
                    self.Message = '合并曲线'


        # 最近点连线
        class PCLINE(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-最近点连线", "RPP_PCLINE",
                                                                   """几何图形到指定线段的最近线段""", "Scavenger",
                                                                   "Curve")
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
                self.SetUpParam(p, "Geo", "G", "一个几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "RefCurve", "C", "曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Line", "L", "几何物体与到这条线段的最近点的连线")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Close_Point", "P", "最近点")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAC8SURBVEhL7c4xDgFBFIDhpdNrFUIlEkJBI1xA4Qg6jWh0DqCj2U7vBiqlQi0OIApR6ESl4X8zppCdlek070++7MzuvOxEmqb9pxw6qJpdeDW07DK9Ck54fcQIaQU3s0ce3na4oYsxZECesu95yPsp5NwcAzywRqIMnliane0Md7NfrnDJj+52mWwL+djHDDI8RANND3k/gpyboI0LNvBWwhHuZnKbkBZwMwcUkFoWdRTNLrwyZE7TtK+i6A0ySS+PMwgz8wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._switch = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

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
                    if Geo and RefCurve:
                        new_point = None
                        if isinstance(Geo, (
                                rg.Line, rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve)) is True:
                            new_point = self.__get_line_curve(Geo, RefCurve)
                        elif isinstance(Geo, (rg.Point3d)) is True:
                            new_point = self.__get_line_point(RefCurve, rg.Point(Geo).Location)
                        else:
                            self.message1('电池不支持此几何类型！')
                        Line = rg.Line(new_point[0], new_point[1]) if self._switch is True else rg.Line(new_point,
                                                                                                        rg.Point(
                                                                                                            Geo).Location)
                        Point = new_point
                        return Line, Point
                    else:
                        self.message2('请确保参数正确连接！')
                finally:
                    self.Message = '最近点连线'


        """
            切割 -- secondary
        """


        # 求线长度
        class LineLength(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-求线长度", "RPP_GetLineLength",
                                                                   """求线长度，并保留规定的小数位。""", "Scavenger",
                                                                   "Curve")
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
                self.SetUpParam(p, "线段", "C", "求长度的线段列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "小数", "N", "保留*小数.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Length", "L", "线段长度.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANNSURBVEhL3ZVrSFNhGMe1peC84cp9E0RFkkCdmxeKMMGEJIn64CeNvGUhigvbDDTXCAKR6VrDVoqj0DRNJdNQ0ayJ5WXzwtQd3VxhmiCKt12aep6e404fpAy8QNAP/rznvM//fZ7nvOflHId/QlxcHCs/Pz9erVYH0FNHC5fLFXl5eYFCoRikp46WiIiIhziAVCrV2meOGCzwAAeQyWQj9pkj5v8pUF5errHP7A0AOBIEESSXy6/y+fzclJSUwrS0tMLa2tpckiRdadtufhUoKSmZqK6u9lOpVH6YyMketaNUKrkJCQkSf3//CU9PT5LJZIKrqyuwWKwdicViXAJc2r4bDodTjANQcnJygqCgIBgeHuZTMTxZUeHh4W9dXFzAw8MDYmJiQCwqgraWZhjTDNj0hHbOoBs36KeJDnwCd2rNb0gkkqzs7OytpKSk7eTkZBAIBD/MZnMej8e7i52S3mw23CssAOO0DqxmE3yZX4Iu9TTUdGq2q1r7TfXdwyvG+SVic9N6iU65G3w0Blb3RwWgfFBncdv6qVBaaiosLnyDtXUTVLzpgysFzyH8hgyibsrgwu1nEC+sAl6mHF60q4EkbUX2jH+hrq7Oxdvbe9DZ2RlqaqqpfYX6riGIzlEAL0MKwseN8E6lAfWoFghiakFvMBjwenV27rsFGztHp/kzmIvp6+vbT73Ajx968JYEgbwZTl2TgOBRPeim9LBpXvmEiW6hglHuaDqOIxvlQ6fZm8jISCWDwYC21rebJLlNZhbXQUhqKTR19oFtY9mISRJp6/7JycmJxwFEIpENEy0WKFrI4JRS6Pmswb3dasVOT9qdBwAXO7LZbC0nLAyTkbPN3YO209fLoLGjD8htawfGj9HWg5Genn6ZOv8N9a8WNkxW40WhEoSyBrCuLc1gQQ/adnACAwPbQ0NDqe4HK5p7rdQR1BFT2Dicpy0HZ2RkhO3m5ma5k5dnwgITifdfgriyFSzry2205XAIhcIE6m/2vqvDMDo9O3cm6wn0Do1R3cfSlsMRHR2987tcWVwYl79WWWL5T2HGoJ/FAgzacjjKysqk+C2ivjGVA6OTq0OTX2F1ZbmJDh8e3PcT1HagmHgdgspABdLhfeLg8BOC7AQKjrtfNQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Curve, Number):
                digit = ".%uF" % Number if Number else ".1F"
                Length = [format(float(crv.GetLength()), digit) for crv in Curve]
                # return outputs if you have them; here I try it for you:
                return Length


        # 根据线长排序
        class LenghtSort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-长度排序", "RPP_LenghtSort",
                                                                   """根据Curve的长度进行排序，从小到大。""", "Scavenger",
                                                                   "Curve")
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
                self.SetUpParam(p, "Curve", "C", "需要排序的线段")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "排序后的线段")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Length", "L", "排序后的长度")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJGSURBVEhLYxgeIDQ0lD8oKKhp4cKF8VAhhn/XnIX/3TPK/3czXBMqRD4IDw93ZmVl/V9QUPDh////bCCxfwdZzP6/Yv//74xeCVgRJSAxMdGFkZHxf05OzpN///6xg8T+HWQw+n+D+f+/0zq5YEWUgPj4eGeoBY9HLcAK6GZBYWHhQ6gQw789DHr/bzH//39KPw0qRD4AWcDExPQfSL+ZMGFC8Iw5i73/XbZz/HeJ6e+/U4qd/69IGfw/o6MBVU46iIuLcwNS/0EYZJGcos7/B6e75/8/xvD//xUgvgPER9iAeaSeBayBVLBhwwYTYPj/T0hI+A+07H9ZRe3/h9d3dvw7r7Lw3znVTf8uqW3+d1Zn1v//DIwREXF6np6eM4Dq7KDaiQPAHOwAjOAYKA4D8nmgUijA3d3dVl9f/7+Ojs5/c3PzS15eXjVlZWWUFycwMHv2bCFnZ+e1BgYGH9TU1P5raWn9B1r4x8bGZm9AQEDqjBkzJKFKEcDKysrNwsLiqKmpKUFsbGx80NLSchfQwOeampr/VVVVwRhkGchXQPkPQLk1vr6+McXFxWJgCzQ0NOJBikGKCGGQYYqKij+A7K/q6uoo4iAM8pGhoeF/Dw+P7VVVVUZgC4CCPLq6ukpABQQx0PU6wHioAfr6GtBhcEOBwfTP2tr6YGBgYFZvb6802GByQEhIiK6ent5/kOuBjgJF9BWghY15eXk6UCWUAWBE2gBd/woY0XOio6MdgKmNCSpFHdDZ2cl77NgxISh3FFAKGBgARSNMAzVxb5MAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            # 排序
            def CurveLen(self, Curve):
                Length = [i.GetLength() for i in Curve]
                CL = zip(Curve, Length)
                AREAS = sorted(CL, key=lambda x: x[1], reverse=False)
                return [_i[0] for _i in AREAS], [_i[1] for _i in AREAS]

            def RunScript(self, Curve):
                try:
                    Curve, Length = self.CurveLen(Curve)
                    return Curve, Length
                except Exception as e:
                    self.message1("运行报错：\n{}".format(str(e)))
                finally:
                    self.Message = 'HAE 长度排序'


        """
            切割 -- tertiary
        """


        # 曲线取值
        class DTS_Get_Vale(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲线取值", "RPP_DTS_Get_Vale",
                                                                   """分解线段，以及下标取值（S为边线，V为点）""",
                                                                   "Scavenger", "Curve")
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
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Curve", "C", "将要分解的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "分解后边线或点的下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "S_V", "B", "选择边线或者点，默认不选为边线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data1", "D1", "第一组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data2", "D2", "第二组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data3", "D3", "第三组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data4", "D4", "第四组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data5", "D5", "第五组数据")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEESURBVEhL7dTPKsRhFMbxcw2MEjsLFmaJ/EkhUSSKhR0LaixYiRKiRLkQpUhRrocFFi6B8H1OM71v78qcncm3PovzNDO/mqmx/37bDu6w5VdqGw94DLhHDbaK78wiVLlH2XkxHEKVe5T14aV+PKMHKt+jnuB1YBrtfqUqmMVcwAza0CJN4hjjfqUmcIqzgBOMwaaQ/zCjUHpovkfZZTHoyarco/xraRyfGILS/oX8xc36gDeCXQz6lRrGPg4C9jCAFqkbC+j0K9WFJSwH6E/TP6+Kd+hHeUMvVD8ae9Qr7CIb5Aiq3KNspRjmoco9ytvEFdb9Sm3gGre4aYJer/et4U9n9gNMCfCsAWct1wAAAABJRU5ErkJggg=="
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
                if Curve:
                    curve = Curve.DuplicateSegments()
                    C_List, P_List = self.get_v_s(curve)
                    I_List = [list(map(int, re.split(r"[.。!！?？；;，,\s+]", i))) for i in index]
                    New_C_List = self.index_erreor(
                        [self.subscript_value(C_List, I_List[i]) for i in range(len(I_List))])
                    New_P_List = self.index_erreor(
                        [self.subscript_value(P_List, I_List[i]) for i in range(len(I_List))])
                    if S_V == 'S' or S_V == 's' or S_V is None:
                        data1, data2, data3, data4, data5 = New_C_List
                        return data1, data2, data3, data4, data5
                    elif S_V == 'V' or S_V == 'v':
                        data1, data2, data3, data4, data5 = New_P_List
                        return data1, data2, data3, data4, data5
                    else:
                        pass
                else:
                    pass


        # 曲线筛选
        class FilterCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲线筛选", "RPP_FilterCurve",
                                                                   """通过曲率选择曲线""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "曲线列表数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "曲率容差度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_Result", "CR", "大于曲率的曲线（曲线结果）")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Line_Result", "LR", "小于曲率的曲线（直线结果）")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAXKSURBVEhLvZVpTFRnFIbHWqw1cQlKbP1RjSIqahNcWgtpamraAAVRa7TRqijUphWVaqxLYht+WNQuSoKlwaXVBqg1FoVUU8cFi0pLXRgGZmUQmGEYmH25y2y8Pd83opa2pr96k5N7595zznPOe86XUfyvV3V19SSlUjkZ7nuTlh+/kDz6i8aUcSV1KaOLlSmKDcdSdpccT25oaOA+/2b19fWTa2pqXniQMnYtWLDg2e7u7tPBYFDsj0ryJbVFmlh0NzpulxrjttYjbu1pbCw9D6fTERVFUfL7/fKTLBQKBTo6Or6m1E9zQF5eXpogiGDXdVMvnj+oxvCdOozd0oJhq64hf/85SF4Hfe0HBT/RqEiex2azhefOnTudA97NzX0DARfqKPmYw3ehOKjBiGI9hmxvwnulVyH7neiPRkDVQ5Kkvxl7z0wQBAQCAYTDYZAigdmzZ8/hgH0frl5U22jA+C/VUHyuwdBSPRT7VNhwvA5BSk7ZIcsyomGqLhpChO7s9+M2AGKQSCQCs9n8CPDimu3LJhap8MweHYYfoOTFKuSeqkOIumKy9EdC/O4JyGjv8cMvyFyGaCTMJWH2OIB18AAwlwNG5pfmJuwxIH5rKxQ7VFh/gir32hElWSJhGQFRxu4fjEjadhPPbVRixpZL+KSiCTIlDofkh9INBsyaNWseB4x5/9DahMJGDFt9HflMc5acqhOFAFUnYcVXd6BY/jNGrruI+NxaKJZUYfjS77G59FfyC0Ig3VlyZmwGbNidnZ3CzJkz53PAiDX71w3LrUZecTVETx9PzipBRMSZehMUy85ibO55JKyrxpAlFZhfWIMOmwfLPq1F7U09SUgQ8h8MSE5OfokDnsr6eH1+aS38DivCQZIkENsGQMa28gYoFp/CuNVVGJJ9AnMKzsLcY6dvYZScacCub67wZwZgRueAz4TOgTBjxoyXOSAta+UqqzWW3Ofz8eQxQBDbyuqgyCiDIv0IUj6oRJfFhqDgAW0ASk7XY2+5kgMGYlg826r29nZx+vTpCzhg+dLFb/XaeriD1+vlVbDn/oiEHy83QfHKPiwsrISluweS3wW3y4GQ6MObm8txob6Zz4H5szgWzwZuMpnEadOmpXJATk5ONutgMIANT/C5kbntO6wrqoKtx4q+vl5oje1YveckNh84g0gopvtgQFtbm/QQkJ2dnWOxWLiDx+P5i0ySGIDLaceOQ9VILyjDil3fIvujcnx27CJCMlvPGIDFsjgWz4ZtNBqlpKSkNA7IyspaQnvLHdxuN6/iYVVkbF0RlWHrc0BrMsPlcnPdxQdDZX4slsWxeDZsg8EgTZ069dV/BLAqmDP7zWwgiUzVhuhcSGJsy3gB9I0Z82dxAwC9Xi8/BGRmZi7r6uriTi6XC15yDIpeiAHqxBcLFOg5JPkRlgkkMjlIa4GBfXReJHpHUlJnLJ4BdTqdnJiY+BoHZGRkvE0Hg9NdLicN0o7Ldy24Z7DhvqWPvzd09uL31m4o/+jEHU0XBL8Xan0XrW0Pzly8DZWmnb9zOBy8a61W+wiQnp6+nA4Gp/vcdtQ09kGp9uCW1onzt50Q/R4cu+bAwRormtocOFqrQcWFJhyq+A07D/+CVdurkL2lEu2dVlphJ1dCo9EEp0yZspADSKIVrAOn0wmPsxfnbnugpA6ajVZU3rDjpzo9Co9qcfKijmbrgbm7F/PWnITylg57j1zFO4UVKCpTwtbbB7s91jEBQrRFr3NAamrqSvoH4sPxelywu3y40uqDzuzFfasbZ29YcP2eFRpTD/ykvSj4cONuB5ykua3PiYraJqi0Zj4TpgI7yTQDTJgwYREHxMXFpZSUlNDg9VA1N0PdrIJR2wxtqxpajRodbRqYDBoYdBq0tLRwMxm1aKW7VtOCrvsG/k2lUqGZ4lny4uLiRkqdyAF0DSVLi4+PLxg/fnxBQkLCJmb0/J/tsZiCUaNGbaJ89GejGPInDRdeIfUoK/YAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def find_curvature(self, o_curve):
                start_pt, end_pt, mid_pt = o_curve.PointAtStart, o_curve.PointAtEnd, ghc.CurveMiddle(o_curve)
                ref_line = rg.Line(start_pt, end_pt)
                ref_mid = ghc.CurveMiddle(ref_line)
                curvature = abs(mid_pt.DistanceTo(ref_mid))
                return o_curve if curvature >= self.tol else None

            def RunScript(self, Curve, Tolerance):
                try:
                    self.tol = 0.001 if Tolerance is None else Tolerance
                    if len(Curve) > 0:
                        result_cur = ghp.run(self.find_curvature, Curve)
                        index_fit_cur = []
                        index_line_cur = []
                        for index_c in range(len(result_cur)):
                            if result_cur[index_c] is None:
                                index_line_cur.append(Curve[index_c])
                            else:
                                index_fit_cur.append(Curve[index_c])
                        Curve_Result, Line_Result = index_fit_cur, index_line_cur
                        return Curve_Result, Line_Result
                    else:
                        self.message2("曲线列表为空！")
                finally:
                    self.Message = '筛选曲线（曲率）'


        # 曲线按照参照平面排序
        class LineSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲线排序", "RPP_LineSortByXYZ",
                                                                   """曲线列表排序，当轴输入端为空时，按线长排序，输入x，y，z将按照x，y，z的轴坐标进行排序，CP可指定平面""",
                                                                   "Scavenger", "Curve")
                return instance

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
                self.SetUpParam(p, "Curve", "C", "曲线列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "轴")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "按坐标轴XYZ排序，默认为世界XY")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Sort_Curve", "C", "排序后的曲线列表")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANHSURBVEhLzZRrSFNhGMdX3iuTlJmaaUa6CorsAmLmvCQqDW+bQYEJXQgSydDIipIKbHOXc46bwSyJMZ1NWvmxMtLNubESipDoAkXfog9+Dgdn/Z/jEXTNefvSH368z/u85zzP+7w3yX+tUZNpk2gurQmWPeJmmANkuzWaeI9ev02wjcY0guxRtTrdxXFSl9GY42LZUpfBoPIxTCG+jaPxsHIaDCfcHFc8aTZHORmmBQFuOPV6JfxtoAm+cifLnkPQZuqjvYK20dvd3T7GMGfFMIsLARU0q0m1OgE/ch6Oq0DC6nGWLXDqdPkuhrlLFWKsBFU0ODkuH3b1S602C8kvimEWF5ZF9qm3t8VtMBwe12orvQxTBXaMaTTZNOZVq/dg1g3jSD6h0+W6dLoaL5L7OjuTXF1dR8UwoWWz2dJ6rdZ02/BwmsViyXjgcCQ/7e/PtDocqUNDQylWqzW1z26XvjCZLrw2mVrhyxjx+ZI8U1OJjzH+0G5PDHQE1ovh/lU/gg0MDOy2DA7mIJhsUGztdruMWhojRkZGdvI8vxlIe3p69jNYsunp6QwaM2Pv6gP10WLICLFdsdaBOvAEfABTQAkkeXxeXNGM6hLZUCpQgONCbxnKBgz4BibBbXAIULLvIKqZb44pmVFegz2nVkDfhRVt3jPwE9hAAZivreAziO0IdEQXzyjbBO/sErWAW0IvhCrAG0Cz04B0EEqnwFsyVLwqbl6C7SBfZIGqwAT4AqjceBBOLLhJhiKg2DAvgRTEghjqRIJq4AVU7mUgDCxD9BYJxzMoQRY4A05TZx9wAip31QpKQKKJCqdKDrTgOrgv2itBBUIloGNaSUYJ6AV9q+ARqAGhEqSALbPm2lQEIoJOEe0rHZhWobcGUZAfIKIx0BgbVAHNfsmLtpTorlwlI8QS0ROyd9ZcKDq/TYDuQTCNIAmQMsEvkEAdeUCOCuqEZBB9Q/tKx3+BaMO/Arps9EQ8D8ID6HZbwCtgBpIyvja5jC/biLeoCYkiD74rp8eObv8uGifR29ENfoPz5AgjKpuO83sgI4fcrywq8SvvFc/Utxf7lXdKeWUu+edEWegG03rSG7IqFf6prS31n/yIKo6JLkgi+QsWY2KtjdvOfQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_axis = {'X': 'x_coordinate', 'Y': 'y_coordinate', 'Z': 'z_coordinate'}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _sort_by_length(self, list_data):
                for f in range(len(list_data)):
                    for s in range(len(list_data) - 1 - f):
                        first_line = list_data[s].GetLength()
                        second_line = list_data[s + 1].GetLength()
                        if first_line > second_line:
                            list_data[s], list_data[s + 1] = list_data[s + 1], list_data[s]
                return list_data

            def _other_by_xyz(self, data, axis, coord_pl):
                for index1 in range(len(data)):
                    min_index = index1
                    for index2 in range(min_index + 1, len(data)):
                        first = ghc.PlaneCoordinates(ghc.CurveMiddle(data[min_index]), coord_pl)[self.dict_axis[axis]]
                        second = ghc.PlaneCoordinates(ghc.CurveMiddle(data[index2]), coord_pl)[self.dict_axis[axis]]
                        if first > second:
                            min_index = index2
                    if min_index != index1:
                        data[index1], data[min_index] = data[min_index], data[index1]
                return data

            def RunScript(self, Curve, Axis, CP):
                try:
                    CP = ghc.XYPlane(rg.Point3d(0, 0, 0)) if CP is None else CP
                    if Curve:
                        if Axis is None:
                            self.message3("轴坐标未输入，将按长度排序！")
                            Sort_Curve = self._sort_by_length(Curve)
                            return Sort_Curve
                        else:
                            Axis = Axis.upper()
                            if Axis in ['X', 'Y', 'Z']:
                                Sort_Curve = self._other_by_xyz(Curve, Axis, CP)
                                return Sort_Curve
                            else:
                                self.message2("请输入正确的轴坐标！")
                    else:
                        self.message2("曲线列表为空！！")
                finally:
                    self.Message = "曲线排序"


        # 均分曲线
        class Equipartition_Curve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-均分曲线", "RPP_Equipartition Curve",
                                                                   """均分曲线""",
                                                                   "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "请输入一根曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Espacement", "E", "间距（默认300）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "HT_Length", "HT", "最后距离曲线的点至少大于（默认20）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Offset", "O", "偏移起始点在曲线上的位置（默认偏移0）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Style", "S", "均分样式 默认为：2（0：从起始点开始，1：从结束点开始，2：从中心点开始）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "PointAtCurve", "P", "在曲线上的点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Parameter", "t", "在曲线上的长度")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMqSURBVEhL7ZRbSBRRGMene0lRUNDtobceIoJsa90xd2ZvulvrrZIoKbqoiQahZRcllzQNllDEooLAeglTd3fmzK6uWm1B9RBCL0EQhLbnnNldr0W3t6Yz7kchogg95u9lmP//mznf/L8zh5vnP0amYu6zn6JXie7fDNKcQdS9DtHMPE3rWATSVHzEVO7DpvtPvolNctw0MDBQsgSsOdEdz06TqdkbGnZtBSmJpnELFOw4FMDC9SDNOiLRjHuhcVPET/liKJkTEtnrQdRyWSKWUyAliWjCYpnaL/WM2qtZB/Uh6srr/SyGOvHOQURLUqBsVuSY4JZUoQFRa1HfmLMO5CR67j6c7g0Pu4rZAhf9OL3t1Y+jW7qiqU2d2HATymbk5UjOKomIzYjaiySS0dA77K4Ai3U/KCxn0VwLqvvKkOpoRqq1NjKRu0b3AqpxVzveTl5HD62YLJ4BvSn2bJmMxWpErOUsoiqw9NzMORLLLajaKiQsnkOqcAwsrp+Ur/WTtDcdxHASpGnI2J4mEaFBwkIFwo4zLI0msJLDlbFwBRHLBYnYKtmQaj0atxBstu1KUpSY41pXdNcDkKYgvdejMd8NkqwTetcytdajqG032KxAFQzskzyI2Mokdg2pdgNYfwiTg3z/mKujW3VuA2mSF8P5G0MjlhaFZhbqu0+h9uIANleDzXHBwYINErbWJbvXVxcvgjWFSEJYiUhmIyKiDaRJEM46Fkw4qnzE2KpQZyHL/07/x4LVYLPOYnl72LQrAzjjOhtsjRKziWBNo4sYK7uihg645fyErwkQvjWccJ9UYtazMhVusTnYwU4STOw70Dee6WUvL9W3lv4vgDUNTfMs7MSpz5/+TG9Bcf6h7xNfrai240gVm8MjzksS4Uuh9C8ffrUsk4n9vBIXbgeoKQ/kGfHhjP3KiPFraDT9iqTyjYGo+UYwlnWib8LZ+CR+ej2UTaUn7jYpxHW1G2fvAGlWHg+l9vZ8Mb5FcUuFoorn/XRve993fhPY04kkylaGYrmH32kFS0GalZ6h/I2+qKkt/M34SFHN3ojmmTHWf2JAm9v5NM8scNxvcdKPj5GW0uMAAAAASUVORK5CYII="
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

                return PointAtCurve, Parameter

            # 数据匹配
            def Data_Matching(self, Data, Matching_Data):
                return Matching_Data * len(Data)

            # Curve 多进程
            def Curve_Multiprocess(self, Combined_Data):
                Curve_list = list(Combined_Data[0])
                # 确保有数据
                if Curve_list == []:
                    return [None], [None]

                Data = [Combined_Data[1]]
                Data = self.Data_Matching(Curve_list, Data)

                PointAtCurve, Parameter = list(zip(*ghp.run(self.Curve_Offset, zip(Curve_list, Data))))
                # （值，None）
                PointAtCurve = PointAtCurve[0]
                Parameter = Parameter[0]
                return PointAtCurve, Parameter

            # 处理操作
            def Processing_Operations(self, Curve, Espacement, HT_Length, Offset, Style):
                # 数据匹配
                Curve_Tree = [list(i) for i in Curve.Branches]
                Data = [(Espacement, HT_Length, Offset, Style)]
                Data = self.Data_Matching(Curve_Tree, Data)

                # 进入多进程
                PointAtCurve, Parameter = zip(*ghp.run(self.Curve_Multiprocess, zip(Curve_Tree, Data)))
                # 还原树形结构
                PointAtCurve = self.Restore_Tree(PointAtCurve, Curve)
                Parameter = self.Restore_Tree(Parameter, Curve)
                return PointAtCurve, Parameter

            # 间距、长度、偏移距离
            def RunScript(self, Curve, Espacement, HT_Length, Offset, Style):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    # 参数定义
                    if Espacement == None:
                        Espacement = 300
                    if HT_Length == None:
                        HT_Length = 100
                    if Offset == None:
                        Offset = 0
                    if Style == None:
                        Style = 2
                    if 'empty tree' in str(Curve):
                        self.message2('请输入曲线')
                        return gd[object](), gd[object]()
                    else:
                        return self.Processing_Operations(Curve, Espacement, HT_Length, Offset, Style)
                finally:
                    self.Message = '曲线均分'


        # 统一曲线方向
        class Filp_Curve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-统一曲线方向", "RPP_Filp Curve", """统一该曲线的方向。
                   传入曲线则所有曲线跟曲线方向保持一致
                   传入真值则为一组数据中曲线中心点最高的曲线为统一方向
                   反之中心点最低的曲线""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curves", "C", "需要反转的曲线列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Direction", "G", "真值则为曲线中中心点最高的曲线、假值则相反（默认真值）\
                           如果为曲线则使用该曲线统一方向\
                           ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curves", "C", "反转后的曲线")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Flag", "F", "是否翻转")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANsSURBVEhL7ZR9aBNnHMczRVuEbSh1Uzb/6KRqYtKXWG0trtKX2Grr6hYFad3wHY1zE60rnbIi6D8FKVYsvUQoqLW9tJfkLi+1pjRssE1ZGFrqC6XYvFwuucvraCbVmvz2XHkoSGcoWvxHP3Dc8/t9v/c8v/s9z53kPW8VAPgAD+eWweCudTauWvsoePVDnEqNWIlarS7SaDSV7e3t+7Ra7c5kMrkEy9Pc5ZuXWYTiy4ZwVqLbLYuj5xZiKTU2m22pSqVKtLa2vmhsbEwQBDHR0tJC1NbW6pqbL34H4Eg3+op+6g1Ig+anmWAc/xy6PWvGZr0ASZKfVVRUQEdHx9/19fX/NjQ0hOrq6kZramoSRw4dH3mWJBUUp/RTbH6yi80EOlD04IbrCxaAWICnkPTxVY1GT5kChy+j0+mWoKsftWX1lcvt17o7qU7NkWP3Dxw4GO/Qkb+InltCVfPAZC7QXOkpG7vj6E3PyoQTmhaJGuPa9u2fkAtWrlotxilBrz0f4HGGzfTH1+MslPuTpzLNYWV//6QMLIGSs6LHwqn20IHCECoore/hieVMRPaC8q43Tk3wKuihHz5lhMK2Hr80inoN+sCqYb0/63c6JgU6rPBZvF9VYavE6SQW3Ald+sjhGEungzkPmUiO3xkhPsbyTKzeajUdkU8YBNlT0qM83+PeuKvbI2+jeNl1W3DznpGRZBq2TjOsh4XmcP4dJipPWEf3/n/vRdDGaRwgB2ukkHL6iAycTomd3Z+HChqxxLIn7e7Dm3B6JkZX2XEHyIDmC87h1Es4fU0ZdLDgMFqcMHgLDpncm8spLk97a0IBaF8e3x77UYqtM2GeqLcMospp7stLYixu2JSAsfAlpw1B6fPegAx62Bwv6V0L5pgCDLxcsAilZwC1CFtnMhRrW2wKK+ImPt8hxoxvyw69R+kSxzAG6UxIaRpIoiqDG1t/FX5eLub/QvchOLlGPGVinBLKu8FsisjgN+7CUjG2+rd+T/qyYHT82ifGgHKQia6N2/ndlVPm18HIltTT7u17cYjeoKyW4rITJrb4njG6EkyBDdEeT54ey29Ol2tVWW84Ewz/rAAmjhYIZT8yc6U7sfzmkJ71lXbIAvSBCX1CxUkYnuVPbLb0sd+U22Mq3V2+aRlOzS3oZMzDw3ceieQ/v1LI1zwofCoAAAAASUVORK5CYII="
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
                Curve_Bool[1], type(Curve_Bool[1])
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

            # 操作多进程
            def Curve_Multiprocess(self, Curve, Guide):
                Curve_Tree = [list(i) for i in Curve.Branches]
                Guide_Curve = [Guide]
                # 判断是否为曲线，不为曲线就拿本身的曲线
                # 为曲线可以直接进入方向统一方法
                if 'Curve' not in str(Guide):
                    # 得到曲线中心点 最高或最低 的曲线（根据 Guide 真假值判断高低曲线）
                    Guide_Curve = list(ghp.run(self.Curve_Height, zip(Curve_Tree, [Guide] * len(Curve_Tree))))
                # 数据匹配
                if len(Curve_Tree) != len(Guide_Curve):
                    Guide_Curve = [Guide] * len(Curve_Tree)

                Curve_list, Flag = zip(*ghp.run(self.Curve_Flip, zip(Curve_Tree, Guide_Curve)))

                # 转树形
                Curve_list = self.Restore_Tree(Curve_list, Curve)
                Flag = self.Restore_Tree(Flag, Curve)

                return Curve, Flag

            def RunScript(self, Curve, Guide):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    Curve_Tree, Flag_Tree = gd[object](), gd[object]()
                    if 'empty tree' in str(Curve):
                        self.message2('请输入曲线')
                    else:
                        # 默认有值都为真
                        Value = True
                        # 传入 假值
                        if Guide == 'False' or Guide == 'false' or Guide == False:
                            Value = False
                        # 传入曲线
                        elif 'Curve' in str(type(Guide)):
                            Value = Guide
                        Guide = Value

                        Curve_Tree, Flag_Tree = self.Curve_Multiprocess(Curve, Guide)
                    return Curve_Tree, Flag_Tree
                finally:
                    self.Message = '统一曲线方向'


        # 获取多折线角平分线
        class AngularBisector(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-角平分线", "RPP_AngularBisector",
                                                                   """根据多线段折角角度推算出角平分线""", "Scavenger",
                                                                   "Curve")
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
                self.SetUpParam(p, "Polyline", "POL", "多线段（不含弧度）；曲线（有弧度）、直线和圆弧均不可")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "需要的角平分线段数；个数为（Count - 1）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Angular_Bisector", "BC", "输出的角平分线段")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM8SURBVEhLY8AGHF9WK7u8qg+DcqkPnJ/XJDm9qH0K5VIfOL2oiXF6WXcNyqU+INWCj/U1fk/ySwygXMKAFAv+TW+RfllasfhwVKYgVIgwIMWCt9WV/TeSC6yhXOIAsRZ8aav3epxX1gzlEg+IseDfnE5ecNB4Ew4aDiC2BGIdIFYGCRBjwbva6ro76SWBUC5eIAfEu4F4JhBXggQIWfC1rdb0SUHpZCiXIAAlrytAfAaIJ4EEnN7Vxzh/aMRqwf//q5hfV1TMvx6erwAVIggCgHg5EB8B4hYgZrQ5mhVptjHxOpDNDMRMQAwHnxqqMx9mlaRDuUSBWCCOAOI8II4HYmGXVzVhNhcKoBZosWk4twkD2Qz/uovln5WUz6tnqEexlBBghdIgwAjETE7vamIcn9dcBQn45N2Vi6i+4uHbeM31YknD3E/RiVogcYqA0+uaGIenVZctGP5xxlTf8CiYfCt/zrRDW2e3bTyoXnpWCqoML7D8ecHQ5u/j2VAuKnB+Vxdt/6TyiovLO7nszmspkxafX7R5xf53s1Zd2Fraf7bGI3GuKFQpCrB4tJLT5ueJWOs/50/b/Lv23+bP3QtQKVTg/Lo62uFR1TWfoKcauX23s1cvO3z94L4Tf9btPH+2ZdblvpCyw65QpWBg9WO7us3PA/22v4+9s/19+pvN7/MLLX+dM4VKYwKQDxweV10Vtvon1dt9qH3NrF2P1u+5eG7Jhgv7mybdqE1wemokmVbPZf9/R4Ddj60H7H7t+W/7+8BN6x+H8y0+HBOCGoMbgOLA7mnFRX/99wLraxbta59wun/qnNt9E3tvNqVMO1LqeH31bMsbU59bXJj0y+HfnrU2v3bZQ7USB1xeVsfqvas48i+7LvFo6Kxsp5xPtlFrNk/yuLHwhsOH+f8dfi29b/dmcbXpugpw8iUZGHyrC02/Uff+fnbRHN37bQUOLyc/cfgy5af9n5mb7H4v8IQqA4EMIHYA4iAwj1hg8qk+KOPnhP+hD1r/23zrfub0c1Kb8/dpSlBpZLAaiDcCcRGYRyxweVyj6vC3Y77Zv+6Q0Cv1bFBhbKAUiM8C8RQwjwYAZEEjEG8C8zAAAwMABU9tbCea1EgAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.eq_part_num = None
                self.tol = sc.doc.ModelAbsoluteTolerance

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

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
                intersection_pt = rg.Intersect.Intersection.CurveCurve(new_first_curve, new_sce_cuvre, self.tol, self.tol)[0].PointA
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
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Angular_Bisector = gd[object]()

                    self.eq_part_num = Count if Count else 2

                    poly_trunk_list, poly_trunk_path = self.Branch_Route(Polyline)
                    plly_trunk_length = len(filter(None, list(chain(*poly_trunk_list))))

                    if plly_trunk_length:
                        iter_ungroup_data = ghp.run(self._get_result, zip(poly_trunk_list, poly_trunk_path))
                        Angular_Bisector = self.format_tree(iter_ungroup_data)
                    else:
                        self.message2('P端数据为空！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Angular_Bisector
                finally:
                    self.Message = '多折线角平分线'


        # 点与封闭曲线的关系
        class PtsCurveRelationship(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-点与曲线关系", "RPP_PtsCurveRelationship", """确定所选取的点与封闭曲线之间的关系""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Points", "P", "选取的点集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "封闭的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tol", "T", "精度（点到曲线的距离）")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Relationship", "R", "点与封闭曲线的关系（0 = 外部，1=在曲线上，2=内部）")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "In_Curve_Index", "ICI", "封闭曲线上的点在原列表中的下标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Outside_Curve_Index", "OCI", "封闭曲线外的点在原列表中的下标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Inside_Curve_Index", "ISCI", "封闭曲线内的点在原列表中的下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO1SURBVEhLrZVtaFNXGMdvY2rX6FpXX2pLcm8SbpuYtVHJlK1sdCBjChNEqG8ffEEo+MEhZptzWGM72MSJY+AcYSsDNVHDrO7Dqhbf8IuiTv2gXwoyWk3bJTdWN5VNkvP4f+49xlT7tuEPfvQ8z83tPfec8zxX+T+ca2y092uau8fnq5apV8vVUKh4UNPa0uXaEpkaQkRRbHI4PpKhkIOlpqYJMqX0uFzVfzZ7P8+2+D6WqTw99fVvZDQt3FNT45Wp0cGPV6Qx44IHLIadNzd6ksZnurDbio4jnmReAXi7KWlV/WRAVcf3gLtut+++y/WWDHfCG7CBsBSNimLH+AcYhyZjLhFuLOK/iYIlkbTD87CUAyE6A0QnmsLhMM++G87i/Jj0ezzzU6raciMYzL822AdPW0OLXDr+C9EFEkJMR7gHtlFzc7GB+7t1nXPDgw1803C5Vierqhwy9Sm8Eo1GHUKc/EikDlRx8lE6Xv3EOPw2jwHvS5fApDKq2t6nqgErPTYfwCR8XYizC4iuUy4d22FeGQrXxDW/oky97fWW91dWFr79iPBr9sH3OBD9+yeJhx2LBv/4eQrHLxKqKrm+sLZ0ngzHxSnYag2fI4wDTvHPby3iQaxGphQR0Z20p47EV4FdMjUm6+HvPCCK2MRgfC4NHjNnnjViq4kuUTYda+aYoUhg4jcfTu9aO7v8pQmZ5/Ye1o3XTqYq4F1Yz4HIHGogukg5I7aXY0okJoj7+3WixIvHeAvk0zYULhhUathQ1Y0y9RP83hqaS1KWfdSxQWSOmA8chXXwKNcR+pWDNbP8gKSm+f8OeuvEl/7da2aX8caWmRf/GwvhGYpEbGgvrSm0GCstIWq0P27xkWjzc+mPCNE5u+j+rkSGhYTgJUI752LjSVvp58wsK7HdmjNzcr4K6ebeyURktg6GSCnCXlzJGvE+IY6YLaMAJ7wMuT8NC1fsIWuItU/FasS/vz7JGfGoTJngFG3PZWLf0tVosUyZiB/rKiMLpvXGls4YsYt2weXWEDc86JgqHh9rz6YPrpKpkeA3fH/ruxWdtC9IotXP1f8SfOSuwXzxjIMG+DU8CY86im3rja06OqzVjYfjFqyzhsPChbYI7oYnYAfcDEefVG8gUPFXbe2012y2LxDyJnFnnAPfgcvgdsh7wzM9CDdAHQ6h1+ksRS1tS3k8Zu/Kk3K7l93TtGc9pAnyhyUB+Z9x9W6C+HiNXhv8gAFNWzng8QRlyuKOrjv5s8jnV6ZeEYryFDQXUJRmojKgAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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

            def relationship_point_curve(self, pts, curve):
                relat_list, in_curve_index, outside_curve_index, inside_curve_index = ([] for _ in range(4))
                for pt_index, pt in enumerate(pts):
                    t = curve.ClosestPoint(pt)[1]
                    test_pt = curve.PointAt(t)
                    distance = test_pt.DistanceTo(pt)
                    if distance < self.tol:
                        in_curve_index.append(pt_index)
                        relat_list.append(1)
                    else:
                        if curve.Contains(pt) == rg.PointContainment.Inside:
                            inside_curve_index.append(pt_index)
                            relat_list.append(2)
                        else:
                            outside_curve_index.append(pt_index)
                            relat_list.append(0)
                return relat_list, in_curve_index, outside_curve_index, inside_curve_index

            def RunScript(self, Points, Curve, Tol):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index = (gd[object]() for _ in range(4))
                    self.tol = Tol

                    if not (Points or Curve):
                        self.message2('P端不能为空！')
                        self.message2('C端不能为空！')
                    elif not Points:
                        self.message2('P端不能为空！')
                    elif not Curve:
                        self.message2('C端不能为空！')
                    else:
                        Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index = self.relationship_point_curve(Points, Curve)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Relationship, In_Curve_Index, Outside_Curve_Index, Inside_Curve_Index
                finally:
                    self.Message = '点与封闭曲线关系'


        # 线与指定向量的关系
        class CurveVectorParallel(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-线与向量关系", "RPP_CurveVectorParallel", """判断线是否与置顶的向量平行（包含反向平行）""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "待判断的曲线集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "指定的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "角度（Degrees）容差")
                Tolerance = sc.doc.ModelAngleToleranceDegrees
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve1", "C1", "与向量平行的线段集合")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve2", "C2", "与向量不平行的线段集合")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index1", "I1", "与向量平行的线段在原线段集合中的下标")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index2", "I2", "与向量不平行的线段在原线段集合中的下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJYSURBVEhL3dPLS1RhGMfxU7suFE2XRUQW1CKhWlRGN4YIyhBMUTAKs8aZcS6eM9OMo3kBwYW2sKihiFy6sBsNUYzk2NXKscBplAmrhYuwFu3qH3j7PvmWdDGsTpt+8GHOeTnzvud93ucYdkQpNUtf/psM1QYSL8LHb+lb+3PtWFX7+6YmlQlFTushe3OisnJxqtr1YTxap0ZDdRE9bG8SHndbLhRSlEqNRWJNengqY/VRayIWy+ZM89cs7fO9lR21hJkdsayxtN+v0j6/ehWJqKwZSmaj0Xl6esO45/V0jYfDapgHhnlwSkBlAlowOKm2VjPVc9NUGQzW+NSAx6ue+HzsIqz63G7V7fMt09MbRry8fHVXRcWBsyUlk8q+VzatztLS4mTAf3LEmixR0u3OdBQVbdRT25PXLY033tQ3qGR19UOnM3++HrYnHy/Ed7xraVa9LlfucGHBAj1sXybaWnteRiNvVX//Qj30Q2RLa7AOG7AJW7ELe1CIYpTjEI7CiyDC21flpfIcjstcS3u2Yye+ifx5EI8xgAe4ixRuoxc3kcBV9KAbFyFfbwxhNKAZ+7Ae8sJfM1v//m5WQHYpu5HFrkBeMA0LM8oSFKAKHfgyyVM8wnV0wg0pz3JMm23w4BSkJFKyIdyH1FlqXIktkIVnFFlVJpXD7EccsuX9yMdft54scAmy3TuQw6vBZsyFrVkLacUz6IPUWRY9hyOQzvjThvhpHNiNRsjhSjtLh0i7Sls6sQi2Rd5ezkU66jxkd88g34zs+iDmwNYsxV60QjptJf6LGMYnkwQFaee6yDEAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.angle = None

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

            def unified_direction(self, tuple_data):
                curve, guide_vector, origin_path = tuple_data
                guide_vector = guide_vector[0]
                curve_parallel, curve_not_parallel, parallel_index, not_parallel_index = ([] for _ in range(4))
                if curve:
                    for curve_index, single_curve in enumerate(curve):
                        single_curve = single_curve.ToNurbsCurve()
                        single_vector = single_curve.TangentAtStart
                        radian = rg.Vector3d.VectorAngle(single_vector, guide_vector)
                        if radian > math.pi / 2:
                            single_curve.Reverse()
                        factor_radian = rg.Vector3d.VectorAngle(single_curve.TangentAtStart, guide_vector)
                        factor_angle = math.degrees(factor_radian)
                        if factor_angle < self.angle:
                            curve_parallel.append(single_curve);
                            parallel_index.append(curve_index)
                        else:
                            curve_not_parallel.append(single_curve);
                            not_parallel_index.append(curve_index)
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [curve_parallel, curve_not_parallel, parallel_index, not_parallel_index])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Curve, Vector, Angle):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.angle = Angle
                    Curve1, Curve2, Index1, Index2 = (gd[object]() for _ in range(4))

                    tree_of_curve, curve_tree_path = self.Branch_Route(Curve)
                    tree_of_vector = self.Branch_Route(Vector)[0]
                    if not (tree_of_curve or tree_of_vector):
                        self.message2('C端不能为空！')
                        self.message2('V端不能为空！')
                    elif not tree_of_curve:
                        self.message2('C端不能为空！')
                    elif not tree_of_vector:
                        self.message2('V端不能为空！')
                    else:
                        c_len, v_len = len(tree_of_curve), len(tree_of_vector)
                        if c_len > v_len:
                            tree_of_vector = tree_of_vector + [tree_of_vector[-1]] * abs(c_len - v_len)
                        zip_list = zip(tree_of_curve, tree_of_vector, curve_tree_path)
                        iter_ungroup_data = zip(*ghp.run(self.unified_direction, zip_list))
                        Curve1, Curve2, Index1, Index2 = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Curve1, Curve2, Index1, Index2
                finally:
                    self.Message = '线与指定向量关系'


        # 创建中间线
        class TweenCurves(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-创建中间线", "RPP_TweenCurves", """在两曲线中创建多条中间线""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve1", "C1", "第一条曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve2", "C2", "第二条曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Number", "N", "数量")
                Count = 1
                p.SetPersistentData(gk.Types.GH_Integer(Count))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "中间线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKISURBVEhLtZZLaFNBFIYvra/6qg9aSe5MirkzqbjwuVEXFnUniAspCBbRSkUEUYob0a1CNyJ0IehCFNGdoOjG10KkIj4WbRYqWosotcltHm0a0o31/2cmRXBhcosffHD+k8Xkzp05ifcP5sHFtvw/bIBZeBtuYmPOjLWsX5qGLpL98DmchveggNEJZfJIRbYXSlL1FxI66dpkC3wGS3APG7WyAO6CZq9nOjsbi77qKgv9pixTlUmhr/6Ixf58D2fhDNxqUg00w68whH1wNTTk/eTuKakHSzL1bUwEyrXJRTgMG0yqAe75MZiGk/AMnKUo9fWCUPlifN3s4uA7PGDL+uiCE/CuSY6cUE+yfsCXXIVPcd+W9ePDDOw3CWQSiVgogsnRRGqta22Hn2GjSREI4C+40SQQCvU09INzLi6BI7DdpIjcgHds6XnjMujFNj12kbyGB20ZjR2QJ4wjw/vpq214ik84o9VtuQkv2zIavCNcgCPDC1ep5VhgZEwqbh85AV/aMjov4HFbYjD56l3oq+rx5N0YhctMighP0jVb4jQJdSsrgisukiF40pbROAxf2RJPINQhPMWgi4QvuQw5ESKhIW+t2YZcMtmMBfKZuNrM7HgIP8AWkyLwEXJsG7hFOV9xrFThqXoE87CbjXq5BAdsidun1MK8UF8mhH7w1vPmuzY5DbkIB2EvbIU1sRJWYI9JYHRNsrUkdLok9XBRqn2uTTg4z0Oerrpm1V7I34FTJgGEBkzavimZKpelHioldM9MR8ci9zEvZ9yWtcNvynHOy7WTDRIK7eN3o286kRrPCH3BtSPDb8U/Adyy9/AoNAwI0ZRva1vh4pzhuOAl5MtvYuNvPO83z1On87DUpboAAAAASUVORK5CYII="
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

            def Tween_Cruve(self, c1, c2, n):
                curve = rg.Curve.CreateTweenCurves(c1, c2, n)
                return curve

            def RunScript(self, C1, C2, n):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    if C1 and C2:
                        return self.Tween_Cruve(C1, C2, n)
                    elif C1 is None and C2 is None:
                        self.message2("C1为空!")
                        self.message2("C2为空!")
                    elif C1 is None:
                        self.message2("C1为空!")
                    elif C2 is None:
                        self.message2("C2为空!")
                    else:
                        pass

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = '创建中间线'


        # 平面修剪曲线
        class PlaneTrimCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-平面修剪曲线", "RPP_PlaneTrimCurve", """移除平面一侧的曲线部分""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "将要修剪的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "做修剪的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Flip", "F", "是否反转曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Trim_List", "T", "修剪后的曲线列表")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Parameters", "t", "平面和曲线相交点的参数值")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Intersected", "I", "如果平面修剪了曲线则为True，反之False")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJBSURBVEhL3ZTPaxNBGIa3+SGl2ZlNoyZVya31IK0iwV5Eg5mdxVRptBArETxU2yKCEkWsF29ePHgQ8SB60KP/gmCK55qdTSu9iPSiF1FUxINg1/cL06BNNk0gXnzgge+dYWd2J1/G+P+w3GzcqGQjOvYeppwZpsReHXsPV8606eWO6Nh7LNc5ZrrytI5dw6r2hOHPRXVsJqbkKKs5Mzp2xfbVScaVfdvwjT491EyslksxJa/o2BVxT4zxmpzXMYClTJQp+3rbtwiAefYkGuSkjsEwV5QT6+e4jsQwPAtvwhuQfqMk/As0yCVz5fg+HYOJfyyU2KI9gnIKvoQ/ob/Jz/ARpM3r4PwXUkrGdAwm9iRTDo8n1lBuXrSV32F5Z6Voxt/mr6JuyxB8FhlP+JFccmOBdfgK3oHUXRfhPfgGNjYKZwY9/unUGdSB0Bl/gH5oxPSjU7t/oH4Ix2ArQrAIl6EflSk/IpKrqPfDJnKw8TZ9u/pfmJXsAk10QD+8u62U/hVKD9DzX6CgiT+hvqfJ95C+xOBr+csY6bhVY08PPTaioa8oaR1qCvq6BqPwAUzVE6BWrd+sHTCwMjFkfStcQEkt+g5unAadTGu4K+dxr1CrbgnursOsKs7ruAdWIW1wnwZawpWYpgd1bAuvipLpyaM6EhZchLP11ArLs4XpiYKObWGuLA8uO2kdOyNedQ5sfXEBPxvhSt4ynhfDeqQzzKXsDlYTJ3QMhL92hllNXtOx91hKHGSezOv4D2j7XzGM38oLoJLIQIxjAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.flip = None
                self.factor = None

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

            def RunScript(self, Curve, Plane, Flip):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Trim_List, Parameters, Intersected = (gd[object]() for _ in range(3))
                    self.flip = True if Flip else False
                    self.factor = sc.doc.ModelAbsoluteTolerance

                    if not (Curve or Plane):
                        self.message2('C端数据为空！')
                        self.message2('P端数据为空！')
                    elif not Curve:
                        self.message2('C端数据为空！')
                    elif not Plane:
                        self.message2('P端数据为空！')
                    else:
                        curve_event = rg.Intersect.Intersection.CurvePlane(Curve, Plane, self.factor)
                        if not curve_event:
                            Intersected = False
                            Trim_List = Curve
                            self.message2('平面未与曲线相交！')
                        else:
                            if self.flip:
                                Curve.Reverse
                            curve_event = curve_event[0]
                            Intersected = True
                            origin_dim = Curve.Domain
                            cut_off_point = curve_event.PointA
                            point_t = Curve.ClosestPoint(cut_off_point)[1]
                            Trim_List = Curve.Trim(rg.Interval(origin_dim[0], point_t)) if self.flip else Curve.Trim(rg.Interval(point_t, origin_dim[1]))
                            Parameters = point_t

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
                                                                   "RPP-统一曲线方向（逆时针）", "RPP_UnifyCurve", """统一曲线方向为逆时针""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "参考平面")
                Origin_Plane = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(Origin_Plane))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "曲线")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Bool", "B", "True反转，False未反转")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANnSURBVEhLzZRZSFRhFMdV0haKNoKguw4i2R7VQ4HlkqbO6IyWRTslGNlKvRSFQetDDxVRDwXRAkFFUb5UZJuUIdg2jrYwo5U2Lm1mWRHh1/9/u9fu5CRtD/3gh37nnHu+e++c+0X8T4yC4779++/ZAoXpcTgc/jPWQqu55We4F0rwr1gIraYbYQq8ZYu9gZtgP/jbOKHVaAcDNubBamjl6+ByGAN/iUnwIxSRUT3OxM9pzR+z6PVoI/Od7nAVrIfWRj44G3bJMPgK8oISBtQM3wk9t1E43P6LQ/OezZ6ySthfyQDIIXgLrY1uwGmwE0PgU8iiO7APjFBSrk5VXTVCcdUK3dMgNOfdCkfepb7M2VDhfvgFWhudgh3wrryQCT8cBA1iY/d0l1Mrnikuv1Cz64SSVr7bTIVjJDwDrU0M2LwUMtAMHTAEeWr5Ps3dIJTMh9iktiVuehUn6mdY03eJi26wzAy8hOMLKkS05nxULGd412BtIE8uSZCTLi+VEkqWae5Goblr3g+f+XCCmf4RNma/JVz0hC/MwEoGHKk3R6h4HZonKJR0bx5jduTEK5u1nFdCyw68HDb3MYfCDl8tJ7AddryJ7ZAbHDVWQE4871ZdAaFm1bZLzspOEyElXd+j574Vera/buycGv7AFrwh9rptrEz4wzDYCjtGUEk6P1/LrhdKVu0nJbOS30YIUnLpYX3Ge6FnVVdNKWzqbYaPQPbi6IZQCZmYZaxMpOSS5ZqnCSMaaNHTvTxRQ5BSys458tpErOdxkRkKQvaZaKxssICJ08bKhpx8ZYOe+1rILn9QcXpDJkwdvaufkl71QXM/KceSPzp78OvudGyMgEy+g/0ZsCMnX9upT28VivORX830DTbDBlLa7Td6TvBuZKRxZrHHISMRhnuQBWHPEzml9KBjRhs38eqeQNy4AhGtT/Ot4dOpLi+/2quQ1+eyPhw8kllw1liFQU4tO84nkTOrhZzuq9c8zWju/9A/fvVMpNtMB7I2HPGQG7DIOIfCoec0FWru4H3N/bxBz2m8MGFdexzCHA5ee4E1XcFDjoV8mgSYBrMg73ABzOffqKiYouheEg+3bXArDEBetwJ2yXrIwj81FnYJJ4TfRAvkwceRq4EPIIeA43gd8rwphifhMXgALoY2IiK+Ak2UQMs6P0amAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.plane = rg.Plane.WorldXY

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

            def is_curve_closed(self, curve):
                # 使用Curve.IsClosed方法来检查曲线是否闭合
                return curve.IsClosed

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

            def RunScript(self, curve, plane):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Curve, Bool = (gd[object]() for _ in range(2))

                    if curve is None or curve == None:
                        self.message2("curve为空!")
                        return Curve, Bool

                    if self.is_curve_closed(curve):
                        Curve, Bool = self.unify_curve(curve, plane)
                    else:
                        self.message1("要求闭合的Curve!")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Curve, Bool
                finally:
                    self.Message = '统一曲线方向（逆时针）'


        # 删除重合曲线
        class RemoveOverlapCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-删除重复曲线", "RPP_RemoveOverlapCurve", """删除重合的线段和曲线，可调节公差将相似重合的曲线删除""", "Scavenger", "Curve")
                return instance

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
                self.SetUpParam(p, "Curve", "C", "待删除的曲线集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "范围内的曲线将视为重合曲线")
                Tolerance = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "删除后的曲线集")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASUSURBVEhLpVZraBxVFD6iaX9IrVbFJjvJSnaypG4SwT4QEa1Cpb+MVtAf6g8tigR8gK+Klobij1YEheIjFUSr2ZndNCVQra1YfNRXtWobg5HYtNrGmu7MPube3c128xi/e+aOppv9IfjBx5xz7ux37r3n3jNL/wm78reS71+gvf+BpEyQJV4hq7iJ/XRuKVnyc/rQ9/G8h2N14EbbVrgR8y3tKtwM3hWYISy5HcyCJSQpUKqwjNL+IthjtI8TjNIW/yL99nmAuFFtiftOc6xbh54Ai+CF7DEs8RGlyz7Z8iQowK06voEGpnwarKqxezlWB45h2k4kdli7y8AZcB17DFveArEyOAEOg+OUHllEhL23vBGyRRXvfKHfXgCnuXVVwWjzc42tLTp0AEwGpoIqohK25e/gEQieRS1u4zFbbEGsCDq0uxzlWB04RuxkJmI+rt0HwInADGGLHeBpJPoJYr9S0tvGccu7Ab4L5jF+B8fqANv0LpIMarcdFIEZIundh2JOQORHvU3BElOlCMRPIV5EbCPH6sA1zM1I8rV2LwWzgRkiJddB4AySHMXzBAR3cTxdbqGkcBGbI7tUc/z+hRMxX3QjsbBOl4P5wAyRkndDREL4OJ5liL7A8WRhPQ2ewylCoa1KnGN1gBUcdI3YG9q9CZSBGcKWr2M7lFAOnMVsV3M86fXRQb4LR9nXOJft7NQmnY1Gl2cN088YprpkCmr1Xwamgrq1djHD25Auz+E5zPGhuSUQztJ+329IZXvnpq7aOlvpSk57if7Zcoc7U0jsUa+5y2PbcOHO8G+IloI+uIE9hiU20V41S2zNkHp6T3E8KR4JWkW5smR3pq2aa9pclYmdlcyKvhmZ+LNSSLw9tt5cnGsyq5lI7CH+DZE6fZOg7l9qlraYpFRxCrNVRzFHKXElj1nyMO2ZVtv2CfvzkBnv4no4ja3PZI2YgykrwYvBafBBNRbA8p6GAAoo/oDgX6jFAMdt2QG/gHEcTxleoAVAcSdx/p/Ubg9YAHUfCm7wz+Ax8AeIjqOoQXZbPorYaSQ/Rf2FNRyrgWPEV+NoVrymdnUsFb4DXw1MhZS4hgUssR+CQ+AoDZRW8Ri3biS1xG9I0MqxGqjWgPM/ot0G0AHnNTmr1I0ExyC8F1vxJiewi9cFY+JlbM03GD/+T6wG2UisF1t0SLuXger2XsseI1W6HUKq9wxA7DWecdiWU8WNsH9BghFs22McqwFaQw8u16h2F4NqBWvZY7wvOyF8Qot/AL4D0aBhWfmr4U/CP4Bn2GPOg2u0rcEKSvloVPUeBZUsLDjQ5zfgxzg93nYIjcF+GDMu0nvuJTxuyUOY/acYy2O1Cwp9ZOXKBtQgh4/N/TqkPp2fBWYIS1gQUAX+Fvbz4DDEevVYN4jWIb9CorofHKxgJ27x99pVPUh9zVQ9NNLiRgig34uXsBIUWfRg/33q96/gcfVdtsXHeM7gj8G8ExLAaYy3TzXHfS9iXq9Dqos+G5gh1PbY4jk8x7mr2qIfdgePWXItH4akuJMGZBfHaoBV7MNWBf9GiNTqdxAR/Q02uobyT+UMIgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = sc.doc.ModelAbsoluteTolerance

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

            def RunScript(self, curves, tol):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Curve = gd[object]()

                    tol = tol if tol else self.tol
                    if len(curves) != 0:
                        Res_Curve = self.remove_duplicate_lines(curves, tol)
                    else:
                        self.message2("Curve为空!")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Curve
                finally:
                    self.Message = '删除重合曲线'


        # 曲线相交位置打断曲线
        class IntersectionBreak(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-相交位置打断曲线", "RPP_IntersectionBreak", """曲线相交位置打断曲线""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "一组相交曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "公差")
                Tolerance = 0.0001
                p.SetPersistentData(gk.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Curve", "C", "在交点位置打断的曲线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALfSURBVEhLpdVrSFNhHAbwOZ1tatp0amkJBbUh04XmsiwkQdMiqcwkCxGC7IaEEkYk1Iq8UEEERdAHKRSS9aGim2WQmUHlhzJHRX3oQhFmmNGFUt6e5z1tzLa5kz7wg/e/7Zy9t/MezSQTCqVglNUE0w5rlaZPIkDAFllNICnAG6yXlf88AXZiQqmE36CXlf8cgw9KM3AsUAMcahkUxuuNOXWZdV02U+Zj1IkwDfhHIeCdxUa9UViSsuL+1n6zGTgVHmnxFjFYOSAc9ibvz3/CZ3gDT6HbbJxzp7+sTzRlH7+OugH2wFZYAdwEnpiAc87RZCVPTa6utFSITeZyXrQT6uEonIELcAseJkUmuk4uPfF9eUohO8DpdHdmCGIgYHbDF6UZNC3wDDiFnCp2NAnGTR84lWbQlMMoRMlKRdgLDnOjrIJnNvD3+bJSkRLgBTNkFTzcWQPA9VKVc/BCaarORXigNMePuzdHZKU+3Gm/wCCrcTIdOD12WanPPOB1ubL6J1zUA7DXWdjadsjePBqpi+YCL4MFYIZZwN9FQhj4y3vYrzTHhg/XcKhWKy4VOUVX8X1hNMSxN/6MwDDwZs/hEXRC+8GF9Z9uF997GxuRwIdyG4w5PsLBZDOlD5bMXdOq0+nmo14CfOQ3QBXUwWE4BW1wBbqBx8brxmzHUHu+U8TgbEJNPtuWU8EvMmT1n8lIyEibEhbuvjE77BMH8AwJNMfBEp0ea/1aZd3RjDZHXyQ/9YoLTitNT3i+8LjmOvGidcAt2QhngYdePwxotSEjnauuip7VvUKvi+BIePjJGxQ05OyrvbayQ9hM9h7UfGh64R38APeceuNifwTOfwe04AFy1Niqb1aYK75F6aPYGe48zSLAsVwm+ktdIm9mAc/7l3AXzgPfWLXAhc4DKyQDt6u/yPsBRy2jg1RDmOFGusn6qjQ1V/WJGCB8B/APtsvKK5yOJqU56VyGXRqNRvMHAvLFHyMDDfkAAAAASUVORK5CYII="
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
                curve, points = tuple
                curves = self.split_curve(curve, points)
                return curves

            def split_curve(self, curve, points):
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
                        curve_intersections = rg.Intersect.Intersection.CurveCurve(curve, other_curve, self.tol, self.tol)
                        for i in curve_intersections:
                            if i.IsPoint:
                                pts.append(i.PointA)
                    intersection_points_list.append(pts)  # 将交点添加到列表中
                return intersection_points_list

            def RunScript(self, curve, tol):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Broken_curve = gd[object]()
                    self.tol = tol if tol else self.tol

                    if curve:
                        self.tol = tol if tol else self.tol
                        intersection_points_list = self.Find_Intersections(curve)

                        zip_list = list(zip(curve, intersection_points_list))
                        Broken_curve = ghp.run(self.temp, zip_list)
                        Broken_curve = ght.list_to_tree(Broken_curve)
                    else:
                        self.message2('C端不能为空！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Broken_curve
                finally:
                    self.Message = '相交位置打断曲线'


        # 原始曲线延伸至目标曲线
        class ExtendTargetCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲线延伸至目标曲线", "RPP_ExtendTargetCurve", """将原始曲线延伸至目标曲线""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "原始曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Target_Curve", "TC", "目标曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "延伸方式：0=Line, 1=Arc, 2=Smooth")
                default_type = 0
                p.SetPersistentData(gk.Types.GH_Integer(default_type))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Curve", "C", "延伸后的曲线")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Res_Bool", "B", "原始曲线能延伸至目标曲线则为True、否则为False")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Extend_Type", "E", "原始曲线两侧都能延伸至目标曲线则为BothExtend；只能起点位置延伸则为StartExtend；只能终点位置延伸则为EndExtend；如果两侧都不能延伸则为NoneExtend")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM9SURBVEhL1ZRbbEtxHMf/TPBgiUtRO+d0dOfsJgiLrHQ93bARIlvE4oXEg5GQzAMR8eAWIh7Ei+uDbBMyQ0NbvZ/T7mIqu0RUuwsPIoZZL7R12Zj+/dr+g8XWdbMXn6fz+/5++f/+v8v5o/+KrjydxF7YqLQWWMuNG4zTiDx+HGqHVOTrt9h4xwWLSmg180LQtc6FXcVubOANS0jYmJkkqB1lotqus/FixF3SibtVbfhERSdeee7tgFMhXDWpLDtv596eSuKTx6q2lotqR4cHDn28phVbebHdphKPP1mmVUqqQ7vQ/X5MQsfGzbybEri1pmN9FxZ5x6CNt58XleIy4o5ji8xBteHLqOrldKIkh1apXdygbnzlLunAgsp+zawyM8T1N7dCAiQpJNbo3MnXLm0qbA4+LHr03Vhg2Urk4TmGJ6O7A0Gki5wkSmJ0Sp0MDvfB4UGNQreCyAlRnGk8Wnb47m5ijkx0h+vVDe7mIuc3jVIztNcJiKSmnh2QSK3EHJmWPMONp8XPMPS/mEhJ4afZQ14qww+rNIlIfzPzeqDy4p4e3J1RV0GkpPGmyddCEvw+PV1KpKFEZldTORf9EdSIMdIPVqCanjnElRQ+iqUDkCDAcCoiDaVBYRHqNjnDKXXhS+j+IEaa/sCq045s4h4VaE2Kl2I/eumMfUT6zYOCBzs88CM5l9/bFhNqQ6XIGGkX8je3RKQyl49hS2L6KEAV7TCHa8SMA4fPaihs+gIPlolIvwhLZdu/ybIwXpiDQwxb2yvj5MQ1LFBBVR/FthIzjllluQ77jvUKPUWkIbym5FyY5u5Ek3xmuB8fGe7Ic5Yd9jnuo+SVkCQA7ZocE4y8baVnfSfWKw0HYkIC/JR842ea8+BFufgTw70IMBmlxPULGLI6OmgfzcUva1ptWgVvjAY+R97dP3AgNOUDzR2ERAPRiqAy7VsZm0vcyMtkpUUTwByKiDQ+3iyQy0I0W4MXZuPvskwcpNlT7rlzZ0R9sEU+GPb+WOC/Er0pVNFG2vb6XRq7GWbQ5Idhk5CJAdqyFxYghNOzcT+T+dVHs9DNCaZ33qL50Kor0STQJieRJ54+muN9FJePEEI/AfSqZENpN+ScAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = sc.doc.ModelAbsoluteTolerance
                self.type_dict = {0: 'Line', 1: 'Arc', 2: 'Smooth'}

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

                    if not (Curve or Target_Curve):
                        self.message2('C端不能为空！')
                        self.message2('T端不能为空！')
                    elif not Curve:
                        self.message2('C端不能为空！')
                    elif not Target_Curve:
                        self.message2('T端不能为空！')
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
                    self.Message = '曲线延伸至目标曲线'


        # 物体确定曲线方向
        class CurveDirGroupByGeo(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-物件确定曲线方向", "CurveDirGroupByGeo", """将曲线最接近的物体的一端作为曲线的起点或终点""", "Scavenger", "Curve")
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
                self.SetUpParam(p, "Curve", "C", "待确定方向的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "一组影响曲线方向的物件")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                default_bool_x = False
                p.SetPersistentData(gk.Types.GH_Boolean(default_bool_x))
                self.SetUpParam(p, "Reverse", "R", "True靠近物件的一端为终点，False靠近物件的一端为起点")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "确定方向后的曲线")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQJSURBVEhLrdV9TBtlHAfwTqbI4qJmhmVSxmyLKX3v9WqQWtlwdFAZA8ZKCXGaLItkZvqP8e0P8Y2hsiqWJW7Z4iKysWaMUSnrKIyObVSSVbJNg0qqe3FMvL7QhZWXrdzP36NHIrRCM/dNPuk9z3P3/O7uubvy7lXyu/5ILbnOruCa9y75F9hUnfv2M2r7+Bmlcyqgds24NMf9b2ZbPCncLolnwxC7Sue+s5Z2Rl5TdU42Ke0Tl+THI1G1G0DRBaB0AchaghHqoO+lGoD7uMPiR/PtyLJs95319MmJ11WOyRacbEjRPgHq0wDUOQB1N4C8JQTyZmZIfejPA1TreDtlv9206eDlR7gpFg7VwuhpD4CmH0CFZydrZkDRzFykbOH9Okd0m2EANKXHfKkP83hkQmHy0qXV+PsF6kFjyIz+O/o+Nl3bdmuPrpPdahhglUX7vI9xkz2JSlAdcqMwgnn8KB/NTTj81qPcJslyJEabUT06i26h+ZONom70KapAMhS7wNPRLaYZtjgwM12wF5vkTBk0f7IR5ES7ECmchR5EC4cd3pk8M2a8BpALEFkHpw7Qxdjdh06g9xG5JeTW3F2mBssl4MsDuEIBXM2BkdPPvsENzQm7WrwqnC4Sku1AmvAdBtt/DywWf2chPXkmG6b6FRA5pwH319pabmhOQnzRDj9f2Orlae7HAiMJF/ilyaC82KSEHw6L4ftvZGCrp8gTEhPmcZEaJz4/yheU+vkiD9e9eG60F0t6G6VwrC4DOj4Tw5HdWvJExARXeQkW6AvyhYMBvjDuScQN01GW2WuVskdrM8CBBWwW2sINxSSQJtoDa7LAnyZcy3UtnlFHmcDdKI2SKyAFjlpoKzcUE4YvMEfSMyEkEOB7l2DGe8wr8RZNttWtgc7PxWBvoD/ihmIS4GemMXzRu1wzsQDAEleD5EKPVQAnGrLgvZfF27E7G61GyWSf/x2HRV3Q1SAJOa2qr5KSkj7Brtm3l3wKBtBh9AHaivToCbQMJZ7GXSWz/0g61IEuIVJgGs0W/LcgGkStiDxV21AeIm89+ZYtnhznJr380HpryorlG7FZit5GzciLQiheYeIm2o3iR+8152l/M/mo302gvlEBT4+9YNvAvlJdwdbk1LL2lbhuSdyu5MMoR+TjRxaf3MrziFzdERQ/fEt2iuSkYbvMuzGovFwOqqtbQHOzCuhwFVDXTEANl49qr5i79eEXPy5gd5a/yn6ZSR4W7nASsj4P/LO5QLLq12XITxXuVbQZihSuwmpZn3GftN/okX73fFg5XAZUsBLo8SrQMJWg+qksSl+v/PGpn0013OF3n9wduQ/Jbc/JVV0F5bLewg9lZ412qcf4q9K3GeSeIrI+GB7vLxGcxVTGg02mAAAAAElFTkSuQmCC"
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

            def get_closestPoints(self, curve, geo_list):
                point = curve.ClosestPoints(geo_list)[2]  # 得到物件距离最近的那个点
                return point

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

            def RunScript(self, Curve, Geomertry, Reverse):
                try:
                    rcurve = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    if Curve == None:
                        self.message2("C端为空！")
                        return rcurve

                    elif Geomertry == None or len(Geomertry) == 0:
                        self.message2("G端为空！")
                        return rcurve
                    else:
                        curve_point = self.compare_distance(Curve, Geomertry)
                        if Reverse:
                            rcurve = self.get_vector(curve_point[::-1], Curve)
                        else:
                            rcurve = self.get_vector(curve_point, Curve)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return rcurve

                finally:
                    self.Message = '通过物件确定曲线方向'

    else:
        pass
except:
    pass

import GhPython
import System
