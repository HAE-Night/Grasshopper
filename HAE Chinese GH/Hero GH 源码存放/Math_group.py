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
import Curve_group
import rhinoscriptsyntax as rs
import scriptcontext as sc
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
from itertools import chain
import random
from decimal import Decimal as dd

Result = Curve_group.Result
try:
    if Result is True:
        """
            切割 -- primary
        """


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
                Start = 0 if Start is None else Start
                if List_Data:
                    Result = List_Data[Start: End + 1] if End is not None else List_Data[Start:]
                    return Result
                else:
                    self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, '列表数据为空！')


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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAY6SURBVEhLxZZ5TJN3GMe7LdmybHNb5rIrWWZi1LGJggiFAqUgDkFQ7g0QgdJyFLmpUGoLLRWGoHILWG4qUI7SYkFUZIfKmNcmmxfiPIY63ebF1Cl+9/TtXJZlJnP7Y0/y5Nf3zfN8nuf3fZ43Kesx7Jk5y4UzZ3nzX3t50aIX6fkJ8+v/aM7SLp/FUmMnN6fv5BKF/jJP1n2FK9We42S1jSzkb8iikJfMkf/CrJObrYMq9kP71U9IaDoAbq4RbkojeDkGuORuh4tiAPP8xZUUOsOc8Zj2Zty2YJFmDCar2jEG6wwtuNIuOGZ1wEGsASe7G5YRhZMUakv+JJP0CHsyT/iOcIuUU1mZzalQy5wqWuWO5aJs8TCv4BOElA3DY30/uLJeOEm0DJyd1gL7te14f5XqIuXzzJhH2Kss1uvD+s3U5zQe3L6K85NnMX5mHNs/G0XSxm3ghsZPzfGKH57nHT9ku6b6hkNmO2xTGmGbrsHcoHWXOVYzYnQaf7sKuZ0lsWZbsFhvE/YpM91szx3Z23P9xu37kHUcgHfREDzyB+G53ggvpQ5ukhZw0hp+sU+pm2KnNk3bpTbBJrEOCxLqsSA0b3p/X9T09LV03JyImR7UhE9t76y5VV8YrmbI8kCLp1uVzpLPNYl35Q16sBVDcFMNwFVBQ8zRw3ldD5yySXeTNGvb8BBuLarF/Hg1FVDiy34+MJUOXE0ALq+BQaOEtlwwpS10DWNJAp5966A25ueJkRL4F/URfCfc82hbcmlTZD1wzu6EI0lin6EheDMWJ9XDOmErFsZVwyKeZArJwsmhUOBHEXCOCl0Mw0BjAEZ0Ofi0MfxrlpDLmnlYyx/ft3sLlubvwpK8fgbOk+mYjbGX6LAwpQPzE1rwXlwD5gnVmMOvweyoWswKKoJUEoL75wl8IQr4LgyYDMKozg/6OjH2NKzazfJ5hfXCAU3o0X5DOXjKQbgp+sCTm+DdYGf1wJGvQHwaH1kyATLXkUujIc7mQyyJQn1pMKZOhBM0EjgTApwOBM6vxBGDJ1pL4tBfFWhg0cSf3tcYPDrYWwSewggXeS/TuUM2nVFSDDSsJF1J2x+SzE4a42IsQanrK+TfU4GJD4Fxf+CUD3DWA6OdS1BXyIeh1LfdNOcnhmoDPv3CkANPRTccpTra9U5YJWkgyaTE68k0vAwCpwGX6PdkPEGFpHcESULaTwQR3Bc4uRw4/gHdxAVdZS5oKo6GocS7jtmkgSrfgeP9GRAU1MBqrQEOmVrMj1WjvJiufYO241IqgRNJZ+rcpPe51QT/iOABBF9BcE/ghDvdwAX3vmZjffoSGLfGQb/Zq5QpoC/17j7Wn45t1alwE9fCKrUNc/m1KCuiDq+lUMe0IedNXUfi7qkQ3DkeiDvf+uLO2HL8+g11fYwHfONIz2y0FdtBlUFbpF2Drg3u+UyB7uJlLYd7UzHSIULzxtUQp4dDKAhCZzVJdNUEjyZtqetzoeirdUP9x87oLOOio9QJjQUcFGdyUSF3xcYsN6hSfWBUx9IcRGgvcM1mCnQVulePakXY274Gn7XGYpc6Ar1lq2jdSOeLJMnZVeZBnvbHgxM0yJPLcOuQK+4dc8YpIweKJG+0bYqArpKPXQ0xDGefRgBNnlMyU6A9n7dpL70YbhZiT5P5HFQLcUhPXU/+ZZDjHrh5kItIP2sM1HAwOcyGMtkDO+v5+KQlhnIFdMZiuGE1WpQOAqaARsXNo48CO2rD0V8dxvj2qjD0Vgbi1pgf3YJWdcLLPMgTLpge46CnjI0Le5zoprZQJi5FX1UoFTTnDm5djR3VwWiUs0OYAlulnNwdWwKhKw1A92Y/xnUlfmgtWIl6lTu+6OThyggX94464v5RB9w8YI+zQ7Zozl+E9Ah7qBWeTE7P77n68kAYylaiIsMmmClQkW4rHqrxg7HClz4Onz+8r2wF2gu9UCJ2RXEaByWZdtgoXgyFyAaZkbZQJTijNd8D+j/lmHyg0g99pd7Ij7P0Zgokh857ozjFLlEZZyOTC6xyZNFWuQ89R2iVu05gpUgNtVRG+liowpbNzY9a8e76lDDLPAl/oZLiFTKKeRhvyleJbGRFyezo+ECL55kC/9BM/yL+zv9PY7F+A33nTztjyle8AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.len = None

            def get_tree(self, len_list_data):
                index_list = [_ for _ in range(len(len_list_data)) if len_list_data[_] == self.len]
                return index_list

            def RunScript(self, Tree, Length):
                self.len = 1 if Length is None else Length
                leaf_list = [list(_) for _ in Tree.Branches]
                if len(leaf_list) != 0:
                    length_list = map(lambda x: len(x), leaf_list)
                    res_index = self.get_tree(length_list)
                    Result = self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, '没有指定长度的树形数据！') if len(res_index) == 0 else ght.list_to_tree([leaf_list[_] for _ in res_index])
                    return Result
                else:
                    self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, '空树无法取值！')


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
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
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

            def RunScript(self, List_Num):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
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

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Data, Random):
                try:
                    if Data is None:
                        self.message2("请输入至少一个数据组！")
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
                                self.message3("随机列表的数量要与原始列表一致！请检查")
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
                    Precision = 0 if Precision is None else Precision
                    if Decimal:
                        per = Decimal * 100
                        per_th = Decimal * 1000
                        Result = str(dd(Decimal).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) if "e" in str(Decimal) else self.handle_str(Decimal, Precision)
                        Percentage = str(dd(per).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '%' if "e" in str(per) else self.handle_str(per, Precision) + "%"
                        Per_thousand = str(dd(per_th).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) + '‰' if "e" in str(per) else self.handle_str(per_th, Precision) + '‰'
                        return Result, Percentage, Per_thousand
                finally:
                    self.Message = "科学计数（精度提取）"


        """
            切割 -- secondary
        """

        """ 
            切割 -- tertiary
        """


except:
    pass

import GhPython
import System
