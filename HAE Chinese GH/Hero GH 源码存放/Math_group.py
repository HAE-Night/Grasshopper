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
                                                                   "RPP_GetValue(Section)", "X1", """Get the range of the list""", "Scavenger", "J-Math")
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
                self.SetUpParam(p, "List_Data", "D", "List Data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Start", "S", "Start of Range")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "End", "E", "End of Range")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Return Data Range")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMtSURBVEhL7ZRJTBNRGMdr9GCMCeGmVzyYkM4+0wVbW2mpbFVWQVSWFKXAzFCm7FuDLKVDWxYRNO6akOjFRA1wQA0XJRg5qBdjkJviEbkgGD/fjIOyeDIkXvglX+bN/L/v/d+bed/odvj/BGyBPTzZE/DTfZMiEZranpCnapmBiSpCLtb56BDdxF0BH9m7KJKheZGUtyFC8xIVXUUGqzqJDCe0cFcBCQXaprYFAZf7/VQUdNV0xNSMdiBS8llFABja//VV+5HPk3WeldcB749PURYAdqlVm3h+q2jvj7dB9/JM26WFZ7XDi9OtNR/Gm2hFE4jQgERF/hj4qN5ziiDzmd1vHkgwO1oBL2974fGABzxuG69omzluYp19UjY8DBfCo2ghTN/hIVh+clrR0HfYaFBF9p1WhBQWu59xhIU0EwUpHAFOEgM7rg8o2mbSTFymDYuHJJTjoDBw0QQk0fp5RfPpBzr8awaN7AiIdOeF8nS2Lc/GQY6FhewEBgqO/hpnWQ0LDdmpRnVWDX9WkvuUzfglx2qA4kQTnLKycNpuhDNoXOwiXghc41MfEV1WDRqYEahk6uvTTIeHvClH56RMF0o0g8dpBiH9GGSY6Y9FTtP7fAfVVW5sxAusrsg5JzOekUBOVKbZ1bx8mxF4twOqTyQuJXFxYjndMFZNRFf+vCK8L09ZWdlx6xhayayDxkaSWSxclmwdr3RbBCzGEltBtcy0GK4COuNQGX9ZEPMpvCzZMuJi9SV2Mr4o1UgOFSeax5V5fPhg518/clxsbIxyXU86c3CfRPY/aeVuKMdZriLD9ztMd0EgesJayhZQww1uMJCYSK6mbYEn5PZO8z0Q8B5Je6SrpsK3L6om3We0RxtABhHUbKATmbClGTUa6rpm1As4TwaJtVDvia6MJg4dAlJ+otWq5OY+2I1W+K6G7v/G48HE9bXKGB3TUbXRBFo+hH4T3xWTRnZ4SwSMNwFNtFQRHzigzf0bL96lRwbQari+pa7VcA3QLubURJHs5uqYQY+PDJVujnr6UqmAByk18S/wWJe1jh48v7EuXFpH9Zf4sGCclrbDDv+MTvcTwSjMT0kDsa0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def RunScript(self, List_Data, Start, End):
                try:
                    Result = gd[object]()
                    re_mes = Message.RE_MES([List_Data], ['List_Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origindata_list = self.Branch_Route(structure_tree)[0][self.RunCount - 1]
                        Result = origindata_list[Start: End + 1] if End is not None else origindata_list[Start:]
                    return Result
                finally:
                    self.Message = 'Get Date of Range'


        # 根据长度得树形数据
        class GetTreeLen(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GetTreeOfLen", "X2", """Get Specific Length of Tree Data""", "Scavenger", "J-Math")
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
                self.SetUpParam(p, "Tree", "T", "Data Tree")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Length", "L", "Length,Default is 1")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "Get Specific Length of Data")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOoSURBVEhL7ZJfTFt1FMfvbFcQQYbMLpjIXIMZXOn9097e27/30r+UlnYto3SOjauT3LWM9hZKSdwSb+KDUiYb8ODkae8868vM4ouJ0UyiRqNx0TgjJi6ZJJj4YNTj79Lf5kDQQXzwwU9ycn6/8zvne+7v/C7xP/9t3tE045KmNBQKhTpF6W+onEk2ASwbNFmu1/caOgeAfTh9dwyHhKQSk756PtbzfVrkvx2U+NWUj7894LPfPBl0fxf3cKu9DvbrmIt7P+l2N+GyB0cOCscTLhYGJQFOBVwwJDogIznhuCjAaK8PUm479PEMRDj6FhDE7m9xOsCX/CwJcsQHSlSELGogh70whBqOhtxwQuQhJrAQc9q/xCW7I9fr+WAk4oGxRADOIOFhvxNyMQmeRQ0KMRGKKJ708OiGrt9K2f4ILvtn9EecHozMj8clQB5KqfCG8HDIA3nkT6NxnYv64MWBMJwMeiHhcYAS899RkmERS+zMZDoQnjgW+FyJeqGcCkElHYFz/QF4LtoDg343GpUPRoJukANOmEr0wEvZ+Mb45KAL8nE/TA1Er02moxm4erUeS24mLtDXow5q3U8dfbufp67Fue4fgnQX+KydIFJdv/Ry3Wt9Dnq9z2G9nXYxN4b9wko+Kq4nHNQ3IapzLSnQkEUjTHm5jyLcM09i2S0cJu515zs6HvWSHaTY1cFK9NGnOjufaBW6jxwiSfIxnEK4KIs5kyFNlpaWZtLS1v50u9libicshJN4GKfUyGSWDRP0/CmNXG7EoT0zTV8ZKlPz3XhbQ6UvH1CZ6q9l22t2HNozSOeWSlcreFsjb321pchU11TbK4J+m71bxqAys5+WmKqKpWuMkVojOvhpkr30M/I/6s22GorfmWQur253dtf02vOOK4D8CJb+k3Fr1VexLYwWqWruL8ZezOWtL6snusbmUHG+yFZzKj17dquVULzMzL9QYBYex7I1JEkzFpjZJVmSt/+HaxwkjMSbeL0j49TMjP4BeFtDIzVTUR+B7dJN5D9ED7Vy1yq2xZUL3JIbpbXtNxne0/MnmDkJxT9BuZsMPe7HFfvi7yV2dlrPu4diX9qPEr6YsM1VVKqavd8q3GL2vO2Ntrq6uiOowbt6fpl63TxlXziGbr3JVLaaRO/4lsrOnN0Qvp8x9uJhvNwWU6OJRA1uoKWxFtmRffoH4/WDYzY/cshgNHxmND503VRvvIDD/y6tra1NDQcb2pqbmw/g0N9AEH8ARAyKk/QWx2IAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.len = None

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

            def get_tree(self, len_list_data):
                index_list = [_ for _ in range(len(len_list_data)) if len_list_data[_] == self.len]
                return index_list

            def RunScript(self, Tree, Length):
                try:
                    self.len = Length
                    Result = gd[object]()

                    structure_tree = self.Params.Input[0].VolatileData
                    leaf_list, origin_path = self.Branch_Route(structure_tree)
                    length_list = list(map(lambda x: len(x), leaf_list))
                    res_index = self.get_tree(length_list)
                    if len(res_index):
                        for _index in res_index:
                            tree_zip = self.split_tree(leaf_list[_index], origin_path[_index])
                            Result.MergeTree(self.format_tree([tree_zip]))
                    else:
                        Message.message2(self, 'No Specific Length of Data Tree！')
                    return Result
                finally:
                    self.Message = 'Get Tree Data as per Specific Length'


        # 输出列表前N项的和
        class GeometricSeries(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GeometricSeries", "X13", """the summary of the first n number""", "Scavenger", "J-Math")
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
                self.SetUpParam(p, "List_Num", "L", "list data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Final_data", "F", "Output Result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMESURBVEhL7ZXLaxNBHMejVhEfWMSjVy+FZmd3k1rTQ/EfUERL8YFepBVlH0ma1NboaLF0Zzc1pkb7EnwcqvaiFsGDhYIH8SR60IIgvVlRL6JSquj6ndmJhKZJoRS8+IWwme9svp95/GYSWmkdU2htQs9uk82VFQ3R1XEt+8ZSWZ+0AhkK290dGRoziVOgzVM1RS8THeaeg+Yq7i0lBPf0xsZ8m7hUWoGsepbqabztd0UHfZN4Ue4ZmmP3xu74luJ+5CMTL1aRrbhNHVre74wU5i2FnZd2ICPsGqcjV/2uyDXfIt457pkqO5FpGOWAt6UAS3V3WcQxF0IR+sAibMJUnAmTsJy0AxUBKX0AM2DPuWcpTvtiAIw026Fd9mkdXSctIZuw4/HG/q2m4j4EZEDagYqAuJrF+nk/UjG22SLu0UVnoLAeeN8XAorCACZNheVlM1ARgFCfPzGKfabq7l8OAP1PqgI69YKPdb5uhVlrpmGkfInCLuUAfF20sqoCsDx+UsuJUEw13R0Z/AugzTfWJ8PeRgT0cYCFA3Wyjm5qaRlfI2OEKgJ4BWGD5zGLXwj4iYp4lNLzmBWbHkcI/KcJNTeL9ld8/43nbFob+JBQs3tkjFBFgFyOl/jhC14lCJnjs8HLb/jo8XwfFEK/WMok3slER9B2j8gYoYqAs9hQzGAK5XaxUw+Wi4PgTdNmWmMS911av+LbqicACYDEEhJ2UMYIVQco7JlBnJjYB4SImcg9MEhvna2yCM7HKLw5nPTGlHoJ7VytjBGqCkDnqzZ9eK1B2AyHlALkqzwgA/g32SzTUoDXvI3QUb7eFQDLOwelANyGe/l5WCbgMQCebAZaCGjTnS0I+cI3tRzgZJNqruwu4gcTxYF7iH1Cgczgc9+od7aLTlwN6b7YXYQ5s8KAEDzJ73ZAP5cCbOIcQMitsgNGvAJruidu5DPRYf/Czps+LwTReQrVkWkYovyKFgbEqwlng+LaaJdWVaGcd6S0/GFetnHNPYQ/n1aq0w2y+7/+mUKhP4m86oqLgBPcAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """disassemble Tree 操作，树形以及多进程框架代码"""
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
                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)
                    re_mes = Message.RE_MES([Abool_factor], ['List_Num'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if len(List_Num):
                            List_Num = filter(None, List_Num)
                            Final_data = []
                            for index in range(1, len(List_Num) + 1):
                                Final_data.append(sum(List_Num[:index]))
                        else:
                            return []
                    return Final_data
                finally:
                    self.Message = 'sum n in the list'


        # 随机数据
        class RandomData(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RandomData", "X14", """random data group""", "Scavenger", "J-Math")
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
                self.SetUpParam(p, "Data", "D", "original data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Random", "R", "Random List，if no input,automatically random input")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "data after random")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQSSURBVEhLzVVdaBxVFF5rWyP4X0XB1IK1GrLZuXdmkk38gVWhokVRxPigxVh/VprszM7MZpNtpZm2m7jzu7PbpFtLGmN/8MEHC+qD4IMgLShSKVgK4oPU1goVRKuCFHX87t2b0Dapib7oB8Pc+e495957znfOJP4XKHWNryiQ6H6ThC+bNCwYSpA1lfoDGq3fJJb8OxjEu9eUqwctuRq/2vV6PKxOxINKjb/Zd0GJYsy/p1E3I0wWh6dazStx0qmR9J4Yzn81aDCuU3cdnjUmGb2VvTXZe9igfoQNzo50T2Gj8EBvu32VcHFpDLSVVuCUR0bSMKLhaFZ1rhVT86IfTi0abNmSnsTt6sfwfYuYmgs7Yy/FiT/Z1LUrzlHnEUEvCjmp8iALHcJ2tG+V3SLoC6FJFXdrz5txf2r0cUEtCJ06a9kt2HgjKT9kd78Rg5vgk+djY7K8kp1AJ84+QS2IrJpdlifuuYJS+1ajwT2My5FKYzMioCnear5oBjr1yqXORmwlg5Vme3hDKdW4XkzNCzsz3WKQahIJP2XJ0c6CHP2I8ebiXe7VQ+qOPzGOxNImQHypS+6nbJyn7jtI2NeWHB6D4YFcx1gbXwSYSlhkeYKCvoIITuAGZ/LEe35Qjs7pxHuLrdEk5yP4O8kNGNiuMMCunse+tbR9DTZYDXWsHVSiPdjoZwNJhNH74I9DkhsGUpWUSZz0sDoeM+fY7EXuDEAObFYjlhrc2CRU57aiuiPWJE/jxEVAwQ2UOnciP95nmUxmqaAT0P1y3EbTkuUL4q1J7gssn5b02p2cYMVTVOpxXvIsTlwEdiOmc4Rju6BmoUt+hxjOAiF7hd3MSFVu54R2R/0KxP03nHCSE+chT6LrEJLDMDicp94PCMU6MZXo7e29HOGD9qvHDeIkBY0Q+VGe+n/MyJcD8f9YJ+43bKwR99miWvPh+CCq+qSlhO+CXoIDrB+Ua99DNYcM4jcMOQhg8x02mGK8Tvxc0xcEQ70jbDwL6H8D6z39knMfJm2EbH9BCUeQaK7vGegdYzfDYdaQwwZO/yE7lCH7j7EcIjSTOXWsjYWT5U2YNIE20WIp1TOWHBwV1IJg4tiE2inI1d9hyx2acnAI3z/1t0/MbXw5yXlyW8/emHVJQf0tWEEWlaiiS2M80bAb3d6zL0Y1r+cL5gN6u1u+ez9r03V8LmmyCwPJ53YQy7igLo287Fa2dk+j/UZfoLofjRPxZWJqDkz8F1Dtn29Dk1zszTmg+SdgeIL/TGhwWpf9vVBHATd8CQVpYTyN5J5iwijItdMacZ4WpouHim6Jqz+D5wP81c4ypQx3TsTsDYn+wlSEuef6VvXN3///CXaru5cNpeqtRVpbM5Sut9rtby8XU/8lEom/AHzfvmOSyHdxAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def RunScript(self, Data, Random):
                try:
                    Result = gd[object]()

                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)
                    re_mes = Message.RE_MES([Abool_factor], ['Data'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        data_list = self.Branch_Route(structure_tree)[0][self.RunCount - 1]
                        if len(Random) == 0:
                            index_list = random.sample([index for index in range(len(data_list))], len(data_list))
                            Result = [data_list[_] for _ in index_list]
                        else:
                            if len(Random) == 1 and Random[0] == -1:
                                Result = data_list[::-1]
                            elif len(Random) == len(data_list):
                                Result = [data_list[_] for _ in Random]
                            else:
                                Message.message3(self, "number in Random list should be same with original list!please check")
                                Result = data_list
                    return Result
                finally:
                    self.Message = "random data"


        # 小数点的精度分析
        class NewRound(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_NewRound", "X5", """Redefine the data accuracy, data optimization (rounding off)""", "Scavenger", "J-Math")
                return instance

            def __init__(self):
                self.switch = False

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
                self.SetUpParam(p, "Decimal ", "D ", "decimals（floating number）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Precision", "P", "remaining numeriacal digit")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "Output Result")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Percentage", "%", "per cent in output result")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Per_thousand", "‰", "thousandth in output result")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Scientific Notation（extract precision）'
                Result, Percentage, Per_thousand = (gd[object]() for _i in range(3))
                if self.RunCount == 1:
                    def _do_main(tuple_data):
                        a_part_trunk, b_part_trunk, origin_path = tuple_data
                        new_list_data = list(b_part_trunk)
                        new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                        match_Decimal, match_Precision = new_list_data
                        Decimal, Precision = self.match_list(match_Decimal, match_Precision)  # 将数据二次匹配列表里面的数据

                        turn__Decimal = ghp.run(self._trun_object, Decimal)  # 将引用数据转为Rhino内置数据
                        turn__Precision = ghp.run(self._trun_object, Precision)

                        zip_list = zip(turn__Decimal, turn__Precision)
                        zip_ungroup_data = ghp.run(self.run_main, zip_list)  # 传入获取主方法中

                        Result, Percentage, Per_thousand = zip(*zip_ungroup_data)

                        ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Result, Percentage, Per_thousand])
                        Rhino.RhinoApp.Wait()
                        return ungroup_data

                    def temp_by_match_tree(*args):
                        # 参数化匹配数据
                        value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                        len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                        max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                        self.max_index = max_index
                        max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                        ref_trunk_path = trunk_paths[max_index]
                        other_list = [
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [
                                [None]]
                            for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
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
                        iter_ungroup_data = zip(*ghp.run(_do_main, zip_list))
                        Result, Percentage, Per_thousand = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                   iter_ungroup_data)
                        return Result, Percentage, Per_thousand

                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    j_list = any([len(_i) for _i in self.Branch_Route(p0)[0]])

                    re_mes = Message.RE_MES([j_list], ['D'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Result, Percentage, Per_thousand = temp_by_match_tree(p0, p1)

                # 将值传回输出端
                DA.SetDataTree(0, Result)
                DA.SetDataTree(1, Percentage)
                DA.SetDataTree(2, Per_thousand)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASTSURBVEhL3VVfTFtlFL/3tpCtFGeFWeusEdFtqdL7rxQwLKhxe5Bse2IJS+aCcU4G9N4WGMNGOhmjvb0ttJPBYBsOMrdMyBiYYXgw0WRDp2+LiS+i0U3wxf1BcDpcrr+vvR0g3d588SS/fuec7/z57vnO+Ur9PyhABZgmMbTGWxx9bCkOlHZbCBbloEViOx9dapMOxC5QFliVjA6qdh2yezhlxsurtz1ceJZA4sK394tHrtcLnb8u0RHcIHspXTo0ubpuSpzSooenqDohnC+xyt8SF62QnGoRQQ3fXmLPzp/aYGEHUzo4VcLuO0nQ5QdA5juuSLxyQg9/P8H8XrZtna5K0T3gbJJFKcs+XAW7y6Skuiot1bGhUQ8XOqmLiwkahHi+rjKZzea1NE0vgB92OByZWI1kw8MqX/pd/XawGTk5OdlWqzUrBZvNZiI2MhdNk4BT5s5su/QkxI+Av3RowAISzdI0dQv8jhZ3/7nyvF2vUTR1Dfp75BDAXR3EZ/IdZ+vn9UJHN/gkpRJENo2Qk+2D4ZCRYcYQVAM/DYyD/wR7Lx0Qu8cqHV435A7ozwEfMww9BAwDI7AJ1XLBCZ8QOUZiJyhVohpn+3pdlSA4kwQDupgg1PfrhsKuJ3QxLUlcZCztHdTwCinRUroL9CRZ1F8MPY02vIIeT9zHgwj3tDyB7Ao+izmYk3l1FwLs9HJqPeS2l+3bf9uat/uil49WSXy4RObU3XAe0t3SEuk0Lxf9zMMrfboKn8QGn8Ed/ImNL5rFnt56PtYps+H2990D8kH3qeaW4v54gxAbl/nIddj8hEEbRLI2D6vWgq+W2LAfZenx8pFx6Cf3ixg0PhzRwy9ecmOyRM8ltfcpF2gDHm/gY6d9fMSPwFUyFwkhWJ/MhU9i7YTcILNqefULh+x1bPgiEhxPeBMiCRqFI9OstagKooZuuJqba7Kh/80Mw/yQ0GUwb/gL+0ZqXzy8MeH0EEom+Nck4/Nu7ti4R0B/T0ClGQzMVEaG4RvC0ww1KtpEE8pwSdl2IpsyUNvRXR+gVXXQMYPBoGINwt5eL8SHVyTwsKE/4mXjT0GkMzONvVjJkGlGA/M9sdECGoMW/UrTNAaHGNBbOAEGICZkbrCW+wuPD6R9i9A5zxPZZMpsxqI70XeMmYyP6FHjyz5XhAwjRZ4Fp9OatXmzM6uszGG2WCxrUk9F2hKRBKNbr1ophtpJToJT/b56dUYICciDp+HUh5td3ed9YqwUvAIdKeWnuK8x4ALsRgyGxFA+4uM7zq9MwKmzsVfPWCF+C2io8+uJTSNVjN8p4Ki/sDeMmdgLfhD4EfgZ+AWYBmYAUk4zHs2zKyYZA7Tgdx/dUpBbIhWsFQ/GXxnP9wrRgr5NE3mVDk/pPjbASayqSrx6ob10YL2XC7J1zlZ+T0FAeKvgPZGA2De74w607OSyL3hbDJAn4Ab6eb5RiM80iV3XyGSngFOTPfyLhWZxkDvka4mMQLeWg9goc/hHm6/j1VY9PEVVVFQYPEUxq5eNrnsYyFslC222dHtL8a5wzPbmBiVbD/9fEkX9AxIWEwLJZv7EAAAAAElFTkSuQmCC"
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

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if ref_obj is None:
                    return None
                elif 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj.Value
                return test_pt

            def run_main(self, tuple_data):
                """运行主方法"""
                Decimal, Precision = tuple_data
                decimal.getcontext().prec = 10000
                Precision = 0 if Precision is None else Precision
                if Decimal is not None:
                    per = Decimal * 100
                    per_th = Decimal * 1000
                    Result = str(dd(Decimal).quantize(dd("1e-{}".format(Precision)),
                                                      rounding="ROUND_HALF_UP")) if "e" in str(
                        Decimal) else self.handle_str(Decimal, Precision)
                    Percentage = str(dd(per).quantize(dd("1e-{}".format(Precision)),
                                                      rounding="ROUND_HALF_UP")) + '%' if "e" in str(
                        per) else self.handle_str(per, Precision) + "%"
                    Per_thousand = str(dd(per_th).quantize(dd("1e-{}".format(Precision)),
                                                           rounding="ROUND_HALF_UP")) + '‰' if "e" in str(
                        per) else self.handle_str(per_th, Precision) + '‰'
                else:
                    Result, Percentage, Per_thousand = (None for _ in range(3))

                return Result, Percentage, Per_thousand

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

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


        # 四舍五入
        class GHRound(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GHRound", "X4", """the decimal point (float point number),rounded off up or down""", "Scavenger", "J-Math")
                return instance

            def __init__(self):
                pass

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
                self.SetUpParam(p, "Decimal", "D", "number（decimal）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Precision", "P", "remain the number of figures")
                accuracy = 1
                p.SetPersistentData(gk.Types.GH_Boolean(accuracy))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Result", "R", "result after rounded to the nearest")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Floor", "F", "rounded down")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Ceil", "C", "rounded up")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Half Adjust'
                Result, Floor, Ceil = (gd[object]() for _i in range(3))
                if self.RunCount == 1:
                    def _do_main(tuple_data):
                        a_part_trunk, b_part_trunk, origin_path = tuple_data
                        new_list_data = list(b_part_trunk)
                        new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中

                        match_Decimal, match_Precision = new_list_data
                        Decimal, Precision = self.match_list(match_Decimal, match_Precision)  # 将数据二次匹配列表里面的数据

                        turn__Decimal = ghp.run(self._trun_object, Decimal)
                        turn__Precision = ghp.run(self._trun_object, Precision)

                        zip_list = zip(turn__Decimal, turn__Precision)
                        zip_ungroup_data = ghp.run(self.run_main, zip_list)  # 传入获取主方法中

                        Result, Floor, Ceil = zip(*zip_ungroup_data)

                        ungroup_data = map(lambda x: self.split_tree(x, origin_path), [Result, Floor, Ceil])
                        return ungroup_data

                    def temp_by_match_tree(*args):
                        # 参数化匹配数据
                        value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                        len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                        max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                        self.max_index = max_index
                        max_trunk = [_ if len(_) != 0 else [None] for _ in value_list[max_index]]
                        ref_trunk_path = trunk_paths[max_index]
                        other_list = [
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [
                                [None]]
                            for _ in range(len(value_list)) if _ != max_index]  # 剩下的树, 没有的值加了个None进去方便匹配数据
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
                        iter_ungroup_data = zip(*ghp.run(_do_main, zip_list))
                        Result, Floor, Ceil = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                      iter_ungroup_data)
                        return Result, Floor, Ceil

                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    j_list = any([len(_i) for _i in self.Branch_Route(p0)[0]])

                    re_mes = Message.RE_MES([j_list], ['D'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Result, Floor, Ceil = temp_by_match_tree(p0, p1)

                DA.SetDataTree(0, Result)
                DA.SetDataTree(1, Floor)
                DA.SetDataTree(2, Ceil)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARzSURBVEhLrZZ7UFRlGIfPaP1RQ8OUZk1ljF0clBKQQQiZnEQmMEeckTGz0MS41K4s4HKXaInLAiJXSYggChhuOgreCIQQDSmgErmzAssuu4dllwV2zQD59Z5lmZ2a/ijh2Xlmvu/dnd/77Xe+c3aZ/8A6cs3icOUxJ6Wkjuwmc0lP8jlyReBWD3KQTCfvkA+N1pHvkcviWZJrUG+YLbKKdCP7SO69j8hH5p8NNpF+ZA2pJztJa/KR4RpwQSqSC+OaTZNcA+5aPEYuC67BJMkFK0lHckVZ+gbjpJZsIrltWjGWrsEVcjPZY5wHkyvCUoMbhhnDrCZTSK7WQG4gl8XSffCLYWZiG9lPcjfgAa6wHCrJ8MUhs3oH85lZNnPXzIHZZ7eWWd+yfpXl7YNPRHh+YBbhJ7TOigqwE7saP2vC105sHmKf7iJyz90v3Jrq47UmKtzrmcikoy+I8niviIv5G1MuhztndqR7lwyGOqUpY9xydIn7Cx+c+bhqJtunfKEguBrlonqId5aCbyWuMMaaCLCN3xJmn4Vo5zx8L7yK+rw2XM9vw62KTnRc68dQhxLDd5WQDpASJRRyFVQTGihYFpKRe5Cxcujmdcg6WgGfDbHNxlgTYbvE5gE2SRrfl+NwMbsBc5iF9v4UJnVa/Lkwi3l6qbUasCqVQSU7jjEFi76+AXR190IqlWNSr0VRRA2OWYhGfO1yHzdGmxDYJN3hvZaM3KBKqKc1kMkUUCjGodPfh1qjxejoGGRyhaEuH1NiUDKEzs5uQxM51TUzGlSdqsMnFqIHx98Uv2SMNSGwTa4RWJ5G6uEisGoVRmVjYFkVZnR6w2pHR+WGGtdgRCpDV1cPNeiCRDJsaDwxpUZdSQt4r4tBWW8ZY01QMf3EGxn4YvdZw2q5sAnaZ26vpRQuk1P4mAJjSlr9PQl6+nvRLxmAUs1CpZ3A9NwUfm/thXBLBnhW8QeNsSYCbFP4oTZZEDqexpBECv1DPfSzerCacSjGWUP4yLAMvV0StPzYjqart1FXdRONVa24VtSMmtxGFEZdAB1V8K2TE4yxJgQ2Yvcwu2wIrJORH3oO5Ym1yAuuQpp3MU4f+Q7i9wsR5/E1Pnf9CqFOGQhxzEC8RwFO7syhcZrBaJczSD1UjEDrdJ2/Vdy7xuhFgnfErBXYJo6Hb8tCafRlVHINAipQnnAJSQe+QapXIVI+zEeRqAznsy7RasvQWNaM+uJmNJW0o0xUi466Luj1U2gq+A3HLZPn+ZuSdxnjFwlyin6HbyleKI28AtDR/IP2FXRodVPTUCtUdB8M4debt9D9cwfa639CW20rBltH0HtjBG3V3WgqbkN1ZgO+PXkewfYpczybWO6n9u8E2ov8BZanUCS8iAtp11EQeW7hbFCZLuPTIjbFK38wZm9mW4hrwg8n3o4v422NzTnyqvBLz3X+gXue8vZyYQ7tsWPct9swbpsPO/q9yHPh/fu/Ef72UHePp4/tdmD2OlgyzhufZCyep7IZyT1N/wcM8xeTS7i+To9tBwAAAABJRU5ErkJggg=="
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

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if ref_obj is None:
                    return None
                elif 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj.Value
                return test_pt

            def match_list(self, *args):
                """匹配列表里面的数据"""
                zip_list = list(args)
                len_list = map(lambda x: len(x), zip_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                max_list = zip_list[max_index]  # 最长的列表
                other_list = [zip_list[_] for _ in range(len(zip_list)) if _ != max_index]  # 剩下的列表
                matchzip = zip([max_list] * len(other_list), other_list)

                def sub_match(tuple_data):  # 数据匹配
                    target_tree, other_tree = tuple_data
                    t_len, o_len = len(target_tree), len(other_tree)
                    if o_len == 0:
                        return other_tree
                    else:
                        new_tree = other_tree + [other_tree[-1]] * (t_len - o_len)
                        return new_tree

                iter_group = map(sub_match, matchzip)  # 数据匹配
                iter_group.insert(max_index, max_list)  # 将最长的数据插入进去

                return iter_group

            def run_main(self, tuple_data):
                """运行主方法"""
                Decimal, Precision = tuple_data
                decimal.getcontext().prec = 10000
                Precision = 0 if Precision is None else Precision
                if Decimal is not None:
                    Result = str(
                        dd(Decimal).quantize(dd("1e-{}".format(Precision)), rounding="ROUND_HALF_UP")) if "e" in str(
                        Decimal) else NewRound().handle_str(Decimal, Precision)
                    Floor = math.floor(Decimal)
                    Ceil = math.ceil(Decimal)
                else:
                    Result, Floor, Ceil = (None for _ in range(3))

                return Result, Floor, Ceil


        # 数字格式化
        class FormatNumber(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FormatNumber", "X11", """format a set of number""", "Scavenger", "J-Math")
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
                self.SetUpParam(p, "Number", "N", "number")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Format", "F", "format character string（00，00）")
                DEFAULT_FORMAT = "00"
                p.SetPersistentData(gk.Types.GH_String(DEFAULT_FORMAT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Prefix", "P", "prefixion of the number")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Suffix", "S", "suffix of the number")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "FormattedNumber", "FN", "data after formatting")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASFSURBVEhLvVXtT1tVGL8XnC9hc4VNF+cmy5hAubc9596W9YWXwqwNTh0jWnHEOYVZldFX2k0TlhrioLctlA7EIRHcGJot4uvUzCUSs8Uv+sH4wS/6xfhF/wiDv+f2DgpdjJ/4Jb+e8zz39Lw85/c8R9hMlJeVCa+iDRfMUkTVlDPMtIxh6jilaLtjyvh7YZ4JGa5tYBps0q0i7BBEcQ7tBwWzFCFMHlPGVgK27E7DJYR4Oj3Ic0+EWXpitHnRBpcE3gJfpO8bcQAc93g8O1XOT3Krtc9qtWqy3DDdzDseiFgzF0JcmworWm9huL7A+9SSb4ClKAKE18DVMcWgBVL9/f1bORbA5H2yLGv1cu1EQDnrivHx30/bJm9gtx/5r/rLu17oejDCMvoCIZ7pC6lagPoALfBcobuGe8Ek+CNoJkcxomwsE+HZ1Bl+nsXZ5Nfeg75hWa3/LaxkRhNqPoCTzQ+qeQpRNfg5eBmsBFdxH3jCoEKOYgSZ1h5mSRP131CnHD6p072vbu+RM96Z7Zh4OKRkntcHCkIN+BL4MlhFjk2DVRDET9BeAvWdbkSEp71hrl0xTB1hJWUeVHKXccJhw+XCPF+iXQS36x4D9SDHR7q0V3TPBgRZagKq+SdoSe0xXAIWPB+zZxVIeAR30Q7XfvARzLMglJUd1wdtQNZkMoUh0yRUlLRYLFcg0+s+e+feKMvMQkHZoJIOGmPpVKsyDSkaqec26JLdhe4aWkVRmGm2WCpVxtoZY21WWe6ttzwaGFDPtSBj/8Qub0VYeqnzhMfU7mu3rcqUaYEg107qsxQkui7jCWZRFG8KW7aQ1O7RPUWIKOk8dhuPsncfTrDJJW9jR9rMa/+ATIfifOIsFv1wyD5dh6EOVISf0CLc6+/yGPgtYkdH69Y9RQjyTEPSk6RcEeJqvqZDOlqzZ/8uedmzfFdczb1OMtYHCgLF/WOQxHKYHJuHlibXgt1uf/qQx+N3OBwXenp6Kp1O5/XW1laz2+VacjpbDja5nTP49kyz2zVpdzgomf4/mNW6COU8ZeOWY5Ikzft8vipZkr5vbGyULJJ0jdulxga5bhpjunH5Mw0Wyx3l/F+4H6SScUes+FfKZ50/lKT/oJpzRNTxhwyTsBvcWuiuoQ38DrwBUj0pAek8zNN/GaaOCE89G1PHLyLh5pb9f9OkXqiRMpmqwi4aY0D8FD9URXtFsXwUsa9CaHaoyDRVVUm6IiaZgt5/DVszDvoHgRLN35C8O8QyA2+7Fp6E6yJIkYiCt8u3Dnrm5sFLFRUVSwpjebwF07iDm5Js/uWoctwc5WPXkGzvYCFN/wdgZLJI78E51yJV1DfBEbg+Q3sKXIcufCANDxZMQcABKqtZtSmm5LoRip9Pq1OzMZb7xtvW9pjdrWQRsrlEnbYNb3UiYZvwG38j/S+BPbplwAJCduIXaEsenIiijYSsqWbqJ9jUyOPK4aED0r6vUOiOJJT8VZxqIVZ4qxlIE9NGV4sigarpW6BdtzYgKSTLjG4J4mq6hk5hmPTox8FaQRCEfwHCHTwO0y16RQAAAABJRU5ErkJggg=="
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

            def RunScript(self, Number, Format, Prefix, Suffix):
                try:
                    FormattedNumber = gd[object]()
                    if str(Number).find('.') <= len(Format):
                        split_dec_list = Format.split('.')
                        if len(split_dec_list) > 1:
                            A_Part, B_Part = split_dec_list
                            B_Part = '.' + B_Part
                        else:
                            A_Part, B_Part = split_dec_list[0], ''
                        reverse_str_list = [_ for _ in A_Part][::-1]
                        pre_str = Prefix if Prefix else ''
                        suf_str = Suffix if Suffix else ''

                        if Number is not None:
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
                        else:
                            self.message2('N terminal is null！')
                    else:
                        self.message2('Format error!')
                    return FormattedNumber
                finally:
                    self.Message = 'format number'


        # 列表数字或字母
        class RangeSeries(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-RangeSeries", "X3", """number or alphabet in the list""",
                                                                   "Scavenger", "J-Math")
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
                self.SetUpParam(p, "Start", "S", "Start of Range")
                START_RANGE = "0"
                p.SetPersistentData(gk.Types.GH_String(START_RANGE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "End of Range")
                END_RANGE = "10"
                p.SetPersistentData(gk.Types.GH_String(END_RANGE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Step", "S", "Length of Step")
                DEFAULT_STEP = 1
                p.SetPersistentData(gk.Types.GH_Number(DEFAULT_STEP))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "List", "L", "Creating List")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN5SURBVEhL1ZVdTBNZFMdHgkZX/MiyRC0DtVDo2jpz587QKUVjUStorYvRrYqCUcGPAhVEQUVUREDQykLVlay6m02MH6/qy+6DJr75YDA+6LMPJhoK8UGjZpM9nju9UBEkGoiJ/+SXnv85t+fMnZncEb6VJiOmWDhhmookxUJBKEReICw5UWpB7sRCQdiAAPKD4SZGfyJPYqEgrHH86Py/PifysFo5/WC81NLOBxttob4pCdPu8v6C3z23EI65rkCd1j1uDuX8DiFyCqYlJv3D+wt+fc5yLFwAvIJxgzuA3VITG/Av7892UADH9MtQp+JVjEGIdkGN2jVqbZBD2gWoIm04YMbQDtY4knX2DB7vpR29Y9EkN/YfJs3PRqsNUqt29hbbaqIfP4MAwt6ioff2cxpIs1x7LVrKuR1Ll5HHsRB3gLxFEqy6daaR+YyiaZnXX6Vm7OZ2VHmKyGz8uYg8MhKo6YhEKSnRKL1JKV0fS49Un2i90W+y7uF2mDweT6LTSdtUlVxBm45Qo8AEAJMUQiKaps1SFBIJBOxTeGmYxhqA/53sdqvLVFXu4Km4JEnKIIS0sliW5XZFUVKMwifqS7Ne70/N2sXtCHm92ixVkdu5jQubWnBAG4sVWe7Aq/nJKHyke4InMYo7GDBlVuIbkcDTw7RypT4Tb3Uzt3HhgOk44JLL5Vogy1IPu5+8NKSomKW/T89+ExUznz6fp416buXlaT5NU27pumzhqbhwyDpVpdcUSfLy1DC9TLEnDaRmvcMBt3lqhPABb9M0Wou3OI+nvk7/ieZuEMW13H65Suz7rBX248p2RyMhKbmLShfU0nL0qy1bdUeyK5/FjKrUxYHNc5etGvSs5rdsc5bbG9A3KLZkdemWn2vUCtKibLLVxT9iQbn5/kHtPOxTwpAvroUq+RTsp7/BdvthWJEegHotYuDLKINfMndCvYoe8ab9CjtwDTvgGPliEVTKrdCQcxH2SM1neHtBqJJbe0/k/g1HnD1QYN6Ah9Y5OKpfgqB8EvyWUmjK/ctgU3YIirOrocmFHvHNL4EKXNOo/2FQYN4IB/AwbHFfxXzbed5eEMocR4LV5HQ4KJ0Mu+Z4e8ocjWcrpZZwsa260yMWdYdIe5jhM5d0+cylXYN+ickfYWuCuJbhNhVGyhwNZ2toZ3jHwqOrefvvVoLwAe03zPfliqAXAAAAAElFTkSuQmCC"
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
                                self.message1("Character List must be integer!")
                        else:  # 两个值都为数值
                            Start, End = float(Start), float(End)
                            List = self.circulate(Start, End, Step)

                    return List
                finally:
                    self.Message = 'number or alphabet in list'


        # 物件快速编号
        class Number(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Number", "X12", """give number to object fastly""",
                                                                   "Scavenger", "J-Math")
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
                self.SetUpParam(p, "Object", "O", "object list need to be numbered")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Start", "S", "start value of the number")
                START_NUMBER = 1
                p.SetPersistentData(gk.Types.GH_Number(START_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Step", "N", "Length of the step")
                STEP_NUMBER = 1
                p.SetPersistentData(gk.Types.GH_Number(STEP_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Format", "F", "number format character string")
                DEFAULT_FORMAT = 'A{0:00}'
                p.SetPersistentData(gk.Types.GH_String(DEFAULT_FORMAT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "FormatNumber", "T", "returned formatted number")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPkSURBVEhLvZVdaBxVFMfHuLTWTcW1NrqpTZrQGHbmfs7X7mQnBkukoU2o0W5BTEvUYv2K5EVo68eixUZRIlVSir7UQP0oFERUqAXrQ+mTD4qloi9VwSJp+lBtHiw04//u3O3sNgrjiz9YMuecO+d/7znnToz/hUwmU27N5J64ZXlu14pM6y64VsWRpQwMDGRoSHPabKZqtKi4thLasmsOP2Y9Hz3LX48GOyoRXF4cWQoj5F1G6R+e592pXYZpmq1CiKekEGcopVu1OyGfXTczKd6IXvTfi0a6x5WAjCPNMMbaKCHznLEFQkhVu41i0QkdR+y2pTgFgae1OyGf7ZiZ4FPRHvdgtLlr+78K4OWXiWWd8Dw5hL9z15dDCP4phCe0mZBGIIqiG6hl/g6RAw7nPqMkQrL7dbiGlPxz+J7RZkIaAZRnI8oTof5f43dKMHZOnUaHa0DgEwg8qs2ENAKEWN9j9x9r0wgClwjOIwiTMAxXu658hDF6jlN6TEo2opfFpBHgnDzs+/QubdbgnG/DBHVAIKcE1BpM00PKr5fEpG2yQiXBLmcbG4ykHCXbJzk/iFNOanfCPwiwONJMpVK5EX34xbFtVZoHtduwbXsUiStSEhcj/FPjCNdoFNjUtX0xyGY3LPb35+fs/vy8H5p/+sGGyHFuthh7AI39ESd4k1rWN/r1Jmxbvo/Y29qMqQvshsBg59iVt9a1Ty94wf7z0tt/3vaPXHJKvy4Ww2K3aX6F3b1UOapOYv2F56aT9vX1oVL0Z3Y369KumMYTDMclsuKIotpynLEsurgW46lm/1v8TuL5Knb6jl5klMs+R3nOFgqFe7QrIU2TUfuPkPA7bprCsiyPc/q4uhe9vb0rfd++F9kvYADGtmwZuDUIgjb9WkwaAdT+CBJv1GYNQsxjaDDF9LyA3X8BgRkM1IcQn9JLYtII1BmaGFqOEb32Ja2DCWvFfejWZjP/RQC7m+WMXpFStmuX4fvODkeKozjJB+jNl+jRHToUk1YA5cjjkzGPJBeRZJ924xskO/WjgdhvKOVObcakFcD8T1mm+RkSlC3LnMNnYpnyV6vVliDwtxaL3quCs9Pw31Z7oU4aAZUEs39BCHYoDEuDamTrt7lUKq2wOZ/EJZiG74SUtHlU0wjYNhvGWF6llBxH8pOYmh/UfdDha7i22EupdVqbMe3ZzkPPOQeiV0qz0ej6nUrAjiMJSHwWCWe1ibqb63FrIzWmrmvvcV33tVLJ34t/m2dIoTCml8Xkblo1fV/HtoWRrvHL4vbyZbiWfOw4IaPXTwd6MYzf2p6enjXozzjK9yTWNLxrGH8Dw5V50EWy1BgAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.Tree = gd[object]()

            def message1(self, msg1):  # 报错红
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):  # 警告黄
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):  # 提示白
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Get_Tree_Data(self, Tree):
                Tree_list = []
                for _ in Tree.Branches:
                    if len(_):
                        Tree_list.append([_[0]])
                    else:
                        Tree_list.append(list(_))
                Tree_Path = [[_] for _ in Tree.Paths]
                return Tree_list, Tree_Path

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
                        return
                    if len(Format) == 2:
                        self.message2("format of the character string is wrong！")
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
                                self.message2("format of the character string is wrong！")
                        elif eval(Format[1: -1]) == 0:
                            number = str(number)
                            number = number.rstrip('0').rstrip('.') if '.' in number else number  # 去掉浮点数后多余的0
                            Format_Str = Font_str + '{}' + last_str
                            Format_List.append(Format_Str.format(number))
                        else:
                            self.message2("format of the character string is wrong！")
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
                    if Object.BranchCount != 0:
                        Data_Length = [[len(_l)] for _l in [_ for _ in Object.Branches]]  # 得到Object每个分支的长度和下标
                        path = self.Get_Tree_Data(Object)[1]
                        # 根据Object将缺少的数据补齐
                        Start_number = self.Complete_data(path, self.Get_Tree_Data(Start)[0])
                        Step = self.Complete_data(path, self.Get_Tree_Data(Step)[0])
                        Format = self.Complete_data(path, self.Get_Tree_Data(Format)[0])
                        Format_List = ghp.run(self.temp, zip(*[Data_Length, Start_number, Step, Format]))
                        try:
                            if Format_List[0] is None:
                                self.message2("format of the character string is wrong！")
                            else:
                                if len(list(chain(Format_List))) != 0:
                                    for i, _path in enumerate(path):  # 将得到的数据还原到原树分支中
                                        FormatNumber.AddRange(Format_List[i], _path[0])
                        except Exception as e:
                            self.message2(str(e))
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return FormatNumber

                finally:
                    self.Message = 'give number to object fastly'

except:
    pass

import System
