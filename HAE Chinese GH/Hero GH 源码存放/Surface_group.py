# -*- ecoding: utf-8 -*-
# @ModuleName: Surface_group
# @Author: invincible
# @Time: 2022/7/8 11:10

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
from functools import reduce
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Curve_group
import math

Result = Curve_group.decryption()

try:
    if Result is True:
        """
            切割 -- primary
        """
        # 曲面收边
        class ShrinkSurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲面收边", "RPP_ShrinkSurface", """关于TrimSurface边界的问题""", "Scavenger", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c2c7a2ac-1b63-4072-ba1b-17c7dd477868")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP8SURBVEhL3ZTtT1tVHMevJsYtm4mGMrfpkk1NjP+Cbxb1/TT6Ql+YjLgYX7iAcxu0PIaxshYQKC2M2YfbFrq15aHtCn2+hdLnlo3yUEBESEDYRoEuMZuAcV9Pe28mILIFEl/4Tb4599yc+/nl973nHOr/ozrTYJ6wc1hSqU/Iqoyj10t0g/XCzqS8WBv7obprXMnXRMUi8yRdrIllRz4dEV0zTaj56qi42jSuLKSjwqqOMXmRKlBce3ucLtOFTnNoVpLeia4660RSaAjPiDrjy+Vt/X5x950/ymiPs743iRKV09LMzICvsHfIPGSU2wwtzCwECkd33e0RCJROM1mPYpXHrkusodJwN59Ds6qxTkla+2b//Mn6LpZcuUi5XseSIxdLTnZMuY7igYP3j3lmzMyX3cey3yXt76OJuZfma+JnOTSry4pwQZGiR//YlwsEKGCAs3/T8+b59vcZByncd51AfqtPm1dv/5hDsxKbJ6XNzPSTZWcOu7h/DybfzdtPodGzAIH27jkOzUqgiV4spR3mtPf43guQruYdb+N7RUCXV7O9A9OkpIWZXtt/B29lOnhSqI1v7aBEGy+s0PXZ0t5j++9AGbp1ts7xCYdmdbVrTCxxJBdX3OQn76uDU6h1zKUv0dE8Ds2qrP1OqbAjHEozR/dWwEccopByHwdfG+/5utH7GYdmdcUwUlVjGUqueo48X4EMMLMus6X9L+CR9xAe2A7AqfsQItv8zAV54EsOzUrYMVrd0Dsy/VwREfh638tYtPEw1vkmApqT8LfyYGx4D2LTMCSeXwe/ldq+4NCsKm6SiIyh4OqzIiLwR8xBuOTvwCPjwSc7iKEWCu4mHqTWEFTR39Fgm4qfb3Z8zqFZCbvHa5sc46kVctx3LUB2ypw1F4z0FSRuUBgldktz0WgJQBlZgypwD1LP3HR+q2drRHx17FK5lrE+fNZBI5mPGN6AX/ZSFs5IcyAx+6AgcDqwSArcR5VxyHyu1vIph2Z1jRw0mefn9WUnb/cCAy8iQJ9A4joFr/RVSExMFq7yL0DpzxRYhGkKKNPFz3NoVgI6erFE7TTtelVk8z9Mfuhh+JoOQdLthDyy/hSuHFhAWywNZXAJlxXejzg0K5F5ovlG/yxWna+xN2VmG243iWep5wAs9TmQdVl2gK+ADq+gos3/FYf9W3xl6LvCH3v0KdcRbDAUNtw7uI9CsO0kavR2EguBkziycGJtdAXq6Cqq9KFvOORWibuGFJrB33DTH4PBH4R+R5OdMvAL2kcA/fBj3EqwNo5tQBt/CJEhsjX3zapsj3xQa5u9IDDMFxQZFv7V5YbpgnJduKBUF3vqK93Jggp1/xkO9V+Kov4Cm/OcEQH331YAAAAASUVORK5CYII="
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMeSURBVEhLYxgFMKBV8V3FuvpifHjz8kwGhv+MUGHyAchAg5KLUfZl22eG1M2+VNpV+XvawvL/3uWzj0GVkAf8apZPCq2be7Ggo/b3vAVJ/09tsv7/bq/Y///HGf5/OSj237Ns3naoUkwwYcIEcQsLi+VBQUEbL1265AIVZrC0tGxxcHDYPGnBrqqExq5v7/aL//9/lAFsKJg+BMSHGf4/362I34LW1lZnYWHh/0Dm/7q6uqsgsfT0dDNBQUGwWHXrtFsVk7ofwQ09gISJsaC+vt5BQUHhv5mZ2X87O7v///79kxUQEOgE+uC/ooL8/5K6/rOlE3oegw0/SKYFEhIS//v6+v5IS0v/37NnzwJWVtab7e3tf9XVVP8VV/eeo4oFW7Zs2aOsrPzYysrqv7q6+v+TJ09u4eHm+gr0wQWKLKitrXUGuXzDhg1To6Ki5gGF/oeHh4OCKoaDnfV/cU3v9dJJFFgwffp0M2tr6zurV6+uWrFihaOmpuadadOmrf3//7+cgb7e3fquOTuKejqekm0BCAANYwNiFhgbLAgEILbron9iWU31H/4fZiTfgpiYmGhgXlABsUNCQlLc3NyEgEzmkED/FIb6/wJZLQ3vKbLAz8+v0NDQUA/Ednd3rwFiSSCTxdXZsUZj8j9hii0IDg5O0tbWVgaxPT09c+zt7QVAbDcXpxzR/f95spopCKLMzExBoAWrfX19E0pLS6WAQbQRmJpcwsLC9IMC/Dd650yzzW5tfE62BcXFxdzm5ub/gSlpOjBPCNnY2Px3cXFJ8fb2drG2svzvGN3pl9ve9IiiIAIavhFYTESB2MDIPuHk5KQH9ImQuanJcY2qf5LZLXUf/58EGggq6ICGwi0i1oKMjAwnYAGnAGJnZ2f75ebm8q1atYo5IzXRM2nDa96QmlkvZ87L+H9kg+P/V3ukIJaALANa+navDGEL8IH//xkY0yackTMsvx5sW75nYlDt/NPAIPs+Y27a/xOb7f5f22Hx36ts9m6ocuoA4/r/cnol14Mdy3dMDGlcfsG/esEGqBRtQPvSw4JQJj0AAwMAfgZy+8cqEK0AAAAASUVORK5CYII="
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

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                p = Grasshopper.Kernel.Parameters.Param_Number()
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALnSURBVEhL5VVbSFRRFD2lmVlQ9hH1GSV9mJGWk6ZZ0UNJSyRNyB4fQdr41ilnGNEaNSnTO2aZOh8VmlMqoeOrx6hj+UwnRa2klIj608D+Cq3VPt47ICLmTPbVhsXd+5xz1zr3nr33Yf+v7RWwxl35xdszuTMuOLOxIja/OlSast4ALHFPn9i8PXko1Otic46/8qHp9GXtWKqgRKU+HKlFeQhMN8ZIy/9sgYVw3pbyyddD0ZGwP6VOH6LWDcuvZkzml8TgWeURjDZuwXeTE9BO2maGW7po+Kh6IqXX57cgtV44m1k8nqZVQl8aAbNhF8aN64CXRNYhoY3QSjCJsVAcjz2qroUJyGIftfTW+gKv6OVOAt8lJ7cQzoa1Al7xFfX9NTtFci7C8YLQQrCQdhF6CPxLaAPWCxhkmKIdd91h6C5imGomIi7CyYlwuJSh/TbDuIHibhsEPhhlGChhoHAaqggiei2SvX/AYLdUHFeE09gQg9ZagRES6KUdUoiNGxhWr2T41kBkbxmijjE4OTI42DNEHqWxQRsFzIWiQMY58XlfRWR0oA7LGJJOMKxfy3B+MQSe5zIc3MGweyvle5w49uYeg/MqEghaBIHWfIaGbNFfTrsP20eklLaODn8hMNokQ3eBSFqlYfhJKcsJedyUR6SUntw/eYB8Ww55qF42nYLXIilryoiE2kFNFkOuXEzZX5TC2liGpzk012tDmpqrZdMpiX4Cr2ReB0SEPoKlornP19hSaH01niKxpXLngw29yDhYR62Ct4LZjW0uWCtwWFl+NypbmCrQyWGsCsDHJy74YVohfpGl+fG2YRG1VoAuF3s/zWcXt6SBMC9F040Alb71zBVhLE1Igb5MbN9fZ7ZvOpsCXczC74O5zC0bzq6KER+PxI4Ev0u15SGpunfyLM3kzZJotFQfgqY4C/7q5mhp+SIYXaGu6olNron9x70VxuvBGkPbBe3jU9LsvzH6tXaSO8MY+w2gMpgCaT3OBAAAAABJRU5ErkJggg=="
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

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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

        # 曲面或者Brep反转
        class BrepFilp(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-BrepFlip", "RPP_Brep反转", """通过向量反转曲面""", "Scavenger", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a5494016-bc1f-4404-86c0-86314ef76601")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOfSURBVEhLpZZ/TNR1GMcfjnnHgXAcuNxsq+wP3KrNClajbNUxSV1Om26mFkq1VXj9XEbdpjVBjuKch+unnHSIU0BBvH6QiKeoEPTDKJ0r3VybTWrzD5camwavns9dFOFhX+K2177f7+f7PJ/35/M87893J0NDQwu6f+gP+EL7Ar5wT8BXO3HWhI8Eyus6qi5dGQwYgdCevnPc81KYpWUhlpfXsKzMOisra/AGN1NUEX82+Y+sraPQ14T5GYFg7f7TPOit5NznLgaidgY6HNbodPDjdifb3kjnd32mW3M77WzfXMgdJTu4+MdIgVV+ODQJvhM4apFTQjRoQySTefmp9Ed07ITQHHqA20sa/i0w50U/x+rTaFw3iV1ldmuUK5V2lsyerCLZ3DAtk+gmIbLVozsYJbDYV0H5s24k2UXqZDdpVkhz485ykzPdRZZeRaaw4K4kPqn3cOeqUQIFz/n5ba+T/tYkzjbbONtigYiNvvpk5t+XHtvBw7PS+bVN2FPnubpEHq9fG+WEHq3jF8oxpU/pUrrHQGOatVQpjmzWFGuuyftWaKoZQ+BCuwb1atBXQu1rDhretMeTDo5Bp3C5Q/hltw2+1OfDii5oZyiBQMxF3Smc14QV87RpSdm8VZICJzVJV5UQ4ySzy+MjxtSFCXcw/xU/0XfTuWV63BF5t2aw7hkna59QdPtWKH0sld3rhdZwAhcter2CqueNE1w4nFnMuNlF7m0Z5NzoIucma0ybmol3YRIRbfJVLvKoiwaPpBB5O5nrr3MzdYqbtg168ExPtNaW0V7s2jJGky8ZF2kNz7Ta8ORm4F2UCt9o0qFxoKZI2GQjcHGfCphVGOcYe/7llNjVJA+vcqSTRqP2vbaAmcgEmolMeYyYjg1G4+PD11icseVoQcsCehY+KhVWPyp0vS+8ulT4vlb44OW49wc15vynGje803ELqL9XzhEWzhKObhWWeFToHeGFxcLPO4Xls4XiuULNao3VxfwvgaKH4hOe+SwudGCjMPdu4eQ2oSBXKF0mPF6osebAjVtAAw9W6+RNev+1sLdK6G8W9geFnxqEvBnCRq/eN+r7kWWyLHBAMU02yeZ++Fuj5Rhoj/cjZmGdMPb+vwQKvBVxR5ivqUm6FibGlCXROxX9OHwvM0sa/xEIdZwi76lKdnx4Py1b8mkJTYBwPr71xcx8Ovy3QKjr9AWKNrSxorqHoureiRHs5clNh/G+167/KeBP0gy8jAnAb0EAAAAASUVORK5CYII="
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

        """
            切割 -- secondary
        """
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQISURBVEhLrZZ/TFtVFMffrK6DhVmEYmlLC6V7pT8oJVJ+tJWSCqw42jJHtjnqwubC/ljEgVPo2gTUxGEMc2RNJjaCIRkLxGSw4GAbi8zNRVwChtVocMmy6CKRFN3+MP7V6/c9ri6Fgt2yT3LSd84995777jn3vDIrGR4eFjQ0NGxJSUlJy8vLS2tqakqmQ08Gi8VSrVQqL2dlZY1zkpmZOZ6dnT2mUqlCkEa73S6hro+H0+kUut3ulPn5eWFPT4+woKBAZDQaDWq12otAIQS/huf+oqIiA53yZPF4PKKcnJwWBJvF70lCiIAOPRrS/Lc1VS/vNVF1FcjNswjSjyBzLpdLTc2J4aj21LU26u976y0dDEOS5Wy9s6LC1lq33eorse6soW48CHJILpf/Zjab9dT0/7zxmnGU3GBIcwN7u/119d1LwTTyy7lkEpkQkltnU8mJd/STjLAtm7ozOp3uVZlMdg9BEiuAlgOmD8lVAbk/8RQh0wwhNyHfQmYhtyA/MWTsxPP3VIY9RXQKg8S3oepuUHV9dteVvfkAu+UXnYJch+CNvjguJkcb2XAoIL/zYCqJXP8042+z/cB/QRQKxRQCtVB1NeXl5WauRF2uHVVLFzYt7xiLL10UkCP7tt5lnvNWLXuSTZ4ax8Grp8V/fvmx9C+7Z/m4ULoa5OMOd1F5t5UUFha+i7Oc1uaXfHLKb5idO7M5SmYY8gcCvHdY9YOzyrantL4libozjMivHHg/d+ZUG/trR8d5/sYjwIhGoznKj8fDZrOxSqXic5FYM/2i3d3+0Vv6/q9DqdErwXTykqN8bPve9lTqSiFP+5p0E837y77itNzc3G3Y5DV+aD1Ylt0lkUjDgi2Wapk2sLXQuvsVOhSXne6K8zU121q5Z4lE8n1CLQW9x4DE/c7tiprWhpANLpfndCAQ0IvF4tGE5nBwfQjlF0GNr3mr/6W7uzvJ7/dnZWRkfIY5h6g5PiMjI5rJyUkd94yG58WEHxPtO+np6UEk+hhVYwmHw5LS0tIrxcXFpLKykvh8Pj55aAnjeO34k1aAI+pF1z1C1ViwaD8WIkNDQycHBgb29/X19XB2HBUrlUp/9nq9m3nHdUCSz6GS6qn6EBzBBix+G92RRKPRh/VOwTFdQPc8SNW4cGtg8Ztc7qgpFtyD77RaLVlYWKiEsygYDJZwk7gxBN+HqhrnHdfAZDLpEGCut7f3GWqKZXBwcJfVaiXIA8HnM9rZ2bmEABu5MYfDIcMndGa97zRy9QHeNETV+EQikTKU2+Gurq7mxcXFF6iZB+f7TT6gagz4w7AReZpHyzFS06PDBcAx1VI1BuTnOC7nKFUfD3TMYyjDVZcOXViKVh2ura1VUBNgmH8Al6pd4AB4HswAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Sweep_Curve, Shape_Curve):
                if Sweep_Curve is not None and Shape_Curve is not None:
                    Brep = rg.Brep.CreateFromSweep(Sweep_Curve, Shape_Curve, 1, 1.0)
                    return Brep
                elif Sweep_Curve is None:
                    return '轨道线不能为空！'
                elif Shape_Curve is None:
                    return '曲线不能为空！'

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

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPNSURBVEhLvZV7TFN3FMePl5eVbeXeBNuOPmit+CBtYbZstBC2YGVGsxRKE5IS0coaG91SMhKmyQKxs5q9kNgFiWA168KIUQeo+2cmom7d8IFGnMvcpvtjJHtkcS7sIRtn51d+A2Qaii77JCf3/n6/c7/fc8/93Xvhf8P6xNLgqhLlEYNhySYAZwHAeAZf+m94qjDnjZHDgFe7UzDaMh9dT8uHtVqTyJcfnicL1eGfjgHiEMXXgLtfgDGAhQq+/PAwg+97SfzjCZM3Nwu3ARQL+fK/QMQ0fpocczHw+/1VxcXFN9rb2xv41OzMxcButw9kZWVhVVXVN2wcCAQ2+ny+PaWlpb1tbW3+RNJMZhq8tUX4maYXTKxO0dHRobVarXeo+isFBQU4Pj5uzs/PP2Gz2dDpdI6WlZWxOTVPn2KmwU6/8KskaT1UlYqnJHC73Q1KpZJV/5coitjZ2bnTYrEc9nq9Q11dXQ0Oh4MZLOfpU8w02FGf8ruUre3Jzc09qdfr91PPE+0ymUwjNTU1P4TD4R0kdtPlco16PJ4blZWV10Kh0LaKigpmkJ8Qnc69W9ScSg90gcFgeFmtVn9ObbC2trZG4vG4m13T09PjjEQiB2Kx2PZoNBrs7+8vouM+MpASotOZ7SEbjUanTqf7kqpN51NzYzYDRl5eXhPdyUE+nBvJGNDLJWg0mrjZbNbzqeRJxoCh1Wp3U6s28CHhVcnkxmqVyvAilXD/tztZA8gw+zJF4xHTspxttWvEgV2bZbfP7k3Fwf0pWL1SHAQoWcEz72bSIE5xDTASFG4BnKeKMBXAZtXrNQ2V5VJfy/OZI+/vSsNvj86bLAbPUVwA/PMMbe+A7E62YtFWLjsFM/ixjxI/BRzqBly/Whi1F4qHGr2Z12PNGfhFt4B4mtYvToglxAcoTvFg58yIvsSfvTsPy4uky6JqhYPLU40WdXjsJGBnE73F9YAf7QX8g8YJMSb6CQUzmC7ITP5Zp+qvvydgrDkdtwceuflMkdS3eKm1hssDrLSrw+c6AF/dSMmXKQYnLpoUZHGWglXJ2kKtHKE29b+ehi31su/c5dLxRXrdS/RvtN3zb+h5Vh3e6gW8tI8upjYlBJkBM2KCdLz1AeCpSCq+tmX+L+vWyk+bl+eE6ONRDtAk5zL3Ry7XhILVJDRMwW75POBvHwJeoN3xdmPG2Cb3Y5dKbKoIyPJcAM89zi9LHp1GuWc4Sn3sFfDgK+nYWPvoV6sc2e9ICqOPGriYpz0YdXV1WZZlisHa1dIxg04TpD1Fexkf7JtzFwB/A5CoKg9BeYYRAAAAAElFTkSuQmCC"
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

        # 曲面按照参照平面排序
        class SurfaceSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-面排序", "RPP_SurfaceSortByXYZ", """曲面排序，输入xyz轴排序，可按照参照平面进行排序""", "Scavenger", "Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c5d243ad-a60f-46ff-8314-851545506bc1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO3SURBVEhLzVRrSBNQFJ6Yumo9QCXnUmwuxZzT+RjbdFPTWJqaimJZDDSyDPNVQggVi8hFTbNSKwpNWqJoFqhhYtYqW1qbZeoPC/oZSGSTEJ+nc9aIGMtG+qMDH/fec+79vnvvufcw/juD19edjGVRefoD4hKd8s94XygtGVbtiLQss98gM9PRkM+enbm+Fkw1LDBdtYFrLJi9uBH6c3nV5kV5eXlrJicnuQDgQOPx8XGvpqYmHxx7myegjY2N+SA8Bzv7g94Ub5oAPQNgEEGtNYYQrc6gy+KdMy/WaDR7IiMjob29/VhRUVGIWCyeValUIJPJZhYXF4P4fP7+hISEhZOnToEwJAR47i7AZTPg410keol4YgX0zd91Ad1ei8DU1NSmwMBAU0pKykRsbOxwTEzM4ujo6GlXV1eora196Onp+S47O3u6X68/c6fhRo3E2/X7ahcGfOlEshdW5LYEyKqqqsqIkMPhQFtbWwP5UHCAx+NBCO66t7e3hnwtLbe9Vzmtn75ZhkQGK+KlBBobG6VMJhNwt4C7LyBfd3d3Bvlo95gPLvl8tgr7BBwk0TkAPLMiXkrAy8urMzExESIiIiArK2scCR0RzuifKy0tHaA5GXv2ZbDWu0OrciPAWxR4jmR9VuS2BHJycuI9PDygo6PjXnl5ea2vry90dXUdoRj58/PzjdTn84NGnFc5gZS7DuQCBgzdQjJ6NX8TwETmarVaI70YhHtdXZ2+p6dHRbHKyso+FL70c961K+pzFSPFsW5z6oMM+NSMZPYm+XfDq2FRq1arN1jGzPr6eqalv+ZTOfszGLFL5PZckbVJpdKGbWj4DzTYl+C/qIiLi9tNMc3mktXGYvfP8BSJCNbk9giEhYW1+vn5CbCtwaTLg4ODqyUSSQbFWjKvspYtEB4e3uzv7x+E7WWRSCTDf1CJPz2dYisloGWz2d54ggsogAcIrsATKCh2P+Xmun8WwAQ6pKenJ+O9P8L7L4uKiuqUy+VnMAcPMAcVu9LS+F07q12WdQIkvof3Pi8QCCA0NBSEQqG5VOBJQLRdIaM5yxLAqrk9ICAA8Fq+YR4WsJJOW8ajFO8XNy/vFeE1OeKOv8bHxx/HUxijo6PP4ilGMAfmySuS5KSkpBNKpZKjUCgOJScn87BGHUpNTRVRbEUEKNm2WrJfAlRJCTobeMWAhaYlBJYyEjAcdftiLhGExzZAJUTrDE/3bjlvWWa/DTVeWDtwmPthuMjDZChkmwxHbQD9H0o4poEC/ukf9kKYzwbUOJ8AAAAASUVORK5CYII="
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

        """
            切割 -- tertiary
        """

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
