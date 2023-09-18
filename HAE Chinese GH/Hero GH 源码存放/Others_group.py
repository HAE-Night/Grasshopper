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
from Grasshopper import DataTree as gd
import urllib
import random
import json
from hashlib import md5
import re
import sys
import initialization
import csv
from itertools import chain
import getpass
import time

reload(sys)
sys.setdefaultencoding('utf-8')

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:
        # 新建视图
        class CreateView(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CreateView", "V3", """Create a new view.""", "Scavenger", "L-Others")
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
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Create", "C", "The switch for creating a view（Ture On）")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Name", "N", "Name of view")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String('HAE'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Wide", "W", "Window width")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(500))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "High", "H", "Height of window")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(500))
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVaSURBVEhLnVZrbBRVFB6QSDBK/EMiWFQUSrozcx9zZ2crAQpCY9FCiWlFCLEF25nd2d0Wu33s7uwytGvLxiKPmqiJ+EMxUaMx4OOPhmBijOGfQEiICsEARkEIEAMGaq/nDGNLQY3hS27mnsf9zuOe2VmF+emIGNjUKKWcpNwEq5yuiJYzzwrfvidU3Rlo3u6ufrUgrWJqUagKwAvubnNrp2xy3XtD1Z3B7I7PF0BkeMltoUrxfX8y8eI/MS9+xdicbAbFZNSLUvtCc6jb5cXk4yibpdRy09/0KO4RvM9dxgbSM3Bftys9NVbOrAgMes4+wfLO8UAAmH67xrakJM/Hf6Q5+yTqWMH1gVyKwRelsTUjQc5AAqd0L/4Z2qsH3blRsJNCvIiy5SdWW9uzEvcKkAyJwU65wEs/hjIrJrqwPdW99sqoZy+2CimKVdJs6zazpWE2zbW9CcTXmed8q+edM3hG+G6j+UqvJHlnH8pGMT5MCokR3CtGrnVRdKhHmsWkjTKFgzRrnxBZZy31Esd4ITHA+9plFFpjDWXmiKLbQH2s0PkKWiktPz3dKDr9AgJo+fgJ5GCF+CEt23YQ90pdOj2VevHfmZfYh72D9oyyHns7z9nLKByATN9ipXYZtK0fnn0pyfCZbStjAJZ3G6DqT6Flp6Gyi7GiG6OFxDUIUAoCIEjW/hCCXIjCpYpyRsY6NyxkRaeWeM4PoH+dFBOjPNOyknW21PLO5mUksz62oHvjfTCFv1JoCwQ6Tbtbu6FFJw3P2cP8pCS9rU+E9DABWXtNkN3m1BnI+nJNTc0UyGI1BDgOtnhwsf0pGrorNQcOTMEny9sf8FKHhLsYsXpaKyDgfl5qH4XBuUQ7mu8PnBEsl54BWVwVMAm0t+1z1Omb3bVkS/I87mlf+3f0pY5z1E/uZqWOj0h/+mfU83LHMwKmRcs7pwI5b++MDntSzznfoDwBJNv2hbUjJ41sWzPKIu9YvHXNMYOQMomJo3T5YslwPblUklp4auRlc1Vtkvenr2h9ye3BmdzG1aLcdUXvecFDeQIibvMD0R1drK6ubrppGJuYph2hVVVSCENSXZOReZUjamXlZVjXSSQS6Dmlkgh+kQvRC+emIg9PPjerqanproD0VlgPz62mhBzFw4xRqanqUVVVy1VVVSuYrq/jnKfwiTLot6Kdqpo0GIMk6BHG2IKQ6naAU45zKjlnUtPUrzVNeyo0KaDfCYHP65omCSEXKKW7QpMCfk9rqnbQ4FyCzyjYnw9N4wCCghAcDusSMusK1QFA93EQVFXHFoeMgXhv6IKYpENFDFoGVUims3WhHn57TL7KMJjUdf2Pm7NGRDlfHLRKGyf/e0EVuJaErgHgvINBoJI/oZIYkJuzKSXnIMtrkHl96DcGSvXBfwuARJBUOXQdAwRZDwFGiK6fhNZg9hzLPRvaJ0DXtdcYI/9cASEY4I3QdQKA/Be8EwXHCQ5/iUGgd++G9jEQTevk/1HBrfeFgGHZg+Tgsz9QQBWzdE09i5cMQd6vr68f+0wKIR4Cx2s4PTeTh/J1uINHQlelsbFxGpC/JwwDbefA9mBogl5HIha042LwUlF62LCspaFJiUQiLdgOXFB68MQF+g2hi2KBP1R0CMkh+CV4T2KhaRz6/PlgUw/faBeMG6WfQAUN8Am9G+6oBvr9NqwDsN6hKl2C+pgZWwVV78N2hW05Ar4kpLwdFRUV02CeByHQVQGBcN4h69+gKiQZhnbuYpQNg7wX9QbjUtwgvopv9syZM//fvxBSWTkHMhmAg99jWwx40TAgkuHCnwbUox399Hnzxj7+41CUvwAMcFBsM23lxAAAAABJRU5ErkJggg=="
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
                    self.factor = Create
                    element = Name if Name not in rs.ViewNames() else self._str_handing(Name)
                    if self.factor is True:
                        Rhino.RhinoDoc.ActiveDoc.Views.Add(element, Rhino.Display.DefinedViewportProjection.Perspective, System.Drawing.Rectangle(600, 300, Wide, High), True)
                finally:
                    self.Message = 'View creation'


        # 字符串处理
        class StrHandle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_StrHandle", "V1", """String handling plug-in,dealing with existing symbolic information""", "Scavenger", "L-Others")
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
                self.SetUpParam(p, "Text", "T", "Text information")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "C", "Symbols to be processed, if you do not input this parameter, all the entries will be cleared by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Selects the string with specified subscript in the list")
                TARGET_INDEX = -1
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(TARGET_INDEX))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "a", "A", "All strings after the symbols are processed")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "Start string")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "End string")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "O", "Specified string,if Index is not entered,same as End")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Rest", "R", "The remaining list of deleted strings from the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATzSURBVEhLtZRZTJRXFMc/ZoZ9FpbisM0w+/LN8s0MDFMEZC1UKkhUrMKggCgIarVAtVpZlAfTtLGmTSsPpom1G02aNkbSlLEDFEvpAxoNqYb4YLekLzbpWyct/577MdrWFJs29SQn891zzj2/c889d7g/y8zMDB/9fDRCgKHr16+Hpqam/ABiQqGQOur6f4QAZ7+cm7s4MTGhnJ2dVUxPT382Pz//JAEboiH/XSi5mxJ+OzY2lhQ1cbR+/c6dOyDAi2w9Nzenpu/1ovPfyOTkpIoAV8OhUGfUxIXDYdmV2dlvyH46amJFbCG9+/nlywL9Do6Pj0ujrofLrVu3dty4cePS8vKyMWpi1Q9fu3r1h+jyvhB4YWlpCeRbjJr+WdRp6oAnK3f75pKKQ7Qs9/l8G776Yu63gc6uM7QuYTam+izNE9cWFr778O33vveqc7eRreyebxUtJiWRxFyReKzgCuzIqy3DO29dwPlLH4ML8Igt9SG+SADn59E3fByLN29C11j7K5dvE+2x63yQlRcgrtiL2BIvZGUFiC3LR2yFHzHK5F/E/DFJ8VOKo7shHe5Cz9nTGB0ewak3XgPf3YL0gzsgIzv/0hF8vbiIY2deBtcXhHKkB6qT+5Db0wzD9gak0/4MUlNTHSwba6DpbYHUpPlpBSBPDCsPBmGpKYPP4YQ+OxsdTU+j2ueHzWBEXEsdXv3kI1z5NARPYQGSDrUiaagLqud3wVXghSfPAHtZEZyFPngMJlIj3IIb8ZkZd0UAl6YM522ohNdiBc/boatZh4z6SmhLA+AtFgyMjmDp9m10tLVBa9Ahu20T1nRtRfqzO8EX+eGy20V1my2w+wTYCeoozEdc1j2AUh62MDoFGKtKkHiyF8mDXeD6gzgw9gouvvs+Pjh/Aa2tQRj1eniMZuRrdNBtqoWNKnfZKDkVZ15bCFX/TqgOdyCtvw1SXVYUkKoIm9b64aEgeyAfj+1rhvz4HsiOdiBwehCWniCKdjXjzXPnYDaboa2rgKa+Chl7t4GnpC52co8bKQdbIX9hDxTUOuVg918B6m11EGw2sRKX0wFzZYnYivjD7ZAe24WcoV7U1lLFDodYYeLIXqiOdsIRKIBAJzJVFFNRXVCST3mkAyoC3QfEJCWE5X07kdNcD15wQTCZaZMJAjs2gVSHqSK6WIvNCqfbjdRDOyCn5CmU7D6gfC0Ux3avDlA8E4R8mKoiUBaBrNQqF53IQyDD+gqkPNdOyV1wuFyrAIofDkgeaIOc+sb6xy5YQQlYVWwyeJ8H6QeCcHjdBHAilfX6QQBr0WoASWJCWFtfjTU928VLYgB2GiNVzjbbCZDKRpLGz00Tw2BJJ+ihPXgHqwES4uLCAnsc7HJpTHWNNbDSBjfPQ9CboKWJSSagpeRxCPSQLFWlMFNB2pYG2IsDKwC6q1UB7CUbiv0QrNRznRFeepnsl42fvrpU3MAmZE3nFjgJyny+7DwYaFzZQ/Nq9DDTe2Cj/fcAReKMghzq/UHk0gVrtz6FnOBGZFArFCd6V/532P3QA0zvb0d2+2Zk7m5CCkFzWxthql6HrM4mKClWNdQN1XA3Ukb3Q6rP+VkEcBLJpMykjUidpojE9YdKeUNEZtVFYi15ERkp+5XaDREJiyNlPilvpG+jGHsvToy16SMxiQk/rgA4LpM07xGohvRRCsf9DknSyU9HIxKfAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def _regular(self, data_1):
                punc = r'~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
                result_str = re.split(r"[%s]+" % punc, data_1)
                return result_str

            def _division(self, data_2, sign):
                result_str = data_2.split(sign)
                return result_str

            def RunScript(self, Text, Symbol, Index):
                All, Start, End, Result, Rest_list = (gd[object]() for _ in range(5))
                if Text:
                    text_list = self._regular(Text) if Symbol is None else self._division(Text, Symbol)
                    All, Start, End, Result = text_list, text_list[0], text_list[-1], text_list[Index]
                    Rest_list = [_ for _ in text_list if _ != Result]
                return All, Start, End, Result, Rest_list


        # 字符处理2
        class StrHandle_02(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_StrHandle_02", "V2", """Splitting of character sets""", "Scavenger", "L-Others")
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
                self.SetUpParam(p, "Text", "T", "Text string")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Symbol", "S", "Symbol")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "Result data，list form")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVbSURBVEhLnVVrjBNVFB5RshoQNcaERBN03Yfbztx5dNruVnA17sYFQniIgEvR7m7bmbY7bXdLt9tO29k3lEeWVzBIFP3hA40xGDXBYAiJSqLEoD/AmAAGSHRB0EU0oLDXc+4O6EY3oF8yycy5557vnHu/c4b7Pwjv2DHVfv3v8G5KV3rWd833buhq9JXSd9rmCVB4ckCd37hTXZ/+SOmNb+Esa4q9NDlUK1mu9Mf3SFb7FWUgSZXBJJX7EsddVrvHdmFoaGi4S6iqHlWWzf9S2ZihJKdd8qVb/zWR68Dgck/sB2Wog5J8hBJTZ48MRPB92pf+qxJVVXm+qvqiq2XpSxL4CzntzA0JZDOywbU2xYLL/Qk7+zhkp1PXmk4q5fWg7cqpsryAr67+2RP3W/KamyQQc/rrSmk1lYsxKqZa9kjJQE7MBD+QetpZFZKpv2u7cooipvnK6uO1ubCurO28WYLwJnWwgyrxVc22iUHMaUfYsZn6Ufi8BW2SRF7mK6oO1JUSzypQNRJ4jJUzcG1SCMmWciXS/IT9eR1IrJTg6HL62WtZioR8xpdX7qzdlFnMCLLaWbT7966f9uiW3FwvPLW7N96BthtCyukFO8uLsweN+9BGiPA9P+vhVN2W9KJxgvAJ35rkQmUgcUyB+8IHjvWo2peoZkEmQ/jQoalyPjKIQUCKv8ze3n1PU0VFGRBc5WfOmucdTi2RQQyCqV8SC1EqDSSo2B+nArzLTI3Rr+ot6zY73Djc/YnHXIPJXXKPcVgqxk6QvD5KrBiroH7/tulqpVAuioQ6ymZUeEuJ5TYBFUFxfFfbKJ98bp+QafuNgFhkuFO5EHvaDg3qKEbTrMGAXeoxqAiBCWRDilFG0DT2bZlcU/MkIYRWcFyZd7DdjwQElAYVnnukdRmPcbyxFY1SITImDXXi3e1mwVUr4lNA/1gqsktAhJtF3FyIMIK3KL1VcThivJO/iHvcVjSAWYq97dQZ969ggWwomeAn8vjRfsMMoPPdCjizbLLaOT7d+gqfCpRId/ighOcKBJTSKcTp3CY4BZQs5ylqbXg/fDZ0vrZj6QTVuLOhdbY4fuKaDKNMNPVTElZgRkZqo344gXFAA2awAfGSn6cnbhedzo95nn8P19zQ3XaQkXorOp1tsAFNmEQ1gYQvc96M9iCc1R8yyqsrtN32YSBmpMiCmPqFRa8O3Ss4nMeBoIRrfyP4Ryf7zFDEJrgCjlGniDMICXKaafswQGVDGATUdH52cHmV4HD8KghCANfc+dDkBHmtg40RrEDtjpTDKLiC2oWht8v24eqtxN2goNNir4HaHvEufOpxqIBKkuTD9esE2fBIk9FUxjbZ8Ba0dXi0fDZ8nmtM+acRUzuDgSQrdmHOZtPX+KL5ELzvw3tBqQpW7LTaUN8CFVz1eDwPYBBGAEmJxdglNT+xa91FfT+qSOgOHWEGUM5e7EQMhvqXitHLLHP8N2Af9BrfKXPqSkDwo8vlYr9LJMBJi00GU/eg8eFmVsXiFzKi0mf8zv4VXcE30QYE4SUKNAYGvPZgD0D5Y9AHY6TXOCn7vO8LNY7DbAPgGgF2MlYq9xmf1w1nSu6B+EmUO5N3MrDQdoeJmgm+gecmQYPh2YK+j0mrA80yVtYTOysq8td8jeMd253zmCENG42NCqgaK2EzCMfEEBCnWr4At4n/arK61RALkbehoq2itvR+Zku3rpK62hoFp3MUJDrMHAFqts3v2ZyjQrrtU5hBwzJkjIFRPaQ7dIqA6mzXm4OzpuY1kOhc+5NzRJ+ZLnQGgkKoWcBvPrZyMckEt/IdLUXHvPqZzInjuD8B8bObwzxTKyoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            punc = r'-_#@$%~&:'

            def RunScript(self, String, Symbol):
                Result = gd[object]()
                if String:
                    self.punc = r'-_#@$%~&' if Symbol is None else Symbol
                    Result = re.split(r"[%s]+" % self.punc, String)
                else:
                    pass
                return Result


        # 某度翻译
        class TranslateByBAIDU(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TranslateByMODU", "V5",
                                                                   """Translation through a certain API interface，ID and key required""",
                                                                   "Scavenger", "L-Others")
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
                self.SetUpParam(p, "Text", "T", "Text to be translated")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appid", "ID", "Translated API interface ID，if no input,there is default ID")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Appkey", "KEY", "Translate the API interface key，if no input,there is default Key")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "To_lang", "L", "Translated into which language 0 -> English，1 -> Chinese，2 -> Cantonese，Default to English")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "Translate the final result")
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
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.endpoint = 'http://api.fanyi.baidu.com'
                self.path = '/api/trans/vip/translate'
                self.lang_of_kind = {0: 'en', 1: 'zh', 2: 'yue'}

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
                        Message.message2(self, "The character cannot be empty！！！")
                finally:
                    self.Message = 'translation by Baidu'


        # 图层重命名
        class LayerRename(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_LayerRename", "V4",
                                                                   """Rename layer，csv file data needs to be imported，the layer is automatically renamed""",
                                                                   "Scavenger", "L-Others")
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
                self.SetUpParam(p, "Button", "B", "Turn on the Translate button")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "CSV_File", "P", "csv file path")
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
                                Message.message2(self, "“{}”There is no corresponding translation".format(tip))
                        else:
                            Message.message3(self, "Layer names have all been replaced！")
                    else:
                        Message.message3(self, "Open button to replace layer name")
                finally:
                    self.Message = 'Layer name replacement'


        # 获取文件路径
        class ActiveFile(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ActiveFile", "V11",
                                                                   """Get Rhinos，Gh file path and current time""", "Scavenger",
                                                                   "L-Others")
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
                self.SetUpParam(p, "x", "U", "Update time button")
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
                self.SetUpParam(p, "Time", "T", "Current time（Time when turn on Gh）")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAULSURBVEhLnVZtTFNnFL79/rrtLQhTcQyHOow6tZMNIcoobMGRoaJmitDyIaUIshakX0BLi1RFMTqdAhOzyaJTaVDAr2xGXTbdluzHsj/Lku3H9mtZFvfHZNmS7dl577VoQ41zJ3nSpPc9z3PueZ/3vJf7j5FBsBJshAbCZoKFoCP871AQ7DK16qYy+9n7mvwV0JYWQFe2FtriPKhW5ED+TOpPtGaIsJIlPE2UyHSabzSFq2DcVQkh1AQh0iwhLP2qQ43Q++vBV70J5cLMfyhnkGAUs58QLsXz88C3VsK8ZxeErkaYfPUJkO2uRuF+P1ZFPdAFSSjkhHaDFTKN+lvKXyDRJA+3ctlCpPXshJESDd7aGeTqDjvWHQxibOwCsoMt4NqrUDoQROa+dujqN0Jm0P1MPGzPZkSxkirXdzuQ0+uG49gBGHx1CSKMfOWeNly7eAnnYzEsCL8NjacGg2dGkdfngabHCYO9HJxC/gXxsT2cDo1Mp/3B6KqCEHRCQ0Ql+wKoPtYPNRHw3jpRQEn/50c7MH72IwydOIFTH47iKJF/MjGF1VEvlLttEPp2QVuUC+J0S9RSNGhezYVAPY9Xy/pcTCJbj+6DioiNJMLELBE3kR+HLxrG1HgMt8cn0DsyiFR/A70tFRJogIk2X55i+pV4eZFdplV/zao3dTmmBRjkJPJGfzc2Hemj6m1iv9cfDCFGbzAxOYnRc2dhjXRAR8J6aqXwIE/obYHW+jJ7C3ZuuGzlouf+FsI7E8jjUJDIhoEerDsUhspjxwGq9vNr1zEUO4e5nY3g6DlPe/VojtDtBO/YDE4mu8AEKsT2kLcfXRSHkcBEXuvvQnjkOG5SvwfOjULXUSO2Ll51AlibqF3Upu+YQJuePCyQNWcsfABWZRkJfHZpCmcuT8DY3Qi1tyY5OQPtgUBrFFlz7jGBTv2W1x8rwMjX7PXiylgMF65MYlOvH5ZSK2a5qkVLJ8sRBciNdGDvM4FWXXkRjYBEAVadnGz3YsSF82fP4Bb1PfdQF0wbi2GZOw9LrAVIbdsGQ6AmIU8EE6AJoMic/RsTKNOssYg7H1/AyJnns4LNGDn9Pu5e+xhb390Prq0SPDltzlvr8FL2YuTVHkdGsA96X2WiANuDjlrITTwbHVyGcn7Gn0JP0zQ583t6pwOHTw3jzuXr6Dw9TORVtOF1MPp3gPfbsLjKj9XNd5G/+w4y/RES2T4twNpjqN3IbPoBE+A4lfIW37xV3BgtkQv0ir3Dx3CbNnWY7MhOss7zcGTwgTqkeJ1YUX8SeU03kO+6gTk+D42WakmAusHGOzGvlwTIqupXlsFID1iVnsHDuEnkF6cmMT/UIo2AB+RxGAJ2pLudsNhPIr/hKnJdYzAHnDB27YCx3Q6ZXvsj8aokehYKxVeK+g0oPRJBYa8H0dPv0ZQMUWu2P9aOTCTN7cBy+ztYW3sVOa17wfeRhVctYdVvk4gfxlIuzfxHdncLbIMDKNrrowNmS0r8KHhykbmjHovsHmT4WqGtsDLymEQ5Myq4zNkw0inV0+hlpzgZaQK8dNpZW6J06WwpASeXf0k8eokueZTL0sy/G+zrpSuSuSuwIzk5WVaIkL3Jlux6pdwpgklkeUIsIoyrli6EwVYukrGTnnAvkxXZBGYfAfL0lF9ofbuY+ZRRQBiWzzJ/r3wh6y917lJo8pZDTV8Uiqy59+jD4FN6zi6WNLZ4ZnDcv9UjRVfhEDXqAAAAAElFTkSuQmCC"
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


    else:
        pass
except:
    pass

import GhPython
import System
