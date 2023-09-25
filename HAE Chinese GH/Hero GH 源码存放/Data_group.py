# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Data_group
# @Time : 2022/9/17 17:06

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc
import ghpythonlib.treehelpers as th
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import rhinoscriptsyntax as rs
from Grasshopper.Kernel.Types import GH_GeometryGroup
from Grasshopper.Kernel import GH_Convert
from itertools import chain
import re
import initialization
from operator import *

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:

        # 列表取值
        class list_values(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_list_values", "D1",
                                                                   """The value of the list is based on the subscript，value subscript interval""",
                                                                   "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("969903d7-b159-4520-be02-36ef0cad97bf")

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
                self.SetUpParam(p, "List", "L", "List input")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "Value subscript")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "Get a list of values")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJLSURBVEhLYxgFFIOkDEf1smzd+LxkDTguy9aKz0y1coMqIQ38//9f4N+/f+xQLkNeslrhxAL2/+3pzHA8MY/5f0mixEmgYkZfX1/X/v5+d6A+ZqgW3GDv3r3aBgYGbysrK3dDhRjyk1UyOzKY/9cnMMBxRxrD/4okwU2Vcz+JcnJw/I+JifkPdJQ+VAtucPv2bZWGhoZ/y5Yt2wkVwmtByZQvEkAl/wMCAkAWmEF04AFPnz6VMzU1/VNbW0ucD2Z/FmdkYPgXGBgIssAEqgU3uHr1qqqYmNj/7Ozs41Ah6loACiJpaen/eXl5R6FCBC0AKvkXFhYGskAVogMPuHfvnrqMjMz/3Nzcy1AhoiywtLT8X15eXuHq6hq6atUqY4hOLACY1JgmT568+OjRo8VQIYbmMq34ifnM/zvSgQZD8cRchv/N2YJrgepZ9PT0/khISPxXUFD4r6am9n/RokXnoFoxgCUQJ3FwcIQB6UggTgVhXWW2JaFWwJRiisBhlgz/7fQYrrCzs6cDwaXMzMynqampT7Oysp6WlZXNBurDCkCGzkPHAnK6x5SdU/8r2MXBsZJTyn9JA89nUDXdQNyJhOOAmHiQselLbNaWH/+Tlj+D48xN3/4nLH28HaqEMhAy8Xhm0vKn/6NnX4XjxKWP/4dNPbMHqoQyMGoBQUB7CyYdz0pe+eJ/zNwbcAxKSeHTzu6DKqEMhEw4mpW47PH/qFmX4ThhycP/YZNP7YUqoQx4t28RDJl4Qsuvew8cg/hezVvkoUoGEjAwAACkarXImiYxrAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Lists, Index):
                try:
                    List = gd[object]()
                    re_mes = Message.RE_MES([Lists, Index], ['Lists', 'Index'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        index_list = Index.split(" ")
                        List = []
                        for i in index_list:
                            List.append(Lists[int(i)])
                    return List
                finally:
                    self.Message = 'Multiple subscript values'


        # 列表多下标取值
        class Subscript_Value(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Subscript_Value", "D5",
                                                                   """multiple subscript values, can obtain six groups of data at maximum""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8eb91efc-115a-4abe-a586-048a30d39705")

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
                self.SetUpParam(p, "List", "L", "The original data list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "I", "The subscript to be valued")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "First set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "Second set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "Third set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "Fourth set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "Fifth set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "Sixth set of data")
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
                        self.marshal.SetOutput(result[5], DA, 5, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJ+SURBVEhLYxgFVAE+9TO5/Ern8Fqh4fr6eiaoEspASZL0rsY0npdViVxgXJPE87I8UfhFeLy/wv///xn//fvHDVVKHqhI5L/YncHwvyUZgttSGP7XJ7H/X7m5V1pKSnq2s7Pz84cPH/pDleMGQJfwATEn0FUSQCwIFQZaIHi6LRVoaAIENyYy/K9O4Phz4tZaGT4+wUPq6ur/b968WQJVjh0ADWTz8fG54OLi8kRLS+u/m5vbq5MnT7qD5HBZsP/iYhkBAeFdIPW3b9/OBRuECwAt4JCRkXmnr6//e+rUqev4+Pj+tzY3rwPJlScKUMcCeXn5D7GxsZeAwSQpJyf3v6KiYgNIjpAFOjo6/3/+/JkMNggXAIW9goLC/9DQ0EdAtjbIgqqqql0gOXwW8PAK7JaSkvrf09Mzw9HR0WvSpElmYAPRAdAHLF1dXVM3b95cC2QzTpw4ceHFixcTQHLN2cLHJ+Qy/O9Mh2Bwikrn+ANylKOT6wagz/8rKSn919TU/N/Z2fkSFJ9gQ9EBMzOzK5BKBeJ8VlZWkJfTgbjITpfhka8xw39PAwj2MmT472bA8I+DjakemDA2JicnP4+JiXmekJDwPD09fSfIgUB9WAHI0E50rOiY8FwroOK/uk8RGGv4lvxX98r/zyEgNgcoXwvEoCQKw3FATBpIXPb0eMbGL/+TVjwH49TVr/8nLH30b+G/f8JQJZSB8GnnTycsefg/evZVMI6dd/N/5IyL/7w7d6lClVAGRi0gCGhuQcT087czNn7+n7T8GRinrH71P2HJo/8+PTs0oEooAyGTjtdEz7k+J2zKGTCOmHF+TsjEk3N8WzeKQ5UMW8DAAACAOLH5SHqLQQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def handling(self, sub):
                if len(sub) < 6:
                    before_list = sub + ([''] * (6 - len(sub)))
                    after_list = [[_] for _ in before_list]
                    result_list = [re.split(r"[.。!！?？；;，,\s+]", word[0]) for word in after_list]
                    return result_list

            def get_value(self, list_data, index_list):
                return [None if index == '' else list_data[int(index)] for index in index_list]

            def RunScript(self, List, Index):
                D1, D2, D3, D4, D5, D6 = (gd[object]() for _ in range(6))
                if List:
                    index_array = self.handling(Index)
                    origin_data = [self.get_value(List, _) for _ in index_array]
                    output_tuple = tuple(origin_data)
                    D1, D2, D3, D4, D5, D6 = output_tuple
                return D1, D2, D3, D4, D5, D6


        # 列表切割
        class List_Cut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_List_Cut", "D2", """Cuts the list at the specified subscript，output data tree；
                （The last cell is not for reference and has been changed）""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("dd4e55e7-7e2c-4fb0-95ef-adaf2461397d")

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
                self.SetUpParam(p, "List", "L", "list need to be cut")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Cut subscript")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataTree", "DT", "The cut list is data tree")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATRSURBVEhLlZQNUFRVGIaFBKUgwdT4S3SbiRUFTBQMCIap0WCMMZB1VsHAAB3QQYhaoJkoGAVWfkQUkpV1RcFNVEBWkVRIWDZ+lASWAM0JJQJjJARRcZb79t3dW9M4TCzvzDP33Hu/93v3nD3nzplOAPhjAz2iP+qLkx8osveyDDWcSv9LfeOQRqPZxpXpL4ZhTAjbw4cPf5iQkLCBxu/frzl2sy/uHXTv5eEXlkhLDEvCMMVMHeNs+qutrW2dQCBoNDc3h6+vLyjA8W5RtLjzs0VQCs10BL4C9bcb2Xezn0F6enp1UFAQ7Ozs4OXlxTbx7i6KSu8MX4LG7QsIcyi3GKMzRRvgxNn0V19fn4iMVd7e3lNubm5sE48eKc3gpQB16kfsu/c42+xERisPDw84OzuzTTIHao93NG2dD9U2My3KwLno3u/LaBjmC84yO1FTW09PTzg6OrIBkt+vFjb/xK79dgstDQITmsFGDe2wIM6ivwYHB18bHh7e5u7uDj5/BfNkfLz8dtvP7Yey8pGTdVRLduYRlBSfeabRTEZwNv2VkZFxnM/nw9jYGIaGhli8eBFzorSCOSCrwzeF1Vq+yq+C/GoHOzs/zqa/aJuKy8rKhktKSvpLS0v7S04X99cqb42kFlxEakGFlq+PnMeZyy1swLucbXYi4+vEPFpjI2JBU/u9S2JpDRdQieSj5ThRfuMp1cQSAkJIrCc+YJgJa67N9KKGFgSPu2XDbPqGHv96UHYNYtlVLWlFVyC71Do5xjDXRhlGwV4fM0wz7apy8m7mrNOLCiwrKir20598lnbSueDg4NY9++I0foGf4uOgUPgLQrGJroEhu7EzPhWhcSladiVm4MsD+dgXG98VEBDwvVAovBAREfFDeHh4CvU059prA0wlEkksew5cXFzg5uYKhxUOWMEnHAga29vzsWw5D7bW1rC1YbGisRWsLS3x1tKlcKC6lStXgsfjwc/PDxMTE2u59jqNj4+/2dTUtCctLc1FoagMuHipJq7murJKfr66kEVxpbZS8WNzV57iNjLPtyDzXAvEZ1twsrYH1+uVsry8vDVyuXxHTEzMVpVKlUXL7EXM49rPLCq2pnUXX/gNkLZrIGPpAMp62cPN5OwM3ZFrZGR0x8DAYGT16tXDFFZEz5dw9plFxckPhwZaK0/JUFZUiDKpBGePf4cq+WnmxbMnFyIiI5GUlIRIulI56Lv2gpbeU+fWQxQgHKqX53WELoQqwACqLXPR+MkctEe/jUf3e1JpGklU4zoyMiIxMTGBj48Pe2b8OfvMomLHB5cL4ruil6NRaKr9yiq3muBu0noM9dwK5mrmhYWFVdMQOTk5fXRvxz7XS1S8duC6NFEXYKb7hAteRW+iK0bvd+ym92/k5ubKqBRRUVHsrw/TOfXUPwHqaN6/AQ00g444JzCTY+JC6cl8U1NThISETFFtIWHDWfUTGdYMXpOKXg5oj3XC89FB2YKFi8eoDKtWrZqysLDotbe3v1dXVxeqc88g2g2GFLCpv6YgUR2xhP5gI6gE81G/eQ5ady3DxKOB2wezD00mJycjPj4eIpEI2dnZUKvVn3Mt/l9cQNrzP+887En3R6vIHTcTvdCdsgGDRZF4OjJwjN6vI9z/Ax00ZuHfi+JXnno5lNAAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def ListToTree(self, List, index):
                DataTree = gd[object]()
                for i in range(List.BranchCount):
                    list = List.Branch(i)
                    if len(index) == 1:
                        data = list[0:index[0]]
                        data2 = list[index[0]:]
                        DataTree.AddRange(data, GH_Path(i, 0))
                        DataTree.AddRange(data2, GH_Path(i, 1))
                    else:
                        for j in range(len(index)):
                            if j == 0:
                                data = list[0:index[j]]
                                DataTree.AddRange(data, GH_Path(i, j))
                            elif j == len(index) - 1:
                                data = list[index[j - 1]:index[j]]
                                data2 = list[index[j]:]
                                DataTree.AddRange(data, GH_Path(i, j))
                                DataTree.AddRange(data2, GH_Path(i, j + 1))
                            else:
                                data = list[index[j - 1]:index[j]]
                                DataTree.AddRange(data, GH_Path(i, j))
                return DataTree

            def RunScript(self, List, Index):
                try:
                    re_mes = Message.RE_MES([List, Index], ['List', 'Index'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        DataTree = self.ListToTree(List, Index)
                        return DataTree
                finally:
                    self.Message = 'List cutting'


        # 求列表极值
        class ListExtremum(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ListExtremum", "D3", """Find an extreme value in a set of data，{1:Maximum，2:Minimum，3:Mean value，4:summation，5:multiplicative}""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d3639f42-b6fc-4b3a-900b-a28a0c3ecc08")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "List", "L", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Extremum", "E", "Type of extreme value")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Extremum result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJsSURBVEhLYxgFtAKMKrm32FUm/mMH01A2Q+gqZqg8ZcAlrZy/PFn0cl0y96OqRAhuyuB7lJ2qFwxVghuoqanVS0lJXYmNjd3z798/MZBYWloav6io6C4VFZUrs2bNybW3r2epSeT81pHK8L8lGYJ7sxj/F6WoJoANwQdkZGQOA6n/srKy//fu3VsCElNUVMxkZWX9z8LC8r+qqnopSKw6ketdcxLD//oECG5PZ/5fkKoWC5LDCwQEBHaYmpr+l5eX/5+enn4WJMbMzHzExcXlv7S09P+SkrLZIDGyLeDm5t7p6+v7Py4u7ouWltaf9evXpwGFf/f29r4SFBT8X1paPgekjmwLeHl5d9nb2/9ftmzZPB4env/W1tY/dXV1/+/Zs6eXkZHxf1lZxVyQOrIt4ODg2GVpafkfGMF+/Pz8b4FC/wsKCh6eOHHCERQHxcUllFlgaGi4OTEx8T8QCHh5ec0yMjL6f/PmzQYgn8fExOT/7NlzpoDUtWZyv+3LYvjfmQHBk/KZ/1dkEbYgzN3d/UJ8fPw3dnb2LmNj47XAJPpbT09vMScnZy9Q/IeHh8cJoLp2Sw2G7w5aDP/tNCHYWZfhv72NNEEL3IE4CYhjgDgfiNOBOBqIM6F8EDuFjYuvWje88atRXO9/g5hOMDZJnvzfJL6PcBARC+KXPHybuvr1/6TlT8E4Y9OX/1EzL1PHAu+KpYIRMy68i5t/+3/07KtgnLjs8f+QiSdGLYCAoW+BW/1KocgZF/+DU9GyJ2Ccsekz0IJjKVAllAGP3InswROOx4RPPZccMukEGEfNvZrs27tfBapk2AAGBgDdvXUPP3896gAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = {1: 'Max', 2: 'Min', 3: 'Average', 4: 'Sum', 5: 'Multiplication'}

            @staticmethod
            def Max(list_data):
                return max(list_data)

            @staticmethod
            def Min(list_data):
                return min(list_data)

            @staticmethod
            def Average(list_data):
                return sum(list_data) / len(list_data)

            @staticmethod
            def Sum(list_data):
                return sum(list_data)

            @staticmethod
            def Multiplication(list_data):
                multiplier = 1
                for _ in list_data:
                    multiplier = multiplier * _
                return multiplier

            def RunScript(self, List, Extremum):
                try:
                    re_mes = Message.RE_MES([List], ['List'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        instruct = self.factor[Extremum]
                        command = eval('self.{}(List)'.format(instruct))
                        return command
                finally:
                    self.Message = 'list extremum'


        # 列表数据删除
        class Data_Delete(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DeleteListFirstLast", "D4", """Deletes the first value in the list
                Delete the last value of the list
                Deletes the first and last values in the list
                The first value of the list
                The last value of the list
                """, "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("dc9ce766-2175-4eda-9b3a-20ef2ccb870d")

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
                self.SetUpParam(p, "List", "L", "A list of required actions")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_First", "CF", "After deleting the first value in the ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_Last", "CL", "After deleting the last value in the list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_First_Last", "FL", "Deletes the first and last values in the list")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Frist", "F", "Delete the first value")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Last", "L", "Delete the last value")
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
                        self.marshal.SetOutput(result[4], DA, 4, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKdSURBVEhL3ZTLTxNhFMXPtKUtBR+VhxCsPGM0Pha6cGVM/B+MBFyLMQZFwK17lFjb8C+oK4MrWeoCE2KMcUdMCBKRIAYBY+xQTa7nlA4ZaEcQogtv8ktmvpl7zp17v/nwX0bFFuwqbAv2kR2bKHGDoD+Ka4fJjk22Y3CU1JC/ZnCS7M7AH7rfxD8xaCBxsjnCJFLE0cLmCDSoJ1fDsFtAvtfBaPOaSYzgDhAdcPCwD1gddDDdDZzjciUpMSkY+PFiqKPNJlpgX0/BRqrh9oUwfgho4uckB4DnmUrk5tthL+ph/Q5mmKsCSkwCDW7HorZyApanwffjNKmiCfCSjGcpvtQGWyYfU7CbwA/mthBtZ7VrPQINHl/usgfVsG/HaEBWjtAkgdwIxRf5ZUtkgeLpGNweB2PMbSVJUmrgD90LTs86HVg2AXe5gwZsx3Ir7EszbJHC802w+1G414HXLPsMczgm7CEa/HoEGgiZXKNANo6cJ/yZwguNsAzF9YyKZ/luO6kjhU3gj20ZZGLISfgThecPwuY42HQFcqz+Fas/zXdTpIqUROAMfq6u2iW2SG2YaygK13GotbAPB2DT+2HDYbi9wAS3dBtz/8zgUXeXDcdgs6xWwjM1rDoCNx1GbmovDbgB3iVgd53CHJ4yN7hFfrwYjEZtiqKz5H1yrVq1S225F4I7GadBFPY2AuPWzTM3eMjluML2PKuCTbJaCWq3aKDqudoyBLhvQrAnfI9/+yxzArepfg6d+TqWde4UuABc7GeiqusBxopbUbslpZ7TcPQGfzCJnwc6uV72R1N4JjoxPWpJI5GxKhNqgfqsYQpda03PJF72qPBCJuVIEJnr09Vf/xB1rTU90zuB4r8LJeiTxYbhFUNr3vOiOPALgJK/DiPWeX8AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, List):
                try:
                    re_mes = Message.RE_MES([List], ['List'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[list](), gd[list](), gd[list](), gd[list](), gd[list]()
                    else:
                        return List[1:], List[:-1], List[1:-1], List[0], List[-1]
                finally:
                    self.Message = 'The beginning and end of the list are deleted'


        # 树形取值
        class PickingFruit(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickingFruit", "D21", """Take branches of tree data，enter the number of branches""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a3450556-ece6-4485-a9c5-bb07f47901c8")

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
                self.SetUpParam(p, "Index", "I", "Data Tree branches")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R1", "R1", "Obtained data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R2", "R2", "Obtained data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R3", "R3", "Obtained data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R4", "R4", "Obtained data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R5", "R5", "Obtained data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R6", "R6", "Obtained data")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOvSURBVEhLzVVfbFNVGL8JKVn/hUzGut577u1Gt3Ww0rS7be+f3rZjSxgJogtBghAycWs7xp/h4pw69MHMMBNBCSGaKYSta3FrcVDWhAUT8I0YEk0MkWjiG8YHeQINPIyP71wO+iKMzT34S25y7jnf9/vO932/cw73v4D7xos2NlxeCOe0IbGg/0imtdtiUb9KJtTNbOm/Q5hUvvDMJUE8HwNxWgepZID0dQz48UgXM1k6SE6NSjMxIOc0wLH58TjmMQBmAlJOkZnp0iDk1cPSbPwf8q80WPtlGJqPBUAqJ+jcGDNdGvis2vUkACUXswoow02w7tMg1GIWuIHLzJSTb8gWd2mRIqjOKy4kvytcNCDyXhO0Z2rh1U2rwTsWBuFKK1ReSryV7PJUePLKyZqS8SuZ0n4jBb3Ej4dDjGJhkIloJ22wNtJs9kIb9sG2nTxUzcZ/2dX+wpEdL1ff3P4agcTbjeC+YIAHMxantXtkUt3AKBaGK69t8Y4rN73jUVgzY8xv76z+MxW0zm7d4b4jogjqsC9bMaj/4wC4p7D5GIjklFuuiYCdUTwH4JUVrrmkv6psNO6NOkf711ru1p2OlL3YFzfKt/FUC8TebAAXZkt75imbvdvNvBcH3H3//saVP6yaS45GjwfAeKMeOvaK0PLBeqgpPg5gimNSHWEuC0MoKAE8zWEO1TJUyRn7/BV/+D4JdJBp/WFyoB70wQZTaZT87wyy2uvM/ekQ8lobNu06koO7FIeqcuKWd0w+uC9gfThYze12XGnt479tgxqz7o/JpUtxEHLqbSlnVDKafwfJRt+XUKIiOvNYZxlLsCXtgY5uCbriq+Z7/dafqR2e7o9IUX9gXiNoS+8tPq89W6pCXlGkGTSe0kxlqO/4IHqkCXwnQ9DeWwsp1QmHI3ZIBSt2UXsypdaTGaNTKOobubRsMUmeBTKpfEivAzytUHsmAptw12toGfAfywSB0Q2/H/BX/NUdsn/PXBaHJwFoTXnMIo5Kaeurg6YTQRAvJ8H5TevRg17LZ71hO6RlRxVze34gsXmT0hLRLLDZ0PC5DLQn+C7c5356id/vW9k/oDpoAIO5LQ58VhmmTaPHX6Kyow0s6t+Rs5EEXe9psR0f1J2QarEt/W1AheikoI3gJXZUKMRa2bSJnpD9+oDmgEzQ1s2mlg89EXtzRrbPH4o6IBWyZtj08iAtcxYszzVaHvrh+F22tDzYE3GuTodsQxnZmukL2/Z0hxzr2NJTwHGPAP8gi3u8n2FzAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Picking_Fruit(self, tree_list, sub):
                fruit = []
                for leaf in tree_list:
                    if leaf is not None:
                        single_leaf = [list(_) for _ in leaf.Branches]
                        fruit.append(single_leaf[sub])
                    else:
                        fruit.append(None)
                return fruit

            def RunScript(self, Index, D1, D2, D3, D4, D5, D6):
                Index = 0 if Index is None else Index
                origin_data = [D1, D2, D3, D4, D5, D6]
                available_trees = [_ for _ in origin_data if _.BranchCount != 0]

                single_data = self.Picking_Fruit(available_trees, Index)
                result_list = single_data if len(single_data) == len(origin_data) else single_data + [None] * abs(len(single_data) - len(origin_data))

                R1, R2, R3, R4, R5, R6 = result_list
                return R1, R2, R3, R4, R5, R6


        # 树形数据处理
        class TreeData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TreeData", "D35",
                                                                   """Data Tree processing problems，A is going to be as long as B is""",
                                                                   "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("22bf3aa8-c9f3-420f-8cdb-eefc24ea864b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "A_Brep", "A", "The Brep set of A")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "B_Brep", "B", "The Brep set of B")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_list", "R", "Corresponding result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVoSURBVEhLrZR5UFNXFIefLCF5W1IVS4QWFQRkRAShKbGERHZCBRcMiAoCsggGhCQIIQTCjgs7Qi0oSl1qW7VSmSqjWMXWDlVRWxVHcV8q7h1bGdvT+8Jr/1DHjlO+mTNz3z3n/s65c8952AhhhsxmePn2mCBjBIxwHClHjswqhP1kGIXPt5ZTX4lvcDMcFpg7Ei5EvVspL9p2Duv/T2i8wuUor3paOS9UGE51SZ5THTNfmMnGSlg/Rja6fSt4HA7kAe+n1B7xLcGzOUBumHEKuajhiDfAi7EN558OAP7lYKD2e/9ODwQD/XMAcObZqJB7tMVcaxnR4rGb7g8C6gKKuxhkjCVqp3ciP98owsLjpE1a5ZQgysycGuNkEm2dYe7Cd7dYYW9HfiO+xr+EEvQHAs0kO+77J9kleUBsE13nyK0+YxIyPsuTIUCd9kcxyI5IB8l2T+YWw3CTJkXRKPuYHj9wLve9SV0OAk7hlK3jQx3Vwu7gIWKAEfeH6XsjQHAKJbkpB3KP+C46aodl2RrcOxVP/TsTgXNOBnSfP/KHAirg8bA6gpcwYQX/LKrkXAAQ5/yAfw0J7PLq5UXaJjtrffroH2a9cO1WgGzHEuDcRgkGQoCbbp/PnI3D3MbHaZNAqPO4Q/T5guBhGJBfix+Y+Y7zwrgBlmJih6iHPCy9T5/wM1ZHo0T0GSRyJQTMcx1W+2CYYMJi123T1NIe2xrJGbzD61dym+hHk7QJSWcPHSLLi0v2RiYvjsNcMBvesokFxNppzXjR1AaUm4/h/pbT6X3eYOyCM34g7AkB6+4QwAfQQ7a5HUdBVkyVKxVJ8dEJi/ZptTl5CnlEIrPHUFpa1KFLyA5jP18PT+WQQn3p9R3/Vijwb8iB2Pkh2KvF9yKiFe1sCJaYuPSjZUvjr62vr9+0pXW7JwCYFRUVtGQoknPHGFzDTUOFAWzo6+GtdFiNevwKnu/8OTaLn+Hr7Ssvyy3urKqvl/T29poHersLFQsW3DEYDE0NDQ2GitLSKH16Tq9nrGSrZX8o4Js9jhKtHkfwVLsEzH40zcr+yyhkzFCYYLhpEF7jth9Le1e+KHJhSV1lXUtra6uLLkc1c3lyMhQUFl6trKzcXq0til+oinlGHZAAcQF1DZoDwaMwoHaLwdyJmGpUfRmO4v0Icoeoi3lcGg0LVma3U7lCeay5pllVWVnWrUxLfZ6n1UKWRhecEhW7ebx6xlPuCelwU5wPBKpHdt8izzmWlXsJvrk70f7BEDPm9ClU0YUg4O4Xw7hyz3ul+pLL5aUVX6QkL7uqUqt/L1TqlssTZj/iHfd5YRRHfc9MMt3tM2gRZRPIKr6CGVftsJjsmNnPXPefJKZ93s+l2rB7BSrd2aWxS64WFOQ/1CSmD05OFV3Eb6E41M7GwUJD+s4fcwGvcd3D6r2KqWiMlDooucv8Fpgr0yf9gLgYAFbfB0NmRgbELYl5oFFl/ZU+PzETy38vBQ3iJT7zbzomG8LLXHYRGz0Oc+MnLmLlXoXzsTCMmWb6Jz+guqXPmLcgDkqekNlO2eo8zV3UpkMajQZSUzP9UTiBzB7fMOM80eZ5Ha1HI2Oa5Q04kGO5WZMjeQkT5+PaKXmCwdlAbhXdRh6T9euqtqQrlZC9KgdWqlQLhw8YEWBcMzG7fisseDmOm7gyS+Ph5pq1PjptDixPTUNdpI03Row0xXptV0V5GWhW6ZTs1shSWZg7r31zG2j1xdXs1siyrrygoW3TRtAXlf3Cbo0cjRUGx6rVJU9qa2thTVUN6IvXxLGu/4derzf5tLkhvLG+5reWpjr4pGk91DU2QWvbFqhu3KDTNzfjbOhrwLC/AVZGNqF2VxWhAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, A_Brep, B_Brep):
                if A_Brep:
                    if len(B_Brep) > len(A_Brep):
                        Result_list = A_Brep * len(B_Brep)
                        return Result_list
                    elif len(B_Brep) == len(A_Brep):
                        Result_list = A_Brep * len(B_Brep)
                        return Result_list
                    elif len(B_Brep) == 0:
                        Result_list = A_Brep * 1
                        return Result_list
                else:
                    pass


        # 简化树形数据
        class Simplify_Data(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Simplify_Data", "D24", """Reduce all incoming tree structures to their simplest state""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("813ad085-0bdf-44e4-9178-79e0549298aa")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_Tree", "DT", "Data Tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Tree", "RT", "The simplest result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def handle_list_data(self, data):
                for single in data:
                    if isinstance(single, (list)) is True:
                        return list(chain(*data))
                return data

            def RunScript(self, Data_Tree):
                try:
                    re_mes = Message.RE_MES([Data_Tree], ['Data_Tree'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Data_Tree.SimplifyPaths()
                        origin_data = [list(_) for _ in Data_Tree.Branches]
                        path_list = [list(d.Indices) for d in Data_Tree.Paths]
                        minpath = set([_[0] for _ in path_list])
                        depest_list = []
                        for father_index in minpath:
                            sub_list = []
                            for index, _ in enumerate(path_list):
                                if _[0] == father_index:
                                    sub_list.append(origin_data[index])
                            depest_list.append(sub_list)
                        result = ght.list_to_tree(ghp.run(self.handle_list_data, depest_list))
                        result.SimplifyPaths()
                        return result
                finally:
                    self.Message = 'Simplify'


        # 树形数据修剪
        class TrimTree(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TrimTree", "D15", """Tree trimmer plug-in，Depth is indicates the pruning depth of the tree""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6334661a-78f2-4b9b-be00-a425575c9abd")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_Tree", "T", "Tree data to be trimmed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Depth", "DP", "trim depth")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "The result after trimming")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.origin_data = None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def flatten(self, origin_list, result_res):
                for each in origin_list:
                    if 'List[object]' in str(type(each)):
                        self.flatten(each, result_res)
                    else:
                        result_res.append(each)
                return result_res

            def _handle_path(self, data):
                temp_res_list = []
                count, total = 0, 0
                while len(data) > total:
                    flatten_list = list(chain(*temp_res_list))
                    if count not in flatten_list:
                        sub_index = []
                        for _ in range(len(data)):
                            if str(data[count]) == str(data[_]):
                                sub_index.append(_)
                        temp_res_list.append(sub_index)
                        total += len(sub_index)
                    count += 1
                temp_new_ghpath = [data[_[0]] for _ in temp_res_list]

                res_list = temp_res_list if len(temp_res_list) != 0 else [[_] for _ in range(len(data))]
                new_ghpath = temp_new_ghpath if len(temp_new_ghpath) != 0 else data
                return zip(res_list, new_ghpath)

            def _trim_tree(self, origin_tree, depths):
                try:
                    origin_tree = [eval("_{}".format(depths[0])) for _ in origin_tree]
                    depths.pop(0)
                    if len(depths) != 0:
                        return self._trim_tree(origin_tree, depths)
                    else:
                        return origin_tree
                except:
                    return origin_tree

            def _deepest_length(self, path, factor):
                if factor < 0:
                    return -1
                else:
                    for _ in path.Paths:
                        if factor >= _.Length:
                            return False
                    return True

            def RunScript(self, Data_Tree, Depth):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    Depth = 1 if Depth is None else Depth
                    Result = gd[object]()
                    Data_Tree.SimplifyPaths()
                    re_mes = Message.RE_MES([Data_Tree], ['Data_Tree'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        temp_data = [list(_) for _ in Data_Tree.Branches]
                        if Depth == 0:
                            Result = [list(chain(*_)) for _ in temp_data]
                            Result = ght.list_to_tree(Result)
                            path_list = [_ for _ in Data_Tree.Paths]
                            [Result.Paths[_].FromString(str(path_list[_])) for _ in range(len(Result.Paths))]
                        else:
                            self.origin_data = []
                            for _ in temp_data:
                                if len(_) == 1 and 'List[object]' in str(type(_[0])):
                                    gh_Geos = [gk.GH_Convert.ToGeometricGoo(g) for g in list(chain(*_[0]))]
                                    ghGroup = gk.Types.GH_GeometryGroup()
                                    ghGroup.Objects.AddRange(gh_Geos)
                                    self.origin_data.append([ghGroup])
                                else:
                                    self.origin_data.append(self.flatten(_, []))

                            if self.origin_data and len(self.origin_data) > 1:
                                result_boolean = self._deepest_length(Data_Tree, Depth)
                                if result_boolean is False:
                                    Message.message3(self, "trimming has been completely！")

                                new_depth = Data_Tree.Paths[0].Length - 1 if result_boolean is False or result_boolean == -1 else Depth
                                depth_cull = ['.CullElement()' for _ in range(new_depth)]
                                origin_path = self._trim_tree([_ for _ in Data_Tree.Paths], depth_cull)
                                index_list, new_paths = zip(*self._handle_path(origin_path))

                                trunk_list = map(lambda x: list(chain(*[self.origin_data[_] for _ in x])), index_list)
                                result_list = []
                                for _ in trunk_list:
                                    if len(_) == 1 and 'List[object]' in str(type(_[0])):
                                        gh_Geos = [gk.GH_Convert.ToGeometricGoo(g) for g in list(chain(*_[0]))]
                                        ghGroup = gk.Types.GH_GeometryGroup()
                                        ghGroup.Objects.AddRange(gh_Geos)
                                        result_list.append([ghGroup])
                                    else:
                                        result_list.append(self.flatten(_, []))
                                Result = ght.list_to_tree(result_list)
                                [Result.Paths[_].FromString(str(new_paths[_])) for _ in range(len(Result.Paths))]

                            elif len(self.origin_data) == 1:
                                Result = Data_Tree
                    return Result
                finally:
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    if -1 >= Depth:
                        self.Message = 'Simplest'
                    else:
                        self.Message = 'trim degree：{}'.format(Depth)


        # RPP_数据结构对比
        class Data_Structure_Comparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data structure", "D31",
                                                                   """Compare the two sets of data，if same,then output True，or else False。\nps：This plug-in only compares data structures，it has nothing to do with data""",
                                                                   "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("344e81f6-d3bc-4a07-a4a6-e9faccaa9e48")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataA", "A", "The first set of comparative data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataB", "B", "The second set of comparative data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "verdict", "V", "Comparison result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAShSURBVEhLlZV7bBRFHMcXe729vd3b7VOuD9qkFnvd2/e117t6XB/Xlru2lCZ4YkgridFExRqNjZKUhgYb/iBINaZSRKJBDWgaa/FFQFHUNgErmghItaC0WKNpQRqIouL4m73xcfZ61k8y2Znf97szv/ntZoZKwhLyXCyL99s2FK9jB4zjtuqsKhJKyqL8dKMzzPapD1ojzgg3VDmb/usaZH9C/SC1iJUsnvQAWJiYM0ZC/5Pq0YX8lL2rdHvabAtyfFiN+E9Cv/HjYcQdqZp1jNT8Yn9KmwILG3PGSOwPLuin2B6xw3G8dk6YiCD+8wbEf1aP8EvCt82I3WkMgyUuI+zn/4efsgYyRG64clr4fhXiT69E/JlYE6abkX2HOkzl8xnEajLPP/4Pf5/62r/9lK0xt5J90TviOFB5kT9ajdjdnus8bJ972Tdue6Skk8qh7MRqYvpf8I4u1v8nNmiKZW3eRrq98D66fmktjJeZSmKwX7thbW4ndXdeu2Vl1goYJ/NTVP3SeraOKhLI8C/Ky8szPR5PFhnGUUWLxZXLyzUyTI4syz2apl4OhUKZJERFRdGqKPK0oki7ScjkVp+PAe+gqioI9N+hXdJ1vZTIiVEUpcLj0VFZmX4nCVGGodQaho40TV5NQibYg+Nut7sGEivSFKVb00SRyAsjud1TkM0IGcKupL2yJF0Nh8M0CZl4dL0DL+DxqF4SWhyy7N4CW0ekTEtggauSJD0XU//G71duVBX5tK5rsDt1j2EYNxEpObDdEvwSfNQolEzHWUIM/yHzgHg6fJs+VVGQpqpXNE0rJ1JyJMl9RlXVg6oq74HyzESj0RQiJcQwXDmwyBx4Xyeh5EBmD+EyQVaQvXs7CccBv27Y7y/Tcb+trY3VNeWSJIoHTPG/8Hq9+fj3M6BUuEwkHAdk3I/LB75JSOQajC/6svViIieGaS+IWptzWnEfdrFecbvvNQWCtTUvQtdkN+A+LpsqSa2qLG+RRXmDj8rPoAIZFdYs682mmUBTBXQRPDOZltwWfiyEHIeD11NkIRSTTZzQWLrBGeZHapDjYOCaRUqbd7mkrM8POz6qQdxL3vMwXB6LUhTH7tTPcu8FZxyD/lPCWTh+TzYgtl97m3vFN2bR0h6A43eUeyc4ye2vOCF83Yj4Uw1wwmpDcDi+b/GkdbG7jGPskH+U21dxTPiuGe6HOmTvLh2w92uDlL0q2+l41f8DPnbNyfG5Dg1PJEw1IXpNXi/o59JmWuJ16AsXmpDttvxdjkMrrpj6l+GY/mkdEr6Cu+F8I6IokbLaHi15mD9RFzvXIXvchIkwchypukzfXlDLbHTdj7OK02EC7t3gj9Z1hRF2m7LNjOOLhzThXARxbwYu4BIxzGZxr4Bfwhl8HEL8GGTwTSPi3grM0atz7rJvcg0I+DLBtxdeCO9gsgl/i5/oVTkd9q3SIN6tWT5IVPgCvHCzOd645WfzIwCMrTWvDSZ6mulynWQ2uZ61dZfusHJWl6kGhHSmvfAetld6ntlcOsH0iPuYXumZVJdgYDn1jmVuprNkK9evH2Iec0/bH1cOwy2431bvDP4BqTzTzW5fEyAAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            # 树形数据取信息
            def Lindex(self, Tree_):
                a = [Tree_.Paths]
                b = [len(Tree_.Branches[i]) for i in range(Tree_.BranchCount)]
                c = [Tree_.BranchCount]
                return ght.list_to_tree([a, b, c])

            # 结构数据对比
            def Compare(self, x_tree, y_tree):
                XData = x_tree.Branches
                YData = y_tree.Branches
                BOOLLIST = []
                if x_tree.BranchCount == y_tree.BranchCount:
                    for i_ in range(x_tree.BranchCount):
                        xl = [x_ for x_ in XData[i_]]
                        yl = [y_ for y_ in YData[i_]]
                        TLB = eq(xl, yl)
                        BOOLLIST.append(TLB)
                else:
                    BOOLLIST.append(False)
                return all(BOOLLIST)

            def RunScript(self, DataTree_A, DataTree_B):
                try:
                    Boolean_tree = gd[object]()
                    re_mes = Message.RE_MES([DataTree_A, DataTree_B], ['DataTree_A', 'DataTree_B'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Data_ = map(self.Lindex, [DataTree_A, DataTree_B])
                        Boolean_tree = self.Compare(Data_[0], Data_[1])
                    return Boolean_tree
                finally:
                    self.Message = 'HAE Structural comparison'


        # 数据清洗
        class Data_rinse(component):

            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data_rinse", "D34",
                                                                   """Remove null and space values""",
                                                                   "Scavenger",
                                                                   "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("13b14752-b265-4040-bfea-81d0c089b31b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "Data that needs to be cleaned")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "The data after cleaning.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOVSURBVEhL3ZVbaBRXGMenlF4pfRDRYqS0Raomu3Nd9jK7s7Mze012d+6TzdXE2GJrkdKX+hBFEu9JS1WMASXqaxAR2peKUTGhrqu7O2k0LU1M8YIPLQiFtoq0cHrOeBqUvmRjnvqDw57vO9/3/873zewu8f8ieNd6DW+XFvqGyjNT+nfsrHWZdfRPKEf7gqmYpHsIwAvu52JZM5N5hayqs4Gi0R0otqwMTGgRsqJeZEqmj5xSt7L3Cmfh+e76m/YblKNuY+81j5CTusxUtBAzbfbRs9YI+YPuwXJEmOPepijqHWwSBOXkG+iy+hM2XbxV9QxVUT8nHfUOM6n1eKfUX2HRTqaomtyM/Zm3qlwiq8pJ6nvtW+6G0QvtcziVkKLCVUmM3uc4brnroJxsHRS63XWy61XXAYHJo1DwCPTPeUu5Xmba6GVKSpR0lCFurnnQU1XGYDenPKV8c2hSXwE7vIzyRJ7fmknGQSaVAFEhPAZdLyI/QVaU4/SPxgX6lnmYva7vgLf/hrmqdsKbXWHv2N3Q3kyVFR3at6ibOuqgDH2nPdDvu6as9cxq58XVzJp4THyckGNAjkXdInww+IFbAEE7us1Nmx8Fx7J11Hg+LMKOqIl8Aztj7aaLuS3c17nX6bJiU46+jSmpcfqKkmCK2nr/TPub9HjWkiOCk0rIrjhaaA/HVcbyz4fs5Qcb04l5cbRQJ2I08gcOWTyhgG8jum1cEp8pgHywwCQOWxzwdZSg8MN/5/70Qs9AjPAf49DasdLS2jY99zAZl/4j7s5fFKbhq/oSDq+NALuOyyXknze12u6spafE0ahQUb/fL+Hw2uBZSuoysg+6LR0YTSnQmIqj284XQKPx+3zDOLw21Fwm3mHm/7KbEuDDFhO0a1mQfjKOefGYKIzC0JefZNRAnxFKH9iQ/P3TQhPY1GqBNk0BuUxyXjwNv8FQvLqoufdbIevL9ujfx3pk0GcE76tJ+UEBFpBiojv/VEJChX4jSfJ9nLJw+m2+42BnDBzdKIOBVuGXAbv+LSuffLenxZxrTCXdBwrXI5+PFnHKwum3eAWJH9oQA191iKBPDyTxEVFfv3qZwPOjjenUYz2fz2D3wtmphzxwLH8i8eGeONhlhbbjo2eQJKkBbxfOToVfNdAizB3pksBQtwz2FsKH8dHSsKcQPnFqcxocheL7CuEh7F469hmR9wZbheL+QgT93D7HfzJB/AP43Ixsj34I7QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def fit_main(self, data):
                if 'str' in str(type(data)):
                    if " " != data:
                        return data
                elif data:
                    return data

            def Data_cut(self, datalist):
                # filter 过滤空值
                dalist = list(filter(self.fit_main, datalist))
                return dalist

            def RunScript(self, Data):
                try:
                    re_mes = Message.RE_MES([Data], ['Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        tree_Data = [list(data_) for data_ in Data.Branches]
                        tree_path = [path_ for path_ in Data.Paths]

                        Datas = ghp.run(self.Data_cut, tree_Data)
                        New_Tree = gd[object]()
                        for tr_ in range(Data.BranchCount):
                            if Datas[tr_]:
                                New_Tree.AddRange(Datas[tr_], tree_path[tr_])
                            else:
                                continue
                        return New_Tree
                finally:
                    self.Message = 'Data cleaning'


        # 数据对比
        class DataComparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Data Comparison", "D32", """Group based on conditions.""",
                                                                   "Scavenger",
                                                                   "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7b77656d-aeeb-4066-a831-c3a7711ab743")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GroupByData", "G", "Grouping basis list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GroupData", "D", "Grouping list list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "ByTree", "G", "results from the group tree")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DaTree", "D", "results from the list tree")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVCSURBVEhLlVUJTBRnFH67szvM7s7MLizgAoqsqEWsrhKsAosXl6gRARUiHm2QKIpWMa1HFMVbLBVI8aqaSioVUaEm1qvWprbWWlsbxaP2CJWoscZ4AYoor+/fGVNg1zT9kpf53/u/9/5j3jcDHuAgE5Xh/wJvNuoj1LFn8Im2dFP1kGfCij7HyPVToq+FRn0yiIcq8k/+/G3Rs0mpUZlqTIEuTBpiWNW3kn83dImhzPGld1MqisdjURtsmqJP7ToD/PQDVGpncMvfS11Xc2DpjkULUha13P0UEU/jni251XnZ8WnJiQMmE8cLOKd/vFyXiObfRqF0biTKVxJR+n7kc/GYs5X5XD/zBKWeG7Rf1S47j3gGn96uwNZ7e9vaHu7DhrryxudPD2Hlx3MvEUcHXqndEsQjMbfNN0YhW0j+JcH1NDeMQdNR5wPOYR6h1HODUFORX9X8YN9LfFyNbfcr8eW9vYhNBxBbP8eKrbM/IY7eRTSsDK8y/zXatXv5WtK/C9RE12sCDeuIM4QROyMrI2Z4w9Wtzdhai/hgH7KF8FEVYvNBLNswvYQoRoBA/g1jqeOCdJau53IimvYMQum7EShfiEPDtog6LtrKTpBNNpIVbQdtwftpK+qvbW1pvFOBj2/uxp++Xo/4vBavXSx9UrJ2WjFxTAoVQOJ6i+P57JCd+oyuh/mckAJdki2f4rQDF7RkeWRxLq8d7AGW2Nk5yQvXF2SeyZ+ZXLSxcPIaCg9SZj2DFdEpww5gbTmHLJ45twICXi3+CjYBdLHq2DP4MYHjTDVRj4WVfY+S66tE3TCPzh3fZu+brvoMBqGo3xFD1eBG/TBfDzpYHf6ZML/XUkOJ4xTTgXSCdBBinKpPD8oBX/1AldoeEz4y+pSHTbaX8aUDdvBpQYvl83FoeZSCwuKwan6sLV07yJJFPFUH1D3m30kHP7TTwXHnC+ZzEeZUpaYL3mTsc5CxEaST3UsGXpKaxqNExeWL8W2s+8Sjzkb5ehIKheGXiUc6SAuOF484b7np4Ca16cmhf3M9xYlETCGbySyI4yYesAZu/kMIiIUP++2SLye8cLX2JcqjXFbH/Gcyei3r8xodXG2ng9roem1P6R3iMB2w3QPu38+19ejTi425odYR9FlpNtdTLtscW4jl/5qEXnNDS4mi6qDE8aN0lnqfdtFBB1sirugSugxmxTxAy2cFF9BVPmNXKX0zHI27Iumqk9F0OPqJV17PDjoQuVAxhZ9h3wbTuh2EXPsSXaL/fIp3bkV3CDqnbqxtgXam/RRMsK3Vz7IXUjRSmXSH/JbGWNz7P4TiAdpgat0ojVik+h0gk7Ge14wGeVEZdMU88LtHfiibJDAVewKLs3+GRBYwD/zullJuHEgb2KQKDnqAzkkF788Bv/P54F+3BYKxEAJaxoK8fSp4nwgCfrRK7gxNGlgOLQXbnelgPb4OgrCcckk4p6eDT+UwkHYSR6DLMiZvopXZZDE91xORWQl0wzIyBwhTlHpu0FOxC7uhu4u7Uc3bQMZi2eB7nTheMBSkXrnge4wVZ5OMyIwlLQD/+t7Ahyn13KBLB+9Zy8HW9EG73CLVxoF5FeOwPuryNljPbacTbCYiI7EEdlWLwfYiEoQMpZ47YkGcsQYCXaffpBZmG2P+RLB8QRRvsNGLmgTea3PB7wbd58Ms8GEv+elC8G9IAUvRm2DqopRzgyaGrjcHrGfopDfJcBJYnlCNlmlgPREFxiTicApVgSUE9FMjtcYCevEx5L+2lzvBQN/2wf3BsLo/CJk+oGOqVwUG8A+AlgcmZniPAwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def indextree(self, gbdata, data):
                if data == 0:
                    if type(th.tree_to_list(gbdata)[0]) != list:
                        atype = type((th.tree_to_list(gbdata))[0])
                    else:
                        atype = type((th.tree_to_list(gbdata))[0][0])
                    gbdatatree = DataTree[atype]()
                    datatree = DataTree[int]()
                    for i in range(len(gbdata.Branches)):
                        gpdalist = list(gbdata.Branch(i))
                        list1 = list(set(gpdalist))
                        list1.sort(key=gpdalist.index)
                        for j in range(len(list1)):
                            num = gpdalist.count(list1[j])
                            gbdatatree.Add(list1[j], GH_Path(i, j))

                            for un in range(num):
                                index = gpdalist.index(list1[j])
                                gpdalist[index] = 'aaaa'
                                datatree.Add(index, GH_Path(i, j))
                    return gbdatatree, datatree

                elif data != 0:
                    if type(th.tree_to_list(gbdata)[0]) != list:
                        atype = type((th.tree_to_list(gbdata))[0])
                    else:
                        atype = type((th.tree_to_list(gbdata))[0][0])
                    if type(th.tree_to_list(data)[0]) != list:
                        btype = type((th.tree_to_list(data))[0])
                    else:
                        btype = type((th.tree_to_list(data))[0][0])
                    gbdatatree = DataTree[atype]()
                    datatree = DataTree[btype]()

                    for i in range(len(gbdata.Branches)):
                        gpdalist = list(gbdata.Branch(i))
                        dalist = list(data.Branch(i))
                        list1 = list(set(gpdalist))
                        list1.sort(key=gpdalist.index)
                        for j in range(len(list1)):
                            num = gpdalist.count(list1[j])
                            gbdatatree.Add(list1[j], GH_Path(i, j))
                            for un in range(num):
                                index = gpdalist.index(list1[j])
                                datab = dalist[index]
                                gpdalist[index] = 'aaa'
                                datatree.Add(datab, GH_Path(i, j))
                    return gbdatatree, datatree

            def RunScript(self, GroupByData, GroupData):
                try:
                    re_mes = Message.RE_MES([GroupByData, GroupData], ['GroupByData', 'GroupData'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        if GroupData.BranchCount < 1:
                            GroupData2 = 0
                        elif GroupData.BranchCount == GroupByData.BranchCount:
                            GroupData2 = GroupData
                        elif GroupData.BranchCount == 1 and GroupByData.BranchCount > 1:
                            btype = type((th.tree_to_list(GroupData))[0])
                            ggdata, GroupData2 = th.tree_to_list(GroupData), DataTree[btype]()
                            for i in range(GroupByData.BranchCount):
                                for j in range(len(ggdata)):
                                    GroupData2.Add(ggdata[j], GH_Path(i))
                        elif GroupData.BranchCount % GroupByData.BranchCount == 0:
                            btype = type((th.tree_to_list(GroupData))[0])
                            GroupData2 = DataTree[btype]()
                            for i in range(GroupByData.BranchCount / GroupData.BranchCount):
                                for j in range(GroupData.BranchCount):
                                    ggdata = GroupData.Branch(j)
                                    for j in range(len(ggdata)):
                                        GroupData2.Add(ggdata[j], GH_Path(i))
                        gbdata, data = self.indextree(GroupByData, GroupData2)
                        return gbdata, data
                finally:
                    self.Message = 'Data comparison'


        # 数据比较
        class CompareSize(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CompareSize", "D33", """Data comparison，used to compare the length and area（Geometric object），only data comparison is also available""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("607f91d1-8b00-4700-94cb-e7e11714f13f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "geometric object for comparision,can be line or Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Specifylen", "T", "cut by specific data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Closed", "C", "the range is closed or not,default is closed")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Compare", "S", "Select range greater or less than ，default is greater than")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "G", "final data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Excluded_Data", "E", "Deleted data")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASkSURBVEhLrVZtTJtVFD5jpfT7paWlUMrHSJcCfb8LLYUiQxlsA4EsRpnKzMZkToObwaKMLXVkEzemkzl1YcsMcwtxv/yxmf0YxixZNNEILrgxjTA3EpJlcSE4mfHjeu7bt4pp0Zn4JE/uPfec+5x7zn17U/iP0Gh5Zj2O3pj5P0GToSnTthc8bxiSL1s+e5CY3iudM2wpiKTy6RvRbYhF3R9KdI/lHtMflTp1L3kjadtX9kNeWqGu1NbDXKknzPfriOUqjtNrlbm2JWcE9+iWY1WpISur8VvDaD+EXEbFEqAFKDL3s3fTbzcR5ts1hPluLTGfD98znwvPWTCB5avVMV5GYiLTcf+EeSR41XKphpg/xcpOBUiKLqVLlUuEri5ro/ld+RYzjSeNC15bQyzfIMdV8TjRZqawEjWWmWkgpg8rftEUm19EKTxrMjzi1qc+7ub07SuGLRdX/ZVkMb+ui1WweA0PYT5X+WtaR+FebUUG/QA0McFEeHRt+YPGD4LztD3MzQbC3EDi3DJRp/TeTBOjIHNdvQ8c6emZsdXEdKJ0Nq05+wDqZMXkEpEKzc4CQ5d3k77be9J4SPjBdFQeNg7J48xkPTEelmYMe3xE31s0YTpbeY323riPHdMPSX3Lmpz7wA7Zqk4iqqurNRUVFS7VpNAh3XRiybUO6ta7d+G0QB8tuYCjB6lZ7mdW4RhCQrWRZ6v4qhV0nhTBYNApCPzPkiT1qksKBI6LCCXcwgvg1qtLf0N9TY0X913nee53URQIz7Mfqa5EsKxvDANnVFMBrk1zHDummgkQBf5zjJmSvF6XLHNVmGA3Lif/HXAc97QsSyRQGRCojdUUS5JIBEHoUAKSAA90hef5yWg0mqIuLQ1RFB1YLhFlcT+1BYHro3Y4HHYoAUmAe5olbI3A87cFWdhB71J1JQfLlnwcb1OsPb5PFMc/gGXZELZx1I/VYxdGy8vLk96XAgzYQC8rEPBvVaoRxQ2q618hCcKTflnGi+YfVpcSEQgELHjyOyh+j47UVl1x/PkMYN81wWBpa21tLUPtcDjUSBP4fL5GJWApsAI3XBYsI5wkHFeXqICjCZjIVrBPtgBzGu1CyM1wcaxvHiv+kX6q9IPADpz1eDxpyq4ksGeCprwoPz9UXOw94nI6lZPkQWpbBDLvDEAOOQK5ZBC5C7JvVYHxJITzrI7ilZEc0bczXShqwHAr3bMUuFawLvRD9mwUHFM94JzfBo4zW8B+4S0UPYAJXlP5DuSRVrCdaQNmx7Ngu9QDtlObIf089o++pskhgmEdCs6dgHzyBrgVUuE3kXHhxdyPPIQxh9F/DPdQ2w1amiD5p1oJpjAm6HsOHF++qgokE46T+ikHMMkeyP7tCbCN5GOLUSr5LxmhlcHQ+BTYRmk7XseNlAeR/aoQnVPGk1M/rYD6O8BxsQZM21DHHpNLhKceTN3bIfOLlyFrllaxE5w/vQJZC29jz/eCi3RCJukGp5KEru2GrLu9kHVzM2TcaAPbQAhMD6DOff0RKPOCrsuGT3YIDKefAfu4H/SdmyCD+MHQ/igwLVjp+y7QRDGWPu2Ln3oVAH8APDu0r+xre+MAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None
                self.type_dict = {0: 'GetArea', 1: 'GetLength'}

            def is_change(self, vaule):
                return self.dict_data if vaule == 'max' else {True: ['<=', '>'], False: ['<', '>=']}

            def choice(self, data_list):
                self.factor = 0 if all([isinstance(_, rg.Brep) for _ in data_list]) is True else 1
                if self.factor == 1:
                    data_list = [l.ToNurbsCurve() for l in data_list if type(l) == rg.Line]
                return data_list, self.type_dict[self.factor]

            def RunScript(self, Geometry, Specifylen, Close, Compare):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        Compare = {True: ['>=', '<'], False: ['>', '<=']} if Compare is None else {True: ['<=', '>'], False: ['<', '>=']}
                        compare_symbols = Compare[Close]
                        if Geometry:
                            data_stream = Geometry if all([isinstance(_, (int, float)) for _ in Geometry]) is True else self.choice(Geometry)
                            try:
                                Result = eval('[r for r in data_stream[0] if r.{}() {} Specifylen]'.format(data_stream[1], compare_symbols[0]))
                                Excluded_Data = eval('[e for e in data_stream[0] if e.{}() {} Specifylen]'.format(data_stream[1], compare_symbols[1]))
                            except:
                                Result = eval('[r for r in Geometry if r {} Specifylen]'.format(compare_symbols[0]))
                                Excluded_Data = eval('[e for e in Geometry if e {} Specifylen]'.format(compare_symbols[1]))
                            return Result, Excluded_Data
                finally:
                    self.Message = 'Data comparison'


        # Python列表数据转
        class Data_py_listdata(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP pydata", "D25",
                                                                   """Converts Python's list type to normal data""", "Scavenger",
                                                                   "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d04813b1-38e1-4c2c-99b7-ce12f95477a2")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "PyData", "P", "Python list data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GhData", "D", "GH data.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJmSURBVEhL7dRNTxNBHAbwrRAb1LS7tWVLFQzUk1XTgzER2K0t3aYkxoPSaEzT3SqiFKz2YgjGNCrFNzBq9GBI5OTF7+DVL2DUlgZMFJWW12h96aXrMzJaIt0N5Uh8kl925r+TmZ3N7DL/U1VUhjHMc9zevNXaQEu6ORN4b+mWcm7Zk3FHvFmXIr7dJ3veuSPt6f1Jj1pLh5WDBWrzLPsjx7IjtKQbRcjI53wzRUXMFKPihCqL6dJpcaqI63y0/ZONDiuHLvAN7tCSbsLS5609/o9Npw693qUI6YIipsd72iabFOFVYyj0vIYOK4cu8BVu09Kag10sYBH9na9/AdWAyRdlIX2fFipnwyxQyHFcipbWmCoXmGPZsZzJ5FyCGbO5hdTpEI2oBhzNL4rw5iEtVA4mqpnl2GyB437Osuz3Bchz3NKcpW4HHaIZGadIFrP3aFc7pe11jpLZ2FwyGZ2Eaja20Fu6CUuLzV2BkoV2K6fX5g3E7cHsWb5jYqVYve9DP++d1nPB1prps4lTF3lpOsZ7X4aY0OoPDTdcA/ZgasDRefWS3T+caJCG+nnf3YRdSsXtHbf6eO8IaZN7GDtaSZz3j8bqDw8mmeQmOu2qbIE22AwcKSDb6JWEh5X9qnMNYkC+hSE4AUlQ4DxFxuwGkj3gWm4yTjiw3NTOFUgA+a/shBdwBELwFKLwBB7AMRiGmxCBMXgMR0EzN2AQrL97DPMIyEkSgEzSBT7ohmfQCUEYB7I7D1wGzZAn/LN9kl5oBAeQ33gYyGsgOyKTkdd4HVrhJByE47CukJNhWG7+zb/9DRWG+QXBbOVgbgxyZQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Data):
                try:
                    re_mes = Message.RE_MES([Data], ['Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        tree_Data = [list(data_) for data_ in Data.Branches]
                        return ght.list_to_tree(tree_Data)
                finally:
                    self.Message = 'PyList to Tree'


        # 通过真假值筛选元素
        class PickFactor(component):

            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PickFactor", "D23", """data tree select in batches,by （True，False）""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d08f954e-5ce0-47ee-8c7f-bd28c8479e31")

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
                self.SetUpParam(p, "Factor", "F", "Control Factor")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "T_Factor", "TF", "True Factor Data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "F_Factor", "FF", "Faulse Factor Data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Result List")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            def format_tree(self, result_tree):
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            for sub_index in range(len(item)):
                                stock_tree.Insert(item[sub_index], path, sub_index)
                        else:
                            stock_tree.Insert(item, path, index)
                return stock_tree

            def split_tree(self, tree_data, tree_path):
                new_tree = ght.list_to_tree(tree_data, True, tree_path)
                result_data, result_path = self.Branch_Route(new_tree)
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def pick_data(self, tuple_data):
                Rhino.RhinoApp.Wait()
                bool_data, data_one, data_two = tuple_data
                bool_data_base = True if bool_data[0] else False
                return data_one if bool_data_base else data_two

            def RunScript(self, Factor, T_Factor, F_Factor):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result = gd[object]()
                    factor_trunk_list, t_trunk_list, f_trunk_list = self.Branch_Route(Factor)[0], self.Branch_Route(T_Factor)[0], self.Branch_Route(F_Factor)[0]
                    re_mes = Message.RE_MES([Factor, T_Factor, F_Factor], ['Factor', 'T_Factor', 'F_Factor'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        len_factor, len_t, len_f = len(factor_trunk_list), len(t_trunk_list), len(f_trunk_list)
                        if len_t != len_f:
                            Message.message1(self, "Filtering data is inconsistent！")
                        else:
                            if len_factor < len_t:
                                Message.message2(self, "The filter factor does not match with data tree！")
                                place_char = [[None]] * (len_t - len_factor)
                                new_factor = factor_trunk_list + place_char
                            elif len_factor > len_t:
                                new_factor = [[all(list(chain(*factor_trunk_list)))]]
                            else:
                                new_factor = factor_trunk_list
                            zip_list = zip(new_factor, t_trunk_list, f_trunk_list)
                            no_format_tree = ghp.run(self.pick_data, zip_list)
                            Result = self.Restore_Tree(no_format_tree, T_Factor)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result
                finally:
                    self.Message = 'data tree filtering in batches'


        # 树形数据同步
        class TreeSynchronization(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TreeSynchronization", "D22", """Tree data synchronization，match the missing parts of the two data tree（Similar to an empty placeholder）""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d8f4e8f5-56ce-4464-96bc-7469c0374158")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "A_Tree", "A", "A data tree，can be a target tree or a synchronization tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Tree", "B", "B data tree，can be a target tree or a synchronization tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Tree", "RT", "After pairing,the tree related to missing part,can be A or B")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARtSURBVEhLrVR9TJVlFD/j3sv7dd/nBfnmXr4u3CtcLvdy+S75CBHEkIkfhGJlzUpwECjYh1mtJhYJ1hR0bdps8w9Y6RZZrsx0MyitNpWszMqVrqzmGthsk+LpnPe+EGu13ZG/7bzPe85zfr9znvO8e2EWSEWLCLzeWmhpIFS2QtQvy0E7gX4sxfSdWSLGWHUUgrT8UYjl/ZDAd4CdN0DYZQwnBnZngQwQO1sg8ux6iPpkBYTvqgG2eSeKPw823geJfBNEnzcD5FWC2lUO1sckMNUb1ODgB+XuXux0D4rR+gzE824UpwLb0d8CseMbIHq8D4tuxT07WFYa1OBQDayHhEmMhGklcbLn0HrQfxGN1i4sgPfTbFCDwxJgDa0QfRLFJqc6/zejJnCMH7pBKjCowcMFYsMTEDtBXU4JUrGpglMnWwMRB0tAzkFKSIAZBJwg3NcJMfxlvIOXcM40jhcMYSpI7xTrx/0nIY7PA6UbaXjvQWIOACsFtRa7G2mBqKsdEH3B6HZiLUSO0WgegZiL9RD+pgymGoM2K/jQbAUgP10FSn8jsKFSkGqrgK2OAHNHIOXWIANcSek5aa7hPLvDY8SCn3kw8Hq9/uwcP3dnZ7uN0P/CdHd+vz8+Pz/f5fP57vJmZXFc68hHo//RTAR1yYLU4XpVesgxiO8WtBDs/O0c7JzEPZmZ+prjR9/rfU1nYJ60Pm2b1OY8hu8q+XrUgGysOsQO5xvat4u4dr6Ki02pb1GsGrLshe7cYo/Hs5HE3W53R5YpZUEeaA6d05y6m41W8bBLd3J5o/NjDP39lzXFCHfIWz3D8m7/u8Iy+1r19aJR7XIN136s5coreUdMKUplSHPS/ZBgqvKkuLx+XzaPmxO91Nw1d0A8kHco9N7kNuve3KOUTzzrodvOma3mMuHBlBbzXNYEFpvs046V8bBfl3B2aj5nH6Gdq+Tsi4XcOjTvmjp0+4R2pYZb1iX3lUBqgjfTczTBGlmiHCwaC7tex9mnCzgbLud0Ap3zTskYFrkR9lMtFze5joO0OnEFG0HRr6o5w7Gwz9DOYoEzaBcwhkYFcAw0b/3ixbq4Yna4eFK7tCiQTzzKJ8MipKX9sJhLT2WMQOgqm1Pp9e1jpysmp8VnmHaxmlsPF18TFsdXkDhBqrHblC7Pdnay/Cb7HAX/wWFfLuTq+6W/W1baV1G+Cb+YdnW4/E+9OiVQITLqCLvB5Otim/NxzFWIQBDvSW5Q3yu9oZ+cODSiqZNgARzbTWlzejdY4uRcZWf2Fe17vNhv8MjYMfsAZzpSzvUY+uqR4j+kdY5e1A18cQI4pGczRzX8auiL00d5uoKrJ8r0iyYOO17GpU7Xfj0fES42Ju5T2px71cGiq0geF9tdp5SBwp/lNmefiQnVRt5MSMJSW4+ywbXfeqDga3mH7ze8pzPWwaLv5C3pA6EO6zIjbxrUncXsUB4OXZPULjzgmI9+Aloabf4HRHqYnUqruT6+SWxKaUQ3HI1+kAiAvwBOdrtcIZYjSgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def synchronism(self, origin_data, synchro_data):
                exported_data = [_ for _ in synchro_data]
                for index, item in enumerate(origin_data):
                    if item not in synchro_data:
                        exported_data.insert(index, item)
                return exported_data

            def RunScript(self, A_Tree, B_Tree):
                try:
                    A_Tree.SimplifyPaths()
                    B_Tree.SimplifyPaths()
                    a_trunk_list = [list(_) for _ in A_Tree.Branches]
                    b_trunk_list = [list(_) for _ in B_Tree.Branches]

                    re_mes = Message.RE_MES([A_Tree, B_Tree], ['A_Tree', 'B_Tree'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        if A_Tree.BranchCount > B_Tree.BranchCount:
                            target_paths = [_ for _ in A_Tree.Paths]
                            synchro_paths = [_ for _ in B_Tree.Paths]
                            target_tree = B_Tree
                        else:
                            target_paths = [_ for _ in B_Tree.Paths]
                            synchro_paths = [_ for _ in A_Tree.Paths]
                            target_tree = A_Tree
                        _out_data = self.synchronism(target_paths, synchro_paths)
                        for single_data in _out_data:
                            if single_data not in synchro_paths:
                                target_tree.AddRange([], single_data)
                        Result_Tree = target_tree
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Result_Tree
                finally:
                    self.Message = 'Tree data synchronization'


        # 树性数据插入
        class Tree_AddRange(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TreeAdd", "D13",
                                                                   """Add data of Data_b to Data_a based on the path attribute information and return""",
                                                                   "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6b33efa2-6ce1-4926-80c7-805b58d2d750")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_a", "DA", "original data tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_b", "DB", "insected data tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Path", "P", "Tree path\nIf the data is short as a string，connect the Path plug-in first")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "return", "RE", "Returned value")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Data_a, Data_b, in_path):
                try:
                    DataTree = gd[object]()
                    if not in_path: return gd[object]()

                    if len(in_path) == Data_b.BranchCount:
                        if len(in_path) == 1:
                            Data_a.AddRange(list(Data_b.Branch(0)), in_path[0])
                        else:
                            for path_ in range(len(in_path)):
                                Data_a.AddRange(Data_b.Branch(path_), in_path[path_])

                        paths = Data_a.Paths
                        Branch = [list(_br) for _br in Data_a.Branches]

                        for _i in range(len(paths)):
                            for _j in Branch[_i]:
                                if 'List[object]' in str(type(_j)):
                                    gh_Geos = [GH_Convert.ToGeometricGoo(_n) for _n in _j]
                                    ghGroup = GH_GeometryGroup()
                                    ghGroup.Objects.AddRange(gh_Geos)
                                    DataTree.Add(ghGroup, paths[_i])
                                else:
                                    DataTree.Add(_j, paths[_i])
                    else:
                        Message.message2(self, "The added data does not match with data path,please check")
                    return DataTree
                finally:
                    self.Message = 'data tree insertion'


        # 数据偏移
        class DataShift(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DataShift", "D12", """The data is grouped one by one by offset data list""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c331dd23-ac5f-4032-bffb-339f7e5a874e")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_List", "L", "Data before offset")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Shift", "S", "The amount to be offset,If no input, the default value is 1")
                shift_data = 1
                p.SetPersistentData(gk.Types.GH_Number(shift_data))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Eliminate", "E", "Eliminate unwanted subscripts（selectable）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_List", "RL", "The offset data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Right_Scissor", "RS", "Remove the last offset data of each branches group")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Left_Scissor", "LS", "Remove the first offset data of each branch group")
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
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.shift, self.cull_list = None, None

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
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            for sub_index in range(len(item)):
                                stock_tree.Insert(item[sub_index], path, sub_index)
                        else:
                            stock_tree.Insert(item, path, index)
                return stock_tree

            def cull_data(self, data_list):
                for index in sorted(self.cull_list, reverse=True):
                    del data_list[index]
                return data_list

            def OneByOne(self, tuple_data):
                data, path = tuple_data
                ensemble_data = list(zip(data, data[1:] + data[:1]))
                right_scissor, left_scissor = ensemble_data[0: -1], ensemble_data[1:]
                ensemble_data = self.cull_data(ensemble_data) if self.cull_list else ensemble_data
                right_scissor = self.cull_data(right_scissor) if self.cull_list else right_scissor
                left_scissor = self.cull_data(left_scissor) if self.cull_list else left_scissor

                ungroup_data_list = map(lambda single_data: self.split_tree(single_data, path), [ensemble_data, right_scissor, left_scissor])
                Rhino.RhinoApp.Wait()
                return ungroup_data_list

            def RunScript(self, Data_List, Shift, Eliminate):
                try:
                    re_mes = Message.RE_MES([Data_List], ['Data_List'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        self.shift = Shift
                        self.cull_list = Eliminate
                        origin_data, data_path = self.Branch_Route(Data_List)
                        iter_ungroup_data = zip(*ghp.run(self.OneByOne, zip(origin_data, data_path)))  # 多输出端使用zip解组
                        Result_List, Right_Scissor, Left_Scissor = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)  # 多输出端利用多进程或者map将数据输出
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Result_List, Right_Scissor, Left_Scissor
                finally:
                    self.Message = 'Data Offset'


        # 通过下标取树形数据
        class GetTreeDataByIndex(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GetTreeByIndex", "D14", """The way data tree is extracted according to subscripts；Multiple subscripts are supported（The mode of the tree path is{0; NTH list - 1; Fruit data}permutation）""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e9722fda-2f6c-4564-baaf-e8f5f94729a9")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Tree_Data", "T", "Original tree data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "subscript")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Final data")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVaSURBVEhLnZULTFNnFMe7RygUbH1E4sLmk2QqOnG6KHOKQ0BA0TnQyYa2FltoodJSoC+hQF/0/bi0lEJhoDIjizJFoiI+lokmqKSCiDgdCmKcTtEZGK7cs9tys8QxN/CXnLb3f87/fPd891HCv4GijUQA8EXR8++haNe6ly97VqHovaBnz/qmDQ93L3W7e3eg6PWlePnE6bu5P3Tg0YnuEfflFwB3sLVuAYq6BkfgygDAVey4Fzs+24iXv5aqqipf74fZbH7fI6Ao6v/y+THW0O8NrQCXsUYuLC5i0YLFT1g0Y3ECi5PQ3+Xo9nZ5DQiChKlUKiZBKpW+LZNpIk82lKb0dpVdfXpvPzy5tw/cgz/A4LN6rNmp0aaDR+DBjVI4d0wBPx7N/63OyUXwXmOw263JWPODPB5vKi4RCC0n1R13223QcckEroum4fuddrjtckLPdQd0XdLD6e+FzyutggecdJZBmk2dgdvGUFdbG6LX669zOJzpuDTKzXr5kWuntdB6TufqbEUu3HGVtjfUChBh1u59iJK+ySilzs7kcNvDwuJm2e0VWVKtNhC3/k1lpWO1SqnoEggEEbg0CvthdqjwgaDRckLQdrRK0XGlWa7IpIZP9uSiNybN35xAXZuTk7NjF412pq4OO0OjqQk7Q6LXjGOxmHLz8/P66HR6GC6NwunmEOP6qL3LIQXm9m3p2FvIb+NQxSvxtBcOJ50jEgoGUlIYLKez3KnS6NLxlBetuviwSCRqioqKGjMVgXmUSVpaH/1o4aVY+LBmjZuVy2kT8SVFeNoLLzU1iMnYDVwuT2+32U5pzCWbPbrRaJytKVbV8vlZTeHhSybz+RlzMPktT+4VFis+Xb3Asqo8RLT8y8y0Pdq8vPwb5TU1wTabbZEnHxMTTPwqMWGQSt11vAQxq62lZWUqlXxDcbGSKxGLgU6nsVkMRjiTyaR4G/4fEpHocLFGe8RqtcY7HI45JRrpDGYKfTAjgwNqtabZYNA/EYvFoXJZwXc52fxOBo22GLeOm3fzJJIutc5QgW3DF4jZ1MTPygI2izWE3d+QlSuWStOSA9lpTIiJiZmHeybG1ri4Gdgk/Y4K53GtVtuUzmbd5WXueVhQUADCIt0yNjPl0NbEhPN4+ZvxTWLiQrlMjsqVKsfuXbSejHR2v0KhGCksyG+m7Ux2x8bGTnhrxiDdK6qXFRUBbecOSE9L65QVFaLYNP3x8fGvPkzjYh4xmKT/6KwfdabnPvfzSA4bwtXpdPB10vYh7Bo83SsRQ3Iy9ZXn4D8hBpPn+dBnbvCZFTCfpF50YMrQFgioD/sTS3nGD4yJiFhYglieMxmMkdTUVMBejpCxh5vrNY8H0ufTo8ktERBwavUg+cyax5TbsTDpwtoX/pXLW/0PrhggkAgf77OW5ctlRZC0PQlkcgVkZ+cW4vb/x3fn7G2Utiig/BIH5JvrgdwWCeSOaKDc3+j9/c5nlHUtPL2fUa95yGalAZfHA6FYYsDt44A1c0qAOfQg5edYILuigNweDeRr2IJ3YiHg0MoO4obAuZ6yIqlwk16j/AN7FYM4r7DG6x0PPiFTFwTUrrg7+dd48GwP+UokUG7FeCeY1LBq2GdzUAJeStCrlT3l5RVQIFN24tI4mEXw9UuZE0/KW1DrX/3JDT9ZyGOSY5nL37Skkbh2+nq8ioBoCreUlZaA2WwBgwmBbIksEk9NiBU+24LisG/Pf8EUr4LhtBnmmvXFPWaTcXQBowk0BvMtmc76AV7yZtTYbIHOcntemd0GlRUOcNqt8G11NVhKbLD/QC2UOircVkelAEGqp+GWf0Ag/AUVLJ/81QCJnwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Tree_Data, Index):
                try:
                    re_mes = Message.RE_MES([Tree_Data, Index], ['Tree_Data', 'Index'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        new_index_list = []
                        for single_str in Index:
                            new_index_list.append([int(_) for _ in single_str.split(',')])
                        leaf_result = [list(_) for _ in Tree_Data.Branches]
                        Result = []
                        for single_index in range(len(new_index_list)):
                            try:
                                Result.append([leaf_result[_] for _ in new_index_list[single_index]])
                            except IndexError:
                                self.message1('Out of index range！{} List data is error,the original data list start from 0 to {}'.format(single_index + 1, len(leaf_result) - 1))
                                Result.append(None)
                        return ght.list_to_tree(Result)
                finally:
                    self.Message = 'Tree data values'


        # 长度转树形数据
        class LenTree(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_LenTree", "D11", """List length to tree""", "Scavenger", "G-Data")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4285e0b0-1f30-4827-9483-7e0b074b16f8")

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
                self.SetUpParam(p, "List", "L", "A Set of data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Spilt", "S", "Divided by several sets of data（If no input,then converted to a single tree directly）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Tree", "T", "Split the data（multi-tree）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.num = None

            def RunScript(self, List, Split):
                try:
                    re_mes = Message.RE_MES([List, Split], ['List', 'Split'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.num = len(List) if Split is None else Split
                        New_list = [List[_: _ + self.num] for _ in range(0, len(List), self.num)]
                        Tree = ght.list_to_tree(New_list)
                        return Tree
                finally:
                    self.Message = 'Definition length tree'

    else:
        pass
except:
    pass

import GhPython
import System