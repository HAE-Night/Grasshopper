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
                                                                   "RPP-list下标取值", "RPP_list_values",
                                                                   """列表根据下标取值，取值下标空格间隔""",
                                                                   "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "列表输入")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "取值下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "获取的值列表")
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
                    self.Message = '多下标取值'


        # 列表多下标取值
        class Subscript_Value(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-多下标取值", "RPP_Subscript_Value",
                                                                   """多下标取值，最多取到六组数据""", "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "原始的数据列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Index", "I", "将要取值的下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "第一组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "第二组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "第三组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "第四组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "第五组数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "第六组数据")
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
                try:
                    D1, D2, D3, D4, D5, D6 = (gd[object]() for _ in range(6))
                    re_mes = Message.RE_MES([List], ['List'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        index_array = self.handling(Index)
                        origin_data = [self.get_value(List, _) for _ in index_array]
                        output_tuple = tuple(origin_data)
                        D1, D2, D3, D4, D5, D6 = output_tuple
                    return D1, D2, D3, D4, D5, D6
                finally:
                    self.Message = '多下标-分组输出'


        # 列表切割
        class List_Cut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-列表切割", "RPP_List_Cut", """在列表指定下标处切割列表，树形结构输出；
                （原电池最后一个下标不做参考，已改）""", "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "需要切割的列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "切割下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataTree", "DT", "切割完成的列表为树形数据")
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
                    self.Message = '列表切割'


        # 求列表极值
        class ListExtremum(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-列表极值", "RPP_ListExtremum", """求一组数据中的极值，{1:最大值，2:最小值，3:平均值，4:求和，5:累乘}""", "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Extremum", "E", "极值的类型")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "极值结果")
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
                    self.Message = '列表极值'


        # 列表数据删除
        class Data_Delete(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-删除列表首尾值", "RPP_删除列表首尾值", """删除列表第一个值
                删除列表最后值
                删除列表第一个和最后的值
                列表的第一个值
                列表的最后值
                """, "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "需要操作的列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_First", "CF", "删除列表第一个值之后")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_Last", "CL", "删除列表最后一个值之后")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Cull_First_Last", "FL", "删除列表第一个和最后一个值")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Frist", "F", "删除的第一个值")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Last", "L", "删除的最后一个值")
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
                    self.Message = '列表首尾删除'


        # 树形取值
        class PickingFruit(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-树形取值", "RPP_PickingFruit", """取树形数据的分支，输入要取的分支标数""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Index", "I", "树形数据的树枝")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D1", "D1", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D2", "D2", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D3", "D3", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D4", "D4", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D5", "D5", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "D6", "D6", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R1", "R1", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R2", "R2", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R3", "R3", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R4", "R4", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R5", "R5", "得到的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "R6", "R6", "得到的数据")
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
                try:
                    re_mes = Message.RE_MES([Index], ['Index'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object](), gd[object](), gd[object](), gd[object]()
                    else:
                        Index = 0 if Index is None else Index
                        origin_data = [D1, D2, D3, D4, D5, D6]
                        available_trees = [_ for _ in origin_data if _.BranchCount != 0]

                        single_data = self.Picking_Fruit(available_trees, Index)
                        result_list = single_data if len(single_data) == len(origin_data) else single_data + [None] * abs(len(single_data) - len(origin_data))

                        R1, R2, R3, R4, R5, R6 = result_list
                        return R1, R2, R3, R4, R5, R6
                finally:
                    self.Message = '树形取值'


        # 树形数据处理
        class TreeData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-树形数据处理", "RPP_TreeData",
                                                                   """树形数据处理的问题，B有多长A就会有多长""",
                                                                   "Scavenger", "Data")
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
                self.SetUpParam(p, "A_Brep", "A", "A的Brep集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "B_Brep", "B", "B的Brep集")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_list", "R", "对应结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJHSURBVEhL1dVbaM5xHMfxvzkUkVMit1yQaHK/GyxKIdy4kF04bLKmKJu1G9EcQgkJEUXJBaUpFJpCQhjlUI453yzDzcL7/fv9/0/Ps2ZMz3OxT732/P7/Z/v/vv/faUkvMxs70YxZ3ihmjuILWlIfcQED0OtMx0GcwjqswWuMQZYRuIXTOIb7uIKl6DHl+IGz2Acf8gsn0DXT4HcnUYVt6MAW/DFWbUX5qcHq2CzIYCyMzVwm4zsmhqsusfrnqA1X/58bWBabMVNwD+/QBl/X6vqhp4xDZWwW5CbmxWacrA/YjqHeIEOwF/3DVfyd7Lv8VOBIbIZY0GI4L7kOVuFBbCZjMSr9zJ9UV8am2CzIYfhA33Y4NmM5zuErfHayH4dskLlw5fgH3vPTjIdrfmC4itmNA7GZbIQbz8UxzBtkJlxRoZe3cB4cGqvaA6txsrN1vRLujZFwpeUvRauuw3FM8EaaVn84zo6ju9QJtgIrewg7eI8VcB58yB04Z8Y3uwY32yM0ogxZbqefIWvxODZDLmMHtuIJ7sIzyLe1A4foKVwcLzEVWezYRfIpXKVxM1lNlgXw/DFWfxFuIo8Dx/YSNqAJ/q1DZ1G+oQ++jknIZQZ+wodkcfeeh2eQk+gQ+FYeJXZ4Buth7KAe1fAI6TYexd/QgDmwcleWnczHLli567wd3W2yv2YJruIZsu0+Gh5k3rMAz5qi/z8wi2D1Ht0liUeBQ+M/m0HeKHbs4A0+oyQdmBdwU/bdDl6hZB14brlEO/EPHSTJb3hUgJMPbzb+AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, A_Brep, B_Brep):
                try:
                    re_mes = Message.RE_MES([A_Brep], ['A'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        if len(B_Brep) > len(A_Brep):
                            Result_list = A_Brep * len(B_Brep)
                            return Result_list
                        elif len(B_Brep) == len(A_Brep):
                            Result_list = A_Brep * len(B_Brep)
                            return Result_list
                        elif len(B_Brep) == 0:
                            Result_list = A_Brep * 1
                            return Result_list
                finally:
                    self.Message = '树形数据处理'


        # 简化树形数据
        class Simplify_Data(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-简化树形数据", "RPP_Simplify_Data", """将所有传进来的树形结构简化至最简状态""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Data_Tree", "DT", "树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Tree", "RT", "最简后的结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAaXSURBVEhLpZVrTNvnFca9VlPupcQEfMN3TDBgCJBq6lK11dZVyqZ0kSZNmjZ1E5PWdduHatrHap20buq6ZYuyZFubi9JEhBCCAYPBEG5xTQKkhJCQcMcYHGMDvvx9xWA/ewzuVm37tld69P457znnd855X0CUXc/Uncl/7W6LstZuVtTaWzS19jYp9/21duvB2kGbnjL8S3Yrfaw59MnjrudOWwt3xg6albUD17Vv/uotcXE2t+hLjiv73ouPiYElPbBSCazWAOvlwJqMex4QKgbCRynaM3uoZMe+pgD8R/hNm9fEeDmwIKWM8AwY3Wd+XVjD/Dm5T/sUbjzJR4SQ2BMt4rNHkFg4SpUjPi+jCrDhKsXGUg1VzW8TbRLE5+T0qeR3NeLTxYg+EiM6LkPsQRmwWIWRBv2Hon37RAWe22We9BMTIg/ViE4UIDapIKQUCSchzgomyufPB5hIhfiCgbYSJObpMyfdAcxVM0aL6MM8Qgh6wK5mTLhXLzsj2rtXJHF3K56mJ4w8PMIOKuiso+SITWVARUgsvooN93eR9PwYSd87SLjfRHS2nL57kZg1Ij5TjejjQgLkLLCSkyBgQoWhy3vPiPbsEcmWOiWerfsyRO4rCTEw0ETAYQKKsem/iPSWH/+5krFpCM5fQpjQIjFtYpyUAB33GoTvGYD7YgxeyD2bAciXbTrP1lgJAQbOkE7jHNW4BJuBG9l0QCqVRiy+SfE7nTVyeecvwj+aiZEQUM4c5RAcBQSo4LikOZcBKBYt0pXNETXCIzq2Z6A0bLUKqaQ3mwYQhCiGBy1w9F3AomsJsQSQ2EhhcsaDMdvLiHIC0QeVEIYVBBQC4xWwX9D8TbR7t6hwsVW5sjmkR3ioCJHPCBhVITxOwMZKNj1fZ3QLd7rfw5h5N6Z6j2Jq7BM8GJ9Ec3MT+uqqCNAjck8DYYgaNAIjGvSfff7vGYBqwazwJgfVPNAiPJxx1EEY4TP0tWbT76xUKolk4BYv+EdwO0ox2myAo94AVy9f0GcscLgIwl0DQv3sgKDes4qPRLt2idQLjQR8qoWQ0Z0MhKMaUWJ9+AWsLNoREDiOZJaSXakEx+T6kBdajPg9djxkYHI9Qg4tgn064I4ePX8p+HgbMHdd4dsY0CB0m5U7KDoKd9mRIwfuWwWY6H8bj0a74HR5EYkB6S9c8qqrB0/ZQeQui3MQwBzBHi3wqQ7df5ZsAzRz1wp9CTqF+gixZzpR8sK/gqS3AVsBG7zDJzHV8hzGLF/Hw8G/IhIJZ9MDntUNjFq/j8CAlHFFCPZrEOhSAf0qdP0x//w2YPaqzJfoUpKsQ2iAFfTmIu48nU0BbCQEeIdO8vxZuC0i+B6+mz0Blj0CehrfwdOOgxBuqxlLQCc76NOi6w+yLOCK0pfoPoyATcUkBPVKEZn8d5LM2krGEXFd5fOt5S9f746Rs3o8tQTLxe/BYz2E8ICe8Xr429XALQ26PpAQkLOLAJ0v1iaF36rgBZUjdEuO9R7+TfFPYmsnz3+tjM3jDaK1tQWd58q2Cwv1aODvUmO9la/IpkHn7zMAdjD1jxxftFXG2ZVTOnYiobMW7u4XMf+oHcsrAlYDCfhDVDABj0/A+GMnms03cO3UK5htyIXA5MFuA2OLsW7hn/0ONTp/K/4ckOeLt5eyAyP8ljzOkKPqq0SAc11sKsD91h/A3vY+elpOoct8Cm3176Px3HdgOy2Hs0mBcJ+RhbH6dhmrl2GtSYm01YDO3xXuAGY+1vpiFhPWzUoe5sLfUYxAt4kBUgSt+fDbtFhuVWO6Lg+Tl/dhul4OdwuL6JAhlDm3qujDAjvLWKAeq9dl2GrMQ8e7B7YB2rnzh1cjN4zwXRVjtf4gWyyBv81EmBRrjWKCjAjaTBA6uTcfQsAsRrCdj8JawYr1WLtxiEnF9C1kTAlWG8qRbi5F92+kFzP/MmX9H+iWYeblfLQHgU/ECDUeRuhmCQLXWN3lPQg28ALNxm0Fb/KVXH0O/isHaFch1ER7Izuuk2D90n6snaf9kgQwF+P0W/KzGcCXX30hv7P3T0WYuSDHfF0JXOYXOZKXsHSzAq7raiw1lWHZ8lXq2I6aq2nXwtWgx5K5hr60tRyjfw2cV7SYOS/DqbcLkZu7/ycZANezJw8ekjqrqipSL79yLH38+OupN779rdSJN775P5Sxf67jqRMnqC/Yv/H619KVR0zJZ3Y/38HEyp38JFAvUT+lfk797P/QL6gfUlqRSCT6J7sj9gfD4fxFAAAAAElFTkSuQmCC"
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
                                                                   "RPP-树形修剪", "RPP_TrimTree", """树形修剪插件，Depth为树形修剪深度""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Data_Tree", "T", "待修剪的树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Depth", "DP", "修剪深度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "修剪后的结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH3SURBVEhLzdVdaM1xHMfxfzJWHkJzs0RZ7pDH9pAbI5oapbjZhVFCIknTNk1au9B2RS6EtVZau6DIBbdu3dnFmufigjw0XKAR7/fvd/6cc+Zhp/O/8KlX/9/3/Nbv/+v38F/yv2c2dqAdR7EWFcgk+/Ae3/ESr3NtX1Z22uBgvVjkD2QD/K02VGVkBRzoSKh+5TruxmayFadjs/RcxcPY/Jm5+IbbuA8noOUoOS/QHZsha+DADvgBV1CHcRxCyXmKM9iJe3DgURzAAqTxBcdj8+/ZhpOxmdTgCdIluIlNKM5i2L85VL9JFY7hMdLB7uSeY7BvFv6UQbzFjFDlZR0GMIEvuIT1eICPaISpximsDFVhuuBEvIAFuQA7HMwjOB9p9uIVmuFx9O+cgJt6C2dxEc9h334UZDvscOOKswR9sD81DJfIFzzDI4zgHJZhUrwUXvv8uHluogP6GejAFnxFA5rgUs7DP7MaDnQZnhhnZO0xbEElTA/SF37GDUw5u+AZd/f74QXKj0vyCW6ia+zL3fgTKCnTcs/iHISznxOqOAFrP3KZxDsxFJsh1+ANziT1cLarQpUkC2G9J1QZxM30K5mmE25yuvllxUH8FLeGKuYNzsdm+ZmOd/CmzoQnyOVZisyyGw7qsfTpfcg8/qs8jI2hmlKS5AeHHXx0WNKFhQAAAABJRU5ErkJggg=="
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
                                    Message.message3(self, "修剪已达最深！")

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
                        self.Message = '修剪深度：{}'.format(Depth)


        # RPP_数据结构对比
        class Data_Structure_Comparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_数据结构对比", "RPP_Data structure",
                                                                   """对两组数据进行对比，一样则输出True，反之False。\n注：此插件仅对数据结构进行比较，与数据内容无关""",
                                                                   "Scavenger", "Data")
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
                self.SetUpParam(p, "DataA", "A", "第一组对比数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DataB", "B", "第二组对比数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "verdict", "V", "对比结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO2SURBVEhL7ZRrTFJhGICPOu1i2rSiskWFt+wqlpQKpYKoEKLWIqYdJPBS5CXCLlLaxVbNwpVgqCV0k1HL5nJmtbJpNQubmyvtZssf/UtXrbVam2/fJ2dpqdhW/+rZHs45471857sc4j9/Dfr8+TMPFBWdft7znlFf3+OFbWnp8erv759AhfwZa9dKwldx2MBhh38KWxHai126dElvwc7tzwDAiwobFTekuyMjBVuFsqQAeHnJCV5ZnKH7ijPUFBKgSs8A9BZBKMYhU5CejvTx8Q0LWcKAjeK5QCYwQJbIgNiImVC4Yxtu4ItiHOJBXR0RtD4xAR62tLY137zb1HzjTtP923ebet90mdEUjadiRgVPg0NoNNpiVigLovjrOllsoY3FFthWoOtCZlQrM5T7NITF7VoVFdtlMVXqqJRBeDweXSwW37JarTH4mcuNOadSqQz+AQEPBAJBY3d393RPz2l+CVE+8MjkArYqV7BV2m1D921VbvC4xg12kZPh0P6jLweKDuWgVjsnmseHAq32vFqtnrocjZSzOhLiBcKvJEl+a29vT0RhM8KXzQatYhLskXsMN8MDRBwv0B0+8sJe9RfiBMKbG8m0NxKJRJ2UnAxyRTpIU8jXHR0dmWiO3RBBQj4fTFUXX1eUVXdWlJ0ZVF/dWXpE/9SoN7x9Zms6Q5X8GZlcnpGUvA6P+p1SmW6rq6tTCEViECUmf6m1WsNQCJ0bGQ1b8oofkOm7G0nFEDdtb7xWe7kC7SZve7XhuKCC88Ii2N8CgxaAXq8/qdFogtvbHqbFxAmgpOR4BdoHtOiVs6B673gwa90H3TcRdqS4QnZWJt6us6l6w5iEf3j8uCfxQhHYWlulwUzmZ4av/wd+bDw0NDRkowbT+exZUHOQgJoiJ3TI7FqKnWB3CgGZcjlu4D9QbQTwYSIMBoPCbDbX431tNBrz9hYW2qwWixGvAfo7kBMeAeq8go85qvy+HJXG7hZN39as3L5bVy68QHHOuM5IjHnQ3N1dFyWJRHDadLX2mO6sseSY6Ye6ExeM+QUnjoawpZuXc1JVLM4Glf5kqRQ1dKHSCbw4+DRixw25xyMfeJ442YfJCqZDboo35EqnQN4Q8bM6lQZaJR32ZNJBljAD8nOz8ZT5odwB8Cf3x3dnJLnxyjXSNf7QcoqAe3pk2ShWElCWg9ckDTcIQbm/R5pSycFroJAp7JKjmypNhXPlOtxgDpU+NqXl5YHN16++QklZSMlYovmPpFJ/H2o3/VMQxHcjpQfzJyKagQAAAABJRU5ErkJggg=="
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
                    self.Message = 'HAE 结构对比'


        # 数据清洗
        class Data_rinse(component):

            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-数据清洗", "RPP_Data_rinse",
                                                                   """去除空值和空格值""",
                                                                   "Scavenger",
                                                                   "Data")
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
                self.SetUpParam(p, "Data", "D", "需要清洗的数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data", "D", "清洗后的数据.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGpSURBVEhL7dIxSAJhFAdwHYSSC3ELbfOGSAfdDAfFQUKhJbEbWhLEwaDFJg2kQRwc6xzEa3VqklYlEKHpBEXEEAXDDEflhtNe3/U9ELfsbqp+cNzd/717H3z36f79Hkaj8SiXyz2FQqFrjDRjiEQit51OB4bDIbjd7ivMNbGXyWTqQPT7ffD7/VWSbdGSevuCIIyU4ZVKRXa5XHck26Yl9ezlcvm11WpBNBrlyfsBjbXhSSaT79PpFMxmM4eZNkwm0wnZDkn5mYFAoI+xNhwOx0WtVlO2/Eu9XpdYlj3HsjrkdGTb7TaOXmk0GkAWPiMtetq5OT3Hcffj8RhHrpMkCeLxuET6zLR9M0wikXicz+c4bp2yaLFYBK/XG8b+jeym0+lnnLVmuVzCaDSCUqn0YbfbT7H/+ywWi5Pn+Rect0aWZRgMBlAoFCSbzXaMn2zGarWGRVHEkSvKfvd6Pcjn828Mw3iw/WecTudlt9vF0QCz2QyazSakUimRlFnapZLP58tOJhNYLBZQrVYhFos9kHiHVjUSDAYF5aSQ+w1GmjOQ65A+/k063SdJvTL9DOGD2gAAAABJRU5ErkJggg=="
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
                    self.Message = '数据清洗'


        # 数据对比
        class DataComparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-数据对比", "RPP_Data Comparison", """Group根据条件分组.""",
                                                                   "Scavenger",
                                                                   "Data")
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
                self.SetUpParam(p, "GroupByData", "G", "分组依据 list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GroupData", "D", "分组列表 list or tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "ByTree", "G", "分组依据所得结果 tree")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "DaTree", "D", "分组列表所得结果 tree")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIHSURBVEhLzdVNiE5RHMfxS4q8y8vCBkWxQSmKxayVFYVsWEgkkRA2bEyxkbKxmcU0FJJILBV5CSklFhKRlwUhQuTl+73dM/2dOTPzPLLwq0/z3P+5585zz/nf+1T/U0ZiEsZjiIV/kUU4hOt4gfd4g4c4hbUYi7YzFxfwqwXPsQUtZz2+onSxgVzEBAyYrShNbtVduEfFLEVpUrsuoU/GwE30hB/N31xe/4hvWS3ZgD+yGw4cxxx8aI6TLlj/DLtqBobCL7YSjxHPfwnbus4wpBPcKHMSccI8zMJOmMWwc9bUR1U1Fa8Q56xGnQVIRW95HOJ+PIPZhSlYhTSmazCdiPUTqGNbxgHXz9t/1xwfgbmD0cj/gbyT81ntPursRxy4AuOT6vF8uOZ+3gOzBNtxEDcR5yevMQrVgaaQfIe9vAJuttmHNH4Y0xCzCfEa8pVSv0Z2NIXIZXJwL8wDWL+Hn81n30tP4HxzDvEaT2EDVcuaQnQVxr2wg6zZoia1dGRcvli7jDqT4eQ46DJNh0lL6IPmftjfbqgP5iNsg8nvwGXtzRnEQbmuJi2PfE3PRJ6NSEuXzEZvFiIOyjXszmr6grOw723h28jPOY0+OYb8xL/xCXmX1RmBWyhNasdy9JuJuIHSxMG4B+swaIbjKEoX6Y+vhQ60FX/we/AWpYvK99Nm+KUKqarfY3pEF6ebo90AAAAASUVORK5CYII="
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
                        # return outputs if you have them; here I try it for you:
                        return gbdata, data
                finally:
                    self.Message = '数据对比'


        # 数据比较
        class CompareSize(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-数据比较", "RPP_CompareSize", """数据比较，用于比较长度和面积的取值（几何物体），也可纯数据比较""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Geometry", "G", "对比的几何物体，可以是线段或者是Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Specifylen", "T", "指定的数据切")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Closed", "C", "是否闭合区间，默认闭合")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Compare", "S", "选择大于区间还是小于区间，默认大于")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "G", "最终的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Excluded_Data", "E", "被剔除的数据")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAF/SURBVEhLzdVLKwVhHMfxKQs2LiXCxsJCShZEsbDwBmTlsuIN2FhZyFJJUexEXoKNEgskl1y21nIrCwvJJRTf38Oc5vbM86Sz8K1PzHPmzL+ZZuYE/60K1Pz+LVp9WMUlvvCJe5xjCb34Ux04gA4qu5jHYWQttIk2eDcGffEZ46hG2BSSA+QFI3A2Cn1hB/VaSDSD5MGjBmFNp6md9lCihYxcA97QjMxO8YToJUnmGiBbSKW7QR/qmuflM0A6EWsN7yg3W/Z8B+iOi3UD3YqufAecoJCeTC2mpmbkO+AOZTDVQovTZis/3wEPqIIpPIMFs5Wf74BbFM5AXWH/59/cfAccI9YKPlBptuz5DphDrB7ogwmzZc93QDtS6e35ijqzlZ3PgA1k1gLtoOtXqoWMXAP0Bm6CtSFoxyM0aiGRa0A/nA1DO+vXaxINCLP9HjxiAN61YhvhAfToL+MsshZah/UV7aobi7iA3vW6xtfQDTGLLhQtPZl6TmJPqL0g+AZkcd0ArTjZVQAAAABJRU5ErkJggg=="
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
                    self.Message = '数据比较'


        # Python列表数据转
        class Data_py_listdata(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PY列表输出", "RPP pydata",
                                                                   """将Python的list类型转为正常数据""", "Scavenger",
                                                                   "Data")
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
                self.SetUpParam(p, "PyData", "P", "Python列表格式数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "GhData", "D", "GH数据格式.")
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
                    self.Message = 'PyList转Tree'


        # 通过真假值筛选元素
        class PickFactor(component):

            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-真假筛选", "RPP-PickFactor", """树形数据批量选取，通过因子（True，False）筛选""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Factor", "F", "控制因子")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "T_Factor", "TF", "正确因子数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "F_Factor", "FF", "错误因子数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "结果列表")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJQSURBVEhL7VQ7a1RBFJ7FFyk05s6d3eycUUFSiIUaBBEURBSx9gGptLAQ7ERFBTGFgiaFoGBjI+IDXGxUEoWIKbJ35krWrEUgIQEfYNaoP0K/mT2o140Ss2uXDz5m55zvPGbO3RGLWBCUNftjR31xoi/ISnEDm+cENN2RpfOxNb3gLjb/ETlp6TI4G1v9MrZUwe93HSjI/gyUpcPS6imvAd+C76XTp9jdCFmm3dLRZ2X1UWxzsixXIug2Co1GabSqrqoj7/IFbwfHcVq/VhBbBadVWW9hWRZwnvUi3gZEI7QdRWp5R5vYFKBccSe6nfaJfxCF/GmilI6wLIvYmR6IPqpXPzuQiTntu4pH1xbZFIA5dUE7joTVX4uEAlbvZVkW9SsxAwickAmdQ4fXEPBVpuYMSzKA7xJYwxzeoInXvrnY6TtisGsFSxrROdapIOwHMTAEWXOMXY0YFktR4Dg0w74I1osdQ+vb2ft3IDDBaebs/HdA+xR8wNt5AJ3hBC9Q4Bbu9SR+96G7K8yrYV9nP/yPwRmZ6D0cPQ/4AkkI/BAG5+hZoDWDzIFA2FDk/r8lZ6DAEBI8FKWNy9nUInwTOXwJPehwCt09USltZk8LUBJL0PUNDGwWye9hfY51RiV0iBXNQaVr9vnkUZkOBkNl6zLM4Kb/BNur61YHWzNA9/hz0RhvAyJrtqFoTY204KoUOkeyT8oWd7BJ4LPsxTVNFpJCnk0Lh7GmDSco4Vrw/JrrSH4X+y94Mk6wpHmE98i/QxgwijxSjg6waxH/A0J8B/SY9Ln2A+A9AAAAAElFTkSuQmCC"
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
                            Message.message1(self, "筛选数据不一致！")
                        else:
                            if len_factor < len_t:
                                Message.message2(self, "筛选因子与数据树不匹配！")
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
                    self.Message = '树形数据批量筛选'


        # 树形数据同步
        class TreeSynchronization(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-树形数据同步", "RPP-TreeSynchronization", """树形数据同步，匹配两树形数据所缺失的部分（类似于空占位符）""", "Scavenger", "Data")
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
                self.SetUpParam(p, "A_Tree", "A", "A树形数据，可以是目标树也可以是同步树")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "B_Tree", "B", "B树形数据，可以是目标树也可以是同步树")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Tree", "RT", "配对后对应的缺失部分的树，可能是A树也可能是B树")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANaSURBVEhL3dTrT1N3GAfww6UUCguQBtKxWi5WylkvaNtDbyBwNLaBpPrCLMbESBeWjqm4aDLr4kTmPHRjU6fZSdwLM0hczYwmGjExC9SRoc7Fni4z7BaVLc32Ykv6ihXG+H33tP4HtL7Zy1+ePM/n+f7Ohevu7g44HA5Jp9NJHMdt7+vr410ul6TX6yWVSvVaIBDQZ88Gg0EqLy+P2Gy2erfbfdxoNEqVlZWSRqPRdXZ2HjCZTFJ1dXV2xnpRFHdZrVZJq9VKXE9Pz3lqQENDA6g42d/fv9Pn84EGoqSkRPH7/R4agJaWFhCQIcDi9XpBA1FVVQVawt7V1bVgsVhQW1ubneEnYMput6Ourg7ZBFFKAEqQLcoEBGljUAKUlpbGKYGQXaCxsRFqtTplNpt5j8eTpgSgBIwAGwEKz/OoqanJzhB7e3tjtAgoQeGAtjYedEXPB7A7fcq6JiOK1RU5YMuWAgEaDQGVnO3elZAyeyGEL8cGMXVyv9guuAsDVFQ8A9ivhxQkjwFfnQabmxRb2x0FBn4YVnD3CHBLArsti6aNwnMEpmVRZ7THDC1tKCrTgHN2dEVb+XZUvJB7h+VgME/g6jnxzTe2xY6GAwjv6AQ3PbE7OjMRwtT7IVyN7JVNTm+wo6NjjcApMHlcZI/DMfz4DvDNGXD4aSiKp/SAHoyDzXwia03O/IBPx8XF7wZjeBgBpsfAZZLhKB5RceYk2I1xuf7l/zuwYYOZ3+RwpV8yNIMrLmOcqgCAy/UMUJWpUy6XmX9lR296q28jLE161tpcY1udP7B2YPPmgGBtF6Ctz/3OU2eObeL/TexPs3gE/8SOs+XPRmyZRHhtQFFRUfzBrQHh7qW9iH88gJtH9qSeXtvDryT2pTF7FOyLUcbyAWjjOPtzSMDPh4H7J8CuR1Ps3lt85tuhNO5EsHJ5JL8EOeA3ApIHqf42Vj4/kVq6czA/IPuhORwCdC/m7rzwwDqrM+jzutHcZEBZaXFhgdUJSf7l613BP2aHkbpyGE/OHoovfj8gMGV47cBS8vXz+H0USJzG6sVTk+xxaCf+ovOjj8Aujyl/z7/qwQI1J94jYDSzPDdsWVH2Acl3aeAHWL44Yl9SwguYp565swR86F9MDk7hCdUfnsN/T1xZnRM/P24AAAAASUVORK5CYII="
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
                    self.Message = '树形数据同步'


        # 树性数据插入
        class Tree_AddRange(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_树形插入", "RPP_TreeAdd",
                                                                   """将Data_b的数据根据path的属性路径添加到Data_a中返回""",
                                                                   "Scavenger", "Data")
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
                self.SetUpParam(p, "Data_a", "DA", "原始树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Data_b", "DB", "插入的树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Path", "P", "树形路径\n如果数据短为字符串，请先连接Path插件")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "return", "RE", "返回值")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMRSURBVEhL7ZVfSNNRFMc1JUuDIiqhoD8P88/m5uacuinKdFM3nTbYaCxhFmIESb35uKcefIhYRBBEUFFQTxVED/ZSbwk9RFT4UmgGBk4isrRNf33Ob3c6xQcjfYm+cLj33N+933Pu95y75f3HliMejxe2tbXZlLu5aGlpKbRarferqqq+OxyOfrW8eairqzttNBq18vJyTYJ0dnYa1afV6O7uLvZ4PC/a29sfBIPBA7KG/7Kjo+MW3/bpm3IwODhYjCwOSCeEXKyyslKz2WwX+/r6StiSn9mpEA6HCyAc8Hq9M9g01k+wIcav2CfmJ0WOUCi0kyz3RyKRUqfT+bCioiJVVlYmAZYIkCJgkiD3oFwdIAsOHiRQsqenR4PU3dXVdQj/ZyAQ0Hw+3wkS2W6xWMaQZQrCJOSLEkCMtZTJZPpVU1MzoOhWQCdsI9MQZB8ka8gvYKfwJ/FnmJ9jLCH7IjK/C5FOmpP9gsyrq6vf1tfX+9i/V1RR9BlNIXvFh2dke0zW8N/gP6YGh/VNQNO0fAhGKO575ElDvnwD8WXkhprL5UrEYrEd6tjGIdqbzeZvinAxNwDr0+g/Cvltv99vXXWDjYJCH0WG19I1QmowGKR7UgTTJcLmsR9I+MXtdh9Rx3TkI8l12vJmti1pwzv413p7e/foO0Bzc7MBiS5DMKsI9Rpk52I8vFluMaSOrAC9z1LIOUzaNIIvbbqATWAh2VNbWzsiBZbMc0lzDammyN6lk64Fuu2CbJysNcYzyp+StqVNz9MApbThU2SZW0ssN6FV08g1T6Hf0QjHFW0GyGEi60cQLjLeoCUDjE+QLs38EvqHIRiHSF6v3jHrBSHAEsUek3op6kz7QTQK4WfI/LKG/xz/I4E94jc1NVnQd5rs15VIuio7pxEmqKFTzi1D3kJua4k8Eli5+mMcHh7e3djYeIVAM2it//4IodQFUumetMz5ZR0VOdXRPwNBC6LRqLWhoSFG0ePyLux2+1VuaKfLHK2tre5EIlGktv890DtBUbfmD0cg/2gin3L/OeTl/Qa/hmABUAXaOwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Data_a, Data_b, in_path):
                try:
                    DataTree = gd[object]()
                    re_mes = Message.RE_MES([in_path], [in_path])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
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
                            Message.message2(self, "添加的数据和路径数据不匹配，请检查")
                    return DataTree
                finally:
                    self.Message = '树性数据插入'


        # 数据偏移
        class DataShift(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-数据偏移", "RPP_DataShift", """通过偏移数据列表的方式将数据一一组合""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Data_List", "L", "偏移前的数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Shift", "S", "需要偏移的量，不输入默认为1")
                shift_data = 1
                p.SetPersistentData(gk.Types.GH_Number(shift_data))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Eliminate", "E", "剔除不需要的下标（可选）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_List", "RL", "偏移后的数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Right_Scissor", "RS", "去除每组树枝最末位的偏移数据")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Left_Scissor", "LS", "去除每组树枝第一位的偏移数据")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMCSURBVEhLYxgFQx8YGxt7WVpaykO51Ad6urrH9PX1Pxvo608yMTHRgQrjBkZGRk6Ghobr9HV11xKDdbS1XwLxfyD7v66Ozh+gZWuB+v309Fy5oUaiAqCCAlMTk/+G+vrYsQEIG0AwkA8yXFtLC4yBvgGL6+np3QVaogc1EhUAJeR1dXVDtbS0QpCxtrp2sIaqRqCamqa/hoZGIExcR0vrGjB4QK4H4f1QvWxQ4ygHujq6a4DBswZosC1UiHhQX8/AVD4zlD853tzBL0yvNa3Mpj4hz3RRdJZ5d26rhyhIjb2WPQ9YMTkgt96ML63CtiAu3nRtZazFnfQC01PRWfqvPUPUb8XkmG6IybaMcPfXSXf00iQzmf5nYIxM1m+IzDDaHZNksjS7zPRZQqHhb/8orctxsXrPQhJNZgXEGU3yTzDSheogDdTX17PEZxgui8vW/RCdbnA+J9/4aWy+wbeEfJOHMVEG9wOTdW+FZ5ttSqlx1IZqIQ3kVlu5FWdbLg5JNdyVG2e2uzDJ+E1YmuHViHTDuyFZhpeCkvUeh6cZnwpNtmoOijRQhWojHqSVWoWHphvuS0k2PpeSYnw6Jtz4QGyW6Z24PMPXgfG6Dz3CNO4mR+s/DYw1XO8aoycG1UYcSC+1Uw1J1L0YnKD1LDFB70lElP7xknznyWGJBo/CknR+eoepv3ILUD2dHWl6NDjSqMo/X18AqpU4EFdgqh2fY7wxOlXnd2CE5t34RNNDOdnWD6ITTC9EpBs8Do7VeewTonXcP0nvSGiSSRJUG/EAWEqyBkebx4SkGdfkpVhMy8003xtXYLYiNdPmYGiC0ZHYTINLkam6z9xD1B5EpBqXAbUwQnSSBphCok2LItKND8Um633zj9bfHJdotSMgXD8nvdwyPzvZ/FBElGkxKJmGhoYyQ/WQBJjKfM2Scwtso6uyLBeHJRlNjk+yarO3h4R3p7m56nx7ew6wSmqA7uIY7qwkpwQol/ogL9lJPDvFKQPKpT7ITbGXyUx2AkUokYCBAQAzuxMn1npfOAAAAABJRU5ErkJggg=="
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
                    self.Message = '数据偏移'


        # 通过下标取树形数据
        class GetTreeDataByIndex(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-树形下标取值", "RPP_GetTreeByIndex", """树形数据根据下标提取的方式；支持多下标（树形路径的模式为{0; 第N列表 - 1; 果实数据}排列）""", "Scavenger", "Data")
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
                self.SetUpParam(p, "Tree_Data", "T", "原始树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "下标")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "最终数据")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASESURBVEhLzVVraBxVFB6fpbtz596ZNE1iC4o/xEdLbGOTZrPZjZvN7rzyggRBRAWloqEifaQpJm7Srd2mttWQR81zX9lNNn2YiNQqEamgRgk2WiiVVClSFH9UxSqUKF7PmY5ISBZF8sMPBnbufve8vzPC/wrekHCrOqCst19XGFy4KTDMCtUo/Sg4RHfbpysDNc68tVHK1DjdpCfY1bo3FF7W7mzC/2qGcgg6t4j/BnjBGGeFlX3UXxpy+jbtXn1Hw2kx1zuRK0L0YXNM5sYo4+Uvk4UtzznyjbgUrJnMIXrUke87pqwz+wsctqnlYQzTu7UkO1c3KfPgMOPuMPm5pEU8Guynfi3GvgcnXxgpmfteo7xkD9mJdzA7LUaf1pPsMzMl3msZygYjpqxTR9gTQP7VHGNcBSdlHYT7XqWXtASbBSfTmEX5AYl7D5JefZROwfk5KN1C7SmZ+3tkt21qKRonhFsCGUlpyKxfHRyhn2tRerH2JF6i3L2fXAYj02AsU52ReelL4iU1yhbg/X0tzi6i08AA5Vv3imW2uaVohDobSVqBv8HYcX1U/gCcpLGprnYSqU4qW6FsTd5O0h4YYI+D8QlwchKDwHK6QuIvG5+lsmUsGwqfWXVXaZvY6omQ1800u2qk2Tg4a/V10802xYI+kZsP4xqpm1R4ZTflZWHyW3GzM9z4Vm6+Gs9SJleH2Ow9JF33dVHuOShB1OK8NiI9UtXnXGtTFuHhLlrk6SQReOb9x+isv595i7YJtxl9VA6FhJtt2g1Aim31U4o1gmZa5ua4zGuOy9wdIftsyrIwU7K7OsPOmBk2A324DO8tgUFaFIzJD1Ql8pwWSR9id8L4nbUI0CwYuTlw9HZNRo4Go6xpSTQ2cChgGHZA00f1UTatxuj5aggMpu8K2gsmHQUWEcWhx5X7qobkDUZabgYnX0NUn5rj7F0tLj1kkbKg/ADpxEwxMCPFrMdq+gCzlP43QO51cZLTGBJux1pW9khznoj0ZcVh6SjW2mYtAi6+YJQ+Cb36CriW+DyHyE+lIXGbTVkMPcY85pvimpK9Yrc7LP3h76O8DsQDZejAqbFpFlBQWpyGIeIMRP9DeUTqcrWRHRuecubZlOWxZZcjH5S7AGrmNSegH1GaBENTVb3kMe8r0hHoyfPYWFcH6amHEQVlj8Fq+VBL0DTeN1LUj0K1jC2H4hZHAI1jTaFRF0ClM5DBddDGN1hrEFcajJ117yNXUOG1VhBsHu7MqqeFVbiXhCxDYQG3KI4rRH0NBPYJ7KRU+X7S5+mUOE4IRHxGT9K5iiPSBXDCMRg8B9413GHB5Jobk5MNRoIVwsh9DJE/2pARrFRL9oitKD7copDVeTXGvgv0Eldxi3gYFPxjcJBZvYJSzeDIW4ayAcWByvUNOvOsNZyQqja/4CiAJv5uiRB1EqU78btR/07e2ge3i7mlLxJXoJ+4tDFyzz9+DxYBavlXw1zt0nbcO3qcfauNsI2BQUnRonL2zflfoI7QXbA931OHlfvto5UHfhqzrY6lEIQ/AbiUx9nw0XgbAAAAAElFTkSuQmCC"
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
                                Message.message1(self, '超出索引范围！第{}列表数据错误,原数据列表从0开始到{}结束'.format(single_index + 1, len(leaf_result) - 1))
                                Result.append(None)
                        return ght.list_to_tree(Result)
                finally:
                    self.Message = '树形数据取值'


        # 长度转树形数据
        class LenTree(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-定义长度树", "RPP_LenTree", """列表长度转树形""", "Scavenger", "Data")
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
                self.SetUpParam(p, "List", "L", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Spilt", "S", "以几组数据分割开（不输入则直接转成单一树）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Tree", "T", "分割后的数据（多树）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEpSURBVEhL7ZXLSgMxFEBn4ScpKBbsQr9Hd0p94Qt15b7+iRsXioL+iwhFEBH0nGCGMG0nE2QWggcONMm9mTSTO6n++S1DPMLTn98pG2i/4wM7SnHCr8QrTLnGdHwFi7hAE29whKuY4gLsv0XjDrCIMzRxM7Tm40OM2wutAtxfE52gjRi3G1oFnGDJA3JxUxxjl5XFrdwJrY4s4BOauG9HC+do3F1oZVjHS3xGk15wEduwBl7R+Ef09DVrpmaMBuo7bmEX3J4PjLnNmqlZw0P07xo4wVwBudo3NN6asB6aNTOTBzQp9w5iQTp5EX5jTOx6irZDq4De66D3Su79WxQLyJfnKufdB/doXO4wTGEBmRhtuw8+cQmLWUZPh/s76z6w3/Fctf9ZquobPDFgj2Jtg2QAAAAASUVORK5CYII="
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
                    self.Message = '定义长度树'

    else:
        pass
except:
    pass

import GhPython
import System
