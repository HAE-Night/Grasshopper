# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/9/17 17:06


from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import Grasshopper.Kernel as gk
import Grasshopper.DataTree as gd
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import Rhino.DocObjects.ObjRef as objref
import System.Collections.Generic.IEnumerable as IEnumerable
from itertools import chain
import math
import initialization
import time
import copy
from System.Collections.Generic import List
from Grasshopper.Kernel.Data import GH_Path

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:

        # Brep切割
        class BrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepCut", "R2",
                                                                   """Brep Cutting，accuracy is highest，will output unintersected and failed cutting Brep""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("66f1cb77-2cff-45f4-80a5-f1170e324852")

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
                self.SetUpParam(p, "A_Brep", "A", "Brep to be cut（Cutting Brep）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "Brep to be cut（Cutting Brep）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance，default is 0.01")
                Tolerance = 0.01
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Breps", "B", "Brep by cutting")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Disjoint", "D", "unintersected cutting brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "False_Breps", "F", "failed cutting brep")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAImSURBVEhL5ZNPSJNxGMd/OvembXvfNynTvTP/hvtHE8NqDHKCoTSzizcZLCLqEHTpUlBZLRaLdtYukWCQw0sdRvQHvQiW1qJyVJKDBA8evHju2/P6m/kOfLdXRIT6wuf2Pt8Pz/O+L9uNmA2y5XRJe0rnFLEsq9iKYy4teUkz+/iosTwe67dj9Y4Tq9cPF4ae6XfZQDOdfNRYhl+Ha4G4B6CCgjzwIOITtywYSg04gJgbuNVSmPtuhI+sCYJ81Fj+dcEgEXVxEl6ca5VUwQk+aiz6ArWcmL9Qh0ykFpmL9TjbbFEFYaJFh3IiL/qCmAtX/ZUwNVtR5pNhapXBRDN8TSYE2wUE2zQcFXCyTfhts5R8pE6RV/PoC6JOdDgqwEaPw5o9DctiL1hXNaYSIrBgBz7XbPCF+GFfk1Gni1fzPJqMHAIeeoF7dGctcTdCTXvBkn7IS72QlvvAumvwNmYDMlT4vnqDGYIknbQJdaqn+puhRHcV0lcakb5Un8/lBgSUcrBrHtrCD/YsAOasxJs4bTBHgndUuo4qoU1yG+QJ3ESSSOmwHPCa0eMX0HNMQCRUgZWJg8AHTXkRQbG8mB8/APzM3Vw9zSyVTWvKtylIfXq6H/iau7m2VMt2BOlREqhfyWbF6/zXglfZ51XAogJ8oxetx3fil4JT9KXRTN6PVizJG+etGInJGBmU9Lkt4cldGY2KSRU4+Kix1BE3iahBzhA7Hcb+AJV+qCe0V0zxAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None
                self.target_paths = None

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
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def tr_object(self, origin_brep, transform):
                wxy_origin_breps = []
                for _ in origin_brep:
                    _.Transform(transform)
                    wxy_origin_breps.append(_)
                return wxy_origin_breps

            def _second_handle(self, set_brep_data):
                sub_brep, cut_brep = set_brep_data
                no_inter_set_tip, fail_set_tip, no_inter_brep, fail_brep = ([] for _ in range(4))
                # 取消空值
                cut_brep = filter(None, cut_brep)
                # 切割体判空
                if cut_brep:
                    # 被切割体判空
                    if sub_brep:
                        count = 0
                        passive_brep = copy.copy(sub_brep)
                        # 获取被切割体的中心点
                        brep_center = passive_brep.GetBoundingBox(False).Center
                        # 映射被切割体
                        pl = rg.Plane.WorldXY
                        pl.Origin = brep_center
                        brep_center_pl = pl
                        center_to_worldxy = rg.Transform.PlaneToPlane(brep_center_pl, rg.Plane.WorldXY)
                        worldxy_to_center = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, brep_center_pl)
                        passive_brep.Transform(center_to_worldxy)
                        # 映射切割体
                        new_cut_brep = self.tr_object(cut_brep, center_to_worldxy)
                        # 循环切割物体
                        while len(new_cut_brep) > count:
                            temp_brep = passive_brep
                            passive_brep = rg.Brep.CreateBooleanDifference(temp_brep, new_cut_brep[count], self.tol)
                            if passive_brep:
                                passive_brep = passive_brep[0]
                            else:
                                passive_brep = temp_brep
                                interse_sets = rg.Intersect.Intersection.BrepBrep(passive_brep, new_cut_brep[count], self.tol)
                                if not interse_sets[1]:
                                    no_inter_set_tip.append(count)
                                else:
                                    fail_set_tip.append(count)
                            count += 1
                        # 输出不相交的Brep
                        no_inter_brep = [cut_brep[_] for _ in no_inter_set_tip]
                        # 输出切割失败的Brep
                        fail_brep = [cut_brep[_] for _ in fail_set_tip]
                        # 将切割好的Brep映射回原来的位置
                        passive_brep.Transform(worldxy_to_center)
                        # 将未相交、失败的Brep映射回原来的位置
                        [_.Transform(worldxy_to_center) for _ in no_inter_brep]
                        [_.Transform(worldxy_to_center) for _ in fail_brep]
                        sub_res_brep = passive_brep

                    else:
                        sub_res_brep = sub_brep
                else:
                    sub_res_brep = sub_brep

                return sub_res_brep, no_inter_brep, fail_brep, no_inter_set_tip, fail_set_tip

            def tree_match(self, temp_data):
                a_set, b_set, origin_path = temp_data
                new_b_set = [copy.deepcopy(b_set) for _ in range(len(a_set))]
                temp_brep = zip(a_set, new_b_set)
                if temp_brep:
                    res_brep, res_no_inter_brep, res_fail_brep, no_inter_tips, fail_tips = zip(
                        *map(self._second_handle, temp_brep))
                    # 切割失败、不相交的物体以列表形式表示
                    res_fail_brep = list(chain(*list(res_fail_brep)))
                    res_no_inter_brep = list(chain(*list(res_no_inter_brep)))
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path),
                                       [res_brep, res_no_inter_brep, res_fail_brep])
                else:
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), ([] for _ in range(3)))
                    no_inter_tips, fail_tips = [[]], [[]]
                Rhino.RhinoApp.Wait()
                return ungroup_data, no_inter_tips, fail_tips

            def RunScript(self, A_Brep, B_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = Tolerance
                    Res_Breps, Disjoint, False_Breps = (gd[object]() for _ in range(3))

                    j_list_1, temp_brep_list_1, a_brep_path = self.parameter_judgment(A_Brep)
                    j_list_2, temp_brep_list_2, b_brep_path = self.parameter_judgment(B_Brep)

                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['A end', 'B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        _a_tr_len, _b_tr_len = len(temp_brep_list_1), len(temp_brep_list_2)
                        if _a_tr_len == _b_tr_len:
                            new_a_trunk = temp_brep_list_1
                            new_b_trunk = temp_brep_list_2
                            new_trunk_path = a_brep_path
                        else:
                            if _a_tr_len < _b_tr_len:
                                new_a_trunk = temp_brep_list_1 + [temp_brep_list_1[-1]] * (_b_tr_len - _a_tr_len)
                                new_b_trunk = temp_brep_list_2
                                new_trunk_path = b_brep_path
                            else:
                                new_a_trunk = temp_brep_list_1
                                new_b_trunk = temp_brep_list_2 + [temp_brep_list_2[-1]] * (_a_tr_len - _b_tr_len)
                                new_trunk_path = a_brep_path
                        zip_list = zip(new_a_trunk, new_b_trunk, new_trunk_path)
                        temp_iter_ungroup, dis_tips, fail_tips = zip(*map(self.tree_match, zip_list))
                        iter_ungroup_data = zip(*temp_iter_ungroup)
                        Res_Breps, Disjoint, False_Breps = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                                   iter_ungroup_data)

                        for f_disjoint_index in range(len(dis_tips)):
                            for s_disjoint_index in dis_tips[f_disjoint_index][0]:
                                Message.message2(self,
                                                 "the order of the data is {}：the cutting brep which subcript is{} is unintersected！".format(
                                                     (f_disjoint_index + 1), s_disjoint_index))

                        for f_fail_index in range(len(fail_tips)):
                            for s_fail_index in fail_tips[f_fail_index][0]:
                                Message.message1(self,
                                                 "the order of the data is {}：the cutting brep which subcript is{} is failed to be cut！".format(
                                                     (f_fail_index + 1), s_fail_index))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Breps, Disjoint, False_Breps
                finally:
                    self.Message = 'Brep Cutting'


        # Brep切割（Fast）
        class FastBrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepCut（Fast）", "R1",
                                                                   """Brep Cutting，optimize time efficiency（unstable situation come out~nomal error），will output unintersected Brep（If you need the output to be failed cutting object，please use RPP-Brep cutting（high accuracy））""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("5079bafd-b964-473c-a68c-163f9f940778")

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
                self.SetUpParam(p, "A_Brep", "A", "Brep to be cut（cutting object）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "Brep to be cut（cutting object）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "tolerance，default is 0.01")
                Tolerance = 0.01
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Breps", "B", "Brep by cutting")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Disjoint", "D", "not intersecting cutting object")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAK9SURBVEhL5ZPdS1NxGMePtem24znqfFvjjM23pSmmeTESqpGpBQW9EGlqI/AF8600dZikki+FmMagKP8CL4quXBFZDLywDLGQ1uxiV7NEggglJfr2nHYObSkhzTu/8Lk4/L6/3/fZ8zxjtpV2EDmEZQMSiJBl6S+Ig/OiAc4ywU+5gHGbAYdMmoeSJyQdnq4yAiNZwMAePzeJ21koz+afSZ6QZH1B1WIgA+ja7aeHoKCyLH5c8oSk4ICedKAjDT9bUnDSxDrpPIwQ5yTyX7K+lAPo8dX2VBw9rkPapVRk5LLL9gtqj93GeuzVrKfQEv6E/BH+a5vXwalKmsFwJnCLel+fBK4tHYzvNAoadgEfEoB5PbAkYKSZ+07+aP+1YMUTZUTFX5QT+cdS2Ke2vCiXLYd3lZrZSXM+v3qgWUBvewwwqwNeERQy1BS5RP4oIlhateKyi9bQ3ZQMN1X4m8ZkvKkxwqwN75JsssKGalkf5qjyGXr49SYC9Kyi5as9zd+CXuq1iLiKNNS9uoh+ySZLM9jILeAjtUV8WOZfATpWcWWBtgI3aEPkVezPwI/rZuQmRnRLNlkq6vUXsefwUIgMfTuuct/ofP0M1gXQtizWJWG+QkBs2M47ZNEHwJ07ono32he9NnqN/wN9lxSq3HSuJoIlBiy2UkAftYYqn682QnveAHVLOooLNGuODm7Z0cqtODr5FWte+BhdEas0bkAMsV6JGoXdJ/8CCpku0YMZ2QfGVYzONi2wQC0QV/GzgPqz7LR0bfNSKpns/YLqgdWkHhXJjlM+KjrBo7I5HhP3Y4G3tO/iIN/rUXNKMyldC0mm58PRgJceniWmpE3ZwoCcx4P0J3JTWwJXcQsD8ibuUu8XA1ZRnMEnAbVn2BnJE5IMpUWque6GSG93VQB1kV5LpvKe5NkSKTdgW4hhfgFGLJ5y1vCiOQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None
                self.target_paths = None

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
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def tr_object(self, origin_brep, transform):
                wxy_origin_breps = []
                for _ in origin_brep:
                    _.Transform(transform)
                    wxy_origin_breps.append(_)
                return wxy_origin_breps

            def _first_handle(self, passive_brep, cut_brep):
                """群组切割方法"""
                res_temp_brep = []
                # 获取映射平面
                pl = rg.Plane.WorldXY
                brep_center = passive_brep.GetBoundingBox(False).Center
                pl.Origin = brep_center
                brep_center_pl = pl
                center_tr_one = rg.Transform.PlaneToPlane(brep_center_pl, rg.Plane.WorldXY)
                center_tr_two = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, brep_center_pl)
                # 映射被切割体
                passive_brep.Transform(center_tr_one)
                # 映射切割体
                new_cut_brep = self.tr_object(cut_brep, center_tr_one)
                # 群组切割
                res_temp_brep = rg.Brep.CreateBooleanDifference([passive_brep], new_cut_brep, self.tol)

                # 判断是否切割成功
                res_temp_brep = [_ for _ in res_temp_brep] if res_temp_brep else None
                if res_temp_brep:
                    # 切割成功，获取最大的一个Brep并映射回原位置
                    area = [_.GetArea() for _ in res_temp_brep]
                    max_index = area.index(max(area))
                    res_temp_brep = res_temp_brep[max_index]
                    res_temp_brep.Transform(center_tr_two)
                else:
                    # 若切割失败，返回原Brep
                    passive_brep.Transform(center_tr_two)
                    res_temp_brep = passive_brep
                return res_temp_brep

            def _collision_brep(self, set_breps):
                # 检测实体Brep是否相交
                bumped_brep, coll_brep = set_breps
                inter_brep, no_intersect_set_tip, no_inter_brep = ([] for _ in range(3))
                coll_brep = filter(None, coll_brep)
                # 切割体判空
                if coll_brep:
                    # 被切割体判空
                    if bumped_brep:
                        # 循环检测
                        count = 0
                        while len(coll_brep) > count:
                            interse_sets = rg.Intersect.Intersection.BrepBrep(bumped_brep, coll_brep[count],
                                                                              sc.doc.ModelAbsoluteTolerance)
                            if interse_sets[1]:
                                inter_brep.append(coll_brep[count])
                            else:
                                no_intersect_set_tip.append(count)
                            count += 1

                        no_inter_brep = [coll_brep[_] for _ in no_intersect_set_tip]
                        res_brep = self._first_handle(bumped_brep, inter_brep)
                    else:
                        res_brep = None
                else:
                    res_brep = bumped_brep

                return res_brep, no_inter_brep, no_intersect_set_tip

            def tree_match(self, temp_data):
                a_set, b_set, origin_path = temp_data
                new_b_set = [copy.deepcopy(b_set) for _ in range(len(a_set))]

                # 匹配数据
                temp_brep = zip(a_set, new_b_set)
                if temp_brep:
                    res_brep, res_no_inter_brep, no_inter_tips = zip(*map(self._collision_brep, temp_brep))
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_brep, res_no_inter_brep])
                else:
                    ungroup_data = map(lambda x: self.split_tree(x, origin_path), ([] for _ in range(2)))
                    no_inter_tips = [[]]
                Rhino.RhinoApp.Wait()
                return ungroup_data, no_inter_tips

            def RunScript(self, A_Brep, B_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = Tolerance
                    Res_Breps, Disjoint = (gd[object]() for _ in range(2))

                    j_list_1, temp_brep_list_1, a_brep_path = self.parameter_judgment(A_Brep)
                    j_list_2, temp_brep_list_2, b_brep_path = self.parameter_judgment(B_Brep)

                    #            _a_trunk, _a_trunk_path = self.Branch_Route(A_Brep)
                    #            _b_trunk, _b_trunk_path = self.Branch_Route(B_Brep)
                    #            _a_tr_len, _b_tr_len = len(_a_trunk), len(_b_trunk)
                    #            _copy_b_trunk = copy.deepcopy(_b_trunk)
                    #
                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['A端', 'B端'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 树形长度匹配
                        _a_tr_len, _b_tr_len = len(temp_brep_list_1), len(temp_brep_list_2)
                        if _a_tr_len == _b_tr_len:
                            new_a_trunk = temp_brep_list_1
                            new_b_trunk = temp_brep_list_2
                            new_trunk_path = a_brep_path
                        else:
                            if _a_tr_len < _b_tr_len:
                                new_a_trunk = temp_brep_list_1 + [temp_brep_list_1[-1]] * (_b_tr_len - _a_tr_len)
                                new_b_trunk = temp_brep_list_2
                                new_trunk_path = b_brep_path
                            else:
                                new_a_trunk = temp_brep_list_1
                                new_b_trunk = temp_brep_list_2 + [temp_brep_list_2[-1]] * (_a_tr_len - _b_tr_len)
                                new_trunk_path = a_brep_path
                        zip_list = zip(new_a_trunk, new_b_trunk, new_trunk_path)

                        temp_iter_ungroup, dis_tips = zip(*map(self.tree_match, zip_list))
                        iter_ungroup_data = zip(*temp_iter_ungroup)
                        _res_breps = zip(*iter_ungroup_data[0])[0]

                        for f_disjoint_index in range(len(dis_tips)):
                            for s_disjoint_index in dis_tips[f_disjoint_index][0]:
                                Message.message2(self,
                                                 "the order of data is {}：the cutting object which subscript is{} is not intersecting！".format(
                                                     (f_disjoint_index + 1), s_disjoint_index))

                        for _f_res_index in range(len(_res_breps)):
                            if not _res_breps[_f_res_index]:
                                Message.message1(self,
                                                 "the data which order is {} failed to be cut：please use RPP-Brep cut （high accuracy）plug-in to look for it！".format(
                                                     _f_res_index + 1))
                        Res_Breps, Disjoint = ghp.run(lambda single_tree: self.format_tree(single_tree),
                                                      iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Breps, Disjoint
                finally:
                    self.Message = 'Brep Cutting（Fast）'


        # Brep结合
        class Brep_Union(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Brep_Union", "R21",
                                                                   """will combine many Brep to One.and delete reference line""",
                                                                   "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("57cfa2b7-7b3d-43ee-b190-3af9cfa5c6f9")

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
                self.SetUpParam(p, "Breps", "B", "Brep Object，Tree Data Type")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "PRE", "P", "Combination Accuracy is [0.00-1.00].not to be changed in success situation")
                PRE = 0.01
                p.SetPersistentData(gk.Types.GH_Number(PRE))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep after structure")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANoSURBVEhL3ZRZSFRhFMcNeulBZ0adcsYmxmV2pITqIYiQdlo0AtGWMc1A6aGGJFqnMk2nDYtpWglNarTJzKXGTMpl1NGszFEKbaOINmghLZv0/jvfJWyha01v9cEfzuXe7/y++z/nfH7/x3pccTj0U0O+4ZnTKij2/qXziIzzVCm4rjLDp5YzguJuOQz9LXY1gBE8oDVNXdBj0qAtTSWo7rVquNNUh7yNhSWozcPHSxZBoWY/ep37HhFgJA9wJYhOdSUFoCnBX1CdRn/UxfvbvK78EtRQovKdgkJVDnorcr4BGpcE5XcmB6JxieQHNS+VoOlr7FkhQX2ixOp1FThwxYLesp34UJ6FPhKLv9egkwCVuQ9+C6hLDOQhvwL00UlZsrfndwzFPgFuLhcjb24ICmOluEHxzwBUW1BkTobneAa8F3f5DugwimCeLkfcRCVuU/wD4NpePCvaiqmTonH35Po/B7gosZssaVsmxp0VAbDNG4NgpRYFsaNxf6X4G6D5IDJT4xARGYk3JTuAK7v5pKwmwwKY35fjA3F2kRSli4NxJk4Kg1aFOdFh6EkRw0UA7obd8dKxDQplOFJiY3Dv1EZ0kk3Mqtcl23mIIIDZsjEmFPJwLTRqNfQaFXQk9nxsgYz+SmIdbC9ybEmaD6l8HKIMOmi1Gqjo24hImhebCVxVrjDAQwDTtLEYpdBjTJgWIZSYbWZxzuxQdKeIrANtpx0r6eQyhRLK8AgEyRSQhCggGh0Kt3UNcHkYQCt5bydbMmfIkTtLBgtpvE6FyYZItCfxc2HlOoocnmMZfGLj/Gk4l5mKws1JKNxkxFP7FvRXZgsDWJGvE4RZ1ZMcwMOkYTrsmS3Do1QRaqkGA01U5MYDSFkYg0kTojBIU8u6CjW78bEiC+8v+NCm26lNp0RF8NCu79u0fj9fVL1Oi+78Dfj8N3PQbhQje6acHzYW/2rQLOmLcfvour8bNNayzvggNFDM7qOfAczrF2fNeF5sxgeyxmcAExs6ocvuPSXqr8geGq5hAa5EcfHDVRLcojtHSA+oyPUJASfoui7FVQu8lVmCQjUBync9GQK0rtabu00Gd2u6RlB3TXq3O12X4W2xF3Cuo+/6qvMENVBre9dXY+sYAviyuFev/Glj8O/EcW8Dv275p5ef3xdPJW9bFlB5AgAAAABJRU5ErkJggg=="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            # brep结合
            def brepbp(self, tuple_data):
                brep_group, origin_path = tuple_data
                Merge_Result = []
                # 清空失效值
                no_none_brep = filter(None, brep_group)
                # Brep联合
                if no_none_brep:
                    temp_brep = rg.Brep.CreateBooleanUnion(brep_group, self.tol)
                    Result = rg.Brep.JoinBreps(brep_group, self.tol) if not temp_brep else temp_brep

                    for Re_ in Result:
                        Re_.MergeCoplanarFaces(sc.doc.ModelAbsoluteTolerance)
                        if Re_.SolidOrientation == rg.BrepSolidOrientation.Inward:
                            Re_.Flip()
                        Merge_Result.append(Re_)

                ungroup_data = self.split_tree(Merge_Result, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Breps, PRE):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Brep = gd[object]()
                    self.tol = PRE
                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Breps)

                    re_mes = Message.RE_MES([j_list_1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        zip_list = zip(temp_brep_list, brep_path)
                        iter_ungroup_data = ghp.run(self.brepbp, zip_list)
                        Brep = self.format_tree(iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Brep
                finally:
                    self.Message = 'Brep Union'


        # 合并以及封面
        class Seam_Merge(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CoverMerge", "R13",
                                                                   """close the surface and combine surface""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8bae4c8b-b1a4-4b0f-a4a0-5471683daf3c")

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
                self.SetUpParam(p, "Suface_Or_Brep_List", "M", "face and Brep data list")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "capping,stitched and coplanar")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH+SURBVEhL3ZXLSxthFMVHjdYmRgtVow2ok9RHjGARXBtQsCJYNPWxVTfFJ9GCYBfVNuILXYm6cSm4ceOf0CIudVEfpQvRLty4cCG4PD33GxMTyGSchV144MfAN/fek/nmOxPtf8tlA1vykB/kygaHpIo8SuFXuVnYDpdit8+L3Z409BLWlBdkg32TRru1wm/cDuB7DbAcBBZqzVkkS0E0lOaKwYTRbq2ukjwHbqcrgW80+VptzgyZrUG954UYRIx2az13A1mT9xO7zgXwzjD4ZLRby9yAv/gy4sevIR0nwzqOR3TsD5ZD6tm3RkIpaCLFJK7UBhx++6UKezyWp6M6/oz58HfCj+NxH+aai+DNd8CVnZlMTiZeOjLE/IK8VtMpU4Obqbc4GCxT26Lucf/VNs0HVP3VpD+ZqUr87C8TA6FBTadMDe74BPsDNJDBsfUYUitmiTAr53xCzhTq1XTqowpalAUrDJqE6T5QiAZwxn1PMk7HfT1nJhl8cHPvFlqKsNpWjNXWBxa5NhMqNAzkiKYamoiJQQHZIUcmXK+3e4xPRaqhiZgYWGm9o9r1pAYbnYE8npynM9jseh4G8g7kJKWDgfzN1LPHlsFWd9DNjNQZiU4Hs3MRiQctnmQrRQudWQj5nAhVWKA70ehV/3ZChep+hPLJZxK1wXtN07R/xQzcRVjpR7UAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

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

            def RunScript(self, Suface_Or_Brep_List):
                try:
                    Result = gd[object]()
                    Brep_List = []
                    tol = sc.doc.ModelAbsoluteTolerance
                    j_list_1, temp_geo_list, geo_path = self.parameter_judgment(self.Params.Input[0].VolatileData)

                    re_mes = Message.RE_MES([j_list_1], ['M end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Suface_Or_Brep_List:
                            # 封顶
                            for i in Suface_Or_Brep_List:
                                if i:
                                    cap_brep = i.CapPlanarHoles(tol)
                                    if not cap_brep:
                                        Brep_List.append(i)
                                    else:
                                        Brep_List.append(cap_brep)
                            if Brep_List:
                                # 第一个合并的方法
                                temp_brep = rg.Brep.CreateBooleanUnion(Brep_List, tol)
                                # 若失败，使用第二个Join方法
                                Result = rg.Brep.JoinBreps(Brep_List, tol) if not temp_brep else temp_brep
                                # 去除结构线
                                Result[0].MergeCoplanarFaces(tol)

                                # 检查Brep是否翻转
                                if Result[0].SolidOrientation == rg.BrepSolidOrientation.Inward:
                                    Result[0].Flip()
                            else:
                                Result = None
                        else:
                            Result = []

                    return Result
                finally:
                    self.Message = 'Brep Join'


        # 分割Brep（面）
        class SplitBrepFace(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SplitBrepFace", "R3",
                                                                   """surface or solid cutting，cutting surface or solid（something like knife cut pancake）""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3c6041a2-9374-4045-98cb-6d3c8fb9e166")

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
                self.SetUpParam(p, "Brep", "B", "Brep to be cut（surface）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "cutting object（flat plane（Plane）or smooth surface（Surface））")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "cutting accuracy")
                tol = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(tol))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                bool_cap = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_cap))
                self.SetUpParam(p, "Cap", "C", "capping or not，capping by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Result_Brep", "B", "Brep by cutting（surface）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALbSURBVEhLtVRbSJNhGJ5jbUpuQs6YJ7owa7MkzVKkdM3JLMxR0IFiTjNtc5uZWHohUfrPdvCURd7UjRdhaGloWlJdeO3oQGBQQt1EFOVNWoEXT+/3b8Hcr2nDPfDA++/9/ufZ9x5+0f+isMR3Qmd4sSvwuP7QHno5qi+dqQg8hoVoomol5uqmhtNyBuuWywUYR1wRJZtixB+zk6Lns1UyIRM3zOfneRb3Zhz9zWJBnt5LUUi+kg77A0JIxVG+6ZotgEsDtKqFbE+G03QDTx3VFKcI804N5prTkaqQ/CQ54U0UUvGbueatdJAOX90upDOJN5i011BMBqH5VnZGg5xE2S+SS/KrBkEuFb/63JgGcGRwhQ6HkmMGvXhsIwOODELzvIkarFwkx/qxFGs1mLBZImfQbrqO8cga9GAskgbXmEGtNTwD2jDfQnMC4E7mxQR0x6KrwoNnjjMUy4V5mjI2vlnxoh8kJ+NFtQbfYb3xfV9hyXRfZhb3jTvlQlelF51mLzrMHfASPeWdxC64zW6cPjIO27EBuCjPbsN64uTZC45GuM10E/l53sV9xVMjxWWz90Tag779euPspULDdGP6NsunO5X1GKy9gCFLPR5YzmPYWocRqwMPrXaM2qtgOz7Ai43RLR5RqVjDJ2zn+NF9Yq/GJC1hLm16bsGwo6jsnYm/xV+wEs03baZNpvpyrEwhdMnRbfbQop2lOI5+Y+eCyJavPRVZSr5EMX7VIKylyaxU7Da8YWh+PaaI9YOVLGIGXjJgfYmYAZss1vywDOhr+vrLxdUMvLj/L4M2NXarZAskl+hXDUKMJGrmexN9rnt2At4MIXuScauqAxN1DUB3qjDfuYOmKwMapXSR5BL8qktx2ZC2ES06JVoK4oXUxuJkcSsqi2oolgvzB5QwZSogjhINkZbYLymEnli+EtP39D9XqT13l8sFaCRKiOFBV/r2tt74oSHwuApEoj89Q3ZdEGG9MgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None
                self.cap_factor = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def cap_brep(self, cap_brep):
                brep_list = []
                for _ in cap_brep:
                    new_cap_brep = _.CapPlanarHoles(self.tol)
                    if not new_cap_brep or self.cap_factor is False:
                        brep_list.append(_)
                    else:
                        brep_list.append(new_cap_brep)
                return brep_list

            def sort_by_xyz(self, pt_list, follow_object):
                dict_pt_data = dict()
                dict_pt_data['X'] = [round(_.X, 1) for _ in pt_list]
                dict_pt_data['Y'] = [round(_.Y, 1) for _ in pt_list]
                dict_pt_data['Z'] = [round(_.Z, 1) for _ in pt_list]

                zip_list = zip(dict_pt_data['Z'], dict_pt_data['X'], dict_pt_data['Y'])
                w_sort_pts = []
                for index in range(len(zip_list)):
                    w_sort_pts.append(list(zip_list[index]) + [index])
                index_list = [_[-1] for _ in sorted(w_sort_pts)]
                new_object_list = [follow_object[_] for _ in index_list]
                return new_object_list

            def _recursive_cutting(self, ent, cut_list, new_brep_list):
                cut = cut_list[0]
                ent = ent if type(ent) is list else [ent]
                for en in ent:
                    temp_brep = list(en.Split.Overloads[IEnumerable[Rhino.Geometry.Brep], System.Double]([cut], self.tol))
                    if len(temp_brep):
                        cap_brep = self.cap_brep(temp_brep)
                        new_brep_list.append(cap_brep)
                    else:
                        new_brep_list.append([en])
                temp_list_brep = list(chain(*new_brep_list))

                cut_list.remove(cut)
                if cut_list:
                    return self._recursive_cutting(temp_list_brep, cut_list, [])
                else:
                    res_list_brep = self._handle_brep(temp_list_brep)
                    return res_list_brep

            def _get_intersect(self, item, pln):
                pln = filter(None, pln)
                if pln:
                    origin_pt = [_.Origin for _ in pln]
                    new_pln = self.sort_by_xyz(origin_pt, pln)
                    cutts = []

                    for pl in new_pln:
                        single_event = rg.Intersect.Intersection.BrepPlane(item, pl, self.tol)
                        # 是否切到实体，未切到则不加入切割列表
                        if single_event[1]:
                            surface_cut = rg.Brep.CreatePlanarBreps(single_event[1])
                            if surface_cut:
                                cutts.append(surface_cut[0])

                    # 若平面全部都没切割到实体，则输出实体
                    if cutts:
                        #                "----------------------------"
                        temp_cutts = ghc.Untrim(cutts)
                        #                # 输入端口调整为列表
                        res_cutts = temp_cutts if type(temp_cutts) is list else [temp_cutts]
                        #                "----------------------------"
                        res_breps = self._recursive_cutting(item, res_cutts, [])
                        sort_breps = self.sort_brep(res_breps)
                    else:
                        sort_breps = item
                else:
                    sort_breps = item
                return sort_breps

            def _handle_brep(self, breps):
                for brep in breps:
                    if brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                        brep.Flip()
                return breps

            def sort_brep(self, temp_breps):
                brep_list = self.sort_by_xyz([_.GetBoundingBox(True).Center for _ in temp_breps], temp_breps)
                return brep_list

            def _get_surface(self, surf, pln_list):
                cutts = []
                for pl in pln_list:
                    single_event = rg.Intersect.Intersection.BrepPlane(surf, pl, self.tol)
                    if single_event[0]:
                        cutts.append(single_event[1][0])
                cut_breps = surf.Split.Overloads[IEnumerable[Rhino.Geometry.Curve], System.Double](cutts, self.tol)
                res_breps = self._handle_brep(cut_breps)
                sort_breps = self.sort_brep(res_breps)
                return sort_breps

            def temp(self, tuple_data):
                breps, planes, origin_path = tuple_data
                # 匹配平面数据
                list_pln = [planes[:] for _ in range(len(breps))]
                res_list = []
                for brep_index, brep_item in enumerate(breps):
                    if brep_item:
                        brep_list = [_ for _ in brep_item.Faces]
                        if len(brep_list) == 1:
                            res_list.append(self._get_surface(brep_item, list_pln[brep_index]))
                        else:
                            res_list.append(self._get_intersect(brep_item, list_pln[brep_index]))
                    else:
                        res_list.append([])
                ungroup_data = self.split_tree(res_list, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Brep, Plane, Tolerance, Cap):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = Tolerance
                    self.cap_factor = Cap
                    Result_Brep = gd[object]()

                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Brep)
                    j_list_2, temp_pl_list, pl_path = self.parameter_judgment(Plane)

                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['B end', 'P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        len_b, len_p = len(temp_brep_list), len(temp_pl_list)
                        if len_b != len_p:
                            new_brep_list = temp_brep_list
                            new_plane_list = temp_pl_list + [temp_pl_list[-1]] * abs(len_b - len_p)
                            new_plane_list = ghp.run(lambda li: [copy.copy(_) for _ in li[:]], new_plane_list)
                        else:
                            new_brep_list = temp_brep_list
                            new_plane_list = temp_pl_list

                        zip_list = zip(new_brep_list, new_plane_list, brep_path)
                        trunk_list_res_brep = map(self.temp, zip_list)
                        Result_Brep = self.format_tree(trunk_list_res_brep)

                    #            trunk_list_brep, trunk_list_path = self.Branch_Route(Brep)
                    #            trunk_list_plane = self.Branch_Route(Plane)[0]
                    #            self.tol = Tolerance
                    #            self.cap_factor = Cap
                    #            len_b, len_p = len(trunk_list_brep), len(trunk_list_plane)
                    #
                    #            if not (trunk_list_brep or trunk_list_plane):
                    #                self.message2("B terminal solid、P terminal plane is no input！")
                    #            elif not trunk_list_brep:
                    #                self.message2("B terminal solid is no input！")
                    #            elif not trunk_list_plane:
                    #                self.message2("P terminal plane is no input！")
                    #            else:
                    #                if len_b != len_p:
                    #                    new_brep_list = trunk_list_brep
                    #                    new_plane_list = trunk_list_plane + [trunk_list_plane[-1]] * abs(len_b - len_p)
                    #                    new_plane_list = ghp.run(lambda li: [copy.copy(_) for _ in li[:]], new_plane_list)
                    #                else:
                    #                    new_brep_list = trunk_list_brep
                    #                    new_plane_list = trunk_list_plane
                    #
                    #                origin_list = zip(new_brep_list, new_plane_list, trunk_list_path)
                    #                trunk_list_res_brep = list(ghp.run(self.temp, origin_list))
                    #                Result_Brep = self.format_tree(trunk_list_res_brep)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    Rhino.RhinoApp.Wait()
                    sc.doc = ghdoc
                    return Result_Brep
                finally:
                    self.Message = 'flat cut Brep（surface）'


        # 圆柱切割体
        class CirBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CirBrep",
                                                                   "R5",
                                                                   """produce cylinder cutting object according to the top Plane""",
                                                                   "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("d8360a85-40c8-4877-8590-048bcd679cc5")

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
                self.SetUpParam(p, "Plane", "P", "reference plan")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "cylinder radius")
                p.SetPersistentData(gk.Types.GH_Number(5))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "HoleCir", "H", "total length of oblong hole")
                p.SetPersistentData(gk.Types.GH_Number(20))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "CriVec", "CV", "extend direction size")
                p.SetPersistentData(gk.Types.GH_Vector(rg.Vector3d(0, 0, 20)))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "CirBrepList", "CB", "circular hole cutting object")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "HoleCirBrepList", "HG", "oblong hole cutting object")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKjSURBVEhL1ZVdSFNhGMedc9s5Tt1qta2zzYY53c42LLP2kab2Ja4FLTI0WoIkloRBub4EzSyXZREi3fRBV9V1UDdCEHQVq4sugsroIiTJq2IXNaJ/z7ujNI3WbIPogR/nwDnv8zvneZ+HN+9fhnGRyImMokhZIJuo0qvia1YQxl+pEbh4vZWP15by8Wp6ZzVRrMp/QWstUor04QnY1EBUBAbt8zlTCQw76GrHwxYLYh1W4AK9N+rEUd9S0Nr9Uor04d0tFgEjTilhKufsmDlhg9/Co6lOhbV2BXq9OmDMjYF6XcYCzy4HCdgfDFDSVEZEdLq1ONzOAVMmfHlmhGiT42VXGaKblzNBWEqRPn4viDpQKxTi0Y0lwFsB+GBGeKcK90NmjG7LhYDqfWWTHp51crx7rMcEiUr1csycrMBQ47IcCGb34TjV3Wvl4DNzeNBmoT1w4XRdcg+yFMxJ6Fmij91TZ7GuuiiiL2eCOQYJJmP3fyUYJsFZ+kLqnCSs3+cSLmSxghATXHZiurcckRod9tk1GN9qlIRs4LIVtLqK8bm/Ei6jEj3tPK6PatDgV6CjSgucp5pnKzhQrcG9HSaEmpTU66Zkz3+PGWC3FGDqyCrpT7IRdJLgZrOA7jYemKSBilF5SOB3KvH6UBkwlAPB7YCArj0keCMJvj01wCcqMdn9vwhusRK1/iwR24OcluhOUEBLQAVMmyXJcwMcpQV435P9Jnv3ukvwidpUpDY9dbAQd69p0dyoQNilmT1wKGkql0T0b0wKMjsPghV0ol114WPEhmM0aGFRg7EtBmkGGKxEqdBQRvzJE61dSpE+SniF7Ml6gfvaYC1MBG3qRKBcndhO1w0WPuE1cfMxM/iElst/RWutUoo/h4xYuUg4YkHk5f0AfPqfOyDBqiQAAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            # 重新定义向量的长度
            def ver_lenght(self, vector, len):
                unit_vector = vector / vector.Length  # 将原向量单位化
                new_vector = unit_vector * len  # 创建新的向量，长度为new_length
                return new_vector

            # 数据自动补齐
            def data_polishing_list(self, data_a, data_b):
                fill_count = len(data_a) - len(data_b)
                # 补齐列表
                data_a_new, data_b_new = data_a, data_b
                if fill_count > 0:
                    data_a_new = data_a
                    data_b_new += [data_b[-1]] * fill_count
                else:
                    data_a_new += [data_a[-1]] * -fill_count
                    data_b_new = data_b
                return data_b_new

            def create_rectangle_from_center(self, pln, width):
                # 创建矩形的中心点和半宽、半高
                half_width = rg.Interval(width * -20, width * 20)
                half_height = rg.Interval(width * -20, width * 20)
                # 使用中心点和半宽、半高创建矩形
                rectangle = rg.Rectangle3d(pln, half_width, half_height).ToNurbsCurve()
                rectangle_brep = rg.Brep.CreatePlanarBreps(rectangle)[0]
                return rectangle_brep

            def circle(self, Data):  # 根据面生成圆柱Brep
                # 判空
                if Data[0]:
                    Cri_Vec = Data[2] * 2
                    Data[0].Translate(-Data[2])
                    C_Plane = Data[0]

                    circle = rg.Arc(C_Plane, Data[1], math.radians(360)).ToNurbsCurve()  # 圆弧转曲线
                    Surface = rg.Surface.CreateExtrusion(circle, Cri_Vec).ToBrep()
                    CirBrep = Surface.CapPlanarHoles(0.01)
                    if CirBrep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                        CirBrep.Flip()

                    if Data[3]:
                        # 创建长圆孔的圆柱体
                        pln = rg.Plane(C_Plane.Origin, C_Plane.YAxis, C_Plane.ZAxis)
                        cir_split = [ci_ for ci_ in
                                     circle.Split(self.create_rectangle_from_center(pln, Data[3]), 0.1, 0.1)]
                        Move_Vec = pln.ZAxis
                        # 切割曲线偏移
                        cir_split_move_1, cir_split_move_2 = cir_split[0], cir_split[1]
                        cir_split_move_1.Translate(self.ver_lenght(Move_Vec, (Data[3] / -2) + Data[1]))
                        cir_split_move_2.Translate(self.ver_lenght(Move_Vec, (Data[3] / 2) - Data[1]))
                        cir_split_move_2.Reverse()
                        HoleCir = rg.NurbsSurface.CreateRuledSurface(cir_split_move_1, cir_split_move_2).ToBrep()
                        HC_Curve = [HC for HC in HoleCir.Edges]
                        Surface_Hold = HoleCir.Faces[0].CreateExtrusion(rg.Line(C_Plane.Origin, Cri_Vec).ToNurbsCurve(), False)
                        HoleCirBrep = Surface_Hold.CapPlanarHoles(0.02)
                        if HoleCirBrep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                            HoleCirBrep.Flip()
                        else:
                            Message.message1(self, "failed to create oblong hole")
                            HoleCirBrep = None
                    else:
                        HoleCirBrep = None
                else:
                    # 若传入数据为空
                    CirBrep, HoleCirBrep = None, None

                return CirBrep, HoleCirBrep

            def RunScript(self, Plane, Radi, HoleCir, CriVec):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    CirBrepList, HoleCirBrepList = (gd[object]() for _ in range(2))
                    j_bool_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]

                    re_mes = Message.RE_MES([j_bool_1, j_bool_2], ['Plane', 'Radi'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Plane and CriVec:
                            # 将标量值转换为列表，方便与Plane进行zip
                            Radi = [Radi] * len(Plane)
                            CriVec = self.data_polishing_list(Plane, CriVec)
                            HoleCir = [HoleCir] * len(Plane)

                            # 使用ghpythonlib.parallel.run并行计算 这里使用run函数并行计算多个圆柱体的生成
                            Geometry = map(self.circle, zip(Plane, Radi, CriVec, HoleCir))
                            #                    # 解包结果
                            CirBrepList, HoleCirBrepList = zip(*Geometry)
                        else:
                            pass

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return CirBrepList, HoleCirBrepList
                finally:
                    self.Message = 'HAE cutting cylinder'


        # 不规则几何物体最小外包围盒(3D)
        class GenerateMinBox3d(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GenerateMinBox3d", "R25",
                                                                   """create minimum boounding box of irregular object through point array（3d）""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("1930f7b3-b706-456f-9303-c909f907ebd9")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Pts", "P", "point array、point assembly（delete repetition by advice）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "iterations，defualt is 18（suggest to be 15~18）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(18))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Box()
                self.SetUpParam(p, "BBox", "B", "final bounding box")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAS5SURBVEhLrVQLUFRVGL7IYyFeIdCmM0SEkRTxGAgDNBcIDYhHGDpKPHdXdllQ3s/lsSwgDwG1olKYgDEqYoxJcwITVGR47oZYlpAKNlqKhDbEQ5Cvc+9uA4SVjHwz39wz957/+8/5v//+1H+BzWZrK5crDzZb/1mWtsYwWR4l9CRk0e9XErH+qQGQtOSBE+aGp8zYg+RdCaEj8/VxwdJmdRf3FqEBx1BHeOi3w4isjIKDtwN01uh3UZpUItlmrti9fNjYuFvN1RPpaiJ8tL4AjWmpOC1KxSluImo8Q5Fg7QpHE7MpdUOtk2R/CKERE/mIKIys4eLEhQp8FShEi20I2h3D0bmZhy53PmQeAnznIcJ5TiTe89wJf74XTF59boTE1RD+r18aeuYGV6pr0tCykYd2pwjIA0S4FBKLQX4Cfo5MwGVuPL4P2oteXyF6XHbjTHgSqvorkNgkBifUFUamRoMsLfUSAxODl5Sai/C6u7MN2r2j0cHh4SIRuhadjFvpYoxJs3EvPwe/S7Lwa0o6SZaIvu3ROG8fiuPvxKBu/BN8OvcFDt+sgr2PA9TU1IRKzXmoaql+XObgA5mbEBd37cH12BRGdPpAHmYOznOyTIrR7CxcFSZBvk2EM9bB+OyDbFRP16J2rAZmdmZjRG6JL09aGT19p3UTFzI/ERN8l5x65mA+Zg9I8aAsl1CC2fJczJIk0+V5GBGL8VNEHDqIP8cDhGiYqEVKYzyIFv3/LMGu4BfsGQP7d8bgZnI6OWkeEaPFJcD+bIZz+3MUiQ7lYbwoF0MxyZD5RqHZKRwnBj4Eh/8anYA2ezFWrVb7+t23A9FDykObOiLOxH1SGvrEjHiRGCjMAIozMVeaw9xqslSKG4lp6AuMxjknLmrrMmBgYThE5DQVqvMwtXR7ZrJlXxzaNnAVCTKXl6CH3DwuxBeUKlWq1FyE+Oj3vSBrEKPVLpwxmO6UKVJnRf2VJSrJYp5MiYgPfxbnYnhPCuT+InRsjYKzxfN0eRwUkgvwhI5Gz7Hr8ejqy8Qp+zDISADdnvcKcjBDaj1brkjyN+mk90mC0exMDPDiIfOMQr1zEFbr6ciJnIpCdR52rn7r5wawD91T2WgO4qPNiYcfgvcy1x8vlDBidHvSp6afdNveleYwBvdtj4HcVYRYW2KuGpWk1JyHigp1JKHEAzdQjGsoQk93KprswtC5JRKXQmPxS1wqRnOy8AdJNF4kYW51m7QnfcN+Usp2Fx5aSYtaWZlMEzkzheoC6BuwdhuxdbpdtppDWumLs3eS0PdlCjo3CdBF5s6FHTHMeLgalcSIXhEk4sewWOYHoxvinGckPjrChZqRerNS8qFYRehMWMo20R30F9iiiOeDJk445O4iyD1F6PUms8dLiK4tAqaE31qHoSmQj/6hAoRIXWlz6an6SNAl9KG0qFqLtca3eeteQeWGbWh9k4/eHdFoCxTgtFCAs5/HoWdCgo4HuTBbb0yPBkMmeplYQ6lT4Vp6rJMvW66diInjoLFTiMvIY/waQgkqvgn519GwXFgSpugaa3ZtfGMd8qv8ILuVgbcibB8+Gh4DC/0a1jfUGjbdbLpkNKwUjDV0NF5Urv8BivoLbf4BS+QugxIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.count, self._global_tol, self.tot_ang = None, None, None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Restore_Tree(self, data, path):
                """还原树"""
                orgin_tree = gd[object]()
                for _ in range(len(data)):
                    orgin_tree.AddRange(data[_], GH_Path(tuple(path[_])))
                return orgin_tree

            def rotateplanes(self, count, init_planes, dir_vec):
                init_planes = [init_planes] if isinstance(init_planes, rg.Plane) else init_planes
                inc = self.tot_ang / (count - 1)
                origin_pt = rg.Point3d(0, 0, 0)

                planes = []
                for i in range(count):
                    for init_plane in init_planes:
                        new_plane = Rhino.Geometry.Plane(init_plane)
                        new_plane.Rotate(inc * i, dir_vec, origin_pt)
                        planes.append(new_plane)
                return planes

            def get_octant_plane(self, _count):
                yz_plane = rg.Plane.WorldYZ

                dir_vec_x = rg.Vector3d(1, 0, 0)
                x_planes = self.rotateplanes(_count, yz_plane, dir_vec_x)

                dir_vec_y = rg.Vector3d(0, -1, 0)
                xy_planes = self.rotateplanes(_count, x_planes, dir_vec_y)

                dir_vec_z = Rhino.Geometry.Vector3d(0, 0, 1)
                xyz_planes = self.rotateplanes(_count, xy_planes, dir_vec_z)
                return xyz_planes

            def rotate_plane_array(self, data_handle):
                plane, tot_ang, divs, axis = data_handle
                out_planes = []
                plane.Rotate(-tot_ang * 0.5, axis)
                out_planes.append(Rhino.Geometry.Plane(plane))
                inc = tot_ang / (divs - 1)
                for i in range(divs - 1):
                    plane.Rotate(inc, axis)
                    out_planes.append(Rhino.Geometry.Plane(plane))
                return out_planes

            def rotate_plane_array3d(self, view_plane, tot_ang, divs):
                view_planes = [view_plane] if isinstance(view_plane, (rg.Plane)) else view_plane
                one_tot_ang = [tot_ang] * len(view_planes)
                one_divs = [divs] * len(view_planes)
                z_axis = map(lambda z: z.ZAxis, view_planes)
                one_zip_res = list(
                    chain(*ghp.run(self.rotate_plane_array, zip(view_planes, one_tot_ang, one_divs, z_axis))))

                two_tot_ang = [tot_ang] * len(one_zip_res)
                two_divs = [divs] * len(one_zip_res)
                y_axis = map(lambda y: y.YAxis, one_zip_res)
                two_zip_res = list(
                    chain(*ghp.run(self.rotate_plane_array, zip(one_zip_res, two_tot_ang, two_divs, y_axis))))

                three_tot_ang = [tot_ang] * len(two_zip_res)
                three_divs = [divs] * len(two_zip_res)
                x_axis = map(lambda x: x.YAxis, two_zip_res)
                three_zip_res = list(
                    chain(*ghp.run(self.rotate_plane_array, zip(two_zip_res, three_tot_ang, three_divs, x_axis))))

                return three_zip_res

            def min3dbox(self, obj):
                init_plane = rg.Plane.WorldXY
                curr_bb = self.get_bbox_by_plane(obj, init_plane)
                if curr_bb:
                    curr_vol = curr_bb.Volume

                    tot_ang = math.pi * 0.5
                    factor = 0.1
                    max_passes = 20

                    """-------consumed most time (parallel iteration)-------"""
                    xyz_planes = self.get_octant_plane(self.count)
                    b_box_list = ghp.run(lambda xyz: self.get_bbox_by_plane(obj, xyz), xyz_planes)
                    min_index = 0
                    for box_index in range(len(b_box_list)):
                        if b_box_list[box_index].Volume < curr_vol:
                            curr_vol = b_box_list[box_index].Volume
                            min_index = box_index
                    best_plane = xyz_planes[min_index]
                    curr_bb = b_box_list[min_index]

                    for f_index in range(max_passes):
                        prev_vol = curr_vol
                        tot_ang *= factor
                        ref_planes = self.rotate_plane_array3d(best_plane, tot_ang, self.count)
                        sub_bbox_list = ghp.run(lambda x_pl: self.get_bbox_by_plane(obj, x_pl), ref_planes)
                        sub_min_index = 0
                        for sub_index in range(len(sub_bbox_list)):
                            if sub_bbox_list[sub_index].Volume < curr_vol:
                                curr_vol = sub_bbox_list[sub_index].Volume
                                sub_min_index = sub_index
                        best_plane = ref_planes[sub_min_index]
                        curr_bb = [sub_bbox_list[sub_min_index]]
                        vol_diff = prev_vol - curr_vol
                        if vol_diff < sc.doc.ModelAbsoluteTolerance:
                            break
                    """-------Cutting Line-------"""
                else:
                    curr_bb = []
                return curr_bb

            def get_bbox_by_plane(self, object, plane):
                world_xy = rg.Plane.WorldXY

                def __objectbbox(geom, xform):
                    if isinstance(geom, rg.Point):
                        pass
                    return geom.GetBoundingBox(xform) if xform else geom.GetBoundingBox(True)

                xform = rg.Transform.ChangeBasis(world_xy, plane)
                bbox = rg.BoundingBox.Empty
                if isinstance(object, (list, tuple)):
                    pass
                else:
                    object_bbox = __objectbbox(object, xform)
                    bbox = rg.BoundingBox.Union(bbox, object_bbox)

                if bbox.IsValid is False:
                    pass
                else:
                    plane_to_world = rg.Transform.ChangeBasis(plane, world_xy)
                    box = rg.Box(bbox)
                    box.Transform(plane_to_world)
                    return box

            def RunScript(self, Pts, Count):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.count = 15 if Count is None else Count
                    if self.count < 0:
                        self.count = int(math.fabs(self.count))

                    self._global_tol = sc.doc.ModelAbsoluteTolerance
                    self.tot_ang = math.pi * 0.5

                    BBox = gd[object]()
                    trunk_list = [list(_) for _ in Pts.Branches]
                    trunk_Path = [list(_) for _ in Pts.Paths]

                    re_mes = Message.RE_MES([Pts, Count], ['Pts', 'Count'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        CutNone_list = map(lambda x: filter(None, x), trunk_list)
                        pts_cloud = ghp.run(lambda pts: rg.PointCloud(pts), CutNone_list)
                        BBox = map(self.min3dbox, pts_cloud)
                        BBox_Tree = self.Restore_Tree(BBox, trunk_Path)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return BBox_Tree
                finally:
                    self.Message = 'minimum bounding box（irregular 3d）'


        # 映射以及挤出
        class MappingExtrusion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Mapping&Extrusion", "R14",
                                                                   """Map an object to specific plane and then extrude the solid through a line or vector""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c8ea9cd3-3a21-4abe-ad66-f4d7061b95d1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Geometry", "G", "closed curve or plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Origin_Plane", "A", "original plane")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "B", "converted plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Mode", "M", "as extruded vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Geometry", "G", "new geometry object")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Transformed_Objects", "T", "object after plane converted")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO0SURBVEhL7ZR/TNRlHMefA+E4D47zjgsE7k45B2aJdxwglbCGqXeXHHhqi61aKI0/7ARZ/iZjYRHVMos0KxaXQREgTG2dOjdNNzN2m1OR1Vozs1hb/5n/NOPd5/M8d2NHrj+u1V+9t9e+3+/u/Tzv+z6fz/cj/te/KadGiLOP3JcRWVs+JxIojVJGlBgjem3SBfJUKWtiaicw0bUIOLYU+KxUMUQcKUPp/Nmg31+VzgS1i8D5tkJguAz4uGQaCljjNnLAgHQmqJ0EwlsXyA1xmDaOMVqOLZ57OOBr6UxQOwgMBedTQPlfAvY/kc8BP0tngmojMPgsBZx+CBihkBinHsS53YUccEc6STYiTHxFcPXjoG7poGuc5s1N3ptlTIJ3sQHPr8tFmz9HUUMEcrGh0swBjNRjloxZONZcgPBzCxBudUhOUAGDyy1s+kHZptXo1722sVYX2+TvkHq6KEcLfMptRgUboCvzRQV6GmxsuqRs06pfmda9epkWT/p0GBuxYCxkRuSwGZf7s3B51IK+DtlFU8otRLDYqgNCVCDmQxfQR+33eREO1qez8aJ0ARrHo9+5+XaDR3RXOlPRuSkDmMwDrs0FxqPcyMOZd0287hZ7WbsqCvTUw24KcMqA7u17sLv1bfhr98J0f8cvNu/4PqtnvM/m+wam6uvhulr/RLEjGa+3pOPOtzn4YywbU1FwMw+9L8g3uKm2F6Kz+t50oH864MXNL6Ox6QM87HsDWa59v9pWjX2Svypywl7zPazeiSvmgtrJlGQBj1s3FQwYEfRnorkuE01eA97cRrQaOOCK2l6I7polBlUDPp7YER1fiK46WcizbFq0/mqq3XfRw/ek4wSObinA7d5S3D7oxG+HXLjRVYz1y/TYXC9HhVzHCtUvnaNmSSyAoYK3rc5m4zlli9MggfPtDlpHjREiP31kv7/nQpPPgMByLa8bkk7SyDNVZmCQjDMCtntlwBlli9P7BCIv0ajoj/6xXhemekrQ4jeiYsksXndAOkmnWlZYVIvOCGhdKWfKaWWL01tCw9N0IR1ttPOYkBs7A2Y47BpexxNX6kLn2lzg5AMqJAY9b/PKgJPKFqdX0lI0uHWomGpFb8DHxIxWYH9DNkwm+ZFtUlYhrvudmTjQaMc7NKRi8HNVoZ6Nd6tBe1qqBj3BHAzvsGJ4az4Gmq34KGhHQ3UmUlJlwOPSmSTEHrrwJnfjS+IpYqYqCR4hkwRPTeanKD8S14gi4h9JS+iJ2TNII/4LCfEn0cFCml3RkE0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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

            def get_new_brep(self, geometry, p1, p2):
                primordial_plane = p1 if p1 is not None else rg.Plane(rg.Point3d(0, 0, 0), rg.Vector3d(0, 0, 1))
                if p2 is not None:
                    transform = rg.Transform.PlaneToPlane(primordial_plane, p2)
                    geometry.Transform(transform)
                    new_geometry = geometry
                    return new_geometry
                else:
                    return None

            def exturde_brep(self, object, curve):
                if 'ToBrep' in dir(object):
                    object = object.ToBrep()
                if curve:
                    mode_brep_list = [_.CreateExtrusion(curve, True) for _ in object.Faces]
                    mode_brep = rg.Brep.JoinBreps(mode_brep_list, 0.001)[0]
                    return mode_brep
                else:
                    return None

            def RunScript(self, Geometry, Origin_Plane, Plane, Mode):
                try:
                    New_Geometry, Transformed_Objects = (gd[object]() for _ in range(2))

                    j_list_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_list_2 = self.parameter_judgment(self.Params.Input[2].VolatileData)[0]

                    re_mes = Message.RE_MES([j_list_1, j_list_2], ['Geometry', 'Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Geometry:
                            Transformed_Objects = self.get_new_brep(Geometry, Origin_Plane, Plane)
                            if Mode:
                                line = rg.Line(rg.Point3d(Mode), Mode) if type(Mode) == rg.Vector3d else Mode
                                mode_line = line.ToNurbsCurve()
                                New_Geometry = self.exturde_brep(Geometry, mode_line)
                        else:
                            Transformed_Objects, New_Geometry = None, None
                    return New_Geometry, Transformed_Objects
                finally:
                    self.Message = 'HAE mapping and extrusion'


        # 多边曲面偏移
        class BrepOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepOffset", "R12",
                                                                   """create offset plane according to broken line；input terminal D or V is ok""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("96643d8a-600a-424c-a69e-2d06e29b111b")

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
                self.SetUpParam(p, "Brep", "B", "multiple side surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "offset distance")
                DEFAULT = 1
                p.SetPersistentData(gk.Types.GH_Number(DEFAULT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Both Side", "B", "Whether to offset to both sides")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                self.SetUpParam(p, "Tolerance", "T", "accuracy")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Cap", "C", "Whether to cover or not")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Brep", "B", "Brep after offset")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMhSURBVEhL1ZVbSJNhGMd3cOo2JTe3qVszy1k6kwpTSCNadlC80Moi8KLoYCGr6EBFdKIsM7qIDhchBnUjmHeBF4ERFSEYFakUUUldKIGlWNCB6t//eb9ZIp+n6qY//PjY9u33vO/7Pe/7Gf6n2CPXf5pF5Cx5QnrIZWIkf5Uosom0ExSmWlG33IOG8hTERZvA7+rJH2cV6YynaOcCBx5XTwdOZgFngsC52Whe45UCwly5eTJxkkaC6nwHXu8NaFKRH5sFHCVyrQuiIhgvBa7Lnyaa+eRF0BWNO5unaeIaikU6klNZ6KpOG5pFtvx5vKwgH9ZyVIOHZ6oR6oqHkFlwVgV+qxTYoAxjZAn5Gs5LAGo5Yhn1kRFCPTjD8yUeKXCTmEWklyzyYVsu5TLq45n6Mj24TA+qpoG9+pUOj7KNiI08LQnY1c2TkgsnMtG3LwCbxfSJHp8yjshFX3wU3h/M0LpET6IHxWq2p4OqgMtm/kZXuqb8nTyCG+t8WreMt+byu8yQ977ZnY6TITdyE61wx0bBZFSdlKGsw3KrJINLIyMZ6u/REDkf/uChmQjnOSkzwukyYnOlFfk5FpG3kGhljaSA4CEfkOoaPekQIucgZCd7rRY4nAY0HJ+CL+3JQN9UhNfYpECDsg5L49IZtonJuc7tW9Ng4qiLF0Zj4H4S8NILPCc9U1FVrvbBNU2rJZEMNlXwhvE2U00m3u7PgM1oQlkoBuhK0cSdKWi54EBlqRWuBHXoNStzJDvcNjMGDrBzxmtLDqA4LQ6pfhO+P9Lk/XeTsDIUK9LvRMRbyTzyK02ZPGtUW45VgPuibWOqiHCv3gm88uFjWzLystRD7SC5ItPLFoLaIjdwNnv0Ihz9yvR4zMk2A8+0Nd+uPdBu4hLRWCklfWEex5+lRc+wENdbbSCBs/vBIrEGExprpwAf/ehvTYIlSvV7uTJMIAHSmuOJwdXVXnTvSkcvz/7ePbzy+dxe71fLc2CDHZdqErCpTHXLOyJvuUmlinRYzEbY+fayWwivMfzM74VO8jjCFfJHkaO2iCwjIbI4QiGZ4IvdYPgJEM+2UYRmKHsAAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def convert_brep(self, trim_brep):
                # 转为未修饰的面
                planar_brep = rg.Brep.CreatePlanarBreps(trim_brep.Loops[0].To3dCurve())
                if planar_brep:
                    new_brep = planar_brep[0]
                else:
                    new_brep = trim_brep.UnderlyingSurface().ToBrep()
                return new_brep

            def untrim_curve(self, origin_brep):
                res_brep_list = []
                # 移除修剪线
                trimSource = [_ for _ in origin_brep.Faces]
                untrimSource = list(map(self.convert_brep, trimSource))
                if untrimSource:
                    # 判断面是否与原来的面方向相同
                    trim_normal = [_.FrameAt(0.5, 0.5)[1].ZAxis for _ in trimSource]
                    untrim_normal = [_.Faces[0].FrameAt(0.5, 0.5)[1].ZAxis for _ in untrimSource]
                    nor_zip_list = zip(trim_normal, untrim_normal)
                    angle_list = map(lambda x: math.degrees(rg.Vector3d.VectorAngle(x[0], x[1])), nor_zip_list)
                    for an_index in range(len(angle_list)):
                        new_untrim = untrimSource[an_index]
                        if angle_list[an_index] >= 90:
                            new_untrim.Flip()
                            res_brep_list.append(new_untrim)
                        else:
                            res_brep_list.append(new_untrim)
                else:
                    res_brep_list.append(origin_brep)
                return res_brep_list

            def offset(self, brep, dis):
                # 将trim线剔除
                untrim_brep_list = self.untrim_curve(brep)
                temp_brep = rg.Brep.JoinBreps(untrim_brep_list, self.tol)
                if temp_brep:
                    untrim_brep = temp_brep[0]
                else:
                    untrim_brep = untrim_brep_list[0]

                # 判断两边是否都需要偏移
                if self.b_side:
                    # 正向实体偏移
                    res_brep_1 = rg.Brep.CreateOffsetBrep(untrim_brep, dis, False, True, True, self.tol)[0][0]
                    # 逆向实体偏移
                    res_brep_2 = rg.Brep.CreateOffsetBrep(untrim_brep, -dis, False, True, True, self.tol)[0][0]
                    # 合并实体
                    res_brep = SectionBody()._do_main(([res_brep_1, res_brep_2], [0]))[0][0][0]
                else:
                    res_brep = rg.Brep.CreateOffsetBrep(untrim_brep, dis, self.cap, True, True, self.tol)[0][0]
                # 判断实体方向是否都朝外
                if res_brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                    res_brep.Flip()
                return res_brep

            def RunScript(self, Brep, Distance, Both, Tolerance, Cap):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.cap = Cap
                    self.tol = Tolerance
                    self.b_side = Both
                    New_Brep = gd[object]()
                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(self.Params.Input[0].VolatileData)

                    re_mes = Message.RE_MES([j_list_1], ['Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Brep:
                            New_Brep = self.offset(Brep, Distance)
                        else:
                            New_Brep = None

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return New_Brep
                finally:
                    self.Message = 'offset surface'


        # 截面实体
        class SectionBody(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SectionBody", "R11",
                                                                   """Loft（EX edition，can loft surface or line），time efficiency be the highest""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3f99dcdb-d937-4272-b283-88d68a08c8bc")

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
                self.SetUpParam(p, "Breps", "B", "N a set of N data，can be line or surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Options", "O", "loft type；0=Normal，1=Loose，2=Tight，3=Straight，5=Uniform")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Integer(0))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Cap", "C", "capping，capping by default")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Result_Breps", "B", "obtain Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARRSURBVEhLxVUNTFVlGD73XuRwPefecy/375wLFgYUbP4Vi7/ASSaCYFIIFj8zzRo5ZdGiMnIpZjEEcrm28AemBoFKoJhbNWdsyQQr6GeF1KatnNXYbK0Vbd7z9H7fudcEZDVn9W7Pzrnf+b7n+Z73e7/3Cv913EYoJ9zOf/0L0VSYIGN9knIl45aIs27J8gqNZRFk/vUmxMmGxW6cKovC0WINe/K8qE51Ij9euniHK7yDvj9CmM1n3kBY7aL5h9blPhwp1NDxgIoueh5f5cc7BPa77l43yufa/kiLtvYromUrrckgRPDV/yDmzvGInLDzQZUTXotDNHa0SMOJh/zooWfzMi+qUhzIi5MuxEWGH6D1JYRZnGmaeDRBCceuRV50LFfRW+RH90qNE08W6yR00beQu/YCFdsXuVA6x/Zbsl/sk8PNNcSXQjBx5mC0bauQUbPWhvJ0CWvm2VFztwt7s33ooVQdozMJpW4yDl/jjm3qjVwvnkhSIIvmE0FuQbCYhb6f3vUC3/rxS78PH7RG6g1VNjyWI6H0Thkb5zvQmOlB5/0aeosNouulkrlj39tW+CDNMJ8P0gsmzWMe+bXPB3yiAR+p0D/XAhj1A5+qGD3uRludA9UlMsrI3Vpyt5nc7Vt6fXfsjOqpIIj3fYNeEJSkxLCxEDkGSWBADbAnzhKGaXyExEY0/Hzai1Mtkah/0oZ1SyWUkbvKBQ40LfTg0AqNn8l7JVHYlO5kAq0GvSDE5meKAXxJRIx8UNWvCkzGx4QvaB5zN6xi5JhbP/iygqcflrEmQ0Zpgh0NlEp2hsS73aAXhPTKVTOBr2kRkRD59AIEtgH+HnL3lQb9UpTestWOqtKZaN6sBGJ9YUygyKAXhJU7n7JPFBicXmAKyNFIlweVxbTJi1EYessNWTL1Eq/FoBeEqq4dDuA7EmC7GdICV3c5CVPGKWXj5KQs14rzVIWXz6iI9pq/IU67QW1EQ0GSFTsrHOhucrKq0fUhIjpH9lm+Wd5DAuRuggCdRXWZhPaXaIOXopGfLv5OfPMM2r+i89lkJ9pyVNSmuVCd6cALhXbsfs6B/gMuXP6Q7gcrAMOdznM/QGKjfr19mwMVBZSasWjUb7CxvLOWMTFEi+nMbuotrH7fpgvEavvNZSq/WM+nReKZbAV16xR0N3J3JEICF/w41+PRFy4Ixzi5HDjogskkNAYpJ4YmW4b35Xt5DfPrTkKsBx0upEtDgkeovpsX+1CbHnKnYM+LTuSkioHT+10Y/0xDYkzYySDd1BBFISbWIW7Mi5d6NyQpY01L3Ly/MDF27dktZYIhd23krvYuNwqSrbwwVudEfE80boPt7yOSkJvij3iVuuPwpnuceku+j7eDUKtmnXRXlhdbVtuwf4tyhean8pU3GIm32sPW58ZJPfRX+mPDfW7eOV9f4sH8+BmI8pofD867KaEQsjNmWXdkxViH6P01Pvr/hSD8CWmp5jIJPDqGAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._dict_data = {0: "Normal", 1: "Loose", 2: "Tight", 3: "Straight", 4: "Developable	", 5: "Uniform"}
                self.op = "Normal"
                self.cap = True

            def format_tree_data(self, target_tree, *origin_tree):
                new_tree_by_format = []
                for single_tree in origin_tree:
                    if single_tree.BranchCount:
                        [single_tree.Paths[_].FromString(str(target_tree.Paths[_])) for _ in
                         range(len(target_tree.Paths))]
                    new_tree_by_format.append(single_tree)
                return new_tree_by_format

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def split_tree(self, tree_data, tree_path):
                """操作树单枝的代码"""
                new_tree = ght.list_to_tree(tree_data, True,
                                            tree_path)  # 此处可替换复写的Tree_To_List（源码参照Vector组-点集根据与曲线距离分组）
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
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def _do_main(self, tuple_data):
                res_brep = []
                group_curve, origin_path = tuple_data
                if group_curve:

                    if all([isinstance(_, (rg.Brep)) for _ in group_curve]) is True:
                        w_set_breps = [group_curve[0], group_curve[-1]]
                        temp_curves = map(lambda x: [_ for _ in x.Edges], group_curve)
                        join_curves = ghp.run(lambda y: rg.Curve.JoinCurves(y), temp_curves)
                        eval_list = ['join_curves[{}]'.format(_) for _ in range(len(join_curves))]
                        eval_str = ','.join(eval_list)
                        # 获取全组Brep边界
                        zip_curves = eval("zip({})".format(eval_str))
                        # Loft
                        loft_cr_to_brep = list(ghp.run(self._loft_curve, zip_curves))
                        # 将首尾Brep和Loft的Brep联合
                        set_breps = w_set_breps + loft_cr_to_brep
                        join_breps = rg.Brep.JoinBreps(set_breps, sc.doc.ModelAbsoluteTolerance)
                        temp_brep = join_breps
                    elif all(['ToNurbsCurve' in dir(_) for _ in group_curve]) is True:
                        # 转换为Nurbs Curve
                        curve_list = [_.ToNurbsCurve() for _ in group_curve]
                        temp_loft_brep = self._loft_curve(curve_list)
                        if type(temp_loft_brep) is list:
                            res_loft_brep = temp_loft_brep
                        else:
                            res_loft_brep = [temp_loft_brep]
                        temp_brep = res_loft_brep
                    else:
                        temp_brep = []
                    # 是否将Brep封盖
                    "---------------------------------"
                    # 删除空值
                    temp_brep = filter(None, temp_brep)
                    "---------------------------------"
                    if self.cap:
                        if temp_brep:
                            res_brep = map(self.cap_brep, temp_brep)
                    else:
                        res_brep = temp_brep
                    ungroup_data = self.split_tree(res_brep, origin_path)
                else:
                    ungroup_data = self.split_tree([], origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def cap_brep(self, brep_data):
                sub_brep = rg.Brep.CapPlanarHoles(brep_data, sc.doc.ModelAbsoluteTolerance)
                return sub_brep if sub_brep else brep_data

            def _loft_curve(self, curves):
                """曲线放样"""
                unset_pt = rg.Point3d.Unset
                opt = eval("rg.LoftType.{}".format(self.op))
                create_brep = ghc.Loft(curves, ghc.LoftOptions(False, False, 0, 0, opt))
                return create_brep

            def RunScript(self, Breps, Options, Cap):
                try:
                    self.cap = Cap
                    Result_Breps = gd[object]()
                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Breps)

                    re_mes = Message.RE_MES([j_list_1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 选择放样类型
                        if Options == 4 or Options > 5:
                            Message.message2(self,
                                             "Developable loft type is out of data！plug-in convert to Normal automatically！")
                            Options = 0
                        self.op = self._dict_data[Options]

                        zip_list = zip(temp_brep_list, brep_path)
                        w_filter_list = map(self._do_main, zip_list)
                        Result_Breps = self.format_tree(w_filter_list)
                    return Result_Breps
                finally:
                    self.Message = 'Loft（surface or line）-> original section solid（already deleted）'


        # 删除重复的Brep
        class CullBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_CullDuplicateBrep", "R23",
                                                                   """delete overlap Brep""", "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("59be0dc6-d5e7-408b-b267-dcd2757ca933")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "The Brep collection to be deleted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance (little influence)")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Number(0.01))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep_Result", "B", "brep after delete")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Subscript of overlapping Brep in the original Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQHSURBVEhL3VNrTFNnGG5pi8M6O9GINzbGwAHSc1oKTC6lkDhqI+ySuKTNNG6ggIBQcITBVgqFVUF/GNQNiTMzG/OybEvMppl/BOemOMEJdUixKIqgw7AsG2YE7LP3XEbCSEwZ//Ykb853vvf+vO8n+V9iN8kx4TgDISStJOv4v/8A59usCjbDYtD5BIkffytgtVIuvf3hq8uwOtB/jP7ThWvfICU5sJlZCOxZA+xdA0faEi7JKV4rkUSo/P2G2rKeBRrVePhuOEIXKTh9hqD2DVuTggO8Q+VhQH0U0BCFvelLuSBtgQF+d9pzn+PvODmzeRWClDIP6VjecxbIDFukGPeUvCAE2x2Fpowg/MBVzv1Td59vXAFq9xrZLhdcZo91ISr5cMf2EKA2AthFgT+IxCSdD2Uu4zo6T7KYt5wD3ksODsBkHSWofhGgr8caygX/iySSt5gDzGzQvD/6S4kmLsGuSL4D1EXia8tKKPyk18nmecF09siKW/EURirChUFT8OrUJThFgf+ZwdktwVAqpANkGyG4CPAO71SO7H+5+ef3E7954NTvmzhiNIqqKZSbwpQYsxMlNFxOypICOVq+mCeTdp/etEpYYUrUkReClU/LfyPd1Bah0fQamk24XBiDu2U6TNTp4T1kPCuq+XdQ+3rEAsBJdFCQwvhnuOAf81raGJlU0vOlmTqhd+AuDkXwQvlo8SvhZQ8OppcP1qdlTToMpyccegzaEtBf+RKGqxIxcTCdizEN1oxwJXJ0Kk6xX7iaQhDJVRs9wKXzZfckEgXrPbrB1VOxFn2lOtq4FAyVxaO3SIsr2xm0bWPQYo6+JbhORynJPuE4AyqSJpLl6KW1chpwtyqBr/oRVT/wThx+2aHBjzlqtGaz+Mys+XeRTwYAqffIhgZ3dfJXf9boux7ZktBfooOrSIP2Ag1u0rmrgEVbdjS+3cLi0zd1qaKrb/A2mkxoMvKD9Nbo8Wv5WritMWjPVeNiDgMPJeggelqz1DhmVg+etL/hL7r6hsfVKR/BSVzbE/GwJgkDxHkPVX9hqxpdhVoavpYSqakDFi0WTbPo5htwzi4fr0q+9XtlAm7QIC9S1deLYuAqZPE9JXBbdeim83mi58xbLI5a4ma8gyfC22BM8DpScIcG6aJBtucyPD0/5TG4lMtOo+e4RX3/RMnGANHVNzyuTXVgTxo8pbHopECd+Ro+wYVtalwrIHqsWlyaoof9RHTzHeN2Q/RoZWLnSEU8+ijY7Z2xRJWGp6e3mDaJuuLo+Y7oadkUmym6zRoytzU2k6qv77PqLl/NZya7abij9HK5YXObdNwSPXYy37BAtJ8bOvK1Ya4dcetvWmMOX8ljXOeyGU+LhbGJaoJE8jcYYhnYpbsTQwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def RunScript(self, Breps, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Brep_Result, Index = (gd[object]() for _ in range(2))

                    temp_geo_list = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list]
                    Abool_factor = any(length_list)

                    re_mes = Message.RE_MES([Abool_factor], ['Breps'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_brep = [list(i) for i in structure_tree.Branches][self.RunCount - 1]

                        total, count, no_need_index = 0, 0, []
                        if filter(None, Breps):
                            while len(Breps) > total:
                                flatten_list = list(chain(*no_need_index))
                                if count not in flatten_list:
                                    sub_index = []
                                    for _ in range(len(Breps)):
                                        if Breps[count] is None or Breps[_] is None:
                                            sub_index.append(None)
                                        else:
                                            if Breps[count].IsDuplicate(Breps[_], Tolerance) is True:
                                                sub_index.append(_)
                                    no_need_index.append(sub_index)
                                    total += len(sub_index)
                                count += 1
                            need_index = [_[0] for _ in no_need_index]
                            Brep_Result = [origin_brep[_] for _ in need_index]
                            # 输出端结构匹配
                            Index = no_need_index[0]
                        else:
                            Brep_Result, Index = [], []

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Brep_Result, Index
                finally:
                    self.Message = 'delete overlap Brep'


        # 修复Brep
        class Fix_Brep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Fix_Brep", "R22",
                                                                   """Repair damaged surface,turn red when it doesn't work out，exist open Brep（Open Brep turn yellow）， message will be sent if repair （ps：This program is not suitable for all models and situations, please use it wisely ）""",
                                                                   "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("2cfd67f4-3e79-4d44-ae86-db7635385f16")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Breps", "B", "BREPs to be repaired")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Toggle", "T", "Open Brep repairs alternative switch")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Fail_Brep", "F", "Unfixed or invalid Brep set")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUWSURBVEhLxVVrUBNnFI122tr2Rzud9l/HdvqrJbub3YSHGHyVQKkjIAItvqpOC1bxgWIRHwhVa1VEMBUVGaUCTTBBnvURVHQcrMOIvElUwAcYRBSo1UGRZE9vkm0xo8PQ6Y+emW8y2ew99+w9Z29k/yusZTPetOUGJ9gLQjNs+SEbRV1Y2IAhcrz083+Hbf/0NaiIAorDXadwFsS84AH7r6GVom5mdH966DvSrf8eMES+Yt/h34oDQUBesOscmQHk06cxzNmQGllt+aFrkRz5mlQ2eoh7pgdBGwgxWY2nP03B0EFqlB/iOrnUyNFMHwqUUiNdSN3gL8FyqXR0sKcFlCNdg6EUPzxc74v7iT7o3eqHgcwAF7mOyHWOhvRE1ETUhfSIeWEfSOUj48m+WR+LaZohbJ2MJ/QE/Rt8cS/RG7dXKdG6kkfr9564uXEi7m6bhod7A/E4Kwh9mUGwamd8IlGMDPvuoG34ORB2Uv8oSY0H6yfg7lov3I5X4dpKAXUxHK4kcqiicyzcA+VzFcj9UiiSykcGchaME1P9rdg+FYPJfviDlPas88EdUn1jtRLmFTxqojnUJQuwlAq4uEuOU7E8DodPnOSsB8aKYtDrTrKXwab94iuHevEHPzzepEYvjad7rTc61qjQGiegaZkC1d9yqE4R0H5ShUtaFpez+cFmA1t1rVzI7Df71rcU83trslSvSpTusKdqLiDN32Uuqb9P6q0JNPN4JSzLSf0iGs1CFqdjWJQs8kBpFI/8Od6x5jLBt0HPH75nUqHRyO8AZGMkymEMZgRz2K0BtkzCAKnvk8ztdKin2VvWCLil90b1JgXKIuUoDJdDN1vRkzsv4C2JQlapVagb9IK/9NUd9t2BmdAGwEbq/5TM7Urwwi0y9yrNvmkVj4Y9POoNLC7uZHB2GamP8twslY+MvqzIt8VUTR/opXrqiKbDXMq+w9x2imcLGXllpQLXsylN55WoyWHQVsSjxcBZzUbuQGMBrxnonRr/2DLRXJvLLZFoh2FLn77Yzdy/o0njuU7mNi4hc+MUqNnLo3KDHKVzWRQtFSqaCtkEMri26SgnDtb4gJqZ6495MhLtMMjcOuyahmfPRdNh7o04Uh+jQG20AlWLWJyMksMYQebO53Fopt8UqVx2Kcfno8tHOFOXSfnAUu4ZIl124Zk2WI0MWgGbh83tJnM7VqvQnqBE93EfWLIFnI9mUELmlsxhkD+bb5DK3dCkFz49l/zhOOmrC7R3CpChkcx1RNNl7k1S37aO4rlPQPUhD9TR3CviGJz4RkBOiG+kVD4yOtIi3rDv+OwRtk9x2zudZG7bKgEtlJT6WAEdJ7zQUs7AUsbgRjEPs4GvvFqijL1aqHLuH+DzqYN3/M42FrD76nO5f2Irg0w2Rvxx8k5k+OMpPYHb3qHkNNNKaCPy9goepxM9YIpn8ft+rqHJyNztOaNE53FK0jHuTmeVauh6MYfaPGZT81GPdyX6YQykTEp6kqK22beonQ0c0XTune84XFjBwLSYXiwyVx+hGNqu0ow30B9Si5HzaT7KJDXq2frukwLMhWxHV+1kL4nyRfRs9BX6NkwwdiV42vrWezmXW+1SBc7TaiibLYdpoQK6ucoy6XY3XMji0q2nhHvNhYpsJMvGSpdfjlvx3h5EntS8nK+6FMP2n6F4ls9nUDRP0VuwwHuCdNsLMKU+N/vR4lyM6r0TXzPcbwtY1Z4I/n3p8ighk/0FoZJMZUIuXLkAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.switch = None

            def _filter_bad_surf(self, brep):
                faces_list = ghc.DeconstructBrep(brep)['faces']
                invalid_srfs = [_ for _ in faces_list if _.IsValid is False]
                valid_srfs = [_ for _ in faces_list if _ not in invalid_srfs]
                bad_breps = map(lambda x: gk.Types.GH_Surface(x), invalid_srfs)
                return bad_breps, valid_srfs

            def _copy_trim(self, data):
                target_sur = gk.Types.GH_Surface(ghc.Untrim(data))
                res_surfs = ghc.CopyTrim(data, target_sur)
                return res_surfs

            def _fix_surfs(self, srf):
                return map(self._copy_trim, srf)

            def _join_breps(self, brep_list):
                t_join_brep = ghc.BrepJoin(brep_list)['breps']
                join_brep = t_join_brep if isinstance(t_join_brep, (list)) is True else [t_join_brep]
                t_union_breps = list(rg.Brep.CreateBooleanUnion(join_brep, sc.doc.ModelAbsoluteTolerance))
                union_breps = [None] if len(t_union_breps) > 1 or all(
                    [_.IsValid for _ in t_union_breps]) is False else t_union_breps
                return union_breps

            def _replace_obj(self, tuple_data):
                time.sleep(0.01)
                bad_srf_id, fix_brep = tuple_data
                if fix_brep is None:
                    return bad_srf_id
                else:
                    if fix_brep.IsSolid is True:
                        res = sc.doc.Objects.Replace(bad_srf_id, fix_brep)
                        return res
                    else:
                        if self.switch == False:
                            return fix_brep
                        else:
                            sc.doc.Objects.Replace(bad_srf_id, fix_brep)
                            return "the order {} Open Brep alternate successfully！"

            def RunScript(self, Breps, Toggle):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    self.switch = Toggle
                    re_mes = Message.RE_MES([Breps], ['Breps'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        _turn_to_breps = map(lambda x: Rhino.DocObjects.ObjRef(x).Geometry(), Breps)
                        _invalid_breps = [_ for _ in _turn_to_breps if _.IsValid is False]
                        _set_breps = ghp.run(self._filter_bad_surf, _invalid_breps)
                        if _set_breps is not None:
                            _invalid_surfs, _natural_data = zip(*_set_breps)
                            _fix_breps = list(ghp.run(self._fix_surfs, _invalid_surfs))
                            _pack_data = map(lambda data: list(chain(*data)), zip(_fix_breps, _natural_data))
                            _join_breps = list(chain(*list(ghp.run(self._join_breps, _pack_data))))

                            _zip_list = zip(Breps, _join_breps)
                            Fail_Brep = []
                            _bool_list = map(self._replace_obj, _zip_list)
                            for _ in range(len(_bool_list)):
                                if isinstance(_bool_list[_], (System.Guid)) is True:
                                    Fail_Brep.append(_bool_list[_])
                                    Message.message1(self, "{} Brep failed to be repaired, please check again！".format(_ + 1))
                                elif _bool_list[_] is True:
                                    Message.message3(self, "{} Brep has been repaired！".format(_ + 1))
                                elif isinstance(_bool_list[_], (rg.Brep)) is True:
                                    Fail_Brep.append(_bool_list[_])
                                    Message.message2(self, "{} Brep is open Brep（Open Brep）,input ‘t’ to alternate".format(_ + 1))
                                elif isinstance(_bool_list[_], (str)) is True:
                                    Message.message3(_bool_list[_].format(_ + 1))
                            return Fail_Brep
                        else:
                            Message.message3(self, "There is no damage in the input model！")
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'Brep repair'


        # 模型比较
        class ModelComparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ModelComparison", "R33",
                                                                   """compare modles by area and length""", "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("df42aa2d-1097-49b7-8560-9af741b3ddbc")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "A_Model", "A", "a set of modle")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Set", "B", "A set of section comparators")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Area_Tolerance", "T0", "area tolerance")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Length_Tolerance", "T1", "length tolerance")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Result", "R", "Comparison result")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "subscript after comparison")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARBSURBVEhLrZR9TBt1GMdPw1zUP6Yz0RhxzoiKkdKtL5Te0btraYXxqhmGMWAhjLE5bRHKBltpC5byIuBgCwH24gaEocsk4hZDWCYYNtzCGEwdCVgotN14HRIrrCDc4139wbaIJGo//9zv+Xzvd7mX5x7s3wDn3n+CqQwWg9H4OFKeZa4Al0K5HG4dJAKR8iyDWcINP2qEp+vjBS8i5VmYL2OenC+j28YOKV5AyrMsVpCpUB8Cg4eCDiPlWaZyAtKZIhm07BFlIuVZmKZ3n7NkiG4bo6lnkMKgjfJivo4KZ76IJJBam4VyUszUhpy/V0JfYqojpJyDkZ3PLp5StdqKyUGLQToyWkj+MGGiY7lsqTa0ecAUxPRoRXZrNp4BgD3G+X+EOSJrmCsj4WKiX3NvmhDummTfOKuCh7syxX1XUvm1wzrJXJda1HR9L//OryX0L325hLVK9QbhyMPr+nTSyboE/6fRpVanXytoGNCKf7MVUZmN230i2nfzHK3J/lfYyAtqlJvmS8gZm1nldzzUx7tjD7/FJPd5jdvX+7Fw4PI+YTm3XhMfDFvfoxa2dH4oMnE1hVFe7MH92ExZ4MYZPd7fmR64kauXYSpC11t1VNytj0T72XLtV8Qx/okipk8jUaFyBaZE9upsLjF1TU15I+VmLI+UjhaGbP5ZLS52mYhuqIl4CkV/Z9pMU5MG2d6rKVvirMYH3cLBFJK82TxivieL2owUBjWp6+xGche3bt8lkEM5DdMmWbw7fBhugE0aKd/xXDprtoi84Mgjjlp0kg9Q7IYpIKWLZhncPEC+jhTmzCc1dvaGuPUfx+gQ+FwJfZmBq38Lm1ayw1VKjzP1IQtw/B0YNeAHJvJlK3OHKaaDoZQGS7ZciBQ2fjigdKEgyMqcUDUzJ5X3HflBcDrKNxzFjzJhptLhmBKgnARgW9WuJya70iVhbPTXR84nI+GogvXkNq4eLFJuGNKT3cNZAeAw4nA9TQTdGhE4T0TEMnUJj7brHTPlazPJvrNkSeyWNAH0qgXQuU8wjWI3TAEVB5VKGM0hkrm6JlW47vsUfrtVK4ZrqXy4nMyD/kwxdGsl0G2Sv+LetMyQXhY9WaSwjeTgd29oxOzMl8JwDg5Tn6k6HJXROHcOFLLDrkoFM4YgnXsTS/17Pt4X4v0avorzc56NfXvufByvrS76zUgUP+Bqgv/zHcn+90YyxHBbI4Cf1FvAqhXBjf1bF5fbkjGTB6FaBU6j9KR700OciQl8qTFJ9jIqV+fs9rckrUlbv23ayfv93A7e/UtJ/PaLiTwlirFRHbF7jO2ifq04B6n/Rn1KqHdtonITKldwVigq5xtCwXkkuAQpz2LVE82LZRQMGQhuNnkOV6EiculUWCfUhgM0RgCcCYOF6m03xwrkUeiU/4crj4xc+lRhculxw4JBopszSPTsyMi3Z+PcP7IGGPYnSNPlz8hGRhsAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.local_tol, self.area_tol, self.length_tol = None, None, None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [_ for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def _origin_data(self, single_brep):
                center_pt = single_brep.GetBoundingBox(True).Center
                center_plane = rg.Plane(center_pt, rg.Plane.WorldXY.ZAxis)
                curve_list = rg.Intersect.Intersection.BrepPlane(single_brep, center_plane, self.local_tol)[1]
                section_brep = rg.Brep.CreatePlanarBreps(curve_list, self.local_tol)[0]

                by_area, by_length = self._get_area(section_brep), self._get_length(curve_list)
                return section_brep, by_area, by_length

            def _get_area(self, a_data):
                return abs(rg.AreaMassProperties.Compute(a_data).Area)

            def _get_length(self, l_data):
                return abs(rg.LengthMassProperties.Compute(l_data).Length)

            def _compare_area_to_get_brep_index(self, origin, handle):
                total, count, res_index = 0, 0, []
                while len(handle) > count:
                    flatten_list = list(chain(*res_index))
                    sub_index = []
                    for _ in range(len(origin)):
                        if _ not in flatten_list:
                            if abs(handle[count] - origin[_]) < self.area_tol:
                                sub_index.append(_)
                    res_index.append(sub_index)
                    count += 1
                return res_index

            def _compare_length_to_get_brep_index(self, len_origin, len_handle):
                total, count, res_index = 0, 0, []
                while len(len_handle) > count:
                    flatten_list = list(chain(*res_index))
                    sub_index = []
                    for _ in range(len(len_origin)):
                        if _ not in flatten_list:
                            if abs(len_handle[count] - len_origin[_]) < self.length_tol:
                                sub_index.append(_)
                    res_index.append(sub_index)
                    count += 1
                return res_index

            def RunScript(self, A_Model, B_Set, Area_Tolerance, Length_Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.local_tol = sc.doc.ModelAbsoluteTolerance
                    self.area_tol = 0.1 if Area_Tolerance is None else Area_Tolerance
                    self.length_tol = 0.5 if Length_Tolerance is None else Length_Tolerance

                    # 内置源参数1
                    temp_geo_list_1 = self.Branch_Route(self.Params.Input[0].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list_1]
                    Abool_factor = any(length_list)

                    # 内置源参数2
                    temp_geo_list_2 = self.Branch_Route(self.Params.Input[1].VolatileData)[0]
                    length_list = [len(filter(None, _)) for _ in temp_geo_list_2]
                    Bbool_factor = any(length_list)

                    Result, Index = (gd[object]() for _ in range(2))

                    re_mes = Message.RE_MES([Abool_factor, Bbool_factor], ['A_Model', 'B_Set'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        if len(A_Model) == 0 or len(B_Set) == 0:
                            Result, Index = [], []
                        else:
                            A_Model = filter(None, A_Model)
                            B_Set = filter(None, B_Set)
                            str_guid_model = [str(_) for _ in A_Model]

                            True_Model = map(lambda x: objref(x).Geometry(), A_Model)
                            "------------------------------------"
                            # 切换为实体模式
                            True_Model = map(lambda y: y.ToBrep() if 'ToBrep' in dir(y) else y, True_Model)
                            "------------------------------------"
                            temp_result, area_value, length_value = zip(*ghp.run(self._origin_data, True_Model))

                            if B_Set:
                                com_area_value, com_length_value = ghp.run(self._get_area, B_Set), ghp.run(
                                    lambda brep: self._get_length(rg.Curve.JoinCurves([_ for _ in brep.Edges])), B_Set)
                                index_by_area = self._compare_area_to_get_brep_index(area_value, com_area_value)
                                index_by_length = self._compare_length_to_get_brep_index(length_value, com_length_value)
                                if index_by_area == index_by_length:
                                    temp_index = index_by_area
                                    Result = ght.list_to_tree([[str_guid_model[_] for _ in sub] for sub in temp_index])
                                else:
                                    Message.message2(self, "Angle tolerances and length tolerances have different results！")
                                    temp_index = index_by_area
                                    Result = ght.list_to_tree([[str_guid_model[_] for _ in sub] for sub in temp_index])
                                Index = ght.list_to_tree(temp_index)
                            else:
                                Result = temp_result
                        return Result, Index
                finally:
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    self.Message = 'HAE Development Group'


        # 模型展开
        class BrepUnfolder(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepUnfolder", "R24",
                                                                   """Profile fab model expansion plug-in""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("132a0a95-c9cd-4a12-a80f-05d7d0aeec8a")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "fab model")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Surfs", "RS", "target surface")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Axis", "RA", "target axis")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKTSURBVEhL5ZRLaBNRFIZn8phEmza1JZqHTUjS5l2hC0vBRaWC+CgaKlJrGEFJRVQUaVWkvoq1FFt8LEoKooJWXLgpSHUlcWFpVq6tIM3CTRR3QqEUjv+ZOyaR6mqyEPzhW8ydM/e/nPPfkf57ZexmecZu/R0Fa3jXJUoMSLHIs++P+6k4HKbi+ZDgchvN7HcTXmdFlQHxab9dbCWaTBDdjgvupej10a1soIoqA4JB7vO5EK3ditHa9ahgPEEvD/vY4JioMiBZkh75nVYKN4FNOs0KuR0WNsiIKgNqUMzPXg34aGEwQAsn/ILTQbrW3cwGfaLKgJps5qc/rrQR3cEMxtF/5kEKLfLWxqBRMT8sIUE0FiO6GRXAbLbP80eDLs5vdZ4ZXjPL0rp1xmqSP+3wb6Ce0EbqCeqE6yjuUtggLbatKMv55RyXM43TzaPHvZE6KiKO5XVmKEwHog56q7bQEpK0dDYoGG6l0Z3aDPaIbStSOb+c43Kmke+PZ4KUaW8gmkpW1hm0Qt3mpNIQ7sFE1T24n6Inae2irTd4cchLK2NxWhmJCNDTRSSjP1kvPr6BHv8C2R9INWinXsXz6tWIAIOe3reFDXrFthWpSZeNutHP7oAOerrdayenzVTq8NgKHe4q8NxoMy3iDrxDz/NlNit5j8OSx36dYtuK1McHPVTCKUroowYi+OFkgGRZmtZrDEmd5xncrZoB+vwVRkhMTq8xJDWHFC0jRctIiQaSwn9LBZHUawxJ7fTZKY2BpmMOQbyediPXfA/0GkNS546gRZOI4yhuJoNEfLkQ5hbVxuBNpkXLcfm/MpWg75e0GdTEYHBil4sKuFiFbEBwKkBz/T7C7+K5XmNI7WDkL+wF/6Ik6SelEYfmZ4ql2QAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = sc.doc.ModelAbsoluteTolerance

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def Branch_Route(self, Tree):
                """分解Tree操作，树形以及多进程框架代码"""
                Tree_list = [list(_) for _ in Tree.Branches]
                Tree_Path = [list(_) for _ in Tree.Paths]
                return Tree_list, Tree_Path

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def along_cur(self, line, base):
                st_pt, ed_pt = line.PointAtStart, line.PointAtEnd
                set_pt = [st_pt, ed_pt]
                pt_coordinate = []
                for _ in set_pt:
                    rc, t = base.ClosestPoint(_)
                    pt_coordinate.append(t)
                pt_index = [0, 1] if pt_coordinate[0] - pt_coordinate[1] < 0 else [1, 0]
                new_set_pt = [set_pt[_] for _ in pt_index]
                new_line = rg.Line(new_set_pt[0], new_set_pt[1])
                return new_line

            def _get_grid_lines(self, base_surf, sub_surfs):
                base_line = [_ for _ in base_surf.ToBrep().Edges]

                count = 0
                total_list = []
                while len(sub_surfs) > count:
                    sub_dist = []
                    for index, line in enumerate(base_line):
                        new_curve = line.ToNurbsCurve()
                        mid_pt = new_curve.PointAt(new_curve.Domain.Mid)
                        test_pt = sub_surfs[count].ToBrep().ClosestPoint(mid_pt)
                        sub_dist.append(abs(mid_pt.DistanceTo(test_pt)))
                    min_index = sub_dist.index(min(sub_dist))
                    total_list.append((base_line[min_index], sub_surfs[count]))
                    count += 1

                return total_list

            def temp_fun(self, data):
                curve_data, face = data
                curve_data = curve_data.ToNurbsCurve()
                curve_mid = curve_data.PointAt(curve_data.Domain.Mid)
                edge_list = [_ for _ in face.ToBrep().Edges]
                dis = []
                ran_list = []
                flip_curve_list = [ghc.FlipCurve(_.ToNurbsCurve(), curve_data)['curve'] for _ in edge_list]
                for edge_index, edge in enumerate(flip_curve_list):
                    ran_list.append((ghc.Angle(rg.Line(curve_data.PointAtStart, curve_data.PointAtEnd),
                                               rg.Line(edge.PointAtStart, edge.PointAtEnd))['angle'], edge_index))

                new_edge_list = [edge_list[_[-1]] for _ in sorted(ran_list)[:2]]
                for edge_index, edge in enumerate(new_edge_list):
                    rc, t = edge.ClosestPoint(curve_mid)
                    if rc:
                        test_cl_pt = edge.PointAt(t)
                        dis.append(abs(curve_mid.DistanceTo(test_cl_pt)))

                min_index = dis.index(min(dis))
                return self.find_curvature(new_edge_list[min_index])

            def find_curvature(self, o_curve):
                start_pt, end_pt, mid_pt = o_curve.PointAtStart, o_curve.PointAtEnd, rs.CurveMidPoint(o_curve)
                ref_line = rg.Line(start_pt, end_pt)
                ref_mid = ghc.CurveMiddle(ref_line)
                curvature = abs(mid_pt.DistanceTo(ref_mid))
                return o_curve if curvature >= 0.1 else rg.Line(start_pt, end_pt)

            def flip_curve(self, tuple_curves):
                l_curve, r_curve = [_.ToNurbsCurve() for _ in tuple_curves]
                r_curve = ghc.FlipCurve(r_curve, l_curve)['curve']
                return r_curve

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result_Surfs, Result_Axis = (gd[object]() for _ in range(2))

                    j_bool_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    re_mes = Message.RE_MES([j_bool_1], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Brep:
                            face_list = [face for face in Brep.Faces]
                            map(lambda shrin: shrin.ShrinkFace(rg.BrepFace.ShrinkDisableSide.ShrinkAllSides), face_list)
                            area_to_brep = map(lambda get_area: get_area[0] * get_area[1], [_.GetSurfaceSize()[1:] for _ in face_list])
                            max_index = 0
                            for _ in range(len(area_to_brep)):
                                if area_to_brep[_] > area_to_brep[max_index]:
                                    max_index = _
                            max_surf = face_list[max_index]
                            sub_surf_list = [_ for _ in face_list if _ is not max_surf]

                            set_data = self._get_grid_lines(max_surf, sub_surf_list)
                            leader_line, Result_Surfs = zip(*set_data)

                            rotation_curve = map(self.temp_fun, set_data)
                            Result_Axis = [rg.Line(_.PointAtStart, _.PointAtEnd) for _ in map(self.flip_curve, list(zip(leader_line, rotation_curve)))]
                        else:
                            Result_Surfs, Result_Axis = [], []

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result_Surfs, Result_Axis
                finally:
                    self.Message = 'profile model layout'


        # 区分是否带孔Brep
        class BrepHole(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepHole", "R32",
                                                                   """Distinguish whether the Brep has holes or not""",
                                                                   "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("db89262c-b474-413c-8cc2-91b6ff1bbb6f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Geometry", "G", "please input Geometry parameter")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Perforated", "P", "object with circular hole")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Solid", "S", "object without circular hole")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUCSURBVEhLvZZ/TNRlHMfvvDvujoOD+6F3x3EigoSCuoliiNpJbsDQSbGaJqRO7ZdjiWauTSoNQynRQsvfOIzN2EzT0pU/cKWIvzF/JlZqWluWUOrcwPnu/XmOTvqu1X99tte+z/d5P/d5f7/P9/M8z+n+zxhNntSQTyR6keEahpEI0oMMJIM1OEk4MvoFDCgttmH2JBvKSGmJDdmDTKA202bSH85NsiGvH0kmKVHIireKVkUWD/FZEEyMRLBPiNEJVliN+rPULETF41MLrMCv8cClOOAC+T2AVa/aJUllP5fpCt5KBZYMAN7uDyxLw5kXE0XbRraffqEP8G4asJhaJccsTEWiw3SXWvgtgsX5NLgYh7KJtorC0ebn7h7z4v25ymBhstN0qXNBivoh3nhEmRyZkSDaFkHaqGTyN6ktSkVneYoY3KLmICpCBnzyybmWeWmJhqI7zV7UvPLQoENj0NzNQNrqzUTjGBmrNcgJT9E3PuCkF2gPT1FFisvUigomX8ppkClYno5zs9QUfSycfSkRqBaNJkupczqTnKY2amGD7Mw0E2oXx2LzwhjUL4pB7ZJYPDXWIkkWeKOMP++c5Mfu4gB2T47H7qkBLM/tJdpWsu2DAg8aZyagcUoAjdN6Y29JAJ4o431qsUSFnkwhr2koJXbyDHlPwwqSTjLJarJOwwwSjgDZSBo0bCBSCePIWtI9gdznkWRSTbQP8DwxEBXTigfZ0TK7L1pYcgq2pY/alGirvuWzageOfOTG+QY3jta78UlVLMxcH9Trqkqjsa/WieN1LjTVurD3QydSehvlt/LgKp6dn+0EVqSHallgW/pEc8Xom+6zqtDiw4k6180Hp3wP7n7lQaRF30h9UzOT4ic/zm5xt9/c0/MervoxPN3USa2PJJcoKXvUEaoAKTWBbekTzWnXH8Jxr3z8Zhm8qdze2NGkDPbzdmPTBhdu7lEfPakoaJmPb+OQOcDUwfsEGS9RMieLBlU0kMUisC19oonBvYMetG53/7bs5eg1F7e6f2nf3ytscGC1E51nfKh9PebLxjWOc7KehvX/u8H0uWLwDmtZFpPAtvSJ5ozWH5MpwTV/iB/9uLWPBmb9Ier1h/kGMkWK66Q1DsNZ9tQSJblEpsdmuDzUb7kx1GcOwTb7vqOWYTTqNuYMjWjLyza35WWFrsGMiDaDXreS+pzswaY/CsdabhcGzbcLx5Ac822HXX+BWngviiKVREqvO+VEYjaRiulOE8klI8gJckpDDQnHrHxuxdXjPajmClWM8yCD2zC1Aq+rxw+7Vjiwf60TB9c5sW+9E+sXxIj2KamXVd19Jcs1YDdKFXmIirkyCKsGhipJqBmImUNUkqeT4w0XcJp7VKsPHU0sV87ztZ09RdtONh9lcizvthfxOsAdIdu1j6goq8hxh6rorzLl3l8SWmhFff2G82CVbKmIORBt0WWda3C3X/9claWcB3XyxCp5124q11RXxB1qXqLivw34Bl+sdJycNj5y+vc73He63kAZHBCDJTToOg/kqjWY9y9TNDHJb7iMFk7Nla7T7oYfV3cog12k4fD03uqUC59ovPZ3R8g3iCMqZowIWFE2yqVWr2KkSwZJklGRVv3X40aaMSFoxhNBCyaMsWBMhtKkUsoHe80I9n14Jj9GeI5fpibVqUIO5yJSoqGASPQk2n8Vsk1biWz1//Svwq3T6XR/AuoV/1LH16SbAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            # 根据树分支和路径还原树形
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 判断圆弧是否闭合
            def CurveIsRound(self, Curve):
                # 先判断是否为弧形、在判断是否闭合
                return Curve.MakeClosed(0.0001)

            # 是否为带弧度的曲线
            def IsHole(self, Curve):
                # 判断原曲线 和 曲线头尾线 两条线的中心点距离为多少
                Curve = Curve[0].ToNurbsCurve()
                Start, End, Mid = Curve.PointAtStart, Curve.PointAtEnd, ghc.CurveMiddle(Curve)
                Line = rg.Line(Start, End)
                Mid_Mid = ghc.CurveMiddle(Line)
                Curvature = abs(Mid.DistanceTo(Mid_Mid))
                return Curve if Curvature > 0.01 else None

            # 是否为闭合的 圆弧 多进程
            def IsHole_Multiprocess(self, Curve_list):
                if Curve_list == [] or Curve_list == None:
                    return [False]
                Bool_list = list(ghp.run(self.CurveIsRound, Curve_list))  # 得到列表是否为闭合的圆弧
                return Bool_list

            # 得到合并曲线
            def Get_Curve(self, Geo):
                if not Geo:
                    pass
                else:
                    if 'Point' in str(type(Geo)):
                        Curves = [None]
                    elif 'Curve' in str(type(Geo)):
                        Curves = [Geo]
                    else:
                        Curves = list(ghp.run(self.IsHole, zip(Geo.Edges)))
                    return list(rg.Curve.JoinCurves(list(Curves)))

            # 去除多余的真假值
            def Remove_Excess(self, Bool):
                if True in Bool:
                    return True
                return False

            # 有无圆弧的Geometry分开
            def HoleInGeometry_Bool(self, Geo_Bool):
                Geo, Geo_Bool = Geo_Bool  # 两组列表
                if Geo_Bool:
                    return Geo, None
                return None, Geo

            # Geometry 炸开成曲线,判断曲线是否是圆弧
            # 分类是否带圆弧的 Geometry
            def Geometry_Multiprocess(self, tuple_data):
                Geometry_list, origin_geo = tuple_data
                if len(Geometry_list) == 0:
                    return [], []
                else:
                    Curve_list = list(ghp.run(self.Get_Curve, Geometry_list))  # 得到所有的合并曲线,查看是否是孔得到判断结果
                    Geometry_Bool_list = list(map(self.IsHole_Multiprocess, Curve_list))  # 判断是否带孔的数据 真假值
                    Geometry_Bool_list = list(
                        ghp.run(self.Remove_Excess, Geometry_Bool_list))  # 简化[[False, False--]] 变为 [[False]]去重 有真则为真
                    return zip(*ghp.run(self.HoleInGeometry_Bool, zip(origin_geo, Geometry_Bool_list)))

            def RunScript(self, Geometry):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Perforated, Solid = (gd[object]() for _ in range(2))
                    # 带孔Geometry，不带孔Geometry
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_brep = [i for i in structure_tree.Branches]

                        Geometry_Tree = [i for i in Geometry.Branches]  # 拿到数据 二维列表
                        zip_list = zip(Geometry_Tree, origin_brep)
                        res = map(self.Geometry_Multiprocess, zip_list)  # 得到物体是否有圆的真假值
                        Perforated, Solid = zip(*res)
                        Perforated = self.Restore_Tree(Perforated, Geometry)
                        Solid = self.Restore_Tree(Solid, Geometry)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Perforated, Solid
                finally:
                    self.Message = 'Distinguishing circular hole'


        # 圆孔修复
        class FixHole(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_FixHole", "R4",
                                                                   """repair circular holes on Brep or Surface""", "Scavenger",
                                                                   "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8767239f-b1fc-432b-8fc0-7585f032402c")

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
                self.SetUpParam(p, "Hole_Brep", "B", "Brep to be repaired")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Repair circular hole accuracy")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "No_Hole_Brep", "B", "repair Brep after circular hole")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASySURBVEhLzZV7TJNXGMaBAmplDhemMhEFJlgspS3FIiQOAooMEZAlM4ZFtkoLUqVGGRkGE50TzaKiu8myyGUTOjenmQPNwmImpfdWCs4KKrqQRbzOqMvQQp+9px/xQlnc7Y89yfPH951zfs857znn+3z+T+KRs8m15AT24r9SOHkT2ZgqDEHla9EIe2HiDXpmQdPJ/1jp5MbwkEnXNMuicOb9RS73sdxh98kC9/1D2fc35ka5Av39+qnPOrIfG/BXFErW8Px8bUvF09CsScDdpiy3+7t8N47mAi3ZwCHyVzlwt60YOf9B+u8r5KFuGmMgL2WAP1OYj6/PwZiZk+9UUwnO7U0DjhHweD7w5TKgmaDjmULdrStc7VuThxNfngri7ORw3sotWzQLD7UE+74A+Gb5+MAnfTjHs5Lhz1+F67NMnFZLEcDz7RvleSlGKQ11X6tKwe396dzg8WbOJkBQ1navbjH6t6bASmDjGhE6yTOnBF4n1vMc8mlNyogMvtqrToRljQQXq5IxVL8U+JpgLQRlYQR2NWXh2u5UnK1YAIMyHjoFgd+MpgABHGoJ4kMnjxArhkOOkSCEbzhTmoCuUhnMCgnOlCRgcFcqRmjm9z5d8mi2nQTV02xNKjGFzEf3lgJ0vZONXo0YmZF8tg8ZHHGMggJ5De2rRThblgg7wW1KqWc1jvUymEok6Fgdg47CcOiLoghOIW9F49IOJXDuFtzO6xhsqMe6tIUsoJgjequyMX8eetcv8ARwphClBHrFPM8sB7Qfoa+2HOYyMTqLwnDuvSrcaPkRvx3T436rFe3bD7CAHRzOWzlb0+agXyN/BGe2FsfBvj4ZLp0FGAQe9NxE34F62DfloUOZgPbyQhjfrcFD+y9oq65mAVoO563YIvEMXN7wdIBFIYBz8yqgzQDXiQ7cbNDiap0WFz5shl2TBtOaSOiVcXCUp+LoKgEC/HyNozwvBaVHBF+/UM5KxME9pnqb1IvQVbMbA3VHMGK/AjguYei4HrYN2TAWC2iP4mEtEUJHqw19LmCAWIEccowEL/LNDs9JerwCZosqDh2qROgqFLjRasJQ9y1c+WQfDMXzPXBTiRjmUjG66JTFTZ/8gFCzOOIY8QN5X5woFOInteypAKtKAjOFGItjaMNFsKxNg+6N2fQc6zlhLIDZWS5D5lzPJ0POEb21ecsr4bTRT5RJJYWNAhjAoIjBhd1q3DHo8HNjLSxq+WiJuPa+DTIoEmawgNc5nLcKCkXTMFiRBNsonAuQ0qUSwqZOBk6ZgZ5B/PqtCc49dbBqMmFUxsK6VoKrlXLsXBLBArZxOG/NnREUOHxkZSwGNsrpNj8OMVGJzGULcbn2Y9zWtmNE54DrpA39NW/jvHoezLSCPVmRkL4UxAIqONz4kk+ZwHPsSJ+Di3TpnGUyzwoYwKQS4rQqCfZtVUA3XQp9D34oSce6BSGICJ54l8YeJKd4KM/QRPK+xVFTcapIhCu0Jxaqs43K0FseD0dpLJpWJiFPOBt8no+T+laSw9jAv6vlIXz/gV0ZEbioSYRBFY/tGXNYGdhfrJWcR/ZnHf+N2I/9cHL4FMwOnsC+93vJItbwbPn4/AHatyJxkIwp4wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

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
                j_list = filter(None, list(chain(*geo_list)))  # 获取所有数据
                return j_list, geo_list, geo_path

            def remove_hole(self, tuple_data):
                brep_list, origin_path = tuple_data
                # 定义修复列表
                new_brep_list = []
                list = List[rg.ComponentIndex]()
                # 循环列表修复Brep
                for sub_brep in brep_list:
                    if sub_brep:
                        for loop in sub_brep.Loops:
                            if loop.LoopType == rg.BrepLoopType.Inner:
                                list.Add(loop.ComponentIndex())
                        new_sub_brep = sub_brep.RemoveHoles(list, self.tol)
                        new_sub_brep = new_sub_brep if new_sub_brep else sub_brep
                        new_brep_list.append(new_sub_brep)
                    else:
                        new_brep_list.append(None)
                ungroup_data = self.split_tree(new_brep_list, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Hole_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    No_Hole_Brep = gd[object]()
                    self.tol = Tolerance
                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Hole_Brep)

                    # 判空
                    re_mes = Message.RE_MES([j_list_1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        zip_list = zip(temp_brep_list, brep_path)
                        temp_breps = ghp.run(self.remove_hole, zip_list)
                        No_Hole_Brep = self.format_tree(temp_breps)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return No_Hole_Brep
                finally:
                    self.Message = 'delete Brep hole'


        # Brep是否闭合
        class BrepSolid(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepSolid", "R31",
                                                                   """check if Brep is closed solid""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7094f91f-7ad9-4cce-ad24-5522ecc737b1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.quarternary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "object to be checked")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Solid_Result", "S", "if Brep closed,return to True；or else False")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAK7SURBVEhL3ZNLTBNBGMfBEA8ejAcj4jtehN2Z7u60tJW2FnoAkQJi4OzB1LtXPfQGxpMnKQ8FDK9WFqNS0vqImgAB8QEoD4NEBAqIIEZBXqGfs8uEaKBLUjnxSybZ+b5//v/MN7MxOw+b7bQj2WCoJZL0wqDXVxqNRjNrqYTD+dzCfNblmWFH4ffPqTfmp89eAThvZW1tLBZztiSKIOh0f68Vvd6kGoTDOdemBtNWh5oJhIISTD0VYPq5Hhb7UiEcdvoBnHtUo81wu91x1GxcMeU5bhUjFOCSklaUPcaCrGiWv53rnhlKg45qBD31CPrv8fBRxvDjjRUWZzPhSVPWSdVsM+x2exzG6BY1HBQEodDlciXoMF6gCxBCzxRNyGdtne0ww3inCcY6jDDWboSRdhN8emmAYBlZrijKPaGaaQEAsc709EQ6qi/0FCDSE4hYvKj0QrKtbfS+CL01HPTWJUFPDQ+vKzloK02EQDFZaii/cFw10YKOaheRhC51NAgtiaJ4ibXUgNAjCfq9PPR5OXhfx8Pbah5eVXHwuIQs+kqcx5g0Mk67fT81nhAwnqPm11lZRSsgSAPq7uQeZVJt0lJSTp2xWDLZdh3NAA9ZkEvzjjBpZBwOR7woCD30DmbpP5DPyioh2dqqcYLf3sr8w0wameRkkqH8CzREueBGVlbZGMD9G1CctXUAfaL7EOJa6B18JYRksLLKtgQwYul49rLvdTQDPNJ8bXnOISaNjlBj5AD6TOdkT14Ck0aHVkCABvgqCg4yaXSMNdpaIo6olPx6UJYdz6TRsUXAT/lu3gEmjQ7NAM82BNBX9G7STzYEdK7dwWrZzf8c0UhDinvSr4epoAATzRhGmzAMPxRgoEEHAQ/x+3wFu5k0erpqiWlQFq8O+PjbH7yoqrseF7VW6Zy0Fbum2FnExPwB7KQEcGCtwI4AAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(filter(None, x)), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Solid_Result = gd[object]()

                    j_bool_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    re_mes = Message.RE_MES([j_bool_1], ['Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Brep:
                            Solid_Result = Brep.IsSolid
                        else:
                            Solid_Result = None
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Solid_Result
                finally:
                    self.Message = 'Brep is closed or not'


        # 沿向量两侧拉伸集合物体
        class BOPP(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BOPP", "R34", """Stretch the object along both sides of the vector""", "Scavenger", "D-Brep")
                return instance

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def get_ComponentGuid(self):
                return System.Guid("2fc1ad34-d653-4a44-88b1-5999a8057347")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Base", "B", "Curve or surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Direction", "D", "Stretch vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Extrusion", "E", "Stretched solid")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAL+SURBVEhL7ZbbSxRhGMbfyAOtus66J1udVVx13Z3zuLvaZi6oncNFwhJ0E8wKNLADGV2EdNFBaEHtogI7/AN6EbSQN4sIIhQR/QPlXRCrUIS5gW/fzkyt6zqY2F098MDM+3zv95vhY3gH1slJXLGF84iztM/nC/p8vnbtNlsnPYXRWC+9OhMpT870bO5Xfc7k5UbTLFmeq3YBhEKhUlkWJwSeR1EQkOf4OAH5tTit+23WBZzgEO969U3yF12OFYBiUyAQaJQE4bnAc2upjRmvVzHPcSqI52dFUewMBoNFCmC0zRrHUbLJiFvfJH/ZVbq421R1rF6WX4s8Py0IwvlQMOgjGyc4lkVJkiJ+We6QRPGZLMvvJEG6vi3A9GlHAgoKbEqTppGRkTyeZZdST8+KYkgrK+rs7FTP7E8BU6ccS2Q5pTRpCofD1C8AeaNDWjlT2wSY1C5V/wFp6wDGY7H8Kp5PVPIccsHgAa2cqZ0AwGCQ2m2l37rtDrRS1KBWzdTYEVscx1jEOx59kzzWXbYRYBwuMn3E8mrE8hqcNNl/GAAkLUtrwE/F5wcrcb7fqe+LlXi71bIR0DBnd+Ka041f6BpcJiB3Tt41LUsrAIb4JbDhBbDqeojkB6FoI8Byy2heQroWkXbjlMWBFORkn8MJMMYfgROjUK7rhyTvBXPWGeTn57f2W+wrV217sbrQeFMrZ+ooATwAGu9Bma4nSN4DJVmAx/gml2bZRBnLYG1j436tnKmdAMLh0Nbfwb8D6IaSZbLcqHap+stvYPpMVZZWRCIRs9YKiLiLbJ5IARiG+X3IZE4UtrS02JWbPwX0ArVodLsOy5L0nkyst2R0RpubmzvINFtmyURr8PuvNDc1DQf8/jlfff0HWRDUj+44FC88gQocJ5voeZLkZ6DkO1leSNO0w1tXd4PM4U8EhhzDKDNZuSYgkk26XC5Z2TwlDvZEz4Fl9SyYk32bOFUfAGuyCQpSfxXrf11yPB7PEMswXzmORcbjeep2ux1aRgTwE9f/qK4AhlbxAAAAAElFTkSuQmCC"
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

            def bopp(self, sub_tuple_data):
                base, vector = sub_tuple_data
                if "ToNurbsCurve" in dir(base):
                    contour_line = base
                elif "ToBrep" in dir(base) or type(base) is rg.Brep:
                    face_list = [f for f in base.Faces]
                    if len(face_list) == 1:
                        contour_line = base
                    else:
                        contour_line = None
                        Message.message2(self, "This stretch only supports surface or line stretching!")
                else:
                    contour_line = None
                    Message.message2(self, "This geometry type does not support stretching!")

                if contour_line:
                    pt_1 = rg.Point3d(vector[0], vector[1], vector[2])
                    new_vetcor = vector * -1
                    pt_2 = rg.Point3d(new_vetcor[0], new_vetcor[1], new_vetcor[2])
                    line = rg.Line(pt_1, pt_2).Direction
                    move_line = ghc.Move(contour_line, vector)['geometry']

                    ext_1 = ghc.Extrude(move_line, line)
                    ext_1.MergeCoplanarFaces(self.tol)
                    res_brep = ext_1

                    if res_brep.SolidOrientation != rg.BrepSolidOrientation.Outward:
                        res_brep.Flip()
                    return res_brep

            def temp_fun(self, tuple_data):
                base_list, vector_list, origin_path = tuple_data
                if base_list and vector_list:
                    base_len, vector_len = len(base_list), len(vector_list)
                    if base_len > vector_len:
                        new_vector_list = vector_list + [vector_list[-1]] * (base_len - vector_len)
                    else:
                        new_vector_list = vector_list
                    sub_zip_list = zip(base_list, new_vector_list)
                    ungroup_data = self.split_tree(map(self.bopp, sub_zip_list), origin_path)
                else:
                    ungroup_data = self.split_tree([], origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def RunScript(self, Base, Direction):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Extrusion = gd[object]()
                    self.tol = sc.doc.ModelAbsoluteTolerance

                    j_bool_1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]

                    re_mes = Message.RE_MES([j_bool_1, j_bool_2], ['B end', 'D end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        base_trunk, base_path = self.Branch_Route(Base)
                        dir_trunk, dir_path = self.Branch_Route(Direction)
                        b_len, d_len = len(base_trunk), len(dir_trunk)
                        if b_len > d_len:
                            new_dir_trunk = dir_trunk + [dir_trunk[-1]] * (b_len - d_len)
                        else:
                            new_dir_trunk = dir_trunk
                        zip_list = zip(base_trunk, new_dir_trunk, base_path)
                        iter_ungroup_data = ghp.run(self.temp_fun, zip_list)
                        Extrusion = self.format_tree(iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Extrusion
                finally:
                    self.Message = 'BOPP'


        # Brep相交
        class BrepIntersect(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepDirection", "R35", """one brep intersect with many brep""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("02152412-2406-4df4-a602-28ada483f803")

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
                self.SetUpParam(p, "A_Brep", "A", "Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "A list of intersecting solid")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance")
                TOL = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(TOL))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Breps", "B", "Resulting solid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "FBreps", "F", "Intersecting failed solid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "NBreps", "N", "An solid that fails to intersect and does not intersect")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI/SURBVEhL5ZRdSFNhHMYH1UZfOzqXbI5BgTU7OMSPaJnGJHJtLCiEQJKWYqkQRKAXw0YWaiVZFwU5IyK1Dw3qKOwmJCiThQZrLhEzmF4E1sWg++Dp/zbaPHLO2QkJoh74XbwX7/M778d5NRQ7cX4NbCMUc+6Ipxw9XS3oaK9XTU9nM4rs+aD5pcka+TRdDjTg69Io5qMPVfNlUcBRbwUTFCVr5NPkbz2BjzRp6nVQNfPvh+BxOf5ywbs3dxEJ35MkPvsEXvc+JuCTNfKRFExP9GNy/DZCYzcgPOuF8FzMy/E7cDrLmKCSyJZhPSEtYOOzLTWwW7bCWWCAc5eYqoIcmDkdHPYN31zlukS1Q5vCValLbDevS1D3zxsmLZh5hOO1Htw/tAnotgGBfDGdNjQW6xF9mgN8ygM+mNN8tsB/agtbnUNRUFvnxYBbD1zjgQ6SrOQKj9MlHN4OGYAYlU6b0pCwrW4zE+zNKHhwmARXSXCRSlfSzaORBOFBEsyQYIqKf7GQh9Z/StB86UI9luMC5iKDKZYXR+FrOIZhDwf0FtKh7hZzvRBnSrIwOaBiBbadVlQf3IOqA8Up2NhqNaHCqoWvjMNJujEiSjnwJi1mR4wZBVmETYabwYAekZARkRGDmGEDFgQjvoepkN0cBYFS2l710RbELUCUvlKK1eW/KWh/cSsbmKMfaXWJEv+XYKKfzmCJzoA9B2pJv0UZBV1Bvx6xsVzEHhvVE8qFz7uRCfYna+TjJvrWwA7iT0aj+QH/tfe4voVjcAAAAABJRU5ErkJggg=="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def thread(self, A_Brep, B_BrepList, Tolerance):
                Breps = []
                FBreps = []
                NBreps = []

                for B_Brep in B_BrepList:
                    if B_Brep is not None:
                        # 得到两个brep的交集
                        Intersecting = rg.Brep.CreateBooleanIntersection(B_Brep, A_Brep, Tolerance)
                        if not Intersecting:
                            LineB_list = B_Brep.Edges
                            PointB_list = []
                            # 取线上的点
                            for LineB in LineB_list:
                                lens = int(LineB.GetLength())
                                nurbsCurve = LineB.ToNurbsCurve()
                                point_list = rg.Curve.DivideEquidistant(nurbsCurve, lens / 20)
                                for k in point_list:
                                    PointB_list.append(k)
                            # 定义相交开关
                            Identifier = True
                            for LineB in PointB_list:
                                # 是否相交
                                if A_Brep.IsPointInside(LineB, Tolerance, True):
                                    Message.message2(self, "End B has solid failure with A Boolean, please check")
                                    FBreps.append(B_Brep)
                                    Identifier = False
                                    break
                            if Identifier:
                                Message.message3(self, "There is an solid on end B that does not intersect with the solid on end A, please check!")
                                NBreps.append(B_Brep)
                        else:
                            Breps.append(Intersecting[0])
                return Breps, FBreps, NBreps

            def RunScript(self, A_Brep, B_Breps, Tolerance):
                try:
                    Tolerance = Tolerance or 0.001
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[1]
                    Breps, FBreps, NBreps = (gd[object]() for _ in range(3))
                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['A end', 'B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Breps, FBreps, NBreps = self.thread(A_Brep, B_Breps, Tolerance)
                    return Breps, FBreps, NBreps
                finally:
                    self.Message = 'Brep Intersect'


        # 获取圆管曲面的中心线
        class PipeCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PipeCurve", "R43", """Get the center line of the circular tube surface""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("188ca450-6f97-4b4f-922a-ff30a31d37d6")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Pipe Brep", "P", "The center line of the round tube to be extracted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Center Curve", "C", "Extract the center line")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOSSURBVEhL7ZRrTFNnHIdJNEY/Or+5BKczXiic+wF6Vm2rFgUvG7GnslqoiEKl4rxMFm+pWQQvkWRzmnkBAcFiO7UXURD1izrnlM37B90W3RYNc5vxNhOGp7+9x74qRAk65weTPR/b8z7vk//55yT8z2vnYcgxqyOcvVP7asqmDn+mjf786sSiDlkL279Gswrs+wCIvA/sngRt+/h6BNU+9LGXB9XuvlpYLdf2ZmuIEnFdJlA7AdieAVTagF0ToX0+NkQffzk6Ijk2LWS/iCY70DAR2EHENeOBKiLeMg7YNBb4bAywOQPt5eZ8eqxnYoGCt0j1ZkSnAiEyijoiriVivXobkX9J5BuIuMKK2BoztLUW3FyuXAqqai+q6J6He3McWmjqzzhA5P6seHU1kevjeFJtBdZZ0FE2Grd9JrQtU3Dl4zR865WHUc2zIJqbqIXUIPaTceyZEhd3qSbiTtUPPh2lV+NqaTouzJdxslhCaAanUF1XYi1OT6zR/ieaSHU9fYk9VF9fasTlRWk45ZVwqIBH0MnEalUxkSrjHPdIw68tV1rurrfiVoUF7ZWkVr9Ar97audrytHoFqf4kXn20SEA0jyUXSNgxjauj2jit88TEc3OFPy5/JKM5l8GRvBSc9/K4VzE6Xr7x+dX6rE/PlXBwJocIkYfzBDQ45aqA3d6PquOc8fJlvyySsT5bQKYi4hsPhxPFqTiUz+N+uenR+j2u/p1UX6PVx2h14wwegelCm3/6ew6q7MpZLx8+5xVgt8gYnMSizJ4GmykVFonFyUIe7atG4e7Kp9WtpLqlgEM4l0XULWCXS95TOXPcQKp7lp9K2JrGQiNGciKSDAzeTeIwaDiDAUMYfKHyuL5Yxq9LjLi4QMZxj4B9erWbQ9Al3NnpMhZSTfdcXSh+WJSlEDGL5BQWIwwsjCIRLDDh/gYrzhTz+K5E3xC9miEjERBwSYdrc03d73pnrFarQ5RSYUhmHl3w9tAU+EvI7CNZ5AOWge/J+Pa7GTJvDgEn/7fflV5Kj/aMqqp9ZFn6geNFsCyPISNZ9H8nGdNsEvk0TMaDLRk4XcShKZ9siEs8VeM0ifToi0Eu6GUwGBSGYcYszeI2Bt0SgsUKIkvM+KsqEzfI1pyYLaDembra5/P1psf+PW0LhVk3SuUff1uWjivzJZydw59vnq1Y6d//DdXmQX1bPUL6hTmS4vOZX736DSUh4R8bWGLj8NIjKAAAAABJRU5ErkJggg=="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def get_max_curve(self, curves):
                leng_list = [_.GetLength() for _ in curves]
                zip_list_curve = zip(leng_list, curves)
                max_curve = sorted(zip_list_curve)[-1][1]
                return max_curve

            def RunScript(self, Pipe_Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    Center_Curve = gd[object]()
                    tol = sc.doc.ModelAbsoluteTolerance
                    re_mes = Message.RE_MES([j_bool_f1], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if Pipe_Brep:
                            curve_list = rg.Curve.JoinCurves(Pipe_Brep.DuplicateEdgeCurves(False))
                            # 区分圆线、其他线
                            circle_list = [_ for _ in curve_list if _.IsCircle() is True]
                            other_list = [_ for _ in curve_list if _ not in circle_list]
                            # 获取其他线中，最长的边线
                            if other_list:
                                pipe_edge = self.get_max_curve(other_list)
                            else:
                                pipe_edge = self.get_max_curve(circle_list)
                            # 基础线和最长边线相交的点
                            max_pt = circle_list[0].ClosestPoints(pipe_edge)[1]
                            # 基础圆线，平面，基础偏移法向
                            base_circle = circle_list[0].TryGetCircle()[1]
                            base_plane = base_circle.Plane
                            base_pt = base_circle.Center
                            normal = base_plane.YAxis
                            # 两线点之间的距离
                            distance = max_pt.DistanceTo(base_pt)
                            # 边线偏移
                            Center_Curve = pipe_edge.Offset(base_pt, normal, distance, tol, rg.CurveOffsetCornerStyle.Sharp)[0]
                        else:
                            Center_Curve = None

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Center_Curve
                finally:
                    self.Message = 'Pipe Round pipe'


        # 布尔分割,不同于Brep剪;对于圆孔切割速率更快
        class BrepBoolSplit(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepBoolSplit", "R41", """Boolean partition,Different from Brep scissors;For round holes the cutting rate is faster""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3bb1425b-b637-434f-b345-fc304fc79c01")

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
                self.SetUpParam(p, "A_Brep", "A", "A set Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "B set Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Brep", "R", "Brep set obtained by Boolean segmentation")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANXSURBVEhLrVVtSFNhFH7v3e7m2JxzN92HX9k2U2eIZFJmFn79CKSwAg0SzDKh0ljmhGr2sbQsxfphYMaQQIqCCAoqqB9iIn1YhEKhUqFSkKCU5Q+z03nvnbbGmpv4wMO973nP1z3vueclywADIZwVn0ZxuXwo5ZVcb55ZNV2SqoF8i+pHhErWh/K94vaSsZYjhLlt26CF0WNmgIYkgPPJwnO81gz2LC0Qwt4jJFrhNggWjOvqVh1AsxXAic7rV/+lM1GQu7bpMQhz020QFDJ3WdUAFzHjUx6OPUnll6xQmhqGQUiuaBYgGEZyrbc8FqARA/hyPs/GJOiviAOJRNLlNg0I8kgVNyo4OIul8HbqydOJMHPcAvHakAG3bUBgFVLmUUtBhHioNIjDh3N3gDlHAlh1ihG37aIwI03iK6nbvUb9+zt1jqXwGQSDf6kxQZiC63bb+IdWzbwtzJb/MsVI3uCyFmlLN8jHBw+vAmjyOg8aEA+5o5B2ErFT+0WxUs++gtd6+PlCD3dbwyHNIn2P4mo+hO27UxyFXYUti2URnGP5JuosEKeRfUUdreDAB3gkI77i6XLk/tgDrP2gAWDECJM9OkgxScdwy4LscmxZIZarxQrDNhOsMypmUV5Abb2RreDYx3kW5ZSMZXpwHS2KSY3LEQYwhtk+1wMMGaG3g6cl6BS3ibM4JRTsm3ngFdJ+XGeL4n/AVuTGK2GgKl745CdlMRAVKmQpKOt5duhpuxbgnRFgGPk5GnbkhNAg9CsoDiBLkKyw8sKmHHQ+R1tv/ie6kAyfsBOyYhVzuL8PqUHeyMmQTTsPhsJDFw9tdjUwDLlOHfgDq5JLXn6sxo6gdfTsBhxgs2cSoTJdQzO9IqoLB7cdWS+TklsYoFmQ+kFaUTLOF8x4wbknMQDdayvUAccwz1A/2LnP7mnIxQ7x7mdP0gGG59KNc8jCcxOESIIZYmxZU36k/wDzbE2BdvEHqhNtA0MmHa0BBUCdI+vpheKzDf8LeYRSOjJpx9vpnNcF4knssJkTCfQPpa0b9G21c+ErfI1iKsP5cigjnGZfLpoEDaaFtuO3kwnibKFdRYm31xRmXiU4Zy67lZeMSjMv+3A0i4fOIoNA20YeTFoZnev7RZVgQMgfVgA+/8g+gJQAAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def BooleanSplit(self, brep, cut):
                cut_brep = []
                cbrep = rg.Brep.CreateBooleanSplit(brep, cut, self.tol)
                for _brep in cbrep:
                    if _brep is not None:
                        cut_brep.append(_brep)
                return cut_brep

            def RunScript(self, A_Brep, B_Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Brep = gd[object]()
                    self.tol = sc.doc.ModelAbsoluteTolerance
                    # 输入端提示信息
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['A end', 'B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 布尔切割
                        Res_Brep = self.BooleanSplit(A_Brep, B_Brep)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Brep
                finally:
                    self.Message = 'BooleanSplit'


        # 通过编号移动面
        class MoveFaces(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_MoveFaces", "R42", """Move surfaces by numbering""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("2ed39877-2a49-4682-a9d0-04f702eb0758")

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
                self.SetUpParam(p, "Brep", "B", "The solid to be offset")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Offset sequence number")
                p.SetPersistentData(gk.Types.GH_Integer(0))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Vector", "V", "Offset direction (vector)")
                p.SetPersistentData(gk.Types.GH_Number(10))
                # p.SetPersistentData(gk.Types.GH_ObjectWrapper(10))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Both Side", "BS", "Whether both ends are offset")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Solid", "S", "Whether to offset to solid")
                p.SetPersistentData(gk.Types.GH_Boolean(True))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Brep", "B", "Offset result")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP4SURBVEhL1ZV7aFNnGMZzadImaUkbk9SmTZp6kia9pBfbxtZ2sq6bKMpsvZRBwcvc6la6+3CO1U6rtavrHzpxF6SCjlGphcEGwoSOsblN6FDRCiLbyjamG7RTXKG7dc+e95xkZhCluv2zB368nOSc532/93vPd3T/J9li8T/VEjJAzpMr5C2iJ/9KKWQzGSOo91nQv9SNweYcpJsN4G+HyF1rNRnPoNFTdVk411EA9BYBe4uBfaUYWeeRBEKF3HwncpAhgo5oFr55PgC8StO+MLAjBLxMJPYXY21xhiQ4Lg/dShbSQiLqlU5XTb6s9abhfCcrPhABBlg1TWe2M+4q1BIIe4pwscMfX0WJPJyo+vvs9v17vP6JdwJhmI1G6eUa8nNeZgrebvXgg01eHGvNwfG2Ajy2sg4NdbUY3lR+M4msgi1b7LVIgo1iKrqn1en6/vOScsxG64FFDZiursWZSAVOhcvxcagMnzKeVCJ4L78Uo75StIcqkV9ZDX+4DNWVFZjpYqt2xlbB/XhtuVsSnCRGSZDfZLf3dud6z44Ew/hxYRRTVYvwuMuDgZAPByN+vF7qxxvkzUgBjpQV4OmFAbiVEEzZClbXhfD7zoS9YJu+aM8HZ/U3erslQaJqounp+5ZmOLBkgQXfdSmYJFMvKfiJUWW7gunuAN5dX4j+B4P4YStNe2Lmwq4wJrcGYDUZZuiXq9n+UztsVh2mXgyq1aiVyfIlJtJLZIrEvJvQWKYIrxSrCZxW4x/0UjTLm6oheP+hXG225cF4ZcmQ/3tozHu/fVZBb6MLVfMscKWlwKBXJymouibow+VBm1aJVJnMNI6Y9xXhRlchOmscNNPD4dTjkTYLohGTmJ8gZtU1psUEZ7hB8mBS0zhiziLkTfZYTMhy6DDYY8evY/OByTx0rrNKgkHVNUFD9y+wzs2cfR7b4oeBVS9rMOP6Z9nAVx7gMrmSh/Zm9T04qtlqmkduDK/lDdKeZMZxdnOUXwjCqjdgVWMqcDFHMx7PwYkDWWhbYYEzUz30RlTnmJ50WY24vo2TI5uWzDgOC1jmT4fPa8DsWc382ifZaGlME9NZIsZbSCX5W8Nhp1k7GW+XgGN7+mGfGOHUIQfwdS6mT89HTZG6qRdIlZgl06MEfU0uHmQlt07C6luUDJSXGIFLWs+f0DZ0gjjF6HZaQSY7eRz/IiO6l4nYb/UFEri6P5kkTWfAUJ8dmPbi2mg2TCnqvDerDnNQgIxG3Kk4ssaDiWcUXOXZf/U5Ru7PRxu8anu2bbTh4O5MbF6lTssUka/cHamdXDAZ9bDx62UzEcZUXvN3YZyci3GY3JXkqG0iD5BGcm+MejLHD7tO9xfgHMCygH1VfwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.cap = True
                self.brep_faces = None

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
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def recopy_geo(self, geo, xform):
                # 按向量偏移并获取新面
                copy_nurf = copy.copy(geo)
                copy_nurf.Translate(xform)
                return copy_nurf

            def isnotparallel(self, curve_tuple):
                # 检测线之间是否平行
                parallel_list = []
                poly_curve, b_curve_list = curve_tuple
                a_curve_list = list(poly_curve.DuplicateSegments())
                for b_cur in b_curve_list:
                    b_vector = b_cur.PointAtEnd - b_cur.PointAtStart
                    for a_cur in a_curve_list:
                        a_vector = a_cur.PointAtEnd - a_cur.PointAtStart
                        radian_num = int(math.degrees(rg.Vector3d.VectorAngle(a_vector, b_vector)))
                        if radian_num == 0:
                            parallel_list.append((a_cur, b_cur))
                return parallel_list

            def loft_brep(self, brep_list):
                opt = rg.LoftType.Normal
                loft_brep = None
                # 判空
                if brep_list:
                    brep_set = brep_list[0]
                    loft_brep = ghc.Loft(brep_set, ghc.LoftOptions(False, False, 0, 0, opt))
                return loft_brep

            def curvesufaceintersection(self, curve, face_list):
                # 将BrepFace列表分割为两部分，相交部分、未相交部分
                a_part, b_part, a_index_list, b_index_list = ([] for _ in range(4))
                for index, face in enumerate(face_list):
                    if rg.Intersect.Intersection.CurveBrepFace(curve, face, self.tol)[1]:
                        a_index_list.append(index)
                        a_part.append(face)
                    else:
                        b_index_list.append(index)
                        b_part.append(face)
                # BrepFace列表相交部分取出未相交线
                no_inter_edge = []
                for single_face in a_part:
                    edge_list = [_ for _ in single_face.Loops[0].To3dCurve().DuplicateSegments()]
                    sub_edge = []
                    for edge_index, edge in enumerate(edge_list):
                        pt0, pt1 = curve.ClosestPoints(edge)[1:]
                        dis = pt0.DistanceTo(pt1)
                        if int(dis) != 0:
                            sub_edge.append(edge)
                    no_inter_edge.append(sub_edge)
                # 将未BrepFace列表转为未相交Brep
                new_b_part = map(lambda b: rg.Brep.CreatePlanarBreps(b.Loops[0].To3dCurve())[0], b_part)
                return no_inter_edge, new_b_part, b_index_list, a_index_list

            def untrim_face(self, face_list, face_len):
                # 重组消线
                sub_res_brep, new_faces, a_part_merge, b_part_merge = ([] for _ in range(4))
                merge_faces = face_list[face_len:]
                origin_faces = face_list[:face_len]
                # 检测面是否平行
                for face in merge_faces:
                    normal = face.FrameAt(0.5, 0.5)[1].ZAxis
                    sub_face_list = [face]
                    for _index, _ in enumerate(origin_faces):
                        o_normal = _.FrameAt(0.5, 0.5)[1].ZAxis
                        angle = math.degrees(rg.Vector3d.VectorAngle(normal, o_normal))
                        if int(angle) == 0:
                            b_part_merge.append(_index)
                            sub_face_list.append(_)
                    sub_res_brep.append(sub_face_list)

                # 组合
                must_meger_brep = map(lambda single_brep: rg.Brep.CreateBooleanUnion([rg.Brep.CreatePlanarBreps(_.Loops[0].To3dCurve())[0] for _ in single_brep], self.tol)[0], sub_res_brep)
                # 单一面消除结构线
                for index, item in enumerate(origin_faces):
                    if index in b_part_merge:
                        must_meger_brep[0].MergeCoplanarFaces(self.tol)
                        origin_faces[index] = must_meger_brep[0]
                        must_meger_brep.pop(0)
                    else:
                        new_sub_brep = rg.Brep.CreatePlanarBreps(item.Loops[0].To3dCurve())[0]
                        new_sub_brep.MergeCoplanarFaces(self.tol)
                        origin_faces[index] = new_sub_brep
                # 重组
                join_brep = rg.Brep.JoinBreps(origin_faces, self.tol)[0]
                temp_brep = ghc.CapHoles(join_brep)
                if temp_brep:
                    cap_brep = temp_brep
                else:
                    cap_brep = join_brep
                return cap_brep

            def move_face(self, origin_brep, index, dir_list):
                # 获取需要的面下标以及方向
                need_index = index[0]
                need_dir = dir_list[0]
                brep_faces = [_ for _ in origin_brep.Faces]
                orinig_face_len = len(brep_faces)
                need_face = brep_faces[need_index]
                # 获取不需要的实体面
                no_need_faces = [brep_faces[_] for _ in range(len(brep_faces)) if _ != need_index]
                # 若为字符和整型则转为向量
                if not isinstance(need_dir, rg.Vector3d):
                    x_vector = need_face.FrameAt(0.5, 0.5)[1].ZAxis * int(need_dir)
                else:
                    x_vector = need_dir
                # 获取将要移动面的边线
                need_curve = need_face.Loops[0].To3dCurve()
                new_curve = self.recopy_geo(need_curve, x_vector)
                new_move_breps = list(rg.Brep.CreatePlanarBreps(new_curve, self.tol))
                # 检测不需要的面与线的相交关系
                no_intersect_edge, no_intersect_brep, no_inter_index, inter_index = self.curvesufaceintersection(need_curve, no_need_faces)
                # 未相交线与面的平行关系
                parallel_zip_list = zip([new_curve] * len(no_intersect_edge), no_intersect_edge)
                parallel_curves = map(self.isnotparallel, parallel_zip_list)
                # 放样实体
                loft_breps = map(self.loft_brep, parallel_curves)
                res_loft_breps = []
                for loft_index, loft_brep in enumerate(loft_breps):
                    if not loft_brep:
                        origin_single_brep = rg.Brep.CreatePlanarBreps(brep_faces[inter_index[loft_index]].Loops[0].To3dCurve(), self.tol)[0]
                        res_loft_breps.append(origin_single_brep)
                    else:
                        res_loft_breps.append(loft_brep)
                # 排序面
                origin_sort_list = zip([need_index], new_move_breps) + zip(no_inter_index, no_intersect_brep) + zip(inter_index, res_loft_breps)
                origin_brep_list = [_[1] for _ in sorted(origin_sort_list)]
                add_breps = origin_brep_list
                # 组合封盖以及封面
                join_brep = rg.Brep.JoinBreps(add_breps, self.tol)[0]
                temp_brep = ghc.CapHolesEx(join_brep)['brep']
                if temp_brep:
                    cap_brep = temp_brep
                else:
                    cap_brep = join_brep
                # 削面
                res_brep = self.untrim_face([_ for _ in cap_brep.Faces], orinig_face_len)
                index.pop(0)
                dir_list.pop(0)
                if index:
                    return self.move_face(res_brep, index, dir_list)
                else:
                    if res_brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                        res_brep.Filp()
                    return res_brep

            def single_face(self, single_face, index, vector, both, solid):
                origin_face = single_face.Faces[0]
                # 若为字符和整型则转为向量
                if not isinstance(vector, rg.Vector3d):
                    x_vector = origin_face.FrameAt(0.5, 0.5)[1].ZAxis * int(vector)
                else:
                    x_vector = vector
                # 判断单面是否需要组成实体
                if solid:
                    # 获取将要移动面的边线
                    need_curve = origin_face.Loops[0].To3dCurve()
                    if both:
                        new_curve_1 = self.recopy_geo(need_curve, x_vector)
                        new_curve_2 = self.recopy_geo(need_curve, x_vector * -1)
                        result_curves = [new_curve_1, new_curve_2]
                    else:
                        new_curve = self.recopy_geo(need_curve, x_vector)
                        result_curves = [need_curve, new_curve]
                    # R11成面
                    res_brep = SectionBody()._do_main((result_curves, [0]))[0][0][0]
                else:
                    # 仅获取移动后的实体
                    if both:
                        brep_1 = self.recopy_geo(origin_face.ToBrep(), x_vector)
                        brep_2 = self.recopy_geo(origin_face.ToBrep(), x_vector * -1)
                        res_brep = [brep_1, brep_2]
                    else:
                        res_brep = self.recopy_geo(origin_face.ToBrep(), x_vector)
                return res_brep

            def RunScript(self, Brep, Index, Vector, Both, Solid):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Brep = gd[object]()

                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    self.tol = sc.doc.ModelAbsoluteTolerance
                    # 输入端判空
                    re_mes = Message.RE_MES([j_bool_f1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        Unrendered_entity = None
                    else:
                        if Brep:
                            face_count = Brep.Faces.Count
                            if face_count == 1:
                                Unrendered_entity = self.single_face(Brep, Index[0], Vector[0], Both, Solid)
                            else:
                                Unrendered_entity = self.move_face(Brep, Index, Vector)
                        else:
                            Unrendered_entity = None
                        Res_Brep = Unrendered_entity
                    # 未渲染实体
                    self.origin_brep = Unrendered_entity
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Brep
                finally:
                    self.Message = 'solid are offset by serial number'

            def DrawViewportWires(self, args):
                try:
                    def Rendering_Brep(un_brep):
                        faces = [_ for _ in self.origin_brep.Faces]
                        for index_f, face in enumerate(faces):
                            if face:
                                center_pt = face.GetBoundingBox(True).Center
                                args.Display.DrawDot(center_pt, str(index_f))
                            args.Display.DrawBrepWires(un_brep, System.Drawing.Color.FromArgb(0, 150, 0))

                    if self.origin_brep:
                        if type(self.origin_brep) is not list:
                            brep_list = [self.origin_brep]
                        else:
                            brep_list = self.origin_brep
                        map(Rendering_Brep, brep_list)
                except:
                    pass


    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def __init__(self):
        icon_text = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAT+SURBVEhLrVVrTJtVGD7hWnTCkPa79ELblQKVbmEKShYNYW6LOEyAjrG1fJe2XwtlM1smDEWzEv3jEhNDzOKYiMv0j+yHiy4maoz+MLIsDtkyFcZFiAMMUIFSbkM4vqe0CB+IMbHJk/d857zned7b9xWRnx/jmP8TQBiD/YWKH7zeeDTE63JCPNs7wzG90w5A1G4LehUcwbp9sq5i+mZ5amzGreu8Lxqb0TjH5GFBhTGvxMvcKlZ4VRjy5/WQ+xGLnQAvjYOc+vMet9kyzBveRWMO9vH5KgrPOpR4xv7fEXKowpaQzwv09IRT6yRl73VZSkd5fXtEQIXnQCDqHLVyEmI3nMF6EaLHbhqHBOarHt6suePbnXpPynXfd5lax6rU19YESAbrL8tFtgIW4Z5ALwVE/RkS9aAna1+PJ7cu4NJ/+KebWph0UN+GBRY4akMGBNsJzFeRqCkc4pkbv7oy9n5TW7hjwG2qHHKam0JO9iYRxi4VDlQxX6wJbNUDuWAQLBmIRYHB05ymiUTd0tISf8+T44PaXwSeSSys+pOeBBzMlxtKFCVbI7X/LUAyDEctsN2/Oc1PtVdUxP7i3fNCtye3GOr/NYl6ETIjQRD/fxQgkYYiTgTkQngEgWBa0Lzj9/sTur2Z2X1ui2/UabgwJ9BBchb1j2KTwBwpR0RkKTzTVNiJYFZkhiZE40FSkh7JWjbg2lUf5NXXl6FcSzBF0aijIJnLBFZ7QEZuimMHR1wZNb+LRvsMz7RPitrrpIn93sfSe6qtJ0dFw1sLHN2PnUo8GyWU9YrYTQLRKQoSISf1xzCva/D7T+286Ss4MMSb+QFXZsOUU3ttEZq4DBnKo5Zjk0AIiBci4xfkqRujLuPhzpN5xbdqn362T9p9PMizPeGoI2UkWB+5HDKB1SZCw1Zg3M6RWpNfX01u8ZA3p/FTb8lDkxzbsQI1J5flxFuWSFRGBDj1XvKqz4rs3UHRtC/CjcYE3dUHAr2MJQYPStklAV730VbTIscmgXF7WhE08soHfkFBiMcFXU1Q1H02ZVeFsAcmhKMGb9UWZAQ5ZuQBlFBOGIU8q7USjVfR+ydE9RVCPsybX8ESjbFE4Xlo5BxMUFdNnnVK0F4mY7ue4N+wlsGswD6BaxmoP9sfcJna5iWDd1HSeOYlvRj0GKrhE3wb+0AUvi3YBe/Gtja6BtRQ8Dmhv0MfH9Jm9B7TtswJmgu9lWxbp033xvel6vqOMs35Thvzyc9H2KtdpUzbHRvTerecfm/Ern57WdK8fruceZ/sdVewF38qZy51lTNtP5bRl1ef6UsDx9StHTZNA9rxKFWG4lU8KRFSqM7GUcZXEUo4DU92hOgnUYrxCKwdABeKSz2DUtK9sLYCDiMUQ/5cyBnZK0bokQKEKACqBgDnwy+i9PR0m0qlqoONyrS0tLrMzMzmlNQU8qU8q1AozlksluLk5GRfQkJCvdFobFSr1c2xsbGH4HwnoDEuLu40+EFQqB5sHXD4YmJiXgb4KYo6j2iaLklNTa0HhwSwXq1W+1pSUtIpIClTKpWFer3+TfA5CmfpYJsgGCecQfSIAxIfWDfYE7BXBALPJCYmkmyq4fmARqOxoby8vF0QmWQymTwQ/XOQ0X6IssRsNlsAZfn5+RI47gEUGQyGQjh7CcQq4c4JgA18RLB2q9X6PKyPZ2Vl1UFQPuA7mp2dXfIXO8FFxSea9bcAAAAASUVORK5CYII="
        icon = System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(icon_text)))
        Grasshopper.Instances.ComponentServer.AddCategoryIcon("Scavenger", icon)
        Grasshopper.Instances.ComponentServer.AddCategoryShortName('Scavenger', 'Save')
        # Grasshopper.Instances.CanvasCreated += self._set_tool_botton

    def _set_tool_botton(self):
        Grasshopper.Instances.CanvasCreated -= self._set_tool_botton
        _toolbar = Grasshopper.Instances.DocumentEditor.Controls[0].Controls[1]
        list_botton = []
        _toolbar.toolbar.Items.Add("弹窗测试 \n by HAE-smbl47")
        for _ in _toolbar.Items:
            if 'HAE' in str(_):
                list_botton.append(_)
        list_botton[-1].Image = self.get_Internal_Icon_24x24()
        list_botton[-1].DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
        list_botton[-1].Click += System.EventHandler(self.print_message)
        return

    def print_message(self, sender, none_e):
        rs.MessageBox('工具栏测试', 0 | 48)

    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANFSURBVEhLrZZbSFRBHMbX1ArNMoow6KF7dNGnioKCCISk6OpW2upWWmbJJiIm0RXKjiZabRBEYRGVhlZ2h/KptKiQ6kV7KO2e0W3PzHr24u7Xf2bXctuzweYe+F7Ozvy+//znm9ljsO1emOYpTVFslumRVcEUxZM3SjHwwmQrLMOBvMQIiVg58UBWDHAuBwZWmKxgcyK4eVj/tZ44GQPBjDHQ7p2GeCJnIOCrB0DNSoTj6U0JR3NNhAwEfKUBLH88nJ3P4SW2/c4JoLY4MgZsuQHqzrlw/+yC1+0Ca1CgXq0Eyhb20yA7AWwZVV5pRI/Xi57vn8Bq94E3VoJtnwaYov7XgMab4qBS5fxMsWy3m1qjXtwNVn8QLDcJfE20TFT4Bv6kqMYB6L5llXDniyaoovLzO8HWxYNnDpLjBDc8gz5J0Z5cl3C37QvsLx+CHc0CN0bTysjAPz48g96kbBkHZ8czCbfftILdPQV+xAS+gtqVnRAwJywDkRRWOoeS8hneHjfY5UNgjVXgu+aBCbjOnGADUaVY4toY6uNgejf0T1IOp8Pj9cDzo0smhV09DF44Azyd4GJeH3Cvgg0EfNsE2A+kgVum0pGPAlslklIkD4/rzQuoF/aAN5RRUkbTflDPQ8CFgg0yBoEVpUBrvQ03+wHtfi3YKYuEO583weZPCjcN+Z2Uv6F9FWwgW0T5XkxVHzND+/oe/HEjZZv6TaeTn9zqT0pcEExP+gbUFr5xFOw3joI11YC31EO9dRzq/lRfv7MDk/IvBRoQnFEM1W2T4Hzti6GzqwPsQR1cLge42Bc6XHqgUAowkDHcNR/ubx8l3PWhHfxsCdS9qXC1t0C7RvdLiDiGkt9guoK1BK/OhMelSbibdtVWOguc9oItMsBOl1f39Wq5Qj1QKEkDW06SgrodMini0R5QcqoywQomUlLozkmPguNVK3j5cnlN6IFCyWdgHqngo6/n3ZfLoS6lKoUo/2wJVX+lAlpbM9ia2LA2WMjXok1jFOydDee7NqjHN4CXzAQvmAy+ZwGt5hIc9J7lj5VnRF7TOqBQkga8KMWKvFggl17QXxzePgXekTofAbcr6E4fAZjpd/G1oPsV8Q9ZhuMXjiPHLIKO5n4AAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def get_AssemblyName(self):
        return "Tradition"

    def get_AssemblyDescription(self):
        return """HAE plug-in"""

    def get_AssemblyVersion(self):
        return "v4.6"

    def get_AuthorName(self):
        return "by HAE Development Team"

    def get_Id(self):
        return System.Guid("86c4ead2-84fa-4dff-a70f-099478c2ccca")

    def get_AuthorContact(self):
        return "smblscr47@163.com"
