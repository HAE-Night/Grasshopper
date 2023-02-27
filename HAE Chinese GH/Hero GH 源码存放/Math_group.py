# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Math_group
# @Time : 2022/9/17 17:38

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import ghpythonlib.treehelpers as ght
import Curve_group

Result = Curve_group.decryption()
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

        # 长度转树形数据
        class LenTree(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-定义长度树", "RPP_LenTree", """列表长度转树形""", "Scavenger", "Math")
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
                if List:
                    self.num = len(List) if Split is None else Split
                    New_list = [List[_: _ + self.num] for _ in range(0, len(List), self.num)]
                    Tree = ght.list_to_tree(New_list)
                    return Tree
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
                o = "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"
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

        # 通过下标取树形数据
        class GetTreeDataByIndex(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-树形下标取值", "RPP_GetTreeByIndex", """树形数据根据下标提取的方式；支持多下标（树形路径的模式为{0; 第N列表 - 1; 果实数据}排列）""", "Scavenger", "Math")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e9722fda-2f6c-4564-baaf-e8f5f94729a9")

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

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def RunScript(self, Tree_Data, Index):
                try:
                    new_index_list = []
                    for single_str in Index:
                        new_index_list.append([int(_) for _ in single_str.split(',')])
                    leaf_result = [list(_) for _ in Tree_Data.Branches]
                    if len(leaf_result) == 0:
                        self.message2('原数据树为空')
                    else:
                        Result = []
                        for single_index in range(len(new_index_list)):
                            try:
                                Result.append([leaf_result[_] for _ in new_index_list[single_index]])
                            except IndexError:
                                self.message1('超出索引范围！第{}列表数据错误,原数据列表从0开始到{}结束'.format(single_index + 1, len(leaf_result) - 1))
                                Result.append(None)
                        return ght.list_to_tree(Result)
                finally:
                    self.Message = '树形数据取值'
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


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Math_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("9fe247e2-04a4-4f52-a621-8a20181137f9")
