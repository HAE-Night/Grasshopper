# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/11/5 16:34

import Rhino
import System
import scriptcontext as sc
import Rhino.RhinoDoc as rd
import Grasshopper, GhPython
from Rhino.DocObjects import *
import rhinoscriptsyntax as rs
from Grasshopper import DataTree  # 树形
import System.Drawing.Color as cor  # 颜色库
import ghpythonlib.parallel as ghpara  # 多进程
from ghpythonlib import treehelpers as ght  # 数列互转
from Grasshopper.Kernel.Data import GH_Path  # 树形分支
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
import time
import re
from itertools import chain
import csv
import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 获取数据详细信息
        class Data_message(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@获取数据详情", "HAE_Data_message", """Get Data Details.""", "Hero",
                                                                   "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a946c7ad-a18f-471c-a9e7-038677fce6a4")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Group", "G", "Information results")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJmSURBVEhLtVZPSzpRFJ2dBn6EzO+gGPYFJEVpabSJ/tEfRENwI1i5EGuyNEgXbZRaCWm4KdRCRVA0UHBhfoYIFNoUYae5w/sNTJZW+jtwdM513ju+d9+9M9zb25vl/f09SIzH48G1tbXg6uqq+P1b0rj19fVgIpEQ5yNywkcEAgKBAI6OjpBOp3F9ff1nXl1dYX9/H6FQiKYF1+v1eAHiD+NELBZDNBoFF4lEeLr4Hzg8PARntVr5crnMQuMFbRk3OzvL12o1FupHs9nExcUFzs/P+0jxdrvN7uxHNpsFZzKZ+Gq1ykJy0D9QKpVQq9WYmpqSUaPRYHJyEiqVCt/tQCaTGWxgsViwsrLC1NeYm5vD8vIyU3IMNTCbzfD5fBCOMl5eXvD6+iqRNGFrawuLi4vi9Wf8aAVUH6VSCQ6HA06nUyJpys/29jaWlpbYCDl+ZLC7u4unpyc0Gg3U63WJpLvdLjY3N0czoLOcSqVgMBgwMzMjkXSxWITb7R7NYGdnB51OB61WCw8PDxJJPz8/Y2NjYzSDg4MD5HI5zM/PY2FhQSLp+/t7uFyu0XPw+PgIuocK8h9J08qG5oAqedgKqCJtNlsfyWjoCgYZUB1QDgZB6P+D62CQgbB9sNvtTH0NWsmfDS4vL6FQKKDT6aDX62Wcnp6GVqvFxMQE7u7u2Ag5RAOj0Tiwm1IVh8Nh8Qn1mScnJ+JJ+g5SN61UKiw0Xtzc3IDz+/382dkZC40Xx8fH4IRq5L1eL25vb1l4PEgmk2Kj5IS2K75VeDwenJ6eilVbKBSQz+d/TRpH+0752dvbE2YFPgDn94A0immrtQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Objects):
                if Objects:
                    Group = Objects.TopologyDescription
                    return Group


        # 物件键值对提取
        class Data_KV(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@提取键值对", "HAE_Data_KV",
                                                                   """Extract the key value pair of the object, when there is no value input for the Key. Extract all key value pairs.""", "Hero",
                                                                   "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("af5ef186-5ae8-4eab-a2e8-42b171fa942a")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Object", "O", "Object Collection List")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "The key to be extracted supports multi key query")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "KS", "Extracted key; When the key has no value, it extracts all keys. On the contrary, only Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Value", "VS", "Extracted Key")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALaSURBVEhLtZbBSxtBFMYXL1ZRqIbERulFiaDgSYIELVQToqX0YFsNJfageJGCOcSqTUwaY7IJ29pSNOIfIIIgCNJLESlK0YPY0ksPeggEqUcxYklU/LrvOaltkaVL4w9edt+8ee+bnZmdjXR6enr//PxcIUskEkpLS4vS1GRVbLYm9arPrFYr51OdXE1J/UlAZWjIi+5uF16GQpBjMcTicUQmJjA6OoKRkX83j8eD9vZ2vhIkoATGxnDnrh3D/jAi8UnEXr1DMBzH+w8fuZNeDg8P0dXVxYLS3NycQiN/5hmGwVAOk9HIZii/iQrzbXz++k2k6SOTyaCjowOS0+FQIhEZwy+CqDAZUVtbK8wCc2UVPm1uiRT98BPYbDZl8s1bPPeFUFx8A1WVZjbzLRPKDUZsbn0R3fUTCAQgNTc3K7IcRTL1HQ9dT9H5+Akeudy496AToehr/MhkRXf9jKlrywKkdB2wAE1RMBgUTflFU2B9fR2Li4vCA6anp7G0tCQ8YG1tDeoOFB6QSqUwNTXFWzSHpkBfXx8sFgvf9/f3Q5IkLC8vs0/Mz89z297eHvterxeFhYVIp9PsE5oCg4ODaG1tRTQaRVFREVZWVkTkgmw2i9LSUszMzLBfU1PDOb+jKeD3+1FSUsKjbGhoEK1/4na74XA4eHoKCgqwsbEhIhdoCvh8Pk6iEZaVlUGWZRG5ZHV1FSaTiaezrq4O6sEpIhdoCgwMDKC+vp7vZ2dn+Ul2dnbYz0EFq6urORZSD8m/0RSgIK2Behiy39jYCJfLdeUo6Qm3t7dFyyWaAsfHx9jf3/8lQIfX7u4uTk5O2M9BgrSTzs7ORMslmgL5gAXoS3StAurcKlctUD6ggUtOp1Oht/A6oLrSwsKCYrfbcXBwIJrzA9WjuvxNHh8fR1tbG5LJpAj/H1SH6tHUS0dHR/yvIhwO877v6enhN7O3t1e3UR7lUx2qBwA/AdFfSvBR19pyAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def NoneKey(self, Object):  # 提取对象键值对
                Key, num1 = [], 0

                for i in Object:  # 获取key值
                    Key.append(rs.GetUserText(i))

                Keys, Value = DataTree[str](), DataTree[str]()
                for ke in range(len(Key)):  # 获取Value
                    for k in range(len(Key[ke])):
                        Keys.Add(Key[ke][k], GH_Path(num1, k))

                        Value.Add(rs.GetUserText(Object[ke], Key[ke][k]), GH_Path(num1, k))
                    num1 += 1
                return Keys, Value

            def HaveKey(self, Object, Key):
                num1 = 0
                Keys, Value = DataTree[str](), DataTree[str]()
                for ke in Key:
                    Keys.Add(ke, GH_Path(num1))
                    for i in range(len(Object)):
                        Value.Add(rs.GetUserText(Object[i], ke), GH_Path(num1, i))
                    num1 += 1
                return Keys, Value

            def RunScript(self, Object, Key):
                if Object and Key:
                    Keys, Value = self.HaveKey(Object, Key)
                else:
                    Keys, Value = self.NoneKey(Object)
                return Keys, Value


        # 键值对赋值
        class DATAKEY(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@赋值键值对", "HAE_DATAKEY",
                                                                   """Assign f to the key value pairs of objects. When assigning multiple objects, pay attention to the key value pair order and data structure;""", "Hero",
                                                                   "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4b68c580-a4e4-4ca8-9e49-082b8f014c0b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Objects", "O", "Object Collection List")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "K", "Key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Values", "V", "Value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQUSURBVEhLrZVdTJNnFMdbFOMWswxxi0MWl2WJyzYudrVkN9vFFiIZy5Il+8CbuQsNuMQFgbYU+gmlfQvFUtqC0NZ+sFSkiDh12uIHMj4ECS0MRFCgRXCgwFg7Wdz23/O8nZWuVUzk4p8+fc/p88v5n/Oeclytpt0Wm44x1DLrLnovx3RUp9Ub9FAxqnUXvZdTb6lWMAwDsVi87qL3RgFEYtG6KS6gWFSEomLhY0XjEqkobmy1aI5YsgpA/aKBc1e0GJqywnvTBu84+Vwt8mxg3IwWjwTXRuvhuxUnh2gk0ABPjxoiSQEYtQqcOlMYIBQK4Rt3YSZ0DJNLNkwtOaI0E3LC3S2H3cXH/MpZTCxaY3L8yw2YWLChxr4fRaJD0YBCoQC+sRaS2IDxewZM/2HGzQVj5Dz3lxUWVw5MP/AwF3Lj1mINAiETxu4aWAVCdbh934z+CTXkmq8hlvJiAd7RFtwOOjE6p8fFfgVuzNdi9k8bOZeia1gN55lcmJ083F1pQ+ewCp1DDPy/m1h1jzDovVGB4VkdFNo9jwfMP2jChWsyJCVvwfVZI35sF4HD4eBo00GcvMRjAUF0QsJ8hR2pyZgOWUh1dux6KwVFii/ZqtYEtPXJkPzSC7g6Wo5XUrbi86z3sQAXHK0HWcDyP5fh7pEiYUMCfh5SYihQjeee34TzXTLW1jUBF/vlePW1bfjw43ewPSWJ9MCCXx/YIwBqkT9Yh5TUJFRb9sF5uiCcR6r5ZeYpLLriU2Bj4gbWGlrJoF9HbHBEALTJ9+DAZ1+8h6y9H+C7vE+QnvkuqbIRvoA2DkAVDWj3loKbwEWJZg/xNhV7sz/CIprhOPkIMP+3HTrTPux8/WW8+fYOMPpvCMAZCzhiqooB0B68uHULAkEzyo3fgsPlkMky4vi58BRRgD9oQu9YBRI3bQSXyyVTxrA2PhXA0yvB5s2J6BurxNSyibUrJ3c3TncIIgDaTHrhG7u2I3XnNnacA0HL2oA7K41k/vVodgvIS1ZLLnGw03GmQxT1Hkz+dgSzKza09crhuSpjATP3rWyTSw/HAdBVMTjeCu+kEV0jCgxOH0b3dSV5oRTwTlVi5E4V6o/th61JiOmlU+gYkrOxgSkNiWvYc8+oEpcGZCiryloFqA8D6Ir1dFXiVDsfzR4eTrT9X3w0/vQ9jp/l4UJfGVzu/Jgc+rvWywJYT2RDJM17BGDXNVmvJUo+GI0QqgoqQYxoTFnOQ5maT77Hz6HPGU0hWdnF4XX9ECCRSNg9XiwqJNUICbDoCXpS/L/Ywz8ci7VGQf3PyMiATCZDeno6cnNz2TNNehZFAPkF+cj8NBN5eXlIS0tDzoFsyEvWCVBn1mp1Oh2kMimUKiWxScI2XF2uZpv0LDIY9fgXDacNWwRC6S4AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Objects, Keys, Values):
                sc.doc = Rhino.RhinoDoc.ActiveDoc
                if Objects:
                    rs.SetUserText(Objects, Keys, Values)
                ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                sc.doc = ghdoc
                return


        # 拷贝模型
        class Bake(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@烘焙物体", "HAE_Bake",
                                                                   """Bake objects when Bake is True. The layer and other information are optional.""", "Hero",
                                                                   "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("09c16def-05d1-47b3-9db1-bf444ba5f240")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometrys", "GT", "Objects to be baked")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "LayerName", "LN", "Bake Layer Name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "NA", "Assignment of model name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "ObjKey", "OK", "Key Value Pair Key Value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "ObjValue", "OV", "Key Value Pair Value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Color", "CR", "colour")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Bake", "BK", "True to bake, otherwise not run")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "result", "RS", "Output prompt on success")
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
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAM6SURBVEhLrVZLS1tBFJ5C20W71YU/oYsug4i2C5eSQLpwW3XRVam4UHzgYyEqXoMPNOJGfGDdCi5KUUsWFVxEwYKgiNBKTPow5mUeN6/79ZzJpElMYmPrBxPOOXfm++aeOXNuRDKZNBuGYePR2dlpq6mpsVVVVdmqq6vvPHgdr2eeLKegHzsILS0tMJvNGBgYwMjIyD8PXs88ra2tTAsW0Nrb29HW1oZEIiGD/wvmYT7mFYuLi1pTUxMoVerx/YD5mFc0NjZqPT09Klwe4XAYJycnODg4wP7+ftFwOp04Pz9XszNgXlFXV6cNDQ2pUDEuLi4wMzMj87uwsICVlRWsrq4WDY53dXUVpJnPQ9TX12uDg4MqVAiHw4Hu7m7s7u6qyO2Ym5tDNBpVHtDf319eYG9vT+5A13UVAQyDDpCOSi9TC/ymsVhMeUqAU3RTIBAIoK+vD5FIRPrhWBzewCe4LztpWOHxvkQo7JTP8lGxwPr6OnZ2dqQdiXlxGXiOwPUjpNMCBgRFBX75X9HbpOWcLCoSSKfTGB8fRzwel74v9FESM2n+0OMC15GvZOdQkQBXzfz8vLSTKQM/rt5Q7osFQpGHuAqekp1DRQJHR0ey7BjhaAhR/QlZheSG8QDxhIAv+IH8HCoSOD4+xvLysrT1RIpy/YKsQgE9/hj+kEAw/Jn8HKampgo6QkkBr9crd8KI01z/tYmsQgFO2bfvr+mQc2R+vx/T09PKy6CkAGNiYgI+nw9pqvtf/nd0FjnyFB14JCaoqr7IuVnwZeTqy0dZga2tLaytrUk7Qim99FvoQJ+SoKCSfUZ34T1SVAD5GB0dhcvlUl4GZQVSqRS4P52eZqpEp/5yFXThp+8tAmGHjOVjY2MDS0tLystBCtTW1hYJMDweD+jLJKsqi8I9Z7C5uYnh4WG5qZuQAiaTqWw3dbvdsh9xFz07O/tTIdzQuG2PjY0VVU4+ZDdtaGjQent7Vag0tre3MTk5KW84F4CmabDb7Tg8PFQzSoN5hc1m0ywWiwrdDk5D/kX6G5hXUM/R+IPf0dGhwvcD5mNeQf1e/quwWq1obm4GvZH8cMzOzt558DpezzzMBwC/AR/JdU9zQ6YsAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def tree_value(self, tree, number):  # 树形数据提取
                try:
                    return tree.Branch(number)  # 提取分支
                except Exception as id:
                    if tree.BranchCount == 1:
                        return tree.Branch(0)
                    elif tree.BranchCount > 0:
                        num = number + 1 % tree.BranchCount
                        return tree.Branch(num)
                    else:
                        return None

            def Baket_bute(self, listc):
                butes = Rhino.DocObjects.ObjectAttributes()  # 属性样式内容定义
                butes.Name = listc[1][0] if listc[1] else None
                Key = listc[2] if listc[2] else None
                Value = listc[3] if listc[3] else None
                butes.ObjectColor = listc[4][0] if listc[4] else cor.Black
                for i in range(len(Key)):
                    butes.SetUserString(Key[i], Value[i])
                Gs = sc.doc.Objects.Add(listc[0][0], butes)
                return Gs

            def RunScript(self, Geometrys, LayerName, Name, ObjKey, ObjValue, Color, Bake):
                if Bake:
                    sc.doc = rd.ActiveDoc
                    BaCs = []

                    for i in range(Geometrys.BranchCount):
                        Geometry = self.tree_value(Geometrys, i)
                        name = self.tree_value(Name, i)
                        Objkey = self.tree_value(ObjKey, i)
                        Objvalue = self.tree_value(ObjValue, i)
                        color = self.tree_value(Color, i)
                        BaCs.append([Geometry, name, Objkey, Objvalue, color])
                    GS = ghpara.run(self.Baket_bute, BaCs)

                    for i in range(len(GS)):
                        LayerNames = rs.LayerNames()
                        Layername = self.tree_value(LayerName, i)[0]
                        if Layername:
                            if Layername not in LayerNames:
                                newlayer = rs.AddLayer(Layername)
                        else:
                            Layername = sc.doc.Layers.CurrentLayer.Name
                        rs.ObjectLayer(GS[i], Layername)
                    result = "Baked successfully!!!" + time.ctime().split(" ")[3]
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return result


        # 拾取图层物体
        class PickItems(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@犀牛图层拾取", "HAE_PickItems", """Pick the object of rhinoceros sub layer""", "Hero", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1947d440-6dc8-4eb7-8338-c936a5f54a4b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Father_Keys", "K", "Subscript of parent layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Unique_ID", "U", "Unique identification")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Switch", "S", "Plug in run button, input't 'to execute, default to not execute")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Data", "D", "Picked Items")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Info", "I", "Pick information for layers")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJNSURBVEhLzdXfa09xHMfxj99hmCJtWIsoU27Ijwtbm5UfNb8mUkuROz+SCCG5k2T/gVwoLTQpsrTtbtSauFNucUUuhMTi+fwcn2w5zvf7HRde9eh73ufH53w+53zO5xv+t0zHXEyL1T/KTJzEc3zFd3zBUxzFX91sM97BRntwGgdxFn1w/2s0oeLsgg08wmJ35GQZBuB5G91RbmzQi27FKksHuvAAN2EHUhydj60mVmXERt5icqyyGz3ETqzCbvTjOswMfMKNWJVILez9kViFcAm3s83fYs/PZJvhArxudqwKkp79Ajgth+BMyouPZBAT0QCva0VhnJLfss2wGveyzT/GR7cUTldvcACFOYZhjMcK2EBRelEHR+kN9qEwTjdPdApOgB/UEuRlJR5nm2EdvG5NrApiT3xEV2KVDdmveE6sfmU+XqA9ViFcwwdMiVWJdMLeOHRzCo7kMg7jKp7hEIyj9fzzsSojVXiFl3BxM4vgjWz8BJxlZiHewNGU1fsUe+U69B573ZGT/fgMO1PvjkpjL+/D4d+FM8vYU2eP++8gjXLM2Q4b68Y8pJW0ogWuVLbARj/+/G3EmDMOfv5T4QuvhtkBX3xaDlx3PO55fjNelxsPuERvQDP8o9mKbbDRNizHyFh73BXWc7UJLbADo166vXiC43A1vQhP3ANv6qI2C5NgZ1zGrT3XRr2JnToHP0BXVpfzUdPW4fq5+/fn8/WZe7E9cwSp9sX6a+1+j9u49Xp4/VrYgZLxudrb9C5cRrzQ3/TsPe55OQnhB3JubI7cUR5DAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def find_true(self, str_list):
                fix_data = [len(_) for _ in str_list]
                index_of_need = (fix_data.index(min(fix_data)))
                return str_list[index_of_need]

            def eliminate_illegal_data(self, list_data):
                result_list = []
                for choice in list_data[1]:
                    result = [_ for _ in list_data[0] if choice in _]
                    length = len(result)
                    if length == 1:
                        re_result_str = result[0]
                        result_list.append(re_result_str)
                    elif length > 1:
                        re_result_str = self.find_true(result)
                        result_list.append(re_result_str)
                    else:
                        pass
                return result_list

            def _get_rhino_objects(self, uid):
                object = Rhino.DocObjects.ObjRef(uid[0]).Brep()
                return object

            def RunScript(self, Father_Keys, Unique_ID, Switch):
                Switch = 'f' if Switch is None else 't'
                self.factor = False if Switch == 'f' else True
                if self.factor is True:
                    if Unique_ID:
                        duplicate_rm = list(set(Unique_ID))
                        sc.doc = rd.ActiveDoc
                        all_layers = rs.LayerNames()
                        children_layers = [_ for _ in all_layers if "::" in _]
                        father_layers = [_ for _ in all_layers if "::" not in _]
                        Father_Keys = Father_Keys if len(Father_Keys) > 0 else [_ for _ in range(len(father_layers))]
                        value_data = []
                        for f in father_layers:
                            re = [_ for _ in children_layers if f in _]
                            value_data.append(re)
                        result_children_layers = [[value_data[_], duplicate_rm] for _ in Father_Keys]
                        result = [_ for _ in ghpara.run(self.eliminate_illegal_data, result_children_layers)]
                        name_of_list = [name for names in result for name in names]
                        Info = name_of_list
                        Data_list = []
                        for _ in name_of_list:
                            if _ in all_layers:
                                Data_list.append(rs.ObjectsByLayer(_, True))
                        sc.doc = Rhino.RhinoDoc
                        Data = [_ for _ in ghpara.run(self._get_rhino_objects, Data_list)]
                        return Data, Info
                    else:
                        pass
                else:
                    pass


        # 获取文件路径
        class ActiveFile(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@获取某些数据", "HAE_ActiveFile", """Get rhinoceros, Gh file path and current time""", "Hero", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a7f1dc8c-0093-4c72-8c53-bfde0f8d0365")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "x", "U", "Button for updating time")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "RP", "RP", "Rhino file path")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GP", "GP", "Gh file path")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Time", "T", "Current time (time to open Gh)")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATsSURBVEhLlVZbT1RnFB0f2vjStOkP6EOf+9Dn9qUPrYkhrZEWGx+AtoKiDnKZOzAMiNYophWjiDYEK2pFYC5nYIByOTNz5sIdhpvFCrVSqIhFasutga7u/XFGRi4hXcnOzJw531rft/de+xzNTjA1333d3C7tsYTcRqPfcckclEoNiqPEFHRmWEL17x/uvvqKeuv/g1mpeTunve6COeSetPY0oWCgFTaOyNon/87tbIAl7B41B93WrMaqN9WlO8MUcGbldNT/WTgoI6e9HkbFCdr95qDrOZ0eFAy2ge7/1eh3fqZSbItdhoDzeuGwlxfA6LNvSWyiyPLWIL3tLnS+WhjovrzuRuT3NdMah1Xl2gy68fuie36Ygi5BZOlw0y43k2fI1TgZ9iAwOYbH888xPvcUtqAbtDkUDsnQyzVmlXIdhraajJMjXkGefLoYCel5OFZZviYWI8I7LwzXY3ZxHgL/AteUJmS0VEFPJ9GRiLW3CWbF+aFKTTlXpLfMAWkhl/JJ6ohPNSEuPp1Ci9TSy7B01b0Q0LZWITw1LrgXl5dwUa7DEc8N6Ok/k9+J890tyKF0GfyOn21yxW4hQKm5yEej/IFaEl+VfIO4T9Px8YFMxKeYYJBrYQ5JIte8S04LwzPSiy/dFdDTCbkefU8m8NPsNH2vEoUnvkMayttrtHBGdAvvglKio+MetBViX1I24vZrkVR0TtSDugsniGjs2RMhEKYaHG65LciD9J3RNz1Bp7xDafqRNxTWGBXXR9znsa1oCrig91Yj7dYVJGTnYe8nx5F85jyyAnbkBiVMPZ8TZIzhp1MYm5tRfwEVvX4hSIZkrn801IoW2wAdRyWPFeF0ZTbexOd6Kz7Yk4KU4guYWFgn3whldBDahptrTUHBG9cQ2SV250YBDioUzGEJae7rSMw/hZHBByoVsEqh3B9BgEg5yrweHHVRPWLWM6+GKl8WK7DRRCeo53NDbjz6e3aNWcXQUBsO1V7FF/ZypNq/wzE6qZFqFOVZF/A5SqICG000+decMNG02jVRTA43YkbWoaunFNkBN/W+BNMW48QWaYHG4Hdm8fDiC5tMtAGrZKoImWjGa8By5AzQfwodnZeR6XMhmzwQS86CPD6oyI732GB8IdZEKysrkPraId+LEDFnHAiOjyLxxrdQ2s4Cg19joY9FirYUofHObTqvsQ0NvWrw2h/yVOScP1texCqRs0OT7NeQWF2G/t9+EQJdvz/EUXJ6mlQJfyuLnH5JREcC0SLn9zdTk9gb15ys2PMKyMns1PE/psVsOdJQCT0bi/zwQDVW7/QjaMmlOoU6i0QUFhlQRSJFkDrKofVR/1M2bP0t7Pp9QsAmO96gvn3MOTPV3UJ60+0X9g+pKWNETcTNIERc6yfBYBE8wSs47pVEcQ2+2pAG2CUEGHpv7X5xLNq13m8XNYmQS6N4yUQkEBXRuitxp64Yds9ZGOjUlq5Gfsot6eTad1TqdejlaquY5+Tic+1N6Bm/v62JoiIGxUXprEJq/Q8wdzTAypO0tTpBpdwMHh08qCztdUghA3FsZaLY4LGy9tj0zOu89gMq1fYweu17qauG+NGZT8Xilot96IigFPJ1TisXlF4QvHrZ8a5KsTOSKyp2Uy5T6a1CoR0u8eBix4u3CyoiN4QlJM3RSd0WxRWvLtsAjeY/RdWqVSmQw40AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = True

            def format_time(self):
                time_array = time.time()
                local_time = time.localtime(time_array)
                date = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
                return date

            def RunScript(self, Updatetime):

                if Updatetime:
                    self.factor = True if Updatetime is True else False
                else:
                    self.factor = True
                if self.factor is True:
                    Rhino_File = Rhino.RhinoDoc.ActiveDoc.Path
                    Grashhoper_File = Grasshopper.Instances.DocumentServer.Document[0].FilePath

                    RP = Rhino_File
                    GP = Grashhoper_File
                    Time = self.format_time()
                    self.factor = False
                    return RP, GP, Time


        # 提取指定图层的物体
        class ExtractObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@提取图层物体", "HAE_ExtractObject", """Extract layer information and get the object of the specified layer""", "Hero", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6bb12637-cbd6-4ae1-8cd2-4904a15d7b41")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "LayerName", "L", "Layer Full Name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Layer_Type", "T", "By default, take all objects on the layer, and enter numbers to select {0: all objects, 1: parent layer objects, 2: child layer objects}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Geo_Type", "GT", "Specifies the type of object to select for output, {0: geometric object (default), 1: point, 2: face, 3: line, 4: Brep}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "Extracted data (Rhino real objects)")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGJSURBVEhL7dTJK0VhHMbxlzJkKEqGkqmsTKWk7CxY2FHKioWUMkR22LJRVgiJDEtDkSFjMo9l49/h+5xzz+ae9w7dexYWnvp0f+977z3vub/33Nf8tWSgzy2DTxpu8YN9TQSZTDzhDFeh13MEkix8YQE5uIOyixukOKMEU4RvLDsjY0rxgVRnZMwe7pHrjBJIA6bc0kkF3qHN9jKJErdMPrYFAs3/AjFTiU8kvEAeit3SmnLoMU13RvbkI+I1RrDhlhGjNkWLrrHulv6MY9MtTQEa0YYOtKIGOjaiRdfYdkt/hqEFlqDjQefPNS6gY+EF2oMHHEK/dhG64xMcYw7eP9+XUWyhHoWasETzzeiB7nYaE+iGfqHmIrZ5DOFv6phWW7zzJ1aG4LXZF2+TB3GER+i5l1foJD3APNTOLrSjE7rzmZBVWKMFtEH6ci+aUIUyVKMFmp/FDtT3S5xCrfVatgZr1MuIq8eZAWhxa/rxBm1yXZxqw8bq/wqsyYY+8JwEtSvWnzGoGPMLn8hXlhxAzR8AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.which = {0: rg.GeometryBase, 1: rg.Point3d, 2: rg.Surface, 3: [rg.Curve, rg.Line, rg.PolyCurve, rg.Polyline, rg.PolylineCurve], 4: rg.Brep}

            def filter_layers(self, name):
                layers = rs.LayerNames()
                all_layer = [_ for _ in layers if name in _]
                father_layer = [_ for _ in layers if name in _ and "::" not in _]
                children_layer = [_ for _ in layers if name in _ and "::" in _]
                res_list_name = [all_layer, father_layer, children_layer]
                return res_list_name

            def choice(self, layer_list):
                array_data = [rs.ObjectsByLayer(_) for _ in layer_list if len(_) != 0]
                list_data = list(chain.from_iterable(array_data))
                return list_data

            def ids_to_objects(self, id_list):
                objects = [rs.coercegeometry(_) for _ in id_list]
                return objects

            def RunScript(self, LayerName, Layer_Type, Geo_Type):
                if LayerName:
                    Layer_Type = 0 if Layer_Type is None else Layer_Type
                    Geo_Type = self.which[0] if Geo_Type is None else self.which[Geo_Type]
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    res_layer = self.filter_layers(LayerName)[Layer_Type]
                    rhino_ids = self.choice(res_layer)
                    Bulk_Geo = map(lambda x: rs.coercegeometry(x), rhino_ids)
                    Geo = Bulk_Geo if Geo_Type is rg.GeometryBase else [_ for _ in Bulk_Geo if type(_) is Geo_Type or type(_) in Geo_Type]
                    return Geo
                else:
                    pass


        # 图层重命名
        class LayerRename(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@图层重命名", "HAE_LayerRename", """To rename a layer, you need to import the csv file data, and the layer will be renamed automatically""", "Hero", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("de0947cf-9bb8-447c-a485-a72a4d80f6ea")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Button", "B", "Turn on translation button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "CSV_Flie", "F", "Csv file path")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.data_csv = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def read_csv_flie(self, flie_path):
                ch_str = []
                en_str = []
                with open(flie_path, 'r') as f:
                    reader_text = csv.reader(f)
                    header = next(reader_text)
                    for line in reader_text:
                        ch_str.append(line[0])
                        en_str.append(line[1])
                return dict(zip(ch_str, en_str))

            def find_have_ch(self, layer_names):
                temp_list_data = [re.findall("[\u4e00-\u9fa5]+", _) for _ in layer_names]
                index_list = [_ for _ in range(len(temp_list_data)) if len(temp_list_data[_]) != 0]
                result = [layer_names[_] for _ in index_list]
                return result

            def replace_layer(self, origin_data):
                word = origin_data[0]
                replace_str = origin_data[1]
                old_word = []
                for _ in word:
                    if _ not in self.data_csv.keys():
                        self.message2("The translation of '{}' does not exist in the csv file database".format(_))
                    else:
                        old_word.append(_)
                replace_str = self.iter_char(replace_str, old_word)
                return replace_str

            def iter_char(self, origin_str, word):
                new_char = origin_str.replace(word[0], self.data_csv[word[0]], 1)
                word.pop(0)
                if len(word) != 0:
                    return self.iter_char(new_char, word)
                else:
                    return new_char

            def replace_layers(self, tuple_data):
                old_layer_name, new_layer_name = tuple_data[0], tuple_data[1]
                format_char = old_layer_name.replace("::", "->")
                new_char = [_ for _ in new_layer_name.split("::")]
                if rs.IsLayer(old_layer_name) is True:
                    if "::" not in old_layer_name:
                        rs.RenameLayer(old_layer_name, new_char[0])
                    else:
                        rs.RenameLayer(old_layer_name, new_char[-1])
                    self.message3("{} layer has been renamed to {}".format(format_char, new_char[-1]))
                else:
                    self.message1("{} layer name does not exist!!!".format(format_char))

            def RunScript(self, Button, CSV_Flie):
                sc.doc = Rhino.RhinoDoc.ActiveDoc
                try:
                    if Button is True:
                        if CSV_Flie is not None:
                            self.data_csv = self.read_csv_flie(CSV_Flie)

                            all_layer_names_ch = self.find_have_ch([_ for _ in rs.LayerNames()])
                            if len(all_layer_names_ch) == 0:
                                self.message2("All layers have been renamed!!!")
                            else:
                                all_ch_word = [re.findall("[\u4e00-\u9fa5]+", _) for _ in all_layer_names_ch]
                                tuple_list_data = list(zip(all_ch_word, all_layer_names_ch))
                                replace_names = ghp.run(self.replace_layer, tuple_list_data)

                                final_zip_data = list(zip(all_layer_names_ch, replace_names))
                                ghp.run(self.replace_layers, final_zip_data)
                                return
                        else:
                            self.message2("File path cannot be empty!!!")
                    else:
                        self.message2("Please open the button!")
                finally:
                    self.Message = 'Layer Rename'
                ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                sc.doc = ghdoc

    else:
        pass
except:
    pass
import GhPython
import System


# 插件信息
class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Object_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("96aa2301-c437-4e3f-b2f1-253a0679d742")
