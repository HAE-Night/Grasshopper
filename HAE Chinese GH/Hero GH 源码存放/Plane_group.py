# -*- ecoding: utf-8 -*-
# @ModuleName: Plane_group
# @Author: invincible
# @Time: 2022/7/8 11:11

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
from Grasshopper import DataTree as gd
import Grasshopper.Kernel as gk
import scriptcontext as sc
import Rhino
import math
import re
import copy
from itertools import chain
import initialization

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:
        # 平面旋转
        class RotatePlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_RotatePlane", "S2", """The plane rotation and the two objects that follow the plane rotation ，Direction（Direction of the axis of rotation）""", "Scavenger", "F-Plane")
                return instance

            def __init__(self):
                super(RotatePlane, self).__init__()
                self.selective_index = 'X'
                self.switch = None

            def get_ComponentGuid(self):
                return System.Guid("63f44167-e9c5-40e5-9040-9bb9cccbc6fe")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Rotated_Plane", "P", "Original plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Angle", "A", "Angle of rotation，default value is 0.5*pi")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(math.radians(90)))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Direction", "D", "Direction of rotation axis")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation1", "F1", "No.1 geometric objects that follows rotation ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Follow_rotation2", "F2", "No.2 geometric objects that follows rotation")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "New_Plane", "P", "plane after rotation")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object1", "R1", "No.1 geometric objects that follows rotation")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Rotated_object2", "R2", "No.2 geometric objects that follows rotation")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Plane rotation'
                New_Plane, Rotated_object1, Rotated_object2 = (gd[object]() for _i in range(3))
                if self.RunCount == 1:
                    def run_main(tuple):
                        Plane, Angle, F1, F2 = tuple
                        Direction = self.selective_index
                        if Plane is not None:
                            center_point = Plane.Origin
                            New_Plane, Rotated_object1, Rotated_object2 = self.get_new_plane(Plane, F1, F2, Angle,
                                                                                             Direction, center_point)
                        else:
                            New_Plane, Rotated_object1, Rotated_object2 = (None for _i in range(3))

                        return New_Plane, Rotated_object1, Rotated_object2

                    def _do_main(tuple_data):
                        a_part_trunk, b_part_trunk, origin_path = tuple_data
                        new_list_data = list(b_part_trunk)
                        new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                        match_orgin, match_x, match_y, match_z = new_list_data

                        Plane, Angle, F1, F2 = self.match_list(match_orgin, match_x, match_y, match_z)  # 将数据二次匹配列表里面的数据

                        trun_Plane = ghp.run(self._trun_object, Plane)  # 将引用数据转为Rhino内置数据
                        trun_Angle = ghp.run(self._trun_object, Angle)
                        # trun_Angle = [_.Value if _ is not None else _ for _ in Angle]
                        trun_F1 = ghp.run(self._trun_object, F1)
                        trun_F2 = ghp.run(self._trun_object, F2)

                        zip_list = zip(trun_Plane, trun_Angle, trun_F1, trun_F2)
                        zip_ungroup_data = ghp.run(run_main, zip_list)  # 传入获取主方法中

                        New_Plane, Rotated_object1, Rotated_object2 = zip(*zip_ungroup_data)

                        ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                           [New_Plane, Rotated_object1, Rotated_object2])

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
                        New_Plane, Rotated_object1, Rotated_object2 = ghp.run(
                            lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                        return New_Plane, Rotated_object1, Rotated_object2

                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.marshal.GetInput(DA, 2)
                    p3 = self.Params.Input[3].VolatileData
                    p4 = self.Params.Input[4].VolatileData

                    j_list = any([len(_i) for _i in self.Branch_Route(p0)[0]])

                    re_mes = Message.RE_MES([j_list], ['Rotated_Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.selective_index = p2 if p2 is not None else 'X'
                        New_Plane, Rotated_object1, Rotated_object2 = temp_by_match_tree(p0, p1, p3, p4)

                DA.SetDataTree(0, New_Plane)
                DA.SetDataTree(1, Rotated_object1)
                DA.SetDataTree(2, Rotated_object2)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAWtSURBVEhLrZQJUFR1HMfX1NRMFC1xOJbdhT3Y5e3u23vf230sIAu4y+kiaUrjWR6kYqZNFJbKeExjMZORjCEWImZYo2bmgYh4gxwCiYr3AaJueFUI3x7Lm3EmddTqM/ObefM7vt/3+7//PN7zsmnTpt5paWl+Lle8PD4mRu5wOPxSUlJ6d9fS09O97Ha71tP4orw/b45j8sS09amu5NMJcY4/HLHRiI4aiZGREffDw8NPMwyzLjIy8ggTZgNFWbK4sWezYkW2+Z2pkw+6khMxMsIGo14HUqWESkmAVKug12lhMhphs9lA0xaYKRpW1sRksizmJJ7O/IzZkxLjndBpSAiFggaBQLBKIOBPEPH5EewzEyQQxAcGBs4xGvS17BYwcwYmMw3aGgajkUrlpB5ndGLiGMZCQyQUNrIiiWzqpZ7K4ygJxXapRAqCIKDVGVgD1ohmYDBRt8xm83Cu7REmk0ZDhCoQHCwq9vf3H8Cln0Yv30G+w4YO5Y/s12/EqoEDfRv9A8RQk1p2C1u30VdcXw8ul2tAaIjsoooIPcWlnpfe5eVMUmGhcVVKqqTIa7D/fqk0BCq1BmFhYa/xeCk8z1WTB8sWGNgP6XQ6u4/lmawuNGoryuhvrzRHtKEjFkA0urrC22sr9Jt5PN+4YT5BNtagP883Q0oJv6G3SYRB1wyhmlKWPpzGk3jVe/S7i2Xh9MKLZWQXMArojAKuW9F1iQIumoHbFlRuJ3dlTRws8kx4yb2CFcecUJTY4RchivUkn8CgqLjxQcu+P6M/1gnhooKWRU7eh8WfBh9+UK0DWih0NRnRWW8C6liTWxE4WEDs5EZ5/SQ/RVxUt6Ui5Mgot1+WOo3Le+gvlVKimbl7yYKzMJR1QFN6G9rSdvDsGdO76wvHBuTcPEgCp9gNatioZqOBxr3j5q7P3xMqPSLBG5hy1TkXlKeToWxMgjA/ZBmbFouSlq1Vf7AfzEetYCY2wrDiDMhfW6A79BekOTsfsD1D2Hh5yxLR/bsVBqCefmRyOxJHC4m93fo8Ya45X305BcTJBISecEKUOxbBS0r+tGZeAzP9LJjRVQizH4NlXDVMWU3Q/HAVqoqH0KbPLWs+JN2yba3yZkORAh1V7PE0WYBLYTi7S3e5cLlkiseAv1KfqT7vQmiVA4ojTih/rIeuFKBn1oOJr4TVdQKWN2tgTa0Gk1AJ87xGqPe0gyiqwe58EnePG3GsQI7WMg1a6403N6yXLGVl+3rEu/HNUFB+mcRs3/kRe9RXnFAdXwly2z1QcxpgTaoClVYLemKdx4RJqIJ19AloN16G+ijg+3b2hTQVb+7SNMGOollBD3L1QWvLvIn51wj95m0SxTrOooe+g0NISUkClM2xUO87Av2aG6Bm1YOeXAd6fK1HmHGyG7Gb6AouQVPmBn/r1Y4pZNS+G0JF6zmJtstNGAGTFa2kAYsDAuyc9CN83rLlqc7Fg6iaC/JnNwyrzsMyqQ7WMdWgxtXAksyasFsZvmgGsacNAdWAIzOv45ZY/PB3jQHtGiPcbKwWBqdwkv/EZ7hoTZxbdSkKqgNboS2+4zkqJq4SFHtM1Ix6UNNOQrzJDdWem8jO/BptYXY8ZMXvaE3o1FMoFElWcmJPxjuayiDqkkDUTQC56xoMyy94bhI9/SQUeS2QlrgxPWc7GqKTAJkMv7FvvEBG7KgICXXvlikOsxK9epSeTh/+klGn1FfsUB5aA23JPSjzryKouB0J31Vi5/gZgFyBO2otckhTk1hMjO0eesP79ZjwIUMCPQrP4hWZyiEvTQbRnABFZTOs21uQNycbXezvGIQSxaSxPUau+ZhtHdgz8S8YsSDqF7IqGfZPpuKcNQ4IkaOcNGIaoV/PG87v+Zn9J8TiEDVj6lCJJNioNeAztfEAL1Bq46r/DwIf/pcyQnl9qEQxmUu9ADze3/VYyPId7vVHAAAAAElFTkSuQmCC"
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

            def get_new_plane(self, plane, f1, f2, angle, dire, point):
                vector = None
                if dire is None:
                    self.switch = 'off'
                    char_of_dir, is_bool = self.str_handing(self.selective_index)
                else:
                    self.switch = 'on'
                    char_of_dir, is_bool = self.str_handing(dire)
                if is_bool is True:
                    vector = eval('plane.{}Axis - plane.{}Axis'.format(char_of_dir[0], char_of_dir[1]))
                elif is_bool is False:
                    vector = eval('plane.{}Axis + plane.{}Axis'.format(char_of_dir[0], char_of_dir[1]))
                elif is_bool is None:
                    vector = eval('plane.{}Axis'.format(char_of_dir[0]))

                plane.Rotate(angle, vector)
                f1.Rotate(angle, vector, point) if f1 is not None else None
                f2.Rotate(angle, vector, point) if f2 is not None else None
                return plane, f1, f2

            def str_handing(self, str_char):
                if self.switch == 'off':
                    alphabet_list = str_char.split(" ")
                else:
                    alphabet_list = [char.upper() for char in str_char]
                if len(alphabet_list) >= 2:
                    if alphabet_list[0] > alphabet_list[1]:
                        return alphabet_list, True
                    else:
                        return alphabet_list, False
                return alphabet_list, None

            def match_list(self, *args):
                """匹配子树"""
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


        # 重构XY轴平面
        class Refactoring_Plane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Refactoring_Plane", "S4",
                                                                   """Reconstruct the XY axis plane by entering an axis vector to reconstruct the XY axis """, "Scavenger", "F-Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("25b06c92-fe12-466e-9ea9-615ee01fc527")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Original plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "New_Axis", "A", "You need to reconstruct the vector axis of the XY axis,input the name of the original plane axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Switch", "S", "Whether to flip the reconstructed vector axis ,t is flipping all the vectors,t1 and t2 are flipped X-axis vectors and Y-axis vectors ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Symmetry_Plane", "P", "The reconstructed plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Origin_Point", "O", "The center point of the plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_XAxis", "OX", "Original plane X vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_YAxis", "OY", "Original plane Y vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Origin_ZAxis", "OZ", "Original plane Y vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "a", "NX", "New plane X vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "b", "NY", "New plane Y vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "c", "NZ", "New plane Z vector")
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
                        self.marshal.SetOutput(result[5], DA, 5, True)
                        self.marshal.SetOutput(result[6], DA, 6, True)
                        self.marshal.SetOutput(result[7], DA, 7, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASjSURBVEhLrZJrTFNnHMb5sK2JizKggEApoND7OW1poZQeLoVCW8qlXGRDuYhzLopDxjaWTIbicNNsSDRz3r7IpjJNBurwQoFNLkq5TZ3T7MOEFaLlotsHo+jM9uyFnph5gWjGL3nyP+f/nvM85z3v3+2/8DYq8nzz6VfZ2/nFnfFZIu0wI6BKtYxtzS9B21TV6jsrsPRgbDPbmlc4YUfjHYqbuRD9YHrgTvuGsP35wXd5aCp1OR2yKxlQDOeAV6Xcyi7ND0v3RjcqRpdBdjEd8uFshDbE/U7aL7lWnw//hf5e7OXjeEZ68sTtxgf0b1kzAdRVK+irmfApEljZR+akRFoSfzi+4cRHisoOtvU4gRVUGfVTOqR9FlBXrJDYzRB1MvDZ4D992NMj+ywtrAqvWrGPOTBgM7XhovUyCsMK3yf9p/FIXcL3Tg1kAj6kncqxbAgOpSFs4yYI3q7+h7Lsc4ozap0C0xanzLrfKS6odKZHvencp9kz3mHpwoW0XvQQ7dLuvkWsFrkcZ8GvjBpW3EyHpKkISdeB5MYpGEpGYCi7AUPxKHSrHCgrbEe/pRvdlgtoMbbirNGG86k9eI/6oJK1mRWOfzlNxjQD4qYC6AfGoT80hNiVA4jN60dcdh9iswahLLKhNvUwOpLbZ8w7UrpwNOHYJN+d78H6zIorwJkBiW0dIqv3QCZTgpIzoCgGtDwGwZQC2do1OGm2odPUhXPmLtgtdqwJXf0j6zEnbAA55Nb1UL2zGcLXOBCHLSbyQ6DAB5lKC1qNLehLuoBt0Z9is24Tmi1t8BWGP3t6nuBRgPj7YuiOdCJq3VfQmvdDYqpFunot2oxnifl51GUehlCrgYDni6wNO+H31voXCxA1Lof+2kMY6u9DnvYdck3foiWpFf2mHnyRUA/NiT7IMq0Qei6CquoThJTOMv9P4AoYy4SkMR+az75BaIIZVtoEm+EkmZxB1DG1EIZHQZJohFQogMiXi9gjpxFUUvECAZPLIK3PQBBNwypORJuZjGWKHTuit0Ag9ENoiBdE3h4Q+y+Gel05TJN/IzB/zTnWY044/u/SDiXZAa85DzkVx9CacAZ9yV3YoTsIpa4SCnUFIlOqoPn4czANZ2AYnoJpAvB7o/j5dyC6Y4XpwGqc0ZyaOdDt+gNQV3aDqRhDfOEI9HW3YRgFDJNA4tA9MOOAMSf/bicvqLWGH7Ka+Hi67J6GE0B2ILlmwdbK3eiP+Rk1+i8h/7oF0b/+AebsEJjTQ4jpHQUzMELkgM5+HYqLN5CVmg2IKdxVaTEoVY6fEEh3lvrxVazvIzhyLe1Qx2mxSpsDR9Ra2CMZ9BjN6IszoDeBKDEJvfok2Bk97NFx6NEwOB+hxSW5CreVkTO6r9YCETo4FBEYlCm7j4sk5ay/G4fmh/y5VCxFMSUB1HJAFQGQl5+SYlpql4jpQ1UUJkidJLpFNEV2AvJx90hYU5hkkvV3ezl4wYJDXlwvWwyXayv08ra9Ppu405U7U3NJreEF/fLXzJdHk98UhUsy5cRxgXhvgY+Pgfi+4rL/H+xaErbSGR6JUwLJQDU/uJS0uK6Vadzc/gXoYYETw49/PAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None  # 是否反转平面的因素

            def get_new_plane(self, plane, str_data_list):
                """
                得到新的平面
                """
                X, Y, Z = plane.XAxis, plane.YAxis, plane.ZAxis
                if self.factor is False:
                    direction = [eval(axis) for axis in str_data_list]
                else:
                    letter = ''.join(re.findall(r'[A-Za-z]', self.factor)).upper()
                    if letter != 'T':
                        direction = [eval(axis) for axis in str_data_list]
                    else:
                        origin_direction = [eval(axis) for axis in str_data_list]
                        if len(self.factor) == 2:
                            num = re.findall("\d+", self.factor.upper())[0]
                            index = int(num) - 1
                            direction = copy.copy(origin_direction)
                            direction[index] = -1 * direction[index]
                        else:
                            direction = [-1 * sub for sub in origin_direction]
                return direction, X, Y, Z

            def str_handing(self, str_of_word):
                """
                字符串New_Axis的处理
                """
                str_of_word = str_of_word if str_of_word is not None else "XY"
                string_list = [map(str, re.split(r"[.。!！?？；;，,\s+]", w))[0].upper() for w in str_of_word.split()]
                if len(string_list) == 1:
                    string_list = [s for s in string_list[0]]
                    return string_list
                elif len(string_list) > 1:
                    return string_list

            def RunScript(self, Plane, New_Axis, Switch):
                if Plane:
                    Axis_list = self.str_handing(New_Axis)
                    if Switch is None:
                        self.factor = False
                    else:
                        self.factor = Switch
                    Origin_Point = Plane.Origin
                    self.get_new_plane(Plane, Axis_list)
                    origin_redirect, Origin_XAxis, Origin_YAxis, Origin_ZAxis = self.get_new_plane(Plane, Axis_list)
                    Symmetry_Plane = rg.Plane(Origin_Point, origin_redirect[0], origin_redirect[1])
                    # 重构后的xyz轴向量
                    New_XAxis, New_YAxis, New_ZAxis = Symmetry_Plane.XAxis, Symmetry_Plane.YAxis, Symmetry_Plane.ZAxis
                    return Symmetry_Plane, Origin_Point, Origin_XAxis, Origin_YAxis, Origin_ZAxis, New_XAxis, New_YAxis, New_ZAxis
                else:
                    pass


        # 偏移平面
        class OffsetPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_OffsetPlane", "S1", """Offset the plane with the X, Y, and Z terminal options""", "Scavenger", "F-Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f4ab7050-c453-4eba-b276-c71fbbf73420")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Offset distance")
                distance = 10
                p.SetPersistentData(gk.Types.GH_Number(distance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_X", "X", "Offset in the X direction")
                bool_x = False
                p.SetPersistentData(gk.Types.GH_Boolean(bool_x))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_Y", "Y", "Offset in the Y direction")
                bool_y = False
                p.SetPersistentData(gk.Types.GH_Boolean(bool_y))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Offset_Z", "Z", "Offset in the Z direction")
                bool_z = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_z))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Offset", "O", "Generated offset plane")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAROSURBVEhLpZV/TFNXFMcLmyOTbVToBlaHQUFXIJJMgw6N6WBmy7JJlhFYYP3Na0u7CBOy/cE61CndmIv8gaIiLBObuBJgjRXdMmwLDErWQKGlW4g4dVNGC122AQaKPTv3vbciBIPiN/nk3ffuOd9733333cN5BG1ANnF2cdLwKkC2ItHIY4u/RSJpzzx3bmZPfd1cals5YBteb2mBtAMHrmP/K0zYypSx/dChm4V374IaAKjADGR6TaCcnQXl3Byo8Nnumprp8FWr3mfjH14R0dFyYUPDLDGW+f0gGfMio7DrDyPkTU9B3tQkvDc9DVLsz7RYIEwo/IxNXV6xO3d+tc9qpWct8flA4kVzrw8K/OPwtuMEVDU1g77VxNBiguMdXXC4phZ2b0j4FtMjGZelFZNYUNBWcOMGvQS0MRmARYRvov7FCUfMbXD4yg/zXP4eqmyd8KF7CJK1Ggf6bGLs5hUWyednvazT+cisi5BCfH2y9vdD4TNF4B6IsF+8CPKsENEiO6q+mHkmIeFd4svYczhRETExF5I1mqsCijJvFonMm8XieSSSi1tkslYaubyFpRnvv1sQJxaZBQqFObW4+MfVfH4r+q5h7FemJ9nrYysiIyOjvrS09Nb+4v233ziaP1pWVubV6XT+nJycbuzfyIStTAm5ubl2m80GniEP9A/0w1FPHTgHBsDlcoHT6YSSkpIxjHuVCX80ZWHyn319fWC328GK29Zis0B5TzVYOzrAioN2dnWBy+2GysrKuTU8HsXmLa/Y2NgP9Hp9kMyyC03IGxDIAB/1fAm29nboCHEVXP398M3Zs5CWknKMtXignkhPT681GAwwODgYMg4N0P0T1DcfA/fH5eD6pCLEYHkF/H7kc7CcPAV7s7NN6PMcY3efeDxekkQi+dnhcMDIyAi9vosZQDxON/0NFtOPfcPDw+DxeECj0VyPj4/fxlrTiuJyuZdkMtlNrVbrlkqlbmyHUCgUTqVS2auiVHYalapHrVJ1UxTlCMXJZW4pXrHPrVarf4uLi7OgL5ex53DCkaeY5pIif2QSQupAKkJqwnbkBeRBIv8J8V1WLwrU6s69TU2BTENjcOuFcsA2vHn5CqTr9bexf0Vb9H9l7dDrR6lAgD77C7EeZP1lBgrrAYGcW1kGQ/BpPr+IjX94Ra5fr808fz5ITKSkHuDJKvaNwZ5bRhBNTNCIESX278P/5Hmh8DibuqzC1wqFJ9/p7aVnveC4HvfCa79+DZpr16AIdxpBje2SCT9QuJOSs7PNmB/6sEtp7UtyuUV05w5TD4jx+HiIgn/+Bt0lIzRU18CZ2jMhTp84DY11DVDh6APBp7oh9Elm7OYVhsfrW9sOHvyXLIkqGATF5CQopqYWMjkF8tl7IMbBxXOBheB3UmAeqQcZ1dXwbGIiqdOhXRSFNbhRoFReTBKJjBvz8oyJK4DOy883pmg0ptXr1mH55HD/Az7pJ4gb7t4rAAAAAElFTkSuQmCC"
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

            def Offset(self, Plane, distance, Axis):
                P = rg.Plane(Plane)
                Vec = rg.Vector3d.Multiply(Axis, distance)
                P.Translate(Vec)
                return P

            def RunScript(self, Plane, distance, X, Y, Z):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    Offset = []

                    if Plane != None:
                        if X or Y or Z:
                            if X:
                                Axis = Plane.XAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                            if Y:
                                Axis = Plane.YAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                            if Z:
                                Axis = Plane.ZAxis
                                Offset.append(self.Offset(Plane, distance, Axis))
                        else:
                            Offset.append(Plane)
                    else:
                        self.message2("null plane！")
                    return Offset

                finally:
                    self.Message = 'Offset Plane'


        # 构造工作平面
        class ConstructionPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ConstructionPlane", "S3", """construct working plane""", "Scavenger", "F-Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a7e30adb-dc28-418c-b318-555ade4dfa5a")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Origin", "O", "Plane origin")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "X-Axis", "X", "X-axis direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Y-Axis", "Y", "Y-axis direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Z-Axis", "Z", "Z-axis direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                self.Message = 'Construct a work plane'
                plane = gd[object]()
                if self.RunCount == 1:
                    def _do_main(tuple_data):
                        a_part_trunk, b_part_trunk, origin_path = tuple_data
                        new_list_data = list(b_part_trunk)
                        new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                        match_orgin, match_x, match_y, match_z = new_list_data

                        GH_orgin_list, GH_x_list, GH_y_list, GH_z_list = self.match_list(match_orgin, match_x, match_y,
                                                                                         match_z)  # 将数据二次匹配列表里面的数据

                        orgin_list = [_.Value if _ is not None else _ for _ in GH_orgin_list]  # 将引用物体转换为GH内置物体
                        x_list = [_.Value if _ is not None else _ for _ in GH_x_list]
                        y_list = [_.Value if _ is not None else _ for _ in GH_y_list]
                        z_list = [_.Value if _ is not None else _ for _ in GH_z_list]

                        zip_list = zip(orgin_list, x_list, y_list, z_list)
                        Plane = ghp.run(self.Judge_Vector_Plane, zip_list)  # 传入获取主方法中

                        ungroup_data = self.split_tree(Plane, origin_path)
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
                            map(lambda x: x if len(x) != 0 else [None], value_list[_]) if len(value_list[_]) != 0 else [[None]]
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
                        iter_ungroup_data = ghp.run(_do_main, zip_list)
                        temp_data = self.format_tree(iter_ungroup_data)
                        return temp_data

                    plane = gd[object]()
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    p3 = self.Params.Input[3].VolatileData

                    j_list = any([len(_i) for _i in self.Branch_Route(p0)[0]])

                    re_mes = Message.RE_MES([j_list], ['O'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        plane = temp_by_match_tree(p0, p1, p2, p3)  # 单次匹配树形数据结构

                DA.SetDataTree(0, plane)  # 返回值

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPQSURBVEhLrVJrTFtlGO4PoybGLKIpm3aF0VKh13N6OC29nZqxbJTVQsbGZRcGZlN3yUBnjDplENu5RDOjZgnRPxNj5ozdhgOjY24z2cbmgEK5yJQEKmEHCv5wkymiPr5tT9hiHCFrn+TJd877fnme9/LJ7oRiH1OZvtn4kPSbWixxyrN033nwRD23QQqlFhkHuca8m5ugOiK0SqGU4oHsY09FmOtlyDlbOLvEmL5CiqcG6RvVXkOvD/q+YjAj66GoZwNSKjVQNdmPM2MboA/5YBophfqoe5TC9yWySSLNkqbI/XbNrHF4XdzAMFBMLIF8q6ZEupIclr9sqDN0+6C7UgRDXwm0l9dA2yFgae3jsWXHnuzD0nk3Pki8Ox7xZinTSzOtSr9zlBn3QfvVc1AHPkbWmx/+k13bLGo3fzqh2dEsanY3i+q9n4hZDc1EOhvp/+0T4qOeqqAktTCU/oJB01ghTB1+cOeAvPOzcL4VhXtXBMIbItwvjUPYJ8J25FfwlOM75mAbBJbXHbooSSwMZaBgyDTmgfHifrDf/Ab+o5/hquyBq4K4sReCrxvuwk7Y6wZhbhHBno6SyV9Q7D54TpJYGPMGHfthbr0B22vX4qKudSG4ShN0F3XC8Ww/uM/GkzQ4dQNW/zCcW8OwV4Xh2BKGs6YPrjLqZlMv8ut/pDsT4K8k0YHl3RE4dvTDvr0fjuo+OKvDcXGBOnHWhGEOXgf//d/3YHBJMnh/FI7n++GMVU87iFdfFoLwdFf8mzs2Dv7qvRjc0UF8LOtDcFSQAVUuFHfHDey1tOikRtR2E9bAMAQSj43ERiOyV9J4vFQ9vSq+KQL2zPySz0oSC+O/HeTTkoXYCyrvge2FH+K7iHXg2DkA7nN6Re1RWMhg6c4Di+zgQMGQMeqB4XIDTF/PgPliApaGYVhe/wl5h0ZgpdO69xq4wxGY2qIwtU8h59IcCqtfmbmgULT7lSu2kUxaQu1/kBFYNcR3eWA+3wDm9C0wZ6bBnoqC/ZLYGoX5+CTYlknKTc9TTQYVNa8CObmY4Wzo0rGTLRrde3uWKTlJ9jbMK61DvGBH+eqVCK+tQKioDN1rid7y22eMsbjETm8lBhwFmDZx+IW14I88G8A7EGF4dOnZCydztC9K8jIZk60RVToDtusZgOEAk3lRnCPhKHGKOE38nTqBxYlbZHYiWzslyctkmoyMD+SZyuBq9ZPBXWptcNsi+IxaH3xHlXP1z3jldhpTPnr0bPSkJrdpi1y+imTvT6gngcOZqirRbEGbRtvZqMzcQ6HHEpkYZLJ/ATSQkFQMCKhjAAAAAElFTkSuQmCC"
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

            def get_x_y_vector(self, vector, z_vector):  # 根据z轴和xy其中一个向量求另外一个向量
                # 确保向量是单位向量
                vector.Unitize()
                z_vector.Unitize()
                # 获取 另外 向量（通过 两个向量 的叉积获得）
                other_vector = rg.Vector3d.CrossProduct(z_vector, vector)
                other_vector.Unitize()

                return other_vector

            def get_one_AXis(self, origin, one_Axis):
                # 根据一个向量构建平面
                return rg.Plane(origin, one_Axis)

            def get_two_Axis(self, origin, one_Axis, other_Axis):
                # 根据两个向量构建平面
                return rg.Plane(origin, one_Axis, other_Axis)

            def Judge_Vector_Plane(self, tuple):
                origin, x, y, z = tuple
                if origin is None:  # 直接返回None值
                    return None
                Axis_List = [x, y, z]
                res = list(filter(None, Axis_List))
                if len(res) == 0:
                    plane = rg.Plane.WorldXY  # xyz向量都没给时，输出世界XY坐标轴
                    Message.message2(self, "If you don't input axis,I will output XY plane!")
                    plane.Origin = origin
                elif len(res) == 1:
                    if Axis_List[0] != None:
                        # 只有x轴
                        y_vector = rg.Vector3d(0, 1, 0)
                        plane = self.get_two_Axis(origin, x, y_vector)
                    elif Axis_List[1] != None:
                        # 只有y轴
                        x_vector = rg.Vector3d(1, 0, 0)
                        plane = self.get_two_Axis(origin, x_vector, y)
                    else:
                        # 只有z轴
                        plane = self.get_one_AXis(origin, Axis_List[2])
                elif len(res) == 2:
                    if x != None and y != None:
                        plane = self.get_two_Axis(origin, x, y)  # 直接根据两个向量构造出一个平面

                    if x != None and z != None:
                        y_vector = self.get_x_y_vector(x, z)  # 根据xz向量求出y向量
                        plane = self.get_two_Axis(origin, x, y_vector)

                    if y != None and z != None:
                        x_vector = self.get_x_y_vector(z, y)  # 根据yz向量求出x向量
                        plane = self.get_two_Axis(origin, x_vector, y)
                else:
                    plane = self.get_two_Axis(origin, x, y)
                return plane

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


        # 平面信息转换
        class PlaneToText(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Plane<->Character", "S5", """Converts text to Plane and converts plane to text，space mark：“&”；
                                                                   \nThis program uses Plane to store and read information in Rhino""", "Scavenger", "F-Plane")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("f5a3e0ff-a46d-4fbb-9839-11e643f5d515")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                p.Simplify = True
                self.SetUpParam(p, "Plane", "P", "Grasshopper Plan information")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                p.Simplify = True
                self.SetUpParam(p, "Text", "T", "Rhino stores text Plane information")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Text", "RT", "Plane converts text information")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "RP", "Text convert Plane")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, False)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, False)
                        self.marshal.SetOutput(result[1], DA, 1, False)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQwSURBVEhLvZRtTFtVGMfPB5UJQ7bR1gwGMxsbG2ZaWm6h0EELzBFly7ohZAwl6xKVb+oHYxRW3jqK5UUUpgxpgZaWrV1hSQsstGFhI0NlQ52KFGHDgMAGbgUxKlkfz7nQQiksW6b+k3/ueZ6T8/zuOc89F/2vSqrtCaM0v8aKKzq3ZKo61yVXd+869GnHzpTK9pCDp6+EHj59edsb0mrv9ErT1pdrru4m+dYk5LW4fG1lKC76UOoRXUTT1AxPO/Y7v364K/5Mr5hqHJ3hasbsHM34dIR23B5dN9h/rLxZGKke6eNpJybxc5TS3/lOUD2QuFhqdQkaBg9xLwHwVQO5aQW6oJj6IUFShXU7V31TSKlHy9gX5iGyYSQrun6Qf6yiJSxcO/FndP1Qxb7KL9k7tfO3Uzu++ssxi76GGdQL9gXj+KrjPrIsAFQ3YsJN88A23O2JUQ8K6eSiREpbOsc4B/G134eR+DV5fTCncXwOAxQp+Nh2aOaHj3e09Tvm0DWHHV13eRYNAyCgixDtVf6Qxj175xanDYDSjOoPfnHFl86rbCcIIFb5E0ViicKwlaOdnOQ0Tdu5+nsQpR3rTEqq8OiD4w/EdwE6pXFP0AMsfsPPn0R0Abyom3yJxCsBmeW65/AOZmNUA2VRDUP54ca52b3VN6LJ3HLhHYhcAEHtj8k87XirUNn/AaWd6GKfv/e3QH2LPhJBnS2LageIU9miSHy8rHFbxLkpiKkbyCYxt2nKxm2avn2gxvIsiZ3CgHgXQGQc2b6n7b46xOKwcPR3L+z/vOcVegIroaZPyNf8YoiruRZC4hOlNZtws5Wi2m+PklhY+01klG7CnHimdz+JnXIDnENovRohqhEhHs48SScfU26Aj1BAYhUKgiq0BeRo8z46+ZhyOPDLOgHFKFD0MS5OXIwCEujkKmJKm9n+snaRf47BZb88kyjHJ1SU5xVKj53591sk716++cISoBwXJ34QgJFt6GYpLgGzwLTgQjM8U2yBN8MOwFu7k8EPjxk4R+Y25ZnBO8fyyAAr81Q7ME6ed9lXZgYqvRB4Rwvo8dKcERj55kcGWJiyNmDkGFz2LTRBZFouRKVK6bFrDkPITuiF/xWA8a8AZCbgHZHCnlQZIIUF1uGitHEvnpZ3eAIUKDCeTq6i1QA+uJmirFx4T/w6iCVySM0sgFexxZJTYIxN8QTIUYDHf8WpjSebL64EbPjQCDuKGiD97TxIy8iHtMx8DMmHwxjQEnvEHYDfHopQYB+GWN292VqKGNbnJaW/+cla3QDMHD1syDbCU7nmpePB9sJH5O08IudNJpAqFAyfeTgIlIgFvIwiWE8+xWWANb28yUUoeGMJbi5p8FouQf4JQe+orvuv2MGaXv6ZPqxID1grLtqalhrpm7649OGE36ybVbLsV/Eg4+KsYiv8A1TvCl8I7pcpAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RE_MES(self, parameter, para_name):
                remes = []
                for i_parameter in range(len(parameter)):
                    if not parameter[i_parameter] or 'empty tree' == str(parameter[i_parameter]):
                        remes.append(para_name[i_parameter])
                return remes

            def Branch_Route_2(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            # 树形数据删除空值
            def Delete_None_Tree(self, Data_Tree):
                Data_List = [data_ for data_ in Data_Tree.Branches]
                Data_List_Paths = [data_ for data_ in Data_Tree.Paths]
                NewData_Tree, Null_Paths = gd[object](), []
                for i_path in range(len(Data_Tree.Paths)):
                    if len(Data_List[i_path]) == 0:
                        Null_Paths.append(Data_List_Paths[i_path])
                    else:
                        NewData_Tree.AddRange(Data_List[i_path], Data_List_Paths[i_path])
                return NewData_Tree, Null_Paths

            # Plane信息转为String
            def PlToTe(self, Plane):
                Text_Plane_List = []
                for pi_ in Plane:
                    if pi_:
                        Text_Plane_List.append("O{}&X{}&Y{}".format("{%s}" % pi_.Origin, "{%s}" % pi_.XAxis, "{%s}" % pi_.YAxis))
                    else:
                        Text_Plane_List.append(None)
                return Text_Plane_List

            # String信息转为Plane
            def TeToPl(self, Plane):
                Plane_Text_List = []
                for si_ in Plane:
                    if si_:
                        Plane_Text = si_.split('&')
                        if len(Plane_Text) == 3:
                            C_T = Plane_Text[0][2:-1].split(",")  # 原点
                            X_T = Plane_Text[1][2:-1].split(",")  # X Axis
                            Y_T = Plane_Text[2][2:-1].split(",")  # Y Axis
                            Plane = rg.Plane(rg.Point3d(float(C_T[0]), float(C_T[1]), float(C_T[2])), rg.Vector3d(rg.Point3d(float(X_T[0]), float(X_T[1]), float(X_T[2]))), rg.Vector3d(rg.Point3d(float(Y_T[0]), float(Y_T[1]), float(Y_T[2]))))
                            Plane_Text_List.append(Plane)
                        else:
                            Message.message2(self, "Check the spacing symbol of the plane storage，spacer splitting failed，the plane output is None")
                            Plane_Text_List.append(None)
                    else:
                        Plane_Text_List.append(None)
                return Plane_Text_List

            # 空列表提示 并添加空数
            def PT_RUN(self, Data, Name, nupa):
                Tree_Have = gd[object]()
                if len(nupa) > 0:  # 树形包含空数列提醒
                    for mes_i in nupa:
                        Tree_Have.AddRange("", mes_i)  # 修改“”，避免输入空值导致报错
                    Message.message3(self, "%s contains empty tree, please check (does not affect other output)" % Name)
                    return True, Tree_Have
                elif Data.BranchCount > 0:  # 增加判断，避免列表和个体数据报错
                    return True, Tree_Have
                else:
                    return False, Tree_Have

            def RunScript(self, Plane_P, Text_P):
                try:
                    PText, TPlane = gd[object](), gd[object]()
                    Geo1_list_1, Geo1_path = self.Branch_Route_2(Plane_P)
                    Geo2_list_1, Geo2_path = self.Branch_Route_2(Text_P)
                    Geo_NickName = [self.Params.Input[0].NickName, self.Params.Input[1].NickName]
                    re_mes = self.RE_MES([Plane_P, Text_P], Geo_NickName)

                    PlaneHave, Pnupa = self.Delete_None_Tree(Plane_P)
                    TextHave, Tnupa = self.Delete_None_Tree(Text_P)
                    if len(re_mes) == 2:  # 树形包含空数列提醒
                        for mes_i in re_mes:
                            Message.message2(self, "Connect the data you want to transform, %s or %s" % (self.Params.Input[0].NickName, self.Params.Input[1].NickName))
                        return PText, TPlane
                    else:
                        with Rhino.RhinoDoc.ActiveDoc:
                            # 禁用视图重绘
                            rs.EnableRedraw(False)
                            PBotton = self.PT_RUN(PlaneHave, self.Params.Input[0].NickName, Pnupa)
                            TBotton = self.PT_RUN(Text_P, self.Params.Input[1].NickName, Tnupa)

                            # Plane信息转换
                            if PBotton[0]:
                                Plane_List_pt = [list(data_) for data_ in PlaneHave.Branches]
                                Plane_List_Paths_pt = [data_ for data_ in PlaneHave.Paths]
                                PText = PBotton[1]
                                TextList = ghp.run(self.PlToTe, Plane_List_pt)
                                for pt_i in range(len(TextList)):
                                    PText.AddRange(TextList[pt_i], Plane_List_Paths_pt[pt_i])
                            # Text信息转换

                            if TBotton[0]:
                                Text_List_pt = [list(data_) for data_ in TextHave.Branches]
                                Text_List_Paths_pt = [data_ for data_ in TextHave.Paths]
                                TPlane = TBotton[1]
                                PlaneList = ghp.run(self.TeToPl, Text_List_pt)
                                for pt_i in range(len(PlaneList)):
                                    TPlane.AddRange(PlaneList[pt_i], Text_List_Paths_pt[pt_i])

                            # 启用视图重绘
                            rs.EnableRedraw(True)
                            sc.doc.Views.Redraw()
                            ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                            sc.doc = ghdoc
                        return PText, TPlane
                finally:
                    self.Message = 'Plane To Text'


    else:
        pass
except:
    pass

import GhPython
import System
