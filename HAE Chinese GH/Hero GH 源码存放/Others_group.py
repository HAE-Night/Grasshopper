# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Others_group
# @Time : 2022/8/13 17:17

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System
import Rhino
import rhinoscriptsyntax as rs
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
import scriptcontext as sc
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
import os
import shutil

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


        # 抽取字符串中所有数字符号，并通过新的格式符号连接
        class ReplaceNumText(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ReplaceNumText", "V12", """Extract all numeric symbols from the string and connect them with the new symbols""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e89f1ee6-68fa-4f7d-94cc-fe5bbfb7b81e")

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
                self.SetUpParam(p, "Text", "T", "The string to be extracted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Split", "S", "Spacing step of separation")
                STEP_NUM = 3
                p.SetPersistentData(gk.Types.GH_Integer(STEP_NUM))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Separator", "Sep", "Separator connect two-character")
                SEP_STR = ','
                p.SetPersistentData(gk.Types.GH_String(SEP_STR))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text_List", "R", "Result of the final character")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPpSURBVEhLrVVbaBxVGB6vbSMVrPqg1tjAlrI7c24ze8tumpSgIlgIgttaY1S6uzOz1+xu4l5mL7Obpm71RcyDWBUK2qcgBGzfjZe+FC22PliLfVCEEtoqeOuLOP5netKklC1NyAc/Z87/n/985/znO2ek24HZeax1p8fobGGM2ZnHhXvjgOrmz6SVPodq+gnSylwizdTzIrQxUCxjidSMffwb182LuGa84wY2CthKnSd25jyuG6fpTN4hVnL9O9BsvQ/K8ANppN4TLl6iX0klUfHpsX7S0DuoYV7x5HKbRHhtQPX0Ae2tKQdKcW2om3rous/8g9jZOdSdGob2U1TVf9GO6ve5CWsFsoxvcDl+FMpxljVTJe4jleQM6+QWaCX5Je1k3tbyE/3u4LWC2WkPtgzH85xnExxkHFvmTyIkaV5vm8nKGSZtWb9MccO01TeLvDwLUOdTbLbgBD+oDwzLzEsJuUopdRhjH46MjNwrUu4cvKZQ60tAclxppQ3QfAa30hdI0/yIxylGC4xRR9O0qJvQA5pt7FEPF77DzfRF2s5+z2Ynu755+36J1lNPw8odT278wRf6+h/jg2XLeBVb+p+2Y99N0Q2CPe5MPUCtZB4U+B8qTIwp0wdLcEH/QY30SclXjG9jxVc887HYPZrKloJaMMsT2GTcKznOXUDwGSfw+/0Bd6YeINV4Fs7vquhKcmH8WV5q0ZUkv6p2+URQ799Hw6NPCLdECTpBKXECgUAuGgoNhVZZJBxOBPz+95/B+AFqmwkQym8xWCjP00oHHsHN1AoBI8SgBDuE4G9htU8KNxDgLzRNdVSVOZqq3mQqHD5v8c5di6ycKKF6ammZgNVffop2sisEsKIdDFYKuzguXC4wxvsJQR1ZlrnNrLIOQsrHGKGz8vaBAGsZBtylKyJNUg/l3gXxXBNdSYISyC4BpfPCdUcA6W7mLakmdO1IyaHtzFew8h9JO/u3t/D6mDuII7pOgmXs1ff24Zr5kq+cSMrV5MRO48Ub5+himQAOec0EwcNZQ53Nfw62wNrZ/cJ9M9ZLoNqmxeApV6p6CTVSk8gyv6a13KMivIJVBJ8IV08Ui8UtvB059tpmeAH+lcvJaTewDLg/4msFnADUwlV0bnc0Wo1GB6vRwVttMBSaAxlfiATC40O1OOZaR+UkEtP0RlhVEaUYdkDg1mqOH7QPl+8WUxlz4AF0GIbLNzpcR3bmL3k6ftt3ykUkEtmKkC+mKMq+XoYQimFFmQLtL3q93mGeh2rGKZDk6eCR3Pbdc1MD2qFsNVDNPOxOuhEgFWMH/GrPkHbmMuj/MvywFne9cXDr9agk/Q+463nj3L771AAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.default_num, self.join_str = (None for _ in range(2))

            def message1(self, msg1):  # 报错红
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):  # 警告黄
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):  # 提示白
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def extract_numbers_with_sign(self, string):
                numbers = re.findall(r'[-+]?\d*\.?\d+', string)
                return numbers

            def RunScript(self, Text, Split, Separator):
                try:
                    Text_List = gd[object]()
                    self.default_num = Split
                    self.join_str = Separator
                    re_mes = Message.RE_MES([Text], ['T'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        num_list = self.extract_numbers_with_sign(Text)
                        temp_str_list = [num_list[_: _ + self.default_num] for _ in range(0, len(num_list), self.default_num)]
                        Text_List = map(lambda x: self.join_str.join(x), temp_str_list)

                    return Text_List
                finally:
                    self.Message = 'Replace Text'


        # 将Gh数据写入到Excel表格中
        from System.IO import FileStream, FileMode, FileAccess
        from System.IO import File
        import sys
        import clr

        sys.path.append(r"C:\Users\Administrator\AppData\Roaming\Grasshopper\Libraries")
        # 加载Microsoft Excel的互操作组件
        clr.AddReference("NPOI")
        clr.AddReference("NPOI.OOXML")
        # 导入Excel相关的命名空间
        from NPOI.HSSF import UserModel as HsModel
        from NPOI.XSSF import UserModel as XsModel


        class WriteExcel(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_WriteExcel", "V14", """Write Gh data to Excel table""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6017aa8b-06bc-4cea-a929-f5901bc2a396")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Write", "W", "Write if set to True")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Path", "P", "Output path with extended file name")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Sheet", "S", "Form Settings, not written to default Sheet1")
                p.SetPersistentData(gk.Types.GH_String('Sheet1'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Cell", "C", "Cell Settings, default A1")
                p.SetPersistentData(gk.Types.GH_String('A1'))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Data", "D", "Comma separated data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Messge", "M", "Excel operation status")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                result = self.RunScript(p0, p1, p2, p3, p4)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQRSURBVEhL7ZN7SFtnGIdTtlbKoKtJTHJMjbWaGLX0ojYxJubupWVTsO06jbXVeInRbhpzT3qZzo2C0A3m0MYLdM6OdWjrrMLYWmqhY3PdrdCxMkZhF+g2KGPr37+95ySYpJox2F+DvfDwnXByfs/3fhfe//Wvak/E0VU47ZxVjjsuRengUEQ6LhVMdr5nWQjNVi2FZ61Xk6n5aOBy3dJAWywmdSnG2u4pZ1+E4u3uKDNObpRPO6G82APr9ZdQvTyIqhsDSexfOQvrQuibWEzqUkTab8unu5A33o68CEFjLsv5Nigm2mF8PwDLYgjmq8EkKq+dgWUh+FksJnUVjdhXiiY6oBxp4SgYaYXyTTvkJMif6oRpIQjrUpiTJFJFnVUuhldiMTxezesn0hivdULsN98UuAzL/L6K5Yx+4zLjr/yDCVZB7LeCCVQi01+Jwt4DUJ5tQO7ocejmPNDP+1BxxRvlchTjB2EY53xxQb6nNlPkM0FwygLmdDXSg0ZsCejB9+ix+QUVRB4ThB4Dtnr1yLGpIevUQhgwI2+0Nbp01NEqETsUbzlA+xcXyHqrGQr4M61XhfoxF759cB+64WPgteVj9Ma7mP/qOra4yklgQM7RslVBLifooOBkifxCF+TrCdgZPu3S4f5vP2Hxzk3sGjwEto5EvNh4ohR8n5ETZDt0EAYtyB1riXcQiQsUF+i0jbWvFQj9RgoqgemcHQ8f/Y7vf/kBU7eugNe1GwJaIlawo1mDbGcFhGErnSoKm3JAPtkZZYIdO5A/0wPlhGOtQECCdFp3NvDOj/e42euHW7Chu5j2wAg+vZcd2QeZrQzibj0yB5+F9JVaSIdY6mLUYtvwQWwbqksW0AypAxMX7rw4hJ8fPsCHdz/Gre++wKaeUqS7K8APmJBZvxfSZ/ZA1KQCv08Hfj9By5qIwE/dunRrBU/1l2PXy4e5mftmXwPjs3DPp+ZH8ERPMSeQ1hdDWrsXGc1qCNwGCGjj2eVLRBgyQ+g2PrZEbsOjtD4Vet55FXNfXoPYZ8YG526cnH8DM58ucR9upZklCdhAH8FKEhCGSeBNEGS7D0jYe5AxUIX0kAmbPGrww3T2aSYbXWpsdmu453S6J9KDJZxARAKhi8KoC2F/Mhl0hOmixgWG04YnpT6rXxSwTGa4TeMCtylCY0TcXParhC6WuFEFsU0FScM+ZJmLaB+KuT0QN9G7dZC0aOj/6rggVW3XFHyyQ78T27UFyNEWEjSad4J5rjQqYMXrIDlGgsZ/IMiqL/5c9rwKWYdKVpEeLuW6+Tskx1mB6nYsJnUxtrK7TJcekjZtHLsWTCtLeUoyHXowNvXXsZjUld2kqxEf1ZwRNahPShJI/P34Mwv7jaxRZ43F/KeLx/sLFL3BLApzcXgAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Write, Path, Sheet, Cell, Data):
                Messge = "False"
                try:
                    # 判断输入地址和数据是否为空
                    if not Path:
                        Message.message2(self, "The input Path is empty")
                        Messge = None
                    elif not Data:
                        Message.message2(self, "Data on the input side is null")
                        Messge = None
                    else:
                        if Write:
                            # 将单元格字符转换为数字的行和列(A1转换为1,1)
                            Cell_E = re.findall(r"[a-zA-Z]+", Cell)[0]
                            Cell_N = re.findall(r"\d+", Cell)[0]
                            row = int(Cell_E, base=26) - int(len(str(Cell_E)) * "9", base=26)
                            # 判断文件路径是否存在(存在创建)
                            if not File.Exists(Path):
                                file_stream = FileStream(Path, FileMode.CreateNew, FileAccess.ReadWrite)
                                new_excel = XsModel.XSSFWorkbook()
                                new_sheet = new_excel.CreateSheet(Sheet)
                                # 遍历数据写入
                                for index_Data in range(0, len(Data)):
                                    List_Data = Data[index_Data].split(",")
                                    new_row = new_sheet.CreateRow(int(Cell_N) + index_Data - 1)
                                    for _ in range(0, len(List_Data)):
                                        new_cell = new_row.CreateCell(row + _ - 1)
                                        new_cell.SetCellValue(List_Data[_])
                                new_excel.Write(file_stream)
                                new_excel.Close()
                            else:
                                # 有这个文件则追加
                                file_stream = FileStream(Path, FileMode.OpenOrCreate, FileAccess.ReadWrite)
                                xs_excel = XsModel.XSSFWorkbook(file_stream)
                                xs_sheet = xs_excel.GetSheet(Sheet) or xs_excel.CreateSheet(Sheet)
                                for index_Data in range(0, len(Data)):
                                    List_Data = Data[index_Data].split(",")
                                    new_row = xs_sheet.GetRow(int(Cell_N) + index_Data - 1) or xs_sheet.CreateRow(int(Cell_N) + index_Data - 1)
                                    for _ in range(0, len(List_Data)):
                                        new_cell = new_row.GetCell(row + _ - 1) or new_row.CreateCell(row + _ - 1)
                                        new_cell.SetCellValue(List_Data[_])
                                ne_file = File.Create(Path)
                                xs_excel.Write(ne_file)
                                xs_excel.Close()
                                ne_file.Close()
                            file_stream.Close()
                            Messge = "True"
                except Exception as e:
                    Messge = e
                    Message.message1(self, str(e))
                finally:
                    pass
                return Messge


        # 重命名文件夹
        class RenameFolder(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RenameFolder", "V25", """Rename folder""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3b98f050-267f-4345-89ef-81e020c02b60")

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
                self.SetUpParam(p, "Path", "P", "The folder path that needs to be renamed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "NewName", "N", "New folder name (without path)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Operate", "O", "Enter True to perform the action")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "NewPath", "N", "Preview the new folder path")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPUSURBVEhL7ZVPbBR1FMdnZuf/7vxmd6HlTytVoNSircAuVdLSzbbSVtJGikCrQHdndzu1LZW2KbO73S7TWjCgcjBE9FDDQbgZNXowGBMvJsSLqRdjvGjUqyWKJtJEnu/361qz2ZK4Em++5JOZN+/Pd96bXzLc//aPzDdpr/flh5p9aatllZzVQqbtcCHl3xs5kwiTdOKmMZ26bjjWtVXS1jWSS72Dzz/C67OF9PLNSCfe9DlWsuCWGJlONlEhkk19QKZTnV4n3uCfSjYWkUXc4cbg2HFSKPvbDCd+xUgnewruPc3MDkZJbvCqkUkUT/oXuAGSSXxqZmKhQsmKYfB13HlvwV014k4EiZsMkolk0MwMBzjblrhIROTcmLomsZiKqx4znMR1WmNkRtdxdrdeIrDJtnXiWJ8ZucEljJWStn66J05iCWuXV/zkLTIz9EOJgOlYR8xzp4BMD5ZPNgUkkyz4KfCfH4MSAXyLd83ZYcBx7w8UoRMXCfhcez2eqttUfc2iMjDnRgB7LRQJ4IM4DaxVUC5mfgh82fj+YgHHumG6978e2hw/9tec6wpMgEzFugJp28Rz/Dv7UGsUlYP54igVyNOX5oyp+Bvk4ng4cDnb7395kp0Cc8YGc3YE6DTsHqHChTdb8XN4Uuj92efZiWGN6T3Nnxv5tQa+9TMBkh96VX2qxREbdyxq3a0s0TvQA0rrHlDam0B/7iB4rUNgjPaDfrSDNaFxX+owitigPR1lMXpqtN42MEb6QGlr+h5bn0XaOfPixKz0WO0nns0VQFEPPAHyvkYQNgRA7dgHyv49INZuAf1YB7v6XzrNrnLTo2DOnwIhSFieMX4SeK8K+jNPAufx/IjNLyPdnHnhhXk5vHNRaQ2x5lKongko0b0QuDQF2qEo8JoCKk4j7X6YrUmoDDIROo2nqhKknVtB64kAr8qg93UBr8ifY/MVMy+Mz+tHDzB1PmCAN9ELSiSMvgby4w1MQKjwg7itmgn7ho+BWPcgNt0GxunjIGJzT/UGELc/wHLUrmba/AvkS6Sdq3zL3apEQl9h0bL4UNVdY3LgZzlcvyzvfWSJzI1+p3Y2/ybtqrvjqaq4K4fq7+DOb4s7algzva/zFxqTGrb/IdbVgNRQe0sw9Dg2/hjZiAgIszO8oS1wsnhVIL4ZTlVew7Usils253GSV3hdpf45XhLf5zV1AfNvIDd5XbvESdKHwjr/CbF6Y4QThPfwOf05fYPMIK0IsyjShexGjiA0cAVxkYNIG7IJ6UcshP5YapETyEnERKgNILsQWvc2chj5L43j/gQ5ckr4LPrThAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Path, NewName, Operate):
                try:
                    NewPath = gd[object]()
                    # 判断输入端
                    re_mes = Message.RE_MES([Path, NewName], ['P end', 'N end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        NewPath = Path.replace(os.path.split(Path)[1], NewName)  # 替换路径

                        if not (os.path.isdir(Path)) and not (os.path.isdir(NewPath)):
                            if Operate:
                                os.makedirs(NewPath)  # 文件夹不存在创建新文件夹
                        elif os.path.isdir(NewPath):
                            Message.message2(self, "The changed file name already exists！")
                        else:
                            if Operate:
                                os.rename(Path, NewPath)  # 文件夹重命名
                    return NewPath

                finally:
                    self.Message = 'Rename folder'


        # 移动或复制文件到指定位置
        class MoveFiles(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Move \ copy files", "V21", """Move or copy a file to a specified location""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("0f572482-3528-4116-9f87-0505d15e86a3")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "FilePath", "FP", "File path to be moved or copied (with file extension)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "TargetPath", "TP", "The destination folder to copy or move to")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "Enter 1 to copy the file，Enter 2 Move files (default copy)")
                NORMALNUM = "1"
                p.SetPersistentData(gk.Types.GH_String(NORMALNUM))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Operate", "O", "Enter True to perform the action")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "TargetFile", "TF", "Preview the path of the file after moving or copying it")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALdSURBVEhLrVU9aBRBFN6oiPFuZjYRDIqKiGBjpyhWJ1YKIrFIITnJzezmkpjkzOXYv9NkjTEakkgMASvFVghY2BnQUgUrwRQ2NooIWiiIihbre3MPks2tuhfzwcftzr73vXlv3rwz1gu8bLXuKpeb6XX9wXx5lDmF2/S6vmir5DPctY6I0d6IufIULa8dmUp+u6gWi7xqLXDfesU99Z676pMY6Ym4r962hp2cTBtGE692B7xqfxRj/ZG40heJy8WIX+qOYC2CQJEYuwBZqPtGGG4gn3RoHezkrGovivGBmiCI8cCqPSMDCOBCAAgKv8+NMLeJXFOgo2Mj8+QTLe6DCNRahCDkqV/clR+AWKLvlMkP5qgD5JkO3JOjWhzKgXVmgf2IBVYe6r9/m6PYjrC4NevIHNpkXemSWzo0O2onCH0TV/uxDO+Y332GPsUgfPsQZPTMiKImWkoHaL/AnBrG1JdaSuf30HIdhN/Xgt1Fr+kBu1riI72ftwwXdtNSDFmnq52HfVPQOTfgDoxDGaeZW+iiz39HJrDadHeU8ydpKQbhy33QtpG4NqDbUxPOAZsgU1EHySwRTZmJUlvWUe2wswdi9qKJwVYTd433QbfsCmKHMV8lnpUGGN0xJ4ciaM0XkPZL3BHuNE5bC+ld44VD4k3GADgyfHma5OohvIINDvPQnjehx28xR84nEcRmtQ3S0bZPMUhiAO6ow3y05y4Y3QPHOXCYrgVQM/CLz3+mr2Ygm0lsVSjNY3NisD6A8Kzj5kQpnnIDxJLC5h7Cxs7p8taVCIYTfHyth9eqQ0tFnEue+grlPQHPP7FBSHkZmC5mUOeckujLPKXgfBaZZ+VJdhlQv2M6AxhoSQL/ogjhcD21AJ03BJQkuwIwYuHDm7WXycYAX4Qnz5qBzJFqHGA4999lcmXJCDs2k2QceuzixUpwTsNameQiySUAIuMfiHmdWrZR0iwSXtdewzCM358jLeGKQxPyAAAAAElFTkSuQmCC"
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

            def RunScript(self, filepath, targetpath, Type, operate):
                try:
                    new_targetpath = gd[object]()
                    # 输入端判断操作
                    re_mes = Message.RE_MES([filepath, targetpath], ['F end', 'P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        filename = os.path.split(filepath)[1]  # 得到文件名
                        new_targetpath = os.path.join(targetpath, filename)  # 得到带文件名的目标路径
                        if not (os.path.exists(filepath)):  # 判断文件是否存在
                            Message.message2(self, "File does not exist!")
                        else:
                            if '.' in filename:  # 判断操作
                                if operate:
                                    if not (os.path.isdir(targetpath)):  # 判断目标文件夹是否存在
                                        os.makedirs(targetpath)  # 创建文件夹
                                        if Type == '1':  # 1为复制，2为移动
                                            shutil.copy(filepath, new_targetpath)
                                        elif Type == '2':
                                            shutil.move(filepath, new_targetpath)
                                    else:
                                        if Type == '1':
                                            shutil.copy(filepath, new_targetpath)
                                        elif Type == '2':
                                            shutil.move(filepath, new_targetpath)
                            else:
                                Message.message2(self, "File input error！")
                    return new_targetpath
                finally:
                    if Type == '1':
                        self.Message = 'Copy'
                    elif Type == '2':
                        self.Message = 'Move'


        # 获取文件夹内的文件名称
        class GetFiles(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GetFiles", "V22", """Gets the file name inside the folder""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8c46bb9b-1c55-4f5d-9ef2-d878551a19b8")

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
                self.SetUpParam(p, "Path", "P", "The name of the folder where you want to get the file")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Filter", "F", "Wildcard (default *)")
                NORMAL_STR_1 = "*"
                p.SetPersistentData(gk.Types.GH_String(NORMAL_STR_1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "1: TopFiles, 2: SubFiles（Default is 1）")
                NORMAL_STR_2 = "1"
                p.SetPersistentData(gk.Types.GH_String(NORMAL_STR_2))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "FullPath", "FP", "Full path name of the file")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "SubPath", "SP", "filename")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO0SURBVEhLrZVdaBRXFMfPJq6bzWbuTBIszKqE4oP0TU3qgxaNHw+C4oMfqElaMjO7Y/2IzdfOzCbBFaT4EX0QhXbFQkFtqSLaKJQUAtr6EKVKFR8KEaW0JtQkNkQSBSXT/xln4wZiomv/8GPnnL13/nPOvXOHsiUcY4toMQ8J22gXtjY1LTEQT1Jq80x/+tTiScqBL1zlUIOrHKyfHh775R5XShqdVLcm5N9mcslOVbGw9ZciaQyIRO0WKaGvfwsSojXumUn2NCbhlu2zUa4rWdpNPzWtZFtfiJY+EpberbQ3Tm0STuhRkYxhkH7LT00ruVlbjQfqKbZNGUZXlSPNb25XTgZOnA3+9oKmmgja+6tyFCaTVZKTgW1USrY25IeesLMu8OJLyVjnnIaGsJ/OzaAkVS0kS38o2uLX8JuG2XFUdEZO7fB2F3blBUql8rzBuRiwlCa9TG4zv8aTX8QNL8LgnGTXnsKajMBwWDXNQm+gZ8C7yDHeyeBNEo7+l+ToQxMNuIJk7DcvQRTwmUyT5TO5AJnlQWFpj9CNf8cNSq+fihasWermRT/43UsQHQN7X11SKfgZzPMiIg1cA5lF3A9Ogo9AN7gXkCNjBRtW9amu6xvc+i4aWlb+ApfPgAA/AJ7EWgZcsNmLiBoBx0u8iKgHXAEfgxEKBA7iXgMRY0O/2tGRZbBy8SjNyOeJ28BX4AT/B2VueNiLiHYBjm3AVfH1WVAB/qEl86XiY84fotUcUtetyzJYsfg5DMYQfg/OAG4Ti6u5C7hNLDYYAZcAt2cQnAbloB8VpEOfLBiW6mseq+l0lkFlxRiFZtxDyBP/BDyZF+8O2ArYpAjUgV8AG94H34BzYBEYALfzy9QXRXXb+ia2qLLCpfDMLsrL24kUl50A3ILHYB/oA9z3HeA8OABuAB5/Gbxq0eySOXibe3Auvd6mnsHycpdCwW4qLFSRGgUWqAJPwW3Ax0IT+Bz8BLgl/L8BOgEbDFIwWB2pWdtbtLtqUE2nsteAKwhxO1g/Am4Rl/8tJyB+Yn5SXvQuTvjaA3gXLQRc7QAF892C9ZW949s0nNoVlRpq3EJzU8ZABrPAXKBwAuL+lwF+L6Kc8MVjOeYT9EMqleZHYhv7i+o/faKm/Aq8NxlfJ6k1njF4L8mt8b6JRwV/0djA0v6fs8jSenGvp+MGJXXVAt/kURx4w/ijXnY0U1i1298Vb16z5og28yVO0wfjxzVLtgxL3r/bVdqbXOVwY+5gPn8TYPAZEdF/8nerSfSj9/gAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Match_filter(self, String, Filter):  # 通配符匹配方法
                if Filter == '*' or Filter == '.':
                    return True
                elif '.' in Filter:
                    ft = Filter.split('.')
                    st = String.split('.')
                    if ft[0] == '*':
                        return st[-1] in ft[-1]
                    elif ft[-1] == '*':
                        return st[0] in ft[0]
                else:
                    Message.message2(self, "Filter input error！")

            def RunScript(self, Path, Filter, Type):
                try:
                    FullPath, SubPath = [], []
                    NFullPath, NSubPath = [], []

                    # 判断输入端
                    re_mes = Message.RE_MES([Path], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if not (os.path.exists(Path)):  # 判断路径是否存在
                            Message.message2(self, "Folder path error！")
                        else:
                            for root, subdirs, files in os.walk(Path, topdown=False):  # 遍历文件夹内的文件
                                if Type == '1' and root == Path:
                                    if len(files) == 0:
                                        FullPath, SubPath = [], []
                                    else:
                                        for f in files:
                                            FullPath.append(os.path.join(Path, f))
                                            SubPath.append(f)
                                elif Type == '2':
                                    for f in files:
                                        FullPath.append(os.path.join(root, f))
                                        SubPath.append(f)

                            if len(FullPath) != 0:
                                for i in range(len(FullPath)):
                                    if self.Match_filter(SubPath[i], Filter):
                                        NFullPath.append(FullPath[i])
                                        NSubPath.append(SubPath[i])

                    return NFullPath, NSubPath
                finally:
                    if Type == '1':
                        self.Message = 'TopFiles'
                    elif Type == '2':
                        self.Message = 'SubFiles'


        # 重命名文件
        class RenameFile(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RenameFile", "V24", """Rename file""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e14af72f-d92d-45b7-8734-7c7c3e3ad76d")

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
                self.SetUpParam(p, "Path", "P", "The file path that needs to be renamed (with file name and extension)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "NewName", "N", "The file path that needs to be renamed (with file name and extension)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Operate", "O", "Enter True to perform the action")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "NewPath", "N", "Preview the new file path and name")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQnSURBVEhLpZR/bFNVFMdv33t9r7/efa/t1q2s6GAuDgebExhjsBaFyZYganR0WQ1rX9dCh+sE1r62G1QT3UQkgEYSo5FECUH/8Ef8x7lEXfwRJRH5Q+OPKKLADA7mzymGueu5b+8PTLquzpN88u497577vefck4uuNZxW2nEmug+r4f1YDeUn0wVE0ijbxuvh+Q2CDshDvUTet5PIjz4wN3TtI3EipruGUU+LoG+T26RUhx0nlas4HR7HydAWMaFsLoAE7o9oYmJKeRP19MwuYs5sK4N0iZgMndRdc5qkKnU4Fb4AB/tQ3r9rRqSz06T//reZE8oCnO4ioqp8rLvmNKkvtAE2/8quRiXIfFR+vA/iwyM5ReYlkIpsgIzP03HJ7vusIPK+JpLOITIvATW8TlRDP+tTzUDkVXr58B1xZ6MW3T0/AUc2gKEkZ3F/9B3I5AnahdAgR6VsjMiDcQLjV1A2y2iL5yNAzZoOl+CByEEoy3G4j5dB6CVRDT4Llz8J2f3qjupZ5BKgdRUHtlXOEMyJI9nloS0upWJ2PUwzyOYcLV9eAThRu7R3+zhWFSA0O0nlEh6IXrSpilcLzPo48F+AvX7KK0CfAEsm4i6Ivs5SuvFMXKEC87VCBWzZaJG8J+azpUM+WyIP6YhP7o96HT0BrAUWKoATQT/Oxs7TxXMyED1nSwSbtMD/VCL6FNNHjL6WswL/r32ycwl4pqfN0kM7iNgfOaU5/o+BAHTfGH6we0L3IBeyWZKm1rXE2t3+HnI4aC3DQIK7qWKHcckixRq712+srw4L3jqFqbguYmppDMhD8Q6mcmFQaFoetg/2+lmP+y6IgW7KMua7b/tOWF//J+K4nVTAa+CNV7jyBX8bJOtJcK4E34/IyA3z61edYReVEdMdvl/4VUsnhTU3T7IVHsKvqJ6SHr7/C6bESQTv8t+kwfjnbKlzCuJCdEODbPuWLS26Cnsdo/O1jMv5qS3mv4J44xmYNwNv0R+6jQDPA3uBuD5+G1gM/AUEAGpjwNN0wBTLY5b2lst0TG014thLrKdkmvEUf4CMxhrwnQXoJj7gGeAj4DVgO/Ak8AnwHEAP1AbUAu8CJ+jFMqXOryGDKcSyh8CHGg3Y9j1b5iKm1jVvwNwDnAbuBOh9HAH2AOPAFmAIOAiMAocBWvso8BjwIuL5KsZl/4xfWf0H6y7eCD50K+OUT9FackvKL1ruaT5kMHJfWjta/WK3P2iQxNN8U90Rg9l0mata/AJTbB/la288wTcsG2aud7/OVZUfY4rkEYNZmIBKTPANtce5Gxb+LjSv/sFaU+OiAvSROmra5OszLqskYm+A0IuFRQS6gQhNtxBx91Zi2thILG23E8G3gti6/cTxVIaYN3mJefM6wtcvJeKurdqYdiPfUEOQwfANQmj0H0Dl6KumU8bpAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Path, NewName, Operate):
                try:
                    NewPath = gd[object]()
                    # 判断输入端
                    re_mes = Message.RE_MES([Path, NewName], ['P end', 'N end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        NewPath = Path.replace(os.path.split(Path)[1], NewName)  # 获取新文件的全路径
                        if not (os.path.exists(Path)):  # 判断路径是否存在
                            Message.message2(self, "File does not exist！")
                        elif os.path.isdir(NewPath):  # 判断文件是否存在
                            Message.message2(self, "The modified file already exists！")
                        else:
                            if Operate:
                                os.rename(Path, NewPath)  # 文件重命名
                    return NewPath

                finally:
                    self.Message = 'Rename file'


        # 获取文件夹内的子目录
        class GetFolders(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GetFolders", "V23", """Gets the folder subdirectory""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a68117c1-e7a4-47db-b6f2-5e905cc72147")

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
                self.SetUpParam(p, "Path", "P", "Gets the folder path of the subdirectory")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "1: TopFolder, 2: SubFolder（Default is 1）")
                NORMAL_STR = "1"
                p.SetPersistentData(gk.Types.GH_String(NORMAL_STR))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "FullPath", "FP", "Full path of the subdirectory path")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "SubPath", "SP", "Part of the subdirectory path")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUFSURBVEhLnVVrbBRVFJ7Z987OzJ1CtTYURMACIRAeImqF8mgiVCNi26Sl6u7M7G6f0JayMztdYKG8CqFRMRgq/NFg/GFioijRRBOjiZpooonRSojRkBCiSHzEaDSxx+/eGUCMiZSTfLv3nnvP6zv33pG4TCm365prHdeL9lOaax7XHGvsCqA7ibV9UrklJjbfjEwtWJrmmOd01zqjDZorVM+sFyiY9UbJWqUXrSMI/FailJkemExe1G1tlQjwqerY8wPVdcLczFpU8qZUTicC1eRFdTMbdcd6JZhKqmM6eil7AtUdBfaCsm+QxGndyz6tu+boTdGmO+YHhpNZyMdw+C6yzrCimdeK9lYgjfUuUNaNgKf0olkSRpMRcP22VrQe5mNke1IrZBp1J7NZ9+zDvNlYP4Aqyyknu0AvWGdqBpqTwvCGpKUlDOM3Up5dxadqwXJFtgVrLiuk16meXacWMivV7XYdX8fe08xNz+TjGxJQMQvcfg70CCpKuZeZY+WUoVy17tq7QNFRVAX+rSdRTR/2XeL9QSXdqLJXwLO26MVsm1TOK4Hb64UV7RaeNXesD2W/YI7ZXIHjCWdf8j5gbjPPtHkSDP3B3s6rzjlcy0Xwy4ZrrQpcotQBewoMRuHgOa1ojrCdHSPGoYGDbLj74xk/vV9hlLsWaU5GnC59uKek7+3doe/D/878Dr3c6Y+hMw727aqZOJ+E3THVy9UL51yQlYlFYnu6yRjpJ20wTUr7gxSrW3xeSkRbU92tJ7Ri9lnJMBbG1t7dH6u/a3ts9fJBpf2hQqKpQYyFvmFFX3gqW600NbymWE1LAve8WXYH291NbFcnJRruIUmWSYqGKVRpkGxopGxupIrD/byx54BfgUvA5fCCWe+Fqqd+hvEPgf432P4pJ+KE8WzAF843ryDZ1MAXKLqoltBgYsM9pG174jtt4PHd/k7pd+AF4DZgGhAFVKAaeBU4r7Ru8BR70yjGMuAL8xDgwFYK11SRnFKEY2O4551bTu2vq6ULlWJTlZTC7x9SNPqMmP9bZOlF/H5f/cmYUiYK+cpAWKkjx3Z0gJYIRRfPI3ZkkG/mb87W+MolHyZb13+FC3dOVhITUiT8o6SnxiVVOZvYuPYsaD3L9nSNR+bM+AXrf+F4j6P6cdD+urI9zSu9EiBPciJGkdk1F9dPTMSVloZjkdrbRT+iC+YQ292F9bioMvHAfRRfs5xSHS3Q42Ds34I9s0nWksT9sHKnODA4kSv8AF42x/ZtofD0Kt6Dj7C4jhuxPT0UYhpF5t0heiKFQxS/dzFVjBbI2NsLZx2EjEXw6PxZJKtJwj0gHHP+f7HCzTM/gGhyPyUa7/ebvHT+BW7EEdJVisydGQQIg8K5hI8QaX3thOb7DnkAJCGnEv4cPcQzMiaccxEBUIE+lPtWikU4/yTDcXjarX7AhXeKAOCYpBCOsIJjCDrDc6aTzikBHVEkIUOPm+1TVLDWCOdcRIBD/aR7ucOVz5dr1eyjE3Hch/iqpZTctI603jaRdSqzUVxApW2DQMp8ROjxfSA13yzWeQ/411HK5/kR9oW/9/yYsmJ6GX+SxTigiJW7eGVXub0OcMb1oIMYvzdc5zd3JHDtC5wWgJ+rBh9L4Th+fdVwsuDVDGWRaHZZ4NoXfBqb8eYP8wWehdj4Xw7+B9wWCfKn49ot/qdorv0SXtFr9EwS3BbJeYE7iCT9DWTObD5nKeXgAAAAAElFTkSuQmCC"
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

            def RunScript(self, Path, Type):
                try:
                    FullPath, SubPath = [], []
                    # 判断输入端
                    re_mes = Message.RE_MES([Path], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        for root, dirs, files in os.walk(Path, topdown=True):
                            if Path != root:
                                if Type == '1':
                                    if '\\' not in root.split(Path)[1][1:]:
                                        FullPath.append(root)
                                        SubPath.append(root.split(Path)[1])
                                elif Type == '2':
                                    FullPath.append(root)
                                    SubPath.append(root.split(Path)[1])
                    return FullPath, SubPath
                finally:
                    if Type == '1':
                        self.Message = 'TopFolder'
                    elif Type == '2':
                        self.Message = 'SubFolder'


        # 新建文件夹
        class CreateNewFile(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CreateNewFile", "V15", """New folder""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1aaaf024-74fd-4b75-8264-c3cce16ecd7c")

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
                self.SetUpParam(p, "Path", "P", "Full path name of the folder to be created")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Operate", "O", "Enter True to perform the action")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJBSURBVEhL7VS/axRBFF78Gc3OzCVRREUEf6SxtbKIhZ2FqHBaRMnO7N7m7vSI5tjZ3Vvv5sxhYfwL9B8QGwsbS7GwFCwUFBQsgqawkFiJxfje3GhycHDrprDJBx/D7s5839v33jxnC/8fe2/NHqRZpUMSv0disWTYqvRI5vMTjcZuu604aCzul5YXNbtbH2DpXkNTKZ6SyDs5ksn1aQjyuKPUNiu7Diq9lHXrGowGmfiadaqatoIcrGjWntdEijfuYrjPSvfBInEOP9LECkthNrOsoknMP8OhTyMZi4+40nZ1BfWsdB+lpjgKoj9pCpGAQd/Mf0ekd2YqEoSphRJTc6O5gCvsTWoT+1XdRTrl8nbHUWd3YATsTqiNSRqsQU6n3FRcpO3wLZitQAC5SCSHlX8BrtIkWGVZ+N78Bbx4xlRVM1XTJBJPHDU3ZmoAz5hfKGAhYrMYA2zNvx0U8dCNxYwR31j0fyUGFvFvxoDF/BIKYv7HZXAKittFs6EHcxI7EFL2whiQJJjGdoPCrh1oXhuHlL1kHSj2kIN5iQG6ki8bA0eVd0HU3+HDq0k1S8H5x5+uKkpTU+ld7hsAoA6vacwf0Eic3mz0NPXxPv1iCT9m5dGAP0JHWJubzj+2vOQfBkYHScQFM1ckf25GxJCDecm60O4xf2ylLR6GO/dE4pCpBbbYkIN5yXo34T7x21Z5HSb/4G5oLl4BLt3AUfN1sjV/2MpuAI6NxD9PM/8q5PBKEbJOrTyReUes4hZGwXF+AytOXFuxd/PPAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def RunScript(self, Path, Operate):
                try:
                    # 判断输入端
                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)
                    re_mes = Message.RE_MES([Abool_factor], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Path:
                            if not (os.path.isdir(Path)):  # 判断路径是否存在
                                if Operate:
                                    os.makedirs(Path)  # 创建文件夹
                            else:
                                Message.message2(self, "Folder already exists！")
                finally:
                    self.Message = 'New folder'


        # 删除占位电池
        class Delete_PlaceholderComponent(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Delete_PlaceholderComponent", "V13", """Remove the placeholder battery，the deletion is irrevocable""", "Scavenger", "L-Others")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("05059936-db83-47b2-b7f5-8189edc0c9c4")

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
                self.SetUpParam(p, "Delete", "Del", "Bool value,Removes the placeholder battery when True")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI2SURBVEhLY6Ab4ODgkIcyaQMYGRk3AfF2KJcmQAJowT0g3gjl0wQIAi24T2tLQOAUIwPDciibOkC9s5SXIS88jSHDL5shxqWJgZPlP1B4HW9NaiFDVmAhQ5wrcTjRo5AhPzxTpr5QCGIyFHDmRzWZL+j6n755yf/0bcv+py6c+l9NU/M/g5bi/+zdq/9nbV32P33TYsJ48+L/dov7/3MURE2FGg0Fab6zmg9v/Y8M3r59+19HTf1/XFgEVIQ4MPX0wf8Mqb7roSZDQZTrsup9G6BKEABkiZyc3H9fX1+oCGHQc2z3f4Z0vxVQkxl4WBgYMhisdZ5W79sIVYIKYJb4+PhARfCDnuNAC1xNXgDNdgNZ0ARMMe8Y/K2XY/MBDJDiE7AF3laglHgIZIE+kHGcwct8Ez4LQIBYS8AWBDuASoWXIAsYmBkYghmsdJ7hCiJkQExwgS1wMnzNxMBQBrYADBK85hHyAQwQ8gk4kiNd9gFNZYcYDgKpvtObDqEmU3zg77cf//XUNf6HBQVDRRBgCiiZpvujlgQs2SHzozcv/L/j7jWi8L4nd/4vO3fsP4Mw//+w0ND/229c/L/j/nWwXPrOlf9Zs0M2QY2GAJHqNDu2yqT9DLlhxxhywo4Sg1krk47y5UcfBWp/xKAo+Z+hLPYgsJg4zFqZeFCkJt0LYjI1gCSPCJC8CMTwzEULIADEd4FF/QYIlzaALvUJyJIHQLwTyEZKptQFwkAL5gJpQQiXZoCBAQDe1PdZRMVw5gAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Delete):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    if Delete:
                        doc = self.OnPingDocument()
                        if (doc != None):
                            objs = doc.Objects
                            deleteComs = [obj for obj in objs if (str(type(obj)) == "<type 'GH_PlaceholderComponent'>")]
                            if (deleteComs != None):
                                func = lambda d: doc.RemoveObjects(deleteComs, False)
                                doc.ScheduleSolution(20, func)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'Remove the placeholder battery'


    else:
        pass
except:
    pass

import System
