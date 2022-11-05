# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/11/5 16:37

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
from System.Windows.Forms import ToolStripSeparator
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
import time
import getpass
import base64
import socket
import re
import copy
import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 平面旋转
        class RotatePlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@平面坐标旋转", "HAE_RotatePlane", """Plane rotation and two objects rotating with the plane, Direction""", "Hero", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("63f44167-e9c5-40e5-9040-9bb9cccbc6fe")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Rotated_Plane", "P", "Original plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "Rotation angle, default to 0.5 * pi if not entered")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Direction", "D", "Rotation axis direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation1", "F1", "One of the geometric objects following the rotation")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation2", "F2", "The second geometric object following rotation")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "New_Plane", "P", "Rotate back plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object1", "R1", "One of the geometric objects after rotation")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object2", "R2", "The second geometric object after rotation")
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
                if Rotated_Plane:
                    Angle = math.radians(90) if Angle is None else float(Angle)
                    center_point = Rotated_Plane.Origin
                    New_Plane, Rotated_object1, Rotated_object2 = self.get_new_plane(Rotated_Plane, Follow_rotation1,
                                                                                     Follow_rotation2, Angle, Direction,
                                                                                     center_point)
                    return New_Plane, Rotated_object1, Rotated_object2


        # 重构XY轴平面
        class Refactoring_Plane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@重构Plane", "HAE_Refactoring_Plane",
                                                                   """Input axial quantity instead of XY axis to reconstruct XY axis plane""", "Hero", "Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("25b06c92-fe12-466e-9ea9-615ee01fc527")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Original plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "New_Axis", "A", "The vector axis of XY axis needs to be reconstructed. The input is the axis vector name of the original plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Switch", "S", "Whether to flip the reconstructed vector axis, t is to flip all vectors, t1 and t2 are to flip the X axis vector and Y axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Symmetry_Plane", "P", "Reconstructed plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Origin_Point", "O", "Center point of the plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_XAxis", "OX", "X axis vector of the original plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_YAxis", "OY", "Y axis vector of the original plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_ZAxis", "OZ", "Z-axis vector of the original plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "a", "NX", "X axis vector of the new plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "b", "NY", "Y axis vector of the new plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "c", "NZ", "Z axis vector of the new plane")
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

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Plane_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("b116b1a2-c43b-4da1-b465-0db11dc9104d")
