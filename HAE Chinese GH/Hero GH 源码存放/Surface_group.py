# -*- ecoding: utf-8 -*-
# @ModuleName: Surface_group
# @Author: invincible
# @Time: 2022/7/8 11:10

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from functools import reduce
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Line_group
import math

Result = Line_group.decryption()

try:
    if Result is True:
        # 扫出曲面
        class SweepOutFitting(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲线扫出", "RPP_SweepOutFitting", """解决原插件扫出的问题""",
                                                                   "Scavenger",
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
                self.SetUpParam(p, "Sweep_Curve", "S", "作为轨道的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Shape_Curve", "C", "模型曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "一个新的Brep")
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
                    return '轨道线不能为空！'
                elif Shape_Curve is None:
                    return '曲线不能为空！'


        # Surface面积排序
        class GeometryArea(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                               "Area sort",
                               "RPP-面积排序",
                               """根据face的面积进行排序""",
                               "Scavenger",
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
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "面、Brep等几何体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "排序后的几何")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Area_Arc", "A", "排序后的面积")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Centroid", "C", "质心")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                if isinstance(p0, Rhino.Geometry.Brep) and p0.Faces.Count == 1: p0 = p0.Faces[0].DuplicateSurface()
                result = self.RunScript(p0)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI6SURBVEhLYxgFJIMF2x4qLzvwJnDh9sdBC7ffh+Bdj4OW7n8dMHfbLVGQmsW7nnsv2fUMIQ9Uu/zAm6C5W+6Zgw3BBeZseKI+a+P9xpUH3vkt2vnEd9HOh77ztz/2Xr79oe3yg+/8Z226Vz9z0/2OxbteRC7dA5GH4RUHXvvO3nS/YvaWRx5Q4zDB3C33I1ccfW0K5cJB19ZbwSB65qZ7sUA8HyyIBazafZd/3rYHJVAuJgB5s2XGNl9tDY2Cf//+cXJxcRmFRMaWLjr+4tSqK1d4Zm18GDZ7870pUOUYYNmeu+Jzdz4shHIxwc6L/zzTirqylRTl/1dWVmZLSEjss7a1fXv0wXfn////M8/a/CB61sZ7U6HKMcD8Lfcl5u94WADlYoJt5/55hSdX5Tg62D23tLR86uXl9dHZ2XkbVJphxsY78RRZsPXcP8/4rPqK2JjILWZmZrfj4uL2uru7r4NKM8zafC+OIgvm73gcvHDrZZ8dOzZpHDlyRP3EiROKq1ev1oNKU27BvK33whfvf2EB5WIAii1YsP1h2MLdD22gXAwwasGoBYPCgkeRi3c/wihNYWDW5rv4y6L99wXmbX9YBOVigjlb7jvO3nw3Z+WhZ6JL9z8VQcZrj34WAxbVdbM231+x6vA7OXR5EJ6z5YH37C330qDGYYL6+v9Ms7fej1qx/03lop2PK4FBBsYg9jKg2LytD5wWb3ugtXjX06olu5/C5UEYpGfO5nv5i7fd4oMaNywAAwMAGY/CV6U66jwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def message1(self, msg1):  # 爆红
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):  # 黄泡
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):  # 白泡
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def bubbling(self, Face):
                # 面积质量属性
                FaceAMP = [rg.AreaMassProperties.Compute(i) for i in Face]

                Area_Arc = [ap.Area for ap in FaceAMP]  # 面积
                Centroid = [ap.Centroid for ap in FaceAMP]  # 质心
                nice = zip(Face, Area_Arc, Centroid)

                # 字典遍历元组排序
                AREAS = sorted(nice, key=lambda x: x[1], reverse=False)
                # 取值
                Faces = [_i[0] for _i in AREAS]
                Area_Arcs = [_i[1] for _i in AREAS]
                Centroids = [_i[2] for _i in AREAS]
                return Faces, Area_Arcs, Centroids

            def RunScript(self, Geometry):
                try:
                    Face, Area_Arc, Centroid = self.bubbling(Geometry)
                    return Face, Area_Arc, Centroid
                except Exception as e:
                    self.message1("运行报错：\n{}".format(str(e)))
                finally:
                    self.Message = 'HAE 面积排序'


        # 计算Surface面积
        class Surface_Area2(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-面积取值", "RPP_Surface_Area2",
                                                                   """Breps求面积：面积除以divisor，保留decimals位小数；""", "Scavenger",
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
                self.SetUpParam(p, "Breps", "B", "Brep/Surface物体列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Divisor", "D1", "除数，默认百万1000000")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Decimals", "D2", "保留小数位，默认三位")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Area", "A", "面积")
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
                                                                   "RPP-求中心平面", "RPP_Surface Plane",
                                                                   """求几何物体的中心平面PLane""", "Scavenger",
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
                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "依附中心点生成的Plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "B", "B", "查看Sur是否有效")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                if isinstance(p0, Rhino.Geometry.Brep) and p0.Faces.Count == 1: p0 = p0.Faces[0].DuplicateSurface()
                result = self.RunScript(p0)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM6SURBVEhL7ZNrSFNhGMfnZTqmVEODmFpTtMT60BevOHTMSxrmBZW0KZIT04lOsSwT85a2TN3CzbykZ5t5yXmBFPM257XCDCk1L6SEVBpiKmkfRufpPboPUoSmBH3oDw/n5bzv8/+d53nOS/qvvy4A0COeOI6bLqzh9svLy4e2Ng4iZKqNDI3EQ7it4sVaQ6Z8+MndKmxJ8KgVRmaW3TXH9i7CcAnAcHAWTy3r/izOkav6ciseLopKEtRtdX4w2WoD6yoyCMUx3zky3FKTtrtwfMOheXiuMkfa9TJLXLBQXpkAysbzMNNmDhs9ZIAhxB5GMYjiGQlEEp7aswQYmvTdhdrgKFbIYLWPDjCqDfAcGRGmhGEfCtWOQO9Fkji1Txlurkn/VagVR+Lj41N9fX3z/P39BWFRCfIIri9en04CRYY2fO3Q2QbsNN4rAJlTkHGTm5vbvKenp5zFYmEBwWGd/sFeIIjRhWuh+hDCpsCmSgug/yfzPQKo1tbWE0KhsKizszNZJpPZYy3KhNzC6zBXS4G5RgPwsjeASUx3u+/7AOiYmpp2x8XFRUgkEm4Y55IyT1jZmn4nUT0lJ8N0AwWCWVQYJwBooPsB6JqZmSnDw8M5aWlpl5lODp94iRmvMvL43yalZBiv0YNAFypMHARAp9N7eDxeMp/P92G5MJtEpXW9aXlX1RMYGWYa9CHIVQPYZ4vIJiYmHWjQTikpKcfPubMbo6Jj318IDsGvBFnCtMIQIr314U3VwWag5HA4yUlJSRGRkZHcLEFhE5cfAzW3DGC0UgsuuurBu2p0lLgPfwpAl8qAwWAMoK/3KS0ttc3Pzz+jUg0EVLd2j+UUFy1mFN5YdbCzgnYJA9b7qdu/KlEJMt5a76ECGpPJfO3s7HzT2NjYCs3jJINBP1UsvMfOLZB6h8YXJp61c91MFbf0CrDajw+kmfBY6gcjChtY6Tq8Nfjikmi1+/3fAAhhGObBZrOVFhYWCtSuejSTOhqNJjMyomGnbaybY6O5UUQrUbUn2mdxR9HT9ZSKjum32eW1UxJpNtyuqoausRVnjd3BhWAUBDtKVD/yAfdoGfkSOD8/f0yz/V//hEikH9g9dLOaG7vaAAAAAElFTkSuQmCC"
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

            # 根据中心点求面 -- U,V与原生不符，却与SEG相符
            def Plane_box(self, box):
                Center = box.Center
                UPT = (box.GetCorners()[0] + box.GetCorners()[1]) / 2
                VPT = (box.GetCorners()[1] + box.GetCorners()[2]) / 2
                Plane = rg.Plane(Center, UPT, VPT)
                return Plane

            # 判断Surface的有效性
            def IsValid(self, Sur):
                return Sur.IsValid

            def GeoBox(self, Surface):
                boxs = [g.GetBoundingBox(False) for g in Surface]  # 获取几何边界

                Plane = map(self.Plane_box, boxs)
                Bool = map(self.IsValid, Surface)
                return Plane, Bool

            def RunScript(self, Geometry):
                try:
                    PB = self.GeoBox(Geometry)
                    return PB
                except Exception as e:
                    self.message2(str(e))
                finally:
                    self.Message = 'HAE 中心平面'

        # 曲面挤出（曲线修剪）
        class Curve_Trim_Offset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲面挤出（修剪、移动）", "RPP_Curve_Trim_Offset",
                                                                   """修剪曲线，选择挤出量，挤出曲面，若不输入挤出量，则输出修剪后的线段""", "Scavenger",
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
                self.SetUpParam(p, "Curve", "C", "待修剪的曲线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "挤出的类型，{0： Line， 1： Arc， 2： Smooth}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "曲线起始点延长的长度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "曲线终点延长的长度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Extrusion", "V", "作为挤出的参考（可以是向量或是曲线）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Move", "M", "移动物体的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Objects", "O", "处理后的物体（曲面或者曲线）")
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
                                                                   "RPP-Sur_Angle", "RPP_Sur_Angle", """求两个面的夹角和补角""", "Scavenger", "Surface")
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
        class BrepFilp(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-BrepFlip", "RPP_Brep反转", """通过向量反转曲面""", "Scavenger", "Surface")
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
                self.SetUpParam(p, "Brep", "B", "Brep或面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "指定方向（向量）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "New_Brep", "B", "处理后Brep")
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
                        self.message2("Brep不能为空！！！")
                    else:
                        if Brep is None:
                            self.message2("Brep不能为空！！！")
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
                                self.message3("向量未设置，默认反转Brep")
                                Brep.Flip()
                                New_Brep = Brep
                            return New_Brep
                finally:
                    self.Message = "Brep反转"


        # 曲面收边
        class ShrinkSurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲面收边", "RPP_ShrinkSurface", """关于TrimSurface边界的问题""", "Scavenger", "Surface")
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
                self.SetUpParam(p, "Surface", "S", "初始面（多边曲面自动分解收边）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "{0: \"不收东边\", 1: \"不收北边\", 2: \"不收南边\", 3: \"不收西边\", 4: \"收至最小\"}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "收边后的结果")
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
                        self.message2("请输入一个曲面！")
                finally:
                    self.Message = "修剪曲面收边"


        # 曲面按照参照平面排序
        class SurfaceSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-面排序", "RPP_SurfaceSortByXYZ", """曲面排序，输入xyz轴排序，可按照参照平面进行排序""", "Scavenger", "Surface")
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
                self.SetUpParam(p, "Geo", "G", "曲面列表数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "轴（x，y，z）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "参照平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Sort_Geo", "G", "排序后的曲面")
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
                        self.message2("曲面列表不能为空！")
                    else:
                        if Axis:
                            Axis = Axis.upper()
                            if Axis in ['X', 'Y', 'Z']:
                                Sort_Geo = self._other_fun(Geo, Axis, CP)
                                return Sort_Geo
                            else:
                                self.message1("请输入正确的轴坐标！")
                        else:
                            self.message3("轴坐标未输入，将按照面积排序！")
                            Sort_Geo = self._normal_fun(Geo)
                            return Sort_Geo
                finally:
                    self.Message = '曲面排序'

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
