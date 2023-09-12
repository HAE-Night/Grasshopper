# -*- ecoding: utf-8 -*-
# @ModuleName: Object_group
# @Author: invincible
# @Time: 2022/7/8 11:10
import time

import Rhino
import scriptcontext as sc
import Rhino.RhinoDoc as rd
import Grasshopper, GhPython
from Rhino.DocObjects import *
import rhinoscriptsyntax as rs
import ghpythonlib.parallel as ghpara  # 多进程
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from Grasshopper.Kernel.Data import GH_Path  # 树形分支
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
from itertools import chain

import initialization

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:
        # 获取数据详细信息
        class Data_message(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data_message", "C3", """获取数据详细信息.""", "Scavenger",
                                                                   "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a946c7ad-a18f-471c-a9e7-038677fce6a4")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKZSURBVEhL3VRLTxNRFGaj0UYSo0IgbAlxoYkxGkU0EHHPwkfiom2gCJ1HpzOdlk5LH+CLtqEqFBFsabEqj1IQ2qIkgl24cu1GE3f+kM97b0fFqEmZ7jjJyb13Mueec77vO7du39sBU/1xc1PLSaWxqe3f3tKmnGhulcm/pyshe7CDh4/0XLfEYB9aQ7+yqPsCbPISbM5l9Ek59Il5cJ4Szlzo+ayHVW+m+obeXmcWjsAWeG8RvK8AjqxiaBX+bBxa+gk8U7MIzuVwudv+TQ+r3ig8Fj4NMVAAH1jGgFzCoLoOfjjHzo57WaiJKbijJbR39X/Rw6q3nwm05DS0F2MYSsYxlIqD0/IkWZEk22CrHPqAjm6bwQRiCsIwqdy9DulhhlXO+VbgjKVg964SyFah3t9Cx1WjHQhzEPwlRjSr2FWAPJ5knWiZKOksAs94Ae2dd4xDxGtvWQcMFtcGBj1vGB+cjyiIwGUcIlOD2Uog8mUS8JJqXZNPoU4lKglIJ3ay0r0S3jHOgdWRhDSyBiG8AJUkEEdfsb0cf844oIpSH7yrjQPet1mBSKlA5JqYhmfmMbT5CHNPjMi0Fg6E4SIjecBZUVNFnoQD0gH9XhsHDsLB/CSpNAr3swm4pyfZpbtdGdmujQM2yf4cFIK7EFr8JVfmCpFtsFzDoNE5IBxQxdALKQfiyGvWEVWU8mgWWmKlBg4oybvmgLoQXGJJqJIYbJFN42+RmcvAOzMLX3aMzQG9kPOv/IaJvUWG5+CYxSqmIY0SvZM3iMpTGsswuP4i+Zrtqx5WvR0yHbX0Ol9CvfsRztA2JH8ZUmAHcvj9H65FPuFil/m7HrYna2471Zk/f+V2+Wz7jf/4zfK5S7fKjU2tdj1mX1ld3Q+GSA0b1KgHdwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Objects):
                try:
                    re_mes = Message.RE_MES([Objects], ['Objects'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        Group = Objects.TopologyDescription
                        return Group
                finally:
                    self.Message = '数据详情'


        # 键值对赋值
        class DATAKEY(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DATAKEY", "C4", """对物件的键值对进行f赋值，当多个物件赋值时，注意键值对顺序和数据结构；""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4b68c580-a4e4-4ca8-9e49-082b8f014c0b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Keys", "K", "Key-键,")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Values", "V", "Value-值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Toggle", "T", "是否赋值")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                result = self.RunScript(p0, p1, p2, p3)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALgSURBVEhLYxgFIwswaRl65ti4pFdbOcSTjW1ckqsNLAKrgOYJQ4xFAFbv8IbPJS1H/ufWbCcbFzbu+x+TOfs/0DwtiLEIwBoY2/GguOnQ/5yqLWCMzQBcGKQ+G4gL6nf/j86YCbJAHWIsArA6eec9iM2a+z88eRIUT/4RkTL1c0TKlC8QDGQnT/6G4EMxUAykPiJlMthwr5BarBYw2LikXE/MWwRWBNT0X0JKIwsoLATEYkDMC6U9gJgPiEHiEkDMBcSmPqF1/+Oz5/9PyF3w382/FLsF7kEV14qbDv7Prd72P6Ns/X9pDUvvDv+yxonR9TJt/hVezf4VXawMrAa13gVLJ4U0K4L0dARVl0WZ+LeHpk79WFC3+39hw97/QbGd2C0A2nytoH7P/6yKjf9Ti1f9l1Qz82/2LdlY7VPQA8QXmvzLdIHKVCo88z4A+ZPr7etZ6n1L/gcZedUHJ096D3JYXu2O/wHRbcRZIK5i4tvkU7ysN6zpf6VnnitUmWK5R05FjXfhnXKv/FKgBY942Ng0QxMn/CXZAil1cz+QBUBD9tV4Fe5eFbqKGahMLdc+RabKu/AzMMh+tgCDECgmFJ40ERy0pFvgW7yn0iPXvtqrcG6Nb9EaNjY2sMZq78JtIJ/NCG9WBnJliLYAFEnZlZv+pxWv/s8nKu8xxzJIHirN0GEfbwGkwBpvMTCwt9pE6IHYQCAeljjhf17Njv/5dTuBFrRit8DaOfl6dPqM/6EJff+D47r/27qmb7fzLmh28i3qcvIt7Lb1LWywckpc6uyTP8HBr6jNxqeg3sW3sA9YPCwEJVOQPpBPgGL/YT5FAb4RzTdALkgvXQPEa//n1+4E50xicGb5erC+7MrN/0GO5OUVxrQgILr9Xnn7MWA47iQbFzce+J+Yu/A/D4+wBtRYBLB3yzgVmTr1XXB8D9k4LGniO4+gqnd8fHwqUGNRAKgIEKQSBiXpUUAIMDAAACzLMF4ss44GAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Set_values_Greater_one(self, Objects, Keys, Values):  # 当key大于1时调用

                if len(Keys) < len(Values):  # Keys的长度小于Values
                    for i in range(len(Objects)):
                        if type(Objects[i]) is System.Guid:
                            for _key in range(len(Keys)):
                                obj_attr = sc.doc.Objects.FindId(Objects[i]).Attributes
                                obj_attr.SetUserString(Keys[_key], Values[_key])
                else:  # Keys的长度大于Values
                    for i in range(len(Objects)):
                        if type(Objects[i]) is System.Guid:
                            for v in range(len(Values)):
                                obj_attr = sc.doc.Objects.FindId(Objects[i]).Attributes
                                obj_attr.SetUserString(Keys[v], Values[v])

            def Set_values_Equal_one(self, Objects, Keys, Values):  # 当key等于1时调用
                n = 0
                for i in range(len(Objects)):
                    if type(Objects[i]) is System.Guid:
                        obj_attr = sc.doc.Objects.FindId(Objects[i]).Attributes
                        obj_attr.SetUserString(Keys[0], Values[n])
                        if n < len(Values) - 1:
                            n += 1
                        else:
                            n = 0

            def RunScript(self, Objects, Keys, Values, T):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()

                    if T:
                        if len(Keys) > 1:
                            self.Set_values_Greater_one(Objects, Keys, Values)
                        elif len(Keys) == 1:
                            self.Set_values_Equal_one(Objects, Keys, Values)
                        else:
                            return

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = '键值对赋值'


        # 物件键值对提取
        class Data_KV(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data_KV", "C2",
                                                                   """对物件的键值对进行提取，当Key没有值输入时。提取所有的键值对.""", "Scavenger",
                                                                   "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("af5ef186-5ae8-4eab-a2e8-42b171fa942a")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANDSURBVEhL7VVZaBNBGF5EVHyxKF4P+tCiLagPCoIIUlSwbTaJ1ip4QZU2m03aZGc3e+8m28OmFkU8QLxARLSHTZrG4oG1HlBBBEVfBGnrswpFiqC0lfGfdStL6QXx0Q8+8v//fDPfP7PDhPqPOcGyns5n5RSq0XuuBuX0tVwYUjPXIsb9c2wstdFZnqJYOR2Sky9xWMvikJLJmbGGZxgaHjhodSywDYJS1/mo+QAzWmcRx3XlMUrHEkZ5vITEE3mlE89GogtKqVs10CyJ/xjI6TOwLVyjppfZhRwREuGolC5MGrMLEwZVWvdKkuse1G3QSCaxXBLe0FRuvNI8/E6SE4ie8KpkuSGafq7QKVFqmbC+eb8pWdsOLA3KmUtTGrDWoxUkN7wCNrzoZqQ0srDBr3yu80uDWmlkuS0GGB5h+4XDzRga6XVKlObhshePNOPGLfsKGP3e2ZkNPGhYo9GNOM13NexTR1BJYLUtdGAVW/Nh8U8JX2yM28vlWcWVi0xv7AepkXFY78qMBiAcqvfLozBplN9ds8kWTYLu4VrOHTqJ495YmU5zJSSGxpJkjJXS12c2oPmBpnIdJ3ziT7E0UmCLJiHujW49VRHHOo3ugEH7qQoTm35hMxmb1cCg+S/AHujufZ1fHiJHYAtdsChrnuZBHy2fNA6N/IIdfXCG5mKARuCYrqo0ym85kIAPLrTawkmAnTa3VCQwIcw56ZTntINxYJbEaimHyO2ADo+T3A2zjN+U8ItjsINR04c2OOXpDQJ6yr4tcEX3uCfAMXjduRsSHV1H6KQ2pjX4W8gRYHCZvElugwtc/BFmpbs7WClTyAidRYS1WrYoILZOeYsIYIG1RDOhJ2Sl9sKglO4kD2cld8N5i6TUUbHxORbq+zBf1+viE/u3WmiL2EIXqvi2E9H4wynm9GI52U9e09fkb8CRg4mYKo+Y9xVWSv0lAwyp3W9jYF6NWnc4Uqoa3dklNDzFYaV70K0nDCsZtVbviQbQn+85KyrFjlXQ6XDEfPCVYbKLjwutayD/Dvx2At3Od2S5gXQsNr4gHfeF1ew7cnTuHf0TBIQ22Tj9BstN/biKbz/mlP8tWCXdwogdyEnnAIr6DXgFXcbMTo/FAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def KeyisNone(self, Object):  # 当Key值为空时，提取所有的Key值和Value
                Key = []

                for obj in Object:  # 根据物体的Guid属性获取Key值
                    obj_attr = sc.doc.Objects.FindId(obj).Attributes
                    Key.append(obj_attr.GetUserStrings())

                Keys, Value = gd[object](), gd[object]()
                for _key in range(len(Key)):
                    for v in range(len(Key[_key])):
                        Keys.Add(Key[_key].GetKey(v), GH_Path(_key, v))  # 获取Key
                        Value.Add(Key[_key].Get(v), GH_Path(_key, v))  # 获取Value

                return Keys, Value

            def HaveKey(self, Object, Key):  # 当Key值不为空时，获取Value
                n = 0
                Keys, Value = gd[object](), gd[object]()

                for _key in Key:
                    Keys.Add(_key, GH_Path(n))
                    for obj in range(len(Object)):  # 根据key值获取value
                        obj_attr = sc.doc.Objects.FindId(Object[obj]).Attributes
                        value = obj_attr.GetUserString(_key)
                        Value.Add(value, GH_Path(n, obj))
                    n += 1
                return Keys, Value

            def RunScript(self, Object, Key):
                try:
                    re_mes = Message.RE_MES([Object, Key], ['Object', 'Key'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc

                        if Object and Key:
                            Keys, Value = self.HaveKey(Object, Key)
                        elif Object and not Key:
                            Keys, Value = self.KeyisNone(Object)
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc.Views.Redraw()
                        sc.doc = ghdoc
                        return Keys, Value
                finally:
                    self.Message = '键值对查询'


        # 拾取图层物体
        class PickItems(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickItems", "C12", """拾取犀牛子图层的物件""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1947d440-6dc8-4eb7-8338-c936a5f54a4b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Switch", "S", "插件运行按钮，输入‘True’执行，默认不执行")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARvSURBVEhL5VVraBxVFI5a6osWhFalIiiKomhEml+CBMGCFFssGmyTNpvsbOY9+5qdxz6SSVtDEtLUZzEbkyabZDfZzc7uZje7adKmaZXGVGmhvqCg6B9Rq9hYsLS+xu8uQyE/JBv0nx9c7txzzj3n3nO+c6fq/wPaH98kRIov8qG8WwjlXUKoWGOr/h1qa411vJ7vEkLTfwYOvm952uYsX/sJK3DwtCWGpj9rCUw8b5uuHZJUulUMTi/oXUsWr+dGWf/k007nwIZmKbmZVbP1CPC12nHGcslJyt6yNtDK5JDW+aHFaOYussZN9iE1A7hNB+NL3kdkCFKUcRtOTm0l64rBBHOPk40tcuoAWcPRJ3D8JadmB3l9qiSGi9dYNV0P1U1iuHSFCaRPEbuKgRS0knw7jKHbGCUzDqcrHHBafgen5SxOj99FByb3S+GSJQWTm2316mAVM4kU/SAZpY2skll2yuYTtuoGGCX9EauZAqtkn/UfWECwbOVpYtVMjFHMnyl34h5WNS9TvuTDtuoGIF/g1IyfUc1tvv0nLUHNPmmrVgcCcKQGYMiDcDTLgkW2qgwuMFlNUiQouS20nOrntdxvsjxyp61eHaxs3o28/s7puXSDNLoRRf4WYw638nH61GExUrqKwN7dwsAWkh4mYEbtrZXD5Z+Qwj3nLLCn+1XuyP0I8IYYnv5YDBXmUPQXnJ7RR6XWY9+LkZlLtD+/yd62NoBBbXrXWQu0PF9VV3eLLa5yecfLhXVHjn1HecYfs8VrgyzPlnMKtmwnzwM5fXmNJvO0zl0XwzMX9tDRTbWGsY7IKwKKVoMcdwrB/JK3/cSPjJYrd7HLl9ildS5aKOwIHywsuttmrzba3cyomXl36+xFdHqMC+Zfqqsz1hP5CtDeRI0ULp4VQ8U/BD3/DeE4RgmpOLSbOlJdtpHTSvjQeUt57QOL8ie3EdleJhqgvPEUq+XOgEmfol7X4OcnRs0yRF8Gp6SfwwmuuyMzJ52+RKRJGu5vEoffbcYMpxhJlnQ0scVGtcWfcpFv6Ha4vIm3Kc/YWw5xuLdJjEUdUkwSQ6Ve0hdo0B5iRxrmlBAqXCDf9XTf503CcIDVMgqC8lrn0lMeY+EBX+/i7YZh3VzeABgpaz1o/JDeubQVBFAZJdveyB+NNjDRGaJvUdKyp23WKhvTqtnsNY7jfS/2OIShl3H613GiwSYplnZ64yZOOE55EzGkYoDyYHjHYk5PfNLpHStizDmlkRK5tYMbpB380L2cnm+G82V0eKEcgIDTzEYpUrqCIL+iUAW8Rd2ULyEjoLSXf8/dQPf569k+mcwY0j6mv6WR79/TKAzvpHwT29GADUKw8CYycYkcFnOfYaRWFnuns3sD+R2CJfNg0i9gDOnkZRTwK1bLnsMLexrjOGTzWC+xau4ibC6j6Qi7/sL8BQjS4fKPP2K7/GfQRv4OLjhVzQdzr8CZBseHUbSjeNzioOUI/gvv4C9ncGqumQtPPyMFS5U/1f8dqqr+Bl7RUaDZ9ES5AAAAAElFTkSuQmCC"
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
                try:
                    Data, Info = (gd[object]() for _ in range(2))
                    self.factor = Switch
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
                    else:
                        Message.message2(self, '程序默认不运行')
                    return Data, Info
                finally:
                    self.Message = '拾取图层物体'


        # 提取指定图层的物体
        class ExtractObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ExtractObject", "C5", """提取图层信息，拿到指定图层物体""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6bb12637-cbd6-4ae1-8cd2-4904a15d7b41")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Geo_Type", "GT", "指定要选择输出的物体类型，{0：几何物体（默认），1：点，2：面，3：线，4：Brep}")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMQSURBVEhL5VVLSFRhFJ4eFEGLwMoeKFkYQguhRVgRgfagXRCTK4maae5rZnScuc+Z8YYEQYtCCgOjh4Wm49x756lm1oglBQpRkAi2sk0SlG2Coub23ZnfwpyC0kXRB4f7n3P+/3znnP9xbX8daME47PR1VRF1ccHI8RZ/85BZ3zRgMpLBEvPCUedtL/WE+kY5JTlDCfoULRqTbiVteoKpS2TKn4OR9EPI+JM33Dfm8HYW07yWoXjtnCug7/aG737xhvoeOOR4MZn++6CEqMMb6m8hqo0RtDFa0K5Y4xPujgpv08CEi4/W5pyLAQQfnSWYhWmaS8hw4ShEsKj4jwloQT9CBaJ7ifpT4JiOU4J2i6gFgbtynOWNGqLmgUVP6YDWZY3tdvsyRoodYKT4BXzvM2J8mJMSraycqKECPQHar1XnFhUAy0ZWo8IXlKjfIaY8QDCEC9SBDEW3kpqGmIxoTKCyLthvM0LsuXV7OTk5DrKAS45WqGpm+X5VXU6JxhYkcpJTUsOIM0Xz+itG0C+T0HmAdRCBeuEccMvJs+5gvIy4voHio+UgOA+Zhpggfwd5y0oxE9V94ORUAgQHEWcEbbpKluXh4vVHyP4GUXOglORmvDd73EpyV71qrCHmHGglXuWWUw5ONJxIaJ/P172KuGy0qI8gmetEzQOsD0HQdorv3MTIiWZkOMmIsSwyzKJVJislPsJ2D76jZMkcqKq6lFPSx9CaRorXH8+rAIHSKG8CL+V79PI1Sr5Ii1q1S4yUMlJ0K57nWtj63cE02hF/A9KbNB/1o7VhWogl4JvxhvtNKqBdyyUram0kdB7ofYbmexKckthJTAWBE7QewXwgyaDCl6wYG2eluIF1Tldjx1prDhIdxima16InKE9nA5ENVsacpG//USg+Wc40GiV1XHvR6QZtoyfYu83p7y7zyN3rOE4vYoJGiXUQsOnP0JE5+2kRtFp/KqvnEOv7S8H8LKr+jDEE4+++rO/MoIk9kEnoPOxqZEVDqG8HJSYrKVFbgCQrWcTxeHpXktD/NGy2r6dE2YUM/0/UAAAAAElFTkSuQmCC"
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
                try:
                    re_mes = Message.RE_MES([LayerName], ['LayerName'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        Layer_Type = 0 if Layer_Type is None else Layer_Type
                        Geo_Type = self.which[0] if Geo_Type is None else self.which[Geo_Type]
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        res_layer = self.filter_layers(LayerName)[Layer_Type]
                        rhino_ids = self.choice(res_layer)
                        Bulk_Geo = map(lambda x: rs.coercegeometry(x), rhino_ids)
                        Geo = Bulk_Geo if Geo_Type is rg.GeometryBase else [_ for _ in Bulk_Geo if type(_) is Geo_Type or type(_) in Geo_Type]
                        return Geo
                finally:
                    self.Message = '提取图层物体'


        # Rhino文本物体提取
        class PickText(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickText", "C11", """提取Rhino物件（可单独选择）中所有的文字""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7965623e-a903-49b1-b217-165075d74605")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHISURBVEhL7ZNbKwRhGMdXXJIbRMoVKSUXbkTSOizWoUTZwlI0O7Mzs2fGsmstCoU7pZwj5cb5mEO58il8lr/nfXecdles7IXy1O9i5n2e/2+aecbwX9+tAkJLAoUELxOBJNBF8DISKClrQFf/Atos4R/TaV1AaXnri6CdhbPigqq6QYzOPcIRvIYzeAU1dAM1fP81oVuaueJz2uwjjM1KfEFFTR/ck7cQRw5gGz2GKm/AS0/kGVj6FHbukFap/4jPuUhW3SB8LRDGTuHrnUeoVkCwUdZRopAxUS9g2DINm/8kcYHXusiDxs2uCC3uN/R7gSYFvp7ZxAWidgjJuw/ZuQvZtQenbQUBs5PCKbTZAdfQMmT3Hj+3e/Zp5jBBgS5h30IYO6OgnQ8CRdmEMH7Oz0Ut8v4TF+iwEEXd/iBQ7euvr+U9/4IkCpQtvvdsLYMmO1Rp7ScCKzzhO0hsRd8hkoCtpGaZwgj9VFr3FBRaT5EE0b3uyTtUm2zxBZXGAfhmHiD7T2OhVbUHLnQu+XW8Pu/0A2oapRhBPYH0jCzk5hcjJ6/wE4qiiO1h8xmZ2S+CDhbOqoJ4SgJ1BK8UIvWXSSNY7p8ug+EZvk7wXVu18vsAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def get_center_pt(self, single_pt):
                center_pt = single_pt.GetBoundingBox(True).Center
                return center_pt, single_pt.Explode()

            def RunScript(self, Objects):
                try:
                    re_mes = Message.RE_MES([Objects], ['Objects'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object](), gd[object]()
                    else:
                        temp_geo = ghp.run(lambda x: Rhino.DocObjects.ObjRef(x).Geometry(), Objects)
                        filter_t_list = [_ for _ in temp_geo if isinstance(_, (rg.TextEntity,)) is True]
                        Text_Entity = filter_t_list
                        Text = [_.PlainText for _ in filter_t_list]

                        Center_Pts, Contour_Line = zip(*[_ for _ in ghp.run(self.get_center_pt, Text_Entity)])
                        Message.message3(self, "已选择{}个Rhino物件，提取{}个文字！".format(len(temp_geo), len(filter_t_list)))
                        return Text_Entity, Text, Center_Pts, ght.list_to_tree(Contour_Line)
                finally:
                    self.Message = 'Rhino物件提取'


        # 按对象的用户属性筛选对象
        class FilterByAttr(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FilterByAttr", "C1", """按对象的用户属性筛选对象，或在没有对象的情况下并行筛选属性""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3e5f7e76-814c-478b-b898-756e3141815f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Attributes", "A", "物件集合列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "参与筛选的Key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Val", "V", "参与筛选的Value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Objects", "O", "筛选出的物件Guid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "筛选的Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Val", "V", "筛选的Value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMfSURBVEhL5ZRbSBRhFMeFXiooCB96KugpH3oR6i16iCiiqKx86aKy7mVmx73P7rqzrqtWZnhDC5MupJnWbjuzq+6uWi4E2h0NKyiIXqKyC1FEkbW4/87YZxEma61v/eDwzXDO+Z/55pzvy/o/ALCYbGUqlVpH6y5azWS1qVQyQOsNsg0sND0UnE1WRsktqdTXaHLi9ejTJ/deXB/qm4h2d+B8WxOaGnyo9BlxyFdI9T6C4s+y9PRQ8FKyL+9f30SVtB/PHrbCZdmOw9JuHD+2Hx2tOkQuWNAfciEesGFspEMt8ErdJZNIDyU0J5NvEDyrw6PbdXh8px6nm/RorC6govnwinmQHLvgJes8ZSRtqEW2sfT0UHwOJUy2nyyB3GbCg5s1aKkrwJlmDdpaDFRMi/ojB+B374aV24wHY8P49PnbRZb+ZzTOyBLOrdTypd0NBpdyuropkTxx5gqONspobFFQWdOOIr4OewtrsWXPIWzcUYmt+dUoNJ6EWCFDrIpNGpyhqNnXL3NORcNkf2GzBRZxLuWSVDsCqz+BIksQRVYFGnuE1jC0Yg94TwyCFIeprI8sTs8xcO5eFNtl6BwyHFXXIB4eAn2gjsnOhHPJPkv5FQieXtAzmZLWDE4ZZioqeGMTWjGQx6Rmx+AOFwlSdNLkjYOj5D+J/jTyW+mDSqToC709uJ5JpEcnhjYJUu8H+qdTXziruH8QRk/vfa0jsIqlzh2NvStX8ESfW8oHZhahd1sFiZf23D0otGezlL9HYwmsFjw9L9XG/uwJiat9MpZ2j+7jO5ex0H9Hbw/lUNPfGj09UwVKvDHQOI8Xm7uWs5DM0TtDCYtvALw7DJM3ltI5AnM/uXOBdymdVv/VqfGlfrwr9J9byFzzA+cKNfxoajcdrvAEbw+vYK75gRorqQXUHqg7obWZueYHgxjJUydnqsnqFeFSxvnSaOYTNA2NqHV6B7w7QoeLJsp9OZe5M4duyj71wP1WwCOvYe7MMIjKTifdkraKBKy0C+eRYXWSbuUHgwtYSGbonZG1Zv9gCYkaOXdEMElxzdz+f1bWdy0JSlUMibMiAAAAAElFTkSuQmCC"
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

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
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

            def HaveKey(self, Object, key, contrast_value):  # 根据Key值，获取Value
                Obj, Keys, Value = [], [], []

                for v in contrast_value:  # 遍历得到的value
                    for obj in range(len(Object)):
                        obj_attr = sc.doc.Objects.FindId(Object[obj]).Attributes
                        value = obj_attr.GetUserString(key)  # 根据输入的key值得到Value
                        if value == str(v):  # 判断得到的value是否与输入的value相等
                            Keys.append(key)
                            Obj.append(obj)
                            Value.append(value)
                return Obj, Keys, Value

            def RunScript(self, attr, key, val):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Obj, Keys, Value = gd[object](), gd[object](), gd[object]()
                    attr_str = [str(_) for _ in attr]

                    if len(attr) == 0:
                        self.message2("A端为空!")
                        return Obj, Keys, Value

                    if key == None:
                        self.message2("K端为空!")
                        return Obj, Keys, Value

                    if len(val.AllData()) == 0:  # 判断是否为空树
                        self.message2("V端为空!")
                        return Obj, Keys, Value

                    value, value_path = self.Branch_Route(val)  # 得到输入的value和path

                    for i in range(len(value)):
                        O, K, V = self.HaveKey(attr, key, value[i])
                        for _ in O:
                            Obj.Add(attr_str[_], value_path[i])
                        for _ in K:
                            Keys.Add(_, GH_Path(value_path[i]))
                        for _ in V:
                            Value.Add(_, GH_Path(value_path[i]))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Obj, Keys, Value
                finally:
                    self.Message = 'Filter by User Attributes'


        # 创建图层
        class Add_Layer(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_AddLayer", "C13", """生成未存在的图层（只考虑最优时间，除图层名和颜色之外全为默认值）""", "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d9bff954-6290-459b-bbe8-bdbaa8088074")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

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

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "LineType", "LT", "线型名称")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                SWITCH = False
                p.SetPersistentData(gk.Types.GH_Boolean(SWITCH))
                self.SetUpParam(p, "Switch", "S", "输入True按钮，生成图层")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Layer", "L", "创建的图层")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPPSURBVEhL7ZRbTJtlGMdRL9QLk3njhcbopfHCaGLUS403BpTD+m1IS9u1tIUVKLQIlBbW0vO5fC2FDnvipICTJQhZlmFQx2KyucxjwAF2hbGNw4LDuJio+ft8X7/ZLCGLBy73T57ke7+87+/9P4e8Rfe17wolci+zg9fYYPKKjpYP5v/+T/n7lp8Ip3K1wVRuPpxZQ//4LfSN/Yxgeu1iILnytrDt3yuYyb4RSudSgVTuZmxsB5GRTfgTWfgGVviIDG8iOrJFF61OBRKXXxKO3VvudPbZQHK1jaBfs0M3EPtwB8HU2t/QQizz4X9/Bb0f3EQotfoHZdnrjS48KaDullhsfPyYf36SHdq43T++C3bwOn/4DujesYQAZcaVjS7aDpFBAI8I6LzESvszqvoojPZT8MR/pI13XO8F3Dv8iZ8QHd1CfOIXtNpOZxmZ6SkBn5fsqO8FVUNsWdUQRYdzFsFkjo+9YIVYoRKuIpy5CmfsezR2fIxKmfvPskPG9RJGX7hA1dT7oje+eC4ysv1rp+dzHKkNQKOLw9bzFULpq0JzC2DOLQflDHT6zkFRH0f5u52Q10XRbJ6cTZ/cOSCg85IonW9qDQlyfoaAawgkr9DGjyBVuaEzjlHZFvmyccBwZh2e/kXouz5B5REPygisbBiANXSBpmqT+neNzpz4grAP5emCSpnG51X1kcXapuOwBL6kMdyCI/otNLSWa/zocM2iu+ci1M1plFd1gZE6oDNN8hlx42pjL0HdlAIj6d4tZVonCPlAnkzSm8ZfiQ5vTEWGNm5xIK5E2vcyfMNpsmD2zEFRF0IFuZXWRmD2nqX/1/ls2hyzENcEIZJ0o84w/HuLdVovYAuSqz1tXe4zsEcu8UDv8SU0to+Scx9ardM8iHPq7P2Od8uVSNs2BlG1DYdkTmruCd4MN6qRoRu/6cwnWQGdl1LpfUyisJkJeLvdNkMXXOZLZA2dB00WamiEuW9L8Dzk2j5UUImqNSyMrjm+2dHRbbj6FtBimYGSa3ilaUZA3y25xvmcVGmfOqofQJfvLO88nF5Hu+0UZGofDoqtUOsH0U31jlAmPVQmS/gC6tvHwVA2JQcNn75T3nyYYfSPCsi9JVHYq6QqT9ZgnqBGfwOW3h1X7Ae4qTTc08CNrdH1GWp0CZQdNu0WV+iTpaKWV4Xj/0xyueVAtdIZVtQFYXScho+eDlf/AvTHplGtDqNE1LpUXG4wl1UanhaO/DfJVY7XZCr3vNaQooa6UFxhmCsWGareamQfFrbsj6pkVkWJqOV1YXlf+6Gior8AECXdwdGsNN0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_data = {1: "Continuous", 2: "Border", 3: "Center", 4: "DashDot", 5: "Dashed", 6: "Dots", 7: "Hidden"}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def create_layer(self, tuple_data):
                name, color = tuple_data
                if not rs.IsLayer(name):
                    rs.AddLayer(name, color)
                else:
                    rs.LayerColor(name, color)

            def change_line_type(self, tuple_data_two):
                layer_name, line_type = tuple_data_two
                rs.LayerLinetype(layer_name, line_type)

            def RunScript(self, Full_Name, Color, LineType, Switch):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    if Full_Name:

                        if Switch:
                            diff_values_one = len(Full_Name) - len(Color)
                            diff_values_two = len(Full_Name) - len(LineType)

                            if diff_values_one > 0:
                                Color = Color + [System.Drawing.Color.White] * diff_values_one
                                zip_list_one = zip(Full_Name, Color)
                            else:
                                zip_list_one = zip(Full_Name, Color)
                            map(self.create_layer, zip_list_one)

                            if diff_values_two > 0:
                                LineType = LineType + ['Continuous'] * diff_values_two
                                zip_list_two = zip(Full_Name, LineType)
                            else:
                                zip_list_two = zip(Full_Name, LineType)
                            map(self.change_line_type, zip_list_two)
                    else:
                        self.message2("图层名为空！")
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Full_Name
                finally:
                    self.Message = '图层生成'
    else:
        pass
except:
    pass

import GhPython
import System
