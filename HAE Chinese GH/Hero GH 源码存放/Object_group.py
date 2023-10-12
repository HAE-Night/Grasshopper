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
import Rhino.DocObjects.ObjRef as objref
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
                                                                   "RPP_Data_message", "C3", """Get data details.""", "Scavenger",
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
                self.SetUpParam(p, "Data", "D", "Data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Group", "G", "Information result")
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
                    self.Message = 'Data detail'


        # 键值对赋值
        class DATAKEY(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DATAKEY", "C4", """Performs an f assignment to the key-value pair of object,when multiple objects are assigned values,pay attention to key-value pair order and data structure；""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "Objects", "O", "Object set list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Keys", "K", "Key-key,")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Values", "V", "Value-value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Toggle", "T", "Assignment or not")
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
                    self.Message = 'Key-value pair assignment'


        # 物件键值对提取
        class Data_KV(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data_KV", "C2",
                                                                   """Extracts key-value pairs for objects,when no value is inputted for Key.Extract all key-value pairs.""", "Scavenger",
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
                self.SetUpParam(p, "Object", "O", "Object set list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "The Key to be extracted,supporting multi-key query")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "KS", "Extracted key；When Key has no value,it extracts all the keys.Otherwise only Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Value", "VS", "The extracted key")
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
                    self.Message = 'Key-value pair query'


        # 拾取图层物体
        class PickItems(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickItems", "C12", """Pick up the objects of the Rhino sublayer""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "Father_Keys", "K", "Subscript of the Father layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Unique_ID", "U", "Unique_ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Switch", "S", "Plug-in run button,input 'True' to run,default is no execution")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Data", "D", "Picked up objects")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Info", "I", "Pick up the layer information")
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
                        Message.message2(self, 'The program does not run by default')
                    return Data, Info
                finally:
                    self.Message = 'Pick up layer objects'


        # 提取指定图层的物体
        class ExtractObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ExtractObject", "C5", """Extract layer information,get the specified layer object""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "LayerName", "L", "LayerName")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Layer_Type", "T", "By default, take all objects in the layer,input number to select{0：all object，1：Father layer object，2：Sublayer object}")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Geo_Type", "GT", "Specifies the type of object to select for output.{0：Geometric object（Default），1：point，2：surface，3：line，4：Brep}")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "Extracted data（Rhino real existing object）")
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
                    self.Message = 'Extract layer object'


        # Rhino文本物体提取
        class PickText(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickText", "C11", """Extract all the words in Rhino objects（Select separately）""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "Objects", "O", "Rhino object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Text_Entity", "TE", "Text entity")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Center_Pt", "C", "center point of Text entity")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Contour_Line", "CL", "Text entity outline")
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
                        Message.message3(self, "{} Rhino objects have been selected,extract {} text！".format(len(temp_geo), len(filter_t_list)))
                        return Text_Entity, Text, Center_Pts, ght.list_to_tree(Contour_Line)
                finally:
                    self.Message = 'Rhino Object extraction'


        # 按对象的用户属性筛选对象
        class FilterByAttr(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FilterByAttr", "C1", """Filter objects by their user properties,or filter attributes in parallel without objects""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "Attributes", "A", "Object set list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "Key that participate in the filtering")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Val", "V", "Value that participate in the filtering")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Objects", "O", "Filtered object Guid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Key", "K", "Filtered Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Val", "V", "Filtered Value")
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
                        self.message2("End A is empty!")
                        return Obj, Keys, Value

                    if key == None:
                        self.message2("The K terminal is empty!")
                        return Obj, Keys, Value

                    if len(val.AllData()) == 0:  # 判断是否为空树
                        self.message2("The V end is empty!")
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
                                                                   "RPP_AddLayer", "C13", """Generates layers that do not exist（Only the optimal time is considered，all are default values except layer name and color）""", "Scavenger", "K-Object")
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
                self.SetUpParam(p, "Full_Name", "F", "The full name of the layer to be generated.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Color", "C", "Layer color")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "LineType", "LT", "Line name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                SWITCH = False
                p.SetPersistentData(gk.Types.GH_Boolean(SWITCH))
                self.SetUpParam(p, "Switch", "S", "Input the True button,generate layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Layer", "L", "Created layer")
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
                        self.message2("Layer name is null！")
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Full_Name
                finally:
                    self.Message = 'Layer generation'


        # 根据犀牛ID拾取物体
        class SelectObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SelectObject", "C21", """Pick up objects based on the Rhino ID""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def get_ComponentGuid(self):
                return System.Guid("6e032788-7968-4154-baeb-ebe8df1df8ab")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Guid", "ID", "Rhino object ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "LayerIgnore", "L", "Ignore hidden or locked layers")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Select", "S", "Perform operation")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVXSURBVEhLzZR9VNNlFMcnwUFNOpl5Cut0KhFoL7/fbwzQQ8ud1CzBADHeJSaC8tIYDRgMgW3iGHMoDIQxGSooICCgCQgZ+AIaJCA6MJKkQIwQTDBfEbk9PzbNP9Tgvz7nfLfn3t37fHee556H8r8FAGb9PVjj9XCsoX7iXrNu4s7ZikcPzu95eL8laPKhDh8Ya1lgKJ05w71HrLrb8jtu/VYO8KAR4FEL8mtFuoDUAY/v/QgT462jPT01Ww0t02dysO7VykJpd9vJLOhuzoWh3iNw8/pxGL5Wg1QNI+h7dLAWHt9tgrbWEp2hbfrUFYQuzdgR/vuxQsldXaMaOs/nQ4+uBLovFkFX20G49FM+dLTsh97LZfB99e5WQ9t/o8nv8ss9fOeMWKWLIOOyfXE7G6t3Qm2FAo4dVkBDjQqOVyrhaEkyFO1NhP2auImMVEHyVDNiCZIAKeB5MjExCnJyDQMPrhJWro0ACsVoc3p6+FuFe0Rnq0rlULhPciNNHq5MTgjMloo2SuKFfm5buG7knk9ZheSINPt5Mjc3n7veO67Mi5sCLh6xVcbGxiEoT+HxfF87kCtOrK5McyXjl8FBWq5fvhAjd3c+weFwjNHaF8lsKjtNSAO7gqOjFplFw4v0qZdCHt08/XJ64B7e0dqM/L5xacblW8HxJ5hkMi+vmZpV0NckU/fU8GTtC6cq9czYgOrmGXk7VtYA4fFV8HVYTkzNmcmF8dISbUp2J8TvbIMtkYWJ2rKR1ZnFY5ao3hNpRgYsKv1j0XqfxA4X96h2uaqxW6ntGw2LKRtw8Yi7vcaV3x8rKenKKLiOzC6MvWdhR47fK/rW6bECiUYuxGIlNUb6HURt+wE28vL6RdIKTVzK6SJe9N6feaJyCBEegiVUdilZOxPsPl35VYjm0FB90u7uBg//7a2fO/OvcoO21+3IvvBYpr4KAfz8zpWrucVrvgyTmJiYkHcwV986PT7y3BB3PSW7C+JT24DL2ytI3d3IFiVVJQbxc2ETTwuB4eq6orpJ/6pOeBvVuyPNaEzxpQ7OWk//5FFHt8i+SJE2LT2v535S1hXw2rTr2PIVXkKp4vhIxsFhiJY3DZi9Yc5HPUb29ixXDGNkstlsjGVDnCZwRjtB4PU4jnP12/4L28xszjK5qqkqXtncErG1uEKQcBTCYivALySHfEIom8Iyr4UKS8E3KH18/oJ3YskcQWCRdBqt3d7e1o9Op09Qra29aTTaNozBABQnkDVPoDuuDdAo1ZdAouqEQEGhbo0Lr9zVXXASmXbu2j94I1hYUue8XqB1XhfhhOrJMaUwcfwbZNBoZ2fjizYcIHMkTCaTh/ITLBbr6T3ZYNgnUT4BiiHvACWs805MIpMpQuG7W2W1IJI3AZef3zVVqWcj+fGMgQ8y+GPqFwTHwcEWxxiAYdgHhhRlGYax1yZntJxEY1ivUqlM1Qd+5ctzrqg8/WUdbt7iv/w3K3JyS0dSFNp+8h3yIZteZLDcwcGZPCYGgzHfkKJg/kGym+n7+iEq+dx9obS8KDVHB4rcfgiOqVRbW1svkKXWVmce+BMS0jpgCZ2jJZsIDAtnUGnnbG2ZG+h02pBYLJ7t5OT0oS3L5hcqlVo7tbMBwtEltDdUWAw+gWnjwfzszECeBrYICtAlZ0nIgpBvNSWh0cXgH5o9/v5iZhZKzUIGIQwa7ZSdHfMLNE2AJqifSeA3GQzaKYIgnn27KMScOfOUuM2qixZWtkdQ7GlFczhBxzgdpqamgSj2Mnv9TT7O+qxrsYVNEYojkUysrKzM0IUuIp9wND04+tf2lpaWT8+dQqFQ/gEqlmmdsWBYiwAAAABJRU5ErkJggg=="
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

            def RunScript(self, Guid, LayerIgnore, Select):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([Guid], ['G'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        layer_name = rs.ObjectLayer(Guid)
                        lock_factor = rs.IsLayerLocked(layer_name)
                        visible_factor = rs.IsLayerVisible(layer_name)

                        def select_obj(id, bool_factor):
                            if bool_factor:
                                rs.SelectObject(id)
                            else:
                                rs.UnselectObject(id)

                        if LayerIgnore:
                            if (lock_factor is True) or (visible_factor is False):
                                Message.message3(self, "Objects exist on locked or invisible layers")
                            else:
                                select_obj(Guid, Select)
                        else:
                            select_obj(Guid, Select)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'Object Select'


        # 替换犀牛物体
        class ReplaceObject(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ReplaceObject", "C15", """Replace Rhino objects""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def get_ComponentGuid(self):
                return System.Guid("382f05d6-aa9f-438c-8452-47f9b6bb3874")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Guid", "ID", "Id of the object to be replaced")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Replacement object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Replace", "R", "Replacement button")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAWLSURBVEhLrZULTFNnFMeryTaWbCY+tsw5o5uVQh9QyiMVohVMBBQqjxahLY9SCqUUKJcW+pCWQgu0tKXykkK04IOhSMQpiMZInA+iIXOaTKdkUTRMtyy6aNxmFjn7ensRBacu2S85yf3O/zvnfN9p77mkuXwz+njZwNnp5cTytbDZ7CXIPiSW83C7x98jHmfp7r1C29M3eaxt371HTs/dp7bdU5fNHZOJSPJjMRisWRis8HBWTkhw8Ck6nR7gi/Zhbb9KcXTdcth3356o6/gRI9wk0oEDY2s7PN8/dPdOgc09AZb2m1DvvgPVrbcgp6TDzAwKsKLM9hkLY7FamMFBfzKZTIHR6PFr3ze13tE10VvXeu2ZrXMCrCiHq+c+6G1jR/ACjuaR/uauq1DtuAhV9kteATT150BjHYNi4+m7+KaXEMbFLYqICKuh0chr9I0XVmnMJ8GxZxLq2m+AyfUdij0LRZp+KFQfANLwzp0fGGr77uvMw1BuHIIy4zAoDUNQoj8Kcs1hkKoOT29JlpcE0akGdGLcUHv0rJAQOy2Q8mhzXLpSLHM9kat6oMJ8BmSqXhDkOYGfZYF0ccMzksdj9Cstb3ugqNgPsvL9UEBYnrIbcoo6QVjQDlyekscKDo5G7ZmxmNDQEAWV8tWhNIG2oki193l+SQcI8+yQKqoFXmYtXiRFaHqKX1mcbz6aK28BEXKK8l0glLpQ9UZIy6qDpIyqB/iml4iIiPiSxWJWoccFZcaRJVlSK+QpWr0nhu1iG548LdsymSoy2fGAXJmFniba8XuqwAjcNC0k8DTA5WshKV0HcQnZLtQeG2qNc8ZCQkJ2BjEYfzMYjJzsbI+fUFJ3OCvP+pdI6kSnN1/jZdUWcPjyj/DkMxQWO6L5It1oQgr2x9Zk5XMuX3U9NV0lQtLCMBpt5cuGWpTADAragwp97osmkTLzrWEiSYMYPS70eeZgb/l2yLFrvFkkkn0qkRjJAMbXb0RwOJxXT/c26u0nQ51t58HVdQ1M7RN8wv3/YW480ehoG4Ma2wjssF14WNczvZSQ3pkRgUDawtnsbdF8DJZjl022U6CuOgRVDWegSD/kIaS3MiwUfnFFJusbzciEpnUxYGNvjCIkH2rr4MeV1Ud+q6weBKXuIGSI6x9z0yprCPmNnM/Ny7kszf/1pqIYdm2MBVdkDDRFbXpgZsesILaQSDrdwHKFugdKtV8jO4je3oHrhPSvXMwqWDEmkQ7eUCjgSoEMumO3QEP4BrCvi4Zd6zdDU2T0JXdoqG+iekfr1mSsVpjbMFiEXvcyw3HAzOfe+EOfFUtO38PK4VSGEOrC2VC4eg3o6SxwRm7Ci3RuiAV7ZMxeYrsPAFgglrdNFZb3gEJ/7LZnFPwI6RVuqJVhqOfQExsPmD8VilavhbK1gVC6hgLVzAhwRvmKdHFQkXXRKiLMR6bUmS1RtOMzSWk63Um4XwBoNPQnpZxoiVwPhavIeFJvcq8pvUYOAEtoFF7EjW7hjIzREaGzbM+2jIjyGlGRXqhoGCsh3DhGo3EhRqEdryCSzjVvAe+t7OyN3nY9sXM4y4jQWXhi7ScpAsMkX2SCfGw/aGzjSkLCEZLJizD/wB+0FDp+6vlFKFAfHAYN7A37iJD5JG2vCOSmaX5OTteDpNQDKsuFbkf30xd/vcLFfitV/tRHFRTaK8m9a20AHcop1EPyVdTPiO2vJzGxjJyYqh7fxtegEd4MBer+h5jlfFtN60883cD0cqU/NcabsBy1BEPJ9QEMUPvT7mAUxruPGj6f/34CT2WM31bySzIa3ZLiTijdcRR9kPq0Xr3EP0BuCAyCSlRIRaG2FTIYi/HA/0pSUtFSLg/jJ/MwU3y8IB65FvgUEqnMn2rAAmgJxHIOJNI/voywhihzFAwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

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

            def replace_obj(self, tuple_data):
                rhino_id, geo = tuple_data
                layer_name = rs.ObjectLayer(rhino_id)
                lock_factor = rs.IsLayerLocked(layer_name)
                if not lock_factor:
                    if self.factor:
                        sc.doc.Objects.Replace(rhino_id, geo)
                    else:
                        Message.message2(self, "Enter True to replace the object！")
                else:
                    Message.message1(self, "The object to be replaced exists in the lock layer！")

            def RunScript(self, Guid, Geometry, Replace):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    id_len, geo_len = len(Guid), len(Geometry)
                    self.factor = Replace

                    re_mes = Message.RE_MES([Guid], ['G'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if id_len != geo_len:
                            Message.message1(self, 'The number of the objects is different from the number of replaced objects！')
                        else:
                            zip_list = zip(Guid, Geometry)
                            map(self.replace_obj, zip_list)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    if not self.factor:
                        self.Message = 'Replace Object'
                    else:
                        self.Message = 'Object replacement successful！'


        # 通过图层名筛选物体
        class FilterByLayer(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FilterByLayer", "C22", """Filter objects by layer name""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def get_ComponentGuid(self):
                return System.Guid("f94e605b-c07d-4f35-92b8-f097493206e6")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Layer", "L", "Layer path name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Updata", "U", "Update button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Type_Out", "T", "The way an object is output（True：Referenced object，False: Guid）")
                TYPE_FACTOR = False
                p.SetPersistentData(gk.Types.GH_Boolean(TYPE_FACTOR))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Object", "O", "Eligible rhino space objects")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAR7SURBVEhLtVN9TFVlGEdX4JVABmgSHxfhcrn3nPOej/uJEF75uEBgQARRSKxGkZfiqwRuiIAhTFPm+tJFM+xrNpmCWzQc2txcZrm5NreK5XL94RZW5qy5tMbT79xzQJuEutFve/e+7/P8nt/zPs95TtD/jgKTKUSW5ZK0tLRY3bSwUBTFZFMUcjud7bppYWGz2ZIlUSSXw9GqmxYWNyXYqJtULGaMb2NMOCsy9qMgCLvQRq8oig/q/iCFsWK73Z4gCsJWSWJnsA/BH+pQlErojTFBOCHw/NScCVSixNg4RGtlmZXwHHcdAd8j4Lzqh7AF56sBEY47B34tNE7zPD/qcNha7TYb4VFHZMY6/quCAJAgHcE1ELuIanZjvwAbh2A/xL/B/WfG8x+AU4kqdsNGsiy9D/ul7u7uxQGRmQRpLldLwACkp6aGgXwK7bmA0o/ifBUtq0fgIO7DgsB/CcFOVHYRCU7D/xm4alt22GT5DdindCltitQEmCJ/RUVFMMq/F/3NUScLo2tSORC8BKE2u12wqFxVGL5IJLzMeLYlIAR4PJ4ldkXZAv9lIloUMDocjiRkJ1FghIDfcb4C0ts4n8GLfsA+KUsSIUGPykfwT+j1sHpGFU+BP42WnWWMTWLfb1ekPnD+gltLoL4YPSzDx3wGAXVoWZ3b7RZdLle4JEnPyrLgxY7vxZJWi+IKJPwbQkWBYEARBBED8bzI85UWiyXK6RTN4Jbo7rtDUrzBYTGvOqxf7xghhtDIQSWtbJRXCg5wct4BXi64sZT8YauY+6GFZb+bKmbvk92P7F26NGIAcfdo4bfHovuWLS/LffhF8m87RS09x7CO3rSOUXP3BDV1TVBb/0nyFm+k0PDox/XYu4Inq7Dhl2rfIFXWvn7Lqva9QznrWn4Dz6vRg5asWRZxotdkGUoKDc3B/fYVRUbFDZSu76eSqj4qfqJ3dpWs1+5hy+7v1akgB4WXcrF/XFvrpfMZHhrixe+efiCuHx5FI8yBFC5ze9PmI9TYOU4Nmz6dXY2bx+mFjjEymlf7daqKsKZi69RBh0KUW0jkxcopoJOudNrDiV8URUY3g2PQqDqSLOk76v2Hydc+ShvaDs0un3+Unms9SMYU5yadqiL8rRrnrwMFIl1xeYiyvETZeUR563DOp9LlKygkJCRJ52qYL8GGthFKTHV36lQVwX3l0rn9DRn0iVXShLML6Fu7m3wxsVSdYLyOBIk6V8NcCXztI9SMaVLPMUbtb56BMzmq56utD1GPLZUmrDL1JCTSo3j5a1aOXjZbpkGZv4LA90D/ix7rmk7mMveCYtSYs4j/qD7jWkcWT5UR0dRlXEX7OIHGbE5qSTH/CX+MRtMxk6ARwursl9W8Svj5RuCya4xb0VJoHt6WK9Cb8Sb62MrTIVGmnUiSvzL2SZ1yA2bes/OlV45TVd0eUtxlx2FS53te2PmotTV8PL1nsmBUGXWkmD+3RkRk6u5/Iy5R3uVaUzUZHGwo1013hESDYax8ZczXclSUTzfpCAr6B6uo5pTv7c+BAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.output_type = None

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

            def decorate_obj(self, data_array):
                ref_brep_list = []
                for data in data_array:
                    rh_guid = System.Guid(data)
                    gh_obj = objref(rh_guid).Geometry()
                    str_type = str(type(gh_obj))

                    if 'Point' in str_type:
                        rh_obj = gk.Types.GH_Point(rh_guid)
                    elif 'Curve' in str_type:
                        rh_obj = gk.Types.GH_Curve(rh_guid)
                    elif ('Brep' in str_type) or ('Extrusion' in str_type):
                        rh_obj = gk.Types.GH_Brep(rh_guid)
                    else:
                        rh_obj = None
                    ref_brep_list.append(rh_obj)
                return ref_brep_list

            def _find_guid(self, tuple_data):
                layer_name, origin_path = tuple_data
                temp_array = map(lambda layer: [str(_) for _ in rs.ObjectsByLayer(layer)], layer_name)
                if self.output_type:
                    guid_array = map(self.decorate_obj, temp_array)
                else:
                    guid_array = temp_array

                ungroup_data = self.split_tree(guid_array, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Layer, Updata, Type_Out):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Object = gd[object]()
                    self.output_type = Type_Out

                    re_mes = Message.RE_MES([Layer], ['L end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        layer_trunk, layer_trunk_path = self.Branch_Route(Layer)
                        zip_list = zip(layer_trunk, layer_trunk_path)
                        iter_ungroup_data = ghp.run(self._find_guid, zip_list)
                        Object = self.format_tree(iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Object
                finally:
                    if self.output_type:
                        self.Message = 'Output type：Geometry'
                    else:
                        self.Message = 'Output type：Guid'


        # 通过物体名称筛选物件
        class FilterByObjName(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FilterByObjName", "C23", """Filter objects by object name""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def get_ComponentGuid(self):
                return System.Guid("5a48ff57-2d25-4a80-a557-aa506671a6e5")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Object name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Updata", "U", "Update button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Type_Out", "T", "The way an object is output（True：Referenced object，False: Guid）")
                TYPE_FACTOR = False
                p.SetPersistentData(gk.Types.GH_Boolean(TYPE_FACTOR))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Object", "O", "Eligible Rhino space objects")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASHSURBVEhL3VV/TNRlGD+3RhHIDwPPcReIHudx9/153C+O484TsEPkEAakyNRp0OGQH5qAnRCFioAM+7ERatpKV8MlFNJQtFFTIpnMwZbFVo3+yTbLtdXW2uTt8973y5l1Vlv1T5/t2fs+z/N5ns/7Pt/vfU/x/4AgCCk8z2fIrgJ7FWK87P5zsCz7RlpaGjGbRafkG/wcx94MJP8NQOAkFeA47gr1GUbfyLLMjLRnlEaj0Y0bxVOfruBGi6Joor7NZgtHPo3uKSwWSxTyG9ArWQ4FBN7mee4qwzI/mc1mE6vXV+IGVzAqAevXyE1DcA5Nk8AdQ2wOse+wXkT8Kqb5Aw7Sk56evpTeHLlJrN8g5pIFmPd4kT+Ck3dwPPcxzzPVIEziJHE43UqXyxUDziya72QYwwxG2Gq3iwloTFhWvxUcG/JfofHryE3SgyA3BIGJoAAncH24VgQa/Cif4KLD4YjFOgD/OtY7PM9WgHsNhelSneGWRqNROxxCPMcxs8hPgDcHzhQEriPfuyAwhOZvykXdJlPgeZxBUQcKbuAGj4BzA7EaKoB1DSFkEQ7zrU6n0+I5qBD/FAcZRf1woClQUlISFtig0SXM+6y05+gc72JUNFaIwtsYzTCKqaiPNoKfTQWw/1mr1epMJtPjEPveaOTdqL0F+wD8a+DVBgTwZuDZmoWAAxgMBjNidrpHUw+I2+hbA0vAPos+Gzm3HhYh3ZD10hidPw5WDb8Y44uisf8cD4dHLDkm2ooGDaKnXy+s7TcInnsmPnE2lcs+rWPXnNRxWacES8HpRyNje1D3kFT+11gUGR1flJ2/mzQdniD1rZdhl35jl0ndc6OktmWUNBwaJzkFz5CIqLiNtE4qDwmNvN4Hl3vdrtvlVcfIkzte+oOVVx0nWevr74CXI9FDIoYRc86UbGn/xbW24pw6UV8txyUseUzdvWHzIVJQdpB4N7UFrWCz5C+OVrbJ1FBwunN9s81d46S99zPy/ItT0+aM4gtyTkKKPrOjtvkCqdk/Qnb53w9aTfMIqX52mCRp05tk6n1YlrDKv3F71/zBV2YIFdjX/uF854kvidW5KfA9C2KFzt61s+ldUtU4SHwN54JW1TRInt77DklKMftl6gL0oiV/tL7lPDnw8jTZd/gjsh8CByBUsq3zrjqZ2yPzJPyZgK9hgCzXWptlqmKpSlfJitlDDW0jfe29N0lT+xhpPTpF/J3jxO3x0U998P8liFACVY0DpA5vE92rkvh60CI0qRnHM7O3vpazzutUqcKtLd2fDNKR+Pa+RVI59ylwQv/Afi8QeB6Yf15py3yKYXXv4hhlvmDJ6/cU+OpsZtGjTVQmq5UKS3lFW0N+qf+LyOi4HXKr0FgQqEFj+u4Xbekk+PENIBX4Q4mNS3zK6ig8YU1b4dCtTDTaraI3r7Cm2SDmUE7wU/NAaA2uI3teGCNllb1EtBaNIZQlZe5hWYK2z+7M3e31FjlX51b0aVLtryL897456uVCj8VZ9nlYWHixHAoFtVbvOG/NLB1SJqzaLsceAIXiV+CS4GM0MX8wAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.output_type = None

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

            def _find_guid(self, tuple_data):
                name_list, origin_path = tuple_data
                temp_array = map(lambda name: [str(_) for _ in rs.ObjectsByName(name)], name_list)
                if self.output_type:
                    guid_array = map(FilterByLayer().decorate_obj, temp_array)
                else:
                    guid_array = temp_array

                ungroup_data = self.split_tree(guid_array, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Name, Updata, Type_Out):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Object = gd[object]()
                    self.output_type = Type_Out

                    re_mes = Message.RE_MES([Name], ['N end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        name_trunk, name_trunk_path = self.Branch_Route(Name)
                        zip_list = zip(name_trunk, name_trunk_path)
                        iter_ungroup_data = ghp.run(self._find_guid, zip_list)
                        Object = self.format_tree(iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Object
                finally:
                    if self.output_type:
                        self.Message = 'Output type：Geometry'
                    else:
                        self.Message = 'Output type：Guid'


        # 将CAD中的物件导入到Grasshopper文档中
        class CADImportGH(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CADImportGH", "C14", """将CAD中的物件导入到Grasshopper文档中 -----> Test""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def get_ComponentGuid(self):
                return System.Guid("94336aac-a48b-44b3-bada-5dbcf54fe105")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "CAD_File", "F", "CAD（The suffix is dwg）File path")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Pick", "B", "Input button, use the Toggle button and set the Toggle button to False when closing the GH file")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GH_Obj", "G", "Objects in a Grasshopper document after conversion")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARhSURBVEhLrdR7TFtVHAfwi24LGU7nYxrIYsNjGxbuCnQtfVLaUmwpj5a2UNryammndNAWBpQOKK8Ao8BGQGTsZWhESDaJ0enYFnCik1TCNgcmTp2L7hEfM3tk0xLpT8ATXAUmc/skJ+nv+zvn98e99xRbilulwj1ylW5anMJG0eMD1tefnYmLvwlsPgCLB5fixSTUejw8UmkesDjwHR4JHioTrrB5PaiFAcDq2bUGlf/Pn3zB53e20WCQFHHhh8htnt+iWbeAgPkabO+UVDWemKzf+9mNtsOXXe3OX7XoyMp5clT4DJsLE3jktJ3PD7pApowDPQauxPDzk40HAnL0rfjsUll2HXG19/4ETQevDttbxl9Ax//bTEJCK7C4MBZFHZmrv+LxzMCIgeu0mKn5DffJ29Fpa97/PVR3fjNh3ze+FsXLg8N2X3cs75qbTIPbFOa9P9i8L91s7o/u2cflprHhW66Ih7YuMBR2NbQcugZlu10L72lZHpkkFdixcHb25X4Uhl88FYZfGiLiX4+Gk+4AlQFXGbFH0VYvBdaByar2SbDUfoyjaGkeFu1DYMbCUVKU1yAnnc6/RaWDh8GBKW5SGIoX5L7mEFW0uMBcc6oLRYs5+ycox/S1d8e3kp1vUSiLhgyTyQ2XqYx3R5kcFooWNLW7GDtrjt8rqhv+vaR+pBvF3jq6Tjqtb5z/GZUPRW/a/4GlegiM5e+Bztx7EcXeGncPDtW0furWODx+KFoxmbI0W1twEPRFfaA2dHSg2FtVbV9H277zYN0zmYyiFVMqC19SZNZPa7Z3QkamnWUgY6tR6x/llU5+bfMJsDaOjqPooaSpK85I0qvG5n4bEv3n7oQPWgt8jJYeV1XzJ2Br/qISZSuWpKkLZAnbNwCMrNJqGetyhREb7HbsCdT+m97cHbXdfGCm2H4MZr9rtaNzTL7LMRaI2vOIROKyf3StFl6XOZN2VpVKJygUiidR7C1Tv0er29ENxrJ+MJf3Q05h70nUwjgcgi+XRbAkCTeXieOCk00mwnqb/lX/0lyezpJJmzJpqCBibgISibQeHVlatqGlIMvQBtKMKsjQtoCuqK9pLrcbQzc3WCNDxLyNVEEM4VyOgv6LMUt0O1fCgnQhEQT0IJAKwqXzQx7EZn87y2DqAbmmDlLSykGt3wsa44Dx/TfXbbp+DvMbchT75SmZRwq0QlBL2JAcFwap/KAbIlawpMfB5dUV0wlo1NLU6qaNMk21RZJuGxTLSs4kykpOi2U1ttOHQqOaShVpJp1kKjeNDanicEjgB96VxodMNu5ky+bOKhTENcW66FirkfL8/LCVUodgT1cY48vMWjHolGTIlocelwuJcmXylgB9elSwo5wTjrZi9nziU/kpxAgDmbz4PjyAj0Cg8dPIXol2VOKim5O051CO9ToEfiVaRgAqH91AK473Ora+iEqsWEMNLDOQX0blozEoyM/oU7bg91+iRLL/WjuHswqV/4JhfwF1Arowby8aeAAAAABJRU5ErkJggg=="
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

            def zoom_box(self, geo_list):
                empty_box = rg.BoundingBox.Empty
                geo_box = [_.GetBoundingBox(True) for _ in geo_list]
                for sub_box in geo_box:
                    empty_box.Union(sub_box)
                return empty_box

            def RunScript(self, CAD_File, Pick):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    GH_Object = gd[object]()
                    view_windows = sc.doc.Views.ActiveView
                    view_port = view_windows.ActiveViewport

                    if CAD_File:
                        if Pick is True:
                            rhino_doc = Rhino.RhinoDoc.CreateHeadless(None)
                            rhino_doc.Import(CAD_File)
                            rhino_objs = []
                            for obj in rhino_doc.Objects:
                                ref_cad_obj = obj.Geometry
                                if isinstance(ref_cad_obj, (rg.Point, rg.Brep, rg.Surface, rg.Curve)):
                                    rhino_guid = sc.doc.Objects.Add(ref_cad_obj)
                                    rhino_objs.append(rhino_guid)

                            gh_obj_list = [objref(_).Geometry() for _ in rhino_objs]
                            vbbox = self.zoom_box(gh_obj_list)
                            anchor_point = vbbox.Center
                            sc_trf = rg.Transform.Scale(anchor_point, 1.5)
                            vbbox.Transform(sc_trf)

                            view_port.SetCameraLocations(anchor_point, anchor_point)
                            view_port.ZoomBoundingBox(vbbox)

                            select_ids = rs.GetObjects("Select objects")

                            if select_ids:
                                format_obj = select_ids[:]
                                GH_Object = [objref(_).Geometry() for _ in rhino_objs if _ in select_ids]
                                self.message3('You have selected {} objects in CAD'.format(len(format_obj)))
                            else:
                                self.message2('You did not select any CAD object!')

                            rs.DeleteObjects(rhino_objs)
                        else:
                            self.message2('Open the button to select the CAD object')
                    else:
                        self.message2('Please enter the CAD file path')

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return GH_Object

                finally:
                    self.Message = 'CAD object convert to Rhino object'

    else:
        pass
except:
    pass

import GhPython
import System
