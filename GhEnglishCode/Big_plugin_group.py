# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Big_plug-in_group
# @Time : 2022/11/5 16:26

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import Rhino.DocObjects.ObjRef as objref
import Line_group
import Rhino.DocObjects.ObjRef as obj
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from itertools import chain
import math

Result = Line_group.decryption()
try:
    if Result is True:
        # 表皮常用信息适应平板
        class NormalInfo(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@平面基础信息", "HAE_PanleInfo", """Common information of epidermis is adapted to flat plate""", "Hero", "Big_plug-in")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("79bbf1e0-d772-44fd-9e8e-fa8b5d26248d")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Brep", "B", "panel")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "ID", "ID", "Panel Guid")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Lower_Baseline", "DB", "Lower baseline")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Right_Baseline", "RB", "Right Baseline")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Upper_Baseline", "UB", "Upper baseline")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Left_Baseline", "LB", "Left Baseline")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "X", "X", "X Vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Y", "Y", "Y Vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Z", "Z", "Z Vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Center Plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Vertical_Plane", "VP", "Vertical Plane")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Transverse_Plane", "TP", "Transverse Plane")
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
                        self.marshal.SetOutput(result[5], DA, 5, True)
                        self.marshal.SetOutput(result[6], DA, 6, True)
                        self.marshal.SetOutput(result[7], DA, 7, True)
                        self.marshal.SetOutput(result[8], DA, 8, True)
                        self.marshal.SetOutput(result[9], DA, 9, True)
                        self.marshal.SetOutput(result[10], DA, 10, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFVSURBVEhLzdVNKwVRHMfx8VQ2nsrCS1AieUqeFhJFYcVCNtY2NhYWFrKQJGXhHVC27GWlLDymbMQLsJCFhRTf3z1zarpzrnvOnc1861Onubf5zz3T3InyVDMOcIY9NKCi+jEaa9KBuEP8JuzA1oJhjKBHB0p1hFc8xLqwjFN8IDngHTq+iD7o+/d4wz6cvUBXYZtC8qSljME2iWezTPeIQbMstArXCYutwDaOG7NMpwFDZlmoDbdwndS6RitsE/AeoOrQiW4HHa9BsuABoXkP0JWt4yR27GA/W0M1lPcAPUiuPXf5Qj1U0BYNQM9BOb2w5eceVGEWGx6mYfMe0AjXfrv8IPge6BcsQX9q5SxA31f5uQeqA3Me2mHzHqDn4BuuPS/2ieB7UIttnHvYRPCTXGn/DniC/iGzpPfJnVmm05toC/MZ7EKvTmczuMRVBhfQNlEU/QHaRq3PYMJ1vwAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def get_id(self, objs):
                str_id_of_objs = [str(_) for _ in objs]
                return str_id_of_objs

            def _get_base_lines(self, geoes):
                below_line = []
                right_line = []
                above_line = []
                left_line = []
                reserve_list = []
                for single in geoes:
                    points = [_.Location for _ in single.Vertices]
                    below_line.append(rg.Line(points[0], points[1]))
                    right_line.append(rg.Line(points[1], points[2]))
                    above_line.append(rg.Line(points[3], points[2]))
                    left_line.append(rg.Line(points[0], points[-1]))
                    reserve_list.append(points)
                return below_line, right_line, above_line, left_line, reserve_list

            def _get_vector_by_points(self, data_of_vectors):
                x_vector = rg.Vector3d(data_of_vectors[1]) - rg.Vector3d(data_of_vectors[0])
                y_vector = rg.Vector3d(data_of_vectors[-1]) - rg.Vector3d(data_of_vectors[0])
                z_vector = ghc.CrossProduct(x_vector, y_vector, False)['vector']
                temp_x_vector, temp_y_vector, temp_z_vector = x_vector, y_vector, z_vector

                avg_point, x, y, z = None, 0, 0, 0
                for points in data_of_vectors:
                    x += points[0] / len(data_of_vectors)
                    y += points[1] / len(data_of_vectors)
                    z += points[2] / len(data_of_vectors)
                avg_point = rg.Point3d(x, y, z)

                centre_plane = rg.Plane(avg_point, x_vector, y_vector)
                vertical_plane = rg.Plane(avg_point, y_vector * -1, z_vector * -1)
                transverse_plane = rg.Plane(avg_point, x_vector, y_vector * -1)

                return x_vector, y_vector, z_vector, centre_plane, vertical_plane, transverse_plane

            def RunScript(self, Brep):
                if Brep:
                    ID = self.get_id(Brep)

                    True_Brep = map(lambda x: objref(x).Geometry(), Brep)

                    base_lines = self._get_base_lines(True_Brep)
                    Lower_Baseline, Right_Baseline, Upper_Baseline, Left_Baseline, Points_list = base_lines

                    origin_data = map(self._get_vector_by_points, Points_list)
                    X = []
                    Y = []
                    Z = []
                    Plane = []
                    Vertical_Plane = []
                    Transverse_Plane = []
                    for _ in origin_data:
                        X.append(_[0])
                        Y.append(_[1])
                        Z.append(_[2])
                        Plane.append(_[3])
                        Vertical_Plane.append(_[4])
                        Transverse_Plane.append(_[5])

                    return ID, Lower_Baseline, Right_Baseline, Upper_Baseline, Left_Baseline, X, Y, Z, Plane, Vertical_Plane, Transverse_Plane


        # 关联表皮信息存储
        class ChainInfo(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@关联表皮信息存储", "HAE_Chain-Info", """Skin association information storage, association skin ID, association skin angle""", "Hero", "Big_plug-in")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("9482bc09-2ab9-47c6-8bad-515edc4b833d")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Brep", "B", "panel")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Below_Panel", "D", "Bottom panel")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Right_Panel", "R", "Right panel")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Top_Panle", "T", "Top panel")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Left_Panle", "L", "Left panel")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Below_Angle", "DA", "Lower angle")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Right_Angle", "RA", "Right angle")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Top_Angle", "TA", "Up angle")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Left_Angle", "LA", "Left angle")
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
                        self.marshal.SetOutput(result[5], DA, 5, True)
                        self.marshal.SetOutput(result[6], DA, 6, True)
                        self.marshal.SetOutput(result[7], DA, 7, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAE+SURBVEhL7dNPK0RRHIfxYyFGRFYTScnGKH9qsqAkSsmG0hgLr8DG0kZZSBZsbCQ7RTZjaWHDQpEkRNKQUngHUhY833Om5s5Qd+aanfvUpzm/O82Z7twzJizstyKZ15I3jSOc4gwbqENJmsMjRtGALuzgDjX4U814gTbObw+Lbhm8JPbd8kcD2HLLYLXjALt2yraCbVxAP9MSin74HXjHGs7RAqXrX9B7E0hAd3iDWhRUGfSBVTsZsw5t2gtt0oROeEth0y39a8MrKuxkzDgOMQl9+Qiq4S2Ge5Tbyac4bt0yJ22u/4PuZkoXPDUijSo7+aSz/Qad9/wWcII+O2Wbgf6EBaeNntFqJ9csPqGj2a0LmcbwgSE7FdEyHnCMK+jB92AeusNLXOMJej6BimIYOkHe6jGIflTqQti/zJhvIVw2Gp/eKk8AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._set_punlic_brep = None
                self.Guid_of_Brep = None

            def diff(self, brep_data):
                diff_set = []
                for single in brep_data:
                    group_set = []
                    for _ in brep_data:
                        if _ != single:
                            group_set.append(_)
                    diff_set.append(group_set)
                return diff_set

            def four_edge(self, edges):
                below_line = []
                right_line = []
                top_line = []
                left_line = []
                for _ in edges:
                    below_line.append(_[0])
                    right_line.append(_[1])
                    top_line.append(_[2])
                    left_line.append(_[3])
                return below_line, right_line, top_line, left_line

            def _first_handle(self, line_data):
                Brep_pipe = []
                for single in line_data:
                    s_line = single.Trim(rg.CurveEnd.Start, 50).Trim(rg.CurveEnd.End, 50)
                    pipe_data = ghc.Pipe(s_line, 50, 0)
                    Brep_pipe.append([pipe_data])
                return Brep_pipe

            def collision_test(self, col_ts):
                return [_ for _ in ghp.run(lambda istance: ghc.CollisionOneXMany(istance[0], istance[1])['collision'], col_ts)]

            def transformation(self, id_data):
                br_list = [obj(System.Guid(_)).Geometry() if _ is not None else None for _ in id_data]
                return br_list

            def inside_index(self, data):
                index_list = [_ for _ in range(len(data[1])) if data[1][_] is True]
                res_index_list = [index_list[0]] if len(index_list) != 0 else [None]
                return res_index_list

            def get_index(self, index_data):
                list_zip = list(zip(self._set_punlic_brep, index_data))
                res = list(chain(*[_ for _ in ghp.run(self.inside_index, list_zip)]))
                return res

            def single_map_id(self, tuple_data):
                map_list_id = map(lambda iml: iml[1][int(iml[0])] if iml[0] is not None else None, tuple_data)
                return map_list_id

            def get_angle(self, brep_tree_data):
                angle_list = []
                for _ in brep_tree_data[1]:
                    if _ is not None:
                        angle_list.append(round(math.degrees(rg.Vector3d.VectorAngle(brep_tree_data[0].ZAxis, -1 * _.ZAxis)), 2))
                    else:
                        angle_list.append(None)
                return angle_list

            def _temp_fun(self, brep_list):
                if type(brep_list) is list:
                    center_pl_list = []
                    for brep in brep_list:
                        if brep is not None:
                            center_pl_list.append(self.get_center_plane([_.Location for _ in brep.Vertices]))
                        else:
                            center_pl_list.append(None)
                    return center_pl_list
                elif type(brep_list) is rg.Brep:
                    center_plane = self.get_center_plane([_.Location for _ in brep_list.Vertices])
                    return center_plane

            def get_center_plane(self, point_list):
                x, y, z = 0, 0, 0
                for point in point_list:
                    x += point[0] / len(point_list)
                    y += point[1] / len(point_list)
                    z += point[2] / len(point_list)
                center_point = rg.Point3d(x, y, z)
                single_vertex = list(zip(point_list, point_list[1:] + point_list[:1]))
                vector_list = [i - j for i, j in single_vertex]
                axis_list = vector_list[2:]
                object_plane = rg.Plane(center_point, axis_list[0], axis_list[1])
                return object_plane

            def RunScript(self, Brep):
                if Brep:
                    Brep_list_id = [str(_) for _ in Brep]
                    self.Guid_of_Brep = Brep_list_id
                    tree_brep_list = [_ for _ in self.transformation(Brep_list_id)]

                    self.set_diff_list = self.diff(Brep_list_id)
                    self._set_punlic_brep = [_ for _ in ghp.run(self.transformation, self.set_diff_list)]

                    True_Brep = map(lambda x: obj(x).Geometry(), Brep)
                    Edges_list = [_ for _ in ghp.run(lambda y: [_ for _ in y.Edges], True_Brep)]
                    handle_Brep = [_ for _ in ghp.run(self._first_handle, self.four_edge(Edges_list))]

                    zip_brep_list = map(lambda z: list(zip(self._set_punlic_brep, z)), handle_Brep)
                    res_bool_list = [self.collision_test(_) for _ in zip_brep_list]

                    _get_tree_id = map(lambda _zip: tuple(zip(_zip, self.set_diff_list)), map(self.get_index, res_bool_list))
                    zip_id_list = map(self.single_map_id, _get_tree_id)

                    origin_pl_list = [self._temp_fun(_) for _ in True_Brep]
                    sub_adjacent_pl_list = [self._temp_fun(self.transformation(_)) for _ in zip_id_list]
                    zip_pl_of_tree = zip(origin_pl_list, zip(*sub_adjacent_pl_list))
                    tree_of_angle = [_ for _ in ghp.run(self.get_angle, zip_pl_of_tree)]

                    Below_Angle, Right_Angle, Top_Angle, Left_Angle = zip(*tree_of_angle)
                    Below_Panel, Right_Panel, Top_Panle, Left_Panle = zip_id_list
                    return Below_Panel, Right_Panel, Top_Panle, Left_Panle, Below_Angle, Right_Angle, Top_Angle, Left_Angle
                else:
                    self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, 'Brep cannot be empty!')


        # 角点强排序
        class SortBuilt(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@角点重排序", "HAE_PointSorted", """Reorder the corners, and sort the irregular corners according to a certain rule""", "Hero", "Big_plug-in")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("00449ea9-31ef-4dbd-b15c-a37b9aa18d54")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Polyline as reference")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Surface", "S", "Original Surface")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Precision (refers to the distance between two points)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "New_Surface", "S", "Reordered Faces")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIcSURBVEhL7ZNNaxNRFIZfqB9JZ5yIUdQWLLpy509wVXfiB51OkgZSFNKPMJmGLIy0pSTQQhUVBHXlzxCE1o2GLiwo6KJFLVqoC8GFINWU6j2+d3IJxqF140bIA4c7897DOfeccy86dPiPEdftUpVKUmZm9hhpB3IxC1ePAu4+I+yOKpXiamJijuu6CoKf/N7gelPGx23jEpLAhYM2Mndpn2hC26DdAPot4xJF8vluVSzWpVoVrg3l+y+lWPwitZowybIa8h3t14OLSRvpVw5GxELqsw3vhY3UlvlfAvLdYcA/YdBqGDwIHvHEx7TGpAn+3wv1cvDsUm/2DDC4rIMx6K0jcMPK4hjoZdJFk6SmtTbCnvv+uiqXvzHoYSO34N5tmbwmz1OFH33WsMThzZmtFs0k2S1W9IEz6TJyEwZwaNuqUHhnpAhfx/w3Mjstj8+PvDZSBBvuR92uJK4cMFITU8F7VtBgq3gr2uHeA5mqyNLgWKMnPiwxeHfMVosYLvexgm0L3lqkAg17PWVmsMDhntCabhdv0sNw0KVg8dzx9GnAqzsY1b2+72DgkPZLIHvSQvqpmc11rUXgKffz9E/MLVL8X+H63dyiur5l2u8U3ASvJAc9qoNt8sSrHLA0g3sLu74JBtnLE0/zHaxy3aS9pVUll4sZF0O/ZSEza2NojcmYJLPCJJPA2b88zN9Q8/Ptg9qByEA7dPiHAL8A67X0N4KBVZIAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            Tol, F_Cur = None, None

            def point_filter(self, v_point_data):
                a_list = []
                b_list = []
                for _ in range(len(v_point_data)):
                    if abs(v_point_data[0].Z - v_point_data[_].Z) < self.Tol:
                        a_list.append(v_point_data[_])
                    else:
                        b_list.append(v_point_data[_])
                return (a_list, b_list)

            def sort_points(self, data):
                sort_points = []
                index_point = []
                for _ in data:
                    dict_data = ghc.SortAlongCurve(_, self.F_Cur)
                    sort_points.append(dict_data['points'])
                    index_point.append(dict_data['indices'])
                return sort_points, index_point

            def single_point_sort(self, data_of_array):
                index_list_arary = [_ for _ in range(len(data_of_array))]
                old_data = [_ for _ in data_of_array]
                single_array = [_[0].Z for _ in data_of_array]
                index_single_array = [_ for _ in range(len(single_array))]

                if len(set(single_array)) != 1:
                    dict_sort = dict(zip(single_array, index_single_array))
                    single_array.sort()
                    new_index = [dict_sort[_] for _ in single_array]

                    new_data = [old_data[_] for _ in new_index]
                    new_data[1].reverse()
                    new_data_list = list(chain.from_iterable(new_data))
                    return new_data_list

            def RunScript(self, Curve, Surface, Tolerance):
                self.Tol = 50 if Tolerance is None else Tolerance
                if Curve and Surface:
                    self.F_Cur = Curve

                    point_v_array = map((lambda x: [_.Location for _ in x.Vertices]), Surface)
                    np_point_list = map(self.point_filter, point_v_array)
                    new_point_index_list = map(self.sort_points, np_point_list)
                    new_point_list = []
                    new_index_list = []
                    for _ in new_point_index_list:
                        length = len(_)
                        new_point_list.append(list(_[:length // 2])[0])
                        new_index_list.append(list(_[length // 2:])[0])

                    sort_points_list = map(self.single_point_sort, new_point_list)

                    polyline_list = map(lambda x: rg.Polyline(x + [x[0]]), sort_points_list)
                    New_Surface = map(lambda x: ghc.BoundarySurfaces(x), polyline_list)
                    return New_Surface
                else:
                    pass


        # 标准矩形单元板
        class StandRectangularElementPlate(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@测试矩形单元体数据处理", "HAE_RectEle", """Original data processing of standard rectangular cell""", "Hero", "Big_plug-in")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("5ded5190-54e7-4ec2-87c0-e84a81fd8837")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Brep_Plane", "P", "Brep panel")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Below_Beam_Section", "BBS", "Cross section of lower crossbeam")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Right_Column_Section", "RCS", "Section of right column")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Upper_Beam_Section", "UBS", "Upper beam section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Guid()
                self.SetUpParam(p, "Left_Column_Section", "LCS", "Left column section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Transverse_Extension_Length", "TLEN", "Transverse extension length")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Vertical_Extension_Length", "VLEN", "Vertical extension length")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Upcut_Of_Column", "UC", "Upcut of column")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Below_Of_Column", "BC", "Column undercutting")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Upper_Beam_Of_LeftCut", "UBLC", "Left cutting of upper crossbeam")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Upper_Beam_Of_RightCut", "UBRC", "Right cutting of upper crossbeam")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Upper_Beam_Of_Avoidance", "UBA", "Avoidance of upper beam column")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Inside_Left_Section_Of_Column", "ILSC", "Left side of column inner section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Inside_Right_Section_Of_Column", "IRSC", "Right side of column inner section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Outside_Left_Section_Of_Column", "OLSC", "Left side of column outer section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Outside_Right_Section_Of_Column", "ORSC", "Right side of column outer section")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Below_Beam_Of_LeftCut", "BBLC", "Left cutting of lower crossbeam")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Below_Beam_Of_RightCut", "BBRC", "Right cutting of lower crossbeam")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Left_Col", "LC", "Left column")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Right_Col", "RC", "Right column")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Upper_Beam", "UB", "Upper crossbeam")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Below_Beam", "BB", "Lower crossbeam")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                p3 = self.marshal.GetInput(DA, 3)
                p4 = self.marshal.GetInput(DA, 4)
                p5 = self.marshal.GetInput(DA, 5)
                p6 = self.marshal.GetInput(DA, 6)
                p7 = self.marshal.GetInput(DA, 7)
                p8 = self.marshal.GetInput(DA, 8)
                p9 = self.marshal.GetInput(DA, 9)
                p10 = self.marshal.GetInput(DA, 10)
                p11 = self.marshal.GetInput(DA, 11)
                p12 = self.marshal.GetInput(DA, 12)
                p13 = self.marshal.GetInput(DA, 13)
                p14 = self.marshal.GetInput(DA, 14)
                p15 = self.marshal.GetInput(DA, 15)
                p16 = self.marshal.GetInput(DA, 16)
                p17 = self.marshal.GetInput(DA, 17)
                result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17)

                if result is not None:
                    if not hasattr(result, '__getitem__'):
                        self.marshal.SetOutput(result, DA, 0, True)
                    else:
                        self.marshal.SetOutput(result[0], DA, 0, True)
                        self.marshal.SetOutput(result[1], DA, 1, True)
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB/SURBVEhL7ZUxCoAwEASj/6/t7PyPWigoKKKVfkJ3IykkIYHEKtzAQK44dqucypLyB50UsIErPBNcYA0tmHzBG/YJcn+HFgxgg1ZP8Uxwe59fTABbpDBDCfAiAUEkIIgEBAkGdHqKx/ubmnvAFrFy/4BOeIlGyAaxDrCCWaDUA7ctdUgvR/O1AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._tol = 0.001
                self.__normal_total_section = None
                self.__normal_total_points = None
                self.t_len = None
                self.v_len = None
                self.__column_plane = None
                self.__beam_plane = None
                self.__normal_x, self.__flip_x = None, None
                self.__normal_y, self.__flip_y = None, None
                self.__dict_section_tips = {1: "Below_Beam_Section", 2: "Right_Column_Section", 3: "Upper_Beam_Section", 4: "Left_Column_Section"}
                self.__dict_tips = {1: 'Upcut_Of_Column',
                                    2: 'Below_Of_Column',
                                    3: 'Upper_Beam_Of_LeftCut',
                                    4: 'Upper_Beam_Of_RightCut',
                                    5: 'Inside_Left_Section_Of_Column',
                                    6: 'Inside_Right_Section_Of_Column',
                                    7: 'Outside_Left_Section_Of_Column',
                                    8: 'Outside_Right_Section_Of_Column',
                                    9: 'Below_Beam_Of_LeftCut',
                                    10: 'Below_Beam_Of_RightCut'}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def forced_stop(self, section_brep):
                tips = [_ for _ in range(len(section_brep)) if section_brep[_] is None]
                messages = [self.message1("{}为空".format(self.__dict_section_tips[_ + 1])) for _ in tips]
                return messages

            @staticmethod
            def general_methods_of_get_vector(curve, length):
                temp_line = curve.ToNurbsCurve().Extend(rg.CurveEnd.Both, length, rg.CurveExtensionStyle.Line) if length >= 0 else curve.ToNurbsCurve().Trim(rg.CurveEnd.Both, abs(length))
                pt_start, pt_end = temp_line.PointAtStart, temp_line.PointAtEnd
                res_vector = rg.Vector3d(rg.Vector3d(pt_end) - rg.Vector3d(pt_start))
                return res_vector, pt_start, pt_end

            @staticmethod
            def general_methods_of_get_extline(origin_curve, transform):
                return ghc.Transform(origin_curve, transform)

            @staticmethod
            def general_methods_of_extrude(geo, direction):
                return ghc.Extrude(geo, direction)

            @staticmethod
            def _general_methods_of_normal_vector(_srf):
                pts = [_.Location for _ in _srf.Vertices]
                center_pt = reduce(lambda pt1, pt2: pt1 + pt2, pts) / len(pts)

                single_vertex = list(zip(pts, pts[1:] + pts[:1]))
                vector_list = [i - j for i, j in single_vertex]
                axis_list = vector_list[2:]
                return rg.Plane(center_pt, axis_list[0], axis_list[1]).ZAxis

            @staticmethod
            def general_methods_is_brepflip(tuple_data):
                try:
                    if tuple_data[1] is True:
                        tuple_data[0].Flip()
                        return tuple_data[0]
                    else:
                        return tuple_data[0]
                except:
                    tuple_data.Flip()
                    return tuple_data

            def _general_methods_cut_brep(self, set_brep):
                passive_brep = set_brep[0]
                cutting_brep = set_brep[1]

                if type(cutting_brep) is not tuple:
                    result_brep = rg.Brep.CreateBooleanDifference(passive_brep, cutting_brep, self._tol)
                    if len(result_brep) == 1:
                        return result_brep[0]
                    else:
                        return [_ for _ in result_brep]
                else:
                    passive_brep = [set_brep[0]]
                    cutting_brep = set_brep[1]
                    result_brep = rg.Brep.CreateBooleanDifference(passive_brep, cutting_brep, self._tol)
                    if result_brep is not None:
                        return [_ for _ in result_brep]
                    else:
                        return None

            def __do_main_one(self, base_brep):
                faces, edges, points = ghc.DeconstructBrep(base_brep)
                avg_point = ghc.Average(points)
                below_base_line, right_base_line, top_base_line, left_base_line = ghc.Line(points[0], points[1]), ghc.Line(points[1], points[2]), ghc.Line(points[3], points[2]), ghc.Line(points[0], points[3])
                base_vector_x, base_vector_y = ghc.Vector2Pt(points[0], points[1], False)['vector'], ghc.Vector2Pt(points[0], points[3], False)['vector']
                base_vector_z = ghc.CrossProduct(base_vector_x, base_vector_y, False)['vector']

                self.__column_plane = ghc.ConstructPlane(avg_point, base_vector_x, -base_vector_z)
                self.__beam_plane = ghc.ConstructPlane(avg_point, -base_vector_z, base_vector_y)
                return below_base_line, right_base_line, top_base_line, left_base_line, base_vector_x, base_vector_y

            def _transfer_fun_beam_brep(self, beam_data):
                t_vector, point_s, point_e = self.general_methods_of_get_vector(beam_data[0], self.t_len)
                tr_brep, t_transform = ghc.Orient(beam_data[1], beam_data[2], ghc.PlaneOrigin(self.__beam_plane, point_s))
                ext_brep = ghc.Extrude(tr_brep, t_vector)
                return ext_brep, t_transform

            def _transfer_fun_column_brep(self, column_data):
                v_vector, point_s, point_e = self.general_methods_of_get_vector(column_data[0], self.v_len)
                tr_brep, v_transform = ghc.Orient(column_data[1], column_data[2], ghc.PlaneOrigin(self.__column_plane, point_s))
                ext_brep = ghc.Extrude(tr_brep, v_vector)
                return ext_brep, v_transform

            def __do_main_two(self, handle_data):
                zip_data = zip(handle_data[:4], self.__normal_total_section, self.__normal_total_points)
                beam_list_data = zip_data[0: len(zip_data): 2]
                beam_data_hadle = zip(*map(self._transfer_fun_beam_brep, beam_list_data))

                column_list_data = [_ for _ in zip_data if _ not in beam_list_data]
                column_data_handle = zip(*map(self._transfer_fun_column_brep, column_list_data))

                section_ext_brep = beam_data_hadle[0] + column_data_handle[0]
                all_transform = beam_data_hadle[1] + column_data_handle[1]

                below_beam_tr, upper_beam_tr = beam_data_hadle[1][0], beam_data_hadle[1][1]
                right_column_tr, left_column_tr = column_data_handle[1][0], column_data_handle[1][1]
                return section_ext_brep, all_transform, below_beam_tr, right_column_tr, upper_beam_tr, left_column_tr

            def __do_main_three(self, sub_dict_data):
                key = sub_dict_data.keys()[0]
                value = sub_dict_data.values()[0]

                origin_line = key
                tr_of_list = value[0][0]
                base_line_of_list = value[0][1]
                ref_vector = value[1]

                geo_list = map(self.general_methods_of_get_extline, [origin_line] * len(tr_of_list), tr_of_list)
                geo_vector = zip(*map(self.general_methods_of_get_vector, base_line_of_list, [self.t_len] * len(base_line_of_list)))[0]
                geo_section = map(self.general_methods_of_extrude, geo_list, geo_vector)
                geo_section_normal = [self._general_methods_of_normal_vector(_) for _ in geo_section]
                bool_list = map(lambda rad: False if (90 >= math.degrees(rg.Vector3d.VectorAngle(rad[0], rad[1])) >= 0) or
                                                     (360 >= math.degrees(rg.Vector3d.VectorAngle(rad[0], rad[1])) >= 270) else True, zip(geo_section_normal, ref_vector))
                res_section = map(self.general_methods_is_brepflip, zip(geo_section, bool_list))
                return res_section

            def __do_mian_four(self, zip_brep):
                sub_zip_brep = zip(zip_brep[0], zip_brep[1])
                result_brep = ghp.run(self._general_methods_cut_brep, sub_zip_brep)
                if all(result_brep) is True:
                    return result_brep
                else:
                    return ghp.run(self._secondary_cutting, sub_zip_brep)

            def additional_fun_create_brep(self, origin_line, tuple_var, towards_left, towards_right):
                base_line = tuple_var[1]
                tr_values = tuple_var[0]
                ex_geo_list = map(self.general_methods_of_get_extline, [origin_line] * len(tr_values), tr_values)
                ex_geo_vector = zip(*map(self.general_methods_of_get_vector, base_line, [self.t_len] * len(base_line)))[0]
                ex_geo_section = map(self.general_methods_of_extrude, ex_geo_list, ex_geo_vector)
                if len(ex_geo_section) == len(towards_left) == len(towards_right):
                    close_ex_geo_section = [ghc.CapHoles(_) for _ in ex_geo_section]
                    cut_brep_left = [_ for _ in ghp.run(self._general_methods_cut_brep, zip(close_ex_geo_section, towards_left))]
                    cut_brep_right = [_ for _ in ghp.run(self._general_methods_cut_brep, zip(close_ex_geo_section, towards_right))]
                    return cut_brep_left, cut_brep_right
                else:
                    return self.message2("The number of Brep of the upper crossbeam avoidance cutting is inconsistent!!!")

            def _secondary_cutting(self, tuple_sec_brep):
                passive_brep = tuple_sec_brep[0]
                cutting_brep = tuple_sec_brep[1]

                count = 0
                temp_brep = passive_brep
                while len(cutting_brep) > count:
                    cut_brep = rg.Brep.CreateBooleanDifference(temp_brep, cutting_brep[count], self._tol)
                    if cut_brep is not None:
                        temp_brep = cut_brep[0]
                        count += 1
                    else:
                        count += 1
                result_brep = [temp_brep]
                return result_brep

            def RunScript(self, Brep_Plane, Below_Beam_Section, Right_Column_Section, Upper_Beam_Section, Left_Column_Section, Transverse_Extension_Length, Vertical_Extension_Length, Upcut_Of_Column, Below_Of_Column, Upper_Beam_Of_LeftCut,
                          Upper_Beam_Of_RightCut, Upper_Beam_Of_Avoidance, Inside_Left_Section_Of_Column, Inside_Right_Section_Of_Column, Outside_Left_Section_Of_Column, Outside_Right_Section_Of_Column, Below_Beam_Of_LeftCut, Below_Beam_Of_RightCut):
                try:
                    self.t_len = 200 if Transverse_Extension_Length is None else Transverse_Extension_Length
                    self.v_len = 200 if Vertical_Extension_Length is None else Vertical_Extension_Length
                    if len(Brep_Plane) != 0:
                        base_data_list = map(self.__do_main_one, Brep_Plane)
                        origin_section_data = [eval(_) for _ in self.__dict_section_tips.values()]
                        if all(origin_section_data) is False:
                            self.forced_stop(origin_section_data)
                        else:
                            self.__normal_total_section = origin_section_data
                            self.__normal_total_points = map(lambda sec: ghc.Seg_GhCommon.SEGGetUserDic(sec, "pln").value, self.__normal_total_section)
                            temp_data_of_brep = zip(*ghp.run(self.__do_main_two, base_data_list))

                            self.__normal_x = zip(*base_data_list)[4]
                            self.__flip_x = [-_ for _ in self.__normal_x]
                            self.__normal_y = zip(*base_data_list)[5]
                            self.__flip_y = [-_ for _ in self.__normal_y]

                            zip_do_handle_data = zip(temp_data_of_brep[2:], zip(*base_data_list)[:4])
                            total_of_dict_data = {1: {Upcut_Of_Column: [zip_do_handle_data[2], self.__flip_y]},
                                                  2: {Below_Of_Column: [zip_do_handle_data[0], self.__normal_y]},
                                                  3: {Upper_Beam_Of_LeftCut: [zip_do_handle_data[3], self.__normal_x]},
                                                  4: {Upper_Beam_Of_RightCut: [zip_do_handle_data[1], self.__flip_x]},
                                                  5: {Inside_Left_Section_Of_Column: [zip_do_handle_data[3], self.__normal_x]},
                                                  6: {Inside_Right_Section_Of_Column: [zip_do_handle_data[1], self.__flip_x]},
                                                  7: {Outside_Left_Section_Of_Column: [zip_do_handle_data[3], self.__normal_x]},
                                                  8: {Outside_Right_Section_Of_Column: [zip_do_handle_data[1], self.__flip_x]},
                                                  9: {Below_Beam_Of_LeftCut: [zip_do_handle_data[3], self.__normal_x]},
                                                  10: {Below_Beam_Of_RightCut: [zip_do_handle_data[1], self.__flip_x]}}
                            temp_flip_handle_brep = []
                            for k, v in total_of_dict_data.items():
                                if v.keys()[0] is None:
                                    temp_flip_handle_brep.append(self.message2("{} Curve is empty".format(self.__dict_tips[k])))
                                else:
                                    temp_flip_handle_brep.append(self.__do_main_three(v))
                            col_inside_left = map(self.general_methods_is_brepflip, temp_flip_handle_brep[4])
                            col_inside_right = map(self.general_methods_is_brepflip, temp_flip_handle_brep[5])
                            if Upper_Beam_Of_Avoidance is not None:
                                upper_col_avo_left, upper_col_avo_right = self.additional_fun_create_brep(Upper_Beam_Of_Avoidance, zip_do_handle_data[2], col_inside_left, col_inside_right)
                            else:
                                upper_col_avo_left = upper_col_avo_right = None
                                self.message2("Upper_Beam_Of_Avoidance Curve is empty")

                            temp_flip_handle_brep.insert(4, upper_col_avo_right)
                            temp_flip_handle_brep.insert(4, upper_col_avo_left)
                            left_col_brep, right_col_brep, upper_beam_brep, below_beam_brep = zip(*temp_data_of_brep[0])[::-1]

                            left_col_cut_brep = zip(*temp_flip_handle_brep[0: 2])
                            right_col_cut_brep = zip(*temp_flip_handle_brep[0: 2])
                            upper_beam_cut_brep = zip(*temp_flip_handle_brep[2: 6])
                            below_beam_cut_brep = zip(*temp_flip_handle_brep[10:])

                            wait_passive_brep = [left_col_brep, right_col_brep, upper_beam_brep, below_beam_brep]
                            wait_cutting_brep = [left_col_cut_brep, right_col_cut_brep, upper_beam_cut_brep, below_beam_cut_brep]

                            set_zip_brep_tuple = zip(wait_passive_brep, wait_cutting_brep)
                            result = ghp.run(self.__do_mian_four, set_zip_brep_tuple)
                            Left_Col, Right_Col, Upper_Beam, Below_Beam = result
                            return ght.list_to_tree(Left_Col), ght.list_to_tree(Right_Col), ght.list_to_tree(Upper_Beam), ght.list_to_tree(Below_Beam)
                    else:
                        self.message1("Brep is empty and cannot be operated!!")
                finally:
                    self.Message = "Standard rectangular cell battery module"

except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Big_plugin_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("86c4ead2-84fa-4dff-a70f-099478c2ccca")
