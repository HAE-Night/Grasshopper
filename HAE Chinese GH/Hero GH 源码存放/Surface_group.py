# -*- ecoding: utf-8 -*-
# @ModuleName: Surface_group
# @Author: invincible
# @Time: 2022/7/8 11:10

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
from functools import reduce
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.parallel as ghp
import initialization
import math
import scriptcontext as sc
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
import ghpythonlib.treehelpers as ght
import System.Collections.Generic.IEnumerable as IEnumerable

from itertools import chain

import Geometry_group as HaeGeo

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:
        # 曲面收边
        class ShrinkSurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ShrinkSurface", "E3", """Questions about TrimSurface boundaries""", "Scavenger", "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c2c7a2ac-1b63-4072-ba1b-17c7dd477868")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "Initial surface（Multi-sided surface automatically decomposes and closes edges ）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Type", "T", "{0: \"Do not closes the east edges\", 1: \"Do not closes the north edges\", 2: \"Do not closes the south edges\", 3: \"Do not closes the west edges\", 4: \"minimize\"}")
                EDGECODE = 4
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(EDGECODE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "R", "The result after closing the edge")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMZSURBVEhLrZV7SFNhGMa3VRCtuULLss7aatCmZSUpFkR2nVOnoARF/xREYheii1ZEUKsgqOxiF0SEzEtZJiG5iuqP1NaIll10F2fltDm3nJRbBtX2dM72rZksdbIfPJzzft/3vs/5LuccVqhQmfoYkeJdNAnDDyVvvkSlapUkDD9UavNFSqY9TsLwMyfDdFqoaD9IwjETT+tmEFVFLlQap8zPf8/cD+nzS0RrRDI4HA7EYjGkUikkEgl9lUAwdwH4C8+BJ1VCNC/O2+brk0IkEoHOY5TkrTACMh6PB7vdjsH09bshztJhySYjXD88pNWHwWAAm81mDBJ8JYbHa+BwOEh6gKNXOnG2zEKiACaTKXSDoTNgcLl/YwBuEgUY0wyCGeAzXbzj3+VhCN1g8iR8sdtIOk3vTzhPWPBloxXmHBva9tnwvesX6QSMBj3Yvk0elcHyyTw+BlxffdkeD3pOtqIt/S1MGz5An23C81Vv0Li7Fe5fvtl0dX5iijMSeysMRpD6Olak6NglkLfsZDQ9sfjy1PgLyM634L7aiR/d3/Aipx4Nmc/QlK5GQ1oTHsmfonJVHax6B+41OqHY2wV+rBLRyypOCdL126k0fa4wy5zrNRCufblSkNFeNlv2ipb2+owVtY8jk2swL8uA87d64LT0oXpdCW6vrsbdNbW4s6YGN1IqUJhcBLOuB8rSblByPaKSqhCz8kE9JXtVzkiYpqvwGgQhmcufhc9WskTw4M6eShwTHkFh4jmcTTyDAmEBrm65Bo/bd6KaWzrB4vCYJZrrKzE89CZPRJ8jsMn9vf0oyyvFkcUFOBS/H5e3FsFhCbwn7SZdSJv832NqM9th/TjodBHC9h6UP/yGkjr/0gUI2SAiIgIul4ukB1i6uQ1xGwz4TWI/ZrM5NAMulwu1Wg2j0eh9Okaaly1Yv02DlK0aNGne/21nxqhUqpAMFLSYwd4kv8aPY2PGgt2YuegAJowPtDPyj6c1qs81RWsHrbyhikwoUkUtLX4SrI9oGq2xI1J8Okz/Mk+SMPzMkWnPCGTaqyQcARbrD5mO385QXqhOAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_data = {0: "DoNotShrinkEastSide", 1: "DoNotShrinkNorthSide",
                                  2: "DoNotShrinkSouthSide", 3: "DoNotShrinkWestSide", 4: "ShrinkAllSides"}
                self.type_of_shrink = None

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list = self.Branch_Route(tree_par_data)[0]
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list

            def RunScript(self, Surface, Type):
                try:
                    self.type_of_shrink = Type
                    Result = gd[object]()
                    j_list_1, temp_geo_list = self.parameter_judgment(self.Params.Input[0].VolatileData)

                    re_mes = Message.RE_MES([j_list_1], ['Surface'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Surface:
                            list_of_surf = [_ for _ in Surface.Faces]
                            if len(list_of_surf) == 1:
                                map(lambda surf: surf.ShrinkFace(eval(
                                    "rg.BrepFace.ShrinkDisableSide.{}".format(self.dict_data[self.type_of_shrink]))),
                                    list_of_surf)
                                Result = list_of_surf
                            else:
                                Result = Surface
                        else:
                            Result = Surface
                    return Result
                finally:
                    self.Message = "Trim surfaces and close edges "


        # Surface面积排序
        class GeometryArea(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Area sort",
                                                                   "E5",
                                                                   """Sort by area of face""",
                                                                   "Scavenger",
                                                                   "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f078e5e4-1f07-452f-a4d8-64babb1a4b9b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "Geometry such as face, Brep, etc ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "The sorted geometry")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Area_Arc", "A", "The sorted area")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Centroid", "C", "barycenter")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                if isinstance(p0, Rhino.Geometry.Brep) and p0.Faces.Count == 1: p0 = p0.Faces[0].DuplicateSurface()
                result = self.RunScript(p0)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARgSURBVEhL3ZVtTFtlFMdvQFcGYxSHvOiKbFEKvb1vbXmRAR0DWgrYoTEOcMbXD5tmyLLFD2Yf1C8zm8TE6TQh84O6jTIwgxZKgRYKyAqbM5uJi24xcdEQY9wSk8VkmR7Pee7T0o5Pzm/+k39yn3PPvb/znPPcVvj/yK4olQ6Ho1NV1Qd5KEWaJtU7HFqnJEm5PFSB/gz9OfoL9Cn0afQA2oc+iTaidUlW8apN00CW5SgPJYRgTZElsON9BLzKwx+XZG2BTlMXPGPaBV2mbnb9QsmLoBgVwPvX0GkskySKliuS1QqKLENNTY2Dh5nwpSdUjCuSBLLV2sPDsdcf64Ur7u/h3I6lhL/D9ZMPP0WA43oalyiWX8WX/yZL0h1FUWjrTBUVFZusongL712jAtTVHVw/LL0LCw2LMFE3yRyqm4Lo9nlQjRoBDuppXKLF8rOmqmGsdgAhtxsbGzdRHFvWoyoK2O3afkkUAWe0lz0gCDePaR/B3PaFFEDEOQtl2WUEeElP4yIAvmi62m7fZtNUsNlsr1Ecq/8RK/+hvqqqnNqnyfIe9oAg/HHc9gmr+G6AOdtMgOf1NC4GUNUldl1eviJJ1ouVlZV1uCuwKUqv0+nMo50ktWjlPaUP5hu+SgEQUMlhQ+7V07j4Di6wa1F8i6rFyn9B36aX41xKaNA45H3sAUG4eKD0IBtsHEBe3BEDV4GbAB/oaVzYihUEfE3XimIuwfXfVLEsS2MU0zSxXJUVkCyW/bRGfeopbEXAcgqAgHu27iXAnJ7GZbVYrmOLzvElrf2sPTZbO61L5eItbFeiGG/RroKMAhivnYCp+nACQEM/pn1IgFvofJZJwtOztaO2o3TSMxUNtk4+h/3faLfbyy63Xc6dbZtdOOv2e7FNotlszuaP5KBvHpVT5zBZP81syjQR5BWWGRcApM+2RcHvHnubh4SoO1q05F2GUXcwfnqSFegufnZNm2K47iruJkBQT+MK7Q5lTbhDdxDwJg8JQXewKNI6AyMt4y/zULLesBntrC10guIA+viOyEcJ8KuexnUPgNaijKI1c6Bv4WTVaViXto4gq7oHgLbhvg1w5vFhCDtnEgCCjW4LQJ4h7z8DLIZ0A6uWqk4GjNUGoTCjMBVAIsCoK5D4oRpsGswhwJctgd08lCwtMz0TfNVnUgDT9ZG1Owg1h7IWnz5fGXRP/BVujbwf3blsoljMG2sIeyIQbp8/RDGeHldzviGfzYAA8SNKPxcD1YNgSDOsAkbbR/NCnqnfI55ZWPJeoGPZE2gL5E56pv+cRkAMj+pIS+DuNu2zbrTCjDOacorou+Cn6IaexjXS7D/8TcclGHdN3Oh39T9AMb/L33+p41sYc43/1Ffdt54lrmqKWlSc+QhsXr85YVob7zcSIPXfcbh5OH+ubQFGXP4jPCT4XL5Hl7znMTZygIeS5UJ3oHdye9FPcNNPjBmdqqHmoUM+ty/lxlDT0Dunms4+xJf/QoLwD/EreY+V3S4zAAAAAElFTkSuQmCC"
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
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

            def bubbling(self, Face, origin_geo):
                # 面积质量属性
                FaceAMP = [rg.AreaMassProperties.Compute(i) for i in Face]

                Area_Arc = [ap.Area for ap in FaceAMP]  # 面积
                Centroid = [ap.Centroid for ap in FaceAMP]  # 质心
                nice = zip(origin_geo, Area_Arc, Centroid)

                # 字典遍历元组排序
                AREAS = sorted(nice, key=lambda x: x[1], reverse=False)
                # 取值
                Faces = [_i[0] for _i in AREAS]
                Area_Arcs = [_i[1] for _i in AREAS]
                Centroids = [_i[2] for _i in AREAS]
                return Faces, Area_Arcs, Centroids

            def RunScript(self, Geometry):
                try:
                    Face, Area, Centroid = (gd[object]() for _ in range(3))
                    # 判断输入的列表是否都为空
                    structure_tree = self.Params.Input[0].VolatileData
                    temp_geo_list = [list(i) for i in structure_tree.Branches]  # 获取所有数据
                    j_list = filter(None, list(chain(*temp_geo_list)))

                    re_mes = Message.RE_MES([j_list], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Geometry:
                            structure_tree = self.Params.Input[0].VolatileData
                            origin_surface = filter(None, self.Branch_Route(structure_tree)[0][self.RunCount - 1])
                            if origin_surface:
                                gh_surface = map(self._trun_object, origin_surface)
                                Face, Area, Centroid = self.bubbling(gh_surface, origin_surface)
                            else:
                                Face, Area, Centroid = (Geometry for _ in range(3))
                        else:
                            Face, Area, Centroid = ([] for _ in range(3))

                    return Face, Area, Centroid
                except Exception as e:
                    Message.message1(self, "Run error：\n{}".format(str(e)))
                finally:
                    self.Message = 'HAE Area ordering'


        # 计算Surface面积
        class Surface_Area2(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Surface_Area2", "E4",
                                                                   """Breps finds the area：Area divided by divisor，keep decimals in decimal place""", "Scavenger",
                                                                   "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9ee46870-e5b6-4d61-a7af-0ffef80f46e1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Breps", "B", "Brep/Surface object list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Divisor", "D1", "divisor，Default million 1000000")
                DIV_NUMBER = 1000000
                p.SetPersistentData(gk.Types.GH_Number(DIV_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Decimals", "D2", "keep decimal place，default three place")
                INT_NUMBER = 1
                p.SetPersistentData(gk.Types.GH_Number(INT_NUMBER))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Area", "A", "Area")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPMSURBVEhLrZVdbBRVFMdn25IFfBHjUjZpWmJrI7Nz73zP7OzslG4bdR9WGg3RuBiKL4qBRI0afdAUNWoM0JaPqKQPhkiM8qgmAvWBAFXagqExPqyY2IqkIBbbRImY2OM5O7ekrDtLSfwnJ3vPf+6c39xz7+xISxUAxMTw9mUYRpKx1ITK+QSOmbBvSOd8q6HrJa4oQ8KqpTUYwxi95YxkWVznjIGmqqBp/LCwyyoUzJVKKnWVruFvSdhR6lgdXz1VbN4E9bH6XcLDJ9R1jjcDQv5iTLkePBgkxSVJVdUncGV07XpKlieEXU2JNcuTc5/5X8CH9kHAfCC0UQZjjFZgmeYhAmma9pq4JCmyfE5lrISQ4zj+UdiVStTF6sZ38X747oHvYUDbQ4D+8BIK286oBZ7rPiWvW3cEV3GZfGydomsamKa5nSnKJwifLN9ws+owjr+RehNOd43Bic5TMKjtrQDgCgiQdpzNXJbzhqGD53m2oig7ye/p6bkTn/5zBPwkbllQA8bhba3bYbR7HI4ExyIAYgWO42zDNIaF5lSVfYu/V7F1x2gOjr+qANwVk2Innr33OfimaxSOBsNLAjxPORY6QDmFZVkbhEeAhRbFMYb75B0w3n32RvFIgMW5YhoGuK79AuW4yTYVx75fyefzVEzCdp1EwBUao17d3NJbLr5QuCagpaVlOR7VR3zfbxYWVrzPw/PbJjI6ro6us26R7nvfOAAnO0eqAvbq+wkwGE6N0Hy205/PdnGRVqqfnpKKVQJO5b6Gd9i7BHg7nFpFM2n/UfACuGZ5cN72U8JerEgAbfjT92wlQDGcWkVTVvqheTsDl3Tn73O23S7sxULAvkgA7Q/OuT+cGqFhztuHFKVRpJXa/x7uAbWjGmDL2icJkA+nCv0aBMlrfq6I7SnOeNnH57z1hT8zHRtmcTyb7ijOZILHLprmSjH9lUKygMXGbjqiNQGX7PTDkFkP4Pr/jXQW/nEz8EMm0yqm09/DEL1ko91n4Mvg6K0Bk4bTNWu6079oZjkuiKDxtG5NT+nmzxOO0ySmk+obYg1nP8BW0X/QAiQS0IdPtZPzOyjybW3ll4u0u6lpBXl9YXsqv2qtjfHG2UPOxzCSO12GRAIWa37jxhV/pP3dv7v+y8KqJTsRT/x20P6ovJIlAS7bmWfA78TeB1Bys66wa8lYtWzVxQF1EEr589C7dgsBoo9pyba1GdOZvKDbY2dM825h30rN+NEZ2SG/Di+2v0SATaEdocX7cBtahvFpLpGDeCy+J7T+fxFkDL8Vb0mSJP0LdW8OAQ0P96cAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list = self.Branch_Route(tree_par_data)[0]
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list

            def RunScript(self, Breps, Divisor, Decimals):
                try:
                    Area = gd[object]()
                    # 初始化参数
                    digit = ".%uF" % Decimals if Decimals is not None else ".3F"

                    # 判断输入的列表是否都为空
                    j_list, temp_geo_list = self.parameter_judgment(self.Params.Input[0].VolatileData)
                    re_mes = Message.RE_MES([j_list], ['Breps'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 计算
                        Area = [format(rs.SurfaceArea(i)[0] / Divisor, digit) if i else None for i in Breps]
                    return Area
                finally:
                    self.Message = "Trim surfaces and close edges "


        # 曲面或者Brep反转
        class BrepFilp(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepFlip", "E1", """Invert surfaces by vectors""", "Scavenger", "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a5494016-bc1f-4404-86c0-86314ef76601")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep or surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Specified direction（Vector）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "New_Brep", "B", "Brep after processing")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, False)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATBSURBVEhLxZV7bBRVFMa3T2ixpRRofXRru2wL7uzsPHZmZ3b2VWmRBqUNhhaNJkarkhoNxEciBYJBQBqUtIBKSaNE1EJ59N3tdoHSajBBgxoT8UVJSSTioxSsFET7eWZ2o9E+gL/8kl/23s2959t77zlnTf+nFhKvE9uIGuI1YgtRTWwiNhAbiduJG5ckCCVaSUkKDTv5VAGLM0tQNPsezJ9VBDXdDTldhjZTQ37KXNCaa0Savm9SBQKBeI6zL2dZ+xecwwGH3d6ZZc76eQm7BCuUlaiUn8JjUgXqtPrRo/5eHC88gWesK3SD5kiE68jpdCawDLPSzjD9uoE1b84pi9mCcn4ZUY4yrhylXCm2uGrR6gmjO/ABFtx6n26wPhIhoouKP++b4uIp0em4ihUE4X7TVFN5RnzGtU4thG7vEQQpaJfnMDo8TWjV3sdRfxsWZXqRl5y86mJh4czvA4FZ+ud5SW0fcWlfD7s8FWfVpUnRmOOqcM60OWjxtKPJ04qDWjP2eUI4JT+CS4INv4giLogSLjoVQo0gqRgUXRih76D6MCypPw44lQXReGNUmJ2cjSat9W+D/Vo7jijVOC6vwMfKamyxaNhpyWvrF+Q1Ot8R5wTXabg8+EGUPxkQlSdP8vzsaLwxsk1PmI4GtZFO0YFDWgvRjEYtiL10XcGCE/Bk3Ku/wfOR5RGdEZXKs6L6UHQ6VpIkmUVe3JCbnyvTtL+G34Gwv4cethNtniCdqI1O04JwoAcVuU/oBvuNjdeTzWZLpNTc6mBZ8BwHyqaBPKv1Tz/rRxFXhLvZArhZFRvkV+ihQwj6wtho36wbnCbijCCTad06UyzDMAXEHtZuv8rz/MvZWVlv5GTkoEpagxedVXjO+QLq1Hq0aB3GtTWo+6FfI23XT3vjcjgc+dFhapwpfmS39C6lZR+laZiuqAv7yKBR60RX4EMEMop1A72NGBpUvI5LXu+EDzueepdbKo07P0AZ1abtRVDbTbyDXt8B1LBVyEtKOvu5pM0d8hZafhLV9iuy5/ywS6v6VZmfGY0xqdZ6Z/nooY9SHYTxpfwohnkrLggODBJDIo/fnBKuym6DIVHBsKgCbj/VgXZ5wKmVRuNMqEU503KNgjtEmRRSt6NPXo1jrnUGH6mbsCrbhc3mO/d8y8uPnxPkz0b1OhBcPf1OV9mnHDe2EZaVlSUCiIlOc1LjU0cPqE0IecNkEjJO0hglRPXgyzB6klEPZyTlgQFJXayP/6sYURRv4zjuaWp2X/EOvoLmosViWZR2y4zfq6VX8aZ7F95z70Uz1UKk8FpwOHAMy8wP6ga1kTATqLjYOoXqYLfI80YdMDbbMKXsBcbGDN01b96oyIhgGBtektdT4+v+l8HSO8p0g62RSJNI/0+goAtZlg3Z7fYFVHzpKSkp7rQpaah3vY0GrZH60UGjP/1j0IOFmUaqro1EuXn5zElmo3K7fUfQ4Q2h3RtEp0+v5m70FPSBS+N1g4cjy29ezwozRDQojaiX3kKdsx47nbuwTdiBWn47NrHVoCTQDdjI8ptXb0JsAqbGTUVibCLiY+IRFxOnB/yDuEJcJk4S1+9H40hPVQ/hJRRCJPRfOo+wEjlEFpFKTCCT6S/UT0S7ialDIgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.set_vector = None

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def _get_normal_vector(self, _srf):
                # 获取实体所有面
                _srf_list = ghc.DeconstructBrep(_srf)['faces']
                if type(_srf_list) is not list:
                    _srf_list = [_srf_list]
                normal = ghc.SurfaceFrames(_srf_list[0], 1, 1)['frames'][0].ZAxis
                return normal

            def RunScript(self, Brep, Vector):
                try:
                    # 判断输入的列表是否都为空
                    structure_tree = self.Params.Input[0].VolatileData
                    j_list_1, temp_geo_list, geo_path = self.parameter_judgment(structure_tree)

                    New_Brep = gd[object]()
                    re_mes = Message.RE_MES([j_list_1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Brep:
                            normal_vector = self._get_normal_vector(Brep)
                            if Vector:
                                # 检测面朝向与向量之间的夹角关系
                                if rg.Vector3d.VectorAngle(normal_vector, Vector) > math.radians(90):
                                    Brep.Flip()
                                    New_Brep = Brep
                                else:
                                    New_Brep = Brep
                            else:
                                # 向量不输入，默认反转
                                Message.message3(self, "Vector not set，Brep is reversed by default")
                                Brep.Flip()
                                New_Brep = Brep
                        else:
                            New_Brep = Brep
                    return New_Brep
                finally:
                    self.Message = "Brep reversal"


        # 扫出曲面
        class SweepOutFitting(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SweepOutFitting", "E13", """Solve the problem of scanning the original plug-in""",
                                                                   "Scavenger",
                                                                   "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9eba4ae2-0e33-47e3-a47e-14f375581a62")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Sweep_Curve", "S", "A curve that acts as an orbit")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Shape_Curve", "C", "Model curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Brep", "B", "A new Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANHSURBVEhL5ZR9SBNxHMYXhJqRbepkZJSVZU2lRInMtpWlmYaalC8ZvVFSvjDLdup0WlKpEWiZoUxtc6VmJkaU5qYzzTSJNLJ/ytLEBPFtSGKC7Ol3dYHUlq6/gh54uOPuns/3+P2eO9b/rYk76bYjcmrDYPG5B2MqaUWvPHE7c+vvNaZMFk2okvPGlVTXiEKiGyqR6CfLUzF1Nw3DpVJ8kFNKdVbUUubx+Wug8OxWnZLSTpVJgfvpmKmU4SsBT5alYEhB4XMxhf4iCrrydLwrTOx+L09yZKJz61PBmXidgtKDQCdvJ2OMAHvyY9F4MQI1qcHoKYhGf4kY3TdPEcdhSCVDU1b0hIqKXM4gjOtjXlzcTAV5U1USevPj8FgaPi4O2tgncl4xvW/tTlzZJkFlVBRuhB1G4YHTSPILhCzCpyz3ZEhsjjiIzWAMq6fgjOtoCaUfLZHgcfLBaXHwpiou27LaxyZgMMflpr7e6ym0glY89KzDI0812kWdiLQ/DhK1+0GYQ4NFiRWTKimUsYGD/LWLsleb85uuulxDm3cHmrc/wxOBGnWCeuaoJtdf4KjDMXqA0w/CHzRck72kr0AyXhG/T8e1YxV5W/v31wsa0Lqj7TvUkE0aoG9QrKlPO4LNfM5AgO3+ieck3ChqQq3giUE4bZMGjJZlOJ+P9ET4qhA0C9ugFjYYhM62SQPEB1duku4OhFqghUaoNQicbXofOnZ14tCqE/MbYLHAIl/uXkw2s9UgkDa9XGqhBi072lEtbIJGUIvzDqEwY7H4DMao+KHLw/QvvF8aBNOm4XSTqgQayJwo5C7zQgvPsbPZjpdC/hN/7r/VQitF5ZYqaEVPjcJbSJuue5QigeuGe2zzDtgtCmbic8p2D8//SzvpunF4K3LdbyGJbY/P3MUZABYw2Xkp4pLLZaN91wgbUe5Vixib9TT8ApOZvzhmnKIqz2o0iAw35xmpYgxpSrmVWRcTMU1ubLcO+oP6+RuYbfpboN8+wWYdZpZxQpmISTL35+0deOP79vsS/epXPq+RT6p7g80egkhkwWRMkq07x0Of6ZoN2Ya035zhkokUh0i0ca3lzPMmy5zYl9jPmC2Jm3mOXHL+L4jF+gY/tnp0YF4HUQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list = self.Branch_Route(tree_par_data)[0]
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list

            def RunScript(self, Sweep_Curve, Shape_Curve):
                try:
                    Brep = gd[object]()
                    j_list_1, temp_sc_list = self.parameter_judgment(self.Params.Input[0].VolatileData)
                    j_list_2, temp_cs_list = self.parameter_judgment(self.Params.Input[1].VolatileData)

                    try:
                        Sweep_Curve = Sweep_Curve.ToNurbsCurve()
                    except:
                        Sweep_Curve = Sweep_Curve

                    try:
                        Shape_Curve = Shape_Curve.ToNurbsCurve()
                    except:
                        Shape_Curve = Shape_Curve

                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['S end', 'C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if not Sweep_Curve or not Shape_Curve:
                            Brep = None
                        else:
                            Brep = rg.Brep.CreateFromSweep(Sweep_Curve, Shape_Curve, 1, 1.0)[0]
                    return Brep
                finally:
                    self.Message = 'Swept surface'


        # 曲面挤出（曲线修剪）
        class Curve_Trim_Offset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Curve_Trim_Offset", "E14",
                                                                   """trim curve，select extrusion，extrud surface，If not input the extrusion quantity，then output the trimmed line """, "Scavenger",
                                                                   "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("6ebbbf0d-5bf7-4833-a961-e0f80e578884")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve to be trimmed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Type", "T", "Extrusion type，{0： Line， 1： Arc， 2： Smooth}")
                DEFAULT_TYPE = '0'
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String(DEFAULT_TYPE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Start", "S", "The length of extension of the start of the curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "End", "E", "The length of extension of the end of the curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Extrusion", "V", "As a reference for extrusion（It could be a vector or a curve）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Move", "M", "Vector of moving objects")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Objects", "O", "Processed objects（Surface or curve）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                result = self.RunScript(p0, p1, p2, p3, p4, p5)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAR6SURBVEhLzVV9TJR1HL8TgiIyCFk0mcFxSR7HPc/v7nkhBQ4kipYcrxIKDKQNZgEZUctwUivKZGrA3XH2R9KMJW2tTCcer8odbyodRAJKiUKbSC43e9HW5rfv7/FRXoaDrdb6bJ89v8/3+/u+PS+/R/EfApTyYknQ8OYAhjfnsbxlL17fJ6LVZDBUeMnuudAYzd4MXzNE+LpKg6HgPtm8IAixrCFCXQPLW6+zXO14ILe/UcXZjrC8eYoI1mnCWypDQ19/SN5+B6Bk+I9SiLj/AhFtlzBBoVqoXi47JehFq4EVrI1EsP3BCnXHWc5ipPZbvCruliFYUKurPYlYm4nxZ/WibVon1LxoNFa4S8EzMLqzgqUMJ5nEBFdxqi6Gq2lCnsPkv6L9KGOoEeTNEqb0wijyG1lKwOlK8NaNEVL1uGyaj4plrKE2Hu/tOyxn3cNw1gJG3BckO+cAk/deJkKDLOdDqTCO596/ESo8ZINCfT7BU14uCYsUUCj4vmQ/3WDyafZCWlnkpc2+vCstTDeSYtePZTxL/QzVZ1ObyWh6ghQwD1cWK0Ch7U/s5G5kg24o+Xu9Mzkk3GWaItOZgIW/inRs9tW6TD9TzQwmHWFcST5ymIRrXITjmkGsl+XC0J1J3G64ugmY4dRJlEpdv6meu5kDWldSj+TvNzVQrRtM6qYaQd93OuFOZxhz+YBq9U+4bkTuReYig5EzIB2JalWVuGVNe8IVdiKjUehN16z9K99EJjdOsedTXxHHXwgio2nZYWPJv6yq5b/GkHE/T3/I8g+EAW04dGl08HKgCPEBG0D1YAi4Kd1u4p5sKfksFChXuP+5aiAWnrDHf4I60z3D71Do5Abwz19tQ93kE/XYDfXEc5CTuxXsuh4Yj3obfiMa+J1o4VxUDTjjhsAR0wWsDwHc/yZNOhulqmXBUPx8GTCT6bAyUwM6RRhEFydC8A/PQFZsPnwZ0AjbK3ZB+MVUaNh0GBz6ZsC3CCb0T8OxqBY4HtUGzthu4H0FWqD0dtoZvBrxyFMwwo/Ae6XVQDu3FH0Kp0J7Ie/jN2DdcA4cTmmCPk0P5NheA+13JvgspRmGyTY4I5bD0egusGORzhgncL78wgWooxNHdBInFH+4E3aUV4FT74DWiDYwfV4Iu0rM2PVtnYT6gxIrnOBo58eQLUst4ITmqFbo4DugTWyHpmg7tKxrxXUbtKxtnadbULdicsrmRQtsu1OAbqQBs2mPnGubryXbPykwm9TfbjwpPdCe9X132R3bB6fj+u/5kEuYh1k4GeO4Z4F24wlMdAo6MPlBoQHeDauEl0KKIC9oCxSoCuGtJ8vhAFcPxEe/8ASsDwvfxg9I3Thiu6Rp6JUm7V7fC4civoBC1VYIW64Fj2UeNMmPyA4kPa7tyEHkdfzQqG8Hcg6KvN29IWVlqtTJHmYf1LBm2K2rgmJ1CUSviAYvNy8aSI8P2p0GOf+HQvEokn7F8ZKaBXqIZSEPIl1Ier5MIy8iO5G7kZHIfw0PIOlv8+6/4n8IheJvHpaDPXCnBmIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._curve_style = None
                self.dict_factor = {'-': ['Trim', None], '+': ['Extend', 'rg.CurveExtensionStyle.{}']}
                self.curve_of_type_list = [rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.ArcCurve]

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list = self.Branch_Route(tree_par_data)[0]
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list

            def parameter_handling(self, par):
                par_factor = self.dict_factor[par[0]]
                line_length = par[1]
                type_of_line = par_factor[1].format(self._curve_style) if par_factor[1] is not None else None
                return par_factor, line_length, type_of_line

            def processing_curve(self, first_cutting_line, first_data, second_data):
                first_factor, first_line_length, first_type_of_line = self.parameter_handling(first_data)

                second_factor, second_line_length, second_type_of_line = self.parameter_handling(second_data)
                after_shear = eval('first_cutting_line.{}(rg.CurveEnd.Start,first_line_length)'.format(
                    first_factor[0])) if first_type_of_line is None else eval(
                    'first_cutting_line.{}(rg.CurveEnd.Start,first_line_length,{})'.format(first_factor[0],
                                                                                           first_type_of_line))
                result_line = eval('after_shear.{}(rg.CurveEnd.End,second_line_length)'.format(
                    second_factor[0])) if second_type_of_line is None else eval(
                    'after_shear.{}(rg.CurveEnd.End,second_line_length,{})'.format(second_factor[0],
                                                                                   second_type_of_line))
                return result_line

            def create_extrude(self, will_ex_curve, ex_data):
                ex_brep = None
                if type(ex_data) is rg.Vector3d:
                    ex_brep = rg.Surface.CreateExtrusion(will_ex_curve, ex_data)
                elif type(ex_data) is rg.NurbsCurve:
                    ex_brep = rg.SumSurface.Create(will_ex_curve, ex_data)
                return ex_brep

            def str_handle(self, str_data):
                if str_data is not None:
                    symbol = '+' if str_data[0].isdigit() is True else '-'
                    num = abs(float(str_data))
                else:
                    symbol = '+'
                    num = 0
                return symbol, num

            def init_movement(self, object, moving_vector):
                object.Translate(moving_vector[0], moving_vector[1], moving_vector[2])
                return object

            def RunScript(self, Curve, Type, Start, End, Extrusion, Move):
                try:
                    Objects = gd[object]()
                    try:
                        Extrusion = Extrusion.ToNurbsCurve()
                    except:
                        Extrusion = Extrusion

                    try:
                        Curve = Curve.ToNurbsCurve()
                    except:
                        Curve = Curve

                    j_list_1, temp_curve_list = self.parameter_judgment(self.Params.Input[0].VolatileData)

                    re_mes = Message.RE_MES([j_list_1], ['Curve'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if int(Type) > 2:
                            Message.message2(self, "KeyError：'{}'不在范围内！".format(Type))
                        elif not (type(Extrusion) is rg.Vector3d or type(Extrusion) is rg.NurbsCurve):
                            Message.message2(self, "V端只能输入向量和线段")
                        else:
                            _style = {'0': 'Line', '1': 'Arc', '2': 'Smooth'}
                            self._curve_style = _style[Type]
                            first = self.str_handle(Start)
                            second = self.str_handle(End)
                            if Curve:
                                curve_of_handle = self.processing_curve(Curve, first, second)
                                extrusion_Surface = curve_of_handle if Extrusion is None else self.create_extrude(
                                    curve_of_handle, Extrusion)
                                Objects = extrusion_Surface if Move is None else self.init_movement(extrusion_Surface,
                                                                                                    Move)
                            else:
                                Objects = None
                    return Objects
                finally:
                    self.Message = 'surface extrusion'


        # 两曲面间夹角
        # class SurfaceAngle(component):
        #     def __new__(cls):
        #         instance = Grasshopper.Kernel.GH_Component.__new__(cls,
        #                                                            "RPP_Sur_Angle", "E11", """Find the Angle between the two faces and the supplementary Angle """, "Scavenger", "C-Surface")
        #         return instance
        #
        #     def get_ComponentGuid(self):
        #         return System.Guid("76f16ac2-4647-423f-ba46-202356f4b55f")
        #
        #     @property
        #     def Exposure(self):
        #         return Grasshopper.Kernel.GH_Exposure.secondary
        #
        #     def SetUpParam(self, p, name, nickname, description):
        #         p.Name = name
        #         p.NickName = nickname
        #         p.Description = description
        #         p.Optional = True
        #
        #     def RegisterInputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_Brep()
        #         self.SetUpParam(p, "G1", "G1", "First face")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        #         self.Params.Input.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_Brep()
        #         self.SetUpParam(p, "G2", "G2", "Second face")
        #         p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        #         self.Params.Input.Add(p)
        #
        #     def RegisterOutputParams(self, pManager):
        #         p = Grasshopper.Kernel.Parameters.Param_Number()
        #         self.SetUpParam(p, "Angle1", "A1", "The Angle between the faces")
        #         self.Params.Output.Add(p)
        #
        #         p = Grasshopper.Kernel.Parameters.Param_Number()
        #         self.SetUpParam(p, "Angle2", "A2", "Supplementary angles between faces")
        #         self.Params.Output.Add(p)
        #
        #     def SolveInstance(self, DA):
        #         p0 = self.marshal.GetInput(DA, 0)
        #         p1 = self.marshal.GetInput(DA, 1)
        #         result = self.RunScript(p0, p1)
        #
        #         if result is not None:
        #             if not hasattr(result, '__getitem__'):
        #                 self.marshal.SetOutput(result, DA, 0, True)
        #             else:
        #                 self.marshal.SetOutput(result[0], DA, 0, True)
        #                 self.marshal.SetOutput(result[1], DA, 1, True)
        #
        #     def get_Internal_Icon_24x24(self):
        #         o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOhSURBVEhLzVVbbExhEN5a1a1tqnarSysam150z/2yu6fbbWtbS0UbCSGCVkRChPBARRNJeaJ1e0HwICIiNK6pdSulUVWl7rVBhCCiiSAePJBmzBynm90qseGhX/Jlzz8z/3wzc/7/rGlIQRTFMaWlQpqxjB9J5uSmLEtWV6YlsysxIXG3YdahaUIWx7KfWIZ5xfO81TDHByVNeX2l9Co0F4XAaXV2GGYdHMetlkQRREEAFJhlmOODZvOFb5bdgsslrZCfkn/ZMOvAynt4nnsi8OwbxuW6ZJjjg9emha8HbsDF4hbITcmNCLjdAkPVy6I4X+T5Op7jqIsM8kmSVKXKcp0sy5ogCAFJELahb7miKIn65mj8TgBnvxWTfqdnr9froDHhyFbQGoWbZUkC7PAL2YlUDMuy68kfg8EE6uvrh+FI3qPIc6zMjxWXYLKPaOsmPyY7LPA8uAoKelVVnYcdPKM1wzBnyR+DwQSw9WIaCQoAbex/RpE+v98/BgX2Y1Jan6F4j6oeoy5Q4BytYzCYALZ6kJK63VIJVs8TUbTSOE2rJEncGS3gdisnDIEQrWMQLZBnzQuZeJOVqkaRNiMkAo5lXmLSd5IkhFRZAdblukp2t6K0qAquWbZdD4xGTAfW3HMmjykVq9muKILHCIkAT8xUjmE2K6K4BG94A3ZTQ3YcUTWetgYUWKwHRmPAiFoN8/9DtECONeeXsfwzogWyR2a/RVMD0qY7/w5OZHWyOfkI/v55RPipoHNcgTyKtJN/ENBtrrSYLTuENPHOnPFzv23hGuGAehDsI+wtP0OiMOAdXDHMM5Grfj6a6CtahNxA/hnjKj+vn1QHhzyHobX0GtyZchceBB9BeNpTKLL7v2FcOm2KwGPzhm+V34aOQCe9g/6L4kZey0oefyyQUf52Rc5K2CvvhwvFl4Bi7wcfwt0p96E90AEnfaehATtYmF3dhyN+jPsK9Az98KUXhU/6TsGavFrA/4RezaY9qsle1Ldd2AFnfM3QUdYJ94IPkA+hs6wLQv7zsEvaA0udy6A4veSlI8lBs1+CzNcTDkQwIxie5qiABRMWQpN2HNomt0M3VkdV3i7v1j/jNF8qoMJR8WGi1Xket9Ui6Z4kUY4/YsbYqnBt/jrY6NoEz6e/QIHrcFRr0tezMmd/ZUaxN80J5s0YOhU5Wt8UD8Q0sZcECu2Fetve0d6e1OGp+9A1FzlBD/pHrEU2GqTvfQJyKMNk+gEi3JSbOid9gQAAAABJRU5ErkJggg=="
        #         return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))
        #
        #     def Branch_Route(self, Tree):
        #         """分解Tree操作，树形以及多进程框架代码"""
        #         Tree_list = [list(_) for _ in Tree.Branches]
        #         Tree_Path = [list(_) for _ in Tree.Paths]
        #         return Tree_list, Tree_Path
        #
        #     def parameter_judgment(self, tree_par_data):
        #         # 获取输入端参数所有数据
        #         geo_list, geo_path = self.Branch_Route(tree_par_data)
        #         if geo_list:
        #             j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
        #         else:
        #             j_list = False
        #         return j_list, geo_list, geo_path
        #
        #     def Point(self, pts):  # 获取所有点坐标信息
        #         for i in pts:
        #             yield i.Location
        #
        #     def Count(self, num1, num2):  # reduce调用+方法
        #         return num1 + num2
        #
        #     def CP(self, PTS):
        #         Pt1, Pt2, Pt3, Pt4 = next(PTS), next(PTS), next(PTS), next(PTS)
        #         Cx = reduce(self.Count, [Pt1[0], Pt2[0], Pt3[0], Pt4[0]]) / 4
        #         Cy = reduce(self.Count, [Pt1[1], Pt2[1], Pt3[1], Pt4[1]]) / 4
        #         Cz = reduce(self.Count, [Pt1[2], Pt2[2], Pt3[2], Pt4[2]]) / 4
        #         Center_PT = rg.Point3d(Cx, Cy, Cz)
        #         Plane_PT = rg.Plane(Center_PT, Pt1, Pt2)
        #         return Center_PT, Plane_PT
        #
        #     def Angle(self, Pla1, Pla2):
        #         zais1 = Pla1.ZAxis
        #         zais2 = Pla2.ZAxis
        #         angle = rg.Vector3d.VectorAngle(zais1, -zais2)
        #         return angle
        #
        #     def RunScript(self, Geo1, Geo2):
        #         try:
        #             angle, angle2 = (gd[object]() for _ in range(2))
        #             j_bool_f_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
        #             j_bool_f_2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
        #
        #             re_mes = Message.RE_MES([j_bool_f_1, j_bool_f_2], ['Geo1', 'Geo2'])
        #             if len(re_mes) > 0:
        #                 for mes_i in re_mes:
        #                     Message.message2(self, mes_i)
        #             else:
        #                 if not Geo1 or not Geo2:
        #                     angle, angle2 = (None for _ in range(2))
        #                 else:
        #                     ptsx = self.Point(Geo1.Vertices)
        #                     ptsy = self.Point(Geo2.Vertices)
        #                     cptx, cpax = self.CP(ptsx)
        #                     cpty, cpay = self.CP(ptsy)
        #                     angle = math.degrees(self.Angle(cpax, cpay))
        #                     angle2 = 180 - angle
        #             return angle, angle2
        #         finally:
        #             self.Message = 'The Angle between two surfaces'

        class SurfaceAngle(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Sur_Angle", "E11",
                                                                   """Find the Angle between the two faces and the supplementary Angle """,
                                                                   "Scavenger", "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("76f16ac2-4647-423f-ba46-202356f4b55f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Geo1", "G1", "First face")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Geo2", "G2", "Second face.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle1", "A1", "The Angle between the faces")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle2", "A2", "Supplementary angles between faces")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOhSURBVEhLzVVbbExhEN5a1a1tqnarSysam150z/2yu6fbbWtbS0UbCSGCVkRChPBARRNJeaJ1e0HwICIiNK6pdSulUVWl7rVBhCCiiSAePJBmzBynm90qseGhX/Jlzz8z/3wzc/7/rGlIQRTFMaWlQpqxjB9J5uSmLEtWV6YlsysxIXG3YdahaUIWx7KfWIZ5xfO81TDHByVNeX2l9Co0F4XAaXV2GGYdHMetlkQRREEAFJhlmOODZvOFb5bdgsslrZCfkn/ZMOvAynt4nnsi8OwbxuW6ZJjjg9emha8HbsDF4hbITcmNCLjdAkPVy6I4X+T5Op7jqIsM8kmSVKXKcp0sy5ogCAFJELahb7miKIn65mj8TgBnvxWTfqdnr9froDHhyFbQGoWbZUkC7PAL2YlUDMuy68kfg8EE6uvrh+FI3qPIc6zMjxWXYLKPaOsmPyY7LPA8uAoKelVVnYcdPKM1wzBnyR+DwQSw9WIaCQoAbex/RpE+v98/BgX2Y1Jan6F4j6oeoy5Q4BytYzCYALZ6kJK63VIJVs8TUbTSOE2rJEncGS3gdisnDIEQrWMQLZBnzQuZeJOVqkaRNiMkAo5lXmLSd5IkhFRZAdblukp2t6K0qAquWbZdD4xGTAfW3HMmjykVq9muKILHCIkAT8xUjmE2K6K4BG94A3ZTQ3YcUTWetgYUWKwHRmPAiFoN8/9DtECONeeXsfwzogWyR2a/RVMD0qY7/w5OZHWyOfkI/v55RPipoHNcgTyKtJN/ENBtrrSYLTuENPHOnPFzv23hGuGAehDsI+wtP0OiMOAdXDHMM5Grfj6a6CtahNxA/hnjKj+vn1QHhzyHobX0GtyZchceBB9BeNpTKLL7v2FcOm2KwGPzhm+V34aOQCe9g/6L4kZey0oefyyQUf52Rc5K2CvvhwvFl4Bi7wcfwt0p96E90AEnfaehATtYmF3dhyN+jPsK9Az98KUXhU/6TsGavFrA/4RezaY9qsle1Ldd2AFnfM3QUdYJ94IPkA+hs6wLQv7zsEvaA0udy6A4veSlI8lBs1+CzNcTDkQwIxie5qiABRMWQpN2HNomt0M3VkdV3i7v1j/jNF8qoMJR8WGi1Xket9Ui6Z4kUY4/YsbYqnBt/jrY6NoEz6e/QIHrcFRr0tezMmd/ZUaxN80J5s0YOhU5Wt8UD8Q0sZcECu2Fetve0d6e1OGp+9A1FzlBD/pHrEU2GqTvfQJyKMNk+gEi3JSbOid9gQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def data_polishing_list(self, data_a, data_b):
                """树形列表:数据自动补齐"""
                fill_count = len(data_a) - len(data_b)
                data_a_new, data_b_new = data_a, data_b
                if fill_count == 0:
                    pass
                elif fill_count > 0:
                    data_a_new = data_a
                    data_b_new += [data_b[-1]] * fill_count
                else:
                    data_a_new += [data_a[-1]] * -fill_count
                    data_b_new = data_b
                return data_a_new, data_b_new

            def Branch_Route_2(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def Delete_None_Tree(self, Data_List, Data_List_Paths, Name):
                """树形数据删除空值"""
                HavaData_Tree, NullData_Tree, _null = gd[object](), gd[object](), 0
                for i_path in range(len(Data_List_Paths)):
                    if len(Data_List[i_path]) == 0:
                        NullData_Tree.AddRange(Data_List[i_path], Data_List_Paths[i_path])
                        _null += 1
                    else:
                        HavaData_Tree.AddRange(Data_List[i_path], Data_List_Paths[i_path])
                if _null > 0:
                    Message.message3(self, "%s 中含有空树形，请检查（并不影响其他输出）" % Name)
                return HavaData_Tree, NullData_Tree

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route_2(tree_par_data)
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def Angle(self, Geo_An):
                # 调用Geo平面方法，得出Plane。此类型不包含Mesh
                """
                import Geometry_group as HaeGeo
                GeoPlane = HaeGeo.GeoCenterPlane()
                """
                if Geo_An[0] and Geo_An[1]:
                    GeoPlane = HaeGeo.GeoCenterPlane()
                    zais1 = GeoPlane.Brep_Plane(Geo_An[0]).ZAxis
                    zais2 = GeoPlane.Brep_Plane(Geo_An[1]).ZAxis
                    angle = math.degrees(rg.Vector3d.VectorAngle(zais1, zais2))
                    reflex_angle = 180 - angle
                else:
                    angle, reflex_angle = None, None
                return [angle, reflex_angle]

            def Run_Angle(self, Geo_tree):
                _A1, _A2 = self.data_polishing_list(list(Geo_tree[0]), list(Geo_tree[1]))
                Rs_ = ghp.run(self.Angle, zip(_A1, _A2))
                Rs_angle = [_an[0] for _an in Rs_]
                Rs_angle_Reflex = [_an[1] for _an in Rs_]
                return Rs_angle, Rs_angle_Reflex

            def RunScript(self, Geo1, Geo2):
                try:
                    angle1_Tree, angle2_Tree = (gd[object]() for _ in range(2))
                    # 获取输入端数据
                    Geo1_list_1, temp_Geo1_list_1, Geo1_path = self.parameter_judgment(Geo1)
                    Geo2_list_1, temp_Geo2_list_1, Geo2_path = self.parameter_judgment(Geo2)
                    Geo_NickName = [self.Params.Input[0].NickName, self.Params.Input[1].NickName]

                    # 进行判定-是否输入，是否存在空列表。并区分出空列表分支
                    re_mes = Message.RE_MES([Geo1_list_1, Geo2_list_1], Geo_NickName)
                    angle1Have, angle1_Tree = self.Delete_None_Tree(temp_Geo1_list_1, Geo1_path, Geo_NickName[0])
                    angle2Have, angle2_Tree = self.Delete_None_Tree(temp_Geo2_list_1, Geo2_path, Geo_NickName[1])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return angle1_Tree, angle2_Tree
                    else:
                        with Rhino.RhinoDoc.ActiveDoc:
                            # 数据预处理
                            Brep1Have_L, B1_path = self.Branch_Route_2(angle1Have)
                            Brep2Have_L, B2_path = self.Branch_Route_2(angle2Have)
                            Path = B1_path if len(B1_path) >= len(B2_path) else B2_path
                            # 角度求值
                            _A1, _A2 = self.data_polishing_list(Brep1Have_L, Brep2Have_L)
                            Rs_angle, Rs_angle_Reflex = zip(ghp.run(self.Run_Angle, zip(_A1, _A2)))
                            # 数据返回
                            for _i in range(len(Rs_angle)):
                                angle1_Tree.AddRange(Rs_angle[_i], Path[_i])

                            for _i in range(len(Rs_angle_Reflex)):
                                angle2_Tree.AddRange(Rs_angle_Reflex[_i], Path[_i])
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return angle1_Tree, angle2_Tree
                finally:
                    self.Message = 'The Angle between two surfaces'


        # 曲面按照参照平面排序
        class SurfaceSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SurfaceSortByXYZ", "E15", """Surface sort，Enter xyz axis to sort，can be sorted by reference plane""", "Scavenger", "C-Surface")
                return instance

            def __init__(self):
                self.dict_axis = {'X': 0, 'Y': 1, 'Z': 2}

            def get_ComponentGuid(self):
                return System.Guid("c5d243ad-a60f-46ff-8314-851545506bc1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "Surface list data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Axis (x, y, z)")
                AXIS = 'X'
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_String(AXIS))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "Reference plane")
                REF_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(REF_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Sort_Geo", "G", "The ordered surface")
                self.Params.Output.Add(p)

            def sort_geo(self, set_data):
                # 获取片段集合中所有点和平面
                origin_geo, pl = set_data
                geometry_list = map(self._trun_object, origin_geo)
                pl = self._trun_object(pl)
                if len(geometry_list):
                    # 新建字典
                    dict_pt_data = dict()
                    from_plane = rg.Plane.WorldXY
                    # 获取转换过程
                    xform = rg.Transform.PlaneToPlane(pl, from_plane)
                    # 取线的中心点
                    pts = [HaeGeo.GeoCenter().center_box(geo) for geo in geometry_list]
                    # 复制点列表
                    copy_pt = [rg.Point3d(_) for _ in pts]
                    # 将转换过程映射至点集合副本中
                    [_.Transform(xform) for _ in copy_pt]
                    dict_pt_data['X'] = [_.X for _ in copy_pt]
                    dict_pt_data['Y'] = [_.Y for _ in copy_pt]
                    dict_pt_data['Z'] = [_.Z for _ in copy_pt]
                    # 按轴排序，最后结果映射只源点列表中
                    zip_list_sort = zip(dict_pt_data[self.axis], origin_geo)
                    res_origin_geo = zip(*sorted(zip_list_sort))[1]
                else:
                    res_origin_geo = []
                return res_origin_geo

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Sort Point'
                # 初始化输出端数据内容
                Sort_Geo = gd[object]()
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    # 确定不变全局参数
                    self.axis = str(p1[0][0]).upper()
                    self.j_bool_f1 = self.parameter_judgment(p0)[0]
                    re_mes = Message.RE_MES([self.j_bool_f1], ['G end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 多进程方法
                        def temp(tuple_data):
                            # 解包元组元素
                            origin_geo_list, origin_pl_list, origin_path = tuple_data
                            # 若平面有多个，重新赋值
                            o_pl_len = len(origin_pl_list)
                            if o_pl_len == 1:
                                origin_geo_list = [origin_geo_list]
                            else:
                                origin_geo_list = [origin_geo_list[:] for _ in range(o_pl_len)]
                            # 每个单元切片进行主方法排序
                            sub_zip_list = zip(origin_geo_list, origin_pl_list)
                            res_cur_list = map(self.sort_geo, sub_zip_list)
                            # 每个单元切片是否有数据输出
                            if res_cur_list:
                                ungroup_data = self.split_tree(res_cur_list, origin_path)
                            else:
                                ungroup_data = self.split_tree([[]], origin_path)
                            return ungroup_data

                        # 数据匹配
                        geo_trunk, geo_path_trunk = self.Branch_Route(p0)
                        pl_trunk, pl_path_trunk = self.Branch_Route(p2)
                        geo_len, pl_len = len(geo_trunk), len(pl_trunk)
                        if geo_len > pl_len:
                            new_geo_trunk = geo_trunk
                            new_pl_trunk = pl_trunk + [pl_trunk[-1]] * (geo_len - pl_len)
                            path_trunk = geo_path_trunk
                        elif geo_len < pl_len:
                            new_geo_trunk = geo_trunk + [geo_trunk[-1]] * (pl_len - geo_len)
                            new_pl_trunk = pl_trunk
                            path_trunk = pl_path_trunk
                        else:
                            new_geo_trunk = geo_trunk
                            new_pl_trunk = pl_trunk
                            path_trunk = geo_path_trunk
                        zip_list = zip(new_geo_trunk, new_pl_trunk, path_trunk)
                        # 获得结果树列表
                        iter_ungroup_data = ghp.run(temp, zip_list)
                        Sort_Geo = self.format_tree(iter_ungroup_data)

                # 将结果添加进输出端
                DA.SetDataTree(0, Sort_Geo)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARtSURBVEhLnZV9TBtlHMcPsogSZxgaNufWAnuRTXQVRtgYUF5K2yvXQjfAKCjbWBzGBbbMsEViiEZINEYYQ3AvDF3IdKMFWt567fWutFAoK4O9CWR/jDj+nNE/jC8Z8vOeu4e+QNXIJ/mlzz2/b++Tu+fuOeL/snB4Yet86fxuqINwPBUEABGGh37Wha+rkkZKu2IjY1EZ4iPjDZJIiTGcCK/GER8sZXc6qVG4qDZuwVM+bBrbF3aS++F60fVn8JSILEo2R2fYoD99UCgmk4W2pK8hjAirxxEfFvWgmyE5aMnulOIpAe+75kiapH+6pZ8GC8kU4mmB57Qvah9P5HrBlmkXajxnAuoTG4DvBQURNGlx2UgWLihuSPCUAKOlywbVQzMDVN+1IRXN4mmB+DLJ24tjOR6wZFiFQuPqHSeRYJ8Y8fNPAlpjcfUrBz/oqW6MGlAPLjJaZiNuEXuOx1cKJw0UVMQdQ4JXxIifUALvm9wLjIYBq5rhrKStY7xgAvirOI7bRMqJ7VWrBOWxh5Fgpxjxsyz4NkDAaK0nGZJ9bFKbPu8lzY12rZ2j1VYvbhNJ7217f5XgSOxRJNglRvysFPChsCFy6FGvsv8zIcBjLLma6NKNQF8enYiOd7wjLV9aKUBXxfdSUCCQUAJDvkHRIe+IEgKYLqor15hnjEHjDbrNhT8HCkazx6Bu98dIoEWBQELdov8kNXrfveEsF6B3AQnQuDWpDQlOiQk/axJsitj0XW+aWXjBkAD99qSZICYi5iqO+FiTgOdEs6wFnFkjggBdCRrvj94/x/eC9py1CjJO7TwN7pxx3zqgt7lUUrbI9+LFiMhaBS8Vbyn5I3ChkezDhFq0DkoxIhJKwBbTyZNFk/Wcjqt3FjprHTpHlaXIHY3bAk8pYvJ+RE/PsgDdoibZOSSoECMioQRmyix3Uq7ePuWAkdbQs9P6O2BQmhNwW4S/33cCnyRHlhMuJbfD+oj1n+CIwLKgM9sQtJsuM6xj7/KiVQ8HkRS118PKHT4BJx+GFlkr6ON0Dx+UPhyfq3ikQTmLaohBAqlU/vRS7S/bFsrne+1arhP1XHr7p/x+9GeL/Maz6DiI5A0pEysFF5IugSz6tR47af/t7qFZ8L4x/Q2bb789oLI8mXrrVrP34M1f7x+agYsZlytnjk5u9hR4oEvRXYJPGUza82lBLxu6RZf3tqM1qOwhe17tU/b9PlVwG1iNAywqK9zUTcIINQZfZbbVov87dKzHrBzoQuNQRCg3KhdWLnLjniYkOIYC5zPOq/gd8i9GzQmCUf7kV7KufIl6Tr31yFzxA+AKuHPuInfNVMlUDa2l41BvGQm/ez6ZUc0JGx2q+6pZ+GhXHRIoxAhBdGS1nx6l3OCmPHAt53sOTxP9mv6Dw5TLxH/RWL5GHdTwiIk0HcBtAXVuTC7UvHwGqrZXC3Um4SykRqcu8b2tYkSkW9F9z5HvhIb0hlXfin8Dfd5SQ9TrfAXRKm9KbE5vXvWtDg1B/A2DtsHmaBDYdQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def _trun_object(self, ref_obj):
                """引用物体转换为GH内置物体"""
                if 'ReferenceID' in dir(ref_obj):
                    if ref_obj.IsReferencedGeometry:
                        test_pt = ref_obj.Value
                    else:
                        test_pt = ref_obj.Value
                else:
                    test_pt = ref_obj
                return test_pt

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

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

            # def Get_different_Center(self, brep, type_str):  # 不同的物体求中心点
            #     if "Plane" in type_str:
            #         center = brep.Origin
            #     elif "Circle" in type_str or "Box" in type_str or 'Rectangle' in type_str:
            #         center = brep.Center
            #     elif "Point" in type_str:
            #         center = brep
            #     elif "Arc" in type_str or "Curve" in type_str:
            #         brep = brep.ToNurbsCurve()
            #         center = brep.GetBoundingBox(True).Center
            #     elif "Line" in type_str:
            #         center = brep.BoundingBox.Center
            #     else:
            #         center = brep.GetBoundingBox(True).Center
            #     return center
            #
            # # 求边界框的中心点
            # def center_box(self, Box):
            #     if not Box: return
            #     type_str = str(type(Box))
            #
            #     # 群组物体判断
            #     if 'List[object]' in type_str:
            #         bbox = rg.BoundingBox.Empty  # 获取边界框
            #         Pt = []
            #         for brep in Box:
            #             type_str = str(type(brep))
            #             if "Circle" in type_str or 'Rectangle' in type_str or "Box" in type_str:
            #                 bbox.Union(brep.BoundingBox)  # 获取几何边界
            #             elif "Plane" in type_str or 'Point' in type_str or 'Arc' in type_str:
            #                 Pt.append(self.Get_different_Center(brep, type_str))
            #                 bbox = rg.BoundingBox(Pt)
            #             elif "Curve" in type_str:
            #                 brep = brep.ToNurbsCurve()
            #                 bbox.Union(brep.GetBoundingBox(True))
            #             elif "Line" in type_str:
            #                 bbox.Union(brep.BoundingBox.Center)
            #             else:
            #                 bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))
            #
            #         center = bbox.Center
            #     else:  # 不是群组
            #         center = self.Get_different_Center(Box, type_str)
            #     return center

            # def _other_fun(self, data_list, axis, coord_pl):
            #     xform = rg.Transform.PlaneToPlane(coord_pl, rg.Plane.WorldXY)
            #
            #     for f_index in range(len(data_list)):
            #         for s_index in range(len(data_list) - 1 - f_index):
            #             if not data_list[s_index]:
            #                 continue
            #             first_center_pt = self.center_box(self._trun_object(data_list[s_index]))
            #             if data_list[s_index + 1]:
            #                 second_center_pt = self.center_box(self._trun_object(data_list[s_index + 1]))
            #             first_center_pt.Transform(xform)
            #             second_center_pt.Transform(xform)
            #
            #             first_center_axis = first_center_pt[self.dict_axis[axis]]
            #             second_center_axis = second_center_pt[self.dict_axis[axis]]
            #             if first_center_axis > second_center_axis:
            #                 data_list[s_index], data_list[s_index + 1] = data_list[s_index + 1], data_list[s_index]
            #     return data_list
            #
            # def RunScript(self, Geo, Axis, CP):
            #     try:
            #         Sort_Geo = gd[object]()
            #         j_list_1, temp_geo_list = self.parameter_judgment(self.Params.Input[0].VolatileData)
            #
            #         re_mes = Message.RE_MES([j_list_1], ['Geo'])
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             Axis = Axis.upper()
            #             if Axis not in ['X', 'Y', 'Z']:
            #                 Message.message2(self, "输入了错误的轴！")
            #             else:
            #                 structure_tree = self.Params.Input[0].VolatileData
            #                 origin_surface = self.Branch_Route(structure_tree)[0][self.RunCount - 1]
            #                 Sort_Geo = self._other_fun(origin_surface, Axis, CP)
            #         return Sort_Geo
            #     finally:
            #         self.Message = 'Surface sort'


        # 延伸曲面（不含非规整曲面）
        class ExtendSurface(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ExtendSurface", "E2", """Extended surface（not contain irregular surfaces），extend the surface through inputting four sides of surface""", "Scavenger", "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4b5244c4-8cef-489e-b1ad-6b01e301de7b")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "Surface to be extended")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edges", "E", "Edge of surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "The distance to be extended")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Smooth", "S", "Whether smooth or not")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Surface", "S", "The extended surface")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                if isinstance(p0, Rhino.Geometry.Brep) and p0.Faces.Count == 1: p0 = p0.Faces[0].DuplicateSurface()
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                result = self.RunScript(p0, p1, p2, p3)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUFSURBVEhLrZZ9TBN3GMfr1KlT3MIU3UaWaIIzm7pNM6eW8qbIXLY5sz/2Yha3memSSZCZaaL4tsFcy/UKBTQwRUVjmAK+8tJCLYhQwBcydII4TWRYZRhDS9vrXct99/zaa5QMxT/2TT6559vf3fP87rm736+qp9F+YKwVGKVYVf5FjAYwQrGqIlker4QBHb169VklfDoZRE8+75e+U6yKlzyFnNf9MYtzRHG2wS9aAgOkbMmziPeLJYodXvlO5yTjgG9A7xf/ZD4XmLqHpq/3e2uYzxoQsw+T533CEuYNklBUyMapMPPDyiC6M/fRBQUE19+/mBfdOpYghyX1uFbxkuDcyxJKHutur/c1I2Sw8+kuy1WPtPGxyvjnjsbg897IFoXTGXe7Zv3Sc2epwSfe4wRXafqdriSd4NhJLfGUyLK6SZYj98hyLrXTQcf3qc7wBZh4n8emE1ycYlV60X2dZryBxTTbaJ3LIVCYR5zUJK9r1HucPRS/xMafSnqf5wLndeUolgoKnYWynEJh9NzPPm3P6OuFaowK5DF31UrssHexWCJ2EI9VNLGaBUbZ35AnyzoWMxXIcssKjuuk0D99WQIM/W5semsrsqdlwrCtCun37IgYO4UVuR644DH6hGAn/bH5atv9daYqK8VpxIltNzvdCzYmI3JEBLTf/449Hj/qlzXDNvssjms7cNAJpM7YwK69QASVL0nRvNvxoWKZEgk8QyRfOo9lRm2gBYyUzotIN5px6pXDqNx6nV5JARWJNah5/QyKtW3Y7wHWR/0QLKDv6wrPloSyIvZq+QSJFz02+rBs6Xf/7tjY1IK0slroG25gE1eC1VNXIX3GT8i60o2SvFuoj6rEsfXNyL51HxVLqMDschTvvIwD3SJSolKDBbbTZ63ru780yysU69zOI7ucD5YzVmTx6YtWrMTJ1MswJ1phia9FU1wzzsc1ojzJgvIEM0zRZlTGmgNxlYYgXxFfjXMftNAdKAVC2ue0T+Z67fMUyzRvLLXDHHUCFrUlkCyQhDAtNMGkNqEqJpjUtIji0JjaDFtM08MC+r6+8BzJW7BbHhjgfd7bWZJQzEjrvHZu7bHjOHD0Jqpia4IJlSTD0ZjQ/LCAtr09LLPfkUrP4ZpO6K/71dW3hbHWVFH0UdrPOKRthYkKsJkOlWwoBhUIaXtr6wucfVCL5oymFlVPK0ONxhJsxxDJhmJQgdyenglGybuZWnSb1pw2gyhwjA0ttrIvDHk49FsHquLpDoZpUXWMBTUxVuIsbAmPPGRtb29Yptuxy+gTH3Ci+y+t21FAvuDH1guVX+bvQ+HB9kCBoZ6BSVON+vgGNMTbUKkxoXThcZxSn0FrYhs2z9wyuEXJTRUTd3V3v61YpjdpW4J5+n9bxJLVxdVT8kZwc3gkTUlC5LhIhI2aiEnPTsL88HexIHxBsIBelsfl+v2fU4usWX6x1CgKXzG+OVrMv7cmFWe2dcASVxt4TdmMz8bWomXxJRyafxjqF9UsSQi2uN0jHI/81qrKsNsn84KrhG0a1CKHzuO00Mpp2Xqr88q3pnKkHDmF0zEVqNPUwRpbh2MLS7Fm+lqMHzk+lMRGfE1MIyYQkwkNsZdgY0Fxvb3z2OaiWKZ3iECSiDEReOP5WZgZNhPjRj4XSvyACKy2T9DLynFI0TqnWk6wDb2fCCXuJtje8Crxv2kqwb6ROcSgvyhPlkr1L4sZ0MRj6DAVAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.smooth = None

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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def _extend_surface(self, surf, edge_list, dis_list):
                # 曲面延伸的主函数
                def key_fun(surf, iso_curve, dis):
                    if dis[0] != 0:
                        temp_surf = surf.Extend(iso_curve[0], dis[0], self.smooth)
                        if temp_surf:
                            sub_surf = temp_surf
                        else:
                            temp_surf = surf
                    else:
                        temp_surf = surf
                    iso_curve.pop(0)
                    dis.pop(0)
                    if iso_curve:
                        return key_fun(temp_surf, iso_curve, dis)
                    else:
                        return temp_surf

                iso_type_list = []
                for index, single_edge in enumerate(edge_list):
                    temp_curve_2d = surf.Pullback(single_edge, sc.doc.ModelAbsoluteTolerance)
                    iso_type = surf.IsIsoparametric(temp_curve_2d)
                    iso_type_list.append(iso_type)
                result_surface = key_fun(surf, iso_type_list, dis_list)
                return result_surface

            def _select_edges(self, data_set_coll):
                # 循环查找曲线的最近曲线
                temp_brep, edge_list, dis_list = data_set_coll
                dis_list = dis_list * len(edge_list)
                temp_brep = ghc.DeconstructBrep(temp_brep)['faces']
                if edge_list:
                    curve_list = [_.ToNurbsCurve() for _ in temp_brep.Edges]
                    count = 0
                    new_edge_list, min_index_list = [], []
                    while len(edge_list) > count:
                        edge_list[count].Domain = rg.Interval(0, 1)
                        origin_mid_center = edge_list[count].PointAt(0.5)
                        min_cur_index = 0
                        for cur_index, single_cur in enumerate(curve_list):
                            curve_list[min_cur_index].Domain = rg.Interval(0, 1)
                            single_cur.Domain = rg.Interval(0, 1)
                            mid_center = single_cur.PointAt(0.5)
                            start_mid_center = curve_list[min_cur_index].PointAt(0.5)
                            if cur_index not in min_index_list:
                                if mid_center.DistanceTo(origin_mid_center) < start_mid_center.DistanceTo(origin_mid_center):
                                    min_cur_index = cur_index
                        new_edge_list.append(curve_list[min_cur_index])
                        count += 1

                    result_surf = self._extend_surface(temp_brep.Faces[0], new_edge_list, dis_list)
                    return result_surf

            def _do_main(self, tuple_data):
                # 重新匹配输入端数据
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)
                sur_list, edge_list, dis_list = new_list_data
                # 数据匹配至唯一值
                edge_list = [edge_list] * len(sur_list)
                dis_list = [dis_list] * len(sur_list)
                sub_zip_list = zip(sur_list, edge_list, dis_list)

                res_nurf = map(self._select_edges, sub_zip_list)
                ungroup_data = self.split_tree(res_nurf, origin_path)
                return ungroup_data

            def match_tree(self, *args):
                # 参数化匹配数据
                value_list, trunk_paths = zip(*map(self.Branch_Route, args))
                len_list = map(lambda x: len(x), value_list)  # 得到最长的树
                max_index = len_list.index(max(len_list))  # 得到最长的树的下标
                self.max_index = max_index
                max_trunk = value_list[max_index]
                ref_trunk_path = trunk_paths[max_index]
                other_list = [value_list[_] for _ in range(len(value_list)) if _ != max_index]  # 剩下的树
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
                iter_ungroup_data = map(self._do_main, zip_list)
                temp_data = self.format_tree(iter_ungroup_data)
                return temp_data

            def RunScript(self, Surface, Edges, Distance, Smooth):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result_Surface = gd[object]()
                    # 判断输入的列表是否都为空
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
                    self.smooth = Smooth

                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['S end', 'E end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Result_Surface = self.match_tree(Surface, Edges, Distance)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result_Surface
                finally:
                    self.Message = 'Surface extension'


        # 曲线切割曲面
        class BrepSplitByCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepSplitByCurve", "E12", """Use curves to cut surfaces；
                ps：Need the two to intersect""", "Scavenger", "C-Surface")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("47db7cdf-8a92-4944-91be-32da81b9294b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "The surface that needs to be divided")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Parting line--list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surfaces", "S", "List of cut surfaces")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKbSURBVEhLtdZbSJNhGAfwzXaQucoMMyTxpoYIImpaVnMHzYmRddGJ1kVXFXSCUqibsm4KLzpgQUyJJZoVLe1AU6fW0uaWoCF0uihI6EKhQRcV0cW/53nGB5HbcHM98LvYu+99/t++9/2+b6oF1kqyiWTIpxRWBWknPwnIaZKSKia9hJuyGdJCVpEF1zHyi3DjEbKNzLtWk6NxtBLlrD+Sk8RJDpIjJNoclk2knGlqNRoqzHBa67G3yiGctnpsKduoNMb65ZWozXGgekVNTI6cOpQuK1Pm8FpJ7dBrtfjWNQj4PwEDbyPGvsDX3CoHFywuwJg9hKD9FV7agjG93jyFG6UuJaCUm3NJwGdXL/BkEngQjBj6gGsHGuVgPrsgBfSZB+J6YR3FpeIr8wygX9F7qkUOXmM04ZnFj36zL2pjRWIBjycw6+6DQZ8OtSoN7Wtvwm8didpYkVgA873DPkudTNia24BQ9XjUxorEA7xTeHO1G2raZVq1Fu7yW9IkWnOWeACjxT5Uu10mlWeVY9QWiLkWyQXQWLhrGNlLMmVio6lJLpXX3J+iAM8YMPgenqYLMtGoMaJ73V1p9m9IcgGsJyQh++nupuNRtLRIdpSvaihFAYy27ff7AZhy86TB7rw9c3bVwgL4UtHNN3m5EzqNRpo0F55D8K/1iBsw434aeQZxSEwTwOg0bp84L00Miwy0dTvkGTVseY6QfRytJdfnBOziMwpcbMO024tp18P42h5h9o4fOzfYpVG+IR8dFZ2y8J7KHpwpPKsElHFzLn55hCkkrNfq5kEbTtenhzMNGWGa95vIo0Sfpp8hXzVqDY8zfgNK6UhWkkoIN+Mzvkf4D4DynYakpGqIclmO88D/qMOEA34QAw+oVCrVH7vEX51nUrS0AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def split_surface_with_curves(self, Brep, curves):
                tol = sc.doc.ModelAbsoluteTolerance
                # 将曲线转换为NURBS曲线列表
                nurbs_curves = [crv_ for crv_ in curves]
                # 使用Brep对象的Split方法来分割曲面
                split_breps = Brep.Split.Overloads[IEnumerable[Rhino.Geometry.Curve], System.Double](nurbs_curves, sc.doc.ModelAbsoluteTolerance)

                return split_breps

            def RunScript(self, Surface, Curve):
                try:
                    res_surfaces = gd[object]()
                    # 获取实际参数
                    just_one = 1
                    if self.RunCount == just_one:
                        self.factor_bool_one, self.parameter_one, suf_path = self.parameter_judgment(self.Params.Input[0].VolatileData)
                        self.factor_bool_two, self.parameter_two, curve_path = self.parameter_judgment(self.Params.Input[1].VolatileData)

                    re_mes = Message.RE_MES([self.factor_bool_one, self.factor_bool_two], ['S', 'C'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Surface and Curve:
                            res_surfaces = self.split_surface_with_curves(Surface, Curve)
                        else:
                            res_surfaces = []

                    return res_surfaces
                finally:
                    self.Message = 'Curve division surface'

    else:
        pass
except:
    pass

import GhPython
import System
