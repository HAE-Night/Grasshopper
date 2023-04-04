# -*- ecoding: utf-8 -*-
# @ModuleName: Line_group
# @Author: invincible
# @Time: 2022/7/8 11:04
# coding=utf-8

import init__

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Rhino
import Grasshopper, GhPython
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
import ghpythonlib.components as ghc
import Grasshopper.DataTree as gd
import ghpythonlib.treehelpers as ght
import re
import socket
import time
import getpass
import base64
import clr
clr.AddReference("System.Management")
import System.Management


def _get_macaddress(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    if ipconfig_list['IPAddress']:
        return ipconfig_list['MACAddress']

def decryption():
    select = "SELECT * FROM WIN32_NetworkAdapterConfiguration"
    arrInfo = System.Management.ManagementObjectSearcher(select)
    prop_list = [strInfo.Properties for strInfo in arrInfo.Get()]
    Mac_List = map(_get_macaddress, prop_list)
    Mac_Address = filter(None, Mac_List)
    Mac_Address = Mac_Address[0] if Mac_Address else None

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
        if origin_list[1] == Mac_Address and int(origin_list[2]) > now_time:
            return True
        else:
            return False
    elif len(origin_data_list) > 1 or len(origin_data_list) == 0:
        return False

# 加密
Result = True
# Result = decryption()

try:
    if Result is True:
        """
            切割 -- primary
        """


        # 点向式绘制直线
        class VectorLineTaking(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-PDWL", "RPP_VectorLineTaking", """点向式绘制直线.""",
                                                                   "Scavenger", "Curve")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACWSURBVEhL7dYxCsJAFEXRXyhBMREEETdkkz42Yq+LsrKxzArchpWV6dyD3hexEKZ8KYS5cCCZ4jNVfuKfm2D0efS1xgEXXFHAWoUnXjjrwF2DB27Y68DZDrr5BjMsYOs7vO7fzOXhyfLwZHl4sjz8pxXm2GKQmx9xRwd9cu210M21MEodOJtCO/QEbaIlrI1h/wOIiHgDjy0m97DfZzoAAAAASUVORK5CYII="
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
                                                                   """修剪曲线，输入负数时修剪曲线，输入正数时延长曲线.""", "Scavenger",
                                                                   "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e96b5a92-6ac1-4a01-9e26-b341f34d39c8")

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
                                                                   """多折线指定序号进行偏移""", "Scavenger", "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f86b09ae-745e-4577-90b9-f5c72b7d6fe1")

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
                self.SetUpParam(p, "Curve", "C", "多折线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Items", "I", "多折线序号，默认为第一根")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移距离，默认偏移-10")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
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
                self.index, self.dis, self.pts, self.curves = None, None, None, None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def _offset_curve(self, tuple_data):
                single_data, dis = tuple_data
                new_offset = ghc.OffsetCurve(single_data, dis, None, 1)
                return new_offset

            def _replace_curves(self, origin_list, zip_list):
                for items in zip_list:
                    origin_list[items[0]] = items[1]
                return origin_list

            def _find_closest_pt(self, data_list):
                count, close_pts = 0, []
                while len(data_list) > count:
                    one_index, two_index = count, count + 1
                    if two_index < len(data_list):
                        single_pt = rs.LineLineIntersection(data_list[one_index], data_list[two_index])
                        if abs(single_pt[0].DistanceTo(single_pt[1])) < sc.doc.ModelAbsoluteTolerance:
                            close_pts.append(single_pt[0])
                    count += 1
                return close_pts

            def _do_main(self, curve_list):
                wait_offset_curves = [curve_list[_] for _ in self.index]
                res_curves = ghp.run(self._offset_curve, zip(wait_offset_curves, self.dis))
                replace_curves = self._replace_curves(curve_list, zip(self.index, res_curves))

                closest_pt = self._find_closest_pt(replace_curves)
                closest_pt.insert(0, replace_curves[0].PointAtStart)
                closest_pt.append(replace_curves[-1].PointAtEnd)

                return closest_pt

            def _get_midpt(self, single_line):
                single_line.Domain = rg.Interval(0, 1)
                single_point = single_line.PointAt(0.5)
                return single_point

            def _closed_curve(self, tuple_data):
                se_tol = 0 if tuple_data[0].IsClosed is False else abs(tuple_data[1][0].DistanceTo(tuple_data[1][-1]))
                res_line = rg.PolylineCurve(tuple_data[1])
                res_line.MakeClosed(se_tol)

                local_center_pt = ghp.run(self._get_midpt, list(res_line.DuplicateSegments()))
                return res_line, local_center_pt

            def RunScript(self, Curve, Items, Distance):
                try:
                    Result_Curve, center_pts = (gd[object]() for _ in range(2))
                    if Curve:
                        self.index = Items if Items else [0]
                        self.dis = Distance if Distance else [-10.0]

                        temp_curves = [list(_.DuplicateSegments()) for _ in Curve]
                        explode_curves = ghp.run(lambda cur: cur if isinstance(cur, (list)) is True else [cur],
                                                 temp_curves)

                        if len(Items) != len(Distance):
                            self.message2("序号和距离列表不一致！")

                        array_pts = list(map(self._do_main, explode_curves))
                        Result_Curve, center_pts = zip(*map(self._closed_curve, zip(Curve, array_pts)))
                    else:
                        self.message2("曲线不能为空！")
                    self.pts = center_pts
                    self.curves = Result_Curve
                    return Result_Curve
                finally:
                    self.Message = '多折线按序号偏移'

            def DrawViewportWires(self, args):
                try:
                    for _c in self.curves:
                        args.Display.DrawCurve(_c, System.Drawing.Color.Pink, 2)
                    for f_items in self.pts:
                        for sub_index in range(len(f_items)):
                            args.Display.DrawDot(f_items[sub_index], str(sub_index),
                                                 System.Drawing.Color.FromArgb(248, 141, 30),
                                                 System.Drawing.Color.FromArgb(255, 255, 255))
                except:
                    pass


        # 偏移多边曲线
        class PlineOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-折线偏移", "RPP_PlineOffset",
                                                                   """折线段分段偏移，三种不同的偏移模式""", "Scavenger", "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4121d1e6-b3a6-4e53-a4e6-c2346dbb6703")

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
                                                                   """简单圆弧拾取插件，通过参数修改，重建一个新的圆弧""", "Scavenger", "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c81a3c2c-9d6c-4833-9ad0-2fe541933635")

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
                                                                   """曲线集的起点和起点连接，终点和终点连接""", "Scavenger", "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8f4035c7-a253-4efb-8a12-c39d503bf27d")

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
                                                                   "RPP-合并曲线", "RPP_Curve_Join", """曲线合并操作（多进程）""",
                                                                   "Scavenger", "Curve")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGBSURBVEhL1dZNKwVRHMfx4zF5fogsZGNlQSIPC6QUdrK0YsfbYecNWNmjlI2yQJ4K5T0I2Yrvb07ndmY698zc3NT91afOqTPzn7nzPzPX/GcGMBwxhG4oPdA8tM7pRyoHuI94wRmUCzwjtM7ZQyotaItYwjWUO8witM7R+SrKFC7t0Fxh1A6rlxn4BcbssHqprQL1aLXDUvIK6MHW2WF+1MNPUOe4xAqs4RFunxTKOt4xn8xsW/oFxu3QLEPrVpNZJH0Y9OiWd/AJnVxX7BcYwSK+sAWt94/X+VI5wkPGCX6gjaV9oB2sqJDu4BXfOEX22EOk0gm9Y0S/ZQN28YYJhO5Az+UD22iEjnPn6EA0m9BvO53Myj8DPSMV2UhmBaMu0gtrLpnZxLpI3XaLwl2kfm6yw1Ly9kEzCu+DUPIK/Dm1X2ASfoGKvwfq296IFdxAUYctILTOaUcq+iZnd6NP3+BjKOfQyzC0ztlHKuph/bMoR3tD7xtFV6d5aJ3TZYwxvy/1aW+oB697AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def _join_curve(self, curve_list):
                curves = [_ for _ in rg.Curve.JoinCurves(curve_list, self.factor, False)]
                return curves

            def RunScript(self, Curve, Tolerance):
                self.factor = 0.001 if Tolerance is None else Tolerance
                trunk = [list(_) for _ in Curve.Branches]
                if len(trunk) > 0:
                    bole = ghp.run(self._join_curve, trunk)
                    all_bole = [_ for _ in bole]
                    New_Curve = ght.list_to_tree(all_bole, True, [0])
                    return New_Curve
                else:
                    return None


        # 最近点连线
        class PCLINE(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-最近点连线", "RPP_PCLINE", """几何图形到指定线段的最近线段""",
                                                                   "Scavenger", "Curve")
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
                                                                   "RPP-求线长度", "RPP_求线长度",
                                                                   """求线长度，并保留规定的小数位。""", "Scavenger",
                                                                   "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c683174a-8426-4e49-9fa3-0d986603bb70")

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
                                                                   "LenghtSort", "RPP-长度排序",
                                                                   """根据Curve的长度进行排序，从小到大。""", "Scavenger",
                                                                   "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e93bc482-0f62-42b6-bf53-97caa94435bc")

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
                return Grasshopper.Kernel.GH_Exposure.tertiary

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
                                                                   "RPP-曲线筛选", "RPP_FilterCurve", """通过曲率选择曲线""",
                                                                   "Scavenger", "Curve")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADfSURBVEhL7dS9DsFQGIfxug8RQgwmC4uBgbswWOxmNh8jdldhlBgY3ITFYrdYbDz/Jke0HFXRIOmT/IYifU/ibZ24n6yABbLu1YfLY48zdsjA1MAohBo8VXCCbm4cUYaa4fa7IFNcS6CFPlbQD5YYoAlVRS8EHfhhXWhAx72KoCE0QKeIpK8NCNqiu62xZRsQtEWerXmWbYBOqM9srFvj7///5EieAz3JbYyxgQasMYGecFXHW1tjKkHvHt3cOKAI5d8iDQ9dGnqL6gZbJGHyb9HLW+MvhzlS7lVctDnOBW5zXVOZwwLKAAAAAElFTkSuQmCC"
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
                                                                   "RPP-Equipartition Curve", "RPP-均分曲线", """均分曲线""",
                                                                   "Scavenger", "Curve")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("49378bcc-dac0-4845-a0dc-f934d8eeb669")

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
                    # 预知代码Bug之前（抛异常）可用
                    # self.mes_box("开发组测试", 1 | 32, "标题")
                    self.Message = 'HAE开发组'


        # 统一曲线方向
        class Filp_Curve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Filp Curve", "RPP-统一曲线方向", """统一该曲线的方向。
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
        return "Curve_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("99e47d1b-376c-4606-8812-cd6625f02566")
