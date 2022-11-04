# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Others_group
# @Time : 2022/8/13 17:17

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import urllib
import random
import json
from hashlib import md5
import re
import Line_group

Result = Line_group.decryption()
try:
    if Result is True:
        # 新建视图
        class CreateView(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@新建视图", "Niko_CreateView", """Create a new view.""", "Hero", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("060ef351-db97-42cf-afbd-e1a71f122236")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Create", "C", "Switch to create a view (input t on)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Name of the view")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Wide", "W", "Window Width")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "High", "H", "Window height")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGzSURBVEhL7dU7SFxBFMbxG0ULJVHESgkGowEtxMY6ICmCUUFUFNTOIk0IpPCFoIXEhKSxMAQEIRDw0fioFK3EWhtNkzRWIZWFhGh8/r9lZzk7ey+7y1qJH/yK3Tln7sy9c3eD+9xWatCDEUxhGN2oRk5pxRb+4zrEGTbwElmlHMsImzTKd5QiberwE7b5HzbxCeP4jG1oB7buEE8RmVr8hm36iqimZ5iHrT9CFVJShl9whVq1HmQm6cc5XK928hBJ0S1wBadohh+dpEl0xj4lpwUXcHOsIpFRuAHpgk0B1mBrFpEHG+3E1rxF0ITL+BdX0Ar99MI2Ou3w8xGaR+M6BMF0/IP8wQP4UZOrsSbgpxDHcDVBI9wD0pU/wI8etmuwXsHPDNy4Dkos72Ab+2CTjyXYmm/wdzsIW/MaiazDDWhHOhV+dM+HELbyDrh7L1pQUh7hB+xFBpBJtHI7+T6KkJIn0JvoCkW3oh5hacACbL1e1gpERj/BB7BNeoF2MIv3+IJduOPt7OEx0qYEWrltTmcOxcgqL6CH/xdhk55gBc+RU7TtNujVH8Mb6M+oEnc6QXAD23K8xwF2+XMAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def _str_handing(self, single_view):
                qualified_list = [_ for _ in rs.ViewNames() if single_view in _]
                last = qualified_list[-1]
                str_list = last.split('-')
                str_part = str_list[0]
                try:
                    num_part = str_list[1]
                except IndexError:
                    num_part = None
                new_str = '-'.join([str_part, str(1)]) if num_part is None else '-'.join([str_part, str(int(num_part) + 1)])
                return new_str

            def RunScript(self, Create, Name, Wide, High):
                try:
                    Create = 't' if 'T' == Create.upper() else 'f'
                except:
                    Create = 'f'
                self.factor = True if Create == 't' else False
                Name = 'New View' if Name is None else Name
                Wide = 500.0 if Wide is None else Wide
                High = 500.0 if High is None else High

                element = Name if Name not in rs.ViewNames() else self._str_handing(Name)
                if self.factor is True:
                    Rhino.RhinoDoc.ActiveDoc.Views.Add(element, Rhino.Display.DefinedViewportProjection.Perspective, System.Drawing.Rectangle(600, 300, Wide, High), True)
                else:
                    pass
                return


        # 字符串处理
        class StrHandle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@字符串处理", "Niko_StrHandle", """String processing plug-in to process existing symbol information""", "Hero", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("33a6d2b6-35df-4a34-b578-256678fd2b3c")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text information")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "C", "Symbols to be processed will be cleared by default if they are not entered")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Picks the string with the specified subscript in the list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "a", "A", "All strings after the symbols are processed")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "Header String")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "Last String")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "O", "The specified string. If Index is not entered, it is the same as End")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Rest", "R", "The remaining list to delete the specified string from the original list")
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
                        self.marshal.SetOutput(result[3], DA, 3, True)
                        self.marshal.SetOutput(result[4], DA, 4, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPOSURBVEhL7VRrTJNnGP3E2dIi0BZbxFYxgy0SxDGg0BZZvWI1AQ2g2WCGgUPEqkUtYAW5tBR6s2Bhomz7s7lsahxZZtymxl2yuWVhTF3mlMYLmuwSluzHkg0zu7Pnu9hYY6Lifi07yZP39nznPO95n3zM/3ggUlNNYoVSPyiVLxiKjkt/N1o2iYhLH5LN0B9TaoypAu3diJfP0qy4Xfv8WWxdPwxzxaNHfeUwFmRsgVisWSGQRkA2Z27x+N4GYKAF6N8dGa80A7105rUAffec3YlX2wC9thkMI14icEZANju5aLzL8gd6GgGfFeg0A446GjcDTpq/7gI+PQ64SIRds/vseddWgC2szwbkZTeRQMwigTMCYQE/JXt2AO+/CZw7C3z8HlXYCly9BA6njgFHDwLHDwGffwiceBvo3gYM0g0M2hYSYIw8ZSTCAm6q8K0AT3bpHHDlIhEOAmOjQCgEfPERcPk8f/7jGHDyKODfCZjLv0aSughyZd6VhCTjJwplfonAzSEssJeS95GnF0eAm1d5sv3twJEDwK0JoLkS+OFb4OebQHsN/zZlpneQNEeHivU1aG21Y8PLDYifYbggcHMIC3jqgTf8vMAZsofFV6eBwwP8/AjZc+0y8NMNwE3WWKuCmKnJR0NjI/b1etHRYUdm9urfRdO1/ZI4/aBcqee6KizgoxuwnrNVsiSjF4ADdnpE6q7gd7zwZyd4qwLUEMsM/VhcWIyeHg/a2trxdJrpNjMl47AqqWC0dK0Z6uTFQUGgeNy782+uJdlO8tBb+KmbvHQjduylPXbOWujbzsdrZJ0+247VpS/A6+mGw+HAssLyUKxc92fVBgt8PjeefGr5b8QfL1fPXjVhrQ6iZdMN2DbysauGRjaENRfh9Rg6zNdDGfOsMC5dAw8J2O12TqR+exORu2Db3QqV+rlrjEajkySo8j9ISFw4olDlf/OgkCcavlSoDMPR07WhtPkmNDY1o7PTAZfLyYXf7+YEjUtexFRJtpO16FEhnSLOHMrVl3BVu7qdnEBVtQV1m62o2bgDWt06SGJzTzFUvPDNQ0KclRIdm3u+0PQSV63T6YDX243StbUQSXOC5P+IVKY7EyXOMVN2FP/RQ0Icl5WiUC38pWzdJs4Ch8POPW5VdT1iZLrvGSZZJqROEk88U2soKEcgwPZ7B9zuLmyzNCFBVfAr/fRT+KTHgEj0bFqi2jjB+twX8MFm2wNN8tK/GGb+ff8/k8JUUebKmepFt0rK6jAvvQhMVEalcPTvQSLJ0U6T5g1Mi8mqELb+02CYfwCwPMJHB31y/AAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def _regular(self, data_1):
                punc = r'~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
                result_str = re.split(r"[%s]+" % punc, data_1)
                return result_str

            def _division(self, data_2, sign):
                result_str = data_2.split(sign)
                return result_str

            def RunScript(self, Text, Symbol, Index):
                Index = -1 if Index is None else Index
                if Text:
                    text_list = self._regular(Text) if Symbol is None else self._division(Text, Symbol)
                    All, Start, End, Result = text_list, text_list[0], text_list[-1], text_list[Index]
                    Rest_list = [_ for _ in text_list if _ != Result]
                    return All, Start, End, Result, Rest_list
                else:
                    pass


        # 字符处理2
        class StrHandle_02(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@字符处理", "Niko_StrHandle_02", """Splitting of character sets""", "Hero", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("20565a9c-625a-446e-9ada-ef20f21c68e6")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "character string")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "S", "Symbol")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "Result data, in tabular form")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAD9SURBVEhL7ZLBbgFRGIVndrWsXT2DSMq7MK1Ww9ZWPAAPVFQ0ghCKtLH1Pr5j/rsgInFDN+ZLTs45M/LfP3cECQmOkvltCMPw0+LVKDK0hUcq5A7qEl/VoUwf4G9x9SPSYAW8Z97Hcvi3uoM+QVM0s0fn4YdtLItrazdYrq11wFDdGxv8gn9ZHyBt7a6kQp/gH3G9Z97Nj6lxRT/4c1w9YcjI4gE8X1r0Rh9xbB9SVMlzvIby5DX6JRf08mLcYHz/v8YXmAavrP/JvWHA1Fxby3UleWVB31j04gHVGbKwwRnUIGvrpvUtSqMUuhgd8IiekIadkt55H5DwnwTBDvynKb0vn/7dAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            punc = r'-_#@$%~&:'

            def RunScript(self, String, Symbol):
                if String:
                    self.punc = r'-_#@$%~&' if Symbol is None else Symbol
                    Result = re.split(r"[%s]+" % self.punc, String)
                    return Result
                else:
                    pass


        # 百度翻译
        class TranslateByBAIDU(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Niko@百度翻译", "Niko_TranslateByBAIDU", """Translating through Baidu API interface requires ID and key""", "Hero", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9258fbd5-2438-4bd4-936d-1f43ada88db0")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "Text to be translated")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appid", "ID", "Translated API interface ID, if not entered, there will be a default ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appkey", "KEY", "Translated API interface key. If it is not entered, there will be a default key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "To_lang", "L", "Which language to translate into 0 ->English, 1 ->Chinese, 2 ->Cantonese, the default is English")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "The final result of translation")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASDSURBVEhL7VRrTBRXFKZp0jQxjW0sLa1NWi1iBYTtssvszszugOyyK+yyAwhYYniDNZQ3EkCgoNZXrbx9LMtjYbeCaCqJgRjBGmtUpFjWByUgNKgISosNoAWLc3pnnLJAjbRJfzX9kpNzzz1zv+/eufccm//xtxGgkK/SikS7VU5OexYz9jstRdnzSxeHUumyRCPB2qJiwktTv8grTszNKPnTUnbmzo5ZY/PR0WHlWgnWipa+pJFLxToZURcUFPTKM7bngMbxD1XOTmbjr4OGhkfD01X3eqarhnqmq0d6p4/0dXKejdl5Nl87NqhHJzH7SiTL/UjidICcvONPyZppGWmmvcTLeForfElypWqtU51+wHLc/PMAVPR3QdXdbihub4NAby8oufItVN3p5ua/5vKWBvS9SYVhH/jh+GuhJPkG8u/q5HipjiT28bRWzAr8dO2YabQf9Ld+AOODW5C6Ox820hpI3VPAxey8mc33W+rRiRtZAZ6Cg5+c8NeRuJEPrVgoYBi8AcVXzkJExCYov3YRwsNCobzrAtSP34Wmp2NQeftmk9LRsVCLYW/zFBz8ZFJfLYnv4EMrFgrU3O/jdr9BpYAt6YmwKVAHKTvzRioHb1RW9HZWF146k6gWCGx1FPV6kEKxVKlULmF5WL9BTdoGOTrOv3CrgOX40YeDcPD6JYiKjYTiy61Q0XcVStvPXvcRuHaI31ppcHz1vSKBrcMhqYPIiMwkW4OZhSuE21me1csEoR6OUqO3ED/lLyfCOHIWc19R/eTQTPXtm2BA/7tmdGC6cerBTOHF00XS5Stqfrwalz0xnlY9PhTP2cS9hOqn48nVj+8nGJjxpLKp0QQ9m28/E5GjFGLnFAq3pZwAVwc41hYTE1mafbgw8ejjkW1Fl1sPJudnFWcc2JW7OSneg1j1cQXDpLUA5ANAFrJczredCEc+ZzYGKADmt5QGySq3WvZlcQIs2EqmJe771QLXbq1QuGO9i/NJrVBwYJ29fbTUzu59ygUzMU9SvgHIhKnRRDh3KgwaK0MgOsATmuo+gQst4fD7wyQkkIl8oon4SGTyoSg7nt4K9I5N/jKigBZbC8YHw9ZQa915gWywfBcFWzZ6QYM+BD4NQd4QDJuD18GAJQ4JZL9YQEtJ/tJjFgp0tEbCtng19HbGQkasCnq74iA92ht6OmIXF0CFcoKWE8F8yGG+QBaMDcZD2S4a9mVrIUzjAftztHB4rz9MDn/G3cOLT0CSatRTvqflsqpAD9kR1Mjy14tJB8pZbGRmUtElsxeawe0UmK2g3xuIxpnP5p6kIY8ueyLpGL7arVYlk73D085HAKoL2kOmQ+S/6AgizUdM2Xm6ujczzNbtDJNznmHSrTaVyo/TxphHyZMMk3eemUzO9XB2b9ZQ1Js85fNBk6QD61Erfhl1zQodQZ7U4LhxrgVQpFFHksYvszUlE8MJnj4S/HNaJm9Bm/uKI/knQL+P8BVJFKo5phZLvXzcpb5eAqxMJcLbtDg+RuNyKb/k34UfSWJ+xJwW8R+Ajc0f5niw7bNbCOcAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.endpoint = 'http://api.fanyi.baidu.com'
                self.path = '/api/trans/vip/translate'
                self.lang_of_kind = {0: 'en', 1: 'zh', 2: 'yue'}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Text, Appid, Appkey, To_lang):
                try:
                    Appid = '20221022001408099' if Appid is None else Appid
                    Appkey = 'JY1NofDe1FPcaCDqtmnQ' if Appkey is None else Appkey
                    if Text is not None:
                        url = self.endpoint + self.path

                        To_lang = 0 if To_lang is None else To_lang
                        from_lang = 'auto'
                        to_lang = self.lang_of_kind[To_lang]

                        def make_md5(s, encoding='utf-8'):
                            return md5(s.encode(encoding)).hexdigest()

                        salt = random.randint(32768, 65536)
                        sign = make_md5(Appid + Text + str(salt) + Appkey)

                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        payload = {'appid': Appid, 'q': Text.encode("utf-8"), 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

                        form_data = urllib.urlencode(payload)
                        result = urllib.urlopen(url, form_data).read()
                        return [_['dst'] for _ in json.loads(result)['trans_result']]
                    else:
                        self.message2("Character cannot be empty!!!")
                finally:
                    self.Message = 'Baidu Translate'

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Others_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return ""

    def get_Id(self):
        return System.Guid("a252e0f7-b694-48e1-9f4a-e146b5a80251")
