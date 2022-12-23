# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/9/17 17:06


from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import Grasshopper.Kernel as gk
import Grasshopper.DataTree as ghdt
import Grasshopper.Kernel.Data.GH_Path as ghpath
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
from functools import reduce
from itertools import chain
import math
import Line_group
import time
import random

Result = Line_group.decryption()

try:
    if Result is True:
        # 合并以及封面
        class Seam_Merge(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@封面合并", "RPP_CoverMerge", """封面以及合并曲面""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8bae4c8b-b1a4-4b0f-a4a0-5471683daf3c")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Suface_Or_Brep_List", "M", "面以及Brep数据列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "封顶缝合以及共面")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFCSURBVEhLtdW9K0VxGMDxg7wNBhGDbMrbYrAoqz9A2XVXJbvYLHZlsGEyKGWQlMkgL/kHJMpLKZK3RfF9buepp1/Pvfid3/3Wp9O59/yeX93OuSeLaCg/1qRRPKK3fFaDDvCNzfJZ4iYhw9UYktWMS9gNjpGsedjhahqF68EbvA3u0IZCbcAbrpYR3QS8oaER/Ls6rOIcp/iEHfqKE1xgCVHVm+MN7AZn0BryY3Td+IDd4BZNSJI8VHa4+EIfkjSLcAMxhSTtwttgDYWT3/8d3gb3aEWhFuANVyVE14UneIPVFVoQ1R68oaF1/LlGjGMf4SB5emeCz9QW5I2nD2fF+uENEPK3La3A+15uhg5UbRDe4h1o8gQfIbzmBZ2o2gDChduQt5qtHYew1z3j1w2GoQuuMYdKyZ/cIh6ga+TOy8uyH7DipjZyJ+85AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Suface_Or_Brep_List):
                if Suface_Or_Brep_List:
                    # 封顶
                    Brep_List = [i.CapPlanarHoles(0.1) for i in Suface_Or_Brep_List]
                    # 封顶后列表去None的操作
                    Bool_List = [i for i in Brep_List if i is not None]
                    if len(Bool_List) != 0:
                        # 缝合以及共面
                        Brep = rg.Brep.CreateBooleanUnion(Bool_List, 0.1)
                        Brep[0].MergeCoplanarFaces(0.1)
                        return Brep
                    else:
                        # 缝合以及共面
                        Brep = rg.Brep.CreateBooleanUnion(Suface_Or_Brep_List, 0.1)
                        Brep[0].MergeCoplanarFaces(0.1)
                        return Brep
                else:
                    pass


        # 映射以及挤出
        class MappingExtrusion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@映射及挤出", "RPP_Mapping&Extrusion", """映射一个物体到指定平面，之后通过线段或者向量来挤出实体""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c8ea9cd3-3a21-4abe-ad66-f4d7061b95d1")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "原始的几何物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Origin_Plane", "A", "原始的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "B", "转换到的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Mode", "M", "作为挤出的模板的线段或者向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Geometry", "G", "新的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Transformed_Objects", "T", "平面转换后的物体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFESURBVEhL7dQ9SgNBGMbxhaBRglEEe8EmeAFLvYaFnaewlKRIkAgqoifwDmKrlgkWduJHDBhjYUAECUH/z5qFl3HXnVULizzwg53MzDub3ZkNRvnXyWHm8/LbTA1lyjIu8YQ9aDE3kzhABw/YxThSk8c13o1VuDmEHSPbSM003mAnbsCmiB7sGOliAqnR37WTFmBTwD1scXmE1wLKETRpMWx9zRncBarwTgWaFPfi9qG+E9zgFjXEbYbEbEFF9LxtouK6AUWbQjInWkDbMYpb/FfZhIrNha0/Lq6dcAwVbOF0eF2GGz2eFZTClmd0QlXQ0gt1M4sG1N/HOlKTdIhe0MSF0YYd43UO9OF6hp0oA5w7rmDH6JvktaN2YCdK3CHSzWgh9b9iDV4ZQx130CFS8aRDpN+XMB+2MkbP80eHaBTPBMEHp5Vw073hBscAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def get_new_brep(self, geometry, p1, p2):
                primordial_plane = p1 if p1 is not None else rg.Plane(rg.Point3d(0, 0, 0), rg.Vector3d(0, 0, 1))
                if p2 is not None:
                    transform = rg.Transform.PlaneToPlane(primordial_plane, p2)
                    geometry.Transform(transform)
                    new_geometry = geometry
                    return new_geometry
                else:
                    return None

            def exturde_brep(self, object, curve):
                if curve:
                    mode_brep_list = [_.CreateExtrusion(curve, True) for _ in object.Faces]
                    mode_brep = rg.Brep.JoinBreps(mode_brep_list, 0.001)[0]
                    return mode_brep
                else:
                    return None

            def RunScript(self, Geometry, Origin_Plane, Plane, Mode):
                if Geometry:
                    Transformed_Objects = self.get_new_brep(Geometry, Origin_Plane, Plane)
                    if Mode:
                        line = rg.Line(rg.Point3d(Mode), Mode) if type(Mode) == rg.Vector3d else Mode
                        mode_line = line.ToNurbsCurve()
                        New_Geometry = self.exturde_brep(Geometry, mode_line)
                        return New_Geometry, Transformed_Objects
                    else:
                        return None, Transformed_Objects


        # Brep结合
        class Brep_Union(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@结合", "RPP_Brep_Union", """将多个Brep结合成一个.并消除参考线""",
                                                                   "Scavenger",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("57cfa2b7-7b3d-43ee-b190-3af9cfa5c6f9")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Breps", "B", "Brep物件，list类型数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "PRE", "P", "合并精度[0.00-1.00].成功情况下不改动")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "结构之后的Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOmSURBVEhLrZXtT9tWFIf37+3PWL/vyyZVKxPTtHaFlU5qNdGmQDcgiUkCawuUlwFVEbB0G2szIDh23klIFuxAYjt2YjvOb8eXjBSaTGJg6VEc5fg891yf3PORIAgfl8vle/F4/Npx87qCh61WC7IsXztuXldw1/1Cn9jf568NURSYpC2QwItJZPJHyOZLV+OwhHSuBF5IdARHR0dIZfNwL7esVsth9/91uTGnseehX9B0WhATGUiS1BEkMznYdhOWZVGgg6h4gNX1MDbD22dsvfkTS2tb2OFTcByHxV7Eti00TAtCIn1BkD6gABumabKV7PFJjPtnMO4NYMIXZHChZ/ii/w5ezC+xKtzYi1iWiXrDhBBPQ+4lcFcnJrMIUMLJSS/8fj9jejqEz2/2YX5h+XICqS0wqbRGo4Fms0klZpjA5/OB4zjGzMw0bt7qx9zCL0zgxl7ENBsw6g0SpC4n8FEFgeA0Pv3sFp7NrzCBaTtt6MU2HXq23luQIEGDSqvX6/SibMTiHYHPzyEUDODV8gzGHj/A+upLVKUs5AK14mEC5UIc+dwBDMOtog7dqHcRpLKUnOyGwbohRnt4KvBiwsthN/wS6n4QeiwEZY+D/HaCUY5MIrflwax/GEbDZgus6QY9f0mBsL0MK/oUdvQx7D1PB34EhfXvMDUyiLrl9BBIpwKDStN1nXUDL54XxP6g1oz9SHgA/kkHcRTy1hCCT4eogiZboFbTERO7CoxzgtDPLzA15YePC1AFS2j1EEhnAru3IE4CN3mtVmOdxFPA6DiHH4af4MHwKPbeLKAl/NRbMHYPet1iOVSt1kWQzLDkmqbBolbb/H0XX3/7Pe4M3Ef/7fuIbM4BiXFKSAKBEv9LYgzH4SEESFAzTJZDUTUSJD8UqJRcVVWSqJDkYxRLMkrSMQqlE5QSv+Fk2wP13TDUt486/OVBem0Q3MgANL3BFlhVVHY6u6d0WyDR0ZAhswpFUVCtVqHRfa2mMXTq73dbi3jl/Qqvp74hbp+xTqxOfInnnAeKZrAFVqpKFwGdftV28g9RkMsX2J8pn893IYfi3yUWqxAnlSrNg/cEblnu+a2zDqihUqmcJa+0UWlfNXp5vXC3141zBcdM4A6ctmBxcRFRPo7nc0tYWF6j2XDI2vT/EhVS2OdFlMs00TY2Nu729fUhHP4VN258gsGBARSLRTajr4IoiqcjMxKJPNzZ2aV9PMTs7BxWVlbIXKZpJF8Zp9XCP0E68839C3s/AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def brepbp(self, Breps):
                Result = rg.Brep.CreateBooleanUnion(Breps[0], Breps[1])
                Result[0].MergeCoplanarFaces(Breps[1])
                return Result[0]

            def RunScript(self, Breps, PRE):
                PRE = PRE if PRE else 0.02
                if Breps.BranchCount > 0:  # 判断执行
                    breplist = []
                    for i in range(Breps.BranchCount):
                        breplist.append([Breps.Branch(i), PRE])  # 参数添加
                    res = ghp.run(self.brepbp, breplist)
                    Brep = ghdt[rg.Brep]()
                    for i in range(len(res)):
                        Brep.AddRange([res[i]], ghpath(i))
                    return Brep


        # ZY_压顶板实体
        class ZY_YDB(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@压顶板实体", "RPP_TopPlate", """压顶板实体插件：
            适用：直线压顶板。接口处需要延伸出一个接口。""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ddf1019d-a9fd-40a8-859d-3762878601c7")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Part", "PA", "整体实体大面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "CE", "截面线（最终线段）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D1", "截面线偏移距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PLA", "PA", "截面线偏移参考Plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "IX", "需要延伸的线段下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Re_Sta", "RS", "延伸的线段起点缩短距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Re_End", "RE", "延伸的线段终点缩短距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vec1", "VE", "延伸线段的延伸向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance2", "D2", "偏移大小")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Surface1", "SF", "延伸面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Breps", "BS", "未结合的Breps")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "偏移结合的Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                p7 = self.marshal.GetInput(DA, 7)
                p8 = self.marshal.GetInput(DA, 8)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7, p8)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANUSURBVEhLrZXJTxNRHMdHxUQTE+XiSqJ/gje9eFFcIDGA8YDRxLgQdwUEo5WDiHFXYlArYDtdBxHCYluBAukyULaKyK4iQTHhYuLCVpi2X997NYFmppAgv+R7eL/tM+/3Zt5wj9TmeFOx7b5aIyy6DKQvV8ALeaIowmq1LrrcbhFcPi/cpYuiIgEGvR5aLQ+eX7hovdFoJP2KYLFYZwAG4qypF9H2vhut7zoXLFpfabMTiCEcoNHq8HlwGIthntZ2shNtOEDL69D3aZAlTE9P/5OEacmPQMA/yxeSJEnwTUkIBgNhfmpiUxsbVxiAJ4Dej19YgiSFEvsHvkJsbsfv0QmyCiLgJ0DahDT99WccjoY2DA2PEEiQuPzwkzg10TMPYGLSh+8jP+Bwe1Btr0djsxfDZP1ndBxTU1MM6CWzrrbXod4hkp0P4efvMYyPT7L6iICe/hBAX2zB7cf5eFGox9btu5B14w5KK2xISc2Gq6kDD54aUFZpQ3zSYRxIPobi0gpk33uGsxk5rL6BjEgnB+gJYIAlvK60I+3qLRw5fga74xIRn5CME6cvITE5BbWuVjzJN+N8mgpx+w9id3wSDh09haMnzyHlwjVyXsEQQDcH4E2NiNy8ArIDHhqdCYVaA5EeN+88QZ3ohU6ogDpfg5e8kYnmqQs0uP1QDckfYCNSBHT3fWaAkoq3iF4bA47jwhW1irwhXlxIV8ljRDv3JrB60dM6N6CUANZt3CxrELViNdweL1Izs2QxqlgyTmrKAJ0eXb0zgPWbtsgaLF+5Bu7Gtn+ApbJ4bFwSq3c3UoBOCfCJJZSU2yICXKQ4NfM6WSsBQjtwN7YoAzp7PrKEuQDOhvkBroYIgA/dIcDrssgAh9iC1Iz5AM2RAP0sge5gQ4wCgByyw92MdHYGS2TxXftCb5EzEqCjq48l8KYSLFsRLWvAcctR5/SQD/CcQozDth17WL1TnANAL7oaRxMuXlYh7UrWjMhTZ6hyyAX4DbnPeXYOs+OXMlR4rhFYvVNsigAgZzAxOQmfz8eeRMnGxsbY7alk1E8vSjpGGcBkNqO03AJrVS0sb+0LlrWqDsUl5TCbTeGAIkGAyWSEwaD/b9HmAunHAC/4V3n0708Xiy2XS8RfYjBLSibHeVUAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def offset(self, cur, Dis, PLA):  # 偏移线段，返回两组线段（偏移线-组面线）
                Reline, SurLine = [], []
                for CE in range(len(cur)):
                    PCL = cur[CE]
                    DIS = Dis[0] if len(Dis) == 1 else Dis[CE]
                    line = rg.PolylineCurve.Offset(PCL, PLA, DIS, 0.01, 0)[0]  # 偏移
                    Reline.append(line)
                    SurLine.append([PCL, line])
                return Reline, SurLine

            def BrJoin(self, Brep, Surface):  # Brep结合
                for sf in Surface:
                    if sf.GetType() == rg.Brep:
                        Brep.Join(sf, 0.02, True)
                    else:
                        Brep.Join(sf.ToBrep(), 0.02, True)
                return Brep

            def TilrExend(self, Curve, sta, end):  # 线段延伸或缩进
                CurveSta = rg.CurveEnd.Start
                CurveEnd = rg.CurveEnd.End
                if sta:
                    Curve1 = Curve.Trim(CurveSta, -1 * sta) if sta < 0 else Curve.Extend(CurveSta, sta, 0)
                else:
                    Curve1 = Curve
                if end:
                    if end < 0:
                        Curve1 = Curve1.Trim(CurveEnd, -1 * end)
                    else:
                        Curve1 = Curve.Extend(CurveSta, end, 0)
                return Curve1

            def Brep_Bool(self, Breps2):  # brep结合，
                Brep = rg.Brep.CreateBooleanUnion(Breps2, 0.01, True)[0]
                Brep.MergeCoplanarFaces(0.002, True)
                return Brep

            def RunScript(self, Part, Curve, Distance, PLA, Index, Re_Sta, Re_End, Vec1, Distance2):
                if Curve:
                    if Distance:
                        Reline, SurLine = self.offset(Curve, Distance, PLA)
                    else:
                        SurLine = Curve
                    Surface1 = []
                    for SL in SurLine:  # 组合先成面
                        Surface1.append(rg.Brep.CreateEdgeSurface(SL))

                    # 缩短线向量成面
                    a = Reline[Index]
                    Curve1 = self.TilrExend(a, Re_Sta, Re_End)

                    Surface3 = ghc.Extrude(Curve1, Vec1)
                    Surface1.append(Surface3)

                    Breps = []
                    if len(Distance2) == 1:
                        for sr in range(len(Surface1)):
                            Breps.append(rg.Brep.CreateOffsetBrep(Surface1[sr], Distance2[0], True, True, 0.02)[0][0])
                    else:
                        for sr in range(1, len(Surface1)):
                            Breps.append(rg.Brep.CreateOffsetBrep(Surface1[sr], Distance2[sr], True, True, 0.02)[0][0])
                    if Part:
                        Breps.append(rg.Brep.CreateOffsetBrep(Part, Distance2[0], True, True, 0.02)[0][0])  # 偏移
                    Breps2 = ghc.BrepJoin(Breps).breps  # 结合
                    Brep = ghp.run(self.Brep_Bool, [Breps2])
                    # return outputs if you have them; here I try it for you:
                    return Surface1, Breps, Brep


        # 圆弧铝板实体
        class ArcPanel(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@圆弧面实体", "RPP_ArcPanel", """圆弧铝板实体生成，参数较多，不易调试查看，
        请将所有参数连接查看效果""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("32aeca57-6e14-4773-82ac-9458b6ce3421")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "PolyLine", "PL", "偏移后的面折线, 生成大面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Up Down", "UD", "横向线段(上下) ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vect1", "V1", "横向线段移动向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Left Right", "LR", "纵向线段(左右)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vect2", "V2", "纵向线段移动向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Rotate", "RT", "纵向线段旋转角度(不用转为弧度)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "RPLA", "RP", "旋转依赖的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "DT", "所有面偏移大小")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Surface", "S", "各线段最终生成的面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "面偏移生成的面板实体")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                p7 = self.marshal.GetInput(DA, 7)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALzSURBVEhLrZVNS1tREIaDLkRQEUFQiCAY/AduxD/QvejOhcugC78QEfeCuoobFzWJpkmxLWKNxtK0obnxWm0VUo1J1KZCdir4Ec2XSd6eGdu0sSemaA683CR35n3unZmTo5l5bntmfb0yPmO0Fl3kq7FarQZFUWC324suRfGAAOP0xWazYm7ODKPR+GTNz88LP5uArPwB0I9r711QN3ew/vnro0X5S/Y19ssBzM6acPQjjGKsrW2v8JvNBRiNJgQOQxyQTCaRSCT4898rk8lkdX9RPOXR2tja4VLlAkwCcPCdAyg4lUphYWGBmxUKhXB2doZIJIKbmxtcXV3h5OQEgUAAFosFbrcb6XQ6+1Dq5jYDlh8C0Gpra4NGo0FZWRlqa2vR0NCAxsZGaLVa1NTUoKSkhO+Pjo5yfEGAPygA4vV/B/b19aG6uppN8qmurg4mkUtli8fjnFcQQLW8vr7G2NgYhoeHMTIygv7+fvT09ECv16O3txeDg4P85AMDA5ienuaSFgCYsR88QkbUkoLPz89RWVnJT0lXKotOp0NzczOamppQX1+P8vJyvt/a2srGBKA3oXGVAwKHSAtzalg4HEZVVVVOOfKppaUlWyLKLQig5fP5UFpaKjW8L3qraDTKvXsQ4PMf4vb2lgGqqkrNZKJy0RhT76i8no08gD3/QXazrK6uSs1kqqiowPHxMZunxAN6Nr6IyZIB9oPZEaUNJDOTifaD1+vl8iRFvkclgOlfwK4vmB21qakpqVk+uVwuzqN8Rd2SA775AojFohw4MTEhNconp9PJkxSLxaCsSwAmAuz5xTTc/decnp7C4XBgcnKSd3RXVxc6OjrQ3t6Ozs5OdHd3Y2hoCAaDQRwsCi4vL1k0Te71zTyA3TsAbTKC0Kb7n0WTd3FxwXkPA6gHibgwjzxacdFkt6zJNDWLb1fEqfYRjncfHi06FV+9WcIL4ZcDEFdYxDFnNpsx9wRRPpmT3y/AS4NbNGl52V50fVI8+AkYhmYwDNzYmwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            # 对偏移后的面进行切割
            def Tile(self, Q_surface, B_surface):  # 1.PLA平面，2.被切割面
                ud_surface2, PLAS = [], []
                for i in range(len(Q_surface)):
                    cenpt = ghc.IsPlanar(Q_surface[i], True).plane  # 引用内置IsPlanar电池提取中心PLA
                    PLAS.append(cenpt)

                for surface in B_surface:
                    if surface.Trim(PLAS[0], 0.02):
                        trsur = surface.Trim(PLAS[0], 0.02)[0]  # 平面切割
                        trsur = trsur.Trim(PLAS[1], 0.02)[0]
                        ud_surface2.append(trsur)
                    else:
                        ud_surface2.append(surface)
                return ud_surface2

            def OffUnio(self, Surface, Distance):  # 偏移曲面 Brep结合
                Brep = []
                for be in range(len(Surface)):
                    if len(Distance) == 1:
                        Brep.append(rg.Brep.CreateOffsetBrep(Surface[be], Distance[0], True, True, 0.002)[0][0])  # 偏移
                    else:
                        Brep.append(rg.Brep.CreateOffsetBrep(Surface[be], Distance[be], True, True, 0.002)[0][0])  # 偏移
                Brep = rg.Brep.CreateBooleanUnion(Brep, 0.02)[0]  # brep结合
                Brep.MergeCoplanarFaces(0.2)  # 消除参考线
                return Brep

            def RunScript(self, PolyLine, Cruve1, Vect1, Cruve2, Vect2, Rotate, RPLA, Distance):
                Distance = Distance if Distance else [-3]
                if Cruve1 and Cruve2:
                    # 生成边框延伸面
                    ud_surface = [rg.Surface.CreateExtrusion(Cruve1[cr], Vect1[0]).ToBrep() for cr in
                                  range(len(Cruve1))]
                    lr_surface = [rg.Surface.CreateExtrusion(Cruve2[cr], Vect2[0]).ToBrep() for cr in
                                  range(len(Cruve1))]

                    # 旋转面
                    for i in range(len(lr_surface)):
                        angle = math.radians(Rotate[i])
                        lr_surface[i].Rotate(angle, RPLA[i].ZAxis, RPLA[i].Origin)

                    ud_surface2 = self.Tile(lr_surface, ud_surface)

                    # 大面 集合
                    BigFace = rg.Brep.CreatePlanarBreps(PolyLine)[0]
                    for sur in lr_surface:
                        BigFace.Join(sur, 0.02, True)
                    Surface = [BigFace]
                    Surface.extend(ud_surface2)

                    # 偏移
                    Brep = self.OffUnio(Surface, Distance)
                    return Surface, Brep


        # 孔 - 圆柱
        class ZY_Cylinder(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@圆柱开孔", "RPP_Cylinder", """在指定坐标原点生成开孔圆柱""",
                                                                   "Scavenger",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d8360a85-40c8-4877-8590-048bcd679cc5")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "指定Plane，以Plane为圆弧的中心")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "圆柱半径.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "CriVec", "C", "圆弧延伸向量，决定了圆柱的长度方向.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Move", "M", "若需要生成多个，输入移动向量.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cylinder", "Cl", "切割孔--圆柱体.")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOzSURBVEhLzVZbT1NZFO5vIJHLGw+E8AOIPiBQeKNCnNECSglQMG3thRaoaDtDgYChPRlhKJQSCgZSERsvOMLUQNQKqDRSriWUQJjIIJCQISE8CAyXz7N3D9YES6LpJPMlq91rnb3Wd9bu2muVt7+/f+Ho6IhZW1tjhEIhExMTw8TFxf2wxMbGMnl5eczW1hZD4vLYD8vu7i7KysrgcDjg9Xrh8/kwNzf33UL8pqenYbfbUV5eDgLexsYGo9frMTs7Sw2hwujoKKqrq8HTarVMT08PZw4tbDYbeKmpqczk5CRnCi2Ghob8BFNTU5zJj/X1dTQ2NqK9vZ1KS0sLmpub6bqjo4N+E91qtX7Rm5qasLm5yUXwY2Rk5NsZkAd8Ph8lahVKNCqwexAVFQV1MaurFVApFThzJhwCgcC/h5Xk5GT6A3+N4eHhbxOwlYXMzExYO+7DYrNDoZDj0aOHyC+U4N5DJ66I8tD37BkKCgpwt/sx7phtyM3N5bwDCEpAIJaoUNjyNyTWv/CLoRpvXc8hkDRA5wQE4tvwvHuJ4lIdlJ3/QPSbF6riUs4zgFMJrubLcLHOB6HRC+2tXzH8oh8JOXWQsQV3PqsC798MQqLQIuf3DxBUuCG9Xsx5BnAqQU6BDJeMPmSZvLjBESSK6iB/ACRl+wmkSi1yGz8g3fB/JBCJ5fjJuAgh48NNvQHvXj9HgsiE6w4gMbsSE+5XkKnKkWP+CIHBA5lcw3kGcDpB/jX8XOFCVuULqNQleOKwIzlbD0nbCviXS/Dn0wcQX5NDVOfGBe0fkEjlnGcAQQk8Hg8iIyMgk0pRWCjGuXNnac2npPChVCqReD4B6enpiI+P/7InPDwci4uLXAQ/ghIMDg4iOjqarnd2PqG2thb9/f3o6uqiNoulGQMDA6g0GKh+sP8vIiIiMDExQfVjBCVwuVxsBpF0vbe3B51Oh76+PtoyCEwmE32J0lJ/7R8cHCAsLAwzMzNUP0ZQArfbjbS0NNTU1NAg3d3d2N7epjeX9KiioiKQGUJ6EWn1BjaTjIyMEy0/KIHT6URbWxtaW1vZ47BgdXWVCulR5LjGxsaovrKygoaGBnR2dsJsNtPnX4MSsE3tRDddWlpCVVUVPRIi5EiMRiMNRkjr6+upTuwkC/ISJAt27HIR/KDdNCkp6UQGoQKdBwqFgiGz+L8AmRO85eVlhh2bWFhY4Myhwfj4OK0+3uHhoYVMIrVajd7eXszPz1OyHxFy0cg/C3IiGo2GvUM7+Ax9rTRuGbJ7sAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def circle(self, Plane, Rad, Vec):  # 根据面生成圆柱Brep
                circle = rg.Arc(Plane, Rad, math.radians(360)).ToNurbsCurve()
                Surface = rg.Surface.CreateExtrusion(circle, Vec).ToBrep()
                Brep = ghc.CapHoles(Surface)
                return Brep

            def RunScript(self, Plane, Radius, CriVec, Move):
                if Plane and Radius and CriVec:
                    cir = self.circle(Plane, Radius, CriVec)
                    cylinder = [cir]
                    if Move:
                        for mo in Move:  # 移动生成
                            msur = ghc.Move(cir, mo).geometry
                            cylinder.append(msur)

                    return cylinder


        # 多边曲面偏移
        class BrepOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@多边曲面偏移", "RPP_BrepOffset", """根据折线生成偏移曲面。""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("96643d8a-600a-424c-a69e-2d06e29b111b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "多边曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "各分线段各自的偏移方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "精度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Brep", "B", "偏移后的Brep")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKLSURBVEhLrdVZqE1RHMfx/WBOZlESXhTJi0RmkRQPSoYUEqJbHjxIKaVEFMqcucwPPBgyRRkyZp7nzHOeCMnw/a51trbtdu7JPb/63Lv26XbWXmv91/8m1cgAtI3D8mcLTuEB+vlBOdMXz+MwmYsDcVi91MZw7MI5OMEGPMNElJz6aBOHId2xApdxFH5ZH9zGuwJXUVK64DxuYD0O4gzmoRNMLdzDOOxFD3xDZ1SZfRiNeviKgcimJpx8CprgIswCXI/D4lmE3fCN32AneiPNYSyNw2Qo3DJTA27V5PBUJHVwAY9xEh7qcfiGy7AOaaZjaxyGDMEXNAxPRWLJeYH8skl+QHzTX5gZnmKWw5VmcwTb47DyWEFeHPe3I05jJDzUwXBy99qx5ToK2bTCD1h5lcYbeS0OQ9yCn+gZnmKc8ArcjjF+kMssPIrDfzMHO+IwaQxXo3wawSJ4gm3I96OnmBGHf8cqmRCH4bZOhf3Gms+mHe7DLVkI39jzqAvjii3zFuEpk6toBg/K22v88vwqesGbnKY1NsMKTM9lP+6gW3giFfiMTQXZ3MWwOAxxbAF4Id1KS9PfrvgDXPVZ2A3cymQEvKGegZOMxzTMxnw8xFvsgffD7bFa/LKPBe/hVt3CK/i35pg/VsFbbJzRSaygjVgDJ/6E1bDZ2Z/Woj+6wpJ2m2wl7rs78B2eo5MlHeDMcmk2PL/Y+5BmMVbGYXg7W0U+Y+G+W1lObEn/6cxN4eGZBrA1vCj8diL/H/g2LXEIvnUaO6pncgmD/KDUtIfNz7q2kbkCe5MT2b6d2OrxPtib/jv+gzmBl3iNJXA7PXwrxdIuS1xBetNvwtIua5rDXuVeWyG29yqSJL8B+BWf/dyaRkoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def polyhedral(self, obj, set_line, vector, distance, acc):
                surface = []
                if len(vector) == 1:
                    surface = [rg.Surface.CreateExtrusion(set_line[i], vector[0]) for i in range(len(set_line))]
                elif len(vector) > 1 and len(set_line) == len(vector):
                    surface = [rg.Surface.CreateExtrusion(set_line[i], vector[i]) for i in range(len(set_line))]
                for i in surface:
                    obj.Join(i.ToBrep(), acc, True)
                return obj

            def offset(self, obj, distance, acc):
                distance = 10 if distance is None else distance
                new_obj = rg.Brep.CreateOffsetBrep(obj, distance, True, True, acc)[0][0]
                return new_obj

            def RunScript(self, Brep, Distance, Vector, Tolerance):
                Tolerance = 0.02 if Tolerance is None else Tolerance
                if Brep:
                    Line_list = [_.EdgeCurve for _ in Brep.Edges]
                    origin_data = self.polyhedral(Brep, Line_list, Vector, Distance, Tolerance) if Vector else self.offset(Brep, Distance, Tolerance)
                    New_Brep = origin_data
                    New_Brep.MergeCoplanarFaces(0.02, True)
                    return New_Brep


        # 截面实体
        class SectionBody(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@截面体", "RPP_SectionBody", """原截面成实体（已删除），Loft（EX版，可放样面或者线），时间效率达到最高""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3f99dcdb-d937-4272-b283-88d68a08c8bc")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Breps", "B", "N N一组的数据，可为线或面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Options", "O", "放样的类型")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Cap", "C", "是否封盖")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Breps", "B", "获得的Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGRSURBVEhLrda/K0ZRHMfx60d+RkoMDCSFUFKUUTblH2CwKCkjJYvssjAohZIJGZTBaJDFyiJKBspvheTX+3Pv863bk9Q9537qVc/5PnW+9zndc84TJEg5BjGHWfQhtWiyS/zgDt+Zz7sog1ea8AZNOKQCacEHVFtRwSeL0ERH4ShKO1STRxTAOfvQRBfIU4HU4wGq7yEXzlmCPe0GbLIGDKA0HHmkA7becoA2pJppWAN5xThSSTdO8I54E1mF1/o34ilDy9IL2w9mGzlwyg40yUg4ilINq5tJJI4msmXRk2dnHtbgCkVIFO1gm2BdhT+iPaDvdXTUqZAkJbiGNZlBdvqh77TpdBgmzhSsgeiXVMAyBtXXwpFD9HZsId7kDD3ohPbDDWrgHDVZRrzJF7S7j9GKVDKKF8QbTSDV6B44hDX4hM4qr1RiGM3hKDr74xttAc7Jhz2xrsoqKIU4h+o6KpxTjGfY0+qisdhFpD8AXrEL5xY6PvRW6W5W7R618Ip29CY0oV5NLZU+n6IL/yQIfgGnWH75rtlR4QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.op = None
                self.c_factor = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _do_main(self, group_curve):
                if all([isinstance(_, (rg.Brep)) for _ in group_curve]) is True:
                    w_set_breps = [group_curve[0], group_curve[-1]]

                    temp_curves = map(lambda x: [_ for _ in x.Edges], group_curve)
                    join_curves = ghp.run(lambda y: rg.Curve.JoinCurves(y), temp_curves)
                    eval_list = ['join_curves[{}]'.format(_) for _ in range(len(join_curves))]
                    eval_str = ','.join(eval_list)
                    zip_curves = eval("zip({})".format(eval_str))

                    loft_cr_to_brep = list(ghp.run(self._loft_curve, zip_curves))
                    set_breps = w_set_breps + loft_cr_to_brep
                    join_breps = rg.Brep.JoinBreps(set_breps, sc.doc.ModelAbsoluteTolerance)
                    return join_breps
                elif all([isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve, rg.Line)) for _ in group_curve]) is True:
                    res_loft_brep = self._loft_curve(group_curve)
                    return [res_loft_brep] if res_loft_brep is not list else res_loft_brep
                else:
                    return False

            def _loft_curve(self, curves):
                create_brep = ghc.Loft(curves, ghc.LoftOptions(False, False, 0, 0, self.op))
                return create_brep

            def RunScript(self, Breps, Options, Cap):
                try:
                    self.op = 0 if Options is None else Options
                    self.c_factor = 'T' if Cap is None else Cap.upper()
                    if self.op == 4:
                        self.message2("Developable放样类型已过时！插件自动转换为Normal放样类型！")
                        self.op = 0

                    if self.c_factor not in ['T', 'F']:
                        self.message2("封盖请输入T或者F！")

                    origin_tree = [list(_) for _ in Breps.Branches]
                    if len(origin_tree) == 0:
                        self.message2("B端Brep组不能为空！")
                    else:
                        w_filter_list = ghp.run(self._do_main, origin_tree)
                        w_cap_breps = [_ for _ in w_filter_list if _ is not False]
                        [self.message1("第{}组数据类型有错误！".format(_ + 1)) for _ in range(len(w_filter_list)) if w_filter_list[_] not in w_cap_breps]

                        Result_Breps = w_cap_breps if self.c_factor == 'F' else ghp.run(lambda b: [ghc.CapHoles(_) for _ in b], w_cap_breps)
                        return ght.list_to_tree(Result_Breps)
                finally:
                    self.Message = 'Loft（面或线）-> 原截面实体（已删除）'


        # Bre切割
        class BrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@Brep切割（优化实用性）", "RPP_BrepCut", """Brep切割优化数据（时间效率最高）""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("66f1cb77-2cff-45f4-80a5-f1170e324852")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "A_Brep", "A", "待切割的Brep（被切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "切割的Brep（切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差，默认0.01")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Breps", "B", "切割出来的Brep集合")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Disjoint", "D", "不相交的切割体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "False_Breps", "F", "切割失败的切割体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG+SURBVEhLxdVLK0VRGMbxTSJSbt/C/X6/E7kbSJhJikx8AQMyYqIw8RlEQrmU20QxMBIDt7HPoPg/i3XOOkcHm12e+nV6d533rL3X2u/x/iOl6EexqX6eBGQgHclIRESysI9Xxw70he9SiQscYAO32EIo8TiCmi6iD0sf9S6+Sh0e0Ggqz+vCE/SjoZRBzRZMFc4KdD3PVJ+j5o8oN5Xn1eMORaZyMgg1ajBVOB3Q9R5TRSa6eRO08hJTRUUbqkZ6LG7WoOs5pgrHV3MlDntQs2UMwTbXRrvx3dxGp2Ubamppg09RCEXP+FfN3eSjHdmmem9yjnFc40/NY2UaLygwVcDNa6GXyB69GtwgkOZ6Ae8xaar3x6O9GTFVQNGpOcYYTjAF3VEgd2AzCq1cx1dphk6TBqPvaGxomtoVVkArnsAlbFPNHl8/ommqaei+B5quZ6iColFyBXuatOFuHTNfTdNDuJnDM3qh/4D5j1p3rZe1Dfq+PpNgYqepmrtZha7badoC1dZsVD0TVVfD5KfTNAXdGEAnMmFX3IqYd+B3mvqOO031WIZhm28ikKRB/6Nqaq0jFYEmF+40/UM87w2FQn0odJBCcwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _is_not_intersect(self, tuple_data):
                a_breps, b_breps = tuple_data
                _disjoint = []
                for single_brep in a_breps:
                    count = 0
                    if single_brep:
                        while len(b_breps) > count:
                            if b_breps[count]:
                                interse_sets = rg.Intersect.Intersection.BrepBrep(single_brep, b_breps[count], sc.doc.ModelAbsoluteTolerance)
                                if len(interse_sets[1]) == 0 and len(interse_sets[2]) == 0:
                                    _disjoint.append(count)
                            count += 1
                _intersect_indexs = [_ for _ in range(len(b_breps)) if _ not in _disjoint]
                return _disjoint, _intersect_indexs

            def _first_handle(self, w_cut_breps):
                passive_body, cut_body = w_cut_breps
                if cut_body:
                    mb_res_brep = rg.Brep.CreateBooleanDifference(passive_body, cut_body, self.tol)
                    if mb_res_brep is not None:
                        res_breps = tuple(mb_res_brep)
                    else:
                        res_breps = cut_body
                    return res_breps
                else:
                    return False

            def RunScript(self, A_Brep, B_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = 0.01 if Tolerance is None else Tolerance

                    Res_Breps, Disjoint, False_Breps = (ghdt[object]() for _ in range(3))
                    _a_trunk, _b_trunk = [list(_) for _ in A_Brep.Branches], [list(_) for _ in B_Brep.Branches]
                    if len(_a_trunk) == 0 and len(_b_trunk) == 0:
                        self.message2("A、B端不能为空！")
                    elif len(_a_trunk) == 0:
                        self.message2("A端不能为空！")
                    elif len(_b_trunk) == 0:
                        self.message2("B端不能为空！")
                    else:
                        _w_handle_tree = list(zip(_a_trunk, _b_trunk))
                        _after_handle_indexs = map(self._is_not_intersect, _w_handle_tree)

                        _no_inter_indexs, _inter_indexs = zip(*_after_handle_indexs)

                        _no_inter_breps, _inter_breps = [], []
                        for _n_index in range(len(_no_inter_indexs)):
                            _no_inter_breps.append([_b_trunk[_n_index][_] for _ in _no_inter_indexs[_n_index]])
                            if len(_no_inter_indexs[_n_index]) != 0:
                                [self.message2("A端第{}个Brep集合与B端第{}个Brep不相交".format(_n_index + 1, _ + 1)) for _ in _no_inter_indexs[_n_index]]
                        for _t_index in range(len(_inter_indexs)):
                            _inter_breps.append([_b_trunk[_t_index][_] for _ in _inter_indexs[_t_index]])

                        _true_result, _temp_fail_result = [], []
                        _true_handle_tree = ghp.run(self._first_handle, zip(_a_trunk, _inter_breps))
                        for _ in range(len(_true_handle_tree)):
                            if isinstance(_true_handle_tree[_], (bool)) is True:
                                _temp_fail_result.append([])
                            elif isinstance(_true_handle_tree[_], (list)) is True:
                                self.message1("A端第{}Brep集合与B端第{}Brep集合切割失败，已初始化数据".format(_ + 1, _ + 1))
                                _temp_fail_result.append(_true_handle_tree[_])
                            elif isinstance(_true_handle_tree[_], (tuple)) is True:
                                _true_result.append(_true_handle_tree[_])

                        Res_Breps = ght.list_to_tree(_true_result) if len(list(chain(*_true_result))) != 0 else Res_Breps
                        Disjoint = ght.list_to_tree(_no_inter_breps) if len(list(chain(*_no_inter_breps))) != 0 else Disjoint
                        False_Breps = ght.list_to_tree(_temp_fail_result) if len(list(chain(*_temp_fail_result))) != 0 else False_Breps
                        return Res_Breps, Disjoint, False_Breps

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Breps, Disjoint, False_Breps
                finally:
                    self.Message = 'Brep切割'


        # 分割Brep（面）
        class SplitBrepFace(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@分割Brep（面）", "RPP_SplitBrepFace", """面或实体切割，分割面或者实体（类似小刀平切面饼）""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3c6041a2-9374-4045-98cb-6d3c8fb9e166")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "待分割的Brep（面）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "分割体（平面（Plane）或者平滑的面（Surface））")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "分割的精度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Cap", "C", "是否封盖，默认封盖")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Result_Brep", "B", "分割出来的Brep（面）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEwSURBVEhL7dXNK0RhFMfxu5NJbGa8xRBREhtr/42FJquZaVZS2NmOUoqUhY2FhZ2Vl1BGLPwDdrZesiK+v9OQuke5i1Oz8KtPtzM9zTkz93nuTVoxHc1rSMp4QMmqgGzhA3WrAjKJV4xYFZBxPGPQqoBM4AVDVmVIFw5xizvHFVagyZ/QgzXoc2/9DQ6Qg6UbunnrqDmOcY4+PCIPDXMEb/0m3qDBLWqg/3bUqnSqUIN+qEEBmnIeXqahX5pqMGNVOks4w88G16jAyyy07r9BCzb47RGgL8qyi6aQ2kU6B9tYdlzAOwc6H976Xbzju0En9nGJhuMEiyhCk/ViFafw1mugPbQjU76eRcNWBWQMulcDVgVEN0/vAzUKyQ60GTasCsgC7jFnVVDamtc/JEk+AUDucEMk06pwAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _get_cutface(self, wait_brep, knife):
                wait_brep = [wait_brep] if type(wait_brep) is not list else wait_brep
                cut_k = knife[0]

                new_brep_list = []
                for single_brep in wait_brep:
                    temp_one = single_brep.Trim(cut_k, self.tol)
                    new_one = temp_one[0] if temp_one else single_brep
                    new_brep_list.append(new_one)
                    cut_k.Flip()
                    temp_two = single_brep.Trim(cut_k, self.tol)
                    new_two = temp_two[0] if temp_two else single_brep
                    new_brep_list.append(new_two)
                knife.remove(cut_k)
                if len(knife) > 0:
                    return self._get_cutface(new_brep_list, knife)
                else:
                    return new_brep_list

            def _cull_geo(self, geo_list):
                total, times, no_need_index = 0, 0, []
                while len(geo_list) > total:
                    sub_index = []
                    for _ in range(len(geo_list)):
                        if geo_list[times].IsDuplicate(geo_list[_], sc.doc.ModelAbsoluteTolerance) is True:
                            sub_index.append(_)
                    if sub_index not in no_need_index:
                        no_need_index.append(sub_index)
                        total += len(sub_index)
                    times += 1
                just_need = [geo_list[_[0]] for _ in no_need_index]
                return just_need

            def _handle_brep(self, brep):
                cap_brep = brep.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance)
                cap_brep = cap_brep if cap_brep is not None else brep
                if cap_brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                    cap_brep.Flip()
                return cap_brep

            def RunScript(self, Brep, Plane, Tolerance, Cap):
                try:
                    self.tol = Tolerance if Tolerance is not None else 0.001
                    self.cap_factor = 'T' if Cap is None else Cap
                    self.cap_factor = self.cap_factor.upper()
                    if self.cap_factor not in ['T', 'F']:
                        self.message2('封盖请输入T或者F')
                        self.cap_factor = 'T'

                    if Brep is None and len(Plane) == 0:
                        self.message2("B端实体未输入！")
                        self.message2("P端平面未输入！")
                    elif Brep is None:
                        self.message2("B端实体未输入！")
                    elif len(Plane) == 0:
                        self.message2("P端平面未输入！")
                    else:
                        origin_brep = self._get_cutface(Brep, Plane)
                        cull_brep = self._cull_geo(origin_brep)
                        Result_Brep = cull_brep if self.cap_factor != 'T' else map(self._handle_brep, cull_brep)
                        self.message3("{}个实体被切出".format(len(Result_Brep)))
                        return Result_Brep
                finally:
                    self.Message = '平切Brep（面）'


        # 删除重复的Brep
        class CullBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@删除重合Brep", "RPP_CullDuplicateBrep", """将重合的Brep删除""", "Scavenger",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("59be0dc6-d5e7-408b-b267-dcd2757ca933")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "待删除的Brep集合")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "公差（影响不大）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep_Result", "B", "删除后的brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "I", "被删除Brep的原下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJKSURBVEhL3ZXLbxJRFMb5G0l52piUhcbUR6OJpjU+qokbF7Uj7ylYMDhoaKu2CQsbozYtUGgHyit9gREYdNtF4+7znMsk1jAgDSyMi1+Ge8853zf3cO8d09PVij2+dxqUPzdHjkK6ptmEGko2gTeln1AKpyOD9ZINwGSeS0kzy0fwrh8jsqUhkmojvKlhYaMF+UtzYDif6yKp70LH8+EI00uHMDnlijQe/QanO43rL7KYTRTwLLkP/8c6whsNLG62sKgbC7b0J8HzHA9RHufPUd1Dqmcd1mNdkzNQlFyv23DKVVh8RYy5d2B/vo2L3gwuBTO4Gs7iVjSH27FdTL9SMaOo4snjmzTPcc7jfJt7W9SzDuu54m3dIK7hglzusFAhqnDIFdgCZVj9RVi8exjz5An1DHkxz3HOc5Ag14l6XculaAYGPeFCNtcRY6O835zT4Pz8Gwbj1Nf+9G7VQAZ27y5snp0e5ODw5SnP2KS/Ab2Zw1+ARUoLEyPYhONDGTh8Kv2uwspblrAHO9uXDqhokY32fVetzmArIIFJ5RCPV+t48K6Gu8vHePS+jssROivBMhnkumt1BjIwSzncWfmKRO4HonRNSOsNBD41MfmyCjutZGgDXsGV2AHur9QwFT/Avbc1XIvtU6tKIm9oA/4zud8Wf4l6X6KroURv3hFnbO7sn3Vn+KuBM0j30HwKVilDu8WA+bSIcW5XPdHfYGCGPGjD8J8YmN2qNEFfHqOEYZlQ6Iv2ZEkN3Vg7oYEmHF1KawRoQm9q7QS/AB8xaSY73/UrAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Breps, Tolerance):
                try:
                    if Breps:
                        Tolerance = 0.001 if Tolerance is None else Tolerance
                        total, count, no_need_index = 0, 0, []
                        while len(Breps) > total:
                            flatten_list = list(chain(*no_need_index))
                            if count not in flatten_list:
                                sub_index = []
                                for _ in range(len(Breps)):
                                    if Breps[count].IsDuplicate(Breps[_], Tolerance) is True:
                                        sub_index.append(_)
                                    # if sub_index not in no_need_index:
                                    no_need_index.append(sub_index)
                                    total += len(sub_index)
                            count += 1

                        need_index = [_[0] for _ in no_need_index]
                        Brep_Result = [Breps[_] for _ in need_index]

                        # index_list = [_ for _ in list(chain(*no_need_index)) if _ not in need_index]
                        return Brep_Result, ght.list_to_tree(no_need_index)
                    else:
                        self.message2("Brep列表不能为空！")
                finally:
                    self.Message = '删除重合Brep'


        # 修复Brep
        class Fix_Brep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP@Brep修复", "RPP_Fix_Brep", """修复损坏的面，不成功时爆红，有开放的Brep（Open Brep爆黄），修复成功会有提示（注：此程序不能适用所有模型和情况，请合理使用）""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("2cfd67f4-3e79-4d44-ae86-db7635385f16")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Breps", "B", "待修复的Brep集合")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Toggle", "T", "Open Brep修复替换的开关")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Fail_Brep", "F", "未修复或无效 Brep集")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJOSURBVEhLldVJyE1hHMfxY0xShmQoyYIQJQtFKEVKZKWwJCUiY0KZliRTGSKJMmRjY0o2yoKULEiiZE4WhLAwfb/Pvf+35973nnvv+6tP3f9znvM855z7nOcUdZmIkZWfbacbRmMqettQlnH4gucYbEOLOPBGPME/XEDpBGPwFnbUQwxCWfriFqL/TfREw0zAR0Tn8AAD0CgXEf3uog9KUzaB7mEE8sxAHH+MgWgZ/6Q3yAcP65DnOGx/ivrJm2Ys3iMf/CemIM8deOxSqprHlVWTRo/rHZw84jO3/TuG2FCS4fhU+VkbZ92PVYhJXmEUzClE+wobGqQ/HsE+TbMeMZjLeBgWZW0+ru7I44qKx/jZhlbZhpjAR3K7WodnuIrdmI5jiGO+iG1lM4ZiDfLBwy+8hlccbWfQpUzGX+QD/4HLNV99L7EWXYpXn28lcmA3x0nwv5qHaWj6VjeKJ9xHPvhl9MJSfIWbZL6U204PXEc++EGYw7BeidibZqJl/B7MxxxcQT74Xph9iLbtNhBXkvWsVJVkB34jTs6dhFkCa6887mIXzA1Yz05VXZbBg77eXuH5aq1riCyEq+lIqoriNOwTdxLfibmpqsa30RfGzS3/s/bAzm4beZzE9qOpKopzsN6Sqsqd/ID7UUo/uKbdP/KMhyeeSFVtFsNjh1JV+WTGxXj1/l6AFFeLL8g3dMxKNsGOW1PVOcvhcR+pOQvr+B/9znTEt8/GF3APOVCtnbTZhyXO2wmXqb+1Gp3i7UYHfYDLtVW8w/y8DSBF8R+3g9QoHwAebAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.switch = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _filter_bad_surf(self, brep):
                faces_list = ghc.DeconstructBrep(brep)['faces']
                invalid_srfs = [_ for _ in faces_list if _.IsValid is False]
                valid_srfs = [_ for _ in faces_list if _ not in invalid_srfs]
                bad_breps = map(lambda x: gk.Types.GH_Surface(x), invalid_srfs)
                return bad_breps, valid_srfs

            def _copy_trim(self, data):
                target_sur = gk.Types.GH_Surface(ghc.Untrim(data))
                res_surfs = ghc.CopyTrim(data, target_sur)
                return res_surfs

            def _fix_surfs(self, srf):
                return map(self._copy_trim, srf)

            def _join_breps(self, brep_list):
                t_join_brep = ghc.BrepJoin(brep_list)['breps']
                join_brep = t_join_brep if isinstance(t_join_brep, (list)) is True else [t_join_brep]
                t_union_breps = list(rg.Brep.CreateBooleanUnion(join_brep, sc.doc.ModelAbsoluteTolerance))
                union_breps = [None] if len(t_union_breps) > 1 or all([_.IsValid for _ in t_union_breps]) is False else t_union_breps
                return union_breps

            def _replace_obj(self, tuple_data):
                time.sleep(0.01)
                bad_srf_id, fix_brep = tuple_data
                if fix_brep is None:
                    return bad_srf_id
                else:
                    if fix_brep.IsSolid is True:
                        res = sc.doc.Objects.Replace(bad_srf_id, fix_brep)
                        return res
                    else:
                        if self.switch == 'F':
                            return fix_brep
                        else:
                            sc.doc.Objects.Replace(bad_srf_id, fix_brep)
                            return "第{}个Open Brep替换成功！"

            def RunScript(self, Breps, Toggle):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    self.switch = 'F' if Toggle is None else Toggle.upper()
                    if self.switch not in ['F', 'T']:
                        self.message2("请输入‘f’，‘t’以开启关闭电池！")
                    else:
                        if Breps:
                            _turn_to_breps = map(lambda x: Rhino.DocObjects.ObjRef(x).Geometry(), Breps)
                            _invalid_breps = [_ for _ in _turn_to_breps if _.IsValid is False]
                            _set_breps = ghp.run(self._filter_bad_surf, _invalid_breps)
                            if _set_breps is not None:
                                _invalid_surfs, _natural_data = zip(*_set_breps)
                                _fix_breps = list(ghp.run(self._fix_surfs, _invalid_surfs))
                                _pack_data = map(lambda data: list(chain(*data)), zip(_fix_breps, _natural_data))
                                _join_breps = list(chain(*list(ghp.run(self._join_breps, _pack_data))))

                                _zip_list = zip(Breps, _join_breps)
                                Fail_Brep = []
                                _bool_list = map(self._replace_obj, _zip_list)
                                for _ in range(len(_bool_list)):
                                    if isinstance(_bool_list[_], (System.Guid)) is True:
                                        Fail_Brep.append(_bool_list[_])
                                        self.message1("第{}个Brep修复失败，请重新检查！".format(_ + 1))
                                    elif _bool_list[_] is True:
                                        self.message3("第{}个Brep已修复！".format(_ + 1))
                                    elif isinstance(_bool_list[_], (rg.Brep)) is True:
                                        Fail_Brep.append(_bool_list[_])
                                        self.message2("第{}个Brep为开放的Brep（Open Brep），输入‘t’以替换".format(_ + 1))
                                    elif isinstance(_bool_list[_], (str)) is True:
                                        self.message3(_bool_list[_].format(_ + 1))
                                return Fail_Brep
                            else:
                                self.message3("输入的模型中未损坏！")
                        else:
                            self.message2("模型列表数据不能为空！")
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'Brep修复'

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Brep_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYE_Niko"

    def get_Id(self):
        return System.Guid("c0301aca-1ba0-4fd4-a08f-2887f6fe702a")
