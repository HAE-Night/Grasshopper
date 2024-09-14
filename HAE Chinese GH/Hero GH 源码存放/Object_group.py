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
import fnmatch

import initialization

Result = initialization.Result
Message = initialization.message()
TreeFun = initialization.TreeOperation()
try:
    if Result is True:
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


        # # 物件键值对提取
        # class Data_KV(component):
        #     def __new__(cls):
        #         instance = Grasshopper.Kernel.GH_Component.__new__(cls,
        #                                                            "RPP_Data_KV", "C2",
        #                                                            """Extracts key-value pairs for objects,when no value is inputted for Key.Extract all key-value pairs.""", "Scavenger",
        #                                                            "K-Object")
        #         return instance
        #
        #     def get_ComponentGuid(self):
        #         return System.Guid("af5ef186-5ae8-4eab-a2e8-42b171fa942a")
        #
        #     @property
        #     def Exposure(self):
        #         return Grasshopper.Kernel.GH_Exposure.primary
        #
        #     def SetUpParam(self, p, name, nickname, description):
        #         p.Name = name
        #         p.NickName = nickname
        #         p.Description = description
        #         p.Optional = True
        #
        #     def RegisterInputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_Guid()
        #         self.SetUpParam(p, "Object", "O", "Object set list")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        #         self.Params.Input.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        #         self.SetUpParam(p, "Key", "K", "The Key to be extracted,supporting multi-key query")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        #         self.Params.Input.Add(p)
        #
        #     def RegisterOutputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        #         self.SetUpParam(p, "Keys", "KS", "Extracted key；When Key has no value,it extracts all the keys.Otherwise only Key")
        #         self.Params.Output.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        #         self.SetUpParam(p, "Value", "VS", "The extracted key")
        #         self.Params.Output.Add(p)
        #
        #     def SolveInstance(self, DA):
        #         p0 = self.marshal.GetInput(DA, 0)
        #         p1 = self.marshal.GetInput(DA, 1)
        #         result = self.RunScript(p0, p1)
        #
        #         if result is not None:
        #             if not hasattr(result, '__getitem__'):
        #                 self.marshal.SetOutput(result, DA, 0, True)
        #             else:
        #                 self.marshal.SetOutput(result[0], DA, 0, True)
        #                 self.marshal.SetOutput(result[1], DA, 1, True)
        #
        #     def get_Internal_Icon_24x24(self):
        #         o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANDSURBVEhL7VVZaBNBGF5EVHyxKF4P+tCiLagPCoIIUlSwbTaJ1ip4QZU2m03aZGc3e+8m28OmFkU8QLxARLSHTZrG4oG1HlBBBEVfBGnrswpFiqC0lfGfdStL6QXx0Q8+8v//fDPfP7PDhPqPOcGyns5n5RSq0XuuBuX0tVwYUjPXIsb9c2wstdFZnqJYOR2Sky9xWMvikJLJmbGGZxgaHjhodSywDYJS1/mo+QAzWmcRx3XlMUrHEkZ5vITEE3mlE89GogtKqVs10CyJ/xjI6TOwLVyjppfZhRwREuGolC5MGrMLEwZVWvdKkuse1G3QSCaxXBLe0FRuvNI8/E6SE4ie8KpkuSGafq7QKVFqmbC+eb8pWdsOLA3KmUtTGrDWoxUkN7wCNrzoZqQ0srDBr3yu80uDWmlkuS0GGB5h+4XDzRga6XVKlObhshePNOPGLfsKGP3e2ZkNPGhYo9GNOM13NexTR1BJYLUtdGAVW/Nh8U8JX2yM28vlWcWVi0xv7AepkXFY78qMBiAcqvfLozBplN9ds8kWTYLu4VrOHTqJ495YmU5zJSSGxpJkjJXS12c2oPmBpnIdJ3ziT7E0UmCLJiHujW49VRHHOo3ugEH7qQoTm35hMxmb1cCg+S/AHujufZ1fHiJHYAtdsChrnuZBHy2fNA6N/IIdfXCG5mKARuCYrqo0ym85kIAPLrTawkmAnTa3VCQwIcw56ZTntINxYJbEaimHyO2ADo+T3A2zjN+U8ItjsINR04c2OOXpDQJ6yr4tcEX3uCfAMXjduRsSHV1H6KQ2pjX4W8gRYHCZvElugwtc/BFmpbs7WClTyAidRYS1WrYoILZOeYsIYIG1RDOhJ2Sl9sKglO4kD2cld8N5i6TUUbHxORbq+zBf1+viE/u3WmiL2EIXqvi2E9H4wynm9GI52U9e09fkb8CRg4mYKo+Y9xVWSv0lAwyp3W9jYF6NWnc4Uqoa3dklNDzFYaV70K0nDCsZtVbviQbQn+85KyrFjlXQ6XDEfPCVYbKLjwutayD/Dvx2At3Od2S5gXQsNr4gHfeF1ew7cnTuHf0TBIQ22Tj9BstN/biKbz/mlP8tWCXdwogdyEnnAIr6DXgFXcbMTo/FAAAAAElFTkSuQmCC"
        #         return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))
        #
        #     def KeyisNone(self, Object):  # 当Key值为空时，提取所有的Key值和Value
        #         Key = []
        #
        #         for obj in Object:  # 根据物体的Guid属性获取Key值
        #             obj_attr = sc.doc.Objects.FindId(obj).Attributes
        #             Key.append(obj_attr.GetUserStrings())
        #
        #         Keys, Value = gd[object](), gd[object]()
        #         for _key in range(len(Key)):
        #             for v in range(len(Key[_key])):
        #                 Keys.Add(Key[_key].GetKey(v), GH_Path(_key, v))  # 获取Key
        #                 Value.Add(Key[_key].Get(v), GH_Path(_key, v))  # 获取Value
        #
        #         return Keys, Value
        #
        #     def HaveKey(self, Object, Key):  # 当Key值不为空时，获取Value
        #         n = 0
        #         Keys, Value = gd[object](), gd[object]()
        #
        #         for _key in Key:
        #             Keys.Add(_key, GH_Path(n))
        #             for obj in range(len(Object)):  # 根据key值获取value
        #                 obj_attr = sc.doc.Objects.FindId(Object[obj]).Attributes
        #                 value = obj_attr.GetUserString(_key)
        #                 Value.Add(value, GH_Path(n, obj))
        #             n += 1
        #         return Keys, Value
        #
        #     def RunScript(self, Object, Key):
        #         try:
        #             Keys, Value = gd[object](), gd[object]()
        #             re_mes = Message.RE_MES([Object], ['Object'])
        #             if len(re_mes) > 0:
        #                 for mes_i in re_mes:
        #                     Message.message2(self, mes_i)
        #                 return gd[object](), gd[object]()
        #             else:
        #                 sc.doc = Rhino.RhinoDoc.ActiveDoc
        #
        #                 if Object and Key:
        #                     Keys, Value = self.HaveKey(Object, Key)
        #                 elif Object and not Key:
        #                     Keys, Value = self.KeyisNone(Object)
        #                 ghdoc = GhPython.DocReplacement.GrasshopperDocument()
        #                 sc.doc.Views.Redraw()
        #                 sc.doc = ghdoc
        #                 return Keys, Value
        #         finally:
        #             self.Message = 'Key-value pair query'

        # 拾取图层物体
        # class PickItems(component):
        #     def __new__(cls):
        #         instance = Grasshopper.Kernel.GH_Component.__new__(cls,
        #                                                            "RPP_PickItems", "C12", """Pick up the objects of the Rhino sublayer""", "Scavenger", "K-Object")
        #         return instance
        #
        #     def get_ComponentGuid(self):
        #         return System.Guid("1947d440-6dc8-4eb7-8338-c936a5f54a4b")
        #
        #     @property
        #     def Exposure(self):
        #         return Grasshopper.Kernel.GH_Exposure.secondary
        #
        #     def SetUpParam(self, p, name, nickname, description):
        #         p.Name = name
        #         p.NickName = nickname
        #         p.Description = description
        #         p.Optional = True
        #
        #     def RegisterInputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_Integer()
        #         self.SetUpParam(p, "Father_Keys", "K", "Subscript of the Father layer")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        #         self.Params.Input.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_String()
        #         self.SetUpParam(p, "Unique_ID", "U", "Unique_ID")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        #         self.Params.Input.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_Boolean()
        #         self.SetUpParam(p, "Switch", "S", "Plug-in run button,input 'True' to run,default is no execution")
        #         p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        #         self.Params.Input.Add(p)
        #
        #     def RegisterOutputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_Geometry()
        #         self.SetUpParam(p, "Data", "D", "Picked up objects")
        #         self.Params.Output.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_String()
        #         self.SetUpParam(p, "Info", "I", "Pick up the layer information")
        #         self.Params.Output.Add(p)
        #
        #     def SolveInstance(self, DA):
        #         p0 = self.marshal.GetInput(DA, 0)
        #         p1 = self.marshal.GetInput(DA, 1)
        #         p2 = self.marshal.GetInput(DA, 2)
        #         result = self.RunScript(p0, p1, p2)
        #
        #         if result is not None:
        #             if not hasattr(result, '__getitem__'):
        #                 self.marshal.SetOutput(result, DA, 0, True)
        #             else:
        #                 self.marshal.SetOutput(result[0], DA, 0, True)
        #                 self.marshal.SetOutput(result[1], DA, 1, True)
        #
        #     def get_Internal_Icon_24x24(self):
        #         o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARvSURBVEhL5VVraBxVFI5a6osWhFalIiiKomhEml+CBMGCFFssGmyTNpvsbOY9+5qdxz6SSVtDEtLUZzEbkyabZDfZzc7uZje7adKmaZXGVGmhvqCg6B9Rq9hYsLS+xu8uQyE/JBv0nx9c7txzzj3n3nO+c6fq/wPaH98kRIov8qG8WwjlXUKoWGOr/h1qa411vJ7vEkLTfwYOvm952uYsX/sJK3DwtCWGpj9rCUw8b5uuHZJUulUMTi/oXUsWr+dGWf/k007nwIZmKbmZVbP1CPC12nHGcslJyt6yNtDK5JDW+aHFaOYussZN9iE1A7hNB+NL3kdkCFKUcRtOTm0l64rBBHOPk40tcuoAWcPRJ3D8JadmB3l9qiSGi9dYNV0P1U1iuHSFCaRPEbuKgRS0knw7jKHbGCUzDqcrHHBafgen5SxOj99FByb3S+GSJQWTm2316mAVM4kU/SAZpY2skll2yuYTtuoGGCX9EauZAqtkn/UfWECwbOVpYtVMjFHMnyl34h5WNS9TvuTDtuoGIF/g1IyfUc1tvv0nLUHNPmmrVgcCcKQGYMiDcDTLgkW2qgwuMFlNUiQouS20nOrntdxvsjxyp61eHaxs3o28/s7puXSDNLoRRf4WYw638nH61GExUrqKwN7dwsAWkh4mYEbtrZXD5Z+Qwj3nLLCn+1XuyP0I8IYYnv5YDBXmUPQXnJ7RR6XWY9+LkZlLtD+/yd62NoBBbXrXWQu0PF9VV3eLLa5yecfLhXVHjn1HecYfs8VrgyzPlnMKtmwnzwM5fXmNJvO0zl0XwzMX9tDRTbWGsY7IKwKKVoMcdwrB/JK3/cSPjJYrd7HLl9ildS5aKOwIHywsuttmrzba3cyomXl36+xFdHqMC+Zfqqsz1hP5CtDeRI0ULp4VQ8U/BD3/DeE4RgmpOLSbOlJdtpHTSvjQeUt57QOL8ie3EdleJhqgvPEUq+XOgEmfol7X4OcnRs0yRF8Gp6SfwwmuuyMzJ52+RKRJGu5vEoffbcYMpxhJlnQ0scVGtcWfcpFv6Ha4vIm3Kc/YWw5xuLdJjEUdUkwSQ6Ve0hdo0B5iRxrmlBAqXCDf9XTf503CcIDVMgqC8lrn0lMeY+EBX+/i7YZh3VzeABgpaz1o/JDeubQVBFAZJdveyB+NNjDRGaJvUdKyp23WKhvTqtnsNY7jfS/2OIShl3H613GiwSYplnZ64yZOOE55EzGkYoDyYHjHYk5PfNLpHStizDmlkRK5tYMbpB380L2cnm+G82V0eKEcgIDTzEYpUrqCIL+iUAW8Rd2ULyEjoLSXf8/dQPf569k+mcwY0j6mv6WR79/TKAzvpHwT29GADUKw8CYycYkcFnOfYaRWFnuns3sD+R2CJfNg0i9gDOnkZRTwK1bLnsMLexrjOGTzWC+xau4ibC6j6Qi7/sL8BQjS4fKPP2K7/GfQRv4OLjhVzQdzr8CZBseHUbSjeNzioOUI/gvv4C9ncGqumQtPPyMFS5U/1f8dqqr+Bl7RUaDZ9ES5AAAAAElFTkSuQmCC"
        #         return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))
        #
        #     def __init__(self):
        #         self.factor = None
        #
        #     def find_true(self, str_list):
        #         fix_data = [len(_) for _ in str_list]
        #         index_of_need = (fix_data.index(min(fix_data)))
        #         return str_list[index_of_need]
        #
        #     def eliminate_illegal_data(self, list_data):
        #         result_list = []
        #         for choice in list_data[1]:
        #             result = [_ for _ in list_data[0] if choice in _]
        #             length = len(result)
        #             if length == 1:
        #                 re_result_str = result[0]
        #                 result_list.append(re_result_str)
        #             elif length > 1:
        #                 re_result_str = self.find_true(result)
        #                 result_list.append(re_result_str)
        #             else:
        #                 pass
        #         return result_list
        #
        #     def _get_rhino_objects(self, uid):
        #         object = Rhino.DocObjects.ObjRef(uid[0]).Brep()
        #         return object
        #
        #     def RunScript(self, Father_Keys, Unique_ID, Switch):
        #         try:
        #             Data, Info = (gd[object]() for _ in range(2))
        #             self.factor = Switch
        #             if self.factor is True:
        #                 if Unique_ID:
        #                     duplicate_rm = list(set(Unique_ID))
        #                     sc.doc = rd.ActiveDoc
        #                     all_layers = rs.LayerNames()
        #                     children_layers = [_ for _ in all_layers if "::" in _]
        #                     father_layers = [_ for _ in all_layers if "::" not in _]
        #                     Father_Keys = Father_Keys if len(Father_Keys) > 0 else [_ for _ in range(len(father_layers))]
        #                     value_data = []
        #                     for f in father_layers:
        #                         re = [_ for _ in children_layers if f in _]
        #                         value_data.append(re)
        #                     result_children_layers = [[value_data[_], duplicate_rm] for _ in Father_Keys]
        #                     result = [_ for _ in ghpara.run(self.eliminate_illegal_data, result_children_layers)]
        #                     name_of_list = [name for names in result for name in names]
        #                     Info = name_of_list
        #                     Data_list = []
        #                     for _ in name_of_list:
        #                         if _ in all_layers:
        #                             Data_list.append(rs.ObjectsByLayer(_, True))
        #                     sc.doc = Rhino.RhinoDoc
        #                     Data = [_ for _ in ghpara.run(self._get_rhino_objects, Data_list)]
        #             else:
        #                 Message.message2(self, 'The program does not run by default')
        #             return Data, Info
        #         finally:
        #             self.Message = 'Pick up layer objects'


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
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
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
                # "--------------------"
                self.text_dim = []
                # "--------------------"
                self.which = {0: gk.Types.GH_GeometricGoo, 1: gk.Types.GH_Point, 2: gk.Types.GH_Surface, 3: gk.Types.GH_Curve, 4: gk.Types.GH_Brep}

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
                list_data = [str(_) for _ in list_data]
                return list_data

            def ids_to_objects(self, id_list):
                objects = [rs.coercegeometry(_) for _ in id_list]
                return objects

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
                    elif ('Text' in str_type):
                        text_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = text_object.Geometry
                        self.text_dim.append(rh_obj)
                    elif ('Dim' in str_type):
                        dim_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = dim_object.Geometry
                        self.text_dim.append(rh_obj)
                    else:
                        rh_obj = None
                    ref_brep_list.append(rh_obj)
                return ref_brep_list

            def RunScript(self, LayerName, Layer_Type, Geo_Type):
                try:
                    re_mes = Message.RE_MES([LayerName], ['LayerName'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        Layer_Type = Layer_Type
                        Geo_Type = self.which[Geo_Type] if Geo_Type is None else self.which[Geo_Type]
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        res_layer = self.filter_layers(LayerName)[Layer_Type]
                        rhino_ids = self.choice(res_layer)
                        Bulk_Geo = self.decorate_obj(rhino_ids)
                        Geo = Bulk_Geo if Geo_Type is gk.Types.GH_GeometricGoo else [_ for _ in Bulk_Geo if (type(_) is Geo_Type)]
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
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes", "A", "Object set list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Key", "K", "Key that participate in the filtering")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Val", "V", "Value that participate in the filtering")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Objects", "O", "Filtered object Guid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Key", "K", "Filtered Key")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
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

            def Graft_List(self, List, Path):
                Tree = gd[object]()
                if len(List) == 1:
                    Tree.Add(List[0], Path)
                else:
                    for index, n in enumerate(List):
                        New_Path = Path.AppendElement(index)
                        Tree.Add(n, New_Path)
                return Tree

            def HaveKey(self, Object, key, contrast_value):  # 根据Key值，获取Value
                Obj, Keys, Value = [], [], []
                for v in contrast_value:  # 遍历得到的value
                    for obj in range(len(Object)):
                        obj_attr = sc.doc.Objects.FindId(Object[obj]).Attributes
                        value = obj_attr.GetUserString(key)  # 根据输入的key值得到Value
                        if value is not None and fnmatch.fnmatch(value, str(v)):  # 使用通配符匹配数据, 判断得到的value是否与输入的value相等
                            Keys.append(key)
                            Obj.append(obj)
                            Value.append(value)
                        if value is None:
                            Keys.append(None)
                            Obj.append(None)
                            Value.append(None)
                return Obj, Keys, Value

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

            def RunScript(self, attr, key, val):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Obj, Keys, Value = gd[object](), gd[object](), gd[object]()
                    value_list = gd[object]()
                    Attributes, Attr_Path = self.Branch_Route(self.Params.Input[0].VolatileData)
                    Key_Length = len(list(chain(*self.Branch_Route(self.Params.Input[1].VolatileData)[0])))

                    __attr = [map(lambda x: x.ReferenceID, filter(None, _)) for _ in Attributes]

                    attr_str = [map(lambda x: str(x), _) for _ in __attr]

                    Objects_list = ghp.run(self.decorate_obj, attr_str)

                    re_mes = Message.RE_MES([attr, key, val], ['A end', 'K end', 'V end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        value, value_path = self.Branch_Route(val)  # 得到输入的value和path

                        for index, v in enumerate(value):
                            value_list.MergeTree(self.Graft_List(v, value_path[index]))

                        v, v_Path = self.Branch_Route(value_list)  # 将value_list转为树形结构得到它的Path

                        for index, at in enumerate(__attr):
                            for i in range(len(v)):
                                O, K, V = self.HaveKey(at, key, v[i])
                                if Key_Length % 2 != 0:
                                    n_path = GH_Path(Attr_Path[index].Indices + v_Path[i].Indices)  # 重新整一个路径
                                else:
                                    RunPath = GH_Path(self.RunCount - 1)
                                    n_path = GH_Path(RunPath.Indices + v_Path[i].Indices)  # 重新整一个路径

                                    if all(element is None for element in O):
                                        Obj.AddRange([], n_path)
                                        Keys.AddRange([], n_path)
                                        Value.AddRange([], n_path)

                                for _ in O:
                                    if _ is not None:
                                        Obj.Add(Objects_list[index][_], n_path)
                                for _ in K:
                                    if _ is not None:
                                        Keys.Add(_, GH_Path(n_path))
                                for _ in V:
                                    if _ is not None:
                                        Value.Add(_, GH_Path(n_path))

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
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Select", "S", "Perform operation")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                # p0 = self.marshal.GetInput(DA, 0)
                # p1 = self.marshal.GetInput(DA, 1)
                # p2 = self.marshal.GetInput(DA, 2)
                # result = self.RunScript(p0, p1, p2)
                self.Message = 'Object Select'
                if self.RunCount == 1:
                    def select_obj(id, bool_factor):  # 亮显物体主方法
                        if bool_factor:
                            rs.SelectObjects(id)
                        else:
                            rs.UnselectObjects(id)

                    flattened_list = list(chain(*self.Params.Input[0].VolatileData.Branches))
                    LayerIgnore = self.marshal.GetInput(DA, 1)
                    Select = self.marshal.GetInput(DA, 2)

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([flattened_list], ['G'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Guid_list = [G.Value for G in filter(None, flattened_list)]
                        layer_name = [rs.ObjectLayer(Guid) for Guid in Guid_list]
                        lock_factor = [rs.IsLayerLocked(ln) for ln in layer_name]
                        visible_factor = [rs.IsLayerVisible(ln) for ln in layer_name]

                        if LayerIgnore:
                            if all(lock_factor) or not all(visible_factor):
                                Message.message3(self, "Objects exist on locked or invisible layers")
                                select_obj(Guid_list, Select)
                            else:
                                select_obj(Guid_list, Select)
                        else:
                            select_obj(Guid_list, Select)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

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
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Guid", "ID", "Id of the object to be replaced")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Replacement object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
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

            def temp(self, tuple_data):
                rhino_id, geo = tuple_data
                if len(rhino_id) == len(geo):
                    zip_list = zip(rhino_id, geo)
                    map(self.replace_obj, zip_list)
                else:
                    Message.message2(self, 'The number of the objects is different from the number of replaced objects！')

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
                    Geo = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    try:
                        Guid = [map(lambda x: System.Guid(str(x)) if 'GH_Guid' in str(type(x)) else x.ReferenceID, _) for _ in Geo]
                        Geometry = self.Branch_Route(Geometry)[0]
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
                                map(self.temp, zip_list)
                    except:
                        Message.message2(self, "Guid does not exist!")

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
                self.text_dim, self.curve = [], []
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
                        self.curve.append(rs.coercerhinoobject(rh_guid, True, True).Geometry)
                        rh_obj = gk.Types.GH_Curve(rh_guid)
                    elif ('Brep' in str_type) or ('Extrusion' in str_type):
                        rh_obj = gk.Types.GH_Brep(rh_guid)
                    elif ('Text' in str_type):
                        text_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = text_object.Geometry
                        self.text_dim.append(rh_obj)
                    elif ('Dim' in str_type):
                        dim_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = dim_object.Geometry
                        self.text_dim.append(rh_obj)
                    else:
                        rh_obj = None
                    ref_brep_list.append(rh_obj)
                return ref_brep_list

            def Get_ALL_Objects(self):
                """获取到Rhino空间中所有的物件"""
                settings = Rhino.DocObjects.ObjectEnumeratorSettings()
                settings.IncludeLights = False
                settings.IncludeGrips = False
                settings.NormalObjects = True
                settings.LockedObjects = True
                settings.HiddenObjects = True
                settings.ReferenceObjects = True
                all_objects = [obj for obj in sc.doc.Objects.GetObjectList(settings)]

                return all_objects

            def _find_By_Layer(self, tuple_data):
                layer_name, origin_path = tuple_data
                all_objects = self.Get_ALL_Objects()
                ByLayerGuid = []
                for layer in layer_name:
                    temp = []
                    for obj in all_objects:
                        layer_index = obj.Attributes.LayerIndex
                        obj_name = sc.doc.Layers.FindIndex(layer_index)
                        if fnmatch.fnmatch(str(obj_name), str(layer)) and obj_name is not None:
                            temp.append(str(obj.Id))
                    ByLayerGuid.append(temp)

                if self.output_type:
                    guid_array = map(self.decorate_obj, ByLayerGuid)
                else:
                    guid_array = ByLayerGuid

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
                        iter_ungroup_data = ghp.run(self._find_By_Layer, zip_list)
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

            def DrawViewportWires(self, arg):
                for _ in self.text_dim:
                    arg.Display.DrawAnnotation(_, System.Drawing.Color.FromArgb(0, 150, 0))

                for curve_list in self.curve:
                    arg.Display.DrawCurve(curve_list, System.Drawing.Color.FromArgb(0, 150, 0), 5)


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
                    elif ('Text' in str_type):
                        text_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = text_object.Geometry
                        self.text_dim.append(rh_obj)
                    elif ('Dim' in str_type):
                        dim_object = rs.coercerhinoobject(rh_guid, True, True)
                        rh_obj = dim_object.Geometry
                        self.text_dim.append(rh_obj)
                    else:
                        rh_obj = None
                    ref_brep_list.append(rh_obj)
                return ref_brep_list

            def Get_ALL_Objects(self):
                """获取到Rhino空间中所有的物件"""
                settings = Rhino.DocObjects.ObjectEnumeratorSettings()
                settings.IncludeLights = False
                settings.IncludeGrips = False
                settings.NormalObjects = True
                settings.LockedObjects = True
                settings.HiddenObjects = True
                settings.ReferenceObjects = True
                all_objects = [obj for obj in sc.doc.Objects.GetObjectList(settings)]

                return all_objects

            def _find_By_Name(self, tuple_data):
                Name, origin_path = tuple_data
                all_objects = self.Get_ALL_Objects()
                ByLayerGuid = []
                for layer in Name:
                    temp = []
                    for obj in all_objects:
                        obj_name = obj.Name
                        if fnmatch.fnmatch(str(obj_name), str(layer)) and obj_name is not None:
                            temp.append(str(obj.Id))
                    ByLayerGuid.append(temp)

                if self.output_type:
                    guid_array = map(self.decorate_obj, ByLayerGuid)
                else:
                    guid_array = ByLayerGuid

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
                        iter_ungroup_data = ghp.run(self._find_By_Name, zip_list)
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
                                                                   "RPP_CADImportGH", "C14", """Import objects from CAD into a Grasshopper document -----> Test""", "Scavenger", "K-Object")
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


        class HAEAttributes:
            def __init__(self, hae_param, layer_name):
                self.__hae_param = hae_param
                self.Layer_name = layer_name

            def __str__(self):
                # 自定义类的字符串表示形式
                return "HAE Attributes"


        # 定义物体属性以及用户文本属性
        class DefineAttributes(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DefineAttributes", "C32", """Define object properties and user text properties""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def __str__(self):
                # 自定义类的字符串表示形式
                return "HAE Attributes"

            def get_ComponentGuid(self):
                return System.Guid("313bbcf7-3d3e-4434-9913-b3320a4435d0")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Keys", "K", "A user-defined key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Values", "V", "A user-defined value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Name of object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "LayerName", "L", "Object layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Colour", "C", "Color of object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Material", "M", "Material of an object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes", "A", "The generated attribute value")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAYSSURBVEhLlVVpTFRXGJ3WH5g26c8uaZrU1Co29Ye1BVyw1sGFilQqiyDFoFJUoOISVCwzghUqiJXFrbIIuICKFRiGQUaGtQzLAAOzvHmzzwADw7BpiE3TzOl9z6dtk5LSk3x5y733fO9+53z38QDhq2bz7oVud44HE7R4iwdNi0nQHgkJCR4ymWwh7z9QVfX0raslhq/zCgY+5V79BYrqWTs8YrFTOrWV1mutNK21arQaG6XTWR9W1VjTz2Xai0pKH7jdbg9uyT+QmilNjE0snIjefxGpWY2zwnzV29zQc7hcwxv7lQNISRHgXGYWNJQO9qEhWG126Gg9ym7ewq07FZA1tYkALOCWscgtUMUcP/sY4XuzEX0gF8dSJdibVHmNG34Ot/sZv6CgAGFhYSRCUVVVRchtoHQ09AYjFL19KCkrg0gsQUNj8z1uGYuMi23JgswmxCYWIPrgJUTG5iM26f4fh9KalnFTeLzx8SG+XC7H4cOHIRAI0dvXzxIzCXQ0DYPRhKbmFhQV34BY8gjSxuZSbikvICDgteDwE5bAkJMIChciguxk/7FykqSympvC46nVCv74+Bj0ehpa7qvNZgMbJhJDQxao1CrUiGpRXFKKunopHstaXpYhcvf3O0MjTyMwNBmhuzPwTWweDpx4gPhUqS87QaFQ8PMK29AmV2HUYYXNZkSNpBtp2RI2SiraMaimMKgaIGWqe7mTBlnzRaLJKwxHSESyPCg8BUERQqLHecQcuYmYpEo5m2B0iOKLpQNITKlGSXkbsi414PgZEUnSA8njXvIsxRFBNWStA6BpCvcrH+DHzEyymzIUFt4IZTiiY9K9gyNSwJQqJCodkd/m4ODJh4gXSMJ4lMHAn54eQ3vnILKvPEbRrVZSfz1Ghi2kPGbY7Wa0/KqEvFsFs8WMfqUS5RV3ceXaz8jJzznAfiVByK6TD3eQHWzfmYLwPVnYl3gDMcfuGnm9vQN+gxoThgkhQ8ZcbeTapVCjs4eQmo1wOCwwmQyg9YwuFlTX1CAuLg7+m/30vmtXq9b7rrHz/fzvBUcIXF9xWsQeKUV0fEE1j1Ir+Rm5MhTfaWO/WKXR4fxlKY7/IMKp9FoIM+tQXdfNkjP27SCO89/khzU+n2HD+nXY5LcBq3x8sHzp+0t3RaedCos6gx0Rp3+L2Jd9PTIy63VWA4q2QECIUs6JkZRWg8vFTdBSjE0NrBYnz9ZC9KgHY04Hurq7EeC/GRs+98Vmvy/g4+0FT8+Pg9gyhYQsCIsUrt4WfHQRWzcGarKDqUknLFYTxA09xE2DGBu1EQ2srEWdY3ZSFhN0eiOZY0Xid/HwWrkCqwgxE4sXL3mpw7+is1PBv35TDkWfBhMuO8bGbGhsUbLuycyX4oGoC0ZS/8kpF65cvoQVyz/COt+16OzqQqpQmM/RzI3xUYp/X9SLw8SKDNnl4mYcPV2N8l862OczFyRIzpBA0tCB4O1bsWTxB7h95w5pAeDZzNQejmZuGCglf2bGCWlzPyGrR16hjBXaSXYyOmolzrKgrcuAs+k5WPbhIkRFRREtxjExOQUjpTnI0cwNJelkldZMrGhjyUZINzM90NOrIVbVwGq14OnTCRw5FIf33n0HFXfvkQROkmByfgle2PRGeTvbA2otzTbcC5umZj+CqF6BoMCt+HTlJ+RcUrNizzvB320qOFfH2bSZHHxMYxlR29BHxmoJuQ8CvtxCmnCIiG6ef4ko5XMNmGOgtkHB2nSUlIuJkREbyHFOyjaM7YHbsGnjRvIzGvl/CTrbFfyKKgX5k+nhdNpYcRV9Wlwva8W10hZyyCkx82QSP13IwjJPT/Y/YbHa5p9gyKj2Ky7vIt0qRmuHCnerOolNa3C1pBVFt9txKqMO6bmN6OgaxNrV3sjOvgCnawLTMzOwUJo4jmZuGAcGNj6ZnkC1pI+cO49Ig8nQ209jYsJBGs9BnGVHZY0C/So76uvFEAoEGHeNY3Z2FiatKoGjmRu0XP6GSa32dv/u8LIZdV6zLqPXtMPopevrY8OmU3m5Z21eLhsZm54m97Pse4fJ5G3o73+To5kDPN6fwBXpsIVXyzIAAAAASUVORK5CYII="
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

            def craete_new_mater(self, material):
                empty_material = Rhino.DocObjects.Material.DefaultMaterial
                if type(material) is Rhino.Display.DisplayMaterial:
                    empty_material.DiffuseColor = material.Diffuse
                    empty_material.SpecularColor = material.Specular
                    empty_material.EmissionColor = material.Emission
                    empty_material.Transparency = material.Transparency
                    empty_material.Shine = material.Shine
                return empty_material

            def match_tree(self, data_1, data_2, data_3, data_4, data_5, data_6):
                one_trunk, two_trunk, three_trunk, four_trunk, five_trunk, six_trunk = \
                    zip(*map(self.Branch_Route, [data_1, data_2, data_3, data_4, data_5, data_6]))[0]
                if len(four_trunk) == 0 and len(five_trunk) == 0 and len(six_trunk) == 0:
                    Defult_LayerName = str(sc.doc.Layers.FindIndex(0))
                    four_trunk = [[Defult_LayerName]]
                zip_list = [one_trunk, two_trunk, three_trunk, four_trunk, five_trunk, six_trunk]
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_trunk = zip_list[max_index]
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                return max_index, map(sub_match, matchzip), max_trunk

            def SetString(self, attr, zip_list):
                """将数据写入属性中"""
                for k_v in zip_list:
                    Key, Value = k_v
                    attr.SetUserString(Key, Value)

            def RunScript(self, Keys, Values, Name, LayerName, Colour, Material):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Attributes = gd[object]()
                    max_index, iter_group, max_group = self.match_tree(Keys, Values, Name, LayerName, Colour, Material)
                    iter_group.insert(max_index, max_group)

                    target_Path = self.Branch_Route(self.Params.Input[max_index].VolatileData)[1]  # 得到最长的目标路径
                    if len(target_Path) == 0: target_Path = [[0]]
                    # 创建默认属性
                    default_attr = [Rhino.RhinoDoc.ActiveDoc.CreateDefaultAttributes() for _ in range(len(target_Path))]

                    Keys = iter_group[0]
                    Values = iter_group[1]  # 匹配后的Key和Value值

                    Material = iter_group[5]
                    if len(Material) != 0:  # 判断材料是否为空
                        new_material = ghp.run(self.craete_new_mater, Material)
                        matIndex = map(lambda x: sc.doc.Materials.Add(x), new_material)
                    else:
                        matIndex = [-1]

                    # k和v的数目保持一致
                    for KV_index in range(len(default_attr)):
                        if len(Keys) != 0 and len(Values) != 0:
                            if len(Keys[KV_index]) == len(Values[KV_index]):
                                zip_list = zip(Keys[KV_index], Values[KV_index])
                                self.SetString(default_attr[KV_index], zip_list)
                            else:
                                self.message2("The K value and the V value must be one-to-one correspondence!")

                    # 颜色
                    Colour = iter_group[4]  # 匹配后的Colour值
                    for c_index in range(len(default_attr)):
                        if len(Colour) != 0:  # 是否输入Colour
                            default_attr[c_index].ObjectColor = Colour[c_index][0]  # 输入多个颜色只取第一个颜色
                            default_attr[c_index].ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject

                    # 材质和名字
                    Name = iter_group[2]  # 匹配后的Name值
                    for n_index in range(len(default_attr)):
                        if len(matIndex) == 1:
                            default_attr[n_index].MaterialIndex = matIndex[0]
                        else:
                            default_attr[n_index].MaterialIndex = matIndex[n_index]  # 输入多个材料只取第一个材料
                        if len(Name) != 0:
                            default_attr[n_index].Name = Name[n_index][0]

                    LayerName = iter_group[3]  # 获取匹配后的LayerName

                    # 自定义属性名称
                    Attributes_List = []
                    for _ in range(len(default_attr)):
                        if len(LayerName) == 0:
                            Defult_LayerName = str(sc.doc.Layers.FindIndex(0))
                            Attributes_List.append(HAEAttributes(default_attr[_], Defult_LayerName))
                        else:
                            Attributes_List.append(HAEAttributes(default_attr[_], LayerName[_][0]))

                    for index in range(len(Attributes_List)):
                        Attributes.Add(Attributes_List[index], GH_Path(tuple(target_Path[index])))

                    return Attributes
                finally:
                    self.Message = 'Define Attributes'


        # 烘培GH空间中的物体，并附加上物体属性以及用户属性
        class BakeGeometry(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BakeGeometry", "C25", """Bake objects in the GH space and attach object properties and user properties""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def get_ComponentGuid(self):
                return System.Guid("c76d2908-13fd-443e-9481-89f3661a9742")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "An object to be baked")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes", "A", "Follow the properties of the baking object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Bake", "B", "Bake button")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Bake'
                sc.doc = Rhino.RhinoDoc.ActiveDoc
                self._doc = sc.doc
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    # 确定不变全局参数
                    self.factor = p2[0][0].Value

                    j_bool_f1, geo_trunk, geo_path = self.parameter_judgment(p0)
                    attr_trunk, attr_path = self.parameter_judgment(p1)[1:]
                    re_mes = Message.RE_MES([j_bool_f1], ['G end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        iter_group, max_i = self.match_tree(geo_trunk, attr_trunk)
                        # 添加原始树路径
                        new_geo_trunk, new_attr_trunk = iter_group
                        zip_list = zip(new_geo_trunk, new_attr_trunk)
                        # 多进程函数运行
                        map(self._do_main, zip_list)

                ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                sc.doc = ghdoc

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASKSURBVEhL3ZR/TNRlHMchy5XpktbWarZ0Nf/JlLsDD0LuDoRNQEQZv+SXwB0gvxGQH1LD5STBIYFMa/HrQDjguAPl/BH+YEJphYqSkq6tVuRkAbUyJIT7vvs8z+Ph0Vyb//baXrv353s/nuf5PM9zDv87NpMfishZRPaQb/JKkEzKRHx6XMh75DJeCc6Te0Tk1JEGETnPkxnks7wSvPXo9YlcIVUiclJJs4gcN/IG6cgrB4fnyFFyE6/E829J9rknco30FJFTTNrP+G3yFsnaZ6OKPCwi5xh5SMSFKMifyBd5JWCziRCRk0QOiDhPPtkiIieOtIi4ENYK+5n4kWxA+/4Ok1oR5zlFFojIySFNIj7mNXKMXMErwecka5ENNcn6vZhXglXkBPk6rwSXSLZ3C9CRZ0XkLCHvkOwHbNSTlSLOU0MaReSsI8fJl3hlx37yiIgcNiPW/6W8EvSTgSJyWOvYJDx4JaglG0VcyG7S/rSwFYyQK3kluEgGiMhh77ETxe4C4xnyJml/CufxItkG2s43g/UyVkROB2m/mexCse/Y9uRlkg3wCq/+BVsuuwPLeSXIJj8QkcOOKFuFDbbK26Tt5rK+swFe5ZU9ktS9bF+O1/bR5pBsqzHOYLXEf/HnZyE93xwMiZg5l7l2xhS9pkir9HVwXFT+6Cs22MGwnRi2enbL7ffEwWHOkrXd2hr1q2SOmMZwOtAbCxijgc4QoCEYuKAFuiIgnYqcliwxX88ZtJHoS9ZIxuj3vBUrS+kn7NvIThQ7MAK0FDrNfhz8BxoCIVV4AD3hsFpi8KA6CKjfAutRH8x1hgHmCEBPA7bR8yZyIAXoDoXUF/+XtSm6+WZfydLfK4OWr3Jawo774zswuS84fGq/LyYqfPCgyg9T9CqZw/B9mT/u5LlhpkYDqc4POB6Fh1XBkI7QoAfdIZkigZMxwDFaoSkEfxtj70qnE8alhoBRqX5LtSRVvMAHuF7sH/Pd+2pczlViqEiFa9memPxIjV9q/HEmxQ2DWa4Y26vE7Ke+GK8OxGhpIMbp/fEyFWZ7UzFRvhmzNTSBpkCgP4NaGwq0bMXk4a3nO0LpD9FSGOB0IsPj7rlMV3TvdEaXToaTO+QY3uuJviI1zDFr0Zv4Lm5kOePnMm9cKdyE60W+uJTsjHu123CLVn97tzd+K1Vjri0ckj4QU2Vq3K8MwOAeTSZfhTFjo8yU6j7YolNMG5IU6NAqcFzrjNPpcrTHrUFD2Gq0Rb2DC2ku+LKABqZVnk1TYSjPEz8e8MJXeRpczVVh7IAP7leoMJJP3SjwwkDxxqt8ABuGlKA3mtO9PVtTN+xqjF/f0hgrH9LvcJ7qpFWZdOvQmSSDOUUOc7KMT6ItTokzaUpcpL3qz1KSnricQ4Onq9Gf6wFzlprdq//GlL9tRXuKJrw10aO8SbfepE9w+UGfIJdatTIY2CDxcnQlK3Ai1RlmmoCRnht1tPpd7qhN2sD+tp+OjpKSxeYcv9WGNLWmLVUTpU/0yK2LV9Y16VxH9FqZ1L5TAb1W/vCTBOUhAI7/AF8uE7240dflAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                meber_list = dir(ref_obj)
                ref_obj.BakeGeometry()
                if 'Value' in meber_list:
                    gh_obj = ref_obj.Value
                elif 'Objects' in meber_list:
                    temp_obj = ref_obj.Objects
                    gh_obj = [_.Value for _ in temp_obj]
                return gh_obj

            def sub_match(self, tuple_data):
                # 子树匹配
                target_tree, other_tree = tuple_data
                t_len, o_len = len(target_tree), len(other_tree)
                if o_len == 0:
                    new_tree = [other_tree] * len(target_tree)
                else:
                    new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                return new_tree

            def match_tree(self, *args):
                # 参数化匹配数据
                len_list = map(lambda x: len(x), args)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = args[max_index]
                other_list = [args[_] for _ in range(len(args)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                # 插入最大列表，获得最新列表
                reslut_list = map(self.sub_match, matchzip)
                reslut_list.insert(max_index, max_trunk)
                return reslut_list, max_index

            def create_layer(self, str_name):
                # 创建图层（包含子图层）

                def add_childlayer(father_str, child_list):
                    # 创建子图层信息
                    child_name = child_list[0]

                    father_index = sc.doc.Layers.FindByFullPath(father_str, True)
                    father_layer = sc.doc.Layers[father_index]
                    childlayer = Rhino.DocObjects.Layer()
                    childlayer.ParentLayerId = father_layer.Id
                    childlayer.Name = child_name

                    new_father_index = sc.doc.Layers.Add(childlayer)
                    new_father_name = Rhino.RhinoDoc.ActiveDoc.Layers.FindIndex(new_father_index)

                    child_list.remove(child_name)
                    if child_list:
                        return add_childlayer(str(new_father_name), child_list)
                    else:
                        return

                layer_name_split = str_name.split("::")

                many_layer_name = ["::".join(layer_name_split[:i + 1]) for i in range(len(layer_name_split))]

                childlayer_list, fatherlayer_list = [], []
                for index, layer_name in enumerate(many_layer_name):
                    layer_index = sc.doc.Layers.FindByFullPath(layer_name, True)
                    if layer_index == -1:
                        childlayer_list.append(layer_name_split[index])
                    else:
                        fatherlayer_list.append(many_layer_name[index])

                if childlayer_list:
                    if fatherlayer_list:
                        new_father_name = fatherlayer_list[-1]
                    else:
                        new_father_index = sc.doc.Layers.Add(childlayer_list[0], System.Drawing.Color.Black)
                        new_father_layer = sc.doc.Layers.FindIndex(new_father_index)
                        new_father_name = str(new_father_layer)
                        childlayer_list.pop(0)
                    if childlayer_list:
                        add_childlayer(new_father_name, childlayer_list)
                    else:
                        pass
                else:
                    pass

            def _new_bake(self, data):
                def sub_bake(o, a):
                    # 第一次引用Bake主方法，获取Bake结果
                    if 'BakeGeometry' not in dir(o):
                        return
                    try:
                        first_bool = o.BakeGeometry(self._doc, a, System.Guid.NewGuid())[0]
                    except:
                        first_bool = None
                    # 若失败
                    if not first_bool:
                        o = o.Value
                        obj_member_list = dir(o)
                        if isinstance(o, rg.InstanceReferenceGeometry):  # Bake图块
                            block = sc.doc.InstanceDefinitions.FindId(o.ParentIdefId)
                            sc.doc.Objects.AddInstanceObject(block.Index, o.Xform, a)  # 将图块bake

                        else:
                            if 'ToNurbsCurve' in obj_member_list:  # 矩形
                                o = o.ToNurbsCurve()
                            elif 'ToBrep' in obj_member_list:  # Box
                                o = o.ToBrep()

                            sc.doc.Objects.Add(o, a)

                # 分解数据流
                obj, attr = data
                if 'HAE' in str(attr):
                    new_attr = attr._HAEAttributes__hae_param
                    Layer_name = attr.Layer_name
                else:
                    new_attr = attr
                    layer_index = attr.LayerIndex
                    Layer_name = str(sc.doc.Layers.FindIndex(layer_index))

                if self.factor:
                    # Bake至的图层；若不存在创建
                    self.create_layer(Layer_name)  # 创建图层
                    layer_index = sc.doc.Layers.FindByFullPath(Layer_name, True)
                    new_attr.LayerIndex = layer_index

                    # 判断是否为HAE内置属性物体
                    if 'HAE' in str(obj):
                        new_obj_list = [_ for _ in obj.Value.list_data]
                        # 包内所有空间类型为包的Attr
                        guid_list = []
                        for _ in new_obj_list:
                            gid = sub_bake(_, new_attr)
                            guid_list.append(gid)
                        # 将Bake出来的物体加入到群组
                        guid_list = filter(None, guid_list)
                        if guid_list:
                            self._doc.Groups.AddToGroup(self._doc.Groups.Add(), guid_list)
                    else:
                        sub_bake(obj, new_attr)

            def _do_main(self, tuple_data):
                # 分解集合数据
                geo_list, attr_list = tuple_data
                # 转换数据类型
                attr_list = map(lambda x: x.Value, attr_list)
                if not attr_list:
                    attr_list = [sc.doc.CreateDefaultAttributes()]
                # 获得最新列表
                map_list = self.match_tree(geo_list, attr_list)[0]
                sub_zip_list = zip(*map_list)
                map(self._new_bake, sub_zip_list)


        # 分解HAE属性
        class DeconstructAttributes(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DeconstructAttributes", "C31", """Decomposed HAE attribute""", "Scavenger", "K-Object")
                return instance

            def __init__(self):
                pass

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def get_ComponentGuid(self):
                return System.Guid("00160982-9e59-4509-be7f-cbdbf98345a0")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes or Referenced", "A", "The geometric object or HAE attribute to be decomposed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Keys", "K", "The key of the decomposed property")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Values", "V", "The value of the decomposed property")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Name", "N", "The name of the decomposed attribute")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Layer_Name", "L", "The name of the layer present in the decomposed property or object")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Color", "C", "Attribute color")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Material", "M", "Attribute material")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                sc.doc = Rhino.RhinoDoc.ActiveDoc
                # 插件名称
                self.Message = 'Deconstruct Attributes'
                # 初始化输出端数据内容
                Keys, Values, Name, Layer_Name, Color, Material = (gd[object]() for _ in range(6))
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    self.j_bool_f1, attr_trunk, attr_path = self.parameter_judgment(p0)
                    re_mes = Message.RE_MES([self.j_bool_f1], ['A end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将属性与树结构集合放入多进程池
                        zip_list = zip(attr_trunk, attr_path)
                        iter_ungroup_data = zip(*ghp.run(self.temp, zip_list))
                        Keys, Values, Name, Layer_Name, Color, Material = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                sc.doc = ghdoc
                # 将结果添加进输出端
                DA.SetDataTree(0, Keys)
                DA.SetDataTree(1, Values)
                DA.SetDataTree(2, Name)
                DA.SetDataTree(3, Layer_Name)
                DA.SetDataTree(4, Color)
                DA.SetDataTree(5, Material)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAXQSURBVEhLrVR7TFNnHK36h04c5Q3yKPhmMy46JjNbtrmh29Rplrn5iDOLbBnJZEs2M3VRhiJOVHwgPhBQEGgrDKFAeUOhQAELVmmB0ncL5VUKAgryvGdfrzfZFs3UbSf58t3ce79z7j2/8/uxXhRAALvP7LcMYM1ibv0/oKhXgh6N+PDMRk+BvtXjPSIwk3n070FRLHeKsttHUfZN/Z12kFXNiGUe/TcMD3/sOvTgxMnJyVArsBuj1k9RKvguO5WvWXs08tyG6JiYVcyrL47JyQWbp6iVXYNDzcjKLocwvwpKVQ80+m5odXqkcrm4mnBtUiyp38QceX5MdPkHUKMcClMrkCdIwtbPdyE4OBjShgbo9HpaoKHxDtJ4fOQKC8fLxZIPmKPPh3EJJxLtHoByEWqrc7A39CccDguDQtEMjVYHlVpDC1WIxeDybyIvv2iEiLzFHH82OlJ91/bzXTAh8oFRJ0WLUoOWViUMRj30Bi1a21RobzdArWlDTm4e+OkZEBYUD9bWNrzOUDwbWaF2X7bFcJCUlA2+4C66u02Q3mnGmctlOHa2CNFkLxbJIFcokCfMJzXhIUuQaykpqV3BULAg9/W3CHxX/S3Kfaneq6fLPaKoFNfFvJCA9XKZdOT0lUocP1+M8FOFyBJK0dyiQkHpHSJUjIpqOTQaFV30mNhLiI65kEXpXT8aE3mKenjzc1XxniuJwAyGnsVqPLCQ/YjrbkGBEx5E+B/XG82G7h4zyirvQtGsgqW3ndijJ7uJ3pUqNV2Pe01NiI3nIvPi19Qo3wFNJ9xOELqnd/l00kIR8h2AdD/cSMxBvkiBgf4OurgJaVWIulCC+BQxGmQtMBh0pBZaImJAvUyBzEu/WEu2zgpiqJ7EROrK1RSXM4EENnCDgzpxBQ6fLkdsYgWORhfhGrcaktsKcDPrEBZVAFFVE4yk+FqdDr0WC2rqGjMYqqcAmDF9cVEDLrkDUY6YPuuDLk0jVHoTMgT1qJM2w9rXAbPZCKu1g/5yOamHVqcl8dXC2m+F0tCZaqOaiF+8hkrz+nEs1iOp+9j8IzT/VPTy7TjlDRx0AQ44ARELkJwgQF6ZHMODncQiLa4ki/Hb+RJcTqrE7cYWGE16mty2jN19MNWVtFAR8ySIc8d0pDvkIW78hhD3QFZ4ePjM6f1+MuxzxdT3Lpje64Cpn30hrRQj/Gw5zl0V4cjpQqRkSEhcW5CRU49fTxbSFplMRroBW9v7cL/qGnB8Nqyhzshc57GP/nIbqB9WvYYQL0zuccLYHmeMf8XG6Lfe6FE1QmvqQHa+lCbuJ9bYeqLfaqZHRnOrmvaf7nBzH3pKEoFv5kC9032kYFegPUNP7Nm+dDt2e+DRDieynDH2BRuTwRykkhSV1rRiiFikJ4lJvlmDUxfLcJ1Xg3tyFUykozVEwCai7iICQvIH2+bCstNrXLd7IYehZ7GMazmbsMUN41uIwGYisJEI7PBBdaEIh6LLaO8jzhSReFZBLJEjJV2CwyRFtmvb2KAFuq3oEVwHNs7FxDYftH/m9y5DT0aDv7+zfo3zQ3xILApyxsT7bNwP8kZXiwxKkiLurTpU1cppa/osHRgY6ISyTQM5aT496QGbXeoeIpBJBN4hAhs9oQjifMLQP0bhMreQkUCSoLeJwJtsDAdywI0TovqOCsNDXXQ807PrcT5eBH5WHZ2qjg4T8f/xCFf3EoEMYlHAXDS94TaducrPl6H+E3l+rvstrxKR5aTRAnxRkl+LsLg68IRNiEysxXleAwpvqxF3S4ZDF4ldcgMMJP/qXgvaRscxnM3F2BI7JC/ziWAon0Sah8uGNi+HNiz1Ang3IMsUDl84eGVMfiEJo4UCDBZkY6hIAGUKH6q0m7DkZmFAcAujpcXQR4Thd/vZ0QzVP8F3TsV8t509L7+UOOhkf0a6hL3O4OWYY3FhP4QrmVO25eEIuJPlykavi/0jueO84oTZs9YzBH8Bi/UHFiNilcB45zoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def temp(self, tuple_data):

                attr_list, origin_path = tuple_data
                k_list, v_list, n_list, ln_list, c_list, m_list = zip(*map(self.break_attr, attr_list))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [k_list, v_list, n_list, ln_list, c_list, m_list])

                Rhino.RhinoApp.Wait()
                return ungroup_data

            def break_attr(self, single_attr):
                # 判断属性是否为HAE属性或者是引用的物体
                if 'HAE' in str(single_attr):
                    true_attr = single_attr.Value
                else:
                    true_attr = single_attr
                # 获取HAE内置属性
                if '_HAEAttributes__hae_param' in dir(true_attr):
                    attr = true_attr._HAEAttributes__hae_param
                    layer_name = true_attr.Layer_name
                elif 'NewGuid' not in dir(true_attr):
                    ref_rh_id = true_attr.ReferenceID
                    attr = sc.doc.Objects.Find(ref_rh_id).Attributes
                    layer_name = str(sc.doc.Layers.FindIndex(attr.LayerIndex))
                else:
                    self.message2("Only the attribute value and the object being referenced can be modified!")
                    attr, layer_name = None, None

                # 获取属性中的键值对
                rh_obj_dict = attr.GetUserStrings()
                key_list, value_list = ([] for _ in range(2))
                for k in rh_obj_dict.AllKeys:
                    key_list.append(k)
                    value_list.append(rh_obj_dict[k])
                k, v = key_list, value_list

                # 获取属性中的材质
                material_index = attr.MaterialIndex
                temp_material = sc.doc.Materials.FindIndex(material_index)
                if temp_material:
                    mater = [temp_material]
                else:
                    init_material = Rhino.DocObjects.Material.DefaultMaterial
                    init_material.Index = -1
                    mater = [init_material]

                # 获取属性中的颜色
                color = [attr.ObjectColor]

                # 获取属性中的名字
                name = [attr.Name]

                # 匹配图层名的数据结构
                if type(layer_name) is not list:
                    layer_name = [layer_name]
                else:
                    layer_name = layer_name

                return k, v, name, layer_name, color, mater

            def RunScript(self, AOR):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    Keys, Values, Name, Layer_Name, Color, Material = (gd[object]() for _ in range(6))
                    if AOR:
                        if '_HAEAttributes__hae_param' in dir(AOR):
                            attr = AOR._HAEAttributes__hae_param
                            Layer_Name = AOR.Layer_name
                        elif 'NewGuid' not in dir(AOR):
                            structure_tree = self.Params.Input[0].VolatileData
                            structure_list = list(chain(*self.Branch_Route(structure_tree)[0]))
                            ref_rh_id = structure_list[self.RunCount - 1].ReferenceID
                            attr = sc.doc.Objects.Find(ref_rh_id).Attributes
                            layer_index = attr.LayerIndex
                            Layer_Name = [sc.doc.Layers.FindIndex(layer_index)]
                        else:
                            attr = sc.doc.CreateDefaultAttributes()
                            self.message2("Only the attribute value and the object being referenced can be decomposed!")

                        rh_obj_dict = attr.GetUserStrings()
                        key_list, value_list = ([] for _ in range(2))
                        for k in rh_obj_dict.AllKeys:
                            key_list.append(k)
                            value_list.append(rh_obj_dict[k])
                        Keys, Values = key_list, value_list

                        material_index = attr.MaterialIndex
                        temp_material = sc.doc.Materials.FindIndex(material_index)
                        if temp_material:
                            Material = [temp_material]
                        else:
                            init_material = Rhino.DocObjects.Material.DefaultMaterial
                            init_material.Index = -1
                            Material = [init_material]

                        Color = [attr.ObjectColor]

                        Name = [attr.Name]

                    else:
                        self.message2("Terminal A cannot be empty!")

                    if isinstance(Layer_Name, (list, tuple)):
                        Layer_Name = Layer_Name
                    else:
                        Layer_Name = [Layer_Name]

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Keys, Values, Name, Layer_Name, Color, Material
                finally:
                    self.Message = 'Deconstruct Attributes'


        # 修改已存在的HAE属性
        class ModifyAttribute(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ModifyAttribute", "C33", """Modify an existing HAE attribute""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def __str__(self):
                # 自定义类的字符串表示形式
                return "HAE Attributes"

            def get_ComponentGuid(self):
                return System.Guid("e47478fa-e06d-4189-a77e-ab7259bd9449")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes or Referenced", "A", "HAE attribute to be modified")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Keys", "K", "Modified key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Values", "V", "Modified value")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Name of object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "LayerName", "L", "Object layer")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Colour", "C", "Object color")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Material", "M", "Material of an object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes", "A", "Properties generated after modification")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATaSURBVEhLpVVNbxpXFO2iUn9B+pH+gDbdRcqiqaJW6rKLZNFdF1FUd5GodqRm00qRKrWJlACN3cqJMXY+GoMDGAyxjcE2YIwZYzDm08DADMMwMIwxNhgltdL0w6dvnonUrcmRnjTS3PfOu/fcc98bKkql+JnDw4ML7bZ0nmXT59Pp9Pm7ev0FjWbwDA14XeRymRmf3wev14tGcwfbjQaWvD4Yxu8fLgeZL7thvcPrXTL39fXh6tWr4HgeJUFAkeMw63Jh2jn7j3+F+aIb2hsEoWBeXvbB7VlARRJRqQio1yWkMylYp2xwzsy9DK5FPu+GHx9P7CHzRlLG7m4dwbUU9I9W8GAyBGZ9C+uRdUzZp2Gbdh4EQuvnuluOh81E1jxhS2Bw1I9fDcsIhNJY8CfodyzBIkJIiB7QDQ5luluOh2yONbfae4hu5iBJZeQLHPgSD0WpEE1KEMoiVoKruHX7Vq675XgwWkNmoz2JVIbFYyuDQb0fQySbxxYGuXyREJRRlWW43e7eMlDqgnktJkB3zwvn/Aa5uUQyEcl3jGZVFgUopHXzhSIl4PnM2c6zhk6SOC3HZbUFjtM+sVh0ujtDPx4eHr5FD/0/rM6wOZWV0G7JJIsCHk4ymLSHkc1zkOtVWqa6sg2eL3UJCtcWFhcxoteT/3XsdzpgC0VYbXY8nXN7ALxJD36FSDRtfmiJ496DFSq0KvCsJ0YzWmUSxHjbkAkBx3GUoMDlrty8eRMXL17ERixGS1gWRayGGLWl4fIsOejBr8CyrHmv1UKQyUCslInAJXIzGcnkJs5+/AnmXPM4ePECXPGoRIToilAWEA6HqW9UcxbJkiSBxLrwdNYFz6Jvkh6uQhV50pEiJSnCaAtTkdUWtc0m8MudIZz68AMEV0NotfYogX2GuWKZyYItClgKHLX3kMGPiakwYvEMXPPzxDsOWO2OcUqgisxES9De82F6ThW5Sm/mcMVQEhsY1Y/g9OnTsNvsSTX+2bNmXyRehmbYS8uaTLNUJ7NjHd6VNEolDhMmE25rtaAEM66ImRMU7LdlGmhxRvDUHSN1LaNWk9BqdzA6asBHp04133vnxA+/DY8ZRUmBLIt0MZEMvIEk9VCtJpJZVsZWNgfDmOFvSrAciM/b3WXMLObxyJqEn+GxECjioSUJobKD5388J40BXL9+He++fQJ9fZf/HXkcJdlGMWZcxTDJ4gHpPO1dL50Cqo5StUrGTPQvStCocl9xJUmnG17SRKMZTadZ07SbkiaRyGtSZEmCoJFrNc13AwOa90+eXPjs03N/rm+xMDljmAtmIe2QbHbq2ODIofE86SqBkFTUZjkiOC5M33z9/e7PP0GRK5D9XihkzCvf9kO5OwyRzYEjo+WIQOiNoHXQufzSPgXl0iUoAwOoEZJqMo76jRuoGE3g6gohkIgx+d4IAsFYP9/oQOFZMqMkrCY5eNey4Bo7qMhV1fEQJYl0U48lCgRi/WOTm3B44hgn4g7fD+C+KUSc7yPvSYbOscrrEGxX+f7m7h4emRl4fHE0d2rEhDIy2SIisRxEMjYqUrV3Aocj1O9ZLmC3WUOO5TBuDGHk9yBxdYqKq74flWpNJTjywXHB5/PXViI1GCaiGDdtILxRwlZegsmeABPlyXRtob2/TyaCjP8AQPhTkrA0zl0AAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def craete_new_mater(self, material):
                # 新建材质
                empty_material = Rhino.DocObjects.Material.DefaultMaterial
                if type(material) is Rhino.Display.DisplayMaterial:
                    empty_material.DiffuseColor = material.Diffuse
                    empty_material.SpecularColor = material.Specular
                    empty_material.EmissionColor = material.Emission
                    empty_material.Transparency = material.Transparency
                    empty_material.Shine = material.Shine
                return empty_material

            def attr_modify(self, obj_attr, key_list, value_list, name, colour, material):
                # 备份一份新属性值
                copy_obj_attr = obj_attr.Duplicate()

                # 修改kv键值对
                attr_dict = copy_obj_attr.GetUserStrings()
                origin_key_list, origin_value_list = ([] for _ in range(2))
                for k in attr_dict.AllKeys:
                    origin_key_list.append(k)
                    origin_value_list.append(attr_dict[k])
                new_key_list = origin_key_list + key_list
                new_value_list = origin_value_list + value_list
                for k_index, k_item in enumerate(new_key_list):
                    copy_obj_attr.SetUserString(k_item, new_value_list[k_index])

                # 若存在新颜色则修改
                if colour:
                    copy_obj_attr.ObjectColor = colour[0]

                # 若存在新材质则修改
                if material:
                    material = material[0]
                    if type(material) is Rhino.Display.DisplayMaterial:
                        new_material = self.craete_new_mater(material)
                        matIndex = new_material.Index
                    #            matIndex = sc.doc.Materials.Add(new_material)
                    elif type(material) is str:
                        matIndex = int(material)
                else:
                    matIndex = -1
                copy_obj_attr.MaterialIndex = matIndex

                # 若存在名字
                if name:
                    copy_obj_attr.Name = name[0]

                return copy_obj_attr

            def _get_attr(self, _hea_attr):
                # 判断属性是否为HAE属性或者是引用的物体
                if 'HAE' in str(_hea_attr):
                    true_attr = _hea_attr.Value
                else:
                    true_attr = _hea_attr
                # 获取HAE内置属性
                if '_HAEAttributes__hae_param' in dir(true_attr):
                    attr = true_attr._HAEAttributes__hae_param
                    temp_layer_name = true_attr.Layer_name
                elif 'NewGuid' not in dir(true_attr):
                    ref_rh_id = true_attr.ReferenceID
                    attr = sc.doc.Objects.Find(ref_rh_id).Attributes
                    temp_layer_name = str(sc.doc.Layers.FindIndex(attr.LayerIndex))
                else:
                    self.message2("Only the attribute value and the object being referenced can be modified!")
                    attr, temp_layer_name = None, None
                return attr, temp_layer_name

            def _do_main(self, tuple_data):
                # 按最长树的下标将树重新插入获得新数据
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)
                aor_list, k_list, v_list, name_list, layer_list, col_list, mater_list = new_list_data

                # 获取hae属性，以及所在图层
                hae_attrs, layer_name_list = zip(*map(self._get_attr, aor_list))
                res_hae_attr = []
                # 单个获取修改后的属性值
                for hae_attr in hae_attrs:
                    if hae_attr:
                        k_len, v_len = len(k_list), len(v_list)
                        if k_len != v_len:
                            new_attr = hae_attr
                            self.message2("The K value and the V value must be a one-to-one correspondence!")
                        else:
                            new_attr_obj = self.attr_modify(hae_attr, k_list, v_list, name_list, col_list, mater_list)
                            # 若更新图层则新增至新属性值中
                            LayerName = layer_list[0] if layer_list else layer_name_list[0]
                            new_attr = HAEAttributes(new_attr_obj, LayerName)
                    else:
                        new_attr = hae_attr
                    res_hae_attr.append(new_attr)
                ungroup_data = self.split_tree(res_hae_attr, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = value_list[max_index]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [value_list[_] for _ in range(len(value_list)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                def sub_match(tuple_data):
                    # 子树匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        new_tree = [other_tree] * len(target_tree)
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                    return new_tree

                # 打包数据结构
                other_zip_trunk = zip(*map(sub_match, matchzip))
                zip_list = zip(max_trunk, other_zip_trunk, ref_trunk_path)
                # 多进程函数运行
                iter_ungroup_data = ghp.run(self._do_main, zip_list)
                temp_data = self.format_tree(iter_ungroup_data)
                return temp_data

            def RunScript(self, AOR, Keys, Values, Name, LayerName, Colour, Material):
                try:
                    Attributes = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    # 树形匹配
                    gh_data_tree = self.Params.Input[0].VolatileData
                    j_bool_f1 = self.parameter_judgment(gh_data_tree)[0]
                    re_mes = Message.RE_MES([j_bool_f1], ['A end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Attributes = self.temp_by_match_tree(gh_data_tree, Keys, Values, Name, LayerName, Colour, Material)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Attributes
                finally:
                    self.Message = 'Modify Attribute'


        # 替换物体的HAE属性
        class ReplaceAttribute(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ReplaceAttribute", "C35", """Replace the HAE property of the object""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def get_ComponentGuid(self):
                return System.Guid("e0208e9c-b074-401f-8d54-1043beec88f9")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Object to be replaced")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Attributes", "A", "Attributes of the object to be replaced")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Replace", "R", "Replacement button")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Replace Attribute'
                # 初始化输出端数据内容
                if self.RunCount == 1:
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    # 确定不变全局参数
                    self.switch = p2[0][0].Value
                    if self.switch:
                        j_bool_f1, geo_trunk, geo_path = self.parameter_judgment(p0)

                        j_bool_f2, attr_trunk, attr_path = self.parameter_judgment(p1)
                        re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['G end', 'A end'])
                        if len(re_mes) > 0:
                            for mes_i in re_mes:
                                Message.message2(self, mes_i)
                        else:
                            sc.doc = Rhino.RhinoDoc.ActiveDoc

                            # 数据匹配
                            iter_group, max_i = self.match_tree(geo_trunk, attr_trunk)
                            # 添加原始树路径
                            geo_trunk, attr_trunk = iter_group
                            zip_list = zip(geo_trunk, attr_trunk, [geo_path, attr_path][max_i])
                            # map函数运行
                            map(self._do_main, zip_list)
                            ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                            sc.doc = ghdoc
                # p0 = self.marshal.GetInput(DA, 0)
                # p1 = self.marshal.GetInput(DA, 1)
                # p2 = self.marshal.GetInput(DA, 2)
                # result = self.RunScript(p0, p1, p2)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARDSURBVEhLvZRtTJtVFMe7zGTRxRk/+JIl6r7oB4zEiEMSoJX2afu0pVh0dshL1RmFFtlgDMrsRtlo6QqDrlBWWhg6yxiUYViGjIAhCJuYTVfWGRVGzKYJjTiZS/aigj2e+3ApBVqMifGf/PP0ued37zn33PuU979qcrJvw3zwq6y/5vyHgvPje2Zmxp6moajydE7GtHYF9E0dNyx2z4za64X1NLRcwbufPxG8N+wD8APAFc43b56/++1Ev4Yiq+RqvaBzt0392eydBUf7LNg8v0JFw/djxqNTj1JkQbjaujvXuoZg7hzcmj4Ls9P98PP1TyHwYz+M+0/DyJc9MRQNyeUa3NrYfBFqnJeh0u6DCpsP9h2+CJVHp6Do4HAPxRYU8LmfDXzTBj9cboer/g64eqUDvvOdgK/HjsP4pS74pLf5EEVDslR3O6vrR2GveQBKTUNQUjkExQcGoLC8D/LKeoI6w6mnKMrjXeitZvwjTjj/WSN8MeTkPDLYCIO9R2CgrxHcLVUeioZUurfpjN7YDe/rOyFf3wU6dN6ek/Bu0cfw9s6PIFvneImiPN7ZD41bTrXuC/a0m+B0ZxXn7nYztB0rB09rBdRYS/QUDSk332LRFrrgTa0D3tI1cc7Jc0DmO3XwatbBe9nZxuXn4LLtbjnZYgBnXSE01u4Ce3UBOGoLwVKRd8Ns3vkYxULKzTVuydCU31bnmCA9oxxUGfvhle0GUOdUQvr20sMUW5Ldbt/QYC04XmfWBm2WfKgxacF6QOs3Gd97kSKrlKkx8LdlGiZU6jJQbisF5WvFc+nq3U7v697IV5XIXlMcU2/dpao1FwiMRuN9dDiqvF7ves0OI1/9RpFmR751Mx3+T7WOlYrcLCvxi8WC5+nYcsnlcn5qaqqOZdlVVigUWoFA8DhFlyktLW2znGXPIQMymQykLPuHhGWzaHhJYrG4Q6VSAQHDjUlBqVRCYmKimKIhKSSSOCzgGhYHOJ+zVCoF8o7P/RRbkETCtISDi5ZIJNykpKQkAUU54cIZ6Duk6khzSHFSmawNd/ggNwED7mgJiPl8fjIHolJSUoQ49hMZX8mHG+O/i0SiBm4SDjijJ5BCcnIynwNRcXFxDyQkJNwvFAqHo+2AYRgy54X4+PhN3CQM1K/VIjyDlzkwTFhdf7QE5InxZyhKEohspG+R4DUSDPxDgucoyh2y49/uAFs0GDUBGq/20jeBAVfkBGLA20JuUSJFQ8LD7pOtURTuYCtFue2WkPu+EiYmCRj8TvAZg96EfkTBsnKMTZOFIvKMmOz6Sbo8j4cVPswIhZfIh0WAlZPCWvEL+hZ5X7k4qZx0gcSwPWV06SXFxsZuxL5WIRwgEDl08iQJyWLEi78X20DeyaKE5XovEo3iNyOjS0YW3vOHMJEK23YEPYq+jr6Ndzu4WC3DiObx/Tf0BPoM8h9g1RH+1nm8vwEDyuWHn+DinwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.switch = None

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

            def sub_match(self, tuple_data):
                # 子树匹配
                target_tree, other_tree = tuple_data
                t_len, o_len = len(target_tree), len(other_tree)
                if o_len == 0:
                    new_tree = [other_tree] * len(target_tree)
                else:
                    new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                return new_tree

            def match_tree(self, *args):
                # 参数化匹配数据
                len_list = map(lambda x: len(x), args)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = args[max_index]
                other_list = [args[_] for _ in range(len(args)) if _ != max_index]  # 剩下的树
                matchzip = zip([max_trunk] * len(other_list), other_list)

                # 插入最大列表，获得最新列表
                reslut_list = map(self.sub_match, matchzip)
                reslut_list.insert(max_index, max_trunk)
                return reslut_list, max_index

            def attr_replace(self, haezip_data):
                # 分解主数据包
                geo, attr = haezip_data
                # 获取传入attr中的数据
                # 若属性数据为引用数据
                if 'Ref' in str(attr):
                    ref_rh_id = attr.ReferenceID
                    attr_data = sc.doc.Objects.Find(ref_rh_id).Attributes
                    if not attr_data:
                        layer_index = -1
                    else:
                        layer_index = attr_data.LayerIndex
                    layer_name = str(sc.doc.Layers.FindIndex(layer_index))
                # 若属性数据为犀牛id
                elif type(attr) is gk.Types.GH_Guid:
                    attr_data = sc.doc.Objects.Find(System.Guid(attr.ToString())).Attributes
                    layer_index = attr_data.LayerIndex
                    layer_name = str(sc.doc.Layers.FindIndex(layer_index))
                elif 'HAE' in str(attr):
                    new_attr = attr.Value
                    attr_data = new_attr._HAEAttributes__hae_param
                    layer_name = new_attr.Layer_name
                else:
                    attr_data, layer_name = None, None

                # 若存在属性
                if attr_data:
                    # 获取源模型属性
                    ref_rh_id = System.Guid(geo.ToString()) if type(geo) is gk.Types.GH_Guid else geo.ReferenceID
                    origin_rh_attr = sc.doc.Objects.Find(ref_rh_id)
                    # 源模型属性和替换属性的K-V值
                    rh_attr_dict = origin_rh_attr.Attributes.GetUserStrings()
                    replace_attr_dict = attr_data.GetUserStrings()
                    # 替换K-V值或新增K-V值
                    rh_key_list = [_ for _ in rh_attr_dict.AllKeys]
                    rh_value_list = [rh_attr_dict[_] for _ in rh_attr_dict.AllKeys]
                    replace_key_list = [_ for _ in replace_attr_dict.AllKeys]
                    replace_value_list = [replace_attr_dict[_] for _ in replace_attr_dict.AllKeys]

                    new_key_list = rh_key_list + replace_key_list
                    new_value_list = rh_value_list + replace_value_list
                    # 新增图层
                    BakeGeometry().create_layer(layer_name)
                    # 新图层的index
                    layer_index = sc.doc.Layers.FindByFullPath(layer_name, True)
                    attr_data.LayerIndex = layer_index
                    # 源模型属性重新赋值
                    origin_rh_attr.Attributes = attr_data
                    for k_index, k_item in enumerate(new_key_list):
                        origin_rh_attr.Attributes.SetUserString(k_item, new_value_list[k_index])
                    # 重新提交至犀牛空间
                    origin_rh_attr.CommitChanges()

            def _do_main(self, tuple_data):
                # 分解集合数据
                geo_list, attr_list, origin_path = tuple_data
                # 获得最新列表
                map_list = self.match_tree(geo_list, attr_list)[0]
                sub_zip_list = zip(*map_list)
                map(self.attr_replace, sub_zip_list)

            # def RunScript(self, Geometry, Attributes, Replace):
            #     try:
            #         sc.doc = Rhino.RhinoDoc.ActiveDoc
            #         j_bool_f1, geo_trunk, geo_path = self.parameter_judgment(self.Params.Input[0].VolatileData)
            #         j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
            #         re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['G end', 'A end'])
            #         self.switch = Replace
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         # 匹配数据
            #         else:
            #             attr_trunk, attr_path = self.Branch_Route(Attributes)
            #             g_len, a_len = len(geo_trunk), len(attr_trunk)
            #             if g_len > a_len:
            #                 new_geo_trunk = geo_trunk
            #                 new_attr_trunk = attr_trunk + [attr_trunk[-1]] * (g_len - a_len)
            #             elif g_len < a_len:
            #                 new_geo_trunk = geo_trunk + [geo_trunk[-1]] * (a_len - g_len)
            #                 new_attr_trunk = attr_trunk
            #             else:
            #                 new_geo_trunk = geo_trunk
            #                 new_attr_trunk = attr_trunk
            #             # 生成打包数据
            #             zip_list = zip(new_geo_trunk, new_attr_trunk)
            #             ghp.run(self.temp, zip_list)
            #         sc.doc.Views.Redraw()
            #         ghdoc = GhPython.DocReplacement.GrasshopperDocument()
            #         sc.doc = ghdoc
            #     finally:
            #         self.Message = 'Replace Attribute'


        # 根据颜色筛选物体
        class ReferenceByColor(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ReferenceByColor", "C24", """Filter objects by color""", "Scavenger", "K-Object")
                return instance

            def __str__(self):
                # 自定义类的字符串表示形式
                return "Ref Text"

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def get_ComponentGuid(self):
                return System.Guid("fecec114-692e-4a81-b2ae-757497ac6a41")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Colour()
                self.SetUpParam(p, "Color", "C", "Colors that participate in screening")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Update", "U", "Update button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Filtered object")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAT7SURBVEhL3VRrTBRXFF4jQsAVFC0UISKUh+wuuzOzszuzs+wuiCyLj10DWiNSEzShYhSlIhIVtRipWqutprGA9iEtTWwU0GqtivgK9Ud9NKWmpn+aNtbG2og2pSlVvp47O6zSJuqP/uqXnJx7zvnud87cmTu6/xdkWU4URdGkKMoYLfXfwOfzRQiCcMBqtYIZrfvJKrTyMFBe4Hn+itlsjtNSTwfHmd+h6eF251R4PApns9m22CWpRSsPAw1QwIaw2+0pWurJcDgccTQUyO/TUiEwEap9QoJfkt/McuRd9ATIyckZR8eZKohiB6tTbh2rk46JOMcpPkp2S91A08Lj8cxkhCEYDAY9EX4gkW7irOKt1j6O47bR05HjBsgbyd+kWgdxVpMfsFgs6/LynBZ2GlT7ghpX60jETZMiNzc3X9NWQflZ7Cj82gun+CXadJdy0y08f5tEN1Lcr5IJdru4muJbLpdjKjUD8ZPVAk3yPBOirg1qQgOR5xDpoRayBj7K3aNhZjMhURR2kP9ZK7PjXEjxHadTKiLuYHZ2dpJWUsUO2ugpREks40TRRhM00IRdRHwg2IQq9awF4QzF3ZIkSMQfIMEZ2qTlrE4NL1O+nT4SkQ1M+eATMBA5muOEQxzP/8ULwgPacFtRpBIiziWRO+T7yK5LkmUy1XgS+oPemZ5qS7VaHwleMZlM8XSHRFr/TrUETX4YRo7T6WK0dQiUGKstVfj9/tBFrGhqGqVb9Chm8HisE8iNCEY6XUTk6NhmXi5pN3JFrVmWwg+MFl+bgfMeZGbkfR9lmQtaMk35LVPM+e+ZbYHWiMiYRto3JGD0R0fXVU2c2LYoPu79hFFR7IJGBUtBjNDHPFc8bdYrqNt6CdWbushOP2ZdWLnxFFZsOIXaxh4UBGowOnrCPLaxNDpqV6fRiHsOB+By4bpgwtbszag3NNzUj9QHVPXH4MmbvvxOWWUz5i3e/S8rq2xB/szqu8SbxsijUsU9u0wCIIu4ryj4U5HwYZYVB+Sj+KqgF1tMjdCH6T2MG0Ls+KQ3Zi9oRKB0C/zzN4cssCAYj4mJV2+zLizMbnjtIjJ3X0O9kceAJQv9Dg7bM4txzH0RJ1wncXnaVSxKWfyNyh9CusG1bUX956hafwLL1x0PWVX9CSxbewzJGY46xotVit92tj+E4xgwae93qJS9uJKeiJ3Zr6I7t0dtcC73AvaJ70IVHkLqFOX1pXWdqFzTgSW1h0NWWdeBl1cfQnK6fS3jJc1d351D4vLH95FzHJjS2o+MFCvajPtVYdbglLsLR5yfPnuDJbXtSMmU1B9aYkndSdbA2TEIW/NvSKtZj0mHecwPlOE8fwEn3adx2n0GHcqRpzeoXNOOlfQ1sXVCsnET443jvY3OTsCy/QZSagKwnjfD9VMR0rp4VIur0CNfwsW8Huzm9zy5gfo+6PxnvLhh8AWDaz9Rhq5/WmJJ9QNDUyHkXhnKtz7IVwsgf+9FxgEOOw1vonfqdZQkzenS+EEMNagiYfbtFy/cDrpo7VSyBhmPEJagW8Z/Zofntp8aFMLxtReOXi+kX71wv1WI8rjyX4iWFmRryDB6dqxqOIvSir3gpeKzlBr2C/8nIpKjytO3mX4Uz+WqDeRrBeA6nYhfkcz2ZgVZjyFpMrfL7i69ER4eOUdLPQuiw5MiZ48vjK8d655QRbEjmGbQ6f4G0fdPdOFCLdIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Get_ALL_Objects(self):
                """获取到Rhino空间中所有的物件"""
                settings = Rhino.DocObjects.ObjectEnumeratorSettings()
                settings.IncludeLights = False
                settings.IncludeGrips = False
                settings.NormalObjects = True
                settings.LockedObjects = True
                settings.HiddenObjects = True
                settings.ReferenceObjects = True
                all_objects = [obj for obj in sc.doc.Objects.GetObjectList(settings)]

                return all_objects

            def Find_Objectsby_Color(self, Colors):  # 根据物件颜色筛选物件
                # 根据物件颜色筛选物件
                all_objects = self.Get_ALL_Objects()
                BycolorsGuid = []
                for c in Colors:
                    """遍历Rhino空间中所有物体"""
                    for obj in all_objects:
                        """遍历颜色组"""
                        objAttr = obj.Attributes.ObjectColor  # 获取物件的ARGB值

                        # "----------------------------"
                        layer_index = obj.Attributes.LayerIndex  # 获取图层索引
                        layerColor = sc.doc.Layers[layer_index].Color  # 获取图层的颜色
                        objArgb = [(objAttr.A, objAttr.R, objAttr.G, objAttr.B), (layerColor.A, layerColor.R, layerColor.G, layerColor.B)]
                        InputARGB = (c.A, c.R, c.G, c.B)
                        #                if objArgb == InputARGB:
                        # "----------------------------"
                        if InputARGB in objArgb:
                            BycolorsGuid.append(str(obj.Id))  # 返回物件的ID
                    return BycolorsGuid

            def Graft_List(self, List, Path):
                Tree = gd[object]()
                if len(List) == 1:
                    Tree.Add(List[0], Path)
                else:
                    for index, n in enumerate(List):
                        New_Path = Path.AppendElement(index)
                        Tree.Add(n, New_Path)
                return Tree

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
                    elif ('Text' in str_type):
                        rh_obj = rs.coercerhinoobject(rh_guid).Geometry
                    #                rh_obj = gk.Types.GH_Guid(rs.coercerhinoobject(rh_guid).Id)
                    elif ('Dim' in str_type):
                        dim_object = rs.coercerhinoobject(rh_guid)
                        rh_obj = dim_object.Geometry
                    else:
                        rh_obj = None
                    ref_brep_list.append(rh_obj)
                return ref_brep_list

            def RunScript(self, Color, Update):
                try:
                    Color_Tree = gd[object]()
                    Object_Tree = gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    color, color_path = TreeFun.Branch_Route(Color)

                    re_mes = Message.RE_MES([Color], ['C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        for index, c in enumerate(color):
                            Color_Tree.MergeTree(self.Graft_List(c, color_path[index]))
                        Color_List, Color_Path = TreeFun.Branch_Route(Color_Tree)
                        Objects_IDList = [_ for _ in ghp.run(self.Find_Objectsby_Color, Color_List)]
                        for index, o in enumerate(Objects_IDList):
                            Object_Tree.AddRange(self.decorate_obj(o), Color_Path[index])

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Object_Tree

                finally:
                    self.Message = 'Reference by Color'


        # 删除物件KV值
        class RemoveAttributes(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RemoveAttributes", "C34", """Delete the object KV value""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def get_ComponentGuid(self):
                return System.Guid("b5a59b58-4aa5-4dcb-b095-2cea6a144fd9")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Objects with KV values need to be deleted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Activate", "A", "Delete button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Message", "M", "Deletes the Attributes information for an object")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAYHSURBVEhLtVRrTFtlGEZi1B/6QxMTE2OWDcw2Njg9Byj+0JD4YxqzzB/O/ViWJSZmUbyQLLuKS43oxi7Z3AZemDAY7oIlQBl03AqUUuidthTac3q/0naDaRZ1S5yP73d6Mv8YnT98ki9Nc/I97/s9z/O+Rf87gKJiSZo/l7+Z6EmnQ9pIZFG7uOjWisGgdspo1J48dbrnXPPX7S5Jela58t8AaIpFScwaDJNobb2AxSU/bq6sIJvPI5VOY1CvR+v3bRgeM8x7vfGnlWsPDwDF44ZRcc+ePdixYweampoQi8cRECVIwRB8i0u4fPUqevsHMGaYsuRyuSeVqw8HVsDusIkNDQ3YtWsXOjsvIRorFGAnFA7D4XSis6sLuut6VmSK7jyhXP93QFNUnExGxGBIwsTkFEQpSJ0HEYuFkUhEkIhHIFGRUYsVnX390E0aMTZpGqEijyoU/wzmwWWtSTTbgsjn04gTYTAUxI86C5rbJtF7wwG/w4X5pmMw1Nej7+N6DOlHMGGa1f1dEd8bbzznVasPOysrP5sWhDq5gE5vEfc3jqC7bw6TJjc+bdKj8fQIOq+Z8UWLEUfqWzHx/AtwlqyDa+1adDMpdQPouNTVqvA+gP2lGnNSrQY7Ro67LxdgErkXQjLpJ0eH5O7ZS9LpmPxrcIYwWH8Q1pK1sHMcLJs24ZvDn6Dx7FmfwivDUvvKvmB1NewqFfxVVRhQqXbKJi/5A9LKrSzpzuQJIZOJUZIish9x8mE5n0IwHsX01q2wvvginFTAtGULjp86aVW4i2zbtq13VVfdcxJ5iMjHKip+lD+wAi1tBrHtipVMjWJ5OQ7TnBdffjWChmNDaDo3iuFxJ+L5HDzj45jeVAZbeTkW6SUDb75pl0kI1poas1+ohE8QMKtSZS+UlT0jf2ASzXt8YlOzUZaopX0KezUD6O63wOZchFZnxYHPB2XD4z+twkpzMrtmDVw8D09FxW96tbrM/mrtuyGSxkHdL1ZWor+8fJtMzsBimiYP8jezuNY7h+86jZj30DTnk8guJ5DPJeSBM1sWEIpGISWTMG1/i/wohZe6NfN8Yk7gf3YRebggTbtCXQB7QY9uTnS4g1i5lZQJk8kYBkedaL88g2GDS/aGScfmI5JZhtc0DZOKg23zZnjoJYycSTPDcbHj69c/pVAXwDzQ9s/KMR0ccciyMKmOHNfj2w4jNCdvyMkaooLRKIWAXhNZvQ37+fOwlJTIiWHGegThfq9KVavQ/gUNSZQhiSxOCUco/wcaB9HZbZZTlM3G5ZgO0LB10EyEI1SApjp88xY8tFoslCimOyuwIAh/GHj+HYX2L7ACAX9AvL2aRyQShj8QRC6bQCJJelO3TK5cLin/sv8hIl/qvgZraak8E0QMNzOcjpPnfx3m+VKFuoBCTCfE7y9bkUrFZA/kmJ5hMdXj2Lkx8mGeFmAEYVrfQd8C7C+/DNuGDRAplqMcd22c42b9QhWkyirM8LxZoS4AGk2xh2J6glYC0765rRBTFk+Hy4+e6zYcJNlaLhqRXCVp6t6DldaFl2SxlHM5TVnZYz8IQrmTXuLhBUpSNQwq4bBCTxIV0TZNFGLa3WdBa9c03N4ALb4kJSchy8Om2yqlsHSxHdZ16+AgaXycCvZTp2YVmqLrPHcyQrNAZsMtCL8Pq9Sc/EFDL7gxahf9IpOHsk/GLmcSmJlbQN+QHRa7D+lbOcS887Cpq2Er2wT7uhL49u5FKJ+3ySSEj15//XEjz0sBkkmkebAIgkdTW/uo7EHHFZN46Ogoab8AvxjE2dYJWZYTLeM49KUeX12cgWv3bthKS+CgPTRbU4MEGR5Npx4UYNCqhVc8NMlukipSrYZJEJqKQBIloqG83ZPBsWYzjp6fQVePG7n8Cu7evYPcL/cwfaYDPpImRJcD5RWI9fbiPnUWlkRJ4X4AvaA6v0wNsHUdpcMKPCL5fDvvrKY/dDg8H4yN2OpWM9G6VFiqCwcCdZlcpi5wqfUDXUlJ4/jGjacNr722P5RKvb+cSHwY9vu2K7wP8DaZPqxS7ZsTVKenOK7hT5RnxpqmyDfCAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Delete_Attr(self, Geometry):
                rhino_object = Rhino.RhinoDoc.ActiveDoc.Objects.Find(Geometry)
                rhino_object.Attributes.DeleteAllUserStrings()
                for item in rhino_object.Geometry.GetUserStrings():
                    rhino_object.Geometry.SetUserString(item, "")

                rhino_object.CommitChanges()
                return rhino_object.Attributes

            def RunScript(self, Geometry, Activate):
                try:
                    Geo_Message = gd[object]()
                    re_mes = Message.RE_MES([Geometry], ['G end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Geometry = list(chain(*TreeFun.Branch_Route(self.Params.Input[0].VolatileData)[0]))
                        Geometry_ID = Geometry[self.RunCount - 1].ReferenceID

                        if Activate:
                            Geo_Message = self.Delete_Attr(Geometry_ID)

                    sc.doc.Views.Redraw()
                    return Geo_Message
                finally:
                    self.Message = 'Remove User Attributes'


        # 根据KV值筛选物体
        class FindByUserAtributes(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FindByUserAtributes", "C42", """Filter objects by KV value""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def get_ComponentGuid(self):
                return System.Guid("eb251c48-ab0c-4249-8bc6-2f7092741d9b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Key", "K", "The Key value of the object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Val", "V", "The Value of the object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Update", "U", "Update button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Filtered object")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASESURBVEhLrZR7TFtVHMdxcwkmJi6L0+niIoEWxqPgGK+yUUofPLKNYGzYJhbGbXtvX5T29vYFeCmPjalsJlMXkiVKnI+WlktpYVA6ShGHcTOKf2zRPxYTE/80mpjFaNzPcy+XDsIKW7JP8s3t/Z3f+X7POc25aY/L8OWf9vM/nzzUQHTYfW7xnr0venVk5NYuvvxoKGXVzQqZ7HJl5dFWvpSE/jieTvVHx1xnE2DpngTX2QWwe6MJ9+DiXr5la+pqJC3yGgmIKyqgvKISDpdWGPmhNM9A4iVkfsM5uABmD7Mq9zg4Bq4D6Z39ubPvWh7fmpojFaWh8tISyM/Pg8LCIsgXFS6ydfdgTER5o3cpZGZCpskAJPYdHRUb8rvNO6PgjFJR/FqhtVBUAEKhEA7m5MC+vc/oh0buiO19s38gg03m60Ns9DTYvLP/2frm2nm7zdA0vSNHKOwRCLJimZkZfc7+GVf3OzfAM7QEVH+MXSV3LJvMe2fQ+HVwnUsAfeEW+/6hgY4/y9umxuwJvoeTV4e1naNDuG10iLB/HuzsiWwIsL49BYT9sxg7zvWQn543uQIfEJQvm7fZyIrFpL3TYVlaMRga+VISsmeszM7uwjORDGD/ZKPDf5JvSc2S2Zy5TBBXvtJqby7rdICeia9x/GLcYNjHt6R1do0pSXQc6wPYozO6/Gda6Xg6To2fMnXPkDgVtGqpgBQAnmLnGRyhvLRZgnjhC7U6cwZryYpj2J/DGLYn3NYmYFpbd3PuiFQBBqe/Teece85gZ4pUKv9Oi4XZTTiYWj3F6AzOUBt6NvMWaWk3jdqChEbzV9RofJkvJUm5A6dfw47rHYwYGXfqXROEzh6sM7uncwmKOYo7xrWcAcuyHhOxAWEc3/StSRWgd/rVOtvk8zpn4DhNx59mewkymG90T5/EneONmNW3hzNg4QPuhXHrIwes7UDrYAoIJ6NBO8EIR7AchaXrbcwruJNp4wxY2IB4O/ZYAQbK9xbuCe/H7UF1hzv0IobE/geW7pl2tqYhfRm8xSq/HGjZWODZbgfbogPdLsV9jbfyvjks/kdDS4DmznMNOx2QPyzA5PZhfMvWKH97s0sJeqgADMSgg+Lvm538EAdJ+2rI3o0Xjf1EmDxfqvmWrREnjsfK7qqg4IcTUPRjExSMKyNsXaVS7TwinTzTdCp829YbgY6uiaRIbwTeUIduiyWhFtTKXayUHLoi1YoYOWQHJCAYLf47d7jotFy68Lq0NrIirZ2HE6pp6PCMoZsbQFp9dnT5oel0GCTyGFQrQt9VK9ddqoeRdenAseyLhy+VYNYxuWxuUVE/DzX1cyBRhABNBnlDAOT1Yw/U4AeJMghVMgaktddAVhdFYaFvqhQTTbzlA4CGHY1lv1bXSb+NKOSL/yoa5tGkKaiujaw+lRE0eWqdIlAlR6tXhNnVs8bcQmpQCCuJfHJJppw6RiNfLiA7zzFUVPI+iIrfhdxCL1Lvtjq4JhG9SQWHziOvYRDm22kuIENo+CQzh4RXBfonpsyDdsgQGD/6Hww4DyQgVIf8AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def Get_ALL_Objects(self):
                """获取到Rhino空间中所有的物件"""
                settings = Rhino.DocObjects.ObjectEnumeratorSettings()
                settings.IncludeLights = False
                settings.IncludeGrips = False
                settings.NormalObjects = True
                settings.LockedObjects = True
                settings.HiddenObjects = True
                settings.ReferenceObjects = True
                all_objects = sc.doc.Objects.GetObjectList(settings)

                object_guids = [obj.Id for obj in all_objects]

                return object_guids

            def HaveKey(self, Object, key, contrast_value):  # 根据Key值，获取Value
                """根据Key值，获取Value"""
                Obj = []
                # 遍历得到的value
                for v in contrast_value:
                    for obj in range(len(Object)):
                        obj_attr = sc.doc.Objects.FindId(Object[obj]).Attributes
                        value = obj_attr.GetUserString(key)  # 根据输入的key值得到Value
                        if value is not None and fnmatch.fnmatch(value, str(v)):
                            Obj.append(obj)
                return Obj

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

            def Graft_Tree(self, tuple):
                """得到升树后的树形结构分支Path"""
                value, orgin_path = tuple
                ungroup_data = map(lambda x: self.split_tree([x[1]], orgin_path + [x[0]]), enumerate(value))
                Data_Tree = self.format_tree(ungroup_data)
                v, v_path = self.Branch_Route(Data_Tree)
                return v_path

            def RunScript(self, key, val, T):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Obj = gd[object]()

                    if key:
                        re_mes = Message.RE_MES([key, val], ['K end', 'V end'])
                        if len(re_mes) > 0:
                            for mes_i in re_mes:
                                Message.message2(self, mes_i)
                        else:
                            attr = self.Get_ALL_Objects()
                            attr_str = [str(_) for _ in attr]
                            All_Objects = self.decorate_obj(attr_str)
                            value, value_path = self.Branch_Route(val)  # 得到输入的value和path
                            Data_Path = map(self.Graft_Tree, zip(value, value_path))
                            value_list = [[item] for sublist in value for item in sublist]  # 将嵌套的列表每个数据展开
                            new_Path = [item for sublist in Data_Path for item in sublist]  # 得到新的路径
                            for i in range(len(value_list)):
                                O = self.HaveKey(attr, key, value_list[i])
                                for _ in O:
                                    Obj.Add(All_Objects[_], GH_Path(tuple(new_Path[i])))
                    else:
                        Obj = None
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Obj
                finally:
                    self.Message = 'Reference by User Atributes'


        # 物体获取它的KV值
        class GETUSERATTR(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GETUSERATTR", "C2", """The object gets its KV value""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def get_ComponentGuid(self):
                return System.Guid("af5ef186-5ae8-4eab-a2e8-42b171fa942a")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Geometry")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Key", "K", "Key of object")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Values", "V", "Values corresponding to object Key")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANDSURBVEhL7VVZaBNBGF5EVHyxKF4P+tCiLagPCoIIUlSwbTaJ1ip4QZU2m03aZGc3e+8m28OmFkU8QLxARLSHTZrG4oG1HlBBBEVfBGnrswpFiqC0lfGfdStL6QXx0Q8+8v//fDPfP7PDhPqPOcGyns5n5RSq0XuuBuX0tVwYUjPXIsb9c2wstdFZnqJYOR2Sky9xWMvikJLJmbGGZxgaHjhodSywDYJS1/mo+QAzWmcRx3XlMUrHEkZ5vITEE3mlE89GogtKqVs10CyJ/xjI6TOwLVyjppfZhRwREuGolC5MGrMLEwZVWvdKkuse1G3QSCaxXBLe0FRuvNI8/E6SE4ie8KpkuSGafq7QKVFqmbC+eb8pWdsOLA3KmUtTGrDWoxUkN7wCNrzoZqQ0srDBr3yu80uDWmlkuS0GGB5h+4XDzRga6XVKlObhshePNOPGLfsKGP3e2ZkNPGhYo9GNOM13NexTR1BJYLUtdGAVW/Nh8U8JX2yM28vlWcWVi0xv7AepkXFY78qMBiAcqvfLozBplN9ds8kWTYLu4VrOHTqJ495YmU5zJSSGxpJkjJXS12c2oPmBpnIdJ3ziT7E0UmCLJiHujW49VRHHOo3ugEH7qQoTm35hMxmb1cCg+S/AHujufZ1fHiJHYAtdsChrnuZBHy2fNA6N/IIdfXCG5mKARuCYrqo0ym85kIAPLrTawkmAnTa3VCQwIcw56ZTntINxYJbEaimHyO2ADo+T3A2zjN+U8ItjsINR04c2OOXpDQJ6yr4tcEX3uCfAMXjduRsSHV1H6KQ2pjX4W8gRYHCZvElugwtc/BFmpbs7WClTyAidRYS1WrYoILZOeYsIYIG1RDOhJ2Sl9sKglO4kD2cld8N5i6TUUbHxORbq+zBf1+viE/u3WmiL2EIXqvi2E9H4wynm9GI52U9e09fkb8CRg4mYKo+Y9xVWSv0lAwyp3W9jYF6NWnc4Uqoa3dklNDzFYaV70K0nDCsZtVbviQbQn+85KyrFjlXQ6XDEfPCVYbKLjwutayD/Dvx2At3Od2S5gXQsNr4gHfeF1ew7cnTuHf0TBIQ22Tj9BstN/biKbz/mlP8tWCXdwogdyEnnAIr6DXgFXcbMTo/FAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def KeyisNone(self, Object):  # 当Key值为空时，提取所有的Key值和Value
                Key = []

                for obj in Object:  # 根据物体的Guid属性获取Key值
                    if obj is not None:
                        obj_attr = sc.doc.Objects.Find(obj).Attributes
                        Key.append(obj_attr.GetUserStrings())
                    else:
                        return [], []

                Keys, Value = gd[object](), gd[object]()
                Keys, Value = [], []

                for _key in range(len(Key)):
                    for v in range(len(Key[_key])):
                        Keys.append(Key[_key].GetKey(v))  # 获取Key
                        Value.append(Key[_key].Get(v))  # 获取Value
                return Keys, Value

            def Graft_List(self, List, Path):
                Tree = gd[object]()
                Path = GH_Path(tuple(Path))
                if len(List) == 0:
                    Tree.AddRange(List, Path)
                else:
                    if len(List) == 1:
                        Tree.Add(List[0], Path)
                    else:
                        for index, n in enumerate(List):
                            New_Path = Path.AppendElement(index)
                            Tree.Add(n, New_Path)
                return Tree

            def RunScript(self, Geometry):
                try:
                    Data_Tree, Key_Tree, val_Tree = gd[object](), gd[object](), gd[object]()
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([Geometry], ['G end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Tree, Tree_Path = self.Branch_Route(self.Params.Input[0].VolatileData)

                        # 取出所有物件的ID，并去除空值
                        Geometry = [map(lambda x: x.ReferenceID if x is not None else x, _) for _ in Tree]

                        for index, G in enumerate(Geometry):
                            Data_Tree.MergeTree(self.Graft_List(G, Tree_Path[index]))

                        Geometry_List, Geometry_Path = self.Branch_Route(Data_Tree)

                        for index, Geo in enumerate(Geometry_List):
                            K, V = self.KeyisNone(Geo)
                            Path = GH_Path(tuple(Geometry_Path[index]))
                            Key_Tree.AddRange(K, Path)
                            val_Tree.AddRange(V, Path)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Key_Tree, val_Tree
                finally:
                    self.Message = 'Get User Attributes'


        # 物体获取它的KV值
        class GETUSERV(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GETUSERV", "C41", """The object gets its KV value""", "Scavenger", "K-Object")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def get_ComponentGuid(self):
                return System.Guid("dd6e80bf-d1e9-4cd1-b76c-8173cb1cd13f")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Geometry")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Key", "K", "Key of object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Values", "V", "Values corresponding to object Key")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAU6SURBVEhLfZV/TFNXFMebbG7LNuOMus0/Jm4JKFjavvfavtefSMcPFSMFKRRaEGpXym+sMsTM6RTERMH5AyM4bEVBO0HETdHA/NG5LYvoNsemDvyxLC4sgnMCKs707N7HpViBfZKT5p5zcr/3nPvOrWCEgtXHFTaHO8mSX2ccMWthQ4LN0ai3Fh5IfNb/fDyDjzuRb9g+WFFvzFhRH0a2Fgjy17RUmGy7h+JMZbeetdiUT3r1yesH41M3d8WlbrrpZ+ZNN9DvbX3K+oE4U+kdsuYt3lzebbTueJSW46oTdHTApLTsvV69uWwD0fMRKgzawjDUP8HBgfnE5YdQOLeRpiUDwYEBi4jLR6qt0p6e6wJBZye8lJpV/TDJutNBYj5okYhlGCmIxZK/wsICXiFuHpamGakUxSSSnjlz5kwmbh+5q91JZnsNEciuGUxc/umHJOaHWCxuZVkOKIqyExePRCJpYjkORBQ15mCYTEe9yWyvHqmgZtA4kQAjVkllMlxFt8FgeAH7ZDJZEM0wXiTSp1Qqx5weY191MMWcNVJB1t4JBTCoCo+cZQFtmIDXEoqq5tDp0XodnzAOmY6GZD+BiVqEQQJRcrkcV+FRKBRvonY9QtaPKplGUsZgX1lvHL0D1KL/E8AgkUs0TeNTdwyLibeS0LhggdRn7uBxgqWygMTGRSgMjJEyNEilNIhFoY+CZr4+nYTGJaugTo86A4J1Z+FFNGSPU3Ocexzrjk/PWX10WkGB8w2brXoSTiwqOjYZ+/NK3DNYTtusVM/vVKojNm6uvjEF+4djJ2dgKykbtcKPvljLC2AWJZRkJlm29xkytt01pFfeWZbrvLc4aWPU/uP3ZlnyXf2JyJ+Ysb0n2VqFJnTnbePyXd1LjeU3E5aWXjWkbe0xpFf0jljCsq19ienb+lJsVfdjDGvX8AKYoCBmuiLKNtfuOLg4LeczsObWpmUXN3frU8q+Ui/IDMGmjcgKZqYys0Qvy981NbRZrN/8tDs6fQ2t1mWEyHkzhcjVphC8DggJe5ts7U9OcVNzeq4TLHnOh+jULcTtY6XXG1Ds9bqLvN4n1gcAEe1PCkloYtAn9z7L0llJy9ba8KeFNu5YnLjBOm9eYDzLylayLPsWzlsx4F2w6qn3QeETgCVf/wmaY39AxKn7/XHnB2byG02ESCS6qFQpQaud7wiLLZ7N+4RBZQoFP0xd+NvHPtO317bEeX4DtuYcyJ0XQX3kKkR5hiDy5P19OD4hSOAsnlStVhWH1xQlcaNN8ftzjGGYV/kkRKg6ZSr98b4eZsdJ4Jzfgerwz6BtuQWR7f2wpG2IImljwQIyNDwajSYHDVAjagkepCoS9iO8fL+F2/ElyHa3geLgJVTFrxBxph8iT/SdIyljwQL8lFIUYCE0TKUkNC5cmeuybNcpYGsvgPLQFdAc7YJoz7+wsH1QT1L88Qmg1xG1BDgF5zEajfzFjkfkFpeWrWgCadVpUNRdBNXnv4DudC9EtP7dZUN/YCRtFCRwDr8vqEXW0NDQCtwijmOvxcbGvkNSxqDctP+IvOoUyGvOg7LhR9A0XofoC08h+vRAEUkZZURApVJZyNqJRViOvRETH/Men/QcsdsOzZZvbngsRa1SuL4HlbsTwlt7QHfi7pChDaaQtGHQqX9AfxxYwDc06JJr8ZuPhAZ1Op2IuP3QlLtK2V2tINtzBjRN10HX3gvhLb9vZ6qfa5NQKMxDvXehzfw2QpWUIP9hVF04cflhrqt7jSs/0MPVekBVf/ma2n3FTEIEgeA/3UOEk1idJugAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def HaveKey(self, Object, Key):  # 根据Key值提取Value
                Value = []
                for _key in Key:
                    for obj in Object:
                        if obj:
                            obj_attr = sc.doc.Objects.Find(obj).Attributes
                            Value.append(obj_attr.GetUserString(_key))
                        else:
                            Value.append(None)

                return Value

            def Graft_List(self, List, Path):
                Tree = gd[object]()
                Path = GH_Path(tuple(Path))
                if len(List) == 0:
                    Tree.AddRange(List, Path)
                else:
                    if len(List) == 1:
                        Tree.Add(List[0], Path)
                    else:
                        for index, n in enumerate(List):
                            New_Path = Path.AppendElement(index)
                            Tree.Add(n, New_Path)
                return Tree

            def RunScript(self, Geometry, Key):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Data_Tree, val_Tree = gd[object](), gd[object]()
                    re_mes = Message.RE_MES([Geometry, Key], ['G end', 'K end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)

                    else:
                        Tree, Tree_Path = self.Branch_Route(self.Params.Input[0].VolatileData)
                        Key, Key_Path = self.Branch_Route(Key)

                        # 获取所有物体的ID值
                        Geometry = [map(lambda x: x.ReferenceID if x is not None else x, _) for _ in Tree]
                        if len(Geometry) == 1 or len(Key) == 1:  # 判断输入端的数据结构，输出不同的数据结构
                            if len(Key[0]) == 1:
                                for index, Geo in enumerate(Geometry):
                                    v = map(lambda _key: self.HaveKey(Geo, _key), Key)[0]
                                    val_Tree.AddRange(v, GH_Path(tuple(Tree_Path[index])))
                            else:
                                for index, G in enumerate(Geometry):
                                    Data_Tree.MergeTree(self.Graft_List(G, Tree_Path[index]))
                                Geometry_List, Geometrylist_Path = self.Branch_Route(Data_Tree)
                                for index, Geo in enumerate(Geometry_List):
                                    v = map(lambda _key: self.HaveKey(Geo, _key), Key)[0]
                                    if (len(Key[0]) == 1) and 0:
                                        val_Tree.AddRange(v, GH_Path(0))
                                    else:
                                        val_Tree.AddRange(v, GH_Path(tuple(Geometrylist_Path[index])))

                        elif len(Key) >= len(Geometry):  # G端输入为树形，K端也为树形，结果与G端树形结构一致
                            remain = len(Key) - len(Geometry)  # Key超出Geometry的部分
                            for index, _Geo in enumerate(Geometry):
                                _value = self.HaveKey(_Geo, Key[index])
                                val_Tree.AddRange(_value, GH_Path(tuple(Tree_Path[index])))

                            if remain > 0:  # 当Key的长度比Geometry多时
                                index = [_ for _ in range(len(Geometry), len(Key))]
                                for _r, _index in enumerate(index):
                                    N_Path_list = [_ for _ in Tree_Path[-1].Indices]
                                    N_Path_list[-1] = _r + 1
                                    N_Path = GH_Path(tuple(N_Path_list))
                                    _value = self.HaveKey(Geometry[-1], Key[_index])
                                    val_Tree.AddRange(_value, N_Path)

                        elif len(Key) < len(Geometry):  # G端大于K端时
                            remain = len(Geometry) - len(Key)  # Geometry超出Key的部分
                            for index, _Key in enumerate(Key):
                                _value = self.HaveKey(Geometry[index], _Key)
                                val_Tree.AddRange(_value, GH_Path(tuple(Tree_Path[index])))

                            if remain > 0:  # 当Key的长度比Geometry多时
                                index = [_ for _ in range(len(Key), len(Geometry))]
                                for _r, _index in enumerate(index):
                                    N_Path_list = [_ for _ in Tree_Path[-1].Indices]
                                    N_Path_list[-1] = _r + 1
                                    N_Path = GH_Path(tuple(N_Path_list))
                                    _value = self.HaveKey(Geometry[_index], Key[-1])
                                    val_Tree.AddRange(_value, N_Path)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return val_Tree
                finally:
                    self.Message = 'Get User Value'


        class Delete_Object(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Delete Object", "C43", """Delete Rhino Object""",
                                                                   "Scavenger", "K-Object")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d98b9537-d5cb-437d-9ebb-715527f90bb7")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Guid", "ID", "Rhino object or object ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Boolean", "D", "If True deletes the input object")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                self.Message = 'Delete object'
                if self.RunCount == 1:
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.marshal.GetInput(DA, 1)

                    guids = self.Branch_Route(p0)[0]

                    def Delete_obj_by_id(guids):
                        for guid in filter(None, guids):
                            new_guid = System.Guid(str(guid))
                            sc.doc.Objects.Delete(new_guid, True)

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([guids], ['G end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if p1:
                            map(Delete_obj_by_id, guids)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATwSURBVEhLzZV7TFNXHMe7zf2zbHFRt7lNx6uFWjao7e2L0hYQoVAqpVCwKA8RxfF+SMvDWl5WReXhA+gcIkSGZDpEiYvu4Xxsc4tzCYkYNeIyExiiiTMTBBnfnXu5bnPBTNw/+yQn955zz/l+zznfX1rO/5oRlWbDuELdwnYZYLfPmlQFtd9VaMzs0MyByfTCuCqwGHIV6PZ3kwl/TQ8UaoxK/H6f8AuIY4dnxgWNZt51SoZxSoFbIikgU+KBQtU6qlAfod+HFkuYscuLqavskplzSCwL/4mSjd0XyzEkkmBC6ocxiYIRHyfPPqH4ZqNAIGCnPxvtFBV8k5IN3xPLMExOQrf7lBzXhJLLlVyuBzvtv3FXrrw4QkQfGTCnoPyOsZ+fHTidL9KB0lczRIR/Iya/kpPQ75CSTOT+j1XXYzS29fs2dQw49hwYOFXfNthX0zrUu6P1dnd16+2svM7JOfScEbnyc8j9mTsfJWFf8hXfIaE+oK+ICZ58uydVdjCCj7Dbj77U0jnY1PzxncmWrhE0d43jg8PjaDz0EI2fALsPAZX77gwU1199/4a319kJsmP6BJdJoHYvL9cOmSzghlg6NkYMJ8n4j0JxNyvN4TidF2Y3tPSdL9vSg4TUCpTXfoNMSyvW5DSQ1oS09fuRY+9BZUM/qtpGkLP14q7rAq/TV4SiX7bz+Z6sDOcjiURLgh/7QSjqIt3np0YJ1XWnepo7B7EkJAZurvMRbc4Dj/sO3F3fhOvCuXBZMAfuLq+DIiEmZzahxHkLuaUnLPaXOfNYiT/Z7uNDG86a6hG2bPvUWOe8gK17LiJUtxICgRcMsZngeSyEVr8KubZurM52IsKYCb6nO7hu85GQ3oCc6kvDfkcmX2Flnky5o/v05rpzqKg9j5DweGLAR6QpAx5ubyF6hRXbWwZR1XAVmxr7kZS+izEWiWTIdXyHVNtX+azM9BQX732juKxztLTqOGxbzyBYu5wx0BvXgev+NpaZslFW34uizWdhcZyBdcvXUKrCwHNfgISMvVhtPfEZKzU9Fkuj1LqxAwW2w7BWnkRQSCy8iYHOkEp2uoBcSzpKqr9FfvlJ5NqPo6DiS4RGrIIHySMy3oaEvC769+a5KbVpyMytVuZZW5BlbUee7SgCg6Ph7c1H2LJVJOSFCI9cS0S/QFbJEWQUHUbWhh5ikAwuKQRdTCHi1u3vJwX+V7X8k7S0Ct6a9JrJtNwPkWE5CE1QFGMQokuEJ6miUH0KskqPkTLtwJr8A+R5EOpAPTxJDvq4EhiSdn3PSk2PRmOflZhSdS0lfTeplGaoAvTEYBGWhsXDk+eCpeGJSCvsREr2PqzOacPKtbXw9XkP73p7w5iwGTqzYycr9WTMSeVlyevqEJ9awwRIG9BZePFcsSQ0nhFfmbYTccmVUKpDmGz8VHoYVjigM9nErMyTSUqyvxqzomzQnLINMkUgBIt4zDXw+VwIhYshI/9aYkpCwucx1yam1DCYy6GNKmpnJf4dg7lYE5u46WFQiJkIKEm5JkEkVsDXl4KPjwi+QikoaSDUQcuJeBnCjUW9waa1s9nlT0dkdOESY7z959hEB6LMG6GPKYLOWEjECqGLtiJy+UZm5+HG9Se12qzX2GUzw2DImBsZV1Kpj7Fc0UUXQm8qQgQRDzPkj2qjCs6FReUlslOfAg7nD919latWtlcnAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def RunScript(self, Guid, Boolean):
                try:
                    pass
                finally:
                    self.Message = 'Delete object'



    else:
        pass
except:
    pass

import GhPython
import System
