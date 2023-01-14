# -*- ecoding: utf-8 -*-
# @ModuleName: Object_group
# @Author: invincible
# @Time: 2022/7/8 11:10

import Rhino
import scriptcontext as sc
import Rhino.RhinoDoc as rd
import Grasshopper, GhPython
from Rhino.DocObjects import *
import rhinoscriptsyntax as rs
from Grasshopper import DataTree  # 树形
import ghpythonlib.parallel as ghpara  # 多进程
import ghpythonlib.treehelpers as ght
from Grasshopper.Kernel.Data import GH_Path  # 树形分支
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
from itertools import chain

import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 获取数据详细信息
        class Data_message(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-获取数据详情", "RPP_Data_message", """获取数据详细信息.""", "Scavenger",
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
                self.SetUpParam(p, "Data", "D", "数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Group", "G", "信息结果")
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
                                                                   "RPP-提取键值对", "RPP_Data_KV",
                                                                   """对物件的键值对进行提取，当Key没有值输入时。提取所有的键值对.""", "Scavenger",
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
                self.SetUpParam(p, "Object", "O", "物件集合列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "需要提取的Key-键,支持多键查询")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "KS", "提取的键；当Key没有值，它提取所有的key。反之只有Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Value", "VS", "所提取的键")
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
                                                                   "RPP-赋值键值对", "RPP_DATAKEY", """对物件的键值对进行f赋值，当多个物件赋值时，注意键值对顺序和数据结构；""", "Scavenger", "Object")
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
                self.SetUpParam(p, "Objects", "O", "物件集合列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "K", "Key-键,")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Values", "V", "Value-值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
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
                if len(Keys) > 1:  # key>1
                    if len(Keys) < len(Values):  # Keys的长度小于Values
                        for i in range(len(Objects)):
                            if type(Objects[i]) is System.Guid:
                                for k in range(len(Keys)):
                                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                                    rs.SetUserText(Objects[i], Keys[k], Values[k])
                                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                                    sc.doc = ghdoc
                        return
                    else:  # Keys的长度大于Values
                        for i in range(len(Objects)):
                            if type(Objects[i]) is System.Guid:
                                for k in range(len(Values)):
                                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                                    rs.SetUserText(Objects[i], Keys[k], Values[k])
                                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                                    sc.doc = ghdoc
                        return
                    # key的长度=1
                if len(Keys) == 1:
                    num = 0
                    for i in range(len(Objects)):
                        if type(Objects[i]) is System.Guid:
                            print num, Keys[0], Values[num]
                            sc.doc = Rhino.RhinoDoc.ActiveDoc
                            rs.SetUserText(Objects[i], Keys[0], Values[num])
                            ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                            sc.doc = ghdoc
                            if num < len(Values) - 1:
                                num += 1
                            else:
                                num = 0
                    return
                else:
                    return


        # 拾取图层物体
        class PickItems(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-犀牛图层拾取", "RPP_PickItems", """拾取犀牛子图层的物件""", "Scavenger", "Object")
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
                self.SetUpParam(p, "Father_Keys", "K", "父图层的下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Unique_ID", "U", "唯一标识")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Switch", "S", "插件运行按钮，输入‘t’执行，默认不执行")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Data", "D", "拾取的物件")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Info", "I", "拾取图层的信息")
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


        # 提取指定图层的物体
        class ExtractObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-提取图层物体", "RPP_ExtractObject", """提取图层信息，拿到指定图层物体""", "Scavenger", "Object")
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
                self.SetUpParam(p, "LayerName", "L", "图层全名")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Layer_Type", "T", "默认拿图层全部的物体，输入数字去选择{0：全部物体，1：父图层物体，2：子图层物体}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Geo_Type", "GT", "指定要选择输出的物体类型，{0：几何物体（默认），1：点，2：面，3：线，4：Brep}")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "提取的数据（Rhino真实存在过的物体）")
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


        # Rhino文本物体提取
        class PickText(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-文本提取", "RPP_PickText", """提取Rhino物件（可单独选择）中所有的文字""", "Scavenger", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7965623e-a903-49b1-b217-165075d74605")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Objects", "O", "Rhino物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Text_Entity", "TE", "文本实体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "文字")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Center_Pt", "C", "文本实体中心点")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Contour_Line", "CL", "文本实体轮廓线")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFUSURBVEhL5dXNK0RRGMfxKxLyWv4NCy9l5WXhH2A1ZaG8/Auy4s+QLSUba6WUt7IiC/IHYIUFK2z4/p45Z0Inc7rPZONXn6bnmTP3uTNz7r3FX6YXFSxhwUGfn0YLaunHNT4aaA+tsMxCzWccOZ3gDTreCCyLUOPQKn9uoeNNWEXmocaxVb604Q463pgaSmpAE7rRk6ETMe3IGtCFGzzgKXgMtV6/1geIyR6gs3+B+vVcISZ7gL76K9SfwxD2Q72BQayGWt80JnuALhTtgik0q0G2oHUrVlVPQu+PWlVN9oBUdqB1a1al888HbELrlq1Kp/QA/eFn0LpdaFelUnrAJbQm2kYqpQes4wLn4TVu1Z9x/Qc5+XWA7ufe6AKNt+vaAD3m1DiFbrcefbiHjjcJywzUeIeme8SfRwZg6YCeofGNRtCm0DPlW4ah/T7uoM+HMy+KT1711l2S3UdKAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def get_center_pt(self, single_pt):
                center_pt = single_pt.GetBoundingBox(True).Center
                return center_pt, single_pt.Explode()

            def RunScript(self, Objects):
                try:
                    if Objects:
                        temp_geo = ghp.run(lambda x: Rhino.DocObjects.ObjRef(x).Geometry(), Objects)
                        filter_t_list = [_ for _ in temp_geo if isinstance(_, (rg.TextEntity,)) is True]
                        Text_Entity = filter_t_list
                        Text = [_.PlainText for _ in filter_t_list]

                        Center_Pts, Contour_Line = zip(*[_ for _ in ghp.run(self.get_center_pt, Text_Entity)])
                        self.message3("已选择{}个Rhino物件，提取{}个文字！".format(len(temp_geo), len(filter_t_list)))
                        return Text_Entity, Text, Center_Pts, ght.list_to_tree(Contour_Line)
                    else:
                        self.message2("尚未选择Rhino中的物体")
                finally:
                    self.Message = 'Rhino物件提取'


        # 创建图层
        class Add_Layer(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-创建图层", "RPP_AddLayer", """生成未存在的图层（只考虑最优时间，除图层名和颜色之外全为默认值）""", "Scavenger", "Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d9bff954-6290-459b-bbe8-bdbaa8088074")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Full_Name", "F", "需要生成的图层全名")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Color", "C", "图层颜色")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Switch", "S", "是否生成，默认为不生成（F），输入（T）生成")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGeSURBVEhL5dVJKEVRHMfxZyhTyZCpbAyZNpQoU2yUjaJMyYKNnbBQUrK2EVlIlnaShYUSsbAylSKsDEspkZUyfX+5p2638+7zXi8bv/rU63/v/b9z7znn3sC/Syyqf35GP004whcOUIuoJA0LUGO3D8wiBRGnG7fwNne7RjvCSiHWYWsYzCry4Zs4jOIZtiahPGIYMbCmE7YLw9UKayqhUdgu+q0HVCBoErEC28WhLCMBQZOJSWShEZewNfI6Rz1yMYFUWNMPXfCEASRhGlrz3qbyjinovCG8QPUOWJOHXZgGOyhCCfacmvdYKfadmmwjG77RnZjJ/oQZ5SDUTHeXjBmYxprcXvimCqfogZ6ne7Iv0AClBdrB5tgScqCBHaMc1rj3wSa0o5tx5dTkzvVbk6s/LcaWU5M2WKOdPI5X6MQ3jCEDmmzTQI9Nq011rRpNtup6A4xAr3XfaEQbMA1PUANtIDUuQx3OYM5ZQwHCSh/uYZrMQR+cRVftBl2IOOlwN3Sbh74XUYkmW49KjQ9hVlRUEw99KkNO4h8lEPgG/yjLPxScSSkAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def test(self, tuple_data):
                layer_name, color = tuple_data
                rs.AddLayer(layer_name, color)

            def RunScript(self, Full_Name, Color, Switch):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    if Full_Name:

                        Switch = 'F' if Switch is None else Switch.upper()

                        zip_list = list(zip(Full_Name, Color))
                        if Switch == 'T':
                            map(self.test, zip_list)
                    else:
                        self.message2("图层名为空！")

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = '图层生成'
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
