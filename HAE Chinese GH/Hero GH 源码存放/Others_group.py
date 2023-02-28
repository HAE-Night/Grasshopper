# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Others_group
# @Time : 2022/8/13 17:17

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
import ghpythonlib.parallel as ghp
import urllib
import random
import json
from hashlib import md5
import re
import sys
import Curve_group
import csv
from itertools import chain
import getpass
import time

reload(sys)
sys.setdefaultencoding('utf-8')

Result = Curve_group.decryption()
try:
    if Result is True:
        """
            切割 -- primary
        """


        # 新建视图
        class CreateView(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-新建视图", "RPP_CreateView", """创建新视图.""", "Scavenger", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("060ef351-db97-42cf-afbd-e1a71f122236")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Create", "C", "创建视图的开关（输入t开启）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "视图的名称")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Wide", "W", "窗口宽度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "High", "H", "窗口的高度")
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
                                                                   "RPP-字符串处理", "RPP_StrHandle", """字符串处理插件,处理存在的符号信息""", "Scavenger", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("33a6d2b6-35df-4a34-b578-256678fd2b3c")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "文本信息")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "C", "要处理的符号, 不输入会默认全部清理")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "选取列表中指定下标的字符串")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "a", "A", "字符串处理掉符号后所有的字符串")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "头字符串")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "尾字符串")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "O", "指定的字符串,若Index没输入,和End一样")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Rest", "R", "从原列表中将指定字符串的删除的剩余列表")
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
                                                                   "RPP-字符处理", "RPP_StrHandle_02", """字符集的拆分""", "Scavenger", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("20565a9c-625a-446e-9ada-ef20f21c68e6")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "T", "字符串")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "S", "符号")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "结果数据，列表形式")
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


        """
            切割 -- secondary
        """


        # 百度翻译
        class TranslateByBAIDU(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-百度翻译", "RPP_TranslateByBAIDU",
                                                                   """通过百度API接口进行翻译，需要ID和密钥""",
                                                                   "Scavenger", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9258fbd5-2438-4bd4-936d-1f43ada88db0")

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
                self.SetUpParam(p, "Text", "T", "待翻译的文本")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appid", "ID", "翻译的API接口ID，不输入会有默认ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appkey", "KEY", "翻译的API接口密钥，不输入会有默认Key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "To_lang", "L", "翻译成哪种语言 0 -> 英文，1 -> 中文，2 -> 粤语，默认为英文")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "翻译最后的结果")
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
                        payload = {'appid': Appid, 'q': Text.encode("utf-8"), 'from': from_lang, 'to': to_lang,
                                   'salt': salt, 'sign': sign}

                        form_data = urllib.urlencode(payload)
                        result = urllib.urlopen(url, form_data).read()
                        return [_['dst'] for _ in json.loads(result)['trans_result']]
                    else:
                        self.message2("字符不能为空！！！")
                finally:
                    self.Message = '百度翻译'


        # 图层重命名
        class LayerRename(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-图层重命名", "RPP_LayerRename",
                                                                   """重命名图层，需要csv文件数据导入，会自动重命名图层""",
                                                                   "Scavenger", "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("03fd28ac-1bcf-4977-8d8b-5a818646613c")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Button", "B", "开启翻译按钮")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "CSV_File", "P", "csv文件路径")
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
                self.dict_csv_data = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def read_file(self, file_path):
                with open(file_path) as csv_f:
                    read_line = csv.reader(csv_f)
                    ch, en = [], []
                    for _ in read_line:
                        ch.append(_[0])
                        en.append(_[1])
                    csv_f.close()
                    return ch, en

            def find_contain_ch(self, origin_data):
                ch_list = re.findall("[\u4e00-\u9fa5]+", origin_data)
                if len(ch_list) != 0:
                    return ch_list

            def replace_str(self, origin_data, wait_str):
                count = 0
                dont_str = []
                while len(wait_str) > count:
                    if wait_str[count] not in self.dict_csv_data.keys() or self.dict_csv_data[wait_str[count]] == "":
                        dont_str.append(wait_str[count])
                    else:
                        origin_data = origin_data.replace(wait_str[count], self.dict_csv_data[wait_str[count]])
                    count += 1
                return origin_data, dont_str

            def rename_layer(self, tuple_data):
                origin_str, relpace_str = tuple_data
                if origin_str != relpace_str:
                    matching_layers = [l for l in Rhino.RhinoDoc.ActiveDoc.Layers if l.Name == origin_str]
                    result_layer = matching_layers[0]
                    replace_layer_name = relpace_str
                    result_layer.Name = replace_layer_name
                    result_layer.CommitChanges()
                    time.sleep(0.25)

            def RunScript(self, Button, CSV_File):
                try:
                    CSV_File = CSV_File if CSV_File is not None else "C:\Users\%s\AppData\Roaming\Grasshopper\Libraries\HAE_Vocabulary\Translate_basedata.csv" % getpass.getuser()
                    if Button is True:
                        c_layer_name, e_layer_name = self.read_file(CSV_File)
                        self.dict_csv_data = dict(zip(c_layer_name, e_layer_name))
                        all_layers = [_.Name for _ in Rhino.RhinoDoc.ActiveDoc.Layers if _.Name is not None]

                        handle_list = ghp.run(self.find_contain_ch, all_layers)
                        layer_index = [_ for _ in range(len(handle_list)) if isinstance(handle_list[_], (list)) is True]
                        copy_list_layers = all_layers[:]
                        temp_info = []
                        for _ in layer_index:
                            en_result = self.replace_str(all_layers[_], handle_list[_])
                            copy_list_layers[_] = en_result[0]
                            temp_info.append(en_result[1])

                        final_handle = list(zip(all_layers, copy_list_layers))
                        ghp.run(self.rename_layer, final_handle)

                        tips_tranl_info = set(list(chain(*temp_info)))
                        if len(tips_tranl_info) != 0:
                            for tip in tips_tranl_info:
                                self.message2("“{}”没有对应的翻译".format(tip))
                        else:
                            self.message3("图层名已全部替换！")
                    else:
                        self.message3("开启按钮替换图层名")
                finally:
                    self.Message = '图层名称替换'


        # 获取文件路径
        class ActiveFile(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-获取某些数据", "RPP_ActiveFile",
                                                                   """获取犀牛，Gh文件路径以及当前时间""", "Scavenger",
                                                                   "Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a7f1dc8c-0093-4c72-8c53-bfde0f8d0365")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "x", "U", "更新时间的按钮")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "RP", "RP", "犀牛文件路径")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GP", "GP", "Gh文件路径")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Time", "T", "当前时间（打开Gh的时间）")
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
        return "Others_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return ""

    def get_Id(self):
        return System.Guid("a252e0f7-b694-48e1-9f4a-e146b5a80251")
