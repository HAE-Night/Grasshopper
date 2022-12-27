# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Data_group
# @Time : 2022/9/17 17:06

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
from System.Windows.Forms import ToolStripSeparator
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
from Grasshopper import DataTree as ghdt
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import rhinoscriptsyntax as rs
import math
from itertools import chain
from decimal import Decimal as dd
import socket
import time
import getpass
import base64
import re
import random
import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 树形数据处理
        class TreeData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@树形数据处理", "RPP_TreeData",
                                                                   """树形数据处理的问题，B有多长A就会有多长""",
                                                                   "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("22bf3aa8-c9f3-420f-8cdb-eefc24ea864b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "A_Brep", "A", "A的Brep集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "B_Brep", "B", "B的Brep集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_list", "R", "对应结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJHSURBVEhL1dVbaM5xHMfxvzkUkVMit1yQaHK/GyxKIdy4kF04bLKmKJu1G9EcQgkJEUXJBaUpFJpCQhjlUI453yzDzcL7/fv9/0/Ps2ZMz3OxT732/P7/Z/v/vv/faUkvMxs70YxZ3ihmjuILWlIfcQED0OtMx0GcwjqswWuMQZYRuIXTOIb7uIKl6DHl+IGz2Acf8gsn0DXT4HcnUYVt6MAW/DFWbUX5qcHq2CzIYCyMzVwm4zsmhqsusfrnqA1X/58bWBabMVNwD+/QBl/X6vqhp4xDZWwW5CbmxWacrA/YjqHeIEOwF/3DVfyd7Lv8VOBIbIZY0GI4L7kOVuFBbCZjMSr9zJ9UV8am2CzIYfhA33Y4NmM5zuErfHayH4dskLlw5fgH3vPTjIdrfmC4itmNA7GZbIQbz8UxzBtkJlxRoZe3cB4cGqvaA6txsrN1vRLujZFwpeUvRauuw3FM8EaaVn84zo6ju9QJtgIrewg7eI8VcB58yB04Z8Y3uwY32yM0ogxZbqefIWvxODZDLmMHtuIJ7sIzyLe1A4foKVwcLzEVWezYRfIpXKVxM1lNlgXw/DFWfxFuIo8Dx/YSNqAJ/q1DZ1G+oQ++jknIZQZ+wodkcfeeh2eQk+gQ+FYeJXZ4Buth7KAe1fAI6TYexd/QgDmwcleWnczHLli567wd3W2yv2YJruIZsu0+Gh5k3rMAz5qi/z8wi2D1Ht0liUeBQ+M/m0HeKHbs4A0+oyQdmBdwU/bdDl6hZB14brlEO/EPHSTJb3hUgJMPbzb+AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, A_Brep, B_Brep):
                if A_Brep:
                    if len(B_Brep) > len(A_Brep):
                        Result_list = A_Brep * len(B_Brep)
                        return Result_list
                    elif len(B_Brep) == len(A_Brep):
                        Result_list = A_Brep * len(B_Brep)
                        return Result_list
                    elif len(B_Brep) == 0:
                        Result_list = A_Brep * 1
                        return Result_list
                else:
                    pass


        # 小数点的精度分析
        class NewRound(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@数据精度提取", "RPP_NewRound", """数据精度的重定义，优化数据（四舍五入）""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e2412c4a-0c46-443a-9c25-ca033de8bd30")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Decimal ", "D ", "小数（浮点数）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Precision", "P", "保留的位数")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "输出结果")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Percentage", "%", "输出结果的百分数")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Per_thousand", "‰", "输出结果的千分数")
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
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.switch = False

            def compare_five(self, carry, keep):
                if keep >= 0:
                    return keep + 1 if carry >= 5 else keep
                else:
                    return keep - 1 if carry >= 5 else keep

            def carry_ten(self, num_list):
                self.switch = True
                int_list_num = [int(_) for _ in num_list]
                if 10 not in int_list_num:
                    return [str(_) for _ in int_list_num]
                else:
                    for ind, num in enumerate(int_list_num):
                        if num == 10:
                            int_list_num[ind] = 0
                            int_list_num[ind - 1] += 1
                return self.carry_ten(int_list_num)

            def handle_str(self, num, acc):
                num_list = str(num).split('.')
                int_part = num_list[0]
                float_part = num_list[1]

                if len(float_part) <= acc:
                    zero_filling = '0' * abs(len(float_part) - acc)
                    extra_decimal_places = zero_filling if len(zero_filling) != 0 else None
                    float_part = float_part if extra_decimal_places is None else (float_part + extra_decimal_places)
                    return '.'.join([int_part, float_part])

                elif acc == 0:
                    change_num = self.compare_five(int(float_part[0]), int(int_part))
                    return str(change_num)

                else:
                    num_list_of_float = [_ for _ in float_part]

                    carry_num = int(num_list_of_float[acc])
                    keep_num = int(num_list_of_float[acc - 1])
                    change_num = self.compare_five(carry_num, keep_num)

                    num_list_of_float[acc - 1] = str(change_num)
                    keep_num_list = num_list_of_float[:acc]

                    float_part = self.carry_ten(keep_num_list) if '10' in keep_num_list else keep_num_list

                    if float_part[-1] == '1' and self.switch is True:
                        float_part[-1] = '0'
                        int_part = str(int(int_part) + 1) if int(int_part) >= 0 else str(int(int_part) - 1)
                        self.switch = False

                    float_part = ''.join(float_part)
                    return '.'.join([int_part, float_part])

            def RunScript(self, Decimal, Precision):
                try:
                    Precision = 0 if Precision is None else Precision
                    if Decimal:
                        per = Decimal * 100
                        per_th = Decimal * 1000
                        Result = str(dd(Decimal).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) if "e" in str(Decimal) else self.handle_str(Decimal, Precision)
                        Percentage = str(dd(per).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '%' if "e" in str(per) else self.handle_str(per, Precision) + "%"
                        Per_thousand = str(dd(per_th).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '‰' if "e" in str(per) else self.handle_str(per_th, Precision) + '‰'
                        return Result, Percentage, Per_thousand
                finally:
                    self.Message = "科学计数（精度提取）"


        # 列表取值
        class list_values(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@list下标取值", "RPP_list_values",
                                                                   """列表根据下标取值，取值下标空格间隔""",
                                                                   "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("969903d7-b159-4520-be02-36ef0cad97bf")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "列表输入")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "I", "取值下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "获取的值列表")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMVSURBVEhLtZbZTxNRFMbnL4HwZOJ/oC8GeCJGMzYFpEQxslWWBkyRRXYCDktAQJaqlFq2NOEBpcQItqQsRRRQIGAolZZaIjxYIlQ0Uvo5985YMAUUUn7Jl07PubnfvffMnBlmd3c3AgC3vr7OsSzLBQUFcSEhIadScHAwVUpKCkfmJGK8Xm+jx+OBUqmETqfDwsICLBYLlpaWTqXZ2VmoVCoUFxfz8wPM9vY2V1RUhJmZGRoIFGSxLS0tYGpqaji1Wi2GA0tlZSUYqVTKjY6OiqHA0tHRAUYikXBms1kMBZbu7m5hB+Pj42LoeFZWVmAwGGA0Gv00NjYGt9stjhTo6uo6mUFcXBzkcjlycnL+Um5uLsLCwtDf3y+OFDixQXp6OsgtfRgajYZOeJB/Gnj2vPi1uyf+AxQKBWQyGZKTk31KSkpCQkICQkND6fEdhBqwrIR7MyEU2ercRJnajKInY2jXz6OyYxKDkzaaI+zsfIfdZoXt0zIVuV5zOuHktbGxgb29/cUQqIHsehSnf2mAYdqJet0UBt/a0WdapgbGqVV4veJonty8PFxmoxApu00VcUUKjiMd4XB8BoZhE6p65uhqHRtbUDYOo7bnHbpeLYpDBWJupeJqxSIS2r4hUb2NiMJpJKcpxaw/viN6PzWJn3ztytrNUPV9wPpXN92BZmBeHCogjY7F+fA7uCC9j4uR+Th3KR7xiXIx6w81IA/anyK3vZhDads4dK8/oo7fQQl//XxkmeYIVusyRoaHfDIZh7D6eU3M+uNnQLA4XJiYXwM5enIHbW79EBI8vb29eFhbjdbmBrQ21dPfhrpqcOWl+6ooRVlJAW10nZ2d/gbHcTOGxaSCwZcHvMqPUAUDWyGDOEkoVE+1pAbsfxvERrPoucHAdJdXxhHKZDCUxiD2Wjgetz07mYG6XYPUjHvIyMo/VmmZOXjU1MzXgD8iYnCm3ZQYkE54FtAiFxQUcFqtVgwFlqqqKjDkayI7O5u+sAPJwMCAYMB/tjS6XC7aKfV6Pex2OxwOx6lltVrpqzIrK4u3AX4DaDWVAOFbm6IAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Lists, Index):
                if Lists:
                    indexlist = Index.split(" ")
                    List = []
                    for i in indexlist:
                        List.append(Lists[int(i)])
                    return List


        # 树形取值
        class Tree_Values(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@树形规划取值", "RPP_Tree_Values", """Explode-True 对树形数据拆分 统一路径.
        Explode-False 取出branch路径的值""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("0eff0c49-1b47-4d30-a4bf-ddfae9774fb2")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Tree", "T", "数据-data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Explode", "E", "True-将树形数据拆分整合，统一路径；False-根据Branch取树形值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Branch", "B", "取值路径信息")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Objects", "O", "输出结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, False)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPuSURBVEhLvZbtT5tlFMb5BzQxJn6ZDlraUkZpmW+JsEEpfX8vMGDMycbalXcN9BXap7VrGJlaB5i5GEQ2J4Np5mLULYuy+fJ/XV7nkbHV1g8asg9X7uZ57udc9/mdc+604YuViufG8idXPsuVDl0St6H4bnS1MjSGcnjk0CVxG4pnxpcvBYew6A4fuiTuczTwhJF1hZC0+ZGw+pGyBep+9Kyy+2vBE0HB248ipXgjB++rDDLOIHIDI1hPTGBtPo6Pp6NIO0MHm/9NC9SY049zlKxxdwg5HlbeVRnI6TM8yU4lgT/vlvH7dyVcnYshZQ/WBM0wSN7Xjw99Axi3uXFUr4fGYECTTgejuQMTrqCaSZWBIFro8eKjiXHs7RTxiNqpJJG0P81CkCgMPMegbzVqmWEAsT4PmpqboWNwVS0tiJNGjUHGQeZDo7hzPYcfNhXc+1JB8fQo0vantSj4B5Fk0BM6IyyvNhJrAHGHH0aTGW2U4VgbHCesKPoH1P1VBoIoxSJtlT/Ao9tF7G0XsM5aCKIlZpdm2pPdDjha23HxZJ+KqRw4hQvMRtdihNFohIGnN3e8gUnuzfObKgNBlLD68OlsFI93i3hMRGKW6ONmGke7ehncjBmrCxPddrz20stY6PPiot1LRFoVTzNXjUGPGDOrQZQlt0V20fa1PHY+z2GXqFaTUzwpiyodRpPLkdNqJoIo3PGmGiTu8MHEwlosx9FmtiB00qa2bH1E7giuL83gxy0FD2/k8Nu3JWwos0g5QmpgQSOIJAv5LRim+PydLiu6OnvUNUhkWT6vMRBEqV4/Vs6fxc83C6rB3jcK7m/loUSGMdPthMfUgdleNwZefxuvvPDiAaKjmiZotRpouTayXc+x8ApbvspAMGQDg9hey+L7jTx+2sypRpWZKBKcbkF0pf8Mznda4TpmxpTViRK7KipFZoGNxlboDS04TlwyfDJsNQaZ4CBur2dxb4PBv8rhwdc0mI0hzUK/z0BOBpYsluRqYCvKKWN2n9qmpnYLWk3t6OnsRrZeDQRRUkX0Hu7fVPBgK4dfb+Xx8JaCwqkRzNu8ZO9UB00MJIAU+YLNBQ07SM9pNuh1aNpHJPdTtQE/kGJuFufwy25JneQ/7l7CnaspZBhI3gsmWZ9IukWuiiNaLRrZokdYAwszSfKwNYikixaJaD09jTW257UMlZ2GMjhcNc3PSoLMEa2f0xuiZJ3khSeZybVSk0GW0ykFFS0Ql1zbUhvB98/gf+8Pq1Ne5KX3RPn94PK+xuCw9XwMSmejy+XQsHp5SXdIyvU2/x+pBvORkdWV/lFcpuQqXiTDZf6u9y/hv6oyNIa/AHG1pSM2zID3AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def treegroup(self, Group):
                GP = Group.Paths
                treetype = type(Group.Branch(GP[0])[0])
                Objects = ghdt[treetype]()
                gplist = []

                for i in range(len(GP)):
                    for j in range(Group.BranchCount - i):
                        gplist.append(GP[i + j].IsAncestor(GP[i], 0)[0])

                for gpbr in range(Group.BranchCount):
                    grouplist = Group.Branch(gpbr)
                    if Group.BranchCount > 1:
                        for libr in range(len(grouplist)):
                            if gplist[gpbr] == True:
                                Objects.Add(Group.Branch(gpbr)[libr], GP[gpbr])
                            else:
                                Objects.Add(Group.Branch(gpbr)[libr], GH_Path(gpbr, libr))

                    else:
                        for libr in range(len(grouplist)):
                            Objects.Add(Group.Branch(gpbr)[libr], GH_Path(0, libr))
                return Objects

            def RunScript(self, Tree, Explode, Branch):
                if Tree.BranchCount > 0:
                    if Explode:
                        Objects = self.treegroup(Tree)
                    else:
                        GP = Tree.Paths
                        treetype = type(Tree.Branch(GP[0])[0])
                        Objects = ghdt[treetype]()

                        if Branch:
                            for br in range(len(Branch)):
                                tu = [int(i) for i in Branch[br].split(" ")]
                                GH = tuple(tu)
                                obj = Tree.Branch(GH)
                                Objects.AddRange(obj, GH_Path(br))

                    return Objects


        # 列表切割
        class List_Cut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@列表切割", "RPP_List_Cut", """在列表指定下标处切割列表，树形结构输出；
        （原电池最后一个下标不做参考，已改）""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("dd4e55e7-7e2c-4fb0-95ef-adaf2461397d")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "需要切割的列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "切割下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataTree", "DT", "切割完成的列表为树形数据")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATRSURBVEhLlZQNUFRVGIaFBKUgwdT4S3SbiRUFTBQMCIap0WCMMZB1VsHAAB3QQYhaoJkoGAVWfkQUkpV1RcFNVEBWkVRIWDZ+lASWAM0JJQJjJARRcZb79t3dW9M4TCzvzDP33Hu/93v3nD3nzplOAPhjAz2iP+qLkx8osveyDDWcSv9LfeOQRqPZxpXpL4ZhTAjbw4cPf5iQkLCBxu/frzl2sy/uHXTv5eEXlkhLDEvCMMVMHeNs+qutrW2dQCBoNDc3h6+vLyjA8W5RtLjzs0VQCs10BL4C9bcb2Xezn0F6enp1UFAQ7Ozs4OXlxTbx7i6KSu8MX4LG7QsIcyi3GKMzRRvgxNn0V19fn4iMVd7e3lNubm5sE48eKc3gpQB16kfsu/c42+xERisPDw84OzuzTTIHao93NG2dD9U2My3KwLno3u/LaBjmC84yO1FTW09PTzg6OrIBkt+vFjb/xK79dgstDQITmsFGDe2wIM6ivwYHB18bHh7e5u7uDj5/BfNkfLz8dtvP7Yey8pGTdVRLduYRlBSfeabRTEZwNv2VkZFxnM/nw9jYGIaGhli8eBFzorSCOSCrwzeF1Vq+yq+C/GoHOzs/zqa/aJuKy8rKhktKSvpLS0v7S04X99cqb42kFlxEakGFlq+PnMeZyy1swLucbXYi4+vEPFpjI2JBU/u9S2JpDRdQieSj5ThRfuMp1cQSAkJIrCc+YJgJa67N9KKGFgSPu2XDbPqGHv96UHYNYtlVLWlFVyC71Do5xjDXRhlGwV4fM0wz7apy8m7mrNOLCiwrKir20598lnbSueDg4NY9++I0foGf4uOgUPgLQrGJroEhu7EzPhWhcSladiVm4MsD+dgXG98VEBDwvVAovBAREfFDeHh4CvU059prA0wlEkksew5cXFzg5uYKhxUOWMEnHAga29vzsWw5D7bW1rC1YbGisRWsLS3x1tKlcKC6lStXgsfjwc/PDxMTE2u59jqNj4+/2dTUtCctLc1FoagMuHipJq7murJKfr66kEVxpbZS8WNzV57iNjLPtyDzXAvEZ1twsrYH1+uVsry8vDVyuXxHTEzMVpVKlUXL7EXM49rPLCq2pnUXX/gNkLZrIGPpAMp62cPN5OwM3ZFrZGR0x8DAYGT16tXDFFZEz5dw9plFxckPhwZaK0/JUFZUiDKpBGePf4cq+WnmxbMnFyIiI5GUlIRIulI56Lv2gpbeU+fWQxQgHKqX53WELoQqwACqLXPR+MkctEe/jUf3e1JpGklU4zoyMiIxMTGBj48Pe2b8OfvMomLHB5cL4ruil6NRaKr9yiq3muBu0noM9dwK5mrmhYWFVdMQOTk5fXRvxz7XS1S8duC6NFEXYKb7hAteRW+iK0bvd+ym92/k5ubKqBRRUVHsrw/TOfXUPwHqaN6/AQ00g444JzCTY+JC6cl8U1NThISETFFtIWHDWfUTGdYMXpOKXg5oj3XC89FB2YKFi8eoDKtWrZqysLDotbe3v1dXVxeqc88g2g2GFLCpv6YgUR2xhP5gI6gE81G/eQ5ady3DxKOB2wezD00mJycjPj4eIpEI2dnZUKvVn3Mt/l9cQNrzP+887En3R6vIHTcTvdCdsgGDRZF4OjJwjN6vI9z/Ax00ZuHfi+JXnno5lNAAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def ListToTree(self, List, index):
                DataTree = ghdt[object]()
                for i in range(List.BranchCount):
                    list = List.Branch(i)
                    if len(index) == 1:
                        data = list[0:index[0]]
                        data2 = list[index[0]:]
                        DataTree.AddRange(data, GH_Path(i, 0))
                        DataTree.AddRange(data2, GH_Path(i, 1))
                    else:
                        for j in range(len(index)):
                            if j == 0:
                                data = list[0:index[j]]
                                DataTree.AddRange(data, GH_Path(i, j))
                            elif j == len(index) - 1:
                                data = list[index[j - 1]:index[j]]
                                data2 = list[index[j]:]
                                DataTree.AddRange(data, GH_Path(i, j))
                                DataTree.AddRange(data2, GH_Path(i, j + 1))
                            else:
                                data = list[index[j - 1]:index[j]]
                                DataTree.AddRange(data, GH_Path(i, j))
                return DataTree

            def RunScript(self, List, Index):
                if List:
                    DataTree = self.ListToTree(List, Index)
                    return DataTree


        # 数据清洗
        class Data_rinse(component):

            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@数据清洗", "RPP_Data_rinse", """去除空值和空格值""", "Scavenger",
                                                                   "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("13b14752-b265-4040-bfea-81d0c089b31b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "需要清洗的数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "清洗后的数据.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGpSURBVEhL7dIxSAJhFAdwHYSSC3ELbfOGSAfdDAfFQUKhJbEbWhLEwaDFJg2kQRwc6xzEa3VqklYlEKHpBEXEEAXDDEflhtNe3/U9ELfsbqp+cNzd/717H3z36f79Hkaj8SiXyz2FQqFrjDRjiEQit51OB4bDIbjd7ivMNbGXyWTqQPT7ffD7/VWSbdGSevuCIIyU4ZVKRXa5XHck26Yl9ezlcvm11WpBNBrlyfsBjbXhSSaT79PpFMxmM4eZNkwm0wnZDkn5mYFAoI+xNhwOx0WtVlO2/Eu9XpdYlj3HsjrkdGTb7TaOXmk0GkAWPiMtetq5OT3Hcffj8RhHrpMkCeLxuET6zLR9M0wikXicz+c4bp2yaLFYBK/XG8b+jeym0+lnnLVmuVzCaDSCUqn0YbfbT7H/+ywWi5Pn+Rect0aWZRgMBlAoFCSbzXaMn2zGarWGRVHEkSvKfvd6Pcjn828Mw3iw/WecTudlt9vF0QCz2QyazSakUimRlFnapZLP58tOJhNYLBZQrVYhFos9kHiHVjUSDAYF5aSQ+w1GmjOQ65A+/k063SdJvTL9DOGD2gAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Data):
                Datas = ghdt[object]()
                serial = 0
                for data in Data.Branches:
                    one = [da for da in data if da and da != " "]
                    if one:
                        Datas.AddRange(one, GH_Path(serial))
                        serial += 1
                return Datas


        # ZiYe数据对比
        class DataComparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@数据对比", "RPP_Data Comparison", """Group根据条件分组.""",
                                                                   "Scavenger",
                                                                   "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7b77656d-aeeb-4066-a831-c3a7711ab743")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GroupByData", "G", "分组依据 list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GroupData", "D", "分组列表 list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "ByTree", "G", "分组依据所得结果 tree")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DaTree", "D", "分组列表所得结果 tree")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIHSURBVEhLzdVNiE5RHMfxS4q8y8vCBkWxQSmKxayVFYVsWEgkkRA2bEyxkbKxmcU0FJJILBV5CSklFhKRlwUhQuTl+73dM/2dOTPzPLLwq0/z3P+5585zz/nf+1T/U0ZiEsZjiIV/kUU4hOt4gfd4g4c4hbUYi7YzFxfwqwXPsQUtZz2+onSxgVzEBAyYrShNbtVduEfFLEVpUrsuoU/GwE30hB/N31xe/4hvWS3ZgD+yGw4cxxx8aI6TLlj/DLtqBobCL7YSjxHPfwnbus4wpBPcKHMSccI8zMJOmMWwc9bUR1U1Fa8Q56xGnQVIRW95HOJ+PIPZhSlYhTSmazCdiPUTqGNbxgHXz9t/1xwfgbmD0cj/gbyT81ntPursRxy4AuOT6vF8uOZ+3gOzBNtxEDcR5yevMQrVgaaQfIe9vAJuttmHNH4Y0xCzCfEa8pVSv0Z2NIXIZXJwL8wDWL+Hn81n30tP4HxzDvEaT2EDVcuaQnQVxr2wg6zZoia1dGRcvli7jDqT4eQ46DJNh0lL6IPmftjfbqgP5iNsg8nvwGXtzRnEQbmuJi2PfE3PRJ6NSEuXzEZvFiIOyjXszmr6grOw723h28jPOY0+OYb8xL/xCXmX1RmBWyhNasdy9JuJuIHSxMG4B+swaIbjKEoX6Y+vhQ60FX/we/AWpYvK99Nm+KUKqarfY3pEF6ebo90AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def indextree(self, gbdata, data):
                if data == 0:
                    if type(th.tree_to_list(gbdata)[0]) != list:
                        atype = type((th.tree_to_list(gbdata))[0])
                    else:
                        atype = type((th.tree_to_list(gbdata))[0][0])
                    gbdatatree = DataTree[atype]()
                    datatree = DataTree[int]()
                    for i in range(len(gbdata.Branches)):
                        gpdalist = list(gbdata.Branch(i))
                        list1 = list(set(gpdalist))
                        list1.sort(key=gpdalist.index)
                        for j in range(len(list1)):
                            num = gpdalist.count(list1[j])
                            gbdatatree.Add(list1[j], GH_Path(i, j))

                            for un in range(num):
                                index = gpdalist.index(list1[j])
                                gpdalist[index] = 'aaaa'
                                datatree.Add(index, GH_Path(i, j))
                    return gbdatatree, datatree

                elif data != 0:
                    if type(th.tree_to_list(gbdata)[0]) != list:
                        atype = type((th.tree_to_list(gbdata))[0])
                    else:
                        atype = type((th.tree_to_list(gbdata))[0][0])
                    if type(th.tree_to_list(data)[0]) != list:
                        btype = type((th.tree_to_list(data))[0])
                    else:
                        btype = type((th.tree_to_list(data))[0][0])
                    gbdatatree = DataTree[atype]()
                    datatree = DataTree[btype]()

                    for i in range(len(gbdata.Branches)):
                        gpdalist = list(gbdata.Branch(i))
                        dalist = list(data.Branch(i))
                        list1 = list(set(gpdalist))
                        list1.sort(key=gpdalist.index)
                        for j in range(len(list1)):
                            num = gpdalist.count(list1[j])
                            gbdatatree.Add(list1[j], GH_Path(i, j))
                            for un in range(num):
                                index = gpdalist.index(list1[j])
                                datab = dalist[index]
                                gpdalist[index] = 'aaa'
                                datatree.Add(datab, GH_Path(i, j))
                    return gbdatatree, datatree

            def RunScript(self, GroupByData, GroupData):
                if GroupByData.BranchCount > 0:
                    if GroupData.BranchCount < 1:
                        GroupData2 = 0
                    elif GroupData.BranchCount == GroupByData.BranchCount:
                        GroupData2 = GroupData
                    elif GroupData.BranchCount == 1 and GroupByData.BranchCount > 1:
                        btype = type((th.tree_to_list(GroupData))[0])
                        ggdata, GroupData2 = th.tree_to_list(GroupData), DataTree[btype]()
                        for i in range(GroupByData.BranchCount):
                            for j in range(len(ggdata)):
                                GroupData2.Add(ggdata[j], GH_Path(i))
                    elif GroupData.BranchCount % GroupByData.BranchCount == 0:
                        btype = type((th.tree_to_list(GroupData))[0])
                        GroupData2 = DataTree[btype]()
                        for i in range(GroupByData.BranchCount / GroupData.BranchCount):
                            for j in range(GroupData.BranchCount):
                                ggdata = GroupData.Branch(j)
                                for j in range(len(ggdata)):
                                    GroupData2.Add(ggdata[j], GH_Path(i))
                    gbdata, data = self.indextree(GroupByData, GroupData2)
                    # return outputs if you have them; here I try it for you:
                    return gbdata, data
                else:
                    pass


        # 列表多下标取值
        class Subscript_Value(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@多下标取值", "RPP_Subscript_Value",
                                                                   """多下标取值，最多取到六组数据""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8eb91efc-115a-4abe-a586-048a30d39705")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "原始的数据列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "I", "将要取值的下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "第一组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "第二组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "第三组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "第四组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "第五组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "第六组数据")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARWSURBVEhLtVZtTFtVGK6dIh0MV4l142MDliUuQWdqgPE5mHQRGOzPNmphDMPY0DoUXdJlYg2QkDAVgThlQDviXEAki1tEwZkyWkazAiXjo4WuUiCAwi2UALWddPf1Pde7iHEMNvFJnuS+H+d5znlv70k5DwNN09tdLtcRF02fpumlBIwjkK+TGABikU+yrY+HP2g6zHXPdQ1FL6FYFDIInw+RGJmC3Mq2rg244GmkNxtyHA7HDtytfKy5akJ/dm+vThbRri9I7O8tTh4bbVHcwV5/tnV1EPH09PQbfn5+cyqV6hibE5BRdH0Qp7+dygV9uifoxO6gO8iBgfPHZ7C2kVm8FqCYV0VFxYhUKoXh4eHP2dzzxKCnMFHXKdkIN9M2M7x1xA0MF96ceCQDbPZsbGy8WlZWZp+amoogOWKAjOspTOpcDwN+Tk4O5e7uDh0dHRI2twUNXl2XE5AR5eXlUb6+vmAwGM6wOW9k2O2CRH232A20Ek/oQOoOc2Gw8uQE1nho8gQj8ABgjcs+/stAdj+HDDVWn6LaxJug7ehWhhqxFxgU71MosFmv1++NjY09h+1SDw8PKZfLlZJn1HoX1/oRHQasgdXHxweMRuNZJud07sT8qSvfNZvKK+uh/MK38On5S3CuvBaamlUWrHlrNJr8hIQECAoKAlwCfD4fhEIhyOVy9IcXiA4DDJ5CgymBQAAjIyPHSQ4FPJAxX19Tm/cdPAZHcwvhTGk9FClbQdU5PIo1HnL3wsLCxb6+PiOPx4OsrKzF+fn5b2w2WzHZwH3xDZmZmTvr6uoGampqoKGh4UR2drbwo6KiKHzhRdWXrzjCouIhMGAb7NoVDNH7U+Cd0/njymrl262trcwuzWazHL8hwG/JzIguBzq9KBaLp0NCQmwikcgeGhq6EB4e7oyPF0FSUiLsCY+mo+Jeg+DglyBguz9sEfBB8Jw3REZGgkwm69ZqtWFkrGS8aWlpw7jhf95RaOBRX18fjKfwz8jI8M3Nzd1GiDkhvvC3Kr+6+sueGBEEBgZA8O6XYX+yGPILPh4rLS2NtlqtfkQQR1S8osFKwMZn0Dyuqq65+8ChN+DEe0Xw4Wd1UFJ7HX7QDPSwbQx6e3tLiIFEIiEGG9j0w4GNbjR9r0RtmHZU/myBKpUFvmwZhC9a7kBLl2Uc63y2lYMn+AR/ppCamjqJm+Kx6dWBzdFtplm7UjsLFzumkRTU3pqDG0YrhTUvto1DUdRJvGqgqampf7nxqiAGatPMYk37NCg0k8hfQamdAbXJNr58pyjqiXEk8lk2tTbggpgHGbQNzT7aXbQSWAP7/2JARoCMaxuy2hQ3KUZcofntrxENzUyuhwG5Kva1Gqm5qnYKqtSTDGu7FuCnfkqPBn/flo8D9sUl60fnXT8OOuG6yQEtQ7/D9wY76Cyz5Gf6306AAu7IV+7edR12Li0l2Z3OlEXn0oElhyMeY/I3ZhPbugI4nD8BuclVqrEz/HkAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def handling(self, sub):
                if len(sub) < 6:
                    before_list = sub + ([''] * (6 - len(sub)))
                    after_list = [[_] for _ in before_list]
                    result_list = [re.split(r"[.。!！?？；;，,\s+]", word[0]) for word in after_list]
                    return result_list

            def get_value(self, list_data, index_list):
                return [None if index == '' else list_data[int(index)] for index in index_list]

            def RunScript(self, List, Index):
                if List:
                    index_array = self.handling(Index)
                    origin_data = [self.get_value(List, _) for _ in index_array]
                    output_tuple = tuple(origin_data)
                    D1, D2, D3, D4, D5, D6 = output_tuple
                    return D1, D2, D3, D4, D5, D6
                else:
                    pass


        # 求列表极值
        class ListExtremum(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@列表极值", "RPP_ListExtremum", """求一组数据中的极值，{1:最大值，2:最小值，3:平均值，4:求和，5:累乘}""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d3639f42-b6fc-4b3a-900b-a28a0c3ecc08")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "List", "L", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Extremum", "E", "极值的类型")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "极值结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIrSURBVEhL3ZXPa9RAFMdXEcEfFxGXXnpqS2XFi1f/BC+iF/8JLyJ6KcRTETzarhuTSXaTJpOJ+TWTuCa7lnix/4R4ExTBg3oorYf4sjwXjet21B7ED3wJ78tj3szLm6T1/6EoylGWbK8SNuwQlkir7/ILGuPLuMxsqqo6QmgqnHj8UXfFnu7yL9KiYtflzz/rNFnH5X6m3j0kv+n7w5ebNF40nHRFRprFl1UnOG9How+E8hiXm43hiUtOMq5ML7uJlhTmk+HADou3hLFzaP0a3UluxKOdqmeHV9CaC2xqjWUvqocGu4jWwRAq1qnYrro6W0VrJqoVX603A8/raMkD7yK1w/zdxoZ/Gq0feERYx0vLirD0Hlq/h+L7x60wfz0IhmU9YWhP6DrZGej5e9jE/Jd6EJsGXbSjYg/G8BZaE4gr/EHw7JWilMfQ+nM0Nwk0R2QYToACn9St+A6GfwfMdgAXL8RwgkH5NZ0lcwdAGuKJsFngUGkW6NPhEkyXbnipCa2aCi6oqVN+F9PkaRYgdtLZigoOBTK4L1M58SiDQvcxTZ5ZLepaYdv0s4Xv5WflgmUVpzBFnmYB0+OXoUW7cIJ9GICpoEX78LEsMU2eWScYDKKzVli065N8U1gUbcZ2TmCKPM0Cj+HnArf4KfQ9hx1P5SbjnLj8AabJo3si1VyRYtjq0WjJCvIe/Jw0WHgqJxrpcONvY5o8k4VAGB4+dV9VVZzE8F+i1foKBGmoNnILxKMAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = {1: 'Max', 2: 'Min', 3: 'Average', 4: 'Sum', 5: 'Multiplication'}

            @staticmethod
            def Max(list_data):
                return max(list_data)

            @staticmethod
            def Min(list_data):
                return min(list_data)

            @staticmethod
            def Average(list_data):
                return sum(list_data) / len(list_data)

            @staticmethod
            def Sum(list_data):
                return sum(list_data)

            @staticmethod
            def Multiplication(list_data):
                multiplier = 1
                for _ in list_data:
                    multiplier = multiplier * _
                return multiplier

            def RunScript(self, List, Extremum):
                Extremum = 1 if Extremum is None else Extremum
                if List:
                    instruct = self.factor[Extremum]
                    command = eval('self.{}(List)'.format(instruct))
                    return command


        # 树形取值
        class PickingFruit(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@树形取值", "RPP_PickingFruit", """取树形数据的分支，输入要取的分支标数""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a3450556-ece6-4485-a9c5-bb07f47901c8")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "树形数据的树枝")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R1", "R1", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R2", "R2", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R3", "R3", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R4", "R4", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R5", "R5", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R6", "R6", "得到的数据")
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
                        self.marshal.SetOutput(result[3], DA, 3, True)
                        self.marshal.SetOutput(result[4], DA, 4, True)
                        self.marshal.SetOutput(result[5], DA, 5, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOvSURBVEhLzVVfbFNVGL8JKVn/hUzGut577u1Gt3Ww0rS7be+f3rZjSxgJogtBghAycWs7xp/h4pw69MHMMBNBCSGaKYSta3FrcVDWhAUT8I0YEk0MkWjiG8YHeQINPIyP71wO+iKMzT34S25y7jnf9/vO932/cw73v4D7xos2NlxeCOe0IbGg/0imtdtiUb9KJtTNbOm/Q5hUvvDMJUE8HwNxWgepZID0dQz48UgXM1k6SE6NSjMxIOc0wLH58TjmMQBmAlJOkZnp0iDk1cPSbPwf8q80WPtlGJqPBUAqJ+jcGDNdGvis2vUkACUXswoow02w7tMg1GIWuIHLzJSTb8gWd2mRIqjOKy4kvytcNCDyXhO0Z2rh1U2rwTsWBuFKK1ReSryV7PJUePLKyZqS8SuZ0n4jBb3Ej4dDjGJhkIloJ22wNtJs9kIb9sG2nTxUzcZ/2dX+wpEdL1ff3P4agcTbjeC+YIAHMxantXtkUt3AKBaGK69t8Y4rN73jUVgzY8xv76z+MxW0zm7d4b4jogjqsC9bMaj/4wC4p7D5GIjklFuuiYCdUTwH4JUVrrmkv6psNO6NOkf711ru1p2OlL3YFzfKt/FUC8TebAAXZkt75imbvdvNvBcH3H3//saVP6yaS45GjwfAeKMeOvaK0PLBeqgpPg5gimNSHWEuC0MoKAE8zWEO1TJUyRn7/BV/+D4JdJBp/WFyoB70wQZTaZT87wyy2uvM/ekQ8lobNu06koO7FIeqcuKWd0w+uC9gfThYze12XGnt479tgxqz7o/JpUtxEHLqbSlnVDKafwfJRt+XUKIiOvNYZxlLsCXtgY5uCbriq+Z7/dafqR2e7o9IUX9gXiNoS+8tPq89W6pCXlGkGTSe0kxlqO/4IHqkCXwnQ9DeWwsp1QmHI3ZIBSt2UXsypdaTGaNTKOobubRsMUmeBTKpfEivAzytUHsmAptw12toGfAfywSB0Q2/H/BX/NUdsn/PXBaHJwFoTXnMIo5Kaeurg6YTQRAvJ8H5TevRg17LZ71hO6RlRxVze34gsXmT0hLRLLDZ0PC5DLQn+C7c5356id/vW9k/oDpoAIO5LQ58VhmmTaPHX6Kyow0s6t+Rs5EEXe9psR0f1J2QarEt/W1AheikoI3gJXZUKMRa2bSJnpD9+oDmgEzQ1s2mlg89EXtzRrbPH4o6IBWyZtj08iAtcxYszzVaHvrh+F22tDzYE3GuTodsQxnZmukL2/Z0hxzr2NJTwHGPAP8gi3u8n2FzAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Picking_Fruit(self, tree_list, sub):
                fruit = []
                for leaf in tree_list:
                    if leaf is not None:
                        single_leaf = [list(_) for _ in leaf.Branches]
                        fruit.append(single_leaf[sub])
                    else:
                        fruit.append(None)
                return fruit

            def RunScript(self, Index, D1, D2, D3, D4, D5, D6):
                Index = 0 if Index is None else Index
                origin_data = [D1, D2, D3, D4, D5, D6]
                available_trees = [_ for _ in origin_data if _.BranchCount != 0]

                single_data = self.Picking_Fruit(available_trees, Index)
                result_list = single_data if len(single_data) == len(origin_data) else single_data + [None] * abs(len(single_data) - len(origin_data))

                R1, R2, R3, R4, R5, R6 = result_list
                return R1, R2, R3, R4, R5, R6


        # 数据比较
        class CompareSize(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@数据比较", "RPP_CompareSize", """数据比较，用于比较长度和面积的取值（几何物体），也可纯数据比较""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("607f91d1-8b00-4700-94cb-e7e11714f13f")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "对比的几何物体，可以是线段或者是Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Specifylen", "T", "指定的数据切")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Closed", "C", "是否闭合区间，默认闭合")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Compare", "S", "选择大于区间还是小于区间，默认大于")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "G", "最终的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Excluded_Data", "E", "被剔除的数据")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAF/SURBVEhLzdVLKwVhHMfxKQs2LiXCxsJCShZEsbDwBmTlsuIN2FhZyFJJUexEXoKNEgskl1y21nIrCwvJJRTf38Oc5vbM86Sz8K1PzHPmzL+ZZuYE/60K1Pz+LVp9WMUlvvCJe5xjCb34Ux04gA4qu5jHYWQttIk2eDcGffEZ46hG2BSSA+QFI3A2Cn1hB/VaSDSD5MGjBmFNp6md9lCihYxcA97QjMxO8YToJUnmGiBbSKW7QR/qmuflM0A6EWsN7yg3W/Z8B+iOi3UD3YqufAecoJCeTC2mpmbkO+AOZTDVQovTZis/3wEPqIIpPIMFs5Wf74BbFM5AXWH/59/cfAccI9YKPlBptuz5DphDrB7ogwmzZc93QDtS6e35ijqzlZ3PgA1k1gLtoOtXqoWMXAP0Bm6CtSFoxyM0aiGRa0A/nA1DO+vXaxINCLP9HjxiAN61YhvhAfToL+MsshZah/UV7aobi7iA3vW6xtfQDTGLLhQtPZl6TmJPqL0g+AZkcd0ArTjZVQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None
                self.type_dict = {0: 'GetArea', 1: 'GetLength'}

            def is_change(self, vaule):
                return self.dict_data if vaule == 'max' else {True: ['<=', '>'], False: ['<', '>=']}

            def choice(self, data_list):
                self.factor = 0 if all([isinstance(_, rg.Brep) for _ in data_list]) is True else 1
                if self.factor == 1:
                    data_list = [l.ToNurbsCurve() for l in data_list if type(l) == rg.Line]
                return data_list, self.type_dict[self.factor]

            def RunScript(self, Geometry, Specifylen, Close, Compare):
                Close = True if Close is None else False
                Compare = {True: ['>=', '<'], False: ['>', '<=']} if Compare is None else {True: ['<=', '>'], False: ['<', '>=']}
                compare_symbols = Compare[Close]
                if Geometry:
                    data_stream = Geometry if all([isinstance(_, (int, float)) for _ in Geometry]) is True else self.choice(Geometry)
                    try:
                        Result = eval('[r for r in data_stream[0] if r.{}() {} Specifylen]'.format(data_stream[1], compare_symbols[0]))
                        Excluded_Data = eval('[e for e in data_stream[0] if e.{}() {} Specifylen]'.format(data_stream[1], compare_symbols[1]))
                    except:
                        Result = eval('[r for r in Geometry if r {} Specifylen]'.format(compare_symbols[0]))
                        Excluded_Data = eval('[e for e in Geometry if e {} Specifylen]'.format(compare_symbols[1]))
                    return Result, Excluded_Data


        # 随机数据
        class RandomData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@随机数据", "RPP_RandomData", """随机数据组""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a0a41cb7-3dfc-4814-8328-557bd222883b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "原始数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Random", "R", "随机列表，可不填（自动随机）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "随机后的数据")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJiSURBVEhLzdXZq41RHIfxlTlTcUQUGUJ0ynFBZB4zJONxzgWlk0QuJGUumYfMiWSKQpkuRCnccS3+BVGEDJEQnmft/R5nn73f7XXOjW99aq93v+/a611r/dYO/0vaYTgWYhkWoApt0KxU4gI+4VfejwafP+AMhuCf0gIHYScvsQNj0BN98nyjdXgB79uDTOmIR/ChNWiJhtmA3piPpeiGFfD+B3A6U+PIH+MzHGG5DMRG3MZkDMY3PERqDsORDIutbOmFG1iCAfD5nSjKICTT0pTcwgisgv30RUEu4VXuY6a4Va9hYmyF0BVOV2u8xSnUx4X5iu2xFUJn7MJpHMMoNM5JrMRZ7IWbww0wB5vxEa0Q44L6WiNjK4ROcGT9MQX3MA/G6+fwDD28QJ5gLVyPA7AI7a++Pqrhhe6xVZwuuA5HfAcW4D440itYj/ZwJi7CgdnfbMTU4SecmrQsx3N0iK1c4R2BmyOJ29xNYiH6AzWIWQQvJK9cKq6JU5FkPI5jaGwVJvmBWbFF3PdeKLWYZjFcTI8Gzx6ncj9c1Mtwqly3JJNgfxZfTFt8we7Yyu2ImZgGd8hNVMA4VS7yUyRr5pttyX2MOYr3KDhmfMj96zw6GkflIVeLUnGfr8Z5OH2eScY68PR1+gqSlLk7Ikvm4irGxtafWEv244FYFKfDLy35pmQcfH5rbKXE0/A7RsdW9kyAnd+NrTKxWO7Dmzfl2+VigW2D91uErkGmuMA+9A6HMBWekNZKP0yHu8W/zb9OS1r8UzmBN7CTxl7DH/FoaFbczx5c1obn1gxYRG7pMgnhN2L3geQRRszFAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Data, Random):
                try:
                    if Data is None:
                        self.message2("请输入至少一个数据组！")
                    else:
                        if len(Random) == 0:
                            index_list = random.sample([index for index in range(len(Data))], len(Data))
                            Result = [Data[_] for _ in index_list]
                            return Result
                        else:
                            if len(Random) == 1 and Random[0] == -1:
                                Result = Data[::-1]
                                return Result
                            elif len(Random) == len(Data):
                                Result = [Data[_] for _ in Random]
                                return Result
                            else:
                                self.message3("随机列表的数量要与原始列表一致！请检查")
                                Result = Data
                                return Result
                finally:
                    self.Message = "随机数据"


        # 简化树形数据
        class Simplify_Data(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@简化树形数据", "RPP_Simplify_Data", """将所有传进来的树形结构简化至最简状态""", "Scavenger", "Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("813ad085-0bdf-44e4-9178-79e0549298aa")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_Tree", "DT", "树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Tree", "RT", "最简后的结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def handle_list_data(self, data):
                for single in data:
                    if isinstance(single, (list)) is True:
                        return list(chain(*data))
                return data

            def RunScript(self, Data_Tree):
                try:
                    is_judge = [list(_) for _ in Data_Tree.Branches]
                    if len(is_judge) != 0:
                        Data_Tree.SimplifyPaths()
                        origin_data = [list(_) for _ in Data_Tree.Branches]
                        path_list = [list(d.Indices) for d in Data_Tree.Paths]
                        minpath = set([_[0] for _ in path_list])
                        depest_list = []
                        for father_index in minpath:
                            sub_list = []
                            for index, _ in enumerate(path_list):
                                if _[0] == father_index:
                                    sub_list.append(origin_data[index])
                            depest_list.append(sub_list)
                        result = ght.list_to_tree(ghp.run(self.handle_list_data, depest_list))
                        result.SimplifyPaths()
                        return result
                    else:
                        self.message2("树形数据为空！")
                finally:
                    self.Message = 'Simplify'


    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Data_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "Niko_ZiYe"

    def get_Id(self):
        return System.Guid("7f63e08b-c8f3-46e8-942d-a324fbd50d90")
