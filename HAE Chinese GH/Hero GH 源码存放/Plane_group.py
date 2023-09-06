# -*- ecoding: utf-8 -*-
# @ModuleName: Plane_group
# @Author: invincible
# @Time: 2022/7/8 11:11

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
import scriptcontext as sc
import Rhino
import math
import re
import copy
from itertools import chain
import initialization

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:
        # 平面旋转
        class RotatePlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-平面坐标旋转", "RPP_RotatePlane", """平面旋转以及跟随平面旋转的两个物体，Direction（旋转的轴方向）""", "Scavenger", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("63f44167-e9c5-40e5-9040-9bb9cccbc6fe")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Rotated_Plane", "P", "原始平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "旋转的角度，不输入默认为0.5*pi")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(math.radians(90)))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Direction", "D", "旋转轴方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation1", "F1", "跟随旋转的几何物体之一")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation2", "F2", "跟随旋转的几何物体之二")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "New_Plane", "P", "旋转后平面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object1", "R1", "旋转后的几何物体之一")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object2", "R2", "旋转后的几何物体之二")
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
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                super(RotatePlane, self).__init__()
                self.selective_index = 'X'
                self.switch = None

            def get_new_plane(self, plane, f1, f2, angle, dire, point):
                vector = None
                if dire is None:
                    self.switch = 'off'
                    char_of_dir, is_bool = self.str_handing(self.selective_index)
                else:
                    self.switch = 'on'
                    char_of_dir, is_bool = self.str_handing(dire)
                if is_bool is True:
                    vector = eval('plane.{}Axis - plane.{}Axis'.format(char_of_dir[0], char_of_dir[1]))
                elif is_bool is False:
                    vector = eval('plane.{}Axis + plane.{}Axis'.format(char_of_dir[0], char_of_dir[1]))
                elif is_bool is None:
                    vector = eval('plane.{}Axis'.format(char_of_dir[0]))

                plane.Rotate(angle, vector)
                f1.Rotate(angle, vector, point) if f1 is not None else None
                f2.Rotate(angle, vector, point) if f2 is not None else None
                return plane, f1, f2

            def str_handing(self, str_char):
                if self.switch == 'off':
                    alphabet_list = str_char.split(" ")
                else:
                    alphabet_list = [char.upper() for char in str_char]
                if len(alphabet_list) >= 2:
                    if alphabet_list[0] > alphabet_list[1]:
                        return alphabet_list, True
                    else:
                        return alphabet_list, False
                return alphabet_list, None

            def RunScript(self, Rotated_Plane, Angle, Direction, Follow_rotation1, Follow_rotation2):
                try:
                    re_mes = Message.RE_MES([Rotated_Plane], ['Rotated_Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object]()
                    else:
                        center_point = Rotated_Plane.Origin
                        New_Plane, Rotated_object1, Rotated_object2 = self.get_new_plane(Rotated_Plane, Follow_rotation1,
                                                                                         Follow_rotation2, Angle, Direction,
                                                                                         center_point)
                        return New_Plane, Rotated_object1, Rotated_object2
                finally:
                    self.Message = '平面旋转'


        # 重构XY轴平面
        class Refactoring_Plane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-重构Plane", "RPP_Refactoring_Plane",
                                                                   """输入代替XY轴的轴向量来重构XY轴平面""", "Scavenger", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("25b06c92-fe12-466e-9ea9-615ee01fc527")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "原始的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "New_Axis", "A", "需要重构成XY轴的向量轴，输入的是原平面的轴向量名称")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Switch", "S", "是否翻转重构后的向量轴,t为翻转所有向量，t1，t2为翻转X轴向量和Y轴向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Symmetry_Plane", "P", "重构后的平面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Origin_Point", "O", "平面的中心点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_XAxis", "OX", "原平面的X轴向量")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_YAxis", "OY", "原平面的Y轴向量")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_ZAxis", "OZ", "原平面的Y轴向量")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "a", "NX", "新平面的X轴向量")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "b", "NY", "新平面的Y轴向量")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "c", "NZ", "新平面的Z轴向量")
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
                        self.marshal.SetOutput(result[6], DA, 6, True)
                        self.marshal.SetOutput(result[7], DA, 7, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAR9SURBVEhLnVVtTFtlFD6Igl8zmYsf8Yf//WFmMjXZGNucC21hlG6Ujba0DCiwjYAD2k1E0wCDMXrL2skUdIkzamI02w+jPzTBJW41EfyBzs0NJpvDEZxkTkmm20qOz3nvvdJCmYsnObn39rzvc57nnPO+pf+0taG7yXfwefLF/OSNdlBZtAfeBq+g8r5njFX/w5ydj5AvGiJvbJTKX2eq7GeqGsATrp749sUY8VN4BsgeXGLsvANz93rBepL8b7ECL+tl8kQWuvxe3oeEsu7geXKFCw2E25gnElbsBDgdqFtjKg0v/H0bElW8gaSRPQZSGnNpGvkPY9GBhQDiLgBv7eH7K1AaeZ8f90Z1Ne6egIGYZKWaS9V2UXAwL+rk/sHv+JerM7y0Goy39MzFVRnhkmTbIVG53kCGVUUeRnB68bJEOKN4H4eOfs1iF678wcv8WFvQrpdLwLd2YZ3xLgnc2hjVx7L1BG4tRP6304OLF3fz0y3vKnCxG4lZvgwVoY/jnC1xJ5Q4WpEwoJdOqiCl8mh+opqBe/BycVH24ijPA2D32bdnVYI/r//NV67NqPfhn6b40WowtgDcUs+U3ww1+/QxdmtDmJrwcxgxo4ZpwMVVCcJ8X1ErD5+7yInZWX6irI07j8VVkvjYJGdam5jyGpisLzHZGtEflMwbTchY1qrDkw5YXMBLu+Fg5Wjnpc4WzmkGofV1TDk7+fDxUypJZfRDfNfo4NZdeqLS/Syj2bUggcy6fS9TCRbIVBS+DPlgtzmEJ5iu2a4DrdvBy8o6+MatBA+PXmJ6AUkFXGLi9hYk8PRqKQkAnuU7wI3vHeflre+DdZshW1jJZiQwAcRzt/OJ0+OqbA85X2HaACJmrAjfGMG9KQmc3fxU8B0lewAzT7nzWM33nFo+Fv9erX/cA4UvotFmTE8QrlIdNxNs2c+P1fWrDYMjo0yra1MBk10SoxdnLk2pybrXHtQbbcbtKC3ujuXqVjSnSOoPFUPjU5xIJPhJHw4TykD580oj36tqeEVDryIjKlLIyLjaGm8ShUJ3QcU5dVmZKhyd7NCOqo2iInMDZMuEWNALYZ2H58pqXrKxmUfGL6t1q5pA0my+uLC3NX5lnORwc8pJFhWbuvjIyTNqc/zHC7waTDMtAMekZAEgb3cf//DzlIp3fzQ4N6Km48xApUtPUBJ6EM2e+FeFlGtzO2fYdvOhT04oELHJ6Ws8MjbBv/2un2Kxjg8+Z1q7Q1dlgst4WneNUElJpp5AzB22qftc5l5uRRfOgJzOHD+vgfwjX3zD5yen+erMdT478Su/+elJXlGHe8csnQlegEYXBGYx1s8ayEnmCu9Rl5QkMZsuo5YLEGkgSpRViDtH2Arwup1zwAocMWGf11BhIKYxTziorltxUSI346bXdJbiAi69SAYWF+CNwVs4lJUG0m3MpVnwn3xaqZGyyRgXGyc6+dDJKMq0iMqC4BAIrDQQ7sCs9dlUHqtBueJQcVP923mhxvGqDijA+U1/oSxfUn6gDDsy9I3JRvQPzTPPJGihTfIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None  # 是否反转平面的因素

            def get_new_plane(self, plane, str_data_list):
                """
                得到新的平面
                """
                X, Y, Z = plane.XAxis, plane.YAxis, plane.ZAxis
                if self.factor is False:
                    direction = [eval(axis) for axis in str_data_list]
                else:
                    letter = ''.join(re.findall(r'[A-Za-z]', self.factor)).upper()
                    if letter != 'T':
                        direction = [eval(axis) for axis in str_data_list]
                    else:
                        origin_direction = [eval(axis) for axis in str_data_list]
                        if len(self.factor) == 2:
                            num = re.findall("\d+", self.factor.upper())[0]
                            index = int(num) - 1
                            direction = copy.copy(origin_direction)
                            direction[index] = -1 * direction[index]
                        else:
                            direction = [-1 * sub for sub in origin_direction]
                return direction, X, Y, Z

            def str_handing(self, str_of_word):
                """
                字符串New_Axis的处理
                """
                str_of_word = str_of_word if str_of_word is not None else "XY"
                string_list = [map(str, re.split(r"[.。!！?？；;，,\s+]", w))[0].upper() for w in str_of_word.split()]
                if len(string_list) == 1:
                    string_list = [s for s in string_list[0]]
                    return string_list
                elif len(string_list) > 1:
                    return string_list

            def RunScript(self, Plane, New_Axis, Switch):
                try:
                    if Plane:
                        Axis_list = self.str_handing(New_Axis)
                        if Switch is None:
                            self.factor = False
                        else:
                            self.factor = Switch
                        Origin_Point = Plane.Origin
                        self.get_new_plane(Plane, Axis_list)
                        origin_redirect, Origin_XAxis, Origin_YAxis, Origin_ZAxis = self.get_new_plane(Plane, Axis_list)
                        Symmetry_Plane = rg.Plane(Origin_Point, origin_redirect[0], origin_redirect[1])
                        # 重构后的xyz轴向量
                        New_XAxis, New_YAxis, New_ZAxis = Symmetry_Plane.XAxis, Symmetry_Plane.YAxis, Symmetry_Plane.ZAxis
                        return Symmetry_Plane, Origin_Point, Origin_XAxis, Origin_YAxis, Origin_ZAxis, New_XAxis, New_YAxis, New_ZAxis
                    else:
                        pass
                finally:
                    self.Message = '重构Plane'


        # 偏移平面
        class OffsetPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-偏移平面", "RPP_OffsetPlane", """通过X、Y、Z端选项去偏移平面""", "Scavenger", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f4ab7050-c453-4eba-b276-c71fbbf73420")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移距离")
                distance = 10
                p.SetPersistentData(gk.Types.GH_Number(distance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_X", "X", "按X方向偏移")
                bool_x = False
                p.SetPersistentData(gk.Types.GH_Boolean(bool_x))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_Y", "Y", "按Y方向偏移")
                bool_y = False
                p.SetPersistentData(gk.Types.GH_Boolean(bool_y))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_Z", "Z", "按Z方向偏移")
                bool_z = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_z))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Offset", "O", "生成偏移平面")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOISURBVEhL7ZRfiFRVHMcnWTUsUEyoB7USfKioe869M7N/dBOMqJeIBMVKpIdY6tEHCREdl5X+YEEWPYSEZT7ElL4EMtu2ze78uTN3vP90Z9udiXZtqV1X2Fxn9s69M3Pv/PqdO0fbdVdUCALxCx/O+f3O78+5B+4v8L/LyoptdV38ztWJ5mYFFUxB9UaRgqA1xugvjb/I6xj2QDP6LlRRaLuri2fgAgUoSgB5tiJncP9xEOA4IwRwOgTuBapXDfFNuJNGtVywwzXpWb9wQQRQBfByTUAT4Oy5rVD6hkL1NAHnFIHaDwTg1+YlXJ0aVY3uiUQiy3i5pkCVVjmK+Jqr0TRM4K2uhAF+x5uym/82D7R/nNgOMIG3n0Cbcanp988nWW4ruCb5o6bRfXNK6DG/wdTPbWFLDX/o5IKfWynpfSsl9lip4CJsRJfbeso3+ZuwHLGnnBSPzqVCX9ha8Phssn2n3+C/lnOg81T5nc7t3Ly94vH4E4qi7BwYGNh1nWQyuSuTyeyIxWJreZiveCTSUune8v3f3Z2vctetNTg4+GQ2m/0UKQ8NDYFpmgtgPjybxEYH+/r6HuFpAevI1p65ox2Em4uFt9uESZ8hc/l8HnAF9C1JLpcDHjOFHIrF5LXuvg17nf2bNvNy/woTnsGgE4hXLBZB0zTAp7kj2BexnEw2e1WW5Q/wizbysv4br0ulUofT6fQwrpVEIjGDz3MZ17uC58zKcsbBRhdx/67foLe39yFVVTdOT0+/VSiME2z48HxOxuFBqQuWS1/C8i4O20eisCJ6UywjGo2ydV1/f//jfoPrsu1qt2XVwtxcILi6eg0Y8xhfvaZRDKzkx7cX+70tyz5WLtsvcFcAok+vwHn0tmfQIVcjpboilBqaUHJNoeRdJCVvhEx6I+JHVja8nqfcWvhJLbbjKjPVxu54JNBS08Qu1yAj/ghgg07HmTNMoPS1BM4BCaoRCeqH8OyrMBsNs3WDHqvkght4uaX157hBKsaL+z3jueEbhc8L0OCwwfdt6nmwYhS8nwi4vUg/NjYRnF2eQa7VdfJJJU0Xvn050/po7bz0nqs+NeYPsHEcZnmcpIzheaB9rrANYBRjRtFmjDT9PmzoTYaxEYW6Rk+UZfFZv8G1gdbNVTO428nRHXaCvmynxZdsZTF1ZEwJLXl2A8x1ZPpKVRffKCWkLX6D+7qXFQj8A01+NViTqfE/AAAAAElFTkSuQmCC"
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

            def Offset(self, Plane, distance, Axis):
                P = rg.Plane(Plane)
                Vec = rg.Vector3d.Multiply(Axis, distance)
                P.Translate(Vec)
                return P

            def RunScript(self, Plane, distance, X, Y, Z):
                try:
                    re_mes = Message.RE_MES([Plane], ['Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        Offset = []
                        if X or Y or Z:
                            if X:
                                Axis = Plane.XAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                            if Y:
                                Axis = Plane.YAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                            if Z:
                                Axis = Plane.ZAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                        else:
                            Offset.append(Plane)
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Offset
                finally:
                    self.Message = 'Offset Plane'


        # 构造工作平面
        class ConstructionPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-构造工作平面", "RPP_ConstructionPlane", """构造工作平面""", "Scavenger", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a7e30adb-dc28-418c-b318-555ade4dfa5a")

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
                self.SetUpParam(p, "Origin", "O", "平面原点")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "X-Axis", "X", "X轴方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Y-Axis", "Y", "Y轴方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Z-Axis", "Z", "Z轴方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "平面")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMfSURBVEhLvZRrSFNhGMcXXYwKoisFoa3S3Kam2MYWhQ26QijlpaAg0VNBlln2IYqgsj74peiGZkZENyhKorxitTlnllFaQpB9CU0F8doHNef59393jjnTrRXVD368z3vgPP9znhdezf9kK72glBqJ3lTKv4eWNtB82kjXUV/Mo2XUoa6V9Dr1yQYKmu3e+WYSNdEoGk/FeweoVyJoMxXNxRpH/WEiFX9+zL3zwRF6Rik126j45XHunXdm0jp6173TaKZSEegXk9XVFylUjKaGiqB6mkW902S1Lv0cYF2sbn+FOAdx2EF0obrOoN7pCLGkNWdYHj6TI1Lt/eHSaCOlSjlUsrsMqS3yWjGS36Nrvvlaf9YK1GIZ3iOSitWzDsYHmPAWZtj6FgWrr/kHEhMntRuMjd2rzXB+jYADYagcFIajEktRhSA4XyfBlnUe9o5olwOBi9RX/eOTxTK3VW+sbY0zwdnEANmgBMg6ONssqLiUhZLIN3j6YC+fBbkcveG/FyDonrhiR9M9E2xQm1Mnv/zp5eMoXtiAoh13UOXS87nOn4AJ6jpMzxSz9OWWCfahADGaAQPKD+XhsbUU5YXJqIYWjoEwzwAjvaSUP5hNq5TSgxEB0HHuwXiWmY+Sk9mwdYXD8S0CL3g2PwWIZp00yb1TyKGFSunBcIBoroXt9DkU78/lgS/hqEIYamAAg0YGCDbRDjqezqVdVFygI3EH3DaiAoGw55xA0c5bqOjjIXNUQ2fiJUDwhJ6lV6i4lUfTE2CWmgt1eF56EEUJD2DvjGTzYDZmUzZ/BT3eiPGNHSBG1U3F188SD0bRq9VK7SlpsCU/Qk2LSa6TtXKtrKc6uV4Ole/3LkfBgBGvBg0uYMxr4RQduvxG0xATta/g8GnsepeC9K+rkN62ga53m9m2DtaGWBg+xiOpOw7WT5svmuq2L1BfHWIPzVXKMbiYtjFkdc3a1ID3a6TpZQnS9PJhp5UnpIZWxzrD6jd/CareclX/Mi45+vkmMRZP0mmeUv4BK4sS5sTcS5ymbscig4pD/mccpTeU8t8QS3crpUbzHdgixmO91slmAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.origin = rg.Point3d(0, 0, 0)

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

            def get_x_y_vector(self, vector, z_vector):  # 根据z轴和xy其中一个向量求另外一个向量
                # 确保向量是单位向量
                vector.Unitize()
                z_vector.Unitize()

                # 获取 另外 向量（通过 两个向量 的叉积获得）
                other_vector = rg.Vector3d.CrossProduct(z_vector, vector)
                other_vector.Unitize()

                return other_vector

            def get_one_AXis(self, one_Axis):
                # 根据一个向量构建平面
                return rg.Plane(self.origin, one_Axis)

            def get_two_Axis(self, one_Axis, other_Axis):
                # 根据两个向量构建平面
                return rg.Plane(self.origin, one_Axis, other_Axis)

            def Construct_plane(self, x, y, z):
                # 根据三个向量构建工作平面
                plane = rg.Plane(self.origin, x, y)
                plane.ZAxis = z
                return plane

            def Judge_Vector_Plane(self, x, y, z):
                Axis_List = [x, y, z]
                res = list(filter(None, Axis_List))
                if len(res) == 1:
                    if Axis_List[0] != None:
                        # x轴
                        y_vector = rg.Vector3d(0, 1, 0)
                        plane = self.get_two_Axis(x, y_vector)
                    elif Axis_List[1] != None:
                        # y轴
                        x_vector = rg.Vector3d(1, 0, 0)
                        plane = self.get_two_Axis(x_vector, y)
                    else:
                        # z轴
                        plane = self.get_one_AXis(Axis_List[2])
                elif len(res) == 2:
                    if x != None and y != None:
                        plane = self.get_two_Axis(x, y)

                    if x != None and z != None:
                        y_vector = self.get_x_y_vector(x, z)
                        plane = self.get_two_Axis(x, y_vector)

                    if y != None and z != None:
                        x_vector = self.get_x_y_vector(z, y)
                        plane = self.get_two_Axis(x_vector, y)

                else:
                    plane = self.get_two_Axis(x, y)
                return plane

            def RunScript(self, origin, x, y, z):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    plane = gd[object]()
                    self.origin = origin if origin else self.origin
                    if x == None and y == None and z == None:
                        plane = rg.Plane.WorldXY
                        Message.message2(self, "你不给轴，我就输出XY平面喽!")
                        plane.Origin = self.origin
                        return plane
                    else:
                        plane = self.Judge_Vector_Plane(x, y, z)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return plane
                finally:
                    self.Message = '构建工作平面'

    else:
        pass
except:
    pass

import GhPython
import System
