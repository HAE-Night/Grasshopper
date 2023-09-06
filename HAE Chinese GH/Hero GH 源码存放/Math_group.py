# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Math_group
# @Time : 2022/9/17 17:38

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import ghpythonlib.treehelpers as ght
import initialization
import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.parallel as ghp
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from itertools import chain
import random
import decimal
from decimal import Decimal as dd
import math

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:

        # 区间取值
        class GetSectionValue(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-区间取值", "RPP_GetValue(Section)", """列表区间取值""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("95d1de9e-2dd7-4ab8-bdd4-627c8493dcbb")

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
                self.SetUpParam(p, "List_Data", "D", "一组数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Start", "S", "开始的区间")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "End", "E", "结束的区间")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "返回的区间数据")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJ/SURBVEhL7VNNS1RRGL67oAR12aqNQbjxRxQtKgjcFBQkFKKrokVfSqFB2aICoUQdpslyxITmQwMJS1KLcCNBIkFO6jgz3pk7dz6cz3s+nt4z3ptGFkSrYB54OOed88z7nvO+z9WqqOI/w/lufuH+iPR1u7j/Zr/117zVz/23PcJ3uqN8zk65jcZG1Fx6aBX8H4CFZSBdBhIlIL4JGDli3l4d2nGCzlNFWtWeyAD0jjJT0+QeO7UD1A36LXNNB74lgXyOoxzJIGMBK7rASoxjdWObKl5PcOSKEpGERJ7WmMFhUhFXgMU0LbbPTuwAtZ4JZqQpYTkUJ9Ub4F4A8M8jXRQIRbeS7mQ8JTE+KzHoExh5LZDelMgUgMEAi2haZK+d2AFq3ePMIA0w9hF4Pgu8nAfu+mGFjMqrfk7OMbMgMDYl8Oq9gDsoML8oof4+4PtDgTT1VhRoANOfgaEZwDONvFnAckxATwEmnesmtZFelM1LfA1LvKAiqtBKTKJAHfjtC4YnmZGiHuoZgNNNsLiOEk0wbFJ/kwLBd6xwtdeamphjJRVHqeeSrhzWJaI0BzMrkKSh71qgvh613S5mRO1WrNFg17O0j0usUhxNAy1drFdpW+8w14Y6+9GurWKhCEeKXrhrgQNNqGvrscyZT6DbbvdaUbnjSxQ4drHcorTNV3j7MvlAJd2pU+7KkmXdwV1dpNc88LKcsqXj7wppT47Fs0lg/1EcUsqDx8tNo2+3fq/4n3Q0JiyFgbkloL3HSjY0/PIdaNqZTn6264kcvvGYeR129LGRjn759HAbO2HLKjjSXmruHJBD6tzRXn/EvNf65PDJy/yULauiin+Gpn0HydTOiw23agwAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, List_Data, Start, End):
                try:
                    re_mes = Message.RE_MES([List_Data], ['List_Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        Result = List_Data[Start: End + 1] if End is not None else List_Data[Start:]
                        return Result
                finally:
                    self.Message = '区间取值'


        # 根据长度得树形数据
        class GetTreeLen(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-根据长度取树形值", "RPP_GetTreeOfLen", """取指定长度的树形数据""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4866e292-44bc-48c2-9100-c206087be3d7")

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
                self.SetUpParam(p, "Tree", "T", "树形数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Length", "L", "长度，默认为1")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "提取指定长度的树")
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
                self.len = None

            def get_tree(self, len_list_data):
                index_list = [_ for _ in range(len(len_list_data)) if len_list_data[_] == self.len]
                return index_list

            def RunScript(self, Tree, Length):
                try:
                    re_mes = Message.RE_MES([Tree], ['Tree'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        self.len = Length
                        leaf_list = [list(_) for _ in Tree.Branches]

                        length_list = map(lambda x: len(x), leaf_list)
                        res_index = self.get_tree(length_list)
                        Result = Message.message2(self, '没有指定长度的树形数据！') if len(res_index) == 0 else ght.list_to_tree([leaf_list[_] for _ in res_index])
                        return Result
                finally:
                    self.Message = '根据长度取树形值'


        # 输出列表前N项的和
        class GeometricSeries(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-输出列表前N项的和", "RPP_GeometricSeries", """列表前n项之和""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("58421664-1b1a-4aea-9324-1ca080a9c8bc")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "List_Num", "L", "数字列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Final_data", "F", "输出结果")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMjSURBVEhL7ZTbS1RBHMe3hIiy5x6D3rpAnHNmzsy5eI6uSiEWFGwQSGVPCT2HZOJDIURPIQn9A1ESJFHQFR9iM6ygi7UtWNBezt7X1DQ11+k3s7Oh6+4WIfTSFw67v+/8znzmzO8341tvjQf6NqXcQL0M11+Tuvncw8Z5GRaVbfDrc42tgznbf2EoMFTHvQT3/K2DGaupWyT9gXLUPsusRhZV9XPSKiqDSRczHMaozdLNBxTuedg8zZM9lcRF0m/01W7S8shg08ScjZcDsoh0FrDBGDZZ2nTEYAKbJxmxWFwl4yJJKuY4imc5x2X4SylCr3/SyM0YNW7Boi5Ju6gSYEEjLK2bQe55mJ6oBEhi0p+GPF9f30ZpCY3b9rEh161PE/N2XCGXpV1UCTCpYJZFdCHR0bE1genRKoDehKpP+hjbIK1VShLjwRpASgIyAFiGbUq4ze0xbLRXBKikN6nifHWAeb8mYAlR2CbrWow4hyoCFNwjAFVUE5ADwDdVZ2mNfkxY7hle9BKA8RXDk9RpXwoAAcbqIF5VB66qgGUARFUym1D0xayCfyQN5wYvelzT3/CcDDbuzehWKKOSbFrBhQyi4TnaEI5Ru0VMIlUVwHSLRbDxKoLIM9FNyJiahV9PI695DkAjDBYxDV8I/9kijPF3vkAziEmkqgNgv6GwIxNwzAtQB95R31cAYir+kEeEQQ1ErTwVsxkATmB6WEwiVRPgITo6BgcpD6vk9RAAlbzjOY9se+dDx9kVRWQAIFOPbXv3E8vaM2ya28QkUjUBcUTe8gPkKSg8B5OvBJSU0kg3dFFOhmtUe4sQfc/jqIoH+H5XAvz1OVgJgDuldR7qMF8JACe5JoBad6MqvSjDosoBLzVtC7Rrdhlux3IA3EP90Kpr7qLJlqYjS37/cBbTdB7TibztDiX9/u1iECbpYpbLIoh6wgBFVP0OM11+t8ekJRRC9GBI06+Wf0FEp1f49T4HiyrAAWXEZp91a58YHENob1gjPUGknxIG6KlKtBC0bFAhndKqqaBh7AibTtsoMdtewBPExv4R190sh//rn8nn+wmyTP73tw7eDwAAAABJRU5ErkJggg=="
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

            def RunScript(self, List_Num):
                try:
                    Final_data = gd[object]()
                    re_mes = Message.RE_MES([List_Num], ['List_Num'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Final_data = []
                        for index in range(1, len(List_Num) + 1):
                            Final_data.append(sum(List_Num[:index]))
                    return Final_data
                finally:
                    self.Message = '列表前n项之和'


        # 随机数据
        class RandomData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-随机数据", "RPP_RandomData", """随机数据组""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a0a41cb7-3dfc-4814-8328-557bd222883b")

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
                self.SetUpParam(p, "Data", "D", "原始数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Random", "R", "随机列表，可不填（自动随机）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "随机后的数据")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJiSURBVEhLzdXZq41RHIfxlTlTcUQUGUJ0ynFBZB4zJONxzgWlk0QuJGUumYfMiWSKQpkuRCnccS3+BVGEDJEQnmft/R5nn73f7XXOjW99aq93v+/a611r/dYO/0vaYTgWYhkWoApt0KxU4gI+4VfejwafP+AMhuCf0gIHYScvsQNj0BN98nyjdXgB79uDTOmIR/ChNWiJhtmA3piPpeiGFfD+B3A6U+PIH+MzHGG5DMRG3MZkDMY3PERqDsORDIutbOmFG1iCAfD5nSjKICTT0pTcwgisgv30RUEu4VXuY6a4Va9hYmyF0BVOV2u8xSnUx4X5iu2xFUJn7MJpHMMoNM5JrMRZ7IWbww0wB5vxEa0Q44L6WiNjK4ROcGT9MQX3MA/G6+fwDD28QJ5gLVyPA7AI7a++Pqrhhe6xVZwuuA5HfAcW4D440itYj/ZwJi7CgdnfbMTU4SecmrQsx3N0iK1c4R2BmyOJ29xNYiH6AzWIWQQvJK9cKq6JU5FkPI5jaGwVJvmBWbFF3PdeKLWYZjFcTI8Gzx6ncj9c1Mtwqly3JJNgfxZfTFt8we7Yyu2ImZgGd8hNVMA4VS7yUyRr5pttyX2MOYr3KDhmfMj96zw6GkflIVeLUnGfr8Z5OH2eScY68PR1+gqSlLk7Ikvm4irGxtafWEv244FYFKfDLy35pmQcfH5rbKXE0/A7RsdW9kyAnd+NrTKxWO7Dmzfl2+VigW2D91uErkGmuMA+9A6HMBWekNZKP0yHu8W/zb9OS1r8UzmBN7CTxl7DH/FoaFbczx5c1obn1gxYRG7pMgnhN2L3geQRRszFAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Data, Random):
                try:
                    re_mes = Message.RE_MES([Data], ['Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        if len(Random) == 0:
                            index_list = random.sample([index for index in range(len(Data))], len(Data))
                            Result = [Data[_] for _ in index_list]
                            return Result
                        else:
                            if len(Random) == 1 and Random[0] == -1:
                                Result = Data[::-1]
                                return Result
                            elif len(Random) == len(Data):
                                Result = [Data[_] for _ in Random]
                                return Result
                            else:
                                Message.message3(self, "随机列表的数量要与原始列表一致！请检查")
                                Result = Data
                                return Result
                finally:
                    self.Message = "随机数据"


        # 小数点的精度分析
        class NewRound(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-数据精度提取", "RPP_NewRound", """数据精度的重定义，优化数据（四舍五入）""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e2412c4a-0c46-443a-9c25-ca033de8bd30")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Decimal ", "D ", "小数（浮点数）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Precision", "P", "保留的位数")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "输出结果")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Percentage", "%", "输出结果的百分数")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Per_thousand", "‰", "输出结果的千分数")
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

            def get_Internal_Icon_24x24(self):
                o = "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"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.switch = False

            def compare_five(self, carry, keep):
                if keep >= 0:
                    return keep + 1 if carry >= 5 else keep
                else:
                    return keep - 1 if carry >= 5 else keep

            def carry_ten(self, num_list):
                self.switch = True
                int_list_num = [int(_) for _ in num_list]
                if 10 not in int_list_num:
                    return [str(_) for _ in int_list_num]
                else:
                    for ind, num in enumerate(int_list_num):
                        if num == 10:
                            int_list_num[ind] = 0
                            int_list_num[ind - 1] += 1
                return self.carry_ten(int_list_num)

            def handle_str(self, num, acc):
                num_list = str(num).split('.')
                int_part = num_list[0]
                float_part = num_list[1]

                if len(float_part) <= acc:
                    zero_filling = '0' * abs(len(float_part) - acc)
                    extra_decimal_places = zero_filling if len(zero_filling) != 0 else None
                    float_part = float_part if extra_decimal_places is None else (float_part + extra_decimal_places)
                    return '.'.join([int_part, float_part])

                elif acc == 0:
                    change_num = self.compare_five(int(float_part[0]), int(int_part))
                    return str(change_num)

                else:
                    num_list_of_float = [_ for _ in float_part]

                    carry_num = int(num_list_of_float[acc])
                    keep_num = int(num_list_of_float[acc - 1])
                    change_num = self.compare_five(carry_num, keep_num)

                    num_list_of_float[acc - 1] = str(change_num)
                    keep_num_list = num_list_of_float[:acc]

                    float_part = self.carry_ten(keep_num_list) if '10' in keep_num_list else keep_num_list

                    if float_part[-1] == '1' and self.switch is True:
                        float_part[-1] = '0'
                        int_part = str(int(int_part) + 1) if int(int_part) >= 0 else str(int(int_part) - 1)
                        self.switch = False

                    float_part = ''.join(float_part)
                    return '.'.join([int_part, float_part])

            def RunScript(self, Decimal, Precision):
                try:
                    decimal.getcontext().prec = 10000
                    Precision = 0 if Precision is None else Precision
                    Result, Percentage, Per_thousand = (gd[object]() for _ in range(3))
                    if Decimal is not None:
                        per = Decimal * 100
                        per_th = Decimal * 1000
                        Result = str(dd(Decimal).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) if "e" in str(Decimal) else self.handle_str(Decimal, Precision)
                        Percentage = str(dd(per).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '%' if "e" in str(per) else self.handle_str(per, Precision) + "%"
                        Per_thousand = str(dd(per_th).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '‰' if "e" in str(per) else self.handle_str(per_th, Precision) + '‰'
                    else:
                        Message.message2(self, 'D端未输入数据！')
                    return Result, Percentage, Per_thousand
                finally:
                    self.Message = "科学计数（精度提取）"


        # 四舍五入
        class GHRound(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-四舍五入", "RPP_GHRound", """小数点（浮点数）四舍五入以及上下取整""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("0b6b166d-332d-4c95-95bd-b7f85482351c")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Decimal", "D", "数字（小数）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Precision", "P", "保留位数")
                accuracy = 1
                p.SetPersistentData(gk.Types.GH_Boolean(accuracy))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "四舍五入后结果")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Floor", "F", "下取整")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Ceil", "C", "上取整")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARVSURBVEhLrZZrTJtVHMarX7Z4+eKcic5Fs2l0xg/bMuOyaIgJ2YxGTMwSjXHo3FyM84ObxCCDFRnI/VJWroOB47bBoEDLegNsYStQCoUgXem49n6n3AcCj//z0qUhftHBk/ySc/558zzn/M9525f3H/Q0sWNjuP16ktAQdkJNJBPhBAvdFj1B+AkWcoloJ1yEm6gljhJbEguYJsq4WUhHiLsEiDBWeFw9CijlZjzey8QXxA3CQrC2vUI8tliAmTARbYSXGCfKCXYWWxY7ZCPBWjFE7Ce2VWwHUwQLYTuREnuJbdOjMygg9hDdxApxmtgWsQB2Tau52YZiCNayJmI3K2xFLGCNEHGzkN4i+ggnseXDziZObQx5vK/DwnZi4s+dUd99vn/f3j3ig28fqEmNvRiRFhv1zY2CrKjirKT3g4+GJOT/8EyVMOO95ptVn1QV50UKEuN+yoiPvpKTGCcsy80sKhGkN1QW53UrxU2G60KBtaqkKFBfWb6olDROSxvrV1vvSNClVkF6uwa5yQnsCm9W9i9nDpTlpqO+ogw9nWoMDw5geEAPk8GAyfFx+L1eeD1eeNw+uFweeDx++PwzcDg9eDA6gSmzDTNzS5A3iZB1JVYRtA0p9dtjz+an/Oa9mpKA7rudmFtY5gw8vgAWl5axvLIKN5k6nO4NHG7Y7C4YRx5geNgIMwV4/QGolAoKiBvh8/ns/dms/OR4fWFWCmTNjfB4p2G1Ojij+YVFCgvAYrHDanNwdZvdidGxCQwNGTBCITaqswVoOtTITrw8J0j69d+3K+/3yw0lggyIblXDRa2wWGxcO+bmF2B3uLi5xUohFDBlttLK71PAMMbGJrlgp8uLfp0OeWlJEKbxDwZtQ8pLupRWLsxC9fVr3Aq5bXv9tBsfN2bmDJvNCZNpjGvNfSOtnlrFzsLjDVB9FGXkkZ0QHRG0DSk/IfocCygV5sBM7fAHZhGYnecMrGTKapNTVs68t7cPPd1adGu6oO/rh66nB1qNBmqlHLdogcL07NigbUj5/KjwigIBinLS0Sa7A+29TqgUMiglzVCKG6FoboC8sR6yhlpIaqvRUlcNlVQMuYjNK9FCyEU3oVWroRJLZpr/KNr8P5F55uRzdYWZLm1rC4Z6NRjUdqGrXYF+TQfUcgnUMgnaW5po3AJtpwqdSikMg3r8pddhYtQEPT1vnhzHwsI85n1O3JOKHna3ije/dIILkR/Iq4rWLaYhrK+vYW52Fqurf+Ph0hLmZgJw260w9PVg3DAIo14L06AOXrsFPocVllEjjAM69Ha0QdFYh7pruStFqfGGoHVIhXHnzylrSqFTyaFVtaK16fYabX9WVFHiuFWSN1ImSOspSObLribEVKfHXBDyz5+O/zny5I/ff3b8y6+OH/3wo8Ovv3vs1V1vHH7+qRffefOlXUHbzbp46tMTZz8OPxFxaN+RQ7t3vEafEC9QmX1JsB+//yEe7x9yo/Z81vR4yAAAAABJRU5ErkJggg=="
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

            def RunScript(self, Decimal, Precision):
                try:
                    decimal.getcontext().prec = 10000
                    Precision = 0 if Precision is None else Precision
                    Result, Floor, Ceil = (gd[object]() for _ in range(3))

                    re_mes = Message.RE_MES([Decimal], ['Decimal'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Result = str(dd(Decimal).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) if "e" in str(Decimal) else NewRound().handle_str(Decimal, Precision)
                        Floor = math.floor(Decimal)
                        Ceil = math.ceil(Decimal)
                    return Result, Floor, Ceil
                finally:
                    self.Message = '四舍五入'


        # 数字格式化
        class FormatNumber(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-格式化数字", "RPP_FormatNumber", """格式化一组数字""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("37069692-3482-4366-bc73-3060444025c4")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Number", "N", "数字")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Format", "F", "格式化字符串（00，00）")
                DEFAULT_FORMAT = "00"
                p.SetPersistentData(gk.Types.GH_String(DEFAULT_FORMAT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Prefix", "P", "数字的前缀")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Suffix", "S", "数字的后缀")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "FormattedNumber", "FN", "格式化后的数据")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVJSURBVEhLvZV7bBRFHMdn99qiVKSAoMiztBS6e7f32MfM7h4tj1oTI9YHBVvKQ4pGG/1DJYIJUilKeASwags1NUgft3d9QxFsJRoV/cP4n41/CGgK3F17lHu2PSj1ztntegWqCf/IJ7nc/L47v52dme9vBtw/4nEy2eXflOwKv6wrE/AhZOvjULkeavRB+Og1JB9yI2mrJnTFUg2u0O6kxgFBixO0B9IIJVgJlNBRXZmAlxMq+lgY9bN5U3UJ9PHizl5kz7uMpH2R9HQT6I4tJpyD3UCJrNO73IYrmg5ao3tWTQEzbBbLVgvDlDIMs58yGquLWPYRHw8PXBHQHrcNFesZwMPDI+q/WxCLPIK4QW2TDYFS4Iok+ozTGF0Emoff2wLAFAseAL+81Gg07s+g6cpuXuL8HOoJI7mz3wY/B01NhidKSmb18/CwmtqnDsBJJWqbrA9sBUq4QG2P0xRPIZXQNqLtxjfgTCxDVxNcY+H7bh7uvipJlhFWUNYhtGuh1XoRL82uYSiVeDjx4ytWyIDO2ByidchJuCLHQP3Aw3o6pvL3SaQjWESeHd2Q7IjQuprgDwjheUmaorYj0M6UMQyclZVVcCkvb6oXitsvCOKzWseW4QXkqdENpCtSApr8ib36/0lRBrKJ1mgdoYTumto4Pg7l9nOwVg81gig3c0CQq/EGb9OE9iHW0BF1EM5Q7R3vmaQEM1I6whThCFWB9lHNDXfjYeFeLyv4Ve/rEvAK4ge9vExfhuJOt5mVwan4/MlnB2fjD/0MO2mt3u022m5WpO0585qFWlqOXVRuMplc2TTdvRGhOdc5ePgqD3dim44VFeYfm2ouEtBGTcTgGdQkNQ9xeqjTcF1ObgpW5prNaTaaXmE2m5czRuOWDBP1yi+CjAKs8NswL3YM2Pg6c0FBGszPZ7FNxwbATnLzY/VhaAg8n+y4XqG2x1FCWUmuwNepzX4G9MRTdDVBPws/9LDoVY/FMvOWDdYWQbh3vsV8pVeQ3gxB8W23gGr6KSoTdIxw+Kj4Prk1YrxjDwyOwHPkyZttxOlb1QYl9LQuJ+jl7It6KEobeEAQ5r7OMOlp+GiIFxYa1KX5k5dE9Rm2+lpD58hxQ+fNTw1KYLmq3T9kEdVzVm71ylx7Ia6rY8XFxdMQQl05OTnZkii2IrRMkCVUg5+9YJfETzgIX9JT7w3zkkwHk5m+mrWYimiaPp6fnz/dSNPf8TxPm2j69GIzK2TQ1FHsrnV482sok+k/j/Z/JxZLxb9JejSBeDxOxNavn1CEgZwcq8dun6mHILXOOwt8G39AD8dIcoZl0DTcSTjDJ0F7fKEu30E/L232cfCiHmr0ScsKfEiuusqjj+IATE46NZKb1DroJBzhOuAKJwbFNg03gLpgJr4oisk6Xzmi5k7HSzPDhivNZrOxuAeBb7N9bpvwIx7IMpakFpp4pBCbENu0NDZnxgpwOlYNDnpTycZgGekIbdK7YRyhClzFVeDLv449dPB8o3XB45X4LqjGe/DDEqPx1x08nxXgoMsvygc8t12b+PhIVHJsXtoz+Mp8i2wb3kW0RBXSGU5U/BjOG0+BlugXwDlUpisAT2DaVFzZAXwc+3j086AkV0VsQkv+ypwV2aJ4yItnEEPoQS+S3vBarau1JCWyimgeOmFwhNdosUZjeCk4F3sRz8SpVrWuJnBz6N1LnMir7VFe3LGZZbc/RlFfXebFJ4OivdYNxaM9CE0H9WHKcO7WGny/nwD1g7O1ZA11/btG3wHOQbOu3DMXOG7eT3gWWoA/juwaLQONwUUAAPA3c3wKhYQUHsgAAAAASUVORK5CYII="
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

            def RunScript(self, Number, Format, Prefix, Suffix):
                try:
                    FormattedNumber = gd[object]()
                    split_dec_list = Format.split('.')
                    if len(split_dec_list) > 1:
                        A_Part, B_Part = split_dec_list
                        B_Part = '.' + B_Part
                    else:
                        A_Part, B_Part = split_dec_list[0], ''
                    reverse_str_list = [_ for _ in A_Part][::-1]
                    pre_str = Prefix if Prefix else ''
                    suf_str = Suffix if Suffix else ''

                    re_mes = Message.RE_MES([Number], ['Number'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        last_byte = int(round(Number, 0))
                        replace_list = [_ for _ in str(last_byte)][::-1]

                        new_indexes = []
                        for index, item in enumerate(reverse_str_list):
                            if item == '0':
                                new_indexes.append(index)

                        if len(new_indexes) > 1:
                            for sub_str_index, sub_str in enumerate(replace_list):
                                reverse_str_list[new_indexes[sub_str_index]] = sub_str
                            new_character_string = ''.join(reverse_str_list[::-1])
                        else:
                            char_list = reverse_str_list[::-1]
                            char_list[(char_list.index("0"))] = str(last_byte)
                            new_character_string = ''.join(char_list)

                        FormattedNumber = pre_str + new_character_string + B_Part + suf_str
                    return FormattedNumber
                finally:
                    self.Message = '数字格式化'


        # 列表数字或字母
        class RangeSeries(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-列表数字或字母", "RPP-RangeSeries", """列表数字或字母""",
                                                                   "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("30b50d1c-1d86-46b1-8eab-1e5b2b165ed3")

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
                self.SetUpParam(p, "Start", "S", "区间起点")
                START_RANGE = "0"
                p.SetPersistentData(gk.Types.GH_String(START_RANGE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "区间终点")
                END_RANGE = "10"
                p.SetPersistentData(gk.Types.GH_String(END_RANGE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Step", "S", "步长")
                DEFAULT_STEP = 1
                p.SetPersistentData(gk.Types.GH_Number(DEFAULT_STEP))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "生成的列表")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANjSURBVEhL1ZVpSBRhGIBf7bAysqL+lBordrpz41pGbce2LmkHW1sRZQf+qD+V0UF0SGZluVpthaaZHWBugtXatdGBdtCBuxZ0UBGFgRZBRYhG5ds7M1+prAqhBD3wsO8x837zzQyz8K/oQQ7Rwy6jF9lXDwESyDpSLXYVGeQFPQSYRyIZomVdw1HymR4CzAwbP7dJ8DTeMbo/VxhLPlV2yrKGCsP2y7VBvfreZPMhafCcDShXInLlnZe/gjj61HsMDh3gZfMhadDM1ShcRoxxf+m0xrJGHJn/CoP79L/K5tMO7OtRrEA0epo6NOZcIxrPf2+z91uOLnTUybpWO5gxcMK8ptjz9Y/l4g/+jhQLa2vForrXUhs9taaqlH7xj9jh/UjP4IY+HsBB4uAW7217RE19mG+YeH8hS9slSH+LHusZ7YBsIINN0dH9tEo7hFt9RUOn+pJZ2iZms9CffnLJaq1AhJKcJAmLFElyS5I0Ry8HEmnzFUVM8y1haSvMZnP32FhplywLhZRGkpLWUEHEIFEQXIqihImi4HI4xvRkrVZ0tACd22PcOHmKLPN7WKkZjuOiBEHYqcY8z2eKokiPJBBa4FikpXoxSwOwWJQwWeQzWdoMDTXQArvUWOT5PXQ1g7RGCxyOM93UHYRb/ctoz/QcA7HZTP3oVqeztBlaIJQWKIiLixvN81yeej9Z6w/DE33CsKRXXyMSqv3Rtkttfrfi45XpiiJ6TCbewErN0CJ2WZaKRY6zsFIrwue6e0fYqusjEqrKWCkAesBLFUVaS7c4npX+DsO0R7ujLE+ms/QvSHVHQ8ZNEdKvCDDWPh42lkqQ5hUhOdMEyqxJWo/sbd0yO8S2zvo7ByVxEizNitWOVRWsk2HNKRn2Um99cYs/sbyXleD5iVDyFWFBGsKJOoTSbwg5VQhL9iKco55q6kmEdacRzlKsmpyJsM+HcKYBwV2PMH8bwrF3CJeod+h5FptOFNb44S4ieMnlTgQP/d4gC2sQVh5BuEWxapoXIf0aAn3aNVfk6gOvU3yNXEbnnv2B8IDigreH2HRi9+2VcPSNEw4+dYJtRR5kP8iG3BdO2FyeA/ZNByCfeqopB/ZDimv/n9y+wQVbL+Zoxx5+7oSkVS7IupcNx6mXUZHIpv+3APwCrn4j2F02t2UAAAAASUVORK5CYII="
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

            def is_numeric(self, s):  # 判断是否为数值
                try:
                    float(s)
                    return True
                except ValueError:
                    return False

            def circulate(self, start, end, step):
                # 累加
                List = []
                if start < end:
                    List = [start + i * step for i in range(int((end - start) / step) + 1)]
                return List

            def RunScript(self, Start, End, Step):
                try:
                    List = []
                    if Start and End:
                        if not self.is_numeric(Start) or not self.is_numeric(End):  # 判断输入的为字符还是数值
                            if Step.is_integer() and Step > 0:  # 判断输入的步长是否为整数
                                if self.is_numeric(Start):  # 判断起始值是否为数值
                                    for i in self.circulate(ord(Start[0]), ord(End), Step):
                                        List.append(chr(i))  # 将得到的值转化为字符形式
                                elif self.is_numeric(End):  # 区间终点是否为数值
                                    pass
                                else:
                                    for i in self.circulate(ord(Start), ord(End), Step):
                                        List.append(chr(i))
                            else:
                                Message.message1(self, "字符列表步进必须为整数!")
                        else:  # 两个值都为数值
                            Start, End = float(Start), float(End)
                            List = self.circulate(Start, End, Step)

                    return List
                finally:
                    self.Message = '列表数字或字母'


        # 物件快速编号
        class Number(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-物件快速编号", "RPP-Number", """物件快速编号""",
                                                                   "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8eeae662-8fab-4d06-8abd-e2bd5874ae4a")

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
                self.SetUpParam(p, "Object", "O", "需要进行编号的物件列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Start", "S", "编号的起始值")
                START_NUMBER = 1
                p.SetPersistentData(gk.Types.GH_Number(START_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Step", "N", "步长")
                STEP_NUMBER = 1
                p.SetPersistentData(gk.Types.GH_Number(STEP_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Format", "F", "数字格式化字符串")
                DEFAULT_FORMAT = 'A{0:00}'
                p.SetPersistentData(gk.Types.GH_String(DEFAULT_FORMAT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "FormatNumber", "T", "返回的格式化数字")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPYSURBVEhLvVVvaFVlGD/NsLy7c1NIW2Wj4Rr3nPfv+Xfv2Y6NrWATJv7JG4QSJTIoGwh9KYkuMdI+RFFRRF+iwawMLaREG6QfZJgkFImhBVaUyJyCiR8q9PR773nu7u6GcPrSDx52n+d5z/N73+f5ve+s/wWtb8i2loM9kbElewPfKluLKLUAfX19t/OYLyO3ERWryeTJqyN3oLi29ee1ibH8VP81a3T1UkotgGDsfcH5n0EQ3E0hy7btvFLqGa3Uac75ZgrXkfssGmz9CQSw/DcDV25FIIRYwRmbkUJcZ4xVKGwVi17seep5V6vjINhB4TqqBGeHEmP5E/0ztyLAxy8zx5kMAj2Ev9Pz26GUPAjiUXLryEKQJMlt3LEvguRNT8pQcJag2AZKV6G1/BKxZ8mtIwsB2jOI9iTo/zHYcSXEeXMaSlcBgs9BsI3cOrIQMOb8gN1/Qq4VRT5TUiYgZnEc3+X7+ikh+HnJ+X6txTpaliILgZRsSxjy+8itQkr5GBR0PwiWGQKzBmp63MRpSYqsQzaQjG3BLsfnDhhFJVo2pqV8F6fcSeE6FhA8t7KZUg0ol8uLMIdfPdc1rXmUwpbruhtRuKw18yHhc3MlXMVcguaTA9Njm3THTXdN+zRsJozta2E0kHhezhFiEwZ7Fid4jTvOt/R5A1xXf4jcW+SmqBEshS0+1f/7iV5/x3Ud7b6gg90X3HDiqlf67WYxLnba9tfY3UvlfeYkzl+aMUElqujp6UGn+C/iQfEAhVLMa9Fl64OOOykFVJqOCNGMKa6CPI32v4Mdxe8b2OnbtMjq7Q0l2nOmUCg8RKE6sgwZvf8YBb+Xtq0cxwmk5CPmXnR3d7eEoduP6pegnq3r1/e1RVG0gj5LkYUAvZ9A4UFyq2DM3o8Bc6jnRez+EGT6DgT1Ecj30JIUWQhqGBodugMSnX1Ja4DC8rgPneQ24r8QYHfjUvC/tdb3UMgKQ+8JT6t9OMlezOYrzGglpVJkJUA72vFkzKDIZRQZozDeIN1BPy3k/kArt5ObIisB9L/Hse0vUKDXcexpPBOLTbxSqTRFUbi5WAxeUVJMIb68+kENWQhMEWj/klLivTguPWIkW7vNpVJpiSvlTlyC1xGb1Jo3SjULgeuKYcjyBufsCIofhWp+NPeB0rPwXbWLc2eK3BS5A9Fw28V1ibGWkwP/WCOdrZSaBQqfQcFxctF3ezVubWJk6vvuC77vv1oqhbvwb/M0KxS20rIUuYmi13Lq4cPGmifXfGqNtOcoNQu8ohvnqwOzGIat6urquhfzeRLtexpr5jwflvUv8XGTVUqM/ogAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.Tree = gd[object]()

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [[_[0]] for _ in Tree.Branches]
                Tree_Path = [[_] for _ in Tree.Paths]
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

            def Complete_data(self, basis_List, Need_List):  # 补全数据
                Last_Data = Need_List[-1]  # 以最后一个值补全数据
                if len(basis_List) > len(Need_List):
                    for _ in range(len(basis_List) - len(Need_List)):
                        Need_List.append(Last_Data)
                return Need_List

            def format_data(self, number_List, format_str):  # 格式化输出数据
                Format_List = []
                for number in number_List:
                    for index, s in enumerate(format_str):
                        if '{' == s:
                            start = index
                        if '}' == s:
                            end = index
                    try:
                        Format = format_str[start: end + 1]  # 取出{}
                    except:
                        print(666)
                        return
                    if len(Format) == 2:
                        self.message1("字符串格式输入错误！")
                    else:
                        Font_str = format_str[:start] if start != 0 else ''  # 取出{}之前的字符串
                        last_str = format_str[end + 1:] if start != 0 else ''  # 取出{}之前的字符串
                        if ':' in Format:
                            sr = Format[Format.index(':') + 1: -1]
                            if eval(sr) == 0:
                                number = int(round(number))
                                number = str(number).zfill(len(sr))  # 根据:后面的位数来针对补0

                                Format_Str = Font_str + '{}' + last_str
                                Format_List.append(Format_Str.format(number))
                            else:
                                self.message1("字符串格式输入错误！")
                        elif eval(Format[1: -1]) == 0:
                            number = str(number)
                            number = number.rstrip('0').rstrip('.') if '.' in number else number  # 去掉浮点数后多余的0
                            Format_Str = Font_str + '{}' + last_str
                            Format_List.append(Format_Str.format(number))
                        else:
                            self.message1("字符串格式输入错误！")
                return Format_List

            def get_number(self, Data_Length, Start_number, Step):  # 获取数值列表
                number_List = []
                while Data_Length:
                    number_List.append(Start_number)
                    Start_number += Step
                    Data_Length -= 1
                return number_List

            def temp(self, tuple):
                Data_Length, Start_number, Step, Format = tuple
                number_List = self.get_number(Data_Length[0], Start_number[0], Step[0])
                Format_List = self.format_data(number_List, Format[0])

                return Format_List

            def RunScript(self, Object, Start, Step, Format):
                try:
                    FormatNumber = gd[object]()

                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    re_mes = Message.RE_MES([Object], ['Object'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Data_Length = [[len(_l)] for _l in [_ for _ in Object.Branches]]  # 得到Object每个分支的长度和下标
                        path = self.Branch_Route(Object)[1]
                        # 根据Object将缺少的数据补齐
                        Start_number = self.Complete_data(path, self.Branch_Route(Start)[0])
                        Step = self.Complete_data(path, self.Branch_Route(Step)[0])
                        Format = self.Complete_data(path, self.Branch_Route(Format)[0])

                        Format_List = ghp.run(self.temp, zip(*[Data_Length, Start_number, Step, Format]))

                        if len(list(chain(Format_List))) != 0:
                            for i, _path in enumerate(path):  # 将得到的数据还原到原树分支中
                                FormatNumber.AddRange(Format_List[i], _path[0])

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return FormatNumber

                finally:
                    self.Message = '物件快速编号'

except:
    pass


import System
