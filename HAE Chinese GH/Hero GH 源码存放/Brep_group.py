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

Result = initialization.Result
Message = initialization.message()

try:
    if Result is True:
        # Brep切割
        class BrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Brep切割（高精度）", "RPP_BrepCut",
                                                                   """Brep切割，精准度最高，会输出未相交以及切割失败的Brep""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "A_Brep", "A", "待切割的Brep（被切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "切割的Brep（切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差，默认0.01")
                Tolerance = 0.01
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Breps", "B", "切割出来的Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Disjoint", "D", "不相交的切割体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "False_Breps", "F", "切割失败的切割体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANDSURBVEhL1ZTJTxNhGMaN8egFjUv8EzwYL8YYTUwkmvkHvLsFtYSKgiIqIRjFIDFW+gGSEqTQhXY63ZnOtJTSBYoBBUFADy6JSxokgDKktFN8/ArjEsV6AGN8k18mmcPzm2fe5F0XCh3cMDN47FByWMXM9hUwUkTFSCFKoIiRhPPLeEsZyXWZSXIUy1UmaaK0VTKyqZqB8Vbeulxj0R3ZNDd0KonX54HxYmC0BHhcCgxcAuLlQOwK0FMBBCsB8TrA3wDc1YCzhj41SGjLDytRK4/uTlZwcgrjhVgYVCH1sAipXjXSkWKku0sgB0oh+8oge8uRcV1FhqvAorUSn81UZq3BW83FfCVq5VEEHz6PFSI5oMJCfxEWYmqkwsVIBUuQ9pcizZchTQWykwpsFchYKrGYFVjWSuC7BNmzLJBpgyWBaS0Ff70B/71Bdgdr2ICGixeQ8tCFO6iMvQi5gy7cQBfedg0w3MBU1fG9StTKk1PgVyMZu43MCx8yz71YnOjE4lgWfgk8ExHlnRGWdbBOh5tzOz2cx8NzfKfARUIxTvQFanMKFkQVpP56QHoFzE4AH39ibgID8Sh8QhCh7jDCPVFEI73ojcUxMvwUAu9/+QdBIaS4loY/A6ae/Mr0CMJBAazNCbfLC6+HB/16CD4/YpE++DrF4f9A0CXAyv7LBtrq/M3S8KlPeHGOHjo1MESP3sAFoJ8evJ5zkAcb6DKfAzOjCiPL0HDMjiJCBTkbNNw6kDcZPzY2/+h0YjpakJjuOZuYDp5NzIiFiY/eM+8mw5rZ+cQo5t4MQvrK2yyPMP/+MUIBX+4GdNbn79mxed+ubVsP7N6+5UdUR3durK2pLbHZXGg3mGE0WmAys7BYOLBWO+w02G53weFw5xTknHuk+YTF6sQDvRH6djPaFUlHh21JwnHO1Qm02vsF2X+sbzPRFh0wmKww0/BsCxvrWCuB65vAqAisimDVv+j/b0DIfbUghmB3eOFy83B7BXTyfhoSgF/sRldXCN0/Hbp430M8HRnPHrvXSszvp6rq5v76Rh25c7eO3NUQoqmrJ3WkkdSTJtJI3zc16YhO10yam1tIS0sraW3VE72+ndisdmJoM5R9AXhmdNkT9EQjAAAAAElFTkSuQmCC"
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

            def tr_object(self, origin_brep, transform):
                wxy_origin_breps = []
                for _ in origin_brep:
                    _.Transform(transform)
                    wxy_origin_breps.append(_)
                return wxy_origin_breps

            def _second_handle(self, set_brep_data):
                passive_brep, cut_brep = set_brep_data
                res_brep, no_inter_set_tip, fail_set_tip = [], [], []
                count = 0
                brep_center = passive_brep.GetBoundingBox(False).Center
                center_to_worldxy = rg.Transform.PlaneToPlane(ghc.XYPlane(brep_center), rg.Plane.WorldXY)
                worldxy_to_center = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ghc.XYPlane(brep_center))
                passive_brep.Transform(center_to_worldxy)
                new_cut_brep = self.tr_object(cut_brep, center_to_worldxy)
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
                no_inter_brep = [cut_brep[_] for _ in no_inter_set_tip]
                fail_brep = [cut_brep[_] for _ in fail_set_tip]
                passive_brep.Transform(worldxy_to_center)
                [_.Transform(worldxy_to_center) for _ in no_inter_brep]

                return passive_brep, no_inter_brep, fail_brep, no_inter_set_tip, fail_set_tip

            def tree_match(self, temp_data):
                a_set, b_set, origin_path = temp_data
                new_b_set = [copy.deepcopy(b_set) for _ in range(len(a_set))]
                temp_brep = zip(a_set, new_b_set)
                res_brep, res_no_inter_brep, res_fail_brep, no_inter_tips, fail_tips = zip(*map(self._second_handle, temp_brep))
                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_brep, res_no_inter_brep, res_fail_brep])
                Rhino.RhinoApp.Wait()
                return ungroup_data, no_inter_tips, fail_tips

            def RunScript(self, A_Brep, B_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = sc.doc.ModelAbsoluteTolerance if Tolerance is None else Tolerance
                    Res_Breps, Disjoint, False_Breps = (gd[object]() for _ in range(3))
                    _a_trunk, _a_trunk_path = self.Branch_Route(A_Brep)
                    _b_trunk, _b_trunk_path = self.Branch_Route(B_Brep)
                    _a_tr_len, _b_tr_len = len(_a_trunk), len(_b_trunk)
                    _copy_b_trunk = copy.deepcopy(_b_trunk)

                    re_mes = Message.RE_MES([A_Brep, B_Brep], ['A_Brep', 'B_Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if _a_tr_len == _b_tr_len:
                            new_a_trunk = _a_trunk
                            new_b_trunk = _b_trunk
                            new_trunk_path = _a_trunk_path
                        else:
                            if _a_tr_len < _b_tr_len:
                                new_a_trunk = _a_trunk + [_a_trunk[-1]] * (_b_tr_len - _a_tr_len)
                                new_b_trunk = _b_trunk
                                new_trunk_path = _b_trunk_path
                            else:
                                new_a_trunk = _a_trunk
                                new_b_trunk = _b_trunk + [_b_trunk[-1]] * (_a_tr_len - _b_tr_len)
                                new_trunk_path = _a_trunk_path
                        zip_list = zip(new_a_trunk, new_b_trunk, new_trunk_path)
                        temp_iter_ungroup, dis_tips, fail_tips = zip(*ghp.run(self.tree_match, zip_list))
                        iter_ungroup_data = zip(*temp_iter_ungroup)
                        Res_Breps, Disjoint, False_Breps = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                        for f_disjoint_index in range(len(dis_tips)):
                            for s_disjoint_index in dis_tips[f_disjoint_index][0]:
                                self.message2("第{}组数据：下标为{}的切割体未相交！".format((f_disjoint_index + 1), s_disjoint_index))

                        for f_fail_index in range(len(fail_tips)):
                            for s_fail_index in fail_tips[f_fail_index][0]:
                                self.message1("第{}组数据：下标为{}的切割体切割失败！".format((f_fail_index + 1), s_fail_index))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Breps, Disjoint, False_Breps
                finally:
                    self.Message = 'Brep切割'


        # Brep切割（Fast）
        class FastBrepCut(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Brep切割（Fast）", "RPP_BrepCut",
                                                                   """Brep切割，优化时间效率（出现不稳定情况~正常报错），会输出未相交Brep（若要输出切割失败物体，请使用RPP-Brep切割（高精度））""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "A_Brep", "A", "待切割的Brep（被切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Brep", "B", "切割的Brep（切割体）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "容差，默认0.01")
                Tolerance = 0.01
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(Tolerance))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Res_Breps", "B", "切割出来的Brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Disjoint", "D", "不相交的切割体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQOSURBVEhLrZVLbBtlFIVDu0IskBBL9iy7QxHqmlXLqiwIxW1RF7QB59U2JA6kpYIWGokKcGjsPOv4MdOxPZ7J2OP3K04cpyl51c7DpKROBI2KQxvH9dgOhz/xCCVplMQSRxrN5v73+8/VPTMVh1XmwbljxfkaRWbogiITqFFk3XWKrHBJIbHNColuURTZ7xXr2tZ35PLylR79pA2rTUDiEjDeCIyqgMGrgP86IN4AAu1Y62ztlcvL11+xc9fxqA656GfIhWogeRuQdzSiwDWjwHwF8G3IdF1Vy+Xl60AA14ZsZ+vPcnn52hMgNKBgvYKCqRlgbyJ7p/m2XF6+tgOkoBI5L2k8x2NjwYuNeQ+wGMRC1LFM0ayftwkBp+gOOB0un3z8YO0GZD1XUPxzDHg+C/wdB9Zn8PtMDLzght8XRGRwGOFgBPLxg7Ub8GITsBwF0tPA0wng2TTmJ8Kg7rEY4O1wOT1wiZ6ifPxgpWNnv8MKWc/JOrKiDUCkBXgSIw7I7VeniIM4fpsaBBnRNoC7BKDpD47u96C19chy6IxyPf55Ih34NPHMffHh04G62ZVEsJheHEP6UQyrqTFMxgKgGdtOB0+ip48Vpi8kc7HqZDakTOY8dUlJvJzMc18k80xLcsP8TVLqveYm9zi67Xnlrcr33tBo767oDQz6+ymYTAzukfGwLL/TwVLk9LtYUAJTtcD9emCIjCFAUuoiuz3wNWC/BQJIkaY71NBw6zVtp27FYGSg19OgTGYwzG4AcZAKf1S58fAipFGy34NKSL565J1kBfkmFMxfAtZvNwFzpOeRUuuSGhsbX+/s1q0YSWODgQZNbQJshwQ46kmASIgo4oa+BkmjmpH7/qfKU5WvdnXrNgSyljwvwuFww+Xyw+cLIRyKYCQ6iuHICF4GeGuRD91AIaJG0d8OBDuRFTqWKcr8vs0mnOA4+8mh8NBJSke9/cOP7Ur1L1qVWt2h6iBvrbZH1dXVp+rr06mMekplMpiaXgK8cFZDmuWAzEIpQGtxZP6YgCh64fX4EQyEMT0Vh50Xa2Uz+2tPQMJKms+UArQ6ieeP78Ni4cDZBNgFESPDoxA4R7XcYn9tAv4hgDwBSASQ2xcwsAWIDscOD1gMf3gcj8mKJkg6xy+TnwhZ1QWejGiOQEhC16aRXX6wC1CGA7/+xJtzYlVVwvpxVYI6W5Uynz/lsfRFI0EfAm4BYZ+IoMcJq5UDz5VGVJaDvXT7p+5+g4lFd68BOh0No9GyC1CGg72k0fTQjJknCaVKCSWfgP8VoNX2svyAa+vbYrXypLEDdrtzK52bqzr+6yQE3lEjl5cvtVpzx2A0L/X09qf67xpTRgOdoigmZWHYlI3lUiQLSzYLf0Yu30cVFf8CBoYWjQuZXXMAAAAASUVORK5CYII="
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

            def tr_object(self, origin_brep, transform):
                wxy_origin_breps = []
                for _ in origin_brep:
                    _.Transform(transform)
                    wxy_origin_breps.append(_)
                return wxy_origin_breps

            def _first_handle(self, passive_brep, cut_brep):
                res_temp_brep = []
                brep_center = passive_brep.GetBoundingBox(False).Center
                center_tr_one = rg.Transform.PlaneToPlane(ghc.XYPlane(brep_center), rg.Plane.WorldXY)
                center_tr_two = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ghc.XYPlane(brep_center))
                passive_brep.Transform(center_tr_one)
                new_cut_brep = self.tr_object(cut_brep, center_tr_one)
                res_temp_brep = rg.Brep.CreateBooleanDifference([passive_brep], new_cut_brep, self.tol)

                res_temp_brep = [_ for _ in res_temp_brep] if res_temp_brep else None
                if res_temp_brep:
                    area = [_.GetArea() for _ in res_temp_brep]
                    max_index = area.index(max(area))
                    res_temp_brep = res_temp_brep[max_index]
                    res_temp_brep.Transform(center_tr_two)
                return res_temp_brep

            def _collision_brep(self, set_breps):
                bumped_brep, coll_brep = set_breps
                inter_brep, no_intersect_set_tip = [], []
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

                return res_brep, no_inter_brep, no_intersect_set_tip

            def tree_match(self, temp_data):
                a_set, b_set, origin_path = temp_data
                new_b_set = [copy.deepcopy(b_set) for _ in range(len(a_set))]
                temp_brep = zip(a_set, new_b_set)
                res_brep, res_no_inter_brep, no_inter_tips = zip(*map(self._collision_brep, temp_brep))

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [res_brep, res_no_inter_brep])
                Rhino.RhinoApp.Wait()
                return ungroup_data, no_inter_tips

            def RunScript(self, A_Brep, B_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    self.tol = sc.doc.ModelAbsoluteTolerance if Tolerance is None else Tolerance
                    Res_Breps, Disjoint = (gd[object]() for _ in range(2))

                    _a_trunk, _a_trunk_path = self.Branch_Route(A_Brep)
                    _b_trunk, _b_trunk_path = self.Branch_Route(B_Brep)
                    _a_tr_len, _b_tr_len = len(_a_trunk), len(_b_trunk)
                    _copy_b_trunk = copy.deepcopy(_b_trunk)

                    re_mes = Message.RE_MES([A_Brep, B_Brep], ['A端', 'B端'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        if _a_tr_len == _b_tr_len:
                            new_a_trunk = _a_trunk
                            new_b_trunk = _b_trunk
                            new_trunk_path = _a_trunk_path
                        else:
                            if _a_tr_len < _b_tr_len:
                                new_a_trunk = _a_trunk + [_a_trunk[-1]] * (_b_tr_len - _a_tr_len)
                                new_b_trunk = _b_trunk
                                new_trunk_path = _b_trunk_path
                            else:
                                new_a_trunk = _a_trunk
                                new_b_trunk = _b_trunk + [_b_trunk[-1]] * (_a_tr_len - _b_tr_len)
                                new_trunk_path = _a_trunk_path
                        zip_list = zip(new_a_trunk, new_b_trunk, new_trunk_path)

                        temp_iter_ungroup, dis_tips = zip(*ghp.run(self.tree_match, zip_list))
                        iter_ungroup_data = zip(*temp_iter_ungroup)
                        _res_breps = zip(*iter_ungroup_data[0])[0]

                        for f_disjoint_index in range(len(dis_tips)):
                            for s_disjoint_index in dis_tips[f_disjoint_index][0]:
                                self.message2("第{}组数据：下标为{}的切割体未相交！".format((f_disjoint_index + 1), s_disjoint_index))

                        for _f_res_index in range(len(_res_breps)):
                            if not _res_breps[_f_res_index]:
                                self.message1("第{}组数据切割失败：请调用RPP-Brep切割（高精度）插件查看！".format(_f_res_index + 1))

                        Res_Breps, Disjoint = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Res_Breps, Disjoint
                finally:
                    self.Message = 'Brep切割（Fast）'


        # Brep结合
        class Brep_Union(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-结合", "RPP_Brep_Union",
                                                                   """将多个Brep结合成一个.并消除参考线""",
                                                                   "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "Breps", "B", "Brep物件，Tree类型数据")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "PRE", "P", "合并精度[0.00-1.00].成功情况下不改动")
                PRE = 0.01
                p.SetPersistentData(gk.Types.GH_Number(PRE))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "结构之后的Brep")
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

            # brep结合
            def brepbp(self, Breps):
                Result = rg.Brep.CreateBooleanUnion(Breps[0], Breps[1])
                Merge_Result = []
                for Re_ in Result:
                    Re_.MergeCoplanarFaces(0.02)
                    Merge_Result.append(Re_)
                return Merge_Result

            def RunScript(self, Breps, PRE):
                Brep = gd[object]()
                PRE = PRE if PRE else 0.02
                if Breps.BranchCount == 0:
                    return Brep
                if Breps.BranchCount > 0:
                    breplist = zip([tb for tb in Breps.Branches], [PRE] * Breps.BranchCount)
                    res = ghp.run(self.brepbp, breplist)
                    Brep = ght.list_to_tree(res)
                return Brep


        # 合并以及封面
        class Seam_Merge(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-封面合并", "RPP_CoverMerge",
                                                                   """封面以及合并曲面""", "Scavenger", "Brep")
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
                self.SetUpParam(p, "Suface_Or_Brep_List", "M", "面以及Brep数据列表")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "封顶缝合以及共面")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJrSURBVEhL7VbfS1NhGPbfifBH0XX3QRQdU8ouishsTTnNublja2oiUWbdfAV2YRKUFuKs1ZaK021u/jZlVCBEKM2Ugmx5dr7zbe7pTY5g5JnSVYEPPBcv5/A8fOd7n/e8eam3F0qzCzLj0xbGxy8zHqtkPCwzfdjG9EE70/sdTPc7me5zsbTXzdLd19h6Vz1b72xkWe9dlu1oOpyXC2r8Ygd+uIAPNmC+BnjnBOJUv6kDptzAmAeINgKhJiDYDPTfAAI3gZctVLch095YY0htj1S8nGFBhjZtgTZhBY9VgUdk0AlAJ4Doc0D4ayF8CtK9V0EnQOZpPTKdZNp7B5mHTVZDanvsGfwHBgEXxAs3hNdD4g1Id11H5nEzMo+om7rvIXu/5awhtT1yGgw4kBo5T8+KoU2WQhs/BT56mt4pAx85AzFxDtqA5Tn31Snc51JET50inrkV0eVRxJMGJdvTquQwqIYWqEVy9gj41/3Qlgu3sADaSgFSX/Zhfa4MCFM+wpSToc2c3AJe3ab6AXYwcCI5cxR8uQjap0N/8nMRvsdKofvobkzuaM/gHzBQ4+XtWKUJOn8FeF9Nk5Qm6izVUwoQ8YDHj1HX5ENLHCQegLa0hSv5WI2V5DbQ4xWF2Y+ypE5bJHWCGKmU1GFZ4oN2SQ04paVwSV9yTkIiehyJyAkkQsVIDBGDJzf47fUlSrpimnQjbuZYm6to/fWvWBuzYi1aBTUkQw3akOq3I0WfUCcKystfG2zc0aIMPmMBn7RCH62CPiJDhGwQwZ1nlSFjDvMm2N0wNGTMsWdgyJhjd1tHw+9bh39z62jDT8ohmpsIqcR3AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Suface_Or_Brep_List):
                Brep = gd[object]()
                if Suface_Or_Brep_List:
                    # 封顶
                    Brep_List = [i.CapPlanarHoles(0.1) for i in Suface_Or_Brep_List]
                    # 封顶后列表去None的操作
                    Bool_List = [i for i in Brep_List if i is not None]
                    if len(Bool_List) != 0:
                        # 缝合以及共面
                        Brep = rg.Brep.CreateBooleanUnion(Bool_List, 0.1)
                        Brep[0].MergeCoplanarFaces(0.1)
                    else:
                        # 缝合以及共面
                        Brep = rg.Brep.CreateBooleanUnion(Suface_Or_Brep_List, 0.1)
                        Brep[0].MergeCoplanarFaces(0.1)
                return Brep


        # 分割Brep（面）
        class SplitBrepFace(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-分割Brep（面）", "RPP_SplitBrepFace",
                                                                   """面或实体切割，分割面或者实体（类似小刀平切面饼）""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Brep", "B", "待分割的Brep（面）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "分割体（平面（Plane）或者平滑的面（Surface））")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "分割的精度")
                tol = sc.doc.ModelAbsoluteTolerance
                p.SetPersistentData(gk.Types.GH_Number(tol))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                bool_cap = True
                p.SetPersistentData(gk.Types.GH_Boolean(bool_cap))
                self.SetUpParam(p, "Cap", "C", "是否封盖，默认封盖")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Result_Brep", "B", "分割出来的Brep（面）")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANQSURBVEhL7ZT7T1NZEMePxBIt8Wf/BH4wGqM/9SeNf8Fqlg3iI6IFn5cW6INHeVWjIhKzoiLRpLCu74u25VVEwFaEVrGACj4TL4HEipqtrUh7W/p1Dr0xZuOumvibTDKZm9zPzJwzM2fYj0pNWto65fP7BWALRpr/WPXcuUXz4DLp+S2asabtmrGzuZqx06R1ezWB00Uany5r5YFFi4pHHZnLXnb8NztZZ9A8rs1froRnbLBhteqtNzuAUR3kgTzInnzEuo2IdxQh7izFbHM54KzBm7rirl2MZb3xbffimR6yl9jbnDUg7jIj3qKw9mqEzpQ/UMInE4SHtON4rEOMnGLkFO8xYtZVhAQ5Ja6RU8tRhOst7TsZ2/RhOMeDF3rEfMT2cdaA2U4zEq0K6zgCudE6qIRPJgj5tRIe5SHSLyDi1iN60wC53YyYowQxsWzOKXSqtI0noMO48VSHyACxHs4WQu4wIeZU2OuHEbFV3VPCzyf4JRL09q5ZSE5BTJqAUSMwXAzcJbCvEujdD3QeInuSxrTMncNYZngkx4+pImCM2BHOWoA7FcAthb15HNFG69O54A2Mqf5asTTtdffm7Om+XCHYrhWCDrLNe4XgJUEIn9MLYZtBmD5XKYxX7c4oS03Vv7qRlTHtI8ZFbOtX2KZy4d0x48Zaxhbz3bL2uFpt2sFYxnrG1mcq+vu/dANjv+Uxlk28aw9jG/+P5f/4TevUavPcLYCKlAnP1vpgf64Y6CRt3S0G7PvEqSs6cepCgTjVZBI/XrCKkzWFFpNKtWPCs836/t5OMXDjC/YqsRc5axQ//F0hvq0vPTwXnAtvctiv/QcT1INHVFc/1ddHdb1Nde2muroOkj2B96csbi2dPjSk9SNgTvZriLOl1C9aET0K2/UnoraqZA+4zL+D+QQ/LUEALwqA+/mA10AjSuPXTePnolF1WskeQ6je0kUPKIsSeDFeSONMrI+zNLI9JbQmFLatFjO2qodKeHpofBf5tX2Jh4I00096SydFugxStN0kyfZiSb5aJiXs1VLwZEnjvpSUraHhnMuJJ3nSzACxbs4WEGuUZIfCXjskRW2VTiV8UgYHc1X4qjZ8Vnt6+pJqtbocvRULv8VyhjHGPgGPiWiG21cMagAAAABJRU5ErkJggg=="
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

            def cap_brep(self, cap_brep):
                brep_list = []
                for _ in cap_brep:
                    new_cap_brep = _.CapPlanarHoles(self.tol)
                    if not new_cap_brep or self.cap_factor is False:
                        brep_list.append(_)
                    else:
                        brep_list.append(new_cap_brep)
                return brep_list

            def sort_surface(self, new_brep_array):
                pt_list = []
                for single_brep in new_brep_array:
                    center_pt = single_brep.GetBoundingBox(True).Center
                    pt_list.append(center_pt)

                brep_sort_by_pln = self.sort_by_xyz(pt_list, new_brep_array)
                return brep_sort_by_pln

            def sort_by_xyz(self, pt_list, follow_object):
                dict_pt_data = dict()
                dict_pt_data['X'] = [_.X for _ in pt_list]
                dict_pt_data['Y'] = [_.Y for _ in pt_list]
                dict_pt_data['Z'] = [_.Z for _ in pt_list]

                zip_list = zip(dict_pt_data['Z'], dict_pt_data['X'], dict_pt_data['Y'])
                w_sort_pts = []
                for index in range(len(zip_list)):
                    w_sort_pts.append(list(zip_list[index]) + [index])
                index_list = [_[-1] for _ in sorted(w_sort_pts)]
                new_object_list = [follow_object[_] for _ in index_list]
                return new_object_list

            def _get_intersect(self, item, pln, new_brep_list, error_brep_list):
                origin_pt = [_.Origin for _ in pln]
                new_pln = self.sort_by_xyz(origin_pt, pln)
                cut_pln = new_pln[0]

                single_event = rg.Intersect.Intersection.BrepPlane(item, cut_pln, self.tol)
                if single_event[0]:
                    surface_cut = rg.Brep.CreatePlanarBreps(single_event[1])
                else:
                    return None
                cut_object = surface_cut[0] if surface_cut else single_event[1][0]
                if 'Curve' in str(cut_object):
                    temp_brep = list(item.Split.Overloads[IEnumerable[Rhino.Geometry.Curve], System.Double]([cut_object], self.tol))
                else:
                    temp_brep = list(item.Split.Overloads[IEnumerable[Rhino.Geometry.Brep], System.Double]([cut_object], self.tol))
                cap_brep = self.cap_brep(temp_brep)
                cut_off_breps = self.sort_surface(cap_brep)

                new_brep, rest_brep = cut_off_breps[:2]
                new_pln.remove(cut_pln)
                new_brep_list.append(new_brep)
                error_brep_list += cut_off_breps[2:]

                if new_pln:
                    return self._get_intersect(rest_brep, new_pln, new_brep_list, error_brep_list)
                else:
                    new_brep_list.append(rest_brep)
                    res_breps = self._handle_brep(new_brep_list + error_brep_list)
                    return res_breps

            def _handle_brep(self, breps):
                for brep in breps:
                    if brep.SolidOrientation == rg.BrepSolidOrientation.Inward:
                        brep.Flip()
                return breps

            def temp(self, tuple_data):
                breps, planes, origin_path = tuple_data
                list_pln = [planes[:] for _ in range(len(breps))]

                res_list = []
                for brep_index, brep_item in enumerate(breps):
                    res_list.append(self._get_intersect(brep_item, list_pln[brep_index], [], []))
                ungroup_data = self.split_tree(res_list, origin_path)
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Brep, Plane, Tolerance, Cap):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result_Brep = gd[object]()

                    trunk_list_brep, trunk_list_path = self.Branch_Route(Brep)
                    trunk_list_plane = self.Branch_Route(Plane)[0]
                    self.tol = Tolerance
                    self.cap_factor = Cap
                    len_b, len_p = len(trunk_list_brep), len(trunk_list_plane)

                    if not (trunk_list_brep or trunk_list_plane):
                        self.message2("B端实体、P端平面未输入！")
                    elif not trunk_list_brep:
                        self.message2("B端实体未输入！")
                    elif not trunk_list_plane:
                        self.message2("P端平面未输入！")
                    else:
                        if len_b != len_p:
                            new_brep_list = trunk_list_brep
                            new_plane_list = trunk_list_plane + [trunk_list_plane[-1]] * abs(len_b - len_p)
                            new_plane_list = ghp.run(lambda li: [copy.copy(_) for _ in li[:]], new_plane_list)
                        else:
                            new_brep_list = trunk_list_brep
                            new_plane_list = trunk_list_plane

                        origin_list = zip(new_brep_list, new_plane_list, trunk_list_path)
                        trunk_list_res_brep = list(ghp.run(self.temp, origin_list))
                        Result_Brep = self.format_tree(trunk_list_res_brep)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    Rhino.RhinoApp.Wait()
                    sc.doc = ghdoc
                    return Result_Brep
                finally:
                    self.Message = '平切Brep（面）'


        # 圆柱切割体
        class CirBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-开孔圆柱",
                                                                   "RPP_CirBrep",
                                                                   """根据置顶Plane生成圆柱切割体""",
                                                                   "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "Plane", "P", "参考平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "圆柱半径")
                p.SetPersistentData(gk.Types.GH_Number(5))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "HoleCir", "H", "长圆孔总长")
                p.SetPersistentData(gk.Types.GH_Number(20))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "CriVec", "CV", "延伸方向大小")
                p.SetPersistentData(gk.Types.GH_Vector(rg.Vector3d(0, 0, 20)))  # 为参数设置缺省值
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "CirBrepList", "CB", "圆孔切割体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "HoleCirBrepList", "HG", "长圆孔切割体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAICSURBVEhLYxj+4N/HJ8IvLm0Uv3tpGVb8+cUe8f///7NClRMPgJrYTq90mHd6nsT7w9MFPx9Cw4enC3w+NJX/67GZwp/PL1G7dW1foT1UK3Hgyo40j2tLef8fnsjw/9Akhv+HkfAhoNjJ6Qz/j8zg/H9iGsP/C7MZ/p9YpHcGqpU4cGqVa8S5uWz/909gwMAnpzP9Xz9Rfe20aQm2GyfIHwVZcGSO3DWoVuLAmdUeoWfnsmO14Owc1v/zpwQlgNQtm2jden0hw/+jcxQugTUSC/BZcGQyw//t/YLP10zSXrJzAt/n06DgoqYF+/qBLp7C8P/cLEicHJtKAwtAhp6Zzfz/KNA3x4CWUdUCkIFbJ8leXtpvVrp9osjDszOpbMHZucBInh4TDVK3fLJjw41FVI7k49MY/2+cIHNs0QTb5K0TJW6fo7YPQHFwHBgHp2axgiOb6nEAT0XADEaTVATKB9v6BZ6unqC1iCb5AJSTF04OiAepW0KLnAwqi9ZN1lg/c2ai/SZgWXQRXBaRaAG+wm4/KKMBU9KhaTzIkUxaYXdxZ6rntSW84KIZFz4CjOCDQPriHGCqWqB9GqqVOHDr3z/20yvsFp2ZL/X58AyRH4emC2PFR2eK/ji/ROXu9d3ZDlCtpIEvL69IPLm8Xvb2qeVY8dvbO2T/AR0DVT7sAAMDAMIBR1n7It7KAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

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
                    Surface_Hold = HoleCir.Faces[0].CreateExtrusion(rg.Line(C_Plane.Origin, Cri_Vec).ToNurbsCurve(),
                                                                    False)
                    HoleCirBrep = Surface_Hold.CapPlanarHoles(0.02)
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

                    re_mes = Message.RE_MES([Plane, Radi], ['Plane', 'Radi'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        # 将标量值转换为列表，方便与Plane进行zip
                        Radi = [Radi] * len(Plane)
                        CriVec = self.data_polishing_list(Plane, CriVec)
                        HoleCir = [HoleCir] * len(Plane)

                        # 使用ghpythonlib.parallel.run并行计算 这里使用run函数并行计算多个圆柱体的生成
                        Geometry = ghp.run(self.circle, zip(Plane, Radi, CriVec, HoleCir))
                        # 解包结果
                        CirBrepList, HoleCirBrepList = zip(*Geometry)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return CirBrepList, HoleCirBrepList
                finally:
                    self.Message = 'HAE 切割圆柱'


        # 不规则几何物体最小外包围盒(3D)
        class GenerateMinBox3d(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-最小外包围盒（不规则3d）", "RPP_GenerateMinBox3d",
                                                                   """通过点阵列生成不规则几何物体的最小外包围盒（3d）""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Pts", "P", "点阵列、点集（建议去重）")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Count", "C", "迭代次数，默认为18（建议15~18之间）")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Integer(18))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Box()
                self.SetUpParam(p, "BBox", "B", "最后生成的包围盒")
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
                curr_vol = curr_bb.Volume

                tot_ang = math.pi * 0.5
                factor = 0.1
                max_passes = 20

                """-------时间进度消耗最多（并行迭代）-------"""
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
                    curr_bb = sub_bbox_list[sub_min_index]
                    vol_diff = prev_vol - curr_vol
                    if vol_diff < sc.doc.ModelAbsoluteTolerance:
                        break
                """-------分割线-------"""
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
                    self._global_tol = sc.doc.ModelAbsoluteTolerance
                    self.tot_ang = math.pi * 0.5

                    BBox = gd[object]()
                    trunk_list = [list(_) for _ in Pts.Branches]

                    re_mes = Message.RE_MES([Pts, Count], ['Pts', 'Count'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        pts_cloud = ghp.run(lambda pts: rg.PointCloud(pts), trunk_list)
                        BBox = map(self.min3dbox, pts_cloud)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return BBox
                finally:
                    self.Message = '最小外包围盒（不规则3d）'


        # 映射以及挤出
        class MappingExtrusion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-映射及挤出", "RPP_Mapping&Extrusion",
                                                                   """映射一个物体到指定平面，之后通过线段或者向量来挤出实体""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Geometry", "G", "闭合曲线或者曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Origin_Plane", "A", "原始的平面")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Plane(rg.Plane.WorldXY))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "B", "转换到的平面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Mode", "M", "作为挤出的向量")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Geometry", "G", "新的几何物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Transformed_Objects", "T", "平面转换后的物体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASuSURBVEhL5VZLUFtVGGbhxhm3jqPjQkfcOK0r9+6cUWd01alASwshTUoeTUII4VHSEJLSWLDDWBctQgivAC2QpLSUVyqtFMIjhApFbNXWaqvV1DTJvffc1+cJuSOdcVPapd/MN2cm+c/3ff/NyX9u3vPgUezIG/KGyStcpbxo90qDDq/U7fJKfpdXznLgZItS+mxIzpUH8GctsFoNzDqB8SYg1AwEKS+0AoETUEp3Dm5Z8w5ZMUokpgeZMYG/VAXxXD3E7gaIXQ3A4OcQ/K4epXznyES1/bhlRWah/D8GCHgg+hv+IH0ulVK+M6RWtLv4Vb1MlgzILOpArhjBj9q2Dc55IfQ62kjAuUfZsjMwi4cGcduCTFSHzJIO3KQO/IgF4vl6oN8Dodv5OxmxF5GeYyXKlqdHakn1Lr+mk/lYOX08+lwH0wbwYWvO4LwXfP/Rs1y48hO2p6FM2fb0YGLqEO5ZIMVp6pgRQtwAeeYIcMkGjLoh9jgfkDFbIQnaC3ZskFql6de1CRLTJrjF8r8yUX2CdpDgpgwJPlSRkEOuBBmqPZ2ZNn1KgtX7dmxwZ970HhvT6dgZYwmZtBx8HLJr0zNmdTqsV5NBq5oM16uSU9ZiMmYpeiaDW7Pm3eno4RImcqRAnKjcmw7WHkhGKvYzF4z7SD9dR+qLkuO2kucwsO1OL+jKmBnjPnHcWpgO15QmI5aDTNh4gAzQdaSuODlRWfo/NlhbNr6dXNYUM1eNheKEpSgdspekIpUFTFBfQPrNhSRUv/fv6coiMm7ZQy7Y95DuY/uVrdsAHC/IP5jz2Qhl0J7P+h358lnPFu9fqvmY+9ZcR79Tk8sVn2U7YK5ZbNyo0cafs9r4YYc1Haq28yG7hR+oq+AD7jpFdhup1bIT8qZZ4qbMEh+qloRepyR2uCk9kjDgloRwTYqfNpcLo7YP2WsGnxw3ydyYSebP22TS55Q5n1sWfY2y5PfIYleToMjmkF5Xv8qtazK4YYT0jRW4WEcnowvoPE6ZnfUnwY7Zgtz18o/IRMUBdkmTwIoJwjj9Z4/YIfW7IGbrOj3AcCukjsYuRTqH9KrqC/xmBBulI3jaAoTtQK8D6Mia0BEccD4mUXWpPHX4A2le04VbenDzBpDLZghDVeD7GsD7aBj/cUjdTYLs9+Qr0nS+3yx9jVs/xAgbGrDZGU8N7oXd+LmvBXc7T+HB4BmsDbaMzy7XFa9E3IbNaNWjjRUH+Hk67J4wID6afugUhHZXhyKdQzquas2mZ1bV4BSD78LNWAx8hXjga8z52+67JgaKxmabTYuzjsnv1xpxdc4Nfo4aTFZADNaA722A1HUCcncTz/pcbynSNH287HWans2mZ26o/+0A4Sqg5ygdwS2Q2xz0g5dfkhdKVFJc9RDrtNOYFmSOXplT1CCUNaD38lAr5PbGNkU6B/rsv9xKT8WfNKAnht6tHkg+z0O5ufnF69erX0ktq4dxWw92RQMuRvmEgTTQCKHLS+gbxZuKdF4eWdfuwh09cJ/O9F8MOW7SsItU/Ar9cadPQ2xvrM7W3p01v58Vx68m4Cda/yNdb9LTtkBPW4TWRk6Dafec2RLeQl7eP3k9Ca1oMJ2oAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

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
                if curve:
                    mode_brep_list = [_.CreateExtrusion(curve, True) for _ in object.Faces]
                    mode_brep = rg.Brep.JoinBreps(mode_brep_list, 0.001)[0]
                    return mode_brep
                else:
                    return None

            def RunScript(self, Geometry, Origin_Plane, Plane, Mode):
                try:
                    re_mes = Message.RE_MES([Geometry, Origin_Plane, Plane], ['Geometry', 'Origin_Plane', 'Plane'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        Transformed_Objects = self.get_new_brep(Geometry, Origin_Plane, Plane)
                        if Mode:
                            line = rg.Line(rg.Point3d(Mode), Mode) if type(Mode) == rg.Vector3d else Mode
                            mode_line = line.ToNurbsCurve()
                            New_Geometry = self.exturde_brep(Geometry, mode_line)
                            return New_Geometry, Transformed_Objects
                finally:
                    self.Message = 'HAE 映射及挤出'


        # 多边曲面偏移
        class BrepOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-多边曲面偏移", "RPP_BrepOffset",
                                                                   """根据折线生成偏移曲面；输入端D和V输入一个端口数据即可。""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Brep", "B", "多边曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "偏移距离")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "各分线段各自的偏移方向")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                self.SetUpParam(p, "Tolerance", "T", "精度")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "New_Brep", "B", "偏移后的Brep")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAP0SURBVEhLtZNdTJNXGMc7pxdmN0t2swuX7Ho3S4ws3hii44IQSMYUgy7bZKBOEAU2QChtpaUtbWn5WAWiI7iBgB2Ikqk4LAUUhraUfkiRtmgDyJAvs4ELLe97/juFEzsDBLqPX/Kkzds+v//pc54K/k9q4+Kj2dv/lt7IlNj+vV93N+9L9LJH/x6JQLLNFp+WaI5J/XUgKhWufWdgiDycwT7+5/Qdytw5ejw7ZeSzTLvncBYcseno3X8CdyOO/VGcHr2LfS18nkokb7/IF2VMZuR5ZtKEGP3iW1g+SUVf9EkMRqXB+FFSI/tqeCzqJe8u6YpEC7LCiUChHNNZQowk05MfOfMqYODjVJgiksO7YJQq3+f1StWyXjmHKh1eyqWYzMmHLz3ntYCBmDSYIpPHLIITOwQQbGftG7OkkX/AVygquQr5ImrKgAsqLGqkmDsvXjdgOC4D3ftTSoK9u8YEO1ck60FUkj18uayOLy8K4JIWqFAgUFYEf7l8wwDrp6dhjjru76duplkfohano1IFVGuAMhm4UimWS2WbBjjiTuH+0dwJ058ksXeOHLk1OfslU74O0YhdqCwGry0Ep6O1xQDLgc9x33APFgAjtLomlz1MGYJoCz4MnhpUHE6AMyEV5qPfoNO7AOMUgdUP3B3n1v7R6HhkqFaDaM+HFxCbhD5tA36ZB0zPCIwTnL97grzHtKtAgDeIWjSE7+ThBXyVCeehUzDe86H9N6CPhrR7Ax1MG4Juzm6USQEq33LA6WyMHjwGa44Wt8aB208I+l4AN71cEtOG4FUFSlTR7SmRbCFAhOmzmRg7eRaD0ko0POxFm4/DnadU7uEWOibIO0y7CiSSbaRY+BjlRZsE0FLk43dhLkZKL8HY6cYNKr3im0fbsB9dU8ANF9fMtCGIRhQBKgrKNwpASQF9LsZ4zWV0mdxo8QAt3qAQaBh+jlZXAMZnwHXXcjzThqCnVwd3HxrxmgBo8mkJMVV7GT3dbhiGAQNd9GtOnhaHVifBlaFZtLkJrjm46Ts28hbTroKEhDeJUuhZueC/BUCVB6jz8LymBj2dj9H0CGgcAprtPJpt3KtqsRHUOWZwe4z+okH+e6YNQYole1fGo6byYEDxOVq5mLl4ET0dLjTYgXoncNXKw2Dl1tRPVuAH+yyuB0dmIQeYNgRRCHXQKwFFDq1szFZXoaf9EeqDjTZ6agtBk5lH4wbVZKZ34FrCj+aXPosFO5h2Fbo924k06wlUuZi7oEfPz3bU0YZaKq9/QLfjAb9pNfTTsY3SnofzWqYNsaQ4F4OmqxjsGkML3YYmN708OudWOu/W4OsWqo32Geh4dA7HHqZlCAR/AcjfanxY7dq3AAAAAElFTkSuQmCC"
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

            def polyhedral(self, obj, set_line, vector, acc):
                surface = []
                if len(vector) == 1:
                    surface = [rg.Surface.CreateExtrusion(set_line[i], vector[0]) for i in range(len(set_line))]
                elif len(vector) > 1 and len(set_line) == len(vector):
                    surface = [rg.Surface.CreateExtrusion(set_line[i], vector[i]) for i in range(len(set_line))]
                for i in surface:
                    obj.Join(i.ToBrep(), acc, True)
                return obj

            def offset(self, obj, distance, acc):
                new_obj = rg.Brep.CreateOffsetBrep(obj, distance, True, True, acc)[0][0]
                return new_obj

            def RunScript(self, Brep, Distance, Vector, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    New_Brep = gd[object]()

                    re_mes = Message.RE_MES([Brep], ['Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Line_list = [_.EdgeCurve for _ in Brep.Edges]
                        if Vector:
                            New_Brep = self.polyhedral(Brep, Line_list, Vector, Tolerance)
                        elif Distance:
                            New_Brep = self.offset(Brep, Distance, Tolerance)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return New_Brep
                finally:
                    self.Message = '曲面偏移'


        # 截面实体
        class SectionBody(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-截面体", "RPP_SectionBody",
                                                                   """原截面成实体（已删除），Loft（EX版，可放样面或者线），时间效率达到最高""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Breps", "B", "N N一组的数据，可为线或面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Options", "O", "放样的类型；0=Normal，1=Loose，2=Tight，3=Straight，5=Uniform")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Integer(0))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Cap", "C", "封盖处理，默认封盖")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Result_Breps", "B", "获得的Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAT0SURBVEhLlZYLTNNXFIevGc1GI2GBhSBE0CFghUIfYAsMEMUMISEjcTPyLEVAcJtDnrNIh7AHymI0MMJ0grpHxh66DQiTiTLeGpERM2cggIIRhUkZpfQBO7un3GoLzLlfcpJ/773nu+ec+yr5P1J1pmzQdqYdNFxKK9X9sK/E8NWBEsPJgpKFykILM1QoSv8+dfiYvrJIwVyfLm2XzN3QnVSpaU3WwPUMgPZMgKYsgO/zAT5XAnx2+ImdeR+grhzmj2bfepgem8IQK2u6Pc5T1yGr0rYnzsGNFFC3yEH9SwLM1ctBW7cXdGfeBn1VLhiOFxgNThXDQqVCY1Ckld4nxKs5KNyFoSyl7Urg6ToTq3VtiVro3QP6XxNh5lICqJploGmJXzYBVCoATpfAfHlOjzpmW9SfhKwd3siXXigrs2FIQgDIqtnuJKm+W/Y1XJMDDNAyUDhcpd/XkmGhKxWgh/2+shegYT/AtxR+rgij1uoUqeX3CNk4TYj7pLW1pDc6ehNDL2oga+cG9UfhOXNVOz78qzz84PTR7blqk328LXf8yGtKU5umNDJXUxSdq8mLydG8Kyuc2BkRR+EujwjxmeJwhCOenoHN+fm2DL2oG2GvetHUvMYJeVllZlOErB8jxPN3skZEv9ct6Vv3G+clEfXhI3iKyxWqrK39+yMifBiWCWDVzdBQgYrDEeMgc5uhUd3l8ULGnZ2lFCIw75uwtRUP+PqGqTkcX2Mb7R/x8AhqLiiwZ+RFKS9fthqUSMR0gMgcYLJBkWjr0jaE3qMwNNMEKisrv76ICCEGzNCLOt7Y+PxdgcCfDrSAYETjrq5SzGCGw/Ex70PogEgUNmFv72caO+biEtiRne3AsE9Up1SuHuXxJNTJogQIHfby2nLf2VliXh41lyuYcHT0H/L2Dn3Eoqe+ov6wMPGy6FFNWVl2Y25uAUsnmLK1FQ3TGpvD0XBd7vB4wdQnEDPB/gc0+na53IkhLdWamrqGliLAIkrqiIAhWh5TlI/7aAZ04i0PuVzjmmH0N4ODN9cBPMeQluqIjXUdd3CQmkN0tDy4Q7AUCHzcR4PAkmF5MBPMetzJKaBDLndluOXq3b3bfdLGRmI+AS4elsdYArN247bl80NwEoSrCRHelkgk1dXVHIZbrqtRUd54QEwQLMkdD49X0JZOgGXB3WOE08xo5gHd8fHrGWplLT1kCMXoVfQgmcOxfYyuFS4wftPoBQNCYUBNTc0LDLVcuDC3zA6ZaQvi9lwaPWaGi4v9uBaTdnbSvl27PBhqZeEhuy0Wb6YwI2SGQ3yG3HkhYy5sCzK4cWKaEU5gin5EIAj8UankMtTKqquoWD3M50upE+4UEV54/WSt3wNC3PBCw8sPDS+2PwjHZ5AQb/yesLL2vx4ZyWOYf1eTUmk3TA8ZTVmIN+fEdo+tM1+8fkF3+o16zYnYBs2RpIa54tQGXWF6/bTyzYvaooym+dK32tQ5yQX/GT2qJzPTcdTBWYqvkCovKFZ/JWEU+tIAWunb2/gOwHd5AGcPAZwsBqj9AODLMvrAFNbC+WMvMsTTdTFa7oQv0Wzljvf0bYkL+GJpWhJA15AC+m8ywHB2P8xX5QB8WgzznxzS6cpz9zDXZ1Nvetym2XMxP0E/PonJMN+WCAttMoCf6e/z+2jE9N9DbSFoK4qGNSUHApnbM4qQfwDk9fBxw79WaQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.op = None

            def format_tree_data(self, target_tree, *origin_tree):
                new_tree_by_format = []
                for single_tree in origin_tree:
                    if single_tree.BranchCount:
                        [single_tree.Paths[_].FromString(str(target_tree.Paths[_])) for _ in
                         range(len(target_tree.Paths))]
                    new_tree_by_format.append(single_tree)
                return new_tree_by_format

            def _do_main(self, group_curve):
                if all([isinstance(_, (rg.Brep)) for _ in group_curve]) is True:
                    w_set_breps = [group_curve[0], group_curve[-1]]

                    temp_curves = map(lambda x: [_ for _ in x.Edges], group_curve)
                    join_curves = ghp.run(lambda y: rg.Curve.JoinCurves(y), temp_curves)
                    eval_list = ['join_curves[{}]'.format(_) for _ in range(len(join_curves))]
                    eval_str = ','.join(eval_list)
                    zip_curves = eval("zip({})".format(eval_str))

                    loft_cr_to_brep = list(ghp.run(self._loft_curve, zip_curves))
                    set_breps = w_set_breps + loft_cr_to_brep
                    join_breps = rg.Brep.JoinBreps(set_breps, sc.doc.ModelAbsoluteTolerance)
                    return join_breps
                elif all([isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve, rg.Line))
                          for _ in group_curve]) is True:
                    res_loft_brep = self._loft_curve(group_curve)
                    return [res_loft_brep] if res_loft_brep is not list else res_loft_brep
                else:
                    return False

            def _loft_curve(self, curves):
                create_brep = ghc.Loft(curves, ghc.LoftOptions(False, False, 0, 0, self.op))
                return create_brep

            def RunScript(self, Breps, Options, Cap):
                try:
                    self.op = Options
                    if self.op == 4:
                        Message.message2(self, "Developable放样类型已过时！插件自动转换为Normal放样类型！")
                        self.op = 0

                    origin_tree = [list(_) for _ in Breps.Branches]
                    re_mes = Message.RE_MES([Breps], ['Breps'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        w_filter_list = ghp.run(self._do_main, origin_tree)
                        w_cap_breps = [_ for _ in w_filter_list if _ is not False]
                        [Message.message1(self, "第{}组数据类型有错误！".format(_ + 1)) for _ in range(len(w_filter_list)) if
                         w_filter_list[_] not in w_cap_breps]

                        Result_Breps = w_cap_breps if Cap == False else ghp.run(
                            lambda b: [ghc.CapHoles(_) for _ in b], w_cap_breps)
                        Result_Breps = ght.list_to_tree(Result_Breps)
                        self.format_tree_data(Breps, Result_Breps)
                        return Result_Breps
                finally:
                    self.Message = 'Loft（面或线）-> 原截面实体（已删除）'


        # 删除重复的Brep
        class CullBrep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-删除重合Brep", "RPP_CullDuplicateBrep",
                                                                   """将重合的Brep删除""", "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "Brep", "B", "待删除的Brep集合")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "公差（影响不大）")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Number(0.01))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep_Result", "B", "删除后的brep")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "被删除Brep的原下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQeSURBVEhLpZZtbFNVGMfvyqDtLayFMtYpOnVVNCxGDWokRvliNhM0sdnYWFQ0TgcjuJa9EmMq6hf5YmLiloCRDyR8WEgIc3R+0SXLBNvbl3V13JZBb19kbnTMmqztbbt7H59zd6rMsa2Rf/LPOfd/zvN77jltmjIyw+xAv8EUIWCYjbh3P1pNo/W1yDAfYiFg0VEarSrc00/3vkCj9YWbH0LHSSF6H41XCPe00j1utJ7GxYm8EVpCz2HxwzT+R5i/QuA4Ju61XpSw+F0K4XDU0Lhwwlmyhl71hEUJQadok3PkGecbcO6kWZuy6X6FIAcFtqO/ofN+unz/QqABgT4CpvAfcdxAl++p2JWd2oGBtfcsE0Jb7mqwl8aK7Ha7qmGgQYEJznJT2Kk7Jri039106k5OB5inSF7HyGo7Y1eR+Qoh0IyeQUu0gRe9hazZ7Yzq1ZG2zXrf14ZLEy9WRJ3st1GOFaf9LMQ8GhBcuqHefY42i2Ghv6nytrVh6/zyrzMCNyMsQMH1aBudX1zaACV1/u6d1b+dMV/knmkJucoWCvA/AioYPfey9MGuUKqpPAcHTfPiQVOiVakrCEEXKPAUjUjTAZp9Tp5fumav2ev5cs8gt/v05Ph2CLt1EHWr4Xd/CZzt6pTqt2WgqeIveKcyj+PcZQVChJDPKOjfEIUZi5mfrEUfMx5m5PFHd3tPPu9wP/49P24Ewc0uNRhXwen2T/Nv6UW5seJPbJCFRtPcTwoEAfUUPoWjQQnvEuZmzJNSSUluqHmP5U35/LMu15N9NzitFHNrsYEGbuEJhvv255sfnMlb9HloNqWhsSLxBZNlmKcRkEWn0TWUuUK4VovOL25SzSZHj1xOTr0djLq3pSNcKUQ4LcS8myA0apTPWD/JHK7x3z6wI3HWYpivIlfwHhbKaAtlrar8c5X9oC4F+OEQ5KZPwHzgdSnuKc9EXJocaRL1qCH8qx58Q08k/cPVLUoRgrXoXcrDGkqHO6pSNzvG5J9bQAweBzHUie6AOxOvZREuRvCaCieZ40sh7ts4LPj0K657VYm8rWtR6IJcvBcyoeOQUZr04CnqJIHTSBFuqQHxzAQZ2esxT5mZlq8t+YpNmwnaBiHWo4ALFkPdcCdQKyOc+L8NglGurJoi1lZy4sjWDG8bhUj3sgZZbJCcbMS335KNe9UKPIrfqsQkSxoM8mNG5RdgXQkjhzTpoPUCOYFIr4cYor2Q4j/2hl3683hNizMBFmbR+NuUiDp1B2h5cUrx7a149zkQuiE/1YlwpVkqGzrRxI8xDyD0K4Fjf4lwuuEbV9n3rzvMxf8xIJKvHTWmeWufGLIl8fOQEH4rHbT1wIi9lKwLQpVGuKp/RHCyJqXg/wiCH21Ph2xNYtBqW+Dba2XHsXXekmH+BpxJkHeWQ4wjAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def RunScript(self, Breps, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Brep_Result, Index = (gd[object]() for _ in range(2))

                    re_mes = Message.RE_MES([Breps], ['Breps'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        total, count, no_need_index = 0, 0, []
                        if filter(None, Breps):
                            while len(Breps) > total:
                                flatten_list = list(chain(*no_need_index))
                                if count not in flatten_list:
                                    sub_index = []
                                    for _ in range(len(Breps)):
                                        if Breps[count].IsDuplicate(Breps[_], Tolerance) is True:
                                            sub_index.append(_)
                                    no_need_index.append(sub_index)
                                    total += len(sub_index)
                                count += 1
                            need_index = [_[0] for _ in no_need_index]
                            Brep_Result = [Breps[_] for _ in need_index]
                            Index = ght.list_to_tree(no_need_index)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Brep_Result, Index
                finally:
                    self.Message = '删除重合Brep'


        # 修复Brep
        class Fix_Brep(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Brep修复", "RPP_Fix_Brep",
                                                                   """修复损坏的面，不成功时爆红，有开放的Brep（Open Brep爆黄），修复成功会有提示（注：此程序不能适用所有模型和情况，请合理使用）""",
                                                                   "Scavenger", "Brep")
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
                self.SetUpParam(p, "Breps", "B", "待修复的Brep集合")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Toggle", "T", "Open Brep修复替换的开关")
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Fail_Brep", "F", "未修复或无效 Brep集")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPzSURBVEhL5ZRdTFtlHMYxM4uJmcbEzMQrjN7pvYkX6s0uvPCSZBcm4AShtKyF8llgpeV7DrcYb2apsCkfawstXwU6pLYMVph8DAaDbBiJJjIVGCHt6TnvOefxf+DFdnaaEU288JectDk97/M+53mf/tP+Pwh3c9OFpYJXhXljurpgPolg5jP8p38GkPZU7HbOkLymF4VZHRNm9GJ86uyuOGXaYDeKQspESXN01Pwmf/zo7C1kF+HnQsiLerA5A+RbZ6HOFALTxcBMOTB3DghZwEbKL/ElT46wkP1KfEUXlZf1EG7lQ5g2gNwjPmGE+G0hxG/MEAPFUAO0UaQe0oClgy99MmIL2X5sGBH7TgeKBvGbBYjfMCIeMkEcL4I4VgxptBTSUBnkQQsQbgJzWxr58r9nbyHnNDbI7TyJa+4j5H5Sc0/iwQP3UqAE0nAZpMEKsL5KKH0Ul78erNN2iss8noeLuhfiy7mb6qoBguZ+mtxPHbgXQyRO7qXr5H5Ec18O1k9n4K0C81QD/Q1gXbYN9Svrc1wuleh8thM/mg7Ek6MJ82g096Pk3k/uB8i9rxKstxqy+xzkrhpg6BKUK7UNXO5RhKWP3lXXDRBvJ0Wzf7Akrh0sbSAMV0AOmMH8pfvRsN4qyB4Sv1YDpdMO9F2E2l5n4JIJcCfjeGzp41XcL0hE88fBHojLQRO2u87jfpNnPxq5n96gh9y7rJA7bYD3ApT2ujCXfBSKxo6fKJrZPIomH/HDg9WiCR5EI4+ZgXEj1mwDWLOMQPZWknvaoNsGtbue3qCJie3217lkAnEl7w1xNY+xJYrlMZ2XeDS7njrEvFZ83+xCJHMZe84WoJc20dz3X4TyZa2dSybQxkF0MSeEH/6689oGsYEqrJ53I1J0E5H8OSwZw/itxQHlGtXT1wjlat0KXNbjXDbB/ryZz53FugmxlGh45+kPxUZKoNAleGoQ7WyA5LLh4WefY8fuBJyXIXVUv8MlU4nN6d6S7xSAzZKw1vmkcSBdp0omdV7us0Dx0kW1VF3UfVcL4jVfDD/IuFK+9aHzPS6ZSiyiq8C9MoiTSZ0/HAfJndda46bWdFHu7iYoHQ2bqnrq2c33HS9tZTpKt7NaL2yfaX3bleE6xqUTUDRf424lpEP3fxoHKZ33fgq1rf40X77Pgw8cr21lOXJ/PdN6gt9KAFfGMTFc2INFK43h8tRxkNz5vhbIbbV+vvRoSKGSKnm8YgeTJBSqBQLkdpC+++iTqoqeZoqmMYa2xnS+5OhEfSUvY6wqS/FXO5iveoLcr7Puml9Yp31X9XyyIzlr9fzRfwcErU/D1fS8etV6EpetL/Lb/yVpab8DAbCxRT6DURIAAAAASUVORK5CYII="
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
                            return "第{}个Open Brep替换成功！"

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
                                    Message.message1(self, "第{}个Brep修复失败，请重新检查！".format(_ + 1))
                                elif _bool_list[_] is True:
                                    Message.message3(self, "第{}个Brep已修复！".format(_ + 1))
                                elif isinstance(_bool_list[_], (rg.Brep)) is True:
                                    Fail_Brep.append(_bool_list[_])
                                    Message.message2(self, "第{}个Brep为开放的Brep（Open Brep），输入‘t’以替换".format(_ + 1))
                                elif isinstance(_bool_list[_], (str)) is True:
                                    Message.message3(_bool_list[_].format(_ + 1))
                            return Fail_Brep
                        else:
                            Message.message3(self, "输入的模型中未损坏！")
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                finally:
                    self.Message = 'Brep修复'


        # 模型比较
        class ModelComparison(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-模型比较", "RPP_ModelComparison",
                                                                   """通过面积以及长度进行模型比较""", "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "A_Model", "A", "一组模型")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "B_Set", "B", "一组截面比较体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Area_Tolerance", "T0", "面积公差")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Length_Tolerance", "T1", "长度公差")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.5))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Result", "R", "比较结果")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "比较后下标")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQDSURBVEhLrZV/aBtlGMcv3To3Z1u32bnuh2m7uNWkTVsDKvunMJWJQqFtMuoaDCZt0ktyl0vTa9PkLm8ul7v8LDX9y+n88Wd/IAz2j+AfThC1UKhQmTJRqggighM2EDdzr+97fV1tnTHBfSDc8zzvc8/7fZ977kLVgOHlgYFXXh0ZyQ4PDT1NYvePC3Z718j58zfdTiccHhxc8Xq99WTp/uBwOPbQNN0eouk4spsAAHVkqXqwqnAgMDzNhociHHd2gmF6I8FgW5SmD+CCPM83IJ8l6bXDKD3NoVg/PxWKDEZY1jPFMBwfDMZ4hklGGCY1ybJZZC/xLBtCV/dUMDiINtSFTIdCrVgIKXVvRrNdx32zrd3E3QY+HS7AcVwL2tw2GQw+hwTYsZBJLIRlY1GOk8IhT9IF+vaS27YzKlvbxvKWk3Smq7KSCviUnucDud6jxN3C67XVj8mWky7Q/TBdtJwg4ZpwFqz7xxVrpzdrfoyEtsCq3fITRgCoOl+u53ESrgk3Uu4H5iOoVjtyDZtRAi1bTniB7RFsj+e6TuON9IUa8Khmk/eirR5vgGo9SMKbYNVMyfQAtnGCO3emQV+oHoNX6ezAhi/dfWy8YD2sRzHoxdmFVROX8ufNR8bST7YQtypw//3oBNj2Zm1Nvkx3q76AYUpPNY4WrG3EpVAfH8IPnLhV4VE6H/1rehxLSHBqS/A/jgQhZfj7iaoBt5UBpkbiUgHVesoBzHt0B/ff7KA2HQJOCM8+s4+4/8nOwfDLvUYPMB/U1TqB2aR9H953ZyU8oF0FF7TllMU+Y2rGnw6SXxEXMO7dOdp4IvFk6v2m2qmmP77wB+GGAOGKCssL0sZbygvNL6WPHyP5FcFCcJuxDVfvfsYNuAv6xCBnV/laQLm9ysGfF8KwvCT9er0003wOGLcmoQJkYgy/r42r2rXpb8ofCAXtvXSLXT7VhkaqRX+ttR88Lu2rSFn7UNC0ZWkdxzpU6tDdB1WBc9PG1h8/dx7+bZW+Ca9GIPxsFmoL6deofqqBmgHscCaTeVuV44vLF6O3Lr8u3rmUFdcAkC7NiPw7kYJzP6lzT/CbSz1LHdK+pfvgRhTeWmIgvKJAbbHgQst1lCCAF+fn56GcVuFkNAEjURHGEklYKpWgKIhfoq5u/6bsAD/Mfv70Ue0603j7E+4N7aPEDW1R+kl7c/Yg1UftRlMEDYIgXC4Wi1BVVagoCszlclCW5XI8Hj9L6vwr0Sh9QBTja4mEtD7Bi58WUuIvxZR4IyYI66jW13oS+jvcnUwmeUmSrqDr+6lU6l1U/Iy+WAVI4Mdzc3MQ3QdjIkC/BERt1wWTlP8HEtiBxH2Xz+dhNpvVO5BOp2E8Hp/4Exj8pAy3ytn0AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.local_tol, self.area_tol, self.length_tol = None, None, None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

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

                    Result, Index = (gd[object]() for _ in range(2))
                    re_mes = Message.RE_MES([A_Model, B_Set], ['A_Model', 'B_Set'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        str_guid_model = [str(_) for _ in A_Model]
                        True_Model = map(lambda x: objref(x).Geometry(), A_Model)
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
                                Message.message2(self, "角度公差和长度公差得出结果不一致！")
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
                    self.Message = 'HAE开发组'


        # 模型展开
        class BrepUnfolder(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-型材模型展开", "RPP-BrepUnfolder",
                                                                   """型材加工图模型展开插件""", "Scavenger", "Brep")
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
                self.SetUpParam(p, "Brep", "B", "加工图模型")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Surfs", "RS", "目标面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result_Axis", "RA", "目标轴")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOxSURBVEhL1ZTfT1t1GMb7H3jhjXqj7kaDJG6ZuzFTQmghbrq5hGy0kTOKlR9t2WBQbKF44PQcuhEXp5MW29OpJDKZyIBuDMqAQgEdbGyjsTCJ8cq6dEt/UEqlLX38AqdZXaIXZV7sTc7NeZ6c55zn/XyPaKdzXrvv2bt9RarlvuOqpS65aqmzTLVsqVD9ZqpSLX1arRJsmY/VmLsX99TAr/XAbR3w8yeAkwFGTgO9bRBsmY/NmPt6cPYjJOZOYH2iBjGHBnE7Ceqlsd7Z8hQEfN2Ws3vtdgVwpwaYqQPGtcCQHhggNXWxOw8wc/uz/nCWeIOTlV7/kMrr7z/pDVyq9Ya7dF6/tdEr2DIfWrnvuZELh1mX7SjnMhWxrnMydvosxc4YS1kXrWAFW+bDG9/eE1uoBNy1wA1C0mQD4CAkXWWB7tankKL1/4OiyHw5OWTVSE6TmsYIRde2KUo+CYq+4nJe/XNS/iDsqvQFHGpfcKDaF+qp80UuNvgCVr1P1MG+9bzHLqXclz6g3J0U5bYpKI+5nLrXrqbuGNTHjOU5L93qKSz2PK5/oabutqqlTOmbrwzx7zIuWyE33l7ETXwm4ybairnpVjk3rv+QE/WaJO/gd3JIPBrgJvm86SZglBwSxxmELE0bHVrJcSwqgcWUTj5/rAUYPo31bxnwmoLiwKwiiYVTwE/E4yT9D5NnXDEAFzmI+kwF4sSCErEbZElOQsFwPRIDBLXLLVi10g8tWrE0NKfYSMwKOlliwk703mas2uhVi6ZASgKiG2kUJdKXvBkQfywgLgSE0wLiaQHblPwz4F8p6jfnS+Ahv9tbhIIpQsEoqeHqJgUGRPjmgFWXJ4vMlwHzKf1jYJDo/QwiF5qj1vp8WXBOEUtRlBzb1BuJ3oLkdwaIuj8X56zMlvlDE0p/YLjKHxqo8a/8oPGvdev9D02Ny+2avGP3XfJk2KVEyFGFFXsNwj9qEP1ejwfmhsiXp8RS72TJX6tTRB+pQuhKSm9EyNYEkVH7xi7nN+8zzo5CZuz8UcZ5VsY4z1DMFFfKjOhK9Crxnhcs+tzXeJ0km68VrhMHyXUk2yw/lFUm3vuMmd6fxdPkfsoj6HzpkeztihbTKyL9DRIK7OzWGxgOHHhRQD6z2aLIrcTmEmNkSXHHI4pCvD5meE/ysmDNbP6LouCTCNiq6Bc1kjerseEiFFx/RNEK35TYcUD3uXxJdL4CazNqREZPYm2wDtHLWsR7aNw3aUEfzNslWDMYkehvqUZItKjznNIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = sc.doc.ModelAbsoluteTolerance

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

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
                    re_mes = Message.RE_MES([Brep], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
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

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result_Surfs, Result_Axis
                finally:
                    self.Message = '型材模型展开'


        # 区分是否带孔Brep
        class BrepHole(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-区分Brep是否带孔", "RPP_BrepHole",
                                                                   """区分Brep是否带孔""",
                                                                   "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "Geometry", "G", "请输入Geometry参数")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Perforated", "P", "有圆孔的物体")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Solid", "S", "没有圆孔的物体")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKHSURBVEhLtVbZb4xRFPe/EN6IqKVePEl4UCKUB8TSiq2oXaPxoLEkQjQeWjGmbZpUU6MtpqPLVKeiTCo6qCb1YJmI2BJpbHOX7/s5d+F7cFszdH7Jyf3uOWd+v3vOXTJTfN9fTFaVL1MC55FHKIEq+/0b3psByOFGyJEmsquQo9fhpfvhve4LLJ0gf8TEVR7le2+TliGAU0B070GmZhpY/QJkwrPB6uZBRLdAdO6EuL3djNHN5J9r4iqvZirEncOWIYBTgMf3gV0rAjJjkI9DmkB07YboPQQRP2DGrjLyz4dMXQLYGOUvh+g7ahkCuCsgEta8BP7HYYjkWbCGhW6BhkKIB2d0HmteSgIVliGAW6CnHJnaGVT+HNMCJdBRSq3ZRS3aYcaOEvJTa67MQiY0k/KnZ1+B/+EpvJc9kEO1kM/b9Yb671Pw3z0KjOZemjb7VdzYi074n0YsQwCngIbMQD4JE9GQdfwb3AK+Rxv8GaK/Uq9Oz5V5IjA1zwLuPbh3AjyyUp8M3rYG/NZGY23FYC3LwNWJuXvcZk8MpwCPbTUn5P5p8Pa1+phqi6wg3ymwxkXg0U02e2K4BeiE/CKQz5rAwgX6UsmH1don4vvBb27Q33/D+BXUFZgL11JkVk8VqbvBiZzVF/5fBbo1qvetq8FvrNOCPFZKq15PvlVkxbRPf/zMCafA+PDtmD2cAt5oK2TyHPX8IuRgNb03l8nJbTQ3OAUUuYiWmCchRq9n70HamC82mhvcArRyTa4etu5yiMQxEvhqo7nBLTB4gVa+jcj3klAZvfNHJrmCVEi3RSQqibwCYuAkHa3vNpobnAKQjFb8zZAKNf6wgdzhFphEKIE8/qsAfgJdGFoFNH4/8QAAAABJRU5ErkJggg=="
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
            def Geometry_Multiprocess(self, Geometry_list):
                Curve_list = list(ghp.run(self.Get_Curve, Geometry_list))  # 得到所有的合并曲线,查看是否是孔得到判断结果
                Geometry_Bool_list = list(map(self.IsHole_Multiprocess, Curve_list))  # 判断是否带孔的数据 真假值
                Geometry_Bool_list = list(
                    ghp.run(self.Remove_Excess, Geometry_Bool_list))  # 简化[[False, False--]] 变为 [[False]]去重 有真则为真
                return zip(*ghp.run(self.HoleInGeometry_Bool, zip(Geometry_list, Geometry_Bool_list)))

            def RunScript(self, Geometry):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    # 带孔Geometry，不带孔Geometry
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        Geometry_Tree = [i for i in Geometry.Branches]  # 拿到数据 二维列表
                        res = map(self.Geometry_Multiprocess, Geometry_Tree)  # 得到物体是否有圆的真假值
                        Perforated, Solid = zip(*res)
                        Perforated = self.Restore_Tree(Perforated, Geometry)
                        Solid = self.Restore_Tree(Solid, Geometry)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Perforated, Solid
                finally:
                    self.Message = '区分圆孔'


        # 圆孔修复
        class FixHole(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-圆孔修复", "RPP_FixHole",
                                                                   """修复Brep或者Surface表面的圆孔""", "Scavenger",
                                                                   "Brep")
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
                self.SetUpParam(p, "Hole_Brep", "B", "待修复的Brep")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "修复圆孔的精度")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(0.01))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "No_Hole_Brep", "B", "修复圆孔之后的Brep")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARWSURBVEhLrZRrTJNnGIaZycj+7NeyxXiIWZTS89fzgba0pSDgYSMIy5iakRnZH0n2Z4kxMU0WY2LIgoRCwiwLy9iCZjgNIIIgwgTsHCDSoehUDlGGgIAcS1vvPd/HK7IBQ41X8vRr3r7vffd97idfxGo0NLjfYV/fLLOTrvhgMLEzFErtmw18kcmW3wwzEy5zOJQQBLZjofYgENh/0u3GOrbl9fH70yOD03E9QAIQdgLPqBBHlYL5+YzLIyNHNrKtr0dgKDET2AHMkWiQxBdN+NqFUOiTgcnJLx1s+6sT7nddRSAJmIgHZlzAPAmHmIlglEQmqeHZ2cxD7MjLM30taVP4lmMeD0l4iAzGqabpe4Buw5ss3obWkUot23fK7z8TyY6vzVSDdRdu2YFuqgckOkhCT6imyGRZy/hcPkYw+Gnr+Hj2Vibx/zys1GejzQL4qLpigb9IiL/NKJlMUs3+x0Qw2kktSxuemzuwg8msTnuJ6sjTOj34CrfGADdswB0HMEAmw2Qg5EImy3LhRzmV6vPD9PEWk1vOpTx5dk+ZCvd+UeFJjQ7BZjPQbgVuU8v6SPhfuSwxoXZ9741Dzolk7NvrbDeZbBfsTmcGk31BRQ7naClSoKVIhttlHB5XaxFoMgF/kMmfZHKfxAZJfGkuNL5ny51QymzglDEwGEzQ6/WwWCywWq3pTHqBM+70yAu5hq7rxRwaCyToKlXiUYUGM1eMq+RCT7jgPmyGRGyAWsVBLpdBq9WSkQFGk/lpcnKKiMkvcNGTtq2+0N7p86rR4BGjvUSB/nNqTNbr8YzPpfN5LvTvxxIQGHKg5BslCWvAcRwUCgXkMpnwNJktsNjsR5n0C7wnvn73UoHrrK9YJ5j87pULuYzV6hBamsvf8eiu0uH+eR0OpGvwwYZoSCRiKElcKpFArdZCbzT9zGSXU+NJPHb1O6PQruYiKXpOcxh+nkubFaGbsWgtVdEAODF104aDaQps+VAhGEjIQKnkoNEZfExuZao9uzMuF8RMNxfJ0VQogf8nJQYrNZj/zYiRaj06KrQ0VTSmwy6E79mxP0WJzVskEIujIaNWaTS6oCM+3s7kVuZc/h5dfaHtjs+rElrW8YNCMOn+kcPdawYKmgIfo5pIwINGK0RR2yASSQQDjlNBbzA/YlKrczov+/26AudFX7EWDfkL4TcXytDvp3bxrw1+ZKfJZDQOhz6LxvoNWyGVSoU2qTXaUSazNjWehNyWU0ahXdU50ei9wRvQuPKvD7rJUJsZ548pstZvjKqIFomgohuotbomdvzlqPLsPHil0BisPylFO00RkCyIBydiUZUn6+P36HTbN4uionrFYjFkEslx4eCrUJmbGltXEDPQ7FWit8OBx3dtuF7KoeyobDfbEuFyud6jWzSKRCILW3o1yvP2bqrN1zTyE1abKwuVH1d8xX5aJCsr6216rP4CXAu3272uvkj30a/fahRsaQUiIv4B6Q48zcsB1rkAAAAASUVORK5CYII="
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

            def remove_hole(self, brep_list):
                new_brep_list = []
                list = List[rg.ComponentIndex]()
                for sub_brep in brep_list:
                    for loop in sub_brep.Loops:
                        if loop.LoopType == rg.BrepLoopType.Inner:
                            list.Add(loop.ComponentIndex())
                    new_sub_brep = sub_brep.RemoveHoles(list, self.tol)
                    new_sub_brep = new_sub_brep if new_sub_brep else sub_brep
                    new_brep_list.append(new_sub_brep)
                return new_brep_list

            def RunScript(self, Hole_Brep, Tolerance):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    self.tol = Tolerance if Tolerance else sc.doc.ModelAbsoluteTolerance
                    ho_brep_trunk = [list(_) for _ in Hole_Brep.Branches]
                    re_mes = Message.RE_MES([Hole_Brep], ['Hole_Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        temp_breps = ghp.run(self.remove_hole, ho_brep_trunk)
                        No_Hole_Brep = self.Restore_Tree(temp_breps, Hole_Brep)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return No_Hole_Brep
                finally:
                    self.Message = 'Brep孔删除'


        # Brep是否闭合
        class BrepSolid(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Brep是否闭合", "RPP_BrepSolid",
                                                                   """检查Brep是否为闭合实体""", "Scavenger", "Brep")
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
                self.SetUpParam(p, "Brep", "B", "待检查的物体")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Solid_Result", "S", "如果Brep闭合返回True；否则为False")
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

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Solid_Result = gd[object]()

                    re_mes = Message.RE_MES([Brep], ['Brep'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        Solid_Result = Brep.IsSolid
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Solid_Result
                finally:
                    self.Message = 'Brep是否闭合'


        # 面板折边（规整铝板）
        class Surface_flanging(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-曲面折边", "RPP_Surface_flanging", """面板折边，适用于规整铝板，特殊板材可半手动处理""", "Scavenger", "Brep")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4ffb7d64-abfe-46ec-95af-f2de4fb17088")

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
                self.SetUpParam(p, "fold_surface", "S", "源曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "fold_size", "S", "通用折边宽度")
                p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(20))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edge_Tree", "EL", "曲线列表，输入需要自定义的边线，未输入统一加折边")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = GhPython.Assemblies.MarshalParam()
                self.SetUpParam(p, "Size_Tree", "SL", "折边宽度列表，控制曲线列表的值，数量必须和曲线列表统一")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Fill_Brep", "R", "偏移折边后组合的面")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Folded_Surface", "S", "偏移的边写组成的面")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOzSURBVEhLxZVtTBNnAMcvxM23WRVxVsW3vZAt+7JEjFliNDH7YMycL7Fh2Ou1RRgbqEvIMNGpLbgwwGpp8Q0xtLRsQukrhfI6DoasohYGzs3AFrNkGca4L0OiErn/np6PW253zBA/+Ev+H5q7+z1v/7syL5zddXWzOV9De1p35/a0zqZTH13j07VX+GR6+fnhfOHdmf1D2H+0GIVpWuRZLDDWVN3Xtoe60qLtR9Njl9/bIgzPpLdPH20g3GPoiaIoZSPOM7NQzizGyaR3ULR5B458dhA5dhs479e307sjLk2MZ/fc7F1FH302ek9gLdd9GZ+WlMNOxGXMcjF2Ro3TTCLJAtjI7xOvr0ehxoDPvyzC3qoLD/QdTb073c5Mqpka1tfgNF4bwLENO0RZGZOskPiAr5LrC8nqFsGqSkHphg9gqj//k1u4eZiq5OwNhZawLR3jWY5vYJ2xksx0qYJcHhsZpHzO6sngox9QLfTfojo5nC902DgwhHx2H84wKkWZUqzMK6g4locARuF8GP2Q6qRoPJ6XtYHG3wxtPIqT19H9VxZKo0bZnNWo/bOHzH7gZxNMCVQpRecPaYx9MeSaSsm+JiqIlGNl5uFcphFB3EXVxPfZVCeH9YV79NGrKEjdKh6ekkyeZShLUKNmJAyXcOOOa7R1LtVJEavZ+R2yzjpgS1hGDo08qCiUxkpadnrTFoTwBxyTfWaqk0M+C05DbBCHtunJ7KdzuCo4fOWoEYbHHfd5NdVJ0Xs8ajbSNm6sD8EyL4Uc7hJF2X9jJSWwr3iXNGcYVZOxC1QnR+dt+MLYP4i87Hwy+/mKMqXEq1lZfAiXhNuTlQ+73qY6KU+rqW/vwlcr15P2JCnK5IlXcw28Y1fhFAYbqE7Ok2peR675hPjKK8vkEauZYUA9fodzoncj1Un5uKLiJZ0/PBSvpnnd9KppJd+h2pEmOIQbfVQnh3W55u5p7WjZd8ZB5AvEj5eyUJqn1fST2Tse92mobmr2Hyn0lr6/EydVb4rbFF+JLb7HCvJ4rKQI7raL5MW69YuJ52dQzdSwjXUHMrqbJ3L9tcgvOA7zP4PFv/0Lxf+Bf+VJsL+WSqr5K5l9/wGqeDasq/INQ8SXo/s23KxrDY7l+C7hYEEhCshglsS3xHY9Wdls1LpPwS2M/GW7F1HRx6dHdp1zOdcS5HR8o5drDd77JEBWVlIC81YNLGtSH3nGeqPVwo9Z9PbnI9dfvcjQHNrF8Y1OY1dkNKO+Zphe+h8Y5m8CNtoPOIxFZAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            # 数据转换成树和原树路径
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 重新定义向量的长度
            def ver_lenght(self, vec_size):
                vector, size = vec_size
                unit_vector = vector / vector.Length  # 将原向量单位化
                new_vector = []
                if "float" in str(type(size)):
                    new_vector.append(unit_vector * size)  # 创建新的向量，长度为new_length

                elif len(size) >= 1:
                    for i_vce_ in size:
                        if i_vce_ != 0:
                            new_vector.append(unit_vector * i_vce_)
                        else:
                            new_vector.append(0)
                return new_vector

            # 数据自动补齐
            def data_polishing_list(self, data_a, data_b):
                fill_count = len(data_a) - len(data_b)
                # 补齐列表
                if fill_count > 0:
                    data_b += [data_b[-1]] * fill_count
                return data_b

            def add_fillet_to_edges(self, fillet):
                brep_surface, fillet_vector = fillet
                # 获取曲面的边界

                edges = [cur for cur in brep_surface.DuplicateEdgeCurves()]
                one_surface = [brep_surface]
                one_surface2 = []
                if len(fillet_vector) == 1:
                    for edge_g in edges:
                        one_surface.append(rg.Surface.CreateExtrusion(edge_g, fillet_vector[0]).ToBrep())
                        one_surface2.append(rg.Surface.CreateExtrusion(edge_g, fillet_vector[0]).ToBrep())
                else:
                    if len(edges) == len(fillet_vector):
                        for i_num_ in range(len(edges)):
                            if fillet_vector[i_num_] != 0:
                                extrusion = rg.Surface.CreateExtrusion(edges[i_num_], fillet_vector[i_num_]).ToBrep()
                                one_surface.append(extrusion)
                                one_surface2.append(extrusion)
                    else:
                        for i_num_ in range(len(fillet_vector)):
                            extrusion = rg.Surface.CreateExtrusion(edges[i_num_], fillet_vector[i_num_]).ToBrep()
                            one_surface.append(extrusion)
                            one_surface2.append(extrusion)
                Brep = rg.Brep.CreateBooleanUnion(one_surface, 0.01)[0]
                Brep2 = rg.Brep.CreateBooleanUnion(one_surface2, 0.01)[0] if one_surface2 else None
                return Brep, Brep2

            def RunScript(self, fold_surface, fold_size, Edge_Tree, Size_Tree):
                try:
                    # 传参判断
                    re_mes = Message.RE_MES([fold_surface], ['fold_surface'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc

                        # 参数定义处理
                        fold_vector_count = []
                        for surface in fold_surface:  # 面法线获取
                            fold_vector_count.append(-(surface.Faces[0].NormalAt(0.5, 0.5)))

                        # 根据参数输入进行向量生成
                        if (Edge_Tree.DataCount == 0) or (Edge_Tree.BranchCount >= 0 and Size_Tree.DataCount == 0):
                            ver_zip = list(zip(fold_vector_count, self.data_polishing_list(fold_surface, fold_size)))
                            fold_size_count = ghp.run(self.ver_lenght, ver_zip)
                            fold = list(zip(fold_surface, fold_size_count))
                        elif Edge_Tree.BranchCount >= 0 and Size_Tree.DataCount > 0:
                            if Size_Tree.BranchCount == 1:
                                ver_zip = list(zip(fold_vector_count, self.data_polishing_list(ght.tree_to_list(Edge_Tree), [ght.tree_to_list(Size_Tree)])))
                            else:
                                ver_zip = list(zip(fold_vector_count, self.data_polishing_list([data_ for data_ in Edge_Tree.Branches], [data_ for data_ in Size_Tree.Branches])))
                            fold_size_count = ghp.run(self.ver_lenght, ver_zip)
                            fold = list(zip(fold_surface, fold_size_count))

                        Fill_Brep, Folded_Surface = zip(*ghp.run(self.add_fillet_to_edges, fold))

                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Fill_Brep, Folded_Surface
                finally:
                    self.Message = 'HAE 曲面折边'



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

    def get_AssemblyName(self):
        return "Tradition v4.3(Test)"

    def get_AssemblyDescription(self):
        return """HAE插件"""

    def get_AssemblyVersion(self):
        return "4.3"

    def get_AuthorName(self):
        return "HAE Development Team"

    def get_Id(self):
        return System.Guid("86c4ead2-84fa-4dff-a70f-099478c2ccca")

