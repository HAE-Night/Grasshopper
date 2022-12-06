# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/11/5 16:37

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from functools import reduce
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Line_group
from itertools import chain
import ghpythonlib.components as ghbc
import math

Result = Line_group.decryption()

try:
    if Result is True:
        # 扫出曲面
        class SweepOutFitting(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲线扫出", "HAE_SweepOutFitting", """Solve the problem of scanning out the original plug-in""",
                                                                   "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9eba4ae2-0e33-47e3-a47e-14f375581a62")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Sweep_Curve", "S", "Curve as rail")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Shape_Curve", "C", "Model curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "A new Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFpSURBVEhLxdPNK0RRGMfxKwtTY2rC7GQsRErDMMaMhhqS8pLXHQv/ABZ2FjRIrJRBJtmwlZgsTCJixVLeyj8gCxuG1T2+xz0z2d8z/OrTPedZ3KfzdI7xX8lT35zEjSus/uw0pxjn6MEWtqEtJTjBIKqwgifEoSUpTFhLowIRLOIRWprIsRw73OXeWSEcVsnwIwZtJ+nMd3lua+JvL4FDU45KZhzLeICWJtHC6o4v3+aHCOyZQ+wLEIRsom1cIWdl9N2XSItQyuxVtSbkvMkk5qC3SW0iOy6ZzLjuofckjQfmgKq1Yh36mzSfml3sXRjFPHSP61MEj8w+VQtjAfpPEtjPvpNhrOEOepsEk6KfvQdtWII8iWxmO2pcaRE+M7szNcgr/Ax5AWzHOgkvPnIpGlRtCnWYgWxmOy2OUv9r2dh0vdo71XcEO9bSftpxgSJEkcQuvNAW+TZucA2tP/4d+co3rOWfxTC+AfdYgpKmKc1DAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Sweep_Curve, Shape_Curve):
                if Sweep_Curve is not None and Shape_Curve is not None:
                    Brep = rg.Brep.CreateFromSweep(Sweep_Curve, Shape_Curve, 1, 1.0)
                    return Brep
                elif Sweep_Curve is None:
                    return 'The track line cannot be empty!'
                elif Shape_Curve is None:
                    return 'The curve cannot be empty!'


        # Surface面积排序
        class Brep_Arae(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@根据面积排序", "HAE_Brep_Arae", """Sort according to the area of the face, from small to large""",
                                                                   "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f078e5e4-1f07-452f-a4d8-64babb1a4b9b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Faces", "F", "Faces to be sorted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Faces", "F", "Sorted Faces")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Area_Arc", "A", "Sorted Area")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANpSURBVEhLrZXdS5NRHMeHd6UZ1h8giAhS6TLfoJnhEsMrpQs1vJREvfRKTcWbKdWglXgjoqJ0K0GEVhAzl7UcMsu9uT2bL3PsBXTLTff2fDvnbE86N71wnvHl2Y/nPN/P77z8zhHNL2oe6y07I99Xfl+6qK9IvfpHwQNwu92XLp4Yi36trstoYDQaoNfpoEtTggf1o77/ATqDCZxtG9bNHXBpSPheT/zcblcM4HK5YDJziESj4ImiaYpOjYXbhNPpTAQEQyGEiUJpKhyOwMzZTgE2OBwFgwgRBc+QkGGqdycVCoUJwArXacDh4RHZT7HGk3EeHR3HtNG1cjgcJMNwSmNBqQFmK/twamoKw8PD4DiOxSqVCjKZDAsLC+jt7UVfXx/8fj+bCppAKgWDoWTAhsXGsiwoKIBIJMLY2BiLW1paWNzW1oaZmRn09PRgb2/vAgAyArr6FRXlzLCjo4MBSktLWdzZ2YnJyUk0Nzdj125n76LRSJKEXbhhIQBXCkBZWRmys7NRU1OD/f195ObmIjMzkwEMBgOWl5fh/evH1s4u7A4ndk6Ixtt2B5yePTYjCQC6BtEoj+LiYlRXV6OoqAhzc3PIz8+HWCxGa2sry5q2j58XcefeA9wtr0JJRXWCbokr8OTpM1ZsHqGSBUAkEkVhYSHa29uZaWNjI6RSKerq6thaCO3L1yVczbrBpi6VSisfwra9mxpAMx4aGkJtbS0yMjLQ3d2NhoYGNDU1xe0pQIWs7LMBlZJHiQB3HEArMC8vD3K5HF1dXazz9PR0CsASrl2/mWQsKAaww+NJANCjIoycnBy270dHR1lntVoNiUSC+vr6uD1PAN/OB9yXwrp1CmA0WUgBBTAwMID5+XlotVo2Co/HA4VCgfHxcValFPD+wydidCXJWNDtkqpkgMFoJgW0z3KkRoFAgP33+XzsSY8Oum0PDwPQaHWQvXiNkVdvMCJ/m6DhlwpMv5sjhbZ1fFxTgD4OoCbniVZxgBwV5zWe/IwmM6mDOMDr88JApujg4IBk7oeXGHm93ouLjNq4YYkBNFq9bG1tDet6E9QaLX6oV7BJtpjFun1hmYmoH7syVT9XZf39/VAqlXhOnoODg7CTs4bdsXr9xXTyTlYuqRXUnB7PExMTmJ2dZfNMdw/tkI54nsc/OdtNDSsgkJoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def SurArea(self, x):
                return rs.SurfaceArea(x)[0]

            def RunScript(self, x, y):
                try:
                    Area = ghp.run(self.SurArea, x)
                    zipsur = dict(sorted(zip(x, Area)))
                    return zipsur.keys(), zipsur.values()
                except Exception, e:
                    self.message2(str(e))
                finally:
                    self.Message = "HAE-Sur-Area"



        # 计算Surface面积
        class Surface_Area2(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@面积取值", "HAE_Surface_Area2",
                                                                   """Breps Calculate Area: divide the area by the divisor, and retain decimals;""", "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9ee46870-e5b6-4d61-a7af-0ffef80f46e1")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Breps", "B", "Brep/Surface Object List")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Divisor", "D1", "Divider, default 1000000")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Decimals", "D2", "Decimal digits reserved, three digits by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Area", "A", "the measure of area")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQ7SURBVEhLrZVLTFtHFIbNo1kUUCOKBAuisAmbUqUrJNYIVFKBhISQsmhaQGpaIECJAilFpUgNsKECqiQEFpVCbIyBNq3aFVKzSFzaAAaMX9cYXz9wBRiXh7F9sbH/nhlTYxLSR8hIv+7c0Z3/mzkz51zZgkl8d9m+1jOrFV65mK/MYLb3h8MRbGy4X7mYr8xotnWxF0EQYDQaYTAYYDyF+HzyYX7MNwYwmgRYRCdEhwui/RSi+cyH+cUBNmAwmeGT9gFEaGvhlxabz3yYH/MlgDUG2PMH6IOjFgwGueJb9D0SfTmpEWTX5z8E8B1EAUZhGdu7Xh47nU4Ht9sdA7hcLj5msVgg7QdhFl1Ytjp4KOIlrDixtb0HHy30OYDFaoPD6UJGRgYSEhJQV1d3uCSguLiYj71z8SKCoQP8PKXGfcUEFGPfxaSa/BFf3Poacwt6HBxE4gCmI4DdsYqzZ9+ATCZDfn4+N/d6vcjMzORjeW/lYT8Ygvr3eXw7Mor7D+QkBZd8VIVPrl3H/KIWoVAYBuMLAG+mpyMpKQnp9PT5fDw0zDw5ORlv50UBT37T4IF8FKMKOUnBpRpT4dqnLQRYOg7QxwFsDifS0tKQR0YsJHq9HhMTE9w8NzcXuRcu8DNggBECKAigIHOmMQ5ohWZBS+d2cDJAtDtx5sxrqKysREpKCuRyOdra2pCTk4OioiLknD+PAF3Bx9NzUChVZKo8BmggwNz8Ivb3QwQ4zINnAQkJMjQ1NfFd1NTUoLCwEGVlZaioqMC5c9kcMD2zgDt372Fo6B4mJye5Hj784d8BVpuDx7ujowPV1dXIyspCamoquru7cfnyZWRnZ8MfkPBUo8P7Vz5EY2MDent70dzcjNbWm6hvugHNvBaSFPxnQGdnJwYHB3mfaWpqiu8gHnDlgyp8fPUqqqqqUFJSgkuX3uOHfALAEgWsEEC0c8P29nao1WreT0xMhMPhQGlpKQewJGIhujs4hIGBPnwzMID+/j7cuX0bdQ3XMatZQCBApeJZwMqKiGWLlZvW1tbC4/HwPgtRJBJBQUEBHfzr2KMy8CvlwYhinO7+GL//CuU4xsa/R31jC2ZmNfD7pTiAMQoQzBY4V//g5kqlkpcIFtuenh7e7+vroxv1GQeMqH5CS1snPu/4inSLq/3LLnxUfwNP57SUP1SL/gYscYAbOhrY9Gzx7A2FQtje3uZ91o71d3YwvyRQKLRUFnRxWsIslYm19U14/tx6HqBnA24PdsiAGb5YWxQCH6RAgGLtPyaJ5PXuYn1jM+rHAIt6c9cu1RsThYjtQJIkqognGf83sQWu00JjAKtjreuXR4/w+IkaM7RtdmBW2yqEZfHlZBFhEKxHIWJ/NHaQLN2Hh4dRXl5O19IOk8lEMv5/0f+YzY39k3WmlX693kA5IGJ6epqK2yRsNju/puyD0ygcjuAvEHdPWuUdFWYAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Breps, Divisor, Decimals):
                # 初始化参数
                divisor = Divisor if Divisor else 1000000
                digit = ".%uF" % Decimals if Decimals else ".3F"

                # 计算
                Area = [format(rs.SurfaceArea(i)[0] / divisor, digit) for i in Breps]
                return Area


        # Surface中心面
        class Surface_PLA(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@面_Plane", "HAE_Surface_PLA",
                                                                   """The plane is generated according to the point order of the face, and the index subscript sequence determines the direction of the plane""", "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e595f6f2-245f-452b-b117-2ff864c578dd")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "Parameters Brep, Surface.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Indexs", "I", "Default point sequence of reference generated by Plane: [0,1,0,3] Note: every two points are a group of vectors, and the first point is the end point of two-point vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "PLA", "P", "Generate Plane")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANJSURBVEhLvZVJT1NRFMdZEvgMbFgRVnwJEr4AKzVRogkuKImEsczVytalxoCKtBTaMnRQZLQ1dIYyFNrKkEaNhGihdB7g7z23vNqHhQUQb/JPX17/9/zOucN5RWVlZV9KSkpwUZWVlX6FQjFwE+n1+oEiClZdXY2ampqcqqqqUFpaCma4kcxmMziAgpaXl4MG/RYXF/MqBofeXE+DQ3g3PAyDwfAXkD8EwOb2zrW05dvDp3kTJiYnr67gJmN1zQO1Wp0F0JpTUEH0jvYglUpxJRJJBI9PCur30QlOwtGcl0TDubIGjUaDooqKCj8FvKja2lokk0lu3g98R69MDtmz53gqHxBJ2tULlXqK+8gvzHG4zgFK5Yhco9HC69/lfwimfPPufgBt7R2QSqXo6uwUqanpCd4rVNyXP0cM0J4Dzs7YciREoncEkHZ2obu7Gz09PSK1tLRAMTrGg+bmsOFwuf8zYNu3g7PTU8TjcZHo3c7e5YBWBhhRZgG5OSwpu7MA4DQPQM9kpPHtxwF6evtYwN7rA7a8X5HJZBCLxbgcDgeWlpZgsVgwOqbG/Qd1aG5uRl8fgf4FUC7CXErO7lwtDKAMgsEg1tfX4fV6cXDwE8YPM2iQNKKxUYL+/v4CABXPOh9gcxQApNNpbgiFQpidneW9xGT6jJevXuPO3XuQSBogkxUGUNBoNMpFiV4ATMCz7ee3kAxUgdPphMvlwu7uDtTaKdQ9fIT6+sdo75CipbUtJwmrbPDtCAdEIhGudDrFACtiwOaWj18SMhDAZrPBarViY2MDH2dmMTyiwsS0ASusx9jYBgpatrn4AYnFogiHw1ypVBJWewFAIhHnBgLMzc3BaDRiYWEBOp0OZpMJfp+PnxbKUFCGLSvNC4VYTzrJKsnugtXuEgM2PF62wTFuODw85Evkdrvh9/tht9vh8Xj4xtMhoD26SuSxsMqoBXGAlgHWN7d5mYKJlmd+fh6Li4u8GqokEAjwJTw+Pr5SdFAsNqcYIFQgAKjsbPNKIHXexCKRMEIsgOC5TLkK2OnMAVxuD4JHIRwc/rqxguwbYV62Q5sFKOV6vQ5K1ThU49pbk5I1QIpLgBf09dfppjE9PXVronhmsxl/AIqlHEPE5LaXAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Point(self, pts):  # 获取所有点坐标信息
                for i in pts:
                    yield i.Location

            def Count(self, num1, num2):  # reduce调用+方法
                return num1 + num2

            def Vector(self, PTS, Index):
                return [PTS[i] for i in Index]

            def RunScript(self, Surface, Indexs):
                if Surface:
                    pts = Surface.Vertices  # 取顶点
                    pt = self.Point(pts)  # 惰性取值
                    Pt1, Pt2, Pt3, Pt4 = next(pt), next(pt), next(pt), next(pt)

                    Cx = reduce(self.Count, [Pt1[0], Pt2[0], Pt3[0], Pt4[0]]) / 4
                    Cy = reduce(self.Count, [Pt1[1], Pt2[1], Pt3[1], Pt4[1]]) / 4
                    Cz = reduce(self.Count, [Pt1[2], Pt2[2], Pt3[2], Pt4[2]]) / 4
                    Center_PT = rg.Point3d(Cx, Cy, Cz)

                    PTS = [Pt1, Pt2, Pt3, Pt4]
                    if Indexs:
                        pt = self.Vector(PTS, Indexs)
                    else:
                        pt = self.Vector(PTS, [0, 1, 0, 3])
                    PLA = rg.Plane(Center_PT, pt[1] - pt[0], pt[3] - pt[2])
                    # return outputs if you have them; here I try it for you:
                    return PLA


        # 曲面偏移
        class ZiYe(object):
            def Move(self, Obj, Vec):  # 移动
                Objcets = []
                for i in range(len(Obj)):
                    Objcets.append(rs.CopyObject(Obj[i], Vec[i]))
                return Objcets

            def CSurface1(self, Brep, Line, Vector):  # 生成偏移曲面1
                Suface = []
                if len(Vector) == 1:
                    for i in range(len(Line)):
                        Suface.append(rg.Surface.CreateExtrusion(Line[i], Vector[0]))
                else:
                    for i in range(len(Line)):
                        Suface.append(rg.Surface.CreateExtrusion(Line[i], Vector[i]))

                for i in Suface:
                    Brep.Join(i.ToBrep(), 0.02, True)
                return Brep

            def CSurface4(self, Brep, Line, Vector, Distance):  # 生成偏移曲面2
                Suface = []
                for i in range(len(Line)):
                    Suface.append((rg.Surface.CreateExtrusion(Line[i], Vector[i])).ToBrep())
                Suface.append(Brep)

                brep = []
                for sf in Suface:
                    brep.append(rg.Brep.CreateOffsetBrep(sf, Distance, True, True, 0.02)[0])
                Breps = [i[0] for i in brep]
                Brep = rg.Brep.CreateBooleanUnion(Breps, 0.02, True)[0]
                return Brep


        class ZYBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@偏移曲面", "HAE_BrepOff", """Generate offset surfaces from polylines.""", "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ee58788c-4219-47bd-8935-e981aedf11a6")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Offset direction of each segment")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Offset distance")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "Brep after offset")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOrSURBVEhLrZVdbFNlGMdrNOhwQHRmusIkjLDqIlGJkWsTboBLbk28MMELv4goX0qIFwbjpVwQDOvHaTnlewvdN+go9Wzrx7q1sLXbuinxA0Lmuq4fO6c97d/neU3LulW2LHuT/8U5fZ7/73mf93lPDWdtrn3SpfYfzjbLay72Ndgv3jhz544HbW1tay72ZcD3LlcbnE4nJEmC2WyBxbJ6cb7dLgk/9i0B7HY7OnpuwzsYxoB/eNXifFfnLeFXBmg2mzESncRarGBolHZiLgeYaXuhe1ERkM1mKyqXy5V+z7H0PB4+mim9Y/Hy0S64XWUAi8VaAmiatkT5fJ4MNMQmp0QMr2++PY1XjK/i3HmbeOY4Xr7B0MoBqqqKd6lkAoryK660duG24oenP4AdpiY8/ZQBH338uYhZFjB8N0I/F4Qpq5gQi8Vwo70bwdE/0NLRC+OWragzboaxrg61tbU4fPRrEVcsxhtYKUCdh9/vx3lHK845b+L0jxKapctkbkR9/RaYTCYB+OKrE8J4eUA4gkIhj/n5eTrQLB48fISfPQGM/5XG/gMfwGAwYFNNHUyvNZF5IxobG8sAnFcoFDAQGK4MGAqP0mHqyGQyKNChRsan8P6Hn+LgJ0dQtX6DAFRvfAmvN+0k8x1LAJzHw8D3YVkAlYKx2G/CdKE2vvAyAd4QO2hoaED18+tx6PCxFQJCI9D1HNLptNhBdGIKz1ZVVwRsb9iGN9/ahff27MWXx0+J1nCeruvo9w9VBgQJkNOzSKVSyNMl4hYtBlRvqoVxcz1qal7E5ZYOjN2fRm9/WFTPeXwZ+30MsBYBrSXA4PA9cZmSySR0CoyMTS4B7Hz7XRw7+R0OfnYC3X1ROK71iEnjCWIA5/f5gv8P0Chwbm6OPgUaRqOxJYBd7+zGgxkVXUoEVvk6hoIBZKg1XBTnaZqKPm8lgNWKAAFUGrVEIiEAd0fG8cy6KmG8bbsJJ+nTcOjIKSi+EH4yy5iYmBDjzMacw1Lp7ijeQeEnALaFgGAYKvVydnaWQBlM/f4n1j3333hK8lUxKZP3/0ZnVzfiM9OiLRy7UJyvDDwBwIdVDOap6Oz5BWabjHh8lipN4J/paVEptyQej5eZszhfGQgsAMjlLdI02jL3U/Q0KarmlUqlxXOSDjKZTD2OWSTOV7w0RYsBDocD11rb0X3LTVX3rlqcf7XFhQvkVwZwyjIc9Ddns1kh2WyrFuc7HHbI5FcEnHG7PeJhreV2e/AvvVnnqkBHQSwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Brep, Vector, Distance):
                Ziye = ZiYe()
                if not Distance:
                    Distance = 3

                if Brep:
                    Linelist = [cr.EdgeCurve for cr in Brep.Edges]

                    if Vector:
                        if len(Vector) == 1:
                            DaM = Ziye.CSurface1(Brep, Linelist, Vector)
                            Brep = rg.Brep.CreateOffsetBrep(DaM, Distance, True, True, 0.2)[0][0]
                        elif len(Vector) > 1:
                            Brep = Ziye.CSurface4(Brep, Linelist, Vector, Distance)
                    else:
                        Brep = rg.Brep.CreateOffsetBrep(Brep, Distance, True, True, 0.02)[0][0]
                    Brep.MergeCoplanarFaces(0.02, True)
                    return Brep


        # 曲面挤出（曲线修剪）
        class Curve_Trim_Offset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲面挤出（修剪、移动）", "HAE_Curve_Trim_Offset",
                                                                   """Trim the curve, select the extrusion amount and extrude the surface. If the extrusion amount is not input, output the trimmed line segment""", "Hero",
                                                                   "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6ebbbf0d-5bf7-4833-a961-e0f80e578884")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve to trim")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "Type of extrusion, {0: Line, 1: Arc, 2: Smooth}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "Length of curve starting point extension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "Length of curve end extension")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Extrusion", "V", "As a reference for extrusion (can be a vector or a curve)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Move", "M", "Vector of moving object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Objects", "O", "Processed object (surface or curve)")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                result = self.RunScript(p0, p1, p2, p3, p4, p5)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALXSURBVEhLhZZZyI5BFMfHGsIXolxQyBbKEkVukIhIuVG2Qh+iKMsF5UIK2V3Yk6yFuMGd7UoR2S6QZLkgIVH27fd7vpnPyzsP//r1zpk5z3lmzsyZ5w0ZtYQVsBkW2IEWwjboU1ghzIMtMLSwQlgEi+uaoRbWw1roYEelOsN1+AkvYAAciPYxaAgbo30JmsIm0Hcw7AHHxEk0hnr1hmfg4HloDnuj7ezVBtA+WVghrIFH0A7sc+w5pJXVy2D3QIcjdqA0c1Oh0sxT8JWgXQNbY/sudIUqTQMdLhdWCIdA231QpqEy+HLQXgetYvsVdISs9oFOo2FCbBtU+RLtE4X1O/hFMMdTor0bSnUQdBoOc2A/KNNj//HCCmEZpOBJ+tuXVpuVx0wnT4pqBNshF/xCYdU9sxq6gf0P4Y9TUynP61vQcS6YS9unQS2FyuDTQdvTpuzXdjIN7MjJ3H8HHUdEVAqe0pKC3wQ3eBD0gidgv6sq1XzQ6Uph1VVnLvgtMB1jou0kusAn+AjtISsr9SV8A6v0BljZKgW/DQYfG22LszuoM2CfY6V6DDq5L7PBDf87eJq5wa3iftAMPH32T4KsvE9+gPl0BWom+NAdaAKVwduAteNhcCJPwbGeUKVO8AB08EiqdMZzwduCdXMffPYoOHYOquTD10CHs3agWVAW3LQMga/g3bMKHDO9vqxKk0EHN1WltHh55YL3j/ZhcNy0voMekNUu8AE3Z2BsG9x9yAX/AgZ0thPBcW/fUqXb02Wbd5f6r+DvweJSVr4+fitKlW7IHdACvCrGxb5ccFPRF2bEX/1ccalcqhWoo/uhbPt1ygXX/wN4nNVV0N9Ul8rZ6CRTYTyYBvfkM1QG9+Pixo6C1uCfgTfgszuhVP4jSC/x8lMeRVfndZCCOz4M/AfifvktsLhew39fkopLloBH1mDemum2HQlebimgG21VewOnCZwKIdT8AoEY9NDOJjWiAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._curve_style = None
                self.dict_factor = {'-': ['Trim', None], '+': ['Extend', 'rg.CurveExtensionStyle.{}']}
                self.curve_of_type_list = [rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.ArcCurve]

            def parameter_handling(self, par):
                par_factor = self.dict_factor[par[0]]
                line_length = par[1]
                type_of_line = par_factor[1].format(self._curve_style) if par_factor[1] is not None else None
                return par_factor, line_length, type_of_line

            def processing_curve(self, first_cutting_line, first_data, second_data):
                first_factor, first_line_length, first_type_of_line = self.parameter_handling(first_data)

                second_factor, second_line_length, second_type_of_line = self.parameter_handling(second_data)
                after_shear = eval('first_cutting_line.{}(rg.CurveEnd.Start,first_line_length)'.format(first_factor[0])) if first_type_of_line is None else eval(
                    'first_cutting_line.{}(rg.CurveEnd.Start,first_line_length,{})'.format(first_factor[0], first_type_of_line))
                result_line = eval('after_shear.{}(rg.CurveEnd.End,second_line_length)'.format(second_factor[0])) if second_type_of_line is None else eval(
                    'after_shear.{}(rg.CurveEnd.End,second_line_length,{})'.format(second_factor[0], second_type_of_line))
                return result_line

            def create_extrude(self, will_ex_curve, ex_data):
                ex_brep = None
                if type(ex_data) is rg.Vector3d:
                    ex_brep = rg.Surface.CreateExtrusion(will_ex_curve, ex_data)
                elif type(ex_data) in self.curve_of_type_list:
                    ex_brep = rg.SumSurface.Create(will_ex_curve, ex_data)
                return ex_brep

            def str_handle(self, str_data):
                if str_data is not None:
                    symbol = '+' if str_data[0].isdigit() is True else '-'
                    num = abs(float(str_data))
                else:
                    symbol = '+'
                    num = 0
                return symbol, num

            def init_movement(self, object, moving_vector):
                object.Translate(moving_vector[0], moving_vector[1], moving_vector[2])
                return object

            def RunScript(self, Curve, Type, Start, End, Extrusion, Move):
                if Curve:
                    _style = {'0': 'Line', '1': 'Arc', '2': 'Smooth'}
                    self._curve_style = _style[Type] if Type is not None else _style['0']
                    first = self.str_handle(Start)
                    second = self.str_handle(End)
                    curve_of_handle = self.processing_curve(Curve, first, second)

                    Extrusion_Surface = curve_of_handle if Extrusion is None else self.create_extrude(curve_of_handle, Extrusion)
                    Objects = Extrusion_Surface if Move is None else self.init_movement(Extrusion_Surface, Move)
                    return Objects


        # 两曲面间夹角
        class SurfaceAngle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Sur_Angle", "Sur_Angle", """Find the included angle and complementary angle of two faces""", "Hero", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("76f16ac2-4647-423f-ba46-202356f4b55f")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "x", "G1", "The x script variable")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "y", "G2", "Script input Geo2.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "angle", "A1", "Script output angle.")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "a", "A2", "Script output angle2.")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAlwSFlzAAASdAAAEnQB3mYfeAAAAgBJREFUSEvtk81rE0EYh+NRtHiohiSEEArFEMVIQIIIEa9682S1KmqhsWJ253t2Jp3dfFmbVgQVK+pBBC9evHjx4qWgFw/SP0HBP6GIB19nCRvSoDQ28WQH5jLMPM/M730nFtsd/2cC1cWVE8S/d2F25fO+f5IAFv71dqMFjMkvVDcfLqjO8bGKsAxmjKdAMwp3m01wMX8VCQqFQjadTu8dSRgJOELgKwWMiCcRMJPJrMXj8ZNjExjPg7kbc+8mk8lcPp/fn0ql3icSicpIAuo1Lhp78+gFt285zw8lk6dKpdLZXC53ulgsnhlJwHTzklG6J6CYr4XAcrl8fhBMOy+O6fpqx2W+Glo6KEAOeRYePjI9XYhNHp4Q999kmVl2mDTrgklYbrUAO/jljgUEsQfi9acDV+arTmXB/SCF2vS1hkXBQeJuI2BMeo2wrYjW2rNRRJJg26byK6XyW00qqHEGnl0L6xPNvxZ0I+oWmdlp4aAo2QLtFwThC1zydNubRxv6/0EIQoj9Fu4RAsaTcKfeAAfxR0MLiAwu13WtB+0XSIxt9sLmbruMsE3KvLdVHlydwasHhxa4qnVOSf09hIQwgrnNnkNgC8sJ/WkjW3eZcebFUnZo6ODGa3JpykKQhX0kTP2ghG8gpk2FtI/uGPqngzf9x1MxgD1jB+8CwwR+AeeNNMG0JN5RAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Point(self, pts):  # 获取所有点坐标信息
                for i in pts:
                    yield i.Location

            def Count(self, num1, num2):  # reduce调用+方法
                return num1 + num2

            def CP(self, PTS):
                Pt1, Pt2, Pt3, Pt4 = next(PTS), next(PTS), next(PTS), next(PTS)
                Cx = reduce(self.Count, [Pt1[0], Pt2[0], Pt3[0], Pt4[0]]) / 4
                Cy = reduce(self.Count, [Pt1[1], Pt2[1], Pt3[1], Pt4[1]]) / 4
                Cz = reduce(self.Count, [Pt1[2], Pt2[2], Pt3[2], Pt4[2]]) / 4
                Center_PT = rg.Point3d(Cx, Cy, Cz)
                Plane_PT = rg.Plane(Center_PT, Pt1, Pt2)
                return Center_PT, Plane_PT

            def Angle(self, Pla1, Pla2):
                zais1 = Pla1.ZAxis
                zais2 = Pla2.ZAxis
                angle = rg.Vector3d.VectorAngle(zais1, -zais2)
                return angle

            def RunScript(self, Geo1, Geo2):
                if Geo1 and Geo2:
                    ptsx = self.Point(Geo1.Vertices)
                    ptsy = self.Point(Geo2.Vertices)
                    cptx, cpax = self.CP(ptsx)
                    cpty, cpay = self.CP(ptsy)
                    angle = math.degrees(self.Angle(cpax, cpay))
                    angle2 = 180 - angle
                    return (angle, angle2)


        # 曲面或者Brep反转
        class MyComponent(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@BrepFlip", "HAE_Brep反转", """Reverse surfaces by vectors""", "Hero", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a5494016-bc1f-4404-86c0-86314ef76601")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep or noodles")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Specify direction (vector)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "New_Brep", "B", "After treatment Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, False)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOzSURBVEhL7ZJ7TFtVHMePWe+rLS29t7fvVveqCwVdmDqzZWOITi0DB4yF8diAwuhLOkYfUMpaUUQkwyi6ZDFu0xl0FGiGZBiNr8SZTBONmf6x6P4z7q/xx+KcmpmvB7jJ4h8OE/lvfpJvcs7vnt/nnHvuJf9zJ1NQwLJ+6V42YC7nOkwdrN/SzwRtw0zYOsKELIOsX44xfrlJ1WbcRqpcVqVrOTYxbKdYxcXFt9i49CPXLd/k4lZwCQeNE1wPTdIOvs8KPmUB328CnzSCT4jXuIT4BddlGGDqTPcpsr+zIOZT+ovCgAg+LVOhBWyXDWynYykRG7guulm3GVxUBh+n4l4JQlKEkDZAPaiH5kUd1Jm8m0I8723ysMOuqAnhIoYO4TkD+IxEm01gD1mp1E6lVNxFTx+j8l564pSZnlqmQiMEulbIGOhYD3V6QayF+hkNNM8L0L7KQ+gTLpMS/T2EVEp5bMxwlU/JVEZPfZiK406w9EoWNwqbrrMB4xUuIF3igtK3bFD8mntavMhH8i/zUd28kKTyIS00o2poj/LQvMBCO8RA9yYLPsa/QsSO++2qiHxDFaVyetdswPIr02L6SLXXmCbbhUrCEA99SYlGQ8PQqGhYGh2xCw5Vie4BZp+ugQ9px4Re4TvtCAf9OAvDh3SzVP4kaZ9KWneervptVch8lTwpZIib3UCbFzk01RvqzCXm6PCupcpybGK4Ot0T2pfVHxjPypAPu84QV3Kbted8/I/QTOhK9WhjhbJykbaT4WNjl15HzVjzSaX0r9AXrV9jHLwb+QHbJHGmt9j859qvH7nQg+gnUfiyge9rT7QOPzJcXbrn+P5TfZ8dQfTTBEqe9UaV/mUxB9d6pCEb8iPGaaLzFYhN2QO/hN8PwT8dQudsDJG5HrRPh9Gc9f3ZlmuD/9xBtMz4UBor9yqO26LZ7/RI4waIA/L4YqHspV3DrXNBNE/40XDah/rxA2jMNqJhsh77JurQOF2PvR/XYONk8bzGby5cbLoNq0fcDxa/57lha3E9qpQI2Zx5rN/7Ru212rN12JOrxu4zlXjqnQpUTpWjKFsA/Ywa1s+NEA+6apWWf8TT53G6a4rKlOktuArHuuLBLQNbX9vxTcmJ0t935LbDOmGCMKvCxh/WwD3kPkWXLfyq/5lVUnXhBumYZdb0pQ675x9C2bubz9N63tLjFaIwt3a0G7vQesH7E6eT1ynllcP3lfd45ucm2B5ffetjrSSlo1s9rob15cr0joSQvwB1RFKrVTVvvAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.set_vector = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _get_normal_vector(self, _srf):
                pts = [_.Location for _ in _srf.Vertices]
                center_pt = reduce(lambda pt1, pt2: pt1 + pt2, pts) / len(pts)

                single_vertex = list(zip(pts, pts[1:] + pts[:1]))
                vector_list = [i - j for i, j in single_vertex]
                axis_list = vector_list[2:]

                return rg.Plane(center_pt, axis_list[0], axis_list[1]).ZAxis

            def RunScript(self, Brep, Vector):
                try:
                    if Brep is None:
                        self.message2("Brep cannot be empty!!!")
                    else:
                        if Brep is None:
                            self.message2("Brep cannot be empty!!!")
                        else:
                            if Vector:
                                normal_vector = self._get_normal_vector(Brep)
                                self.set_vector = Vector
                                angle = math.degrees(rg.Vector3d.VectorAngle(normal_vector, self.set_vector))
                                if (90 >= angle >= 0) or (360 >= angle >= 270):
                                    New_Brep = Brep
                                else:
                                    Brep.Flip()
                                    New_Brep = Brep
                            else:
                                self.message3("Vector is not set, Brep is reversed by default")
                                Brep.Flip()
                                New_Brep = Brep
                            return New_Brep
                finally:
                    self.Message = "Brep inverts according to vector"


        # 曲面收边
        class ShrinkSurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲面收边", "HAE_ShrinkSurface", """On TrimSurface Boundary""", "Hero", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c2c7a2ac-1b63-4072-ba1b-17c7dd477868")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "Initial face (polygonal surface auto explode edge)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", '{0:  "No east side ", 1:  "No north side ", 2:  "No south side ", 3:  "No west side ", 4:  "Minimum side "}')
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Result after edge trimming")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFFSURBVEhLtdUrSwRRGIfxEfGyYDCLaBDjigbBJgr6LbyEjYLRYjCIIIIGg8Us+A1EEMSixWTQ7CWIRQwG788fd+DsmXfGPbPHB37sMju8Zy8zZ5OS9WCkQLVuFKU6xXcTdhHcKqxhvmt0o6EBzP0+NRvHJ6yBrg+MIdMRdMIx/O9P7+YG/jDLCjItwT3pDRuoQO3BfT2Pfp9ME7BOliuse8fyvGAQDbVjCwdYwwLOYA34yzwytdUf3RZhDShyiKbT1aTfwBpkeUAvgrqENcz3ihkEN4UnWENdunRLN4QLWINT7xhG6bqwD2t4qoaW042Yt00EXUFFTeIO/gL30CeNUh9O4C+ijTBaujm34d4r5gbXao9IF9AOHDX9JabD5RnBd3NRnVjGF9JFZhG9aegq0gKbOvAf9eMct7B25yh1YAfOtpEkP+yZxPhvIRGHAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_data = {0: "DoNotShrinkEastSide", 1: "DoNotShrinkNorthSide",
                                  2: "DoNotShrinkSouthSide", 3: "DoNotShrinkWestSide", 4: "ShrinkAllSides"}
                self.type_of_shrink = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Surface, Type):
                try:
                    self.type_of_shrink = 4 if Type is None else Type
                    if Surface is not None:
                        list_of_surf = [_ for _ in Surface.Faces]
                        map(lambda surf: surf.ShrinkFace(eval("rg.BrepFace.ShrinkDisableSide.{}".format(self.dict_data[self.type_of_shrink]))), list_of_surf)
                        Result = list_of_surf
                        return Result
                    else:
                        self.message2("Please enter a surface!")
                finally:
                    self.Message = "Trimming surface trimming"

            # 曲面按照参照平面排序
            class SurfaceSortByXYZ(component):
                def __new__(cls):
                    instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                       "HAE@面排序", "HAE_SurfaceSortByXYZ", """Surface sorting: enter the xyz axis to sort by reference plane""", "Hero", "Surface")
                    return instance

                def get_ComponentGuid(self):
                    return System.Guid("c5d243ad-a60f-46ff-8314-851545506bc1")

                def SetUpParam(self, p, name, nickname, description):
                    p.Name = name
                    p.NickName = nickname
                    p.Description = description
                    p.Optional = True

                def RegisterInputParams(self, pManager):
                    p = Grasshopper.Kernel.Parameters.Param_Geometry()
                    self.SetUpParam(p, "Geo", "G", "Surface List Data")
                    p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                    self.Params.Input.Add(p)

                    p = Grasshopper.Kernel.Parameters.Param_String()
                    self.SetUpParam(p, "Axis", "A", "Axis（x，y，z）")
                    p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                    self.Params.Input.Add(p)

                    p = Grasshopper.Kernel.Parameters.Param_Plane()
                    self.SetUpParam(p, "CP", "CP", "Reference plane")
                    p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                    self.Params.Input.Add(p)

                def RegisterOutputParams(self, pManager):
                    p = Grasshopper.Kernel.Parameters.Param_Geometry()
                    self.SetUpParam(p, "Sort_Geo", "G", "Sorted Surfaces")
                    self.Params.Output.Add(p)

                def SolveInstance(self, DA):
                    p0 = self.marshal.GetInput(DA, 0)
                    p1 = self.marshal.GetInput(DA, 1)
                    p2 = self.marshal.GetInput(DA, 2)
                    result = self.RunScript(p0, p1, p2)

                    if result is not None:
                        self.marshal.SetOutput(result, DA, 0, True)

                def get_Internal_Icon_24x24(self):
                    o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEZSURBVEhL1dUxS0JRGMbxk9UQlbsEfoC+hEODfYcQHB0cdQycFfoSOtTmpBC1BYZjSzgoSFODESEuCvp/z+Xo8WJ51HMDH/jhfYX3fXCQq/4zp4gFj/5zjj7KeoogF5iirqcIkoAUPOgpguxVQQrXweMivgqO8YmKnqz4KihB7hT0ZMVHwSXGkDtF+cKOj4IXyA0vBVk8I60npXIwx3cuSOIH5pgUfVmz2KngCfaxVZwLbtBCBkfII3xsFaeCE3zALL1jZM1/cSq4RXjR1doCmYcIL7r6teBeT8FneGkT8uuXYgqqOMQbeuhuSHY6uMJSTEFNTxHEvNEGeEQTjS3Jrty4w/wdf4ZXfGPiSRvy35lH2uIeHSil1AxX8Lwjz7Z6iQAAAABJRU5ErkJggg=="
                    return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

                def __init__(self):
                    self.dict_axis = {'X': 'x_coordinate', 'Y': 'y_coordinate', 'Z': 'z_coordinate'}

                def message1(self, msg1):
                    return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

                def message2(self, msg2):
                    return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

                def message3(self, msg3):
                    return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

                def _normal_fun(self, geo_list):
                    for f_index in range(len(geo_list)):
                        min_index = f_index
                        for s_index in range(min_index + 1, len(geo_list)):
                            if geo_list[min_index].GetArea() > geo_list[s_index].GetArea():
                                min_index = s_index
                        if min_index != f_index:
                            geo_list[f_index], geo_list[min_index] = geo_list[min_index], geo_list[f_index]
                    return geo_list

                def get_center_pt(self, pt_list):
                    center_pt = reduce(lambda pt1, pt2: pt1 + pt2, pt_list) / len(pt_list)
                    return center_pt

                def _other_fun(self, data_list, axis, coord_pl):
                    for f_index in range(len(data_list)):
                        for s_index in range(len(data_list) - 1 - f_index):
                            first_center_pt = ghc.PlaneCoordinates(self.get_center_pt([_.Location for _ in data_list[s_index].Vertices]), coord_pl)[self.dict_axis[axis]]
                            second_center_pt = ghc.PlaneCoordinates(self.get_center_pt([_.Location for _ in data_list[s_index + 1].Vertices]), coord_pl)[self.dict_axis[axis]]
                            if first_center_pt > second_center_pt:
                                data_list[s_index], data_list[s_index + 1] = data_list[s_index + 1], data_list[s_index]
                    return data_list

                def RunScript(self, Geo, Axis, CP):
                    try:
                        CP = CP if CP is not None else ghc.XYPlane(rg.Point3d(0, 0, 0))
                        if len(Geo) == 0:
                            self.message2("The surface list cannot be empty!")
                        else:
                            if Axis:
                                Axis = Axis.upper()
                                if Axis in ['X', 'Y', 'Z']:
                                    Sort_Geo = self._other_fun(Geo, Axis, CP)
                                    return Sort_Geo
                                else:
                                    self.message1("Please enter correct axis coordinates!")
                            else:
                                self.message3("Axis coordinate is not entered, it will be sorted by area!")
                                Sort_Geo = self._normal_fun(Geo)
                                return Sort_Geo
                    finally:
                        self.Message = 'Surface sorting'
    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Surface_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("cfdcf3f4-f42f-4d64-beef-3bfa11511a00")
