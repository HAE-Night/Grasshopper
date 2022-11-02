# -*- ecoding: utf-8 -*-
# @ModuleName: 001
# @Author: invincible
# @Time: 2022/7/8 11:02

# coding=utf-8

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import Grasshopper.DataTree as ghdt
import ghpythonlib.parallel as ghpara
import Grasshopper.Kernel.Data.GH_Path as ghpath
import ghpythonlib.components as ghcomp
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
from functools import reduce
import math
import Line_group

Result = Line_group.decryption()

try:
    if Result is True:
        # 合并以及封面
        class Seam_Merge(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@封面合并", "MyComponent", """封面以及合并曲面""", "Hero",
                                                                   "Brep")
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
                                                                   "Niko@映射及挤出", "Niko_Mapping&Extrusion", """映射一个物体到指定平面，之后通过线段或者向量来挤出实体""", "Hero", "Brep")
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


        # Brep切割
        class Brep_Diff(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZY_Brep实差切割", "Brep_Bool", """Brep的实差切割体..""",
                                                                   "Hero",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8258170c-1c5b-4391-9389-b2b67aae0f42")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "A_Brep", "A", "第一组Brep物品")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "第二组Brep物品")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "PRE", "P", "精度[0.00-1.00]，当切割失败时，调动。其他情况勿动")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "B", "差集切割物体")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMRSURBVEhLrZXZTxNRFIcHJUERJPFJE41LjL76aGKCb5q6Rv8lo8HEBQXXYBDrQjTGuKQt7cydGdrOTKellm6zVGOAxGhbUOOLbYGfZwoo0CIIPHyZSZP5fb33nnMPV6lUXJUpdJQqU+uOk8tl7JEuesH495/rzuQ0wOkJoyOfz8M0TVimAdsy14yTYxKFQh5cLGmRoADLsmBaNtJZC8l0Fqm0sSqSaROGlavmFQqFGYHz4qwgY49BkDX4eYaAIK0KHy9BH7arf3ZWYFQFlp0DL0cgiQL0iAZdj8w8FxHVNQzKEkSR1UGsfu8XZGRoJ4rF+QIyykEFr996cPnKTVy93oVrnd2L6MKVztt45xkgiVwNrIVBEB2BWStQtCgeuvtxuP0Yduzah5279y9kzwFsbtuO+z0PoalqnfBlBGE1iqf9L+A6dQ4cx9VhI7gNm/Cgt29tguMnztYJ/8vdnl4oJOAZq0GURDDpPwUNGxrRfuQozrhO4rTrDN68fI24GoEmBxcQDYXBAiIGeBFZY05AjbacoHlLK3KRIUx/+oiylcW3eAzFaATjMf0PE0NRfKUqe3SDisDHwzDnqmglguYtyARDKCd1lONh/KpDJaGiGBLQfeEiPH62tOCZc8inz4NraCToUInmljakB4OopKIov1dQqsPksIYJRcSdSx1LC5wy7XvyHHsPHkJjU2uVjU0t2LptO9K0gjULnEbzeAeoDN3ocz/9y+N+jCaGUUpomKagqTogreOHJv1bIMphSBKDqioLUBQVY4kkvgwyjIcYiuFaJhQJo4IPtxafgXNdzxcwJixoHIlwGsf/ygOf2w3f4ydLMkC47/XC6xfrCwIsVCNwYISfF6iRxGURJbpVmUTX/mwfzBeEoynwdFVLJJGo5ecj09atBEHgwYI6sqaNIuWSIFMVGAZNoQ8jiA2b8PJBeAIyvIHBFeNx8MuQ1TiyuRHaIlrBnGBuojnt7QyKjGEhlTH/H5oBJk0zg3L+TLQZQb76gz1Lzl49tgNlzAhoJsdTdldpEvj8dXzdKU0CvwFtCDTndcE1nQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def tree_value(self, tree, number):  # 取树形数据的指定项
                try:
                    return tree.Branch(number)
                except Exception as id:
                    if tree.BranchCount == 1:
                        return tree.Branch(0)
                    elif tree.BranchCount > 0:
                        num = number + 1 % tree.BranchCount
                        return tree.Branch(num)
                    else:
                        return None

            def boolD(self, list):  # Brep切割
                A = list[0]
                B = list[1]
                PRE = list[2]
                diff = rg.Brep.CreateBooleanDifference(A, B, PRE)
                return diff

            def RunScript(self, A_Brep, B_Brep, PRE):
                Brep = ghdt[Rhino.Geometry.Brep]()  # 定义初始化
                clist = []
                PRE = 0.02 if not PRE else PRE
                if A_Brep.BranchCount > 0:
                    for i in range(A_Brep.BranchCount):
                        lt = [A_Brep.Branch(i), self.tree_value(B_Brep, i), PRE]
                        clist.append(lt)

                    res = ghpara.run(self.boolD, clist, True)  # 多线程运行

                    branch = 0
                    for i in range(len(res)):
                        if A_Brep.BranchCount == 1:
                            Brep.AddRange([res[i]], ghpath(branch))
                        else:
                            Brep.AddRange([res[i]], ghpath(branch))
                            if len(res) / A_Brep.BranchCount * (branch + 1) == i + 1:
                                branch += 1
                    return Brep


        # Brep结合
        class Brep_Union(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZY_Brep结合", "Brep_Union", """将多个Brep结合成一个.并消除参考线""",
                                                                   "Hero",
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
                    res = ghpara.run(self.brepbp, breplist)
                    Brep = ghdt[rg.Brep]()
                    for i in range(len(res)):
                        Brep.AddRange([res[i]], ghpath(i))
                    return Brep


        # Brep炸开
        class Brep_Data(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZY_炸开Brep", "Brep_Data",
                                                                   """将Brep炸开，获取点线面。中心点坐标系，Brep的ID""",
                                                                   "Hero", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d4bc9a70-0c2d-4646-82d9-c38c58c9ffff")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Brep", "B", "Brep模型.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Index", "I", "中心点坐标系下标-根据Brep点序输入；"
                                                 "默认[0, 1, 0, 3].")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "PT", "顶点.")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Line", "LE", "边线.")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Face", "FE", "面.")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "PE", "中心点坐标系.")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "GUID", "ID", "Brep的ID.")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKmSURBVEhLzVbfS1phGD43wXYzlpbWHLtLdiH9BSHdbzD6E7zZTQtBImoUJAsvPrVkohANDJQlVv4A+7E5lErJ0Qz8wUrLEVPqIijxpkjw2fnejC2G1NZh7IHnnI/3e9/znO877/t+R6jVas/q9TqrVCqsv7+f9fT0MK1Wy3p7e/+YPI7HDw4OsrOzM8afK4gXx/n5OYaGhjA7O4t4PI7N5GeRyd+5uXkjNzY2MDMzg5GREXAIh4eHbHh4GJlMhgxSYXt7G2NjYxB0Oh1bXFy8tNaqCDgNeP3yOcZfvcD4QIPimNvm7QPARYVcV1dXMT093ZQ7Ozvwer0Quru7WaFQoKCv624oH7agtV2FduV1yhQqtD1oQfrTO/Ll2xEIBJpyd3cX2WwWgkajYcVikYISITsedcjR1aWGWn2dXSI7FXLE5q3kexvwbaIV7O/vkyEZduJxZ3MBlVKOdb+NfG+D/1+gXC7DbrfD4XDA6XRicnISW1tbjVkJBNxuN2XK0dERkae60WhszEogMDExgYODA+RyOSTFQuQFa7X+TII7CbhcLng8HhovLCxQF6hWq9IJRCIRTE1NQexl4IXKBSUV4LDZbOBFenp6CrHlkM1isdCd484C/M3NZjNisRjW1tbg8/lgMpkasxII8I+6srKCYDCIUChEgjybrnBngZvw7wUSwbdQtrc2FVC0yRD1mcn3NkilUpcCV930e3oJmif3IZPJ0CF2zl8pl8vwVHUP374EyJfXwOjoaFNGo1HKMGrXVyvgKCZ9WHKN44P7DT56GhTHSy4jCon3oked/EqlEh0qzXh8fIx0Og2hr6+PLS8vU5DUmJubgyA2KGYwGKgzSol8Pg/x7wL0V8GXq9frEQ6H6ajje/c33Nvbo+3x+/30vJOTE/wAhPiD+YvdyqwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Count(self, num1, num2):  # reduce调用+方法
                return num1 + num2

            def Point(self, PTS):  # 点坐标信息
                for pt in PTS:
                    yield pt.Location  # 惰性生成

            def Cenpoint(self, PTS, indexs):  # 中心点 坐标平面
                PTS = self.Point(PTS)
                PT1, PT2, PT3, PT4 = next(PTS), next(PTS), next(PTS), next(PTS)

                coord = [reduce(self.Count, [PT1[cr], PT2[cr], PT3[cr], PT4[cr]]) / 4 for cr in range(3)]  # 重点坐标
                Center_Point = rg.Point3d(coord[0], coord[1], coord[2])
                PTlist = [PT1, PT2, PT3, PT4]

                PLA_pt = [PTlist[pt2] for pt2 in indexs] if indexs else [PTlist[pt2] for pt2 in
                                                                         [0, 1, 0, 3]]  # Plane点排序
                Plane = rg.Plane(Center_Point, PLA_pt[1] - PLA_pt[0], PLA_pt[3] - PLA_pt[2])  # 点- 两组向量做plane

                return Plane

            def Module(self, Brep):  # 面 边线
                Linelist = Brep.Edges
                Facelist = [i.DuplicateSurface() for i in Brep.Faces]
                return Linelist, Facelist

            def RunScript(self, Brep, Index):
                if Brep:
                    sc.doc = Rhino.RhinoDoc
                    GUID = str(Brep)
                    Brep = Rhino.DocObjects.ObjRef(Brep).Brep()
                    Point = Brep.Vertices

                    Plane = self.Cenpoint(Point, Index)
                    Line, Face = self.Module(Brep)

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return (Point, Line, Face, Plane, GUID)


        # ZY_压顶板实体
        class ZY_YDB(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZY_压顶板实体", "MyComponent", """压顶板实体插件：
            适用：直线压顶板。接口处需要延伸出一个接口。""", "Hero", "Brep")
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

                    Surface3 = ghcomp.Extrude(Curve1, Vec1)
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
                    Breps2 = ghcomp.BrepJoin(Breps).breps  # 结合
                    Brep = ghpara.run(self.Brep_Bool, [Breps2])
                    # return outputs if you have them; here I try it for you:
                    return Surface1, Breps, Brep


        # 圆弧铝板实体
        class ArcPanel(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZY_圆弧面实体", "ArcPanel", """圆弧铝板实体生成，参数较多，不易调试查看，
        请将所有参数连接查看效果""", "Hero", "Brep")
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
                    cenpt = ghcomp.IsPlanar(Q_surface[i], True).plane  # 引用内置IsPlanar电池提取中心PLA
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
                                                                   "ZY_圆柱开孔", "ZY_Cylinder", """在指定坐标原点生成开孔圆柱""",
                                                                   "Hero",
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
                Brep = ghcomp.CapHoles(Surface)
                return Brep

            def RunScript(self, Plane, Radius, CriVec, Move):
                if Plane and Radius and CriVec:
                    cir = self.circle(Plane, Radius, CriVec)
                    cylinder = [cir]
                    if Move:
                        for mo in Move:  # 移动生成
                            msur = ghcomp.Move(cir, mo).geometry
                            cylinder.append(msur)

                    return cylinder


        # 多边曲面偏移
        class BrepOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@多边曲面偏移", "Niko_BrepOffset", """根据折线生成偏移曲面。""", "Hero", "Brep")
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
                                                                   "Niko@截面体", "Niko_SectionBody", """截面成实体， N N一组的同数据截面进行放样，放样类型有{1: 'Normal', 2: 'Loose', 3: 'Tight', 4: 'Straight', 5: 'Uniform'}，输入对应的数字即可；当一组数据只有一个的时候，可以通过轨道线来sweep截面""", "Hero",
                                                                   "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3f99dcdb-d937-4272-b283-88d68a08c8bc")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Object", "O", "N N一组的数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "轨道线")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Style", "S", "放样的类型")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "精度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Brep", "B", "最后闭合的Brep")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGRSURBVEhLrda/K0ZRHMfx60d+RkoMDCSFUFKUUTblH2CwKCkjJYvssjAohZIJGZTBaJDFyiJKBspvheTX+3Pv863bk9Q9537qVc/5PnW+9zndc84TJEg5BjGHWfQhtWiyS/zgDt+Zz7sog1ea8AZNOKQCacEHVFtRwSeL0ERH4ShKO1STRxTAOfvQRBfIU4HU4wGq7yEXzlmCPe0GbLIGDKA0HHmkA7becoA2pJppWAN5xThSSTdO8I54E1mF1/o34ilDy9IL2w9mGzlwyg40yUg4ilINq5tJJI4msmXRk2dnHtbgCkVIFO1gm2BdhT+iPaDvdXTUqZAkJbiGNZlBdvqh77TpdBgmzhSsgeiXVMAyBtXXwpFD9HZsId7kDD3ohPbDDWrgHDVZRrzJF7S7j9GKVDKKF8QbTSDV6B44hDX4hM4qr1RiGM3hKDr74xttAc7Jhz2xrsoqKIU4h+o6KpxTjGfY0+qisdhFpD8AXrEL5xY6PvRW6W5W7R618Ip29CY0oV5NLZU+n6IL/yQIfgGnWH75rtlR4QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor_dict = {1: 'Normal', 2: 'Loose', 3: 'Tight', 4: 'Straight', 5: 'Uniform'}

            def along(self, obj1, curve, acc):
                edge_list = [[_ for _ in single.Edges] for single in obj1][0]
                all_brep = [rg.Brep.CreateFromSweep(curve, index, False, acc)[0] for index in edge_list]
                return all_brep

            def explode(self, obj2, send_style):
                if all(isinstance(_, rg.Brep) for _ in obj2) is True:
                    result_list = [[_ for _ in single.Edges] for single in obj2]
                    eval_list = ['result_list[{}]'.format(_) for _ in range(len(result_list))]
                    eval_str = ','.join(eval_list)
                    dict_data = eval('zip({})'.format(eval_str))
                    result_brep = self.loft(dict_data, send_style)
                    return result_brep
                else:
                    brep_list = [_.ToBrep() for _ in obj2]
                    return self.explode(brep_list, send_style)

            def curve_loft(self, obj3, style_num, acc):
                rebulit_brep = eval('rg.Brep.CreateFromLoft(obj3, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.{}, False)[0]'.format(self.factor_dict[style_num]))
                cap_brep = rebulit_brep.CapPlanarHoles(acc)
                return cap_brep

            def loft(self, list_data, style_num):
                brep = [eval('rg.Brep.CreateFromLoft(_, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, False)[0]'.format(self.factor_dict[style_num])) for _ in list_data]
                return brep

            def RunScript(self, Object, Curve, Style, Tolerance):
                Tolerance = 0.01 if Tolerance is None else Tolerance
                Style = 1 if Style is None else Style
                if Object:
                    length = len(Object)
                    Brep = None
                    if length <= 1:
                        if Curve:
                            list_of_brep = self.along(Object, Curve, Tolerance)
                            sweep_brep = list(rg.Brep.JoinBreps(list_of_brep, Tolerance))
                            cap_brep = [_.CapPlanarHoles(Tolerance) for _ in sweep_brep]
                            Brep = cap_brep
                        else:
                            pass
                    else:
                        if all(isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Line)) for _ in Object) is True:
                            Re_Brep = self.curve_loft(Object, Style, Tolerance)
                            Brep = Re_Brep
                        else:
                            Re_Brep = self.explode(Object, Style)
                            list_brep = [Object[0], Object[-1]]
                            for _ in Re_Brep:
                                list_brep.append(_)
                            Brep = rg.Brep.JoinBreps(list_brep, Tolerance)[0]
                    return Brep


        # Bre切割
        class BrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@Brep切割（优化实用性）", "Niko_BrepCut", """Brep切割（优化版）,优化实用性，牺牲部分时间效率；注意当有Brep切割失败时，可以开启二次处理开关，此时插件的时间效率会大大降低，但会输出失败的Brep切割成功的部分""", "Hero", "Brep")
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
                self.SetUpParam(p, "A_Brep", "A", "待切割的Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "切割体Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差，部分切割失败时可调整")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Switch", "S", "二次处理的开关，默认为关（1：开）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Succ_Brep", "B", "成功切割的Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "False_Brpe", "F", "切割失败的Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "False_Sub_B", "f", "切割失败的切割体Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Secondary_Brep", "Sec", "False_Brpe的二次处理，输出成功的部分")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Secondary_Fasle_Brep", "S-f", "二次处理后，剩余的切割失败的切割体Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Tip_Fail_Brep", "I", "二次处理提示信息（第i次切割失败）")
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
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)
                        self.marshal.SetOutput(result[4], DA, 4, True)
                        self.marshal.SetOutput(result[5], DA, 5, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG+SURBVEhLxdVLK0VRGMbxTSJSbt/C/X6/E7kbSJhJikx8AQMyYqIw8RlEQrmU20QxMBIDt7HPoPg/i3XOOkcHm12e+nV6d533rL3X2u/x/iOl6EexqX6eBGQgHclIRESysI9Xxw70he9SiQscYAO32EIo8TiCmi6iD0sf9S6+Sh0e0Ggqz+vCE/SjoZRBzRZMFc4KdD3PVJ+j5o8oN5Xn1eMORaZyMgg1ajBVOB3Q9R5TRSa6eRO08hJTRUUbqkZ6LG7WoOs5pgrHV3MlDntQs2UMwTbXRrvx3dxGp2Ubamppg09RCEXP+FfN3eSjHdmmem9yjnFc40/NY2UaLygwVcDNa6GXyB69GtwgkOZ6Ae8xaar3x6O9GTFVQNGpOcYYTjAF3VEgd2AzCq1cx1dphk6TBqPvaGxomtoVVkArnsAlbFPNHl8/ommqaei+B5quZ6iColFyBXuatOFuHTNfTdNDuJnDM3qh/4D5j1p3rZe1Dfq+PpNgYqepmrtZha7badoC1dZsVD0TVVfD5KfTNAXdGEAnMmFX3IqYd+B3mvqOO031WIZhm28ikKRB/6Nqaq0jFYEmF+40/UM87w2FQn0odJBCcwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            Tol, Factor = 0, None

            def _second_handle(self, cut_brep):
                passive_body, cutting_body = cut_brep[0], cut_brep[1]
                res_brep = rg.Brep.CreateBooleanDifference(passive_body, cutting_body, self.Tol)
                final_brpe = [_ for _ in res_brep] if res_brep is not None else "此Brep切割失败，请检查数据类型！"
                return final_brpe

            def _third_handle(self, brep_data):
                data_one, data_two = brep_data[0], brep_data[1]
                final_brep, sec_fail_index, tip_times = [], [], []
                for single_brep in data_one:
                    count = 0
                    while len(data_two) > count:
                        temp_brep = single_brep
                        change_brep = rg.Brep.CreateBooleanDifference(single_brep, data_two[count], self.Tol)
                        if len(change_brep) != 0:
                            single_brep = change_brep[0]
                        else:
                            single_brep = temp_brep
                            sec_fail_index.append(count)
                            tip_times.append(count + 1)
                        count += 1
                    final_brep.append(single_brep)
                return final_brep, sec_fail_index, tip_times

            def RunScript(self, A_Brep, B_Brep, Tolerance, Switch):
                self.Tol = 0.001 if Tolerance is None else Tolerance
                self.Factor = False if Switch is None else True

                a_leaf_list = [list(_) for _ in A_Brep.Branches]
                b_leaf_list = [list(_) for _ in B_Brep.Branches]
                a_len = len(a_leaf_list)
                b_len = len(b_leaf_list)

                if a_len != 0 and b_len != 0:
                    _first_handle_of_a = map(lambda x: [_ for _ in rg.Brep.CreateBooleanUnion(x, 0.001)], a_leaf_list)
                    _first_handle = list(zip(_first_handle_of_a, b_leaf_list))

                    if len(_first_handle) == len(_first_handle_of_a) == b_len:
                        result = [_ for _ in ghp.run(self._second_handle, _first_handle)]

                        fail_index_list = [_ for _ in range(len(result)) if type(result[_]) is str]
                        success_index_list = [_ for _ in range(len(result)) if _ not in fail_index_list]

                        succ_res = [result[_] for _ in success_index_list]
                        fail_a_leaf = [a_leaf_list[_] for _ in fail_index_list]
                        fail_b_leaf = [b_leaf_list[_] for _ in fail_index_list]

                        Succ_Brep = ght.list_to_tree(succ_res)
                        False_Brpe = ght.list_to_tree(fail_a_leaf)
                        False_Sub_B = ght.list_to_tree(fail_b_leaf)

                        if self.Factor is True:
                            union_a_f = map(lambda x: [_ for _ in rg.Brep.CreateBooleanUnion(x, 0.001)], fail_a_leaf)
                            _secondary_brep_zip = list(zip(union_a_f, fail_b_leaf))
                            _secondary_brep_array = [_ for _ in ghp.run(self._third_handle, _secondary_brep_zip)]

                            _sec_brep_brep_list = [_[0] for _ in _secondary_brep_array]
                            _sec_fail_brep_index = [_[1] for _ in _secondary_brep_array]
                            tips_of_strs_list = [_[2] for _ in _secondary_brep_array]
                            _sec_brep_sub_list = map(lambda x, y: [y[index] for index in x], _sec_fail_brep_index, fail_b_leaf)

                            tips_of_strs = map(lambda x: ["第{}次切割不成功".format("、".join([str(_) for _ in x]))], tips_of_strs_list)
                            Secondary_Brep, Secondary_Fasle_Brep, Tip_Fail_Brep = ght.list_to_tree(_sec_brep_brep_list), ght.list_to_tree(_sec_brep_sub_list), ght.list_to_tree(tips_of_strs)
                        else:
                            Secondary_Brep, Secondary_Fasle_Brep, Tip_Fail_Brep = None, None, None

                        return Succ_Brep, False_Brpe, False_Sub_B, Secondary_Brep, Secondary_Fasle_Brep, Tip_Fail_Brep

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
