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
import webbrowser as wb
from System.Collections.Generic import List
from Grasshopper.Kernel.Data import GH_Path
import Curve_group

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
                Tolerance = sc.doc.ModelAbsoluteTolerance
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
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def tr_object(self, origin_brep, transform):
                wxy_origin_breps = []
                for _ in origin_brep:
                    _.Transform(transform)
                    wxy_origin_breps.append(_)
                return wxy_origin_breps

            def _first_handle(self, passive_brep, cut_brep):
                """群组切割方法"""
                # 获取映射平面
                pl = rg.Plane.WorldXY
                brep_center = passive_brep.GetBoundingBox(False).Center
                brep_pl = rg.Plane.WorldXY
                brep_pl.Origin = brep_center
                center_tr_one = rg.Transform.PlaneToPlane(brep_pl, pl)
                center_tr_two = rg.Transform.PlaneToPlane(pl, brep_pl)
                # 映射被切割体
                # passive_brep.Transform(center_tr_one)
                # 映射切割体
                # new_cut_brep = self.tr_object(cut_brep, center_tr_one)
                new_cut_brep = cut_brep
                # 群组切割
                res_temp_brep = rg.Brep.CreateBooleanDifference([passive_brep], new_cut_brep, self.tol)
                #
                # 判断是否切割成功
                res_temp_brep = [_ for _ in res_temp_brep] if res_temp_brep else None
                if res_temp_brep:
                    # 切割成功，获取最大的一个Brep并映射回原位置
                    area = [_.GetArea() for _ in res_temp_brep]
                    max_index = area.index(max(area))
                    res_temp_brep = res_temp_brep[max_index]
                    # res_temp_brep.Transform(center_tr_two)
                else:
                    # # 若切割失败，返回原Brep
                    # passive_brep.Transform(center_tr_two)
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
                            interse_sets = rg.Intersect.Intersection.BrepBrep(bumped_brep, coll_brep[count], sc.doc.ModelAbsoluteTolerance)
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
                # 解包数据
                a_set, b_set, origin_path = temp_data
                # 复制b集合数据列表
                new_b_set = [b_set[::] for _ in range(len(a_set))]

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

                    j_bool_f1, a_trunk_brep, a_brep_path = self.parameter_judgment(A_Brep)
                    j_bool_f2, b_trunk_brep, b_brep_path = self.parameter_judgment(B_Brep)

                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['A end', 'B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 树形长度匹配
                        _a_tr_len, _b_tr_len = len(a_trunk_brep), len(b_trunk_brep)
                        if _a_tr_len > _b_tr_len:
                            new_a_trunk = a_trunk_brep
                            new_b_trunk = b_trunk_brep + [b_trunk_brep[-1]] * (_a_tr_len - _b_tr_len)
                            new_trunk_path = a_brep_path
                        elif _b_tr_len < _a_tr_len:
                            new_a_trunk = a_trunk_brep + [a_trunk_brep[-1]] * (_b_tr_len - _a_tr_len)
                            new_b_trunk = b_trunk_brep
                            new_trunk_path = b_brep_path
                        else:
                            new_a_trunk = a_trunk_brep
                            new_b_trunk = b_trunk_brep
                            new_trunk_path = a_brep_path
                        # 构筑打包数据运行多进程
                        zip_list = zip(new_a_trunk, new_b_trunk, new_trunk_path)
                        temp_iter_ungroup, dis_tips = zip(*ghp.run(self.tree_match, zip_list))
                        iter_ungroup_data = zip(*temp_iter_ungroup)
                        _res_breps = zip(*iter_ungroup_data[0])[0]

                        # 检索切割与被切割未相交个体
                        for f_disjoint_index in range(len(dis_tips)):
                            for s_disjoint_index in dis_tips[f_disjoint_index][0]:
                                Message.message2(self, "the order of data is {}：the cutting object which subscript is{} is not intersecting！".format((f_disjoint_index + 1), s_disjoint_index))

                        # 检索切割失败个体
                        for _f_res_index in range(len(_res_breps)):
                            if not _res_breps[_f_res_index]:
                                Message.message1(self, "the data which order is {} failed to be cut：please use RPP-Brep cut （high accuracy）plug-in to look for it！".format(_f_res_index + 1))
                        Res_Breps, Disjoint = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "cutting object（flat plane（Plane）or smooth surface（Surface））")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "cutting accuracy")
                p.SetPersistentData(gk.Types.GH_Number(0.001))
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Flat cut Brep（surface）'
                # 初始化输出端数据内容
                Result_Brep = gd[object]()
                if self.RunCount == 1:
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData
                    p3 = self.Params.Input[3].VolatileData
                    # 确定不变全局参数
                    self.tol = float(p2[0][0].Value)
                    self.cap_factor = p3[0][0].Value

                    j_bool_f1, brep_trunk, brep_path = self.parameter_judgment(p0)
                    j_bool_f2, pln_trunk, pln_path = self.parameter_judgment(p1)

                    re_mes = Message.RE_MES([j_bool_f1, j_bool_f2], ['B end', 'P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        brep_trunk = list(ghp.run(lambda x: map(self._trun_object, x), brep_trunk))
                        pln_trunk = list(ghp.run(lambda y: map(self._trun_object, y), pln_trunk))

                        len_b, len_p = len(brep_trunk), len(pln_trunk)
                        if len_b != len_p:
                            new_brep_list = brep_trunk
                            new_plane_list = pln_trunk + [pln_trunk[-1]] * abs(len_b - len_p)
                            new_plane_list = ghp.run(lambda li: [copy.copy(_) for _ in li[:]], new_plane_list)
                        else:
                            new_brep_list = brep_trunk
                            new_plane_list = pln_trunk

                        zip_list = zip(new_brep_list, new_plane_list, brep_path)
                        trunk_list_res_brep = list(ghp.run(self.temp, zip_list))
                        Result_Brep = self.format_tree(trunk_list_res_brep)
                DA.SetDataTree(0, Result_Brep)

                # p0 = self.marshal.GetInput(DA, 0)
                # p1 = self.marshal.GetInput(DA, 1)
                # p2 = self.marshal.GetInput(DA, 2)
                # p3 = self.marshal.GetInput(DA, 3)
                # result = self.RunScript(p0, p1, p2, p3)
                #
                # if result is not None:
                #     self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALbSURBVEhLtVRbSJNhGJ5jbUpuQs6YJ7owa7MkzVKkdM3JLMxR0IFiTjNtc5uZWHohUfrPdvCURd7UjRdhaGloWlJdeO3oQGBQQt1EFOVNWoEXT+/3b8Hcr2nDPfDA++/9/ufZ9x5+0f+isMR3Qmd4sSvwuP7QHno5qi+dqQg8hoVoomol5uqmhtNyBuuWywUYR1wRJZtixB+zk6Lns1UyIRM3zOfneRb3Zhz9zWJBnt5LUUi+kg77A0JIxVG+6ZotgEsDtKqFbE+G03QDTx3VFKcI804N5prTkaqQ/CQ54U0UUvGbueatdJAOX90upDOJN5i011BMBqH5VnZGg5xE2S+SS/KrBkEuFb/63JgGcGRwhQ6HkmMGvXhsIwOODELzvIkarFwkx/qxFGs1mLBZImfQbrqO8cga9GAskgbXmEGtNTwD2jDfQnMC4E7mxQR0x6KrwoNnjjMUy4V5mjI2vlnxoh8kJ+NFtQbfYb3xfV9hyXRfZhb3jTvlQlelF51mLzrMHfASPeWdxC64zW6cPjIO27EBuCjPbsN64uTZC45GuM10E/l53sV9xVMjxWWz90Tag779euPspULDdGP6NsunO5X1GKy9gCFLPR5YzmPYWocRqwMPrXaM2qtgOz7Ai43RLR5RqVjDJ2zn+NF9Yq/GJC1hLm16bsGwo6jsnYm/xV+wEs03baZNpvpyrEwhdMnRbfbQop2lOI5+Y+eCyJavPRVZSr5EMX7VIKylyaxU7Da8YWh+PaaI9YOVLGIGXjJgfYmYAZss1vywDOhr+vrLxdUMvLj/L4M2NXarZAskl+hXDUKMJGrmexN9rnt2At4MIXuScauqAxN1DUB3qjDfuYOmKwMapXSR5BL8qktx2ZC2ES06JVoK4oXUxuJkcSsqi2oolgvzB5QwZSogjhINkZbYLymEnli+EtP39D9XqT13l8sFaCRKiOFBV/r2tt74oSHwuApEoj89Q3ZdEGG9MgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None
                self.cap_factor = None

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

            def cap_brep(self, cap_brep):
                brep_list = []
                for _ in cap_brep:
                    new_cap_brep = _.CapPlanarHoles(self.tol)
                    if not new_cap_brep or self.cap_factor is False:
                        brep_list.append(_)
                    else:
                        brep_list.append(new_cap_brep)
                return brep_list

            def sort_by_xyz(self, follow_objects, pln):
                pt_list = [_.GetBoundingBox(True).Center for _ in follow_objects]
                # 获取转换过程
                xform = rg.Transform.PlaneToPlane(pln, rg.Plane.WorldXY)
                # 映射点
                dict_pt_data = dict()
                copy_pt = [rg.Point3d(_) for _ in pt_list]
                [_.Transform(xform) for _ in copy_pt]
                dict_pt_data['X'] = [round(_.X, 1) for _ in copy_pt]
                dict_pt_data['Y'] = [round(_.Y, 1) for _ in copy_pt]
                dict_pt_data['Z'] = [round(_.Z, 1) for _ in copy_pt]

                # 点按Z方向排序
                zip_list = zip(dict_pt_data['Z'], dict_pt_data['X'], dict_pt_data['Y'])
                w_sort_pts = []
                for index in range(len(zip_list)):
                    w_sort_pts.append(list(zip_list[index]) + [index])
                # 获取下标
                index_list = [_[-1] for _ in sorted(w_sort_pts)]
                # 下标映射
                new_object_list = [follow_objects[_] for _ in index_list]
                return new_object_list

            def _recursive_cutting(self, ent, cut_list, new_brep_list):
                cut = cut_list[0]
                ent = ent if type(ent) is list else [ent]
                for en in ent:
                    temp_brep = list(en.Split.Overloads[IEnumerable[Rhino.Geometry.Brep], System.Double]([cut], self.tol))

                    if len(temp_brep):
                        cap_brep = self.cap_brep(temp_brep) if self.cap_factor else temp_brep
                        new_brep_list.append(cap_brep)
                    else:
                        new_brep_list.append([en])
                temp_list_brep = list(chain(*new_brep_list))

                cut_list.remove(cut)
                if cut_list:
                    return self._recursive_cutting(temp_list_brep, cut_list, [])
                else:
                    res_list_brep = self._handle_brep(temp_list_brep)
                    # res_list_brep = [_ for _ in res_list_brep if _.IsSolid]
                    return res_list_brep

            def get_box_surface(self, geo_list, pln):
                # 获取最小边界框
                pt_list = []
                for geo in geo_list:
                    pt_list += [_.Location for _ in geo.Vertices]
                total_box = rg.Box(pln, pt_list)  # 最小包围盒
                total_bbox = total_box.BoundingBox  # 最小边界框

                # 获取最大面
                def get_max_face(face_list):
                    face_list = face_list if type(face_list) is list else [face_list]
                    area_list = [_.GetArea() for _ in face_list]
                    max_index = area_list.index(max(area_list))
                    bounding_face = [face_list[max_index]]
                    return bounding_face

                # 如果最小边界框体积为0
                if int(total_bbox.Volume) == 0:
                    bbox_sur_list = ghc.DeconstructBrep(total_bbox)['faces']
                    # if bbox_sur_list:
                    #     get_max_face(bbox_sur_list)
                    #     # bbox_sur_list = bbox_sur_list if type(bbox_sur_list) is list else [bbox_sur_list]
                    #     # area_list = [_.GetArea() for _ in bbox_sur_list]
                    #     # max_index = area_list.index(max(area_list))
                    #     # bounding_face = [bbox_sur_list[max_index]]
                    # else:
                    #     bounding_face = [_ for _ in geo_list]
                else:
                    bbox_sur_list = ghc.DeconstructBrep(total_box.ToBrep())['faces']

                # 炸开之后获得获得最大面
                if bbox_sur_list:
                    bounding_face = get_max_face(bbox_sur_list)
                else:
                    bounding_face = [_ for _ in geo_list]

                    # if bbox_sur_list:
                    #     get_max_face(bbox_sur_list)
                    # bbox_sur_list = bbox_sur_list if type(bbox_sur_list) is list else [bbox_sur_list]
                    # area_list = [_.GetArea() for _ in bbox_sur_list]
                    # max_index = area_list.index(max(area_list))
                    # bounding_face = [bbox_sur_list[max_index]]
                    # else:
                    #     bounding_face = [_ for _ in geo_list]

                # 将面列表所有边都延申100
                res_cut_brep = []
                for surf in bounding_face:
                    surf = surf.Faces[0].ToNurbsSurface()
                    surf = surf.Extend(rg.IsoStatus.East, 100, True)
                    surf = surf.Extend(rg.IsoStatus.North, 100, True)
                    surf = surf.Extend(rg.IsoStatus.South, 100, True)
                    surf = surf.Extend(rg.IsoStatus.West, 100, True)
                    res_cut_brep.append(surf)
                return res_cut_brep

            def _get_intersect(self, item, pln):
                pln = filter(None, pln)
                if pln:
                    new_pln = pln
                    cutts = []

                    for pl in new_pln:
                        single_event = rg.Intersect.Intersection.BrepPlane(item, pl, self.tol)
                        # 是否切到实体，未切到则不加入切割列表
                        if single_event[0]:
                            curves = list(rg.Curve.JoinCurves(single_event[1], 0.1))
                            array_c = list(chain(*[list(_.DuplicateSegments()) for _ in curves]))
                            array_c_len = len(array_c)

                            if not array_c_len == 4:
                                if curves:
                                    temp_surface_cut = list(rg.Brep.CreatePlanarBreps(curves, 0.1))
                                    # c_len, temp_s_len = len(curves), len(temp_surface_cut)
                                    surface_cut = self.get_box_surface(temp_surface_cut, pl)

                                    temp_surface_Prop = rg.AreaMassProperties.Compute(temp_surface_cut[0])  # 计算面积质量属性
                                    surface_Prop = rg.AreaMassProperties.Compute(surface_cut[0])

                                    if temp_surface_Prop and surface_Prop and temp_surface_Prop.Area > surface_Prop.Area:
                                        surface_cut = temp_surface_cut
                                    cutts += surface_cut
                            else:
                                surface_cut = [ghc.BoundarySurfaces(array_c)]
                                cutts += surface_cut

                    # 若平面全部都没切割到实体，则输出实体
                    if cutts:
                        temp_cutts = ghc.Untrim(cutts)
                        # 输入端口调整为列表
                        res_cutts = temp_cutts if type(temp_cutts) is list else [temp_cutts]
                        res_breps = self._recursive_cutting(item, res_cutts, [])
                        sort_breps = self.sort_by_xyz(res_breps, new_pln[0])
                    else:
                        sort_breps = [item]
                else:
                    sort_breps = [item]

                return sort_breps

            def _handle_brep(self, breps):
                for brep in breps:
                    if brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                        brep.Flip()
                return breps

            def _recursive_cutting_sur(self, sur, cut_list, new_brep_list):
                cut = cut_list[0]
                sur = sur if type(sur) is list else [sur]
                for s in sur:
                    # 面切割取第一个数据
                    temp_brep = list(s.Split.Overloads[IEnumerable[Rhino.Geometry.Brep], System.Double](cut, self.tol))
                    # temp_brep = list(s.Split.Overloads[IEnumerable[Rhino.Geometry.Curve], System.Double](cut, self.tol))

                    if len(temp_brep):
                        # 获取剩余的surf
                        rest_list = temp_brep[1:]
                        # 如果平面线切割组只剩最后一组
                        if len(cut_list) == 1:
                            rest_brep = self.cap_brep(rest_list) if self.cap_factor else rest_list
                        else:
                            rest_brep = rg.Brep.JoinBreps(rest_list, 0.1)[0]
                            rest_brep = self.cap_brep([rest_brep]) if self.cap_factor else [rest_brep]

                        cap_brep = self.cap_brep([temp_brep[0]]) if self.cap_factor else [temp_brep[0]]
                        new_brep_list.append(cap_brep)
                        new_brep_list.append(rest_brep)
                    else:
                        new_brep_list.append([s])
                temp_list_brep = list(chain(*new_brep_list))

                cut_list.pop(0)
                if cut_list:
                    return self._recursive_cutting_sur(temp_list_brep, cut_list, [])
                else:
                    res_list_brep = self._handle_brep(temp_list_brep)
                    return res_list_brep

            def get_single_surf(self, uu_set_data):
                # 获取相交线两边偏移后的面
                crv, pln = uu_set_data
                temp_crv_1 = crv.Offset(pln, 0.1, 0.01, rg.CurveOffsetCornerStyle.Sharp)[0]
                temp_crv_2 = crv.Offset(pln, -0.1, 0.01, rg.CurveOffsetCornerStyle.Sharp)[0]

                crv_1 = temp_crv_1 if temp_crv_1 else crv
                crv_2 = temp_crv_2 if temp_crv_1 else crv
                surface = ghc.Loft([crv_1, crv_2], ghc.LoftOptions(False, False, 0, 0, rg.LoftType.Normal))
                return surface

            def _get_surface(self, surf, pln_list):
                cutts_curve = []
                for pl in pln_list:
                    single_event = rg.Intersect.Intersection.BrepPlane(surf, pl, self.tol)
                    if single_event[0]:
                        temp_cutts = map(lambda x: x if "ToNurbsCurve" in dir(x) else None, list(single_event[1]))
                        pls = [pl] * len(temp_cutts)
                        single_cutts = map(lambda c: self.get_single_surf(c), zip(temp_cutts, pls))
                    else:
                        single_cutts = [None]
                    cutts_curve += [single_cutts]
                cutts_curve = [filter(None, list(chain(*cutts_curve)))]

                cut_breps = self._recursive_cutting_sur(surf, cutts_curve, [])
                res_breps = self._handle_brep(cut_breps)
                sort_breps = self.sort_by_xyz(res_breps, pln_list[0])
                return sort_breps

            def temp(self, tuple_data):
                breps, planes, origin_path = tuple_data
                # 匹配平面数据
                list_pln = [planes[:] for _ in range(len(breps))]
                res_list = []
                if breps:
                    for brep_index, brep_item in enumerate(breps):
                        if brep_item:
                            brep_list = [_ for _ in brep_item.Faces]
                            if len(brep_list) == 1:
                                # if not brep_item.IsSolid:
                                res_list.append(self._get_surface(brep_item, list_pln[brep_index]))
                            else:
                                if not brep_item.IsSolid:
                                    temp_brep_item = brep_item.CapPlanarHoles(0.01)
                                    if (not temp_brep_item) or (not temp_brep_item.IsSolid):
                                        res_list.append(self._get_surface(brep_item, list_pln[brep_index]))
                                    else:
                                        res_list.append(self._get_intersect(brep_item, list_pln[brep_index]))
                                else:
                                    res_list.append(self._get_intersect(brep_item, list_pln[brep_index]))
                        else:
                            res_list.append([])
                else:
                    res_list.append([])
                ungroup_data = self.split_tree(res_list, origin_path)
                return ungroup_data
            # def RunScript(self, Brep, Plane, Tolerance, Cap):
            #     try:
            #         self.tol = Tolerance
            #         self.cap_factor = Cap
            #         Result_Brep = gd[object]()
            #
            #         j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Brep)
            #         j_list_2, temp_pl_list, pl_path = self.parameter_judgment(Plane)
            #
            #         re_mes = Message.RE_MES([j_list_1, j_list_2], ['B end', 'P end'])
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             len_b, len_p = len(temp_brep_list), len(temp_pl_list)
            #             if len_b != len_p:
            #                 new_brep_list = temp_brep_list
            #                 new_plane_list = temp_pl_list + [temp_pl_list[-1]] * abs(len_b - len_p)
            #                 new_plane_list = ghp.run(lambda li: [copy.copy(_) for _ in li[:]], new_plane_list)
            #             else:
            #                 new_brep_list = temp_brep_list
            #                 new_plane_list = temp_pl_list
            #
            #             zip_list = zip(new_brep_list, new_plane_list, brep_path)
            #             trunk_list_res_brep = ghp.run(self.temp, zip_list)
            #             Result_Brep = self.format_tree(trunk_list_res_brep)
            #
            #         return Result_Brep
            #     finally:
            #         self.Message = 'flat cut Brep（surface）'


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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "HoleCir", "H", "total length of oblong hole")
                # p.SetPersistentData(gk.Types.GH_Number(20))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "CriVec", "CV", "extend direction size")
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

            # 重新定义向量的长度
            def ver_lenght(self, vector, len):
                unit_vector = vector / vector.Length  # 将原向量单位化
                new_vector = unit_vector * len  # 创建新的向量，长度为new_length
                return new_vector

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

            def Vec_line(self, Pln):
                V_Line = rg.Line(Pln.Origin, Pln.ZAxis, 10).ToNurbsCurve()
                Vec_01 = rg.Vector3d(V_Line.PointAtStart - V_Line.PointAtEnd)
                return Vec_01

            def circle(self, Data):
                # 根据面生成圆柱Brep
                Cri_Vec = Data[2] * 2  # 拉伸向量
                Data[0].Translate(-Data[2])
                C_Plane = Data[0]  # 拉伸平面

                circle = rg.Arc(C_Plane, Data[1], math.radians(360)).ToNurbsCurve()  # 圆弧转曲线
                Surface = rg.Surface.CreateExtrusion(circle, Cri_Vec).ToBrep()
                CirBrep = Surface.CapPlanarHoles(0.001)
                if CirBrep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                    CirBrep.Flip()

                if Data[3]:
                    # 创建长圆孔的圆柱体
                    pln = rg.Plane(C_Plane.Origin, C_Plane.YAxis, C_Plane.ZAxis)
                    cir_split = [ci_ for ci_ in circle.Split(self.create_rectangle_from_center(pln, Data[3]), 0.1, 0.1)]
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
                    if HoleCirBrep:
                        if HoleCirBrep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                            HoleCirBrep.Flip()
                    else:
                        Message.message1(self, "长圆孔生成失败")
                        HoleCirBrep = None
                else:
                    HoleCirBrep = None

                return CirBrep, HoleCirBrep

            def RunScript(self, Plane, Radi, HoleCir, CriVec):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    CirBrepList, HoleCirBrepList = (gd[object]() for _ in range(2))

                    re_mes = Message.RE_MES([Plane, Radi], [self.Params.Input[0].NickName, self.Params.Input[1].NickName])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将标量值转换为列表，方便与Plane进行zip
                        Plane, Radi_list, HoleCir = self.match_list(Plane, Radi, HoleCir)
                        if CriVec:
                            CriVec_list = self.data_polishing_list(Plane, CriVec)
                        else:
                            CriVec_list = list(map(self.Vec_line, Plane))
                        if len(HoleCir) == 0:
                            HoleCir = [i_ * 2 for i_ in Radi_list]
                        # 使用ghpythonlib.parallel.run并行计算 这里使用run函数并行计算多个圆柱体的生成
                        Geometry = ghp.run(self.circle, zip(Plane, Radi_list, CriVec_list, HoleCir))
                        # 解包结果
                        CirBrepList, HoleCirBrepList = zip(*Geometry)

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
                # p0 = self.marshal.GetInput(DA, 0)
                # p1 = self.marshal.GetInput(DA, 1)
                # p2 = self.marshal.GetInput(DA, 2)
                # p3 = self.marshal.GetInput(DA, 3)
                # p4 = self.marshal.GetInput(DA, 4)
                # result = self.RunScript(p0, p1, p2, p3, p4)
                #
                # if result is not None:
                #     self.marshal.SetOutput(result, DA, 0, True)

                New_Brep = gd[object]()
                self.Message = 'offset surface'
                if self.RunCount == 1:
                    Brep = self.Params.Input[0].VolatileData
                    Distance = self.Params.Input[1].VolatileData
                    self.cap = self.marshal.GetInput(DA, 4)
                    self.tol = self.marshal.GetInput(DA, 3)
                    self.b_side = self.marshal.GetInput(DA, 2)
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    j_list_1, temp_brep_list, brep_path = self.parameter_judgment(Brep)

                    re_mes = Message.RE_MES([j_list_1], ['Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        New_Brep = self.temp_by_match_tree(Brep, Distance)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                DA.SetDataTree(0, New_Brep)

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
                untrim_brep = brep
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

            def _do_main(self, tuple_data):
                a_part_trunk, b_part_trunk, origin_path = tuple_data
                new_list_data = list(b_part_trunk)
                new_list_data.insert(self.max_index, a_part_trunk)  # 将最长的数据插入到原列表中
                match_brep, match_dis = new_list_data

                GH_brep_list, GH_dis_list = self.match_list(match_brep, match_dis)  # 将数据二次匹配列表里面的数据

                brep_list = [_.Value if _ is not None else _ for _ in GH_brep_list]  # 将引用物体转换为GH内置物体
                dis_list = [_.Value if _ is not None else _ for _ in GH_dis_list]

                zip_list = zip(brep_list, dis_list)
                New_Brep = ghp.run(self._run_main, zip_list)  # 传入获取主方法中

                ungroup_data = self.split_tree(New_Brep, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def temp_by_match_tree(self, *args):
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
                iter_ungroup_data = ghp.run(self._do_main, zip_list)
                temp_data = self.format_tree(iter_ungroup_data)
                return temp_data

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

            def _run_main(self, tuple_data):
                Brep, Distance = tuple_data
                if Brep:
                    New_Brep = self.offset(Brep, Distance)
                else:
                    New_Brep = None
                return New_Brep

            # def RunScript(self, Brep, Distance, Both, Tolerance, Cap):
            #     try:
            #         sc.doc = Rhino.RhinoDoc.ActiveDoc
            #         self.cap = Cap
            #         self.tol = Tolerance
            #         self.b_side = Both
            #         New_Brep = gd[object]()
            #         j_list_1, temp_brep_list, brep_path = self.parameter_judgment(self.Params.Input[0].VolatileData)
            #
            #         re_mes = Message.RE_MES([j_list_1], ['Brep'])
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             if Brep:
            #                 New_Brep = self.offset(Brep, Distance)
            #             else:
            #                 New_Brep = None
            #
            #         sc.doc.Views.Redraw()
            #         ghdoc = GhPython.DocReplacement.GrasshopperDocument()
            #         sc.doc = ghdoc
            #         return New_Brep
            #     finally:
            #         self.Message = 'offset surface'


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
                    # 删除空值
                    temp_brep = filter(None, temp_brep)
                    # 是否将Brep封盖
                    if self.cap:
                        if temp_brep:
                            res_brep = map(self.cap_brep, temp_brep)
                    else:
                        res_brep = temp_brep
                    ungroup_data = self.split_tree(res_brep, origin_path)
                else:
                    ungroup_data = self.split_tree([], origin_path)
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
                            # 切换为实体模式
                            True_Model = map(lambda y: y.ToBrep() if 'ToBrep' in dir(y) else y, True_Model)
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
                            area_to_brep = map(lambda get_area: get_area[0] * get_area[1],
                                               [_.GetSurfaceSize()[1:] for _ in face_list])
                            max_index = 0
                            for _ in range(len(area_to_brep)):
                                if area_to_brep[_] > area_to_brep[max_index]:
                                    max_index = _
                            max_surf = face_list[max_index]
                            sub_surf_list = [_ for _ in face_list if _ is not max_surf]

                            set_data = self._get_grid_lines(max_surf, sub_surf_list)
                            leader_line, Result_Surfs = zip(*set_data)

                            rotation_curve = map(self.temp_fun, set_data)
                            Result_Axis = [rg.Line(_.PointAtStart, _.PointAtEnd) for _ in
                                           map(self.flip_curve, list(zip(leader_line, rotation_curve)))]
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

                if not Curve.IsClosed:  # 判断线是否闭合
                    Line_length = round(rg.Line(Start, End).ToNurbsCurve().GetLength(), 2)  # 根据起始点重构一根直线
                    Curve_length = round(Curve.ToNurbsCurve().GetLength(), 2)
                    Tool = Line_length == Curve_length  # 比较它们的长度
                else:
                    Tool = True
                return Curve if Curvature > 0.01 and Tool else None

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
                    contour_line = base
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
                    Tolerance = Tolerance
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    j_bool_f2 = self.parameter_judgment(self.Params.Input[1].VolatileData)[0]
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
                self.SetUpParam(p, "Pipe Brep", "P", "The center line of the pipe to be extracted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Skillful", "S", "Remove the needless part at both ends of the pipe center line")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Just Max Srf", "M", "Only extract the center line of the largest surface of the pipe")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Total Center Curve", "C1", "Extract the center lines of all surfaces")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Max Center Curve", "C2", "Longest center line")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Pipe Round pipe'
                # 初始化输出端数据内容
                Total_Center_Curve, Max_Center_Curve = [gd[object]() for _ in range(2)]
                if self.RunCount == 1:
                    self.tol = sc.doc.ModelAbsoluteTolerance
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    p2 = self.Params.Input[2].VolatileData

                    self.skill = p1[0][0].Value
                    self.j_max_surf = p2[0][0].Value

                    j_bool_f1, pipe_trunk, pipe_path = self.parameter_judgment(p0)
                    re_mes = Message.RE_MES([j_bool_f1], ['P end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 获取Gh内置数据
                        new_pipe_trunk = ghp.run(lambda x: map(self._trun_object, x), pipe_trunk)
                        # zip打包数据
                        zip_list = zip(new_pipe_trunk, pipe_path)
                        # 多进程函数运行
                        iter_ungroup_data = zip(*ghp.run(self._do_main, zip_list))
                        Total_Center_Curve, Max_Center_Curve = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                DA.SetDataTree(0, Total_Center_Curve)
                DA.SetDataTree(1, Max_Center_Curve)
                # p0 = self.marshal.GetInput(DA, 0)
                # result = self.RunScript(p0)
                #
                # if result is not None:
                #     self.marshal.SetOutput(result, DA, 0, True)

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

            def uv_srf(self, set_srf_brep):
                srf, origin_brep = set_srf_brep

                faceDomU = srf.Domain(0)
                faceDomV = srf.Domain(1)
                limitPt1 = srf.PointAt(faceDomU.Min, faceDomV.Min)
                limitPt2 = srf.PointAt(faceDomU.Max, faceDomV.Max)

                parU = srf.Domain(0).Mid
                parV = srf.Domain(1).Mid

                UIso = srf.IsoCurve(0, parV)
                VIso = srf.IsoCurve(1, parU)

                pt = rg.Surface.PointAt(srf, parU, parV)
                vecNorm = rg.Surface.NormalAt(srf, parU, parV)

                UCrv = VIso.CurvatureAt(parU)
                VCrv = UIso.CurvatureAt(parV)

                if UCrv.Length > VCrv.Length:
                    section = VIso
                    source = UIso
                    UDir = True
                else:
                    section = UIso
                    source = VIso
                    UDir = False

                copy_srf = srf.Duplicate()

                # 判断是否为圆锥体
                type_cone, x_cone = rg.NurbsSurface.TryGetCone(copy_srf, self.tol)
                # 判断是否为圆柱体
                type_cylinder, x_cylinder = rg.NurbsSurface.TryGetCylinder(copy_srf, self.tol)
                # 判断是否为圆环体
                type_torus, x_torus = rg.NurbsSurface.TryGetTorus(copy_srf, self.tol)
                # 判断是否为球体
                type_sphere, x_sphere = rg.NurbsSurface.TryGetSphere(copy_srf, self.tol)
                #
                type_arc, x_arc = rg.Curve.TryGetArc(section, self.tol)

                if type_cone:
                    resut_curve = rg.Line(x_cone.BasePoint, x_cone.ApexPoint)
                elif type_cylinder:
                    curve_list = rg.Curve.JoinCurves(origin_brep.DuplicateEdgeCurves(False))

                    # 区分圆线、其他线
                    circle_list = [_ for _ in curve_list if _.IsCircle() is True]
                    if circle_list:
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
                        resut_curve = pipe_edge.Offset(base_pt, normal, distance, self.tol, rg.CurveOffsetCornerStyle.Sharp)[0]
                    else:
                        domU = copy_srf.Domain(0)
                        domV = copy_srf.Domain(1)
                        plane = rg.Plane.WorldXY

                        line = rg.Line(x_cylinder.Center, x_cylinder.Center + (x_cylinder.Axis))
                        bb = copy_srf.GetBoundingBox(plane)
                        line.ExtendThroughBox(bb)
                        p1 = line.ClosestPoint(limitPt1, self.tol)
                        p2 = line.ClosestPoint(limitPt2, self.tol)
                        resut_curve = rg.Line(p1, p2)
                elif type_torus:
                    circle = rg.Circle(x_torus.Plane, x_torus.MajorRadius)
                    plane = circle.Plane
                    domU = copy_srf.Domain(0)
                    domV = copy_srf.Domain(1)

                    p1 = plane.ClosestPoint(copy_srf.PointAt(domU[0], domV[0]))
                    p2 = plane.ClosestPoint(copy_srf.PointAt(domU[1], domV[1]))
                    p3 = circle.Center
                    vec1 = p3 - p1
                    vec2 = p3 - p2
                    arc = None
                    ang = rg.Vector3d.VectorAngle(vec1, vec2)

                    if ang > 0.001:
                        arc = rg.Arc(circle, ang)

                    if arc:
                        resut_curve = arc
                    else:
                        resut_curve = circle
                elif type_sphere:
                    resut_curve = x_sphere.Center
                elif type_arc:
                    nCirc = x_arc.ToNurbsCurve()
                    vecTest = rg.Vector3d(x_arc.Center - pt)
                    p2 = nCirc.PointAt(nCirc.Domain.Min)

                    parIso = copy_srf.ClosestPoint(p2)
                    if UDir:
                        iso2 = copy_srf.IsoCurve(0, parIso[2])
                    else:
                        iso2 = copy_srf.IsoCurve(1, parIso[1])

                    lType = rg.LoftType.Straight
                    uPt = rg.Point3d.Unset

                    def trim_curve(cur):
                        rc, rc_curve, rc_pts = rg.Intersect.Intersection.CurveBrep(cur, origin_brep, 0.1)
                        if rc:
                            new_cur = rc_curve[0]
                        else:
                            new_cur = cur
                        return new_cur

                    if self.skill:
                        loft = rg.Brep.CreateFromLoft(map(trim_curve, [source, iso2]), uPt, uPt, lType, False)
                    else:
                        loft = rg.Brep.CreateFromLoft([source, iso2], uPt, uPt, lType, False)
                    lSrf = loft[0].Faces[0].UnderlyingSurface()
                    resut_curve = lSrf.IsoCurve(1, lSrf.Domain(0).Mid)
                else:
                    resut_curve = None
                return resut_curve

            def get_max_curve(self, geos):
                curves = [_ for _ in geos if "ToNurbsCurve" in dir(_)]
                pts = [_ for _ in geos if _ not in curves]
                if curves:
                    curves = [c.ToNurbsCurve() for c in curves]
                    leng_list = [_.GetLength() for _ in curves]
                    zip_list_curve = zip(leng_list, curves)
                    res_max = sorted(zip_list_curve)[-1][1]
                else:
                    res_max = pts[0]
                return res_max

            def get_center_curve(self, brep):
                # 炸开Brep实体
                face_list = ghc.DeconstructBrep(brep)['faces']
                face_list = face_list if type(face_list) is list else [face_list]
                copy_face_list = [_.Faces[0].DuplicateFace(False) for _ in face_list]
                if self.j_max_surf:
                    # 获取面
                    brep_max = sorted([(_.GetArea(), _) for _ in copy_face_list])[-1][1]
                    faces = brep_max.Faces
                    faces.ShrinkFaces()
                    srf_list = [faces[0].ToNurbsSurface()]
                    # 原始Brep实体
                    origin_brep_list = [brep]
                else:
                    # 获取面列表
                    faces = [_.Faces for _ in copy_face_list]
                    [_.ShrinkFaces() for _ in faces]

                    srf_list = [_[0].ToNurbsSurface() for _ in faces]
                    # 原始Brep实体
                    origin_brep_list = [brep] * len(srf_list)

                sub_zip_sur_brep = zip(srf_list, origin_brep_list)
                temp_curves = filter(None, list(ghp.run(self.uv_srf, sub_zip_sur_brep)))
                reason_curve = Curve_group.RemoveOverlapCurve().remove_duplicate_lines(temp_curves, 1)
                max_reason_curve = self.get_max_curve(reason_curve)

                return reason_curve, max_reason_curve

            def _do_main(self, tuple_data):
                brep_list, origin_path = tuple_data
                reslut_list = map(self.get_center_curve, brep_list)

                # map函数批量处理
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), zip(*reslut_list))
                Rhino.RhinoApp.Wait()
                return ungroup_data
            # def RunScript(self, Pipe_Brep):
            #     try:
            #         sc.doc = Rhino.RhinoDoc.ActiveDoc
            #         j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
            #         Center_Curve = gd[object]()
            #         tol = sc.doc.ModelAbsoluteTolerance
            #         re_mes = Message.RE_MES([j_bool_f1], ['P end'])
            #         if len(re_mes) > 0:
            #             for mes_i in re_mes:
            #                 Message.message2(self, mes_i)
            #         else:
            #             if Pipe_Brep:
            #                 curve_list = rg.Curve.JoinCurves(Pipe_Brep.DuplicateEdgeCurves(False))
            #                 # 区分圆线、其他线
            #                 circle_list = [_ for _ in curve_list if _.IsCircle() is True]
            #                 other_list = [_ for _ in curve_list if _ not in circle_list]
            #                 # 获取其他线中，最长的边线
            #                 if other_list:
            #                     pipe_edge = self.get_max_curve(other_list)
            #                 else:
            #                     pipe_edge = self.get_max_curve(circle_list)
            #                 # 基础线和最长边线相交的点
            #                 max_pt = circle_list[0].ClosestPoints(pipe_edge)[1]
            #                 # 基础圆线，平面，基础偏移法向
            #                 base_circle = circle_list[0].TryGetCircle()[1]
            #                 base_plane = base_circle.Plane
            #                 base_pt = base_circle.Center
            #                 normal = base_plane.YAxis
            #                 # 两线点之间的距离
            #                 distance = max_pt.DistanceTo(base_pt)
            #                 # 边线偏移
            #                 Center_Curve = pipe_edge.Offset(base_pt, normal, distance, tol, rg.CurveOffsetCornerStyle.Sharp)[0]
            #             else:
            #                 Center_Curve = None
            #
            #         sc.doc.Views.Redraw()
            #         ghdoc = GhPython.DocReplacement.GrasshopperDocument()
            #         sc.doc = ghdoc
            #         return Center_Curve
            #     finally:
            #         self.Message = 'Pipe Round pipe'


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

                if res_brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                    res_brep.Flip()

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


        # 求Brep的近似最小包围盒
        class MMB2(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_MMB2", "R44", """Find the approximate minimum bounding box of Brep""", "Scavenger", "D-Brep")
                return instance

            def __init__(self):
                pass

            def get_ComponentGuid(self):
                return System.Guid("cfb20b2e-b936-4ab6-af0e-46430790e659")

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
                self.SetUpParam(p, "Brep", "B", "The Brep that needs to be solved")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Smooth", "S", "Smooth surface or not. The default value is False")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Box()
                self.SetUpParam(p, "Box", "B", "Approximate minimum bounding box obtained by Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Minimum bounding box reference plane")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'MBB-2'
                # 初始化输出端数据内容
                Box, Plane = (gd[object]() for _ in range(2))
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    # 确定不变全局参数
                    self.smooth = p1[0][0].Value
                    self.j_bool_f1, brep_trunk, brep_path = self.parameter_judgment(p0)
                    re_mes = Message.RE_MES([self.j_bool_f1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将实体与树结构集合放入多进程池
                        zip_list = zip(brep_trunk, brep_path)
                        iter_ungroup_data = zip(*ghp.run(self.temp, zip_list))
                        Box, Plane = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                # 将结果添加进输出端
                DA.SetDataTree(0, Box)
                DA.SetDataTree(1, Plane)

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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQsSURBVEhLrZVrTBxVFMe3WMk2xS7NyqMElAbKwszO7MyyLEtZWFoK2MVSnhVqLZQWCIqNhTYiTdMao6WkD6i8BAQqL5sCWj8A5VGJGvxA1A+2mppAamJMqtZnomFp8vfM7qWPuFmq8ksm98699/zOnTN3dlUrwLogP1U566846qq8x67Oj4agOEP9Ad2vcQ2vDOr9iYFTi+1bgHdSsdidgKP2J2Zo3N81/f9Q798aNOXoeApoTgPqtwGN1Hba0VvI36D5CNey/4b6wLYNE47O7S75eZIvXY0pQFc6WveG36J1Ftfyf4dL3kVyZccnbUBDMvXvS3KekvSmou+Y35/+WlUGi3sQ+euMIOO3z4Sx2yXUB1ICJxzdVBZFXmfDwutW/HY8npKQVNn9UpLTtGZWxuAZH7DYB5E/zYySrmf+Lt3MvZy4UCQoYyVpAeNOeRPJa21wvGzFL/lx+D4hBvMvmnHnTXqSVppTErWk448BGc8XPDrkFLrD8NmOj2NRjIDRlIM1m7UXHReYnMriqLXih90W/Boai5sJJowURWGskMc3NRYsnEvGd6dsyDdrB5jKPcavsoza8dSqwKlkzFwi+dlUl/wNK34+FIcf42Mxt8WEmSwRg3t06MnehP4cHbp26WEK0fQyjWeqzZqB0UtpiLmejZkOqi3V+3ZlHH6KicW1HTLGyzgMFkSiP1eHoXwO3Yr8Sc0FFu4R75Ltj19x9FBJaOeT7ckQrmVgui4Jf8lmfKnISzkMKfK8CGo5tOfwiAn17WTxHvEusWuvOOiooYlKQy8UNfEYbktCTkk8ZlMMuKrI85Wdu+QduTzkEN82Fu8R71K7dux++eKrVtyuicOtg9H4sEjASDGHYSYfZjs3hmpaWLxHvMue1o46+u7J7zD5fKUJn5cbML2Pd8r7mLwli4N+g6aRxXtkTdlOn1HHAJ3lJvpK3cgni/i7ZXmP5K3ZHITgdQ0s3iNeO5NXj2A23LXzk0nLyhsznfIzLH5ZVsXLXsWT9QFA21YsnkhwI9e55Lt5kkchItCnjsU+PPTD9Ox0BQ+8log5D3Kdn/owC7mLxWJ5uD8aa7Bm3xcvSJg7FI2JQuUo6pwv9H2Sn03XIdTf921OliskSayNjpb2yrJ0TpblcOrnmkxyPl3NNNdqtQrrmfKfZHPrS/t3bcLYHh5d9kgM0ddZnxGJMO3aqrUbjYIoih8JgnBEEPSfUL+a+s2UoMBgEC/T/XFJFNsMgvAS07knLNirYuhIEG60RKCnbCMig3yOKeNGgyFV1OtPmUwmPcnqJLOZI9kASV+RJMO7PM8b6AnKKekJp8gTcSavwxcbNEja7HWUDakoMIESVBuNRuoKNa5EQq0sis+R+C1J4mOMRkOpKOorWciySKxdYlVeXt4jbloVx3E+NpttNV3qey9dpfobxCpftex7dvgAAAAASUVORK5CYII="
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

            def parameter_judgment(self, tree_par_data):
                # 获取输入端参数所有数据
                geo_list, geo_path = self.Branch_Route(tree_par_data)
                if geo_list:
                    j_list = any(ghp.run(lambda x: len(list(filter(None, x))), geo_list))  # 去空操作, 判断是否为空
                else:
                    j_list = False
                return j_list, geo_list, geo_path

            def convert_cuvre(self, curve):
                # 将曲线替换为首位相连的直线
                start_pt = curve.PointAtStart
                end_pt = curve.PointAtEnd
                line = rg.Line(start_pt, end_pt)
                return line

            def get_max_angle_line(self, line_list, ref_vec):
                # 获取角度列表
                angle_list = map(lambda x: rg.Vector3d.VectorAngle(x.Direction, ref_vec), line_list)
                # 获取角度最大的线段
                max_angle = max(angle_list)
                max_index = angle_list.index(max_angle)
                res_line = line_list[max_index]
                return res_line

            def group_hv_line(self, line_list, ref_pl):
                # 剔除失效的线段
                line_list = [_ for _ in line_list if _.IsValid is True]
                # 分割为x、y轴
                x_list, y_list = [], []
                vector_list = [_.Direction for _ in line_list]
                for v_index, vector in enumerate(vector_list):
                    x_ispara = vector.IsParallelTo(ref_pl.XAxis, 45)
                    y_ispara = vector.IsParallelTo(ref_pl.YAxis, 45)
                    # 判断线是否与x轴平行
                    if x_ispara == 1 or x_ispara == -1:
                        # 若为反向平行，将直线反转
                        if x_ispara == -1:
                            line_list[v_index].Flip()
                        x_list.append(line_list[v_index])
                    # 判断线是否与y轴平行
                    elif y_ispara == 1 or y_ispara == -1:
                        # 若为反向平行，将直线反转
                        if y_ispara == -1:
                            line_list[v_index].Flip()
                        y_list.append(line_list[v_index])
                # 获得线与x、y轴夹角最大的线
                if x_list:
                    x_line = self.get_max_angle_line(x_list, ref_pl.XAxis)
                else:
                    x_line = None

                if y_list:
                    y_line = self.get_max_angle_line(y_list, ref_pl.YAxis)
                else:
                    y_line = None
                return x_line, y_line

            def determine_z(self, vector, z_vector):
                # 确保向量是单位向量
                vector.Unitize()
                z_vector.Unitize()

                # 获取 另外 向量（通过 两个向量 的叉积获得）
                other_vector = rg.Vector3d.CrossProduct(z_vector, vector)
                other_vector.Unitize()

                return other_vector

            def _generate_plane(self, origin_pt, x, y):
                res_plns = []
                # 消除空值，获取轴的方向
                filter_ax_list = filter(None, [x, y])
                ax_list = [_.Direction for _ in filter_ax_list]
                ax_len = len(ax_list)
                # 判断有多少个轴，即多少种情况
                if ax_len == 1:
                    only_plane = rg.Plane(origin_pt, ax_list[0])
                    res_plns.extend([only_plane])
                elif ax_len > 1:
                    # 每根线分别做一个平面
                    single_planes = [rg.Plane(origin_pt, _) for _ in ax_list]
                    res_plns.extend(single_planes)
                    x_axis, y_axis = ax_list
                    # 确定标准平面的Z轴
                    z_axis = self.determine_z(x_axis, y_axis)
                    # 按轴生成xy平面
                    xy_plane = rg.Plane(origin_pt, x_axis, y_axis)
                    yx_plane = rg.Plane(origin_pt, y_axis, x_axis)
                    res_plns = [xy_plane, yx_plane]
                    # 按轴生成xz平面
                    xz_plane = rg.Plane(origin_pt, x_axis, z_axis)
                    zx_plane = rg.Plane(origin_pt, z_axis, x_axis)
                    res_plns.extend([xz_plane, zx_plane])
                    # 按轴生成yz平面
                    yz_plane = rg.Plane(origin_pt, y_axis, z_axis)
                    zy_plane = rg.Plane(origin_pt, z_axis, y_axis)
                    res_plns.extend([yz_plane, zy_plane])
                else:
                    Message.message2(self, 'Plane axis error！')
                # 标准平面
                standard_xy_pl, standard_xz_pl, standard_yz_pl = rg.Plane.WorldXY, rg.Plane.WorldZX, rg.Plane.WorldYZ
                standard_xy_pl.Origin = origin_pt
                standard_xz_pl.Origin = origin_pt
                standard_yz_pl.Origin = origin_pt
                res_plns.extend([standard_xy_pl, standard_xz_pl, standard_yz_pl])
                return res_plns

            def get_bbox(self, origin_brep):
                if origin_brep is None:
                    return None, None
                # 获取最大面
                temp_face_list = ghc.DeconstructBrep(origin_brep)['faces']
                if type(temp_face_list) is not list:
                    faces_list = [temp_face_list]
                else:
                    faces_list = temp_face_list
                area_list = [_.GetArea() for _ in faces_list]
                max_area = max(area_list)
                max_index = area_list.index(max_area)
                max_face = faces_list[max_index]
                # 除最大面的其他面
                others_faces = [faces_list[_] for _ in range(len(faces_list)) if _ != max_index]
                # 是否顺滑面
                if self.smooth:
                    max_face = max_face.Faces[0].ToBrep()
                else:
                    max_face = max_face
                # 获取最大面的中心点
                center_pt = origin_brep.GetBoundingBox(True).Center
                # 取其他面的前15个和最大面组成新列表
                others_faces = others_faces[0: 15]
                temp_faces = [max_face] + others_faces

                # 闭包函数获取最小包围盒
                def get_minbox(surf):
                    surf = ghc.Untrim(surf)
                    # 获取最大面的平面
                    pln = ghc.IsPlanar(surf, True)['plane']
                    # 获取最大面所有边线
                    edges = [_ for _ in surf.Loops[0].To3dCurve().DuplicateSegments()]
                    #            edges = [_ for _ in surf.Edges]
                    lines = map(self.convert_cuvre, edges)
                    # 将线段分为偏水平和偏竖直的线集合
                    res_x, res_y = self.group_hv_line(lines, pln)
                    # 点、结果x、y线生成9平面
                    pln_list = self._generate_plane(center_pt, res_x, res_y)
                    # 获得9平面生成的包围盒，并拿取之中包围盒面积最小的，并输出平面
                    box_list = map(lambda x: rg.Box(x, origin_brep), pln_list)
                    min_index = 0
                    for box_index, box in enumerate(box_list):
                        if box.Area < box_list[min_index].Area:
                            min_index = box_index
                    sub_res_box = box_list[min_index]
                    sub_res_pln = pln_list[min_index]

                    return sub_res_box, sub_res_pln

                # 每个面分别获取最小包围盒
                boxes, plns = zip(*map(get_minbox, temp_faces))
                # 每个面的最小包围盒，拿取之中包围盒面积最小的，并输出平面
                min_index = 0
                for box_index, box in enumerate(boxes):
                    if box.Area < boxes[min_index].Area:
                        min_index = box_index
                res_box = boxes[min_index]
                res_pln = plns[min_index]
                return res_box, res_pln

            def temp(self, tuple_data):
                brep_list, origin_path = tuple_data
                if len(brep_list) != 0:
                    brep_list = map(self._trun_object, brep_list)
                    boxes, plns = zip(*map(self.get_bbox, brep_list))
                else:
                    boxes, plns = [], []
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [boxes, plns])
                Rhino.RhinoApp.Wait()
                return ungroup_data


        # Mesh转Brep
        class MeshToBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_MeshToBrep", "R45", """Rhino grid convert to Brep""", "Scavenger", "D-Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("17b4df2c-82ef-4bf7-9ba3-98ede6e291e3")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Mesh()
                self.SetUpParam(p, "Mesh", "M", "The grid to be converted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Join", "J", "Whether to merge Mesh")
                p.SetPersistentData(gk.Types.GH_Boolean(False))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Breps", "B", "The generated Brep collection")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                # 插件名称
                self.Message = 'Mesh to Brep'
                # 初始化输出端数据内容
                Breps = gd[object]()
                if self.RunCount == 1:
                    # 获取输入端
                    p0 = self.Params.Input[0].VolatileData
                    p1 = self.Params.Input[1].VolatileData
                    # 确定不变全局参数
                    self.join = p1[0][0].Value
                    self.j_bool_f1, mesh_trunk, mesh_path = self.parameter_judgment(p0)
                    re_mes = Message.RE_MES([self.j_bool_f1], ['M end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将网格与树结构集合放入多进程池
                        zip_list = zip(mesh_trunk, mesh_path)
                        iter_ungroup_data = ghp.run(self.temp, zip_list)
                        Breps = self.format_tree(iter_ungroup_data)

                # 将结果添加进输出端
                DA.SetDataTree(0, Breps)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARTSURBVEhLrVZ/TFtVFO6jpY++/oCW0rUFB7T8fH2vr8AQgk4YrJrMAd0YbrKRTKYiUzZmNLjNicp+BN3QRbclGONEliks7A+jqDESHFni3IyDLMMNjC6GOExeMBpnlujnuaUk4uxYAif50nfb8+537jnfObcaMi0hg5B9G7gI0WwpQYkCmaCxEtSNsgXlqUaIXh3qQwbUryJUGlB1Hw/6vZs5RrET631mNBZbsdIjQHLwaCyyovFuK+6y6P5kDlaO0/z6dpUTwxtT0d5sBKZSgO/cwLVk/DyQxAh6mGMU67n+TAZwzI+BTSl47h4b8KYMvC4hlGP6gzlY7/cKar3fgtpMCw4/awau0ObnnMCoC2N99vlO0D32VDpw0IfeWje2U/ToEIH9uXgw0/g7c7CuyzWp49s9bCOc3JcwE/1iElR4BBWHZWzKiUfbVkrRRDLw1SISUHFUvCZhb1kSdLwGU587gBHXIhN0SmhbkYjqlXpsqTLM1GFRCQ5JeKIgAd98YMOGYBz6O6gWpKLLvbcSlJSUmBkiyzskeNWHzQELRk8l4oePklAoxuLmRRcmTodl+i5znLX8/HyvosgHI8s7JOjwoU4x42Iv6finZLzQYELbFhOmv3Awgp5gMGicjTwvLy9DlqUbYnEpmwBvXGkmgkM+9D3kRgsjeIUIDuRi9RyC/SJqFRPGP7SHC3zzghMVhXqc3GuB0yEMy37lsixJU5LPd12SpF8UxQ9JUfo4jntr7Ml5ThCkRkN7LmoCRkx+lgRcIAWNuXGmy4YUB4ckm/C17Pf/FaBNFf8M6ARQFOU3nueHy9MFVEtmLHPHwWONRTWNjmrRDIdRO0PAOhltOVhbYIQ6RBKl6MONNu5GU42BUhQ7RBEPST5xxCeKI3SKS4xE8ge66P0jZx5Zism2bHRVLsGj+fGYfD4LkzszUZEuzBA8QAR/7yaCQgE3zv6L4JILV/vDKppT5CKpaAmlaVosLHXS8sjENg9YH/WvT8YOGnosXSxNlVmRFFExVOzKxcPLBRoTLD0RXHNj6tNwkefINBAIZMqyvDuyfG9eFbnMOnUd5cyVqEVjSMDm1QY00KjeVmcM9wT5zCEoLi42iKKojyznl2nZMr365XErTHwMfJY4nG1Ix7dNXhwLOmlzDryOW1gnh8p49cdP7NhalICXS+3Yea8NV2nGl6cJ6F7jgpXXLpCglFfPv2/D4wXxwFEFa3JM4Gh0j7d4oLZm3JKi/9j8BGtX8OoQpWjP8kSMtngRpKuPJIaeGhemWzMXTrAhSCc4kYhgmhGrvEZM7PCGXwhlm/BSmR12w+1T9D1dVuyKZDJ9+n9kaivN0+Noq4VFiuMhF0aaPTjflIaP6Y5NiNNCF6M5zRyj2Klzj6VCbc/BO9VONNJEVl/MhronC3SRsT01BsI+QqeW03TSH4BO9jwL9h191hGi2S6bIWbQYdINWvQxgwYdF35m0MdwA/8AwZMWid5L/YgAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

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

            def _get_mesh_pt(self, single_mash_face):
                # 判断各个Mash面为三角形还是四边形
                corner_str = ['A', 'B', 'C', 'D']
                # 循环获取角点的下标
                corner_index = []
                for _ in corner_str:
                    corner_index.append(eval("single_mash_face.{}".format(_)))
                return corner_index

            def turn_brep(self, sub_mesh):
                if not sub_mesh:
                    return [None]
                # 获取网格的面和点
                faces = [_ for _ in sub_mesh.Faces]
                pts = [_ for _ in sub_mesh.Vertices]
                # 获取每个网格子面对应的点下标
                pt_indexes_list = ghp.run(self._get_mesh_pt, faces)
                # 获取四点成面
                surf_list = []
                for pt_indexes in pt_indexes_list:
                    sub_pt = [pts[_] for _ in pt_indexes]
                    surf = rg.NurbsSurface.CreateFromCorners(sub_pt[0], sub_pt[1], sub_pt[2], sub_pt[3])
                    surf_list.append(surf)
                # 曲面列表合并为Brep
                sub_brep = rg.Brep.JoinBreps([_.ToBrep() for _ in surf_list], 0.01)
                return sub_brep

            def temp(self, tuple_data):
                mesh_list, origin_path = tuple_data
                if len(mesh_list) != 0:
                    mesh_list = map(self._trun_object, mesh_list)
                    if self.join is True:
                        new_mesh_list = [ghc.MeshJoin(mesh_list)]
                    else:
                        new_mesh_list = mesh_list

                    single_brep = map(self.turn_brep, new_mesh_list)
                else:
                    single_brep = [[]]
                ungroup_data = self.split_tree(single_brep, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data


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
        if Result:
            Listener().PriorityLoad()

    def get_AssemblyName(self):
        return "Tradition"

    def get_AssemblyDescription(self):
        return """HAE plug-in"""

    def get_AssemblyVersion(self):
        return "v4.7.1"

    def get_AuthorName(self):
        return "by HAE Development Team"

    def get_Id(self):
        return System.Guid("86c4ead2-84fa-4dff-a70f-099478c2ccca")

    def get_AuthorContact(self):
        return "software_team@heroesae.com"

    def get_AssemblyIcon(self):
        icon_text = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAT+SURBVEhLrVVrTJtVGD7hWnTCkPa79ELblQKVbmEKShYNYW6LOEyAjrG1fJe2XwtlM1smDEWzEv3jEhNDzOKYiMv0j+yHiy4maoz+MLIsDtkyFcZFiAMMUIFSbkM4vqe0CB+IMbHJk/d857zned7b9xWRnx/jmP8TQBiD/YWKH7zeeDTE63JCPNs7wzG90w5A1G4LehUcwbp9sq5i+mZ5amzGreu8Lxqb0TjH5GFBhTGvxMvcKlZ4VRjy5/WQ+xGLnQAvjYOc+vMet9kyzBveRWMO9vH5KgrPOpR4xv7fEXKowpaQzwv09IRT6yRl73VZSkd5fXtEQIXnQCDqHLVyEmI3nMF6EaLHbhqHBOarHt6suePbnXpPynXfd5lax6rU19YESAbrL8tFtgIW4Z5ALwVE/RkS9aAna1+PJ7cu4NJ/+KebWph0UN+GBRY4akMGBNsJzFeRqCkc4pkbv7oy9n5TW7hjwG2qHHKam0JO9iYRxi4VDlQxX6wJbNUDuWAQLBmIRYHB05ymiUTd0tISf8+T44PaXwSeSSys+pOeBBzMlxtKFCVbI7X/LUAyDEctsN2/Oc1PtVdUxP7i3fNCtye3GOr/NYl6ETIjQRD/fxQgkYYiTgTkQngEgWBa0Lzj9/sTur2Z2X1ui2/UabgwJ9BBchb1j2KTwBwpR0RkKTzTVNiJYFZkhiZE40FSkh7JWjbg2lUf5NXXl6FcSzBF0aijIJnLBFZ7QEZuimMHR1wZNb+LRvsMz7RPitrrpIn93sfSe6qtJ0dFw1sLHN2PnUo8GyWU9YrYTQLRKQoSISf1xzCva/D7T+286Ss4MMSb+QFXZsOUU3ttEZq4DBnKo5Zjk0AIiBci4xfkqRujLuPhzpN5xbdqn362T9p9PMizPeGoI2UkWB+5HDKB1SZCw1Zg3M6RWpNfX01u8ZA3p/FTb8lDkxzbsQI1J5flxFuWSFRGBDj1XvKqz4rs3UHRtC/CjcYE3dUHAr2MJQYPStklAV730VbTIscmgXF7WhE08soHfkFBiMcFXU1Q1H02ZVeFsAcmhKMGb9UWZAQ5ZuQBlFBOGIU8q7USjVfR+ydE9RVCPsybX8ESjbFE4Xlo5BxMUFdNnnVK0F4mY7ue4N+wlsGswD6BaxmoP9sfcJna5iWDd1HSeOYlvRj0GKrhE3wb+0AUvi3YBe/Gtja6BtRQ8Dmhv0MfH9Jm9B7TtswJmgu9lWxbp033xvel6vqOMs35Thvzyc9H2KtdpUzbHRvTerecfm/Ern57WdK8fruceZ/sdVewF38qZy51lTNtP5bRl1ef6UsDx9StHTZNA9rxKFWG4lU8KRFSqM7GUcZXEUo4DU92hOgnUYrxCKwdABeKSz2DUtK9sLYCDiMUQ/5cyBnZK0bokQKEKACqBgDnwy+i9PR0m0qlqoONyrS0tLrMzMzmlNQU8qU8q1AozlksluLk5GRfQkJCvdFobFSr1c2xsbGH4HwnoDEuLu40+EFQqB5sHXD4YmJiXgb4KYo6j2iaLklNTa0HhwSwXq1W+1pSUtIpIClTKpWFer3+TfA5CmfpYJsgGCecQfSIAxIfWDfYE7BXBALPJCYmkmyq4fmARqOxoby8vF0QmWQymTwQ/XOQ0X6IssRsNlsAZfn5+RI47gEUGQyGQjh7CcQq4c4JgA18RLB2q9X6PKyPZ2Vl1UFQPuA7mp2dXfIXO8FFxSea9bcAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(icon_text)))


class Listener(gk.GH_AssemblyPriority):
    def __init__(self):
        pass

    def PriorityLoad(self):
        Grasshopper.Instances.CanvasCreated += LockGh().Instances_CanvasCreated
        Grasshopper.Instances.CanvasCreated += Cancel_connection()._Display_connection
        Grasshopper.Instances.CanvasCreated += Cancel_connection()._Show_connection
        Grasshopper.Instances.CanvasCreated += Cancel_connection()._Cancel_connection
        Grasshopper.Instances.CanvasCreated += CreateMenu()._CreateMenu
        return gk.GH_LoadingInstruction.Proceed


class LockGh(object):
    def __init__(self):
        pass

    def Instances_CanvasCreated(self, canvas):
        Grasshopper.Instances.CanvasCreated -= self.Instances_CanvasCreated
        _toolbar = Grasshopper.Instances.DocumentEditor.Controls[0].Controls[1]
        button = System.Windows.Forms.ToolStripButton("Lock/Unlock GH\nPowered by HAE Development Team")
        _toolbar.Items.Insert(7, button)
        button.Image = self.Lock_Unlock_Icon_24x24()
        button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
        button.Click += System.EventHandler(self.Gh_solver_en_dis)

    def Gh_solver_en_dis(self, sender, none_e):
        lock_state = Grasshopper.Plugin.GH_RhinoScriptInterface().IsSolverEnabled()
        if lock_state is True:
            Grasshopper.Plugin.GH_RhinoScriptInterface().DisableSolver()
        else:
            Grasshopper.Plugin.GH_RhinoScriptInterface().EnableSolver()

    def Lock_Unlock_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATaSURBVEhLrZR7TFt1FMevixinQ8kmMUZBoYwRZDJJSHAbWNgYBLJO2kIfUPrgVdh4FlqeozwKd6OUjlEeDkgcjI0JWMZrY7wfAoPNbWbqPyYu/jFjDEk1kS1LPJ77QDYLionf5JPfOed3cr/tub/fJZ6RS0h4uPAtF5dANv//5Orufog01z9p7+4BU0sriOSKz7H8ArO7fTk4OOzH5R0m29COtBzN98WV1Q89PPZJuUdCc/RkDQSHR+Sy+9vRe5qCoq/OXWgD/dlaCP+EX87WCcLPz+/YqVwdYOjDVAjihEDYcipX+xuGu5jKP0udmXWrymT+40hYWLFYFt9abqyDgKCg4/SmQCKtlyoTv6MTVhwOh6stLQNnZ+cDbGlLuXI4fvml5bDb2VnAlgi+SDQolqtmmUQiaRIrVEt0wsrLy+ujTG0+Grzty5a2VERUVLZSnfY7hjuYCkEEBAQcF0pjf8HwRXQTW9Bghdli5O3tfThLV7Atg2hpnCU+MfkbNqXl7u7uIxBLf8XwTQIDi0SVcJvZYvRfDCRy+RWZKmmGTWl5ebl5ovEajtiD4AmEjQJJ3By7R4syYEbk/K8GsXKlVSJX3GBTWjhiT5FM/tTV1cOb+OCAX7OP74fUuf9LlEF6nm67Br1ShXKETWl5erq6UQYuLi4c4mBQUFVg8NE77B6t9z09/dOyNbBrzx4vtrSZqIvo9DGXOxoYxJ3E+NVn8OWGHH2KazBCvIy8RgWsHHbufImvTEqm7sYxhLqZz+KGvIHsVqWkPKyoMUFhWeVjPWl8RFF2xviopIr8uajcAHkl+sfY97xCQriF1Sbzk4u9VqixND8529C0RlFDYWlea/ys82mMTDGMrY6kyfR4YvkuDE3Pw/DsAozMLdJcn1uCmwsrcHX4JvUjn1fUicjanuHr0NbdBx1fDECndZChfxAu9Q/Btck5SDiZMY2tjtywSFtskhqi45V2iJUJwBPH2Rvs5bxLRsfJICo2HqKkuP4NkTIJ9vsfGsdWx7iERFspfnt0OA5dGUKtSD5SZCAhs/C0vQGPF0l29lmhtbsXWq/04D9ZpxfakavXx0Cekk4bmBsttvn73+I4luHm4gqMrbN0G2bufA3WsSl7g8jIMLL9cjc0XuyiaVqnowuaOy7jqIZAlpBKG/CiRbb0/CJIydIguZCSvUFarhbkqembjciNjJHheOKQ2E1GpNoYUSRfaFNrtKA6mWFHUkY2SBPV9gZ8Po+kXnKHdWjjBSPUC6YYmJqDpPQc2sDU0GCbvfsAbswvwY0vb8EoBTUuZGrlHvSNTtobhIYGk/WtbWBsvgDGpk8Rar0AtZhTtFzqhhiZijZQpqhthnMWOE0aGc4YoZSmFipqzaDVG+wN9u11IyUKJQjxqAllCjukeCx9A4Jog8DQMJtIlQh8PHHPI8NeOURES+wNogX8utH5BejH894/MYunZgK6R8bpeGBqHmbuPYDUrLwFbHU01NSsjS7eBuv4NPRTTMzQXEOoC9c1MGJvcPhgQHp+qf6+puj0/VOavB/NDXXQ0tYIWVrdTzkFxcuFFdUroRG8RmzdlZya+oPR0rJaWWterTSdWzVQ1NWvViFnz1tWSwxnVpmnbqFXdhAFOtUB0Kv9wdvVwcqW10V97F5HnLaGcPoT8S29cENG0iAAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


class Cancel_connection(object):
    # 取消电池连线
    def __init__(self):
        pass

    def Cancel_connection_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH3SURBVEhL7ZTfS1NhGMdf2CilHzDI6Y5z5po0xWhBiHmlUV50GyNvuu0iRCzYdSQi+icEXRbloBAc50KZ5+yMc4ptxdCaNsbU+avWttN0nu0ct/P0Ol6w6O49N13sA9+7z/t9Lt7nfVGD/w+v12tKJpNnWZalit/vP0Oq/iUUCj2IxWJJQRDSPM9TBZ9Ph8PhGVL5N0GOWyyVSmAk8kEReEkqSHNzzaT2lKXl5XdlTQMjqAUZxIXAFgIwpc61WlHO5rqbZZwvTgZsevo/qol1olISX4HM4PDGJ5+POWScX5FssU3p9m7IDI0syabzoL56Q0w6aiurkLfYKvtuTwocVwGtTk4/B88AHLdehl1XH+QSa0Slo7y7p+27r+tgc0LW7hIR+ys/mh19eHBkvghfHj2G7WNjd3BYrSqbd+5pSpMFvj/xbSAFIUfR3i3XWhyQuXYTsuk0UelQ17/Vflo74ehSB1Ru3AKUY67MQqcbtodGUkXzBai8fktUOvTPcfjR1aOvjU3koa0LD2h33ceZlySpecfZE1exYIQq3sLE+NOdl7rOFKwds/X9h97e+vMOBgLvK6pKVDqUchn4D9LWM44z18v/JCgI7MkADT822iiKAiFByHMc10RqTxFF8XYkEuHwnyRhgSrRaFTEf9k4qWzQwDAI/QaomQGgdek8+gAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def Display_connection_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJSSURBVEhL7ZVPiFJRFMaFIlwIM5XMiDY4/nm+0Xzv3nfuc3JIMKJdEWW1aNFsIoZpUwQxyzYtEtoJYZt2rd2YRahhMUoQMZvBpTiEi5BhlBoXTd7OqbeKkXyNm6APfsi53O9898/zPcfvMk0zAQC3TIC786Z5w2ua6tATuCdn/WesKX8nbHwRG68bhvEWOH8ZAdiIc/6+ForKphKXdzTtmjXVvrDxAzCghb+XU7oeCQB8PM1Yr+uPbOHqn3EhrquGsYXhVyzL+BKcX2WM7aTT6cNUuwEeXwIhP82F5fOoLl1C3KTxRV0PcG58wZ0aVI8tXdfxJHgLV7lMdVaNZfvBmHy0EJeBRELiUZ2lcSHEGmPGJu7CS7UtqZqmeQSsP1W111+9oe2H0XjVlzA3GcCTpaXEBbz3FwbAG8bS05bFvj77lOzOnLJ7OxZ/5THhHd7HBx0vORgMtdwzM1mcEkL8iGoTh6PrCyd3T4Q3BrP+earTjE0nk0mf0+lK5fP5XqPR2C6VSnvFYlGOS6VSkblcTv4MkI5fF7yPTtbrdTkcDmW/37cFechr9RkpVi6XZa/Xk51OxxbkIa/VZ6T+3QC6k0NIaFIBbiSJcIReainkGLKKT8P3gwbQShcRH6IjFEJj55D71Wr120EDjiACOYosIDGEdB5ZmUQAKYKcQuiYaOV0RB5kDQP2JhFAOo64kCmEduNEgjRpUgH76f8f7c8BtVpNDgYD2e12bUEe8lp9RgoKhYJst9uy2WzagjzktfqM1JSiKBn8TGbw02oL8iiKkvkBJyMUgOaZwIUAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def Show_connection_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIISURBVEhL7ZXPaxNBFMcLLZJDodWWYu1BTNhatOz82J0aoRCR3lqEpj0LIqKe1EPp0bPngOQv6DVQ0ngwG4lggiCCh5JjyCWHEsSEQg5t8/w+mJO6mCG5CH7hw86b3e/37cxmsxO/KgxDo7V+Al4qpR6hXrWnRhOCHiD0E0I/SinfYfwNx0PUdYzfg8Be6i6YX2ulmzhuG2OWEfoV9NAgwtwixs/ACdixluEVSLkrhPiRyWSmuEZoDk0Ic2TMGkmpX/C87/s3pFSnWKniemjBuIrQZhAED7nG+DEeAymlKQhDwgru8zzO7wuhjrGKa1w7CSYfHGObD7U22xgfIJzD3pq7ZgsNj5TWH4TIzFqLu3iLlFCvEBpJftBaf/Gl/JxMpprzCwtvcEkKXAc3Hfld2P/ZdDq9lEhMr+fz+W69Xv9eKpXOi8UiDUsURZTL5chGxup2rVajwWBAvV7PCfaw1+bESpTLZep2u9Rut51gD3ttTqz+3Qb80k2C1LgazIM0kOAeWAdXwHP8Gi5GbcB3ugaWgA+4Cc9tgL1KpXI2aoNLgP8pL4MVcAuwNsHTcTRgLYM7gLeJ75y36CrYR4PzcTRgzYFpMAN4NQmQ5IvG1eBP+v+i/b1BtVqlfr9PnU7HCfaw1+bEShcKBWq1WtRoNJxgD3ttTqxmPM/L4iOUxafVCfZ4npf9CUMaAg3rSJxbAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def _Cancel_connection(self, canvas):
        Grasshopper.Instances.CanvasCreated -= self._Cancel_connection
        _toolbar = Grasshopper.Instances.DocumentEditor.Controls[0].Controls[1]
        button = System.Windows.Forms.ToolStripButton(
            "Cancel connection Wire\nClick the left mouse button to disconnect the front wire of the selected battery\nClick the right mouse button to disconnect the behind wire of the selected battery\nClick the middle mouse button to disconnect all the wire of the selected battery\nPowered by HAE Development Team")
        _toolbar.Items.Insert(7, button)
        button.Image = self.Cancel_connection_Icon_24x24()
        button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
        button.MouseDown += System.Windows.Forms.MouseEventHandler(self.Mouse_Click_Event)

    def _Display_connection(self, canvas):
        Grasshopper.Instances.CanvasCreated -= self._Display_connection
        _toolbar = Grasshopper.Instances.DocumentEditor.Controls[0].Controls[1]
        button = System.Windows.Forms.ToolStripButton(
            "Display Wire\nClick the left mouse button to hide the front wire of selected battery\nClick the right mouse button to hide the behind wire of selected battery\nClick the middle mouse button to hide all wire of selected battery\nPowered by HAE Development Team")
        _toolbar.Items.Insert(7, button)
        button.Image = self.Display_connection_Icon_24x24()
        button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
        button.MouseDown += System.Windows.Forms.MouseEventHandler(self.Mouse_Click_Event_1)

    def _Show_connection(self, canvas):
        Grasshopper.Instances.CanvasCreated -= self._Show_connection
        _toolbar = Grasshopper.Instances.DocumentEditor.Controls[0].Controls[1]
        button = System.Windows.Forms.ToolStripButton(
            "Show Wire\nClick the left mouse button to show the front wire of selected battery\nClick the right mouse button to show the behind wire of selected battery\nClick the middle mouse button to show all wire of selected battery\nPowered by HAE Development Team")
        _toolbar.Items.Insert(7, button)
        button.Image = self.Show_connection_Icon_24x24()
        button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
        button.MouseDown += System.Windows.Forms.MouseEventHandler(self.Mouse_Click_Event_2)

    def Mouse_Click_Event(self, sender, e):
        if e.Button == System.Windows.Forms.MouseButtons.Left:
            self.Cancel_front_end_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Middle:
            self.Both_Cancel_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Right:
            self.Cancel_backend_connection(sender, e)

    def Mouse_Click_Event_1(self, sender, e):
        if e.Button == System.Windows.Forms.MouseButtons.Left:
            self.Display_front_end_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Middle:
            self.Both_Display_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Right:
            self.Display_backend_connection(sender, e)

    def Mouse_Click_Event_2(self, sender, e):
        if e.Button == System.Windows.Forms.MouseButtons.Left:
            self.Show_front_end_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Middle:
            self.Both_Show_connection(sender, e)
        elif e.Button == System.Windows.Forms.MouseButtons.Right:
            self.Show_backend_connection(sender, e)

    def Cancel_front_end_connection(self, sender, e):
        """取消电池前端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        params = []
        for compent in selected_objects:
            if 'RemoveAllSources' in dir(compent):
                params.append(compent)
            elif 'Params' in dir(compent):
                params += [_ for _ in compent.Params.Input]

        true_params = [_ for _ in params if _.Sources]
        sources = [param.Sources[0] for param in true_params]

        doc.UndoUtil.RecordWireEvent("Remove wire", true_params)
        zip_list = zip(true_params, sources)
        map(lambda x: x[0].RemoveSource(x[1]), zip_list)

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Cancel_backend_connection(self, sender, e):
        """取消电池后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        params = []
        for compent in selected_objects:
            if 'RemoveAllSources' in dir(compent):
                params.append(compent)
            elif 'Params' in dir(compent):
                params += [_ for _ in compent.Params.Output]

        true_params = list(chain(*[list(_.Recipients) for _ in params]))
        sources = [param.Sources[0] for param in true_params]

        doc.UndoUtil.RecordWireEvent("Remove wire", true_params)
        zip_list = zip(true_params, sources)
        map(lambda x: x[0].RemoveSource(x[1]), zip_list)

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Both_Cancel_connection(self, sender, e):
        """同时取消电池前后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        input_params = []
        output_params = []
        for compent in selected_objects:
            if 'RemoveAllSources' in dir(compent):
                input_params.append(compent)
                output_params.append(compent)
            elif 'Params' in dir(compent):
                input_params += [_ for _ in compent.Params.Input]
                output_params += [_ for _ in compent.Params.Output]

        true_in_params = [_ for _ in input_params if _.Sources]
        true_out_params = list(chain(*[list(_.Recipients) for _ in output_params]))
        true_params = true_in_params + true_out_params

        sources = [param.Sources[0] for param in true_params]

        doc.UndoUtil.RecordWireEvent("Remove wire", true_params)
        zip_list = zip(true_params, sources)
        map(lambda x: x[0].RemoveSource(x[1]), zip_list)

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Display_front_end_connection(self, sender, e):
        """隐藏电池前端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        input_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                input_params.append(obj)
            elif 'Params' in dir(obj):
                for _input in obj.Params.Input:
                    input_params.append(_input)

        for _index, item in enumerate(input_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.hidden

        doc.NewSolution(False)
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Display_backend_connection(self, sender, e):
        """隐藏电池后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        output_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                output_params.append(obj)
            elif 'Params' in dir(obj):
                output_params += [_ for _ in obj.Params.Output]

        output_params = list(chain(*[list(_.Recipients) for _ in output_params]))

        for _index, item in enumerate(output_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.hidden

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Both_Display_connection(self, sender, e):
        """同时隐藏电池前后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        input_params = []
        output_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                input_params.append(obj)
                output_params.append(obj)
            elif 'Params' in dir(obj):
                input_params += [_ for _ in obj.Params.Input]
                output_params += [_ for _ in obj.Params.Output]

        output_params = list(chain(*[list(_.Recipients) for _ in output_params]))
        total_params = input_params + output_params

        for _index, item in enumerate(total_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.hidden

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Show_front_end_connection(self, sender, e):
        """显示电池前端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        input_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                input_params.append(obj)
            elif 'Params' in dir(obj):
                for _input in obj.Params.Input:
                    input_params.append(_input)

        for _index, item in enumerate(input_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.default

        doc.NewSolution(False)
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Show_backend_connection(self, sender, e):
        """显示电池后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        output_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                output_params.append(obj)
            elif 'Params' in dir(obj):
                output_params += [_ for _ in obj.Params.Output]

        output_params = list(chain(*[list(_.Recipients) for _ in output_params]))

        for _index, item in enumerate(output_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.default

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()

    def Both_Show_connection(self, sender, e):
        """同时显示电池前后端连线"""
        doc = Grasshopper.Instances.ActiveCanvas.Document
        selected_objects = [obj for obj in doc.SelectedObjects() if isinstance(obj, Grasshopper.Kernel.IGH_ActiveObject)]  # 获取选中的电池

        input_params = []
        output_params = []
        for obj in selected_objects:
            if 'RemoveAllSources' in dir(obj):
                input_params.append(obj)
                output_params.append(obj)
            elif 'Params' in dir(obj):
                input_params += [_ for _ in obj.Params.Input]
                output_params += [_ for _ in obj.Params.Output]

        output_params = list(chain(*[list(_.Recipients) for _ in output_params]))
        total_params = input_params + output_params

        for _index, item in enumerate(total_params):
            item.RecordUndoEvent('Display Wire')
            item.WireDisplay = Grasshopper.Kernel.GH_ParamWireDisplay.default

        Rhino.RhinoApp.Wait()
        doc.NewSolution(False)  # 刷新GH画布
        Grasshopper.Instances.ActiveCanvas.Refresh()


class CreateMenu(object):
    def __init__(self):
        self.reload_ico = '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'
        self.website_ico = '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'

    def _CreateMenu(self, canvas):
        # 创建菜单
        Grasshopper.Instances.CanvasCreated -= self._CreateMenu
        _toolbar = Grasshopper.Instances.DocumentEditor.MainMenuStrip
        HAE_ = System.Windows.Forms.ToolStripMenuItem("HAE-Facadehub2.0")
        _toolbar.Items.Insert(6, HAE_)  # 创建菜单

        _toolbar.ShowItemToolTips = True

        # 下面是创建二级菜单
        Reload = System.Windows.Forms.ToolStripMenuItem("Reload")  # 添加重启按钮
        HAE_.DropDownItems.Add(Reload)  # 创建子菜单
        Reload.Image = System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(self.reload_ico)))  # 添加图标
        Reload.Click += System.EventHandler(self.reload_gh)  # 添加点击事件
        Reload.ToolTipText = "Reload Grasshopper\nPowered by HAE Development Team"  # 添加提示
        Reload.AutoToolTip = False

        Open_Web = System.Windows.Forms.ToolStripMenuItem("View the HAE official website")  # 添加公司官网
        HAE_.DropDownItems.Add(Open_Web)  # 创建子菜单
        Open_Web.Image = System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(self.website_ico)))  # 添加图标
        Open_Web.Click += System.EventHandler(self.open_webpage)  # 添加点击事件
        Open_Web.ToolTipText = "Open the HAE official website\nPowered by HAE Development Team"  # 添加提示
        Reload.AutoToolTip = False

    def reload_gh(self, sender, e):
        # 重启事件
        btn = Rhino.UI.ShowMessageButton.YesNo  # 添加YN的按钮
        icon = Rhino.UI.ShowMessageIcon.Warning  # 添加图标
        dlg_result = Rhino.UI.Dialogs.ShowMessage("Are you sure you want to restart?", "Reload", btn, icon)  # 添加弹窗

        if dlg_result == Rhino.UI.ShowMessageResult.Yes:
            Grasshopper.Plugin.Commands.Run_GrasshopperUnloadPlugin()
            Grasshopper.Plugin.Commands.Run_Grasshopper()

    def open_webpage(self, sender, e):
        # 跳转网页事件
        url = "https://heroesae.com/"
        wb.open(url)
