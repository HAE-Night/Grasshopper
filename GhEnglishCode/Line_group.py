# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Brep_group
# @Time : 2022/11/5 16:32

import init__

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import ghpythonlib.parallel as ghp
import ghpythonlib.components as ghc
import Grasshopper as gh
import ghpythonlib.treehelpers as ght
import re
import socket
import time
import getpass
import base64
from itertools import chain


def decryption():
    hostname = socket.gethostname()
    designer_names = init__.designer_database
    origin_data_list = []
    now_time = int(time.time())
    for name in designer_names:
        try:
            with open(r'C:\Users\%s\AppData\Roaming\Grasshopper\Libraries\{0}-KEY.licence'.format(
                    name) % getpass.getuser(), 'r') as f:
                data = f.read()
                origin_data_list.append(data)
        except:
            pass
    if len(origin_data_list) == 1:
        data_list = [i for i in origin_data_list[0]]
        re_reversed_list1 = data_list[0:10]
        re_reversed_list1.reverse()
        re_reversed_list2 = data_list[10:]
        re_reversed_list2.reverse()
        result_list = re_reversed_list1 + re_reversed_list2
        result = ''.join(result_list)
        try:
            origin_data = str(base64.b64decode(result))
            origin_list = origin_data.split('-')
        except TypeError:
            return False
        if origin_list[1] == hostname.replace("-", "%") and int(origin_list[2]) > now_time:
            return True
        else:
            return False
    elif len(origin_data_list) > 1 or len(origin_data_list) == 0:
        return False


Result = decryption()
try:
    if Result is True:
        # 曲线取值
        class DTS_Get_Vale(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲线取值", "HAE_DTS_Get_Vale",
                                                                   """Decomposition line segment and subscript value (S is the boundary, V is the point)""",
                                                                   "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("50fd4090-ae7a-4e99-8ef2-075c8be0ac09")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Curve", "C", "Curve to be exploded")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Index", "I", "Subscript of exploded boundary or point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "S_V", "B", "Select a boundary line or point. By default, it is not selected as a boundary line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data1", "D1", "The first group of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data2", "D2", "The second set of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data3", "D3", "The third group of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data4", "D4", "The fourth group of data")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "data5", "D5", "The fifth group of data")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEESURBVEhL7dTPKsRhFMbxcw2MEjsLFmaJ/EkhUSSKhR0LaixYiRKiRLkQpUhRrocFFi6B8H1OM71v78qcncm3PovzNDO/mqmx/37bDu6w5VdqGw94DLhHDbaK78wiVLlH2XkxHEKVe5T14aV+PKMHKt+jnuB1YBrtfqUqmMVcwAza0CJN4hjjfqUmcIqzgBOMwaaQ/zCjUHpovkfZZTHoyarco/xraRyfGILS/oX8xc36gDeCXQz6lRrGPg4C9jCAFqkbC+j0K9WFJSwH6E/TP6+Kd+hHeUMvVD8ae9Qr7CIb5Aiq3KNspRjmoco9ytvEFdb9Sm3gGre4aYJer/et4U9n9gNMCfCsAWct1wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            @staticmethod
            def get_v_s(array_list):
                c_list = [i for i in array_list]
                point = []
                for i in c_list:
                    point.append(i.PointAtStart)
                    point.append(i.PointAtEnd)
                p_list = list(set(point))
                p_list.sort(key=point.index)
                p_list += [p_list[-1]]
                return c_list, p_list

            @staticmethod
            def subscript_value(mod_list, list_data):
                new_list = []
                for index, i in enumerate(list_data):
                    new_list.append(mod_list[i])
                return new_list

            @staticmethod
            def index_erreor(P_Slist):
                if len(P_Slist) < 5:
                    P_Slist = P_Slist + [None] * (5 - len(P_Slist))
                    return P_Slist
                else:
                    return P_Slist

            def RunScript(self, Curve, index, S_V):
                if Curve:
                    curve = Curve.DuplicateSegments()
                    C_List, P_List = self.get_v_s(curve)
                    I_List = [list(map(int, re.split(r"[.。!！?？；;，,\s+]", i))) for i in index]
                    New_C_List = self.index_erreor(
                        [self.subscript_value(C_List, I_List[i]) for i in range(len(I_List))])
                    New_P_List = self.index_erreor(
                        [self.subscript_value(P_List, I_List[i]) for i in range(len(I_List))])
                    if S_V == 'S' or S_V == 's' or S_V is None:
                        data1, data2, data3, data4, data5 = New_C_List
                        return data1, data2, data3, data4, data5
                    elif S_V == 'V' or S_V == 'v':
                        data1, data2, data3, data4, data5 = New_P_List
                        return data1, data2, data3, data4, data5
                    else:
                        pass
                else:
                    pass


        # 偏移多边曲线
        class PlineOffset(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@折线偏移", "HAE_PlineOffset", """Segment offset of broken line, three different offset modes""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4121d1e6-b3a6-4e53-a4e6-c2346dbb6703")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Original curved line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Distance", "D", "Offset distance. Enter several offset distances for several folds")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Simply", "S", "The port is closed by default, and it is normal offset when it is turned on (t)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Double", "DU", "The port is turned off by default, and when it is turned on (t), the first and last lines of polylines before and after offset will be connected")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Rescur_list", "R", "Final polyline")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIOSURBVEhLtZa9a5NRGMUDikUtQgtiV9sUIZA0398lXZ0stQl0cXF1URQk4KLoJDiIpdX/QeoqCnZooYXODg5FoYMlVSndCsbfKccMmpY3cj3wcN97bp7zPPfc9yaJ/Q+kUqnzlUplNp/Pj5sKh2azeSqXy72vVqtdxm+mj0ehUBgrFov30un0VVMnAtFz2Wz2kJyuipjuD3ezXqvVukogcdpLxwJbFkulUpfGvpL72nR/JBKJM4h2lECikrTtN4ytcrk86o/1wGdf1et1NfKAhi6YPhkIXkNwh6R9YolCuxygCv5UMeIG8YL5OkUl3nZqdCDQVHImk4nbthlZwdgRrx2qKOJvnTIYZIfsQeCpqSM0Go3TFHquw9Q5/bk+EEheIz572kM8Hh+iyEN28ziy7/2AwC3ZgdgVU2FBd5flNbu4ayo82MUnCmx5Gh6IP9KFYyeXTP0b8Pk6Yi1Pe+BNSut15GtjwdTgwIbbElHw/IyOpxAe063WOoW/MN9inDhKGBSILuswZcXvS6Q7AH+A6EfG7+IZtyk67LToQKTt7je5uXOM88R94iWxpoIKnmXVRadFA52dxf8OyR9M/QXWnlBgg/Gmqeig4zv+oSiaCgddebz+gUWrpsICa9o6PAqUTIVBMpkcwZJ3Ft80HQ6ItuS7XkWe9/SPwEthwKs2yQ72VIQCK/pB8VIAxGK/ADVGu47UwxZAAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = False

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def offset_curve(self, tuple_data):
                single_data, dis = tuple_data
                new_offset = ghc.OffsetCurve(single_data, dis, None, 1)
                return new_offset

            def find_closest_pt(self, data_list):
                count = 0
                colse_pts = []
                while len(data_list) > count:
                    one_index, two_index = count, count + 1
                    if two_index < len(data_list):
                        single_pt = rs.LineLineIntersection(data_list[one_index], data_list[two_index])
                        if abs(single_pt[0].DistanceTo(single_pt[1])) < 0.001:
                            colse_pts.append(single_pt[0])
                    else:
                        if self.factor is True:
                            two_index = len(data_list) - two_index
                            single_pt = rs.LineLineIntersection(data_list[one_index], data_list[two_index])
                            if abs(single_pt[0].DistanceTo(single_pt[1])) < 0.001:
                                colse_pts.insert(0, single_pt[0])
                    count += 1
                return colse_pts

            def double_line(self, origin_line, offset_line):
                start_pts = ghc.Discontinuity(offset_line, 1)["points"]
                end_pts = ghc.Discontinuity(origin_line, 1)["points"][::-1]
                set_of_poly_list = start_pts + end_pts
                return ghc.PolyLine(set_of_poly_list, True)

            def RunScript(self, Curve, Distance, Simply, Double):
                try:
                    res_poly_line = None
                    if Curve is not None:
                        Simply = 'F' if Simply is None else Simply.upper()
                        self.factor = Curve.IsClosed
                        if Simply not in ['T', 'F']:
                            self.message1("Please input the correct letter at S end!!")

                        if Simply == 'F':
                            explode_curves = ghc.Explode(Curve, True)["segments"]
                            if len(Distance) == len(explode_curves):
                                zip_offset_curve = zip(explode_curves, Distance)
                                offset_list = ghp.run(self.offset_curve, zip_offset_curve)
                                closest_pt = self.find_closest_pt(offset_list)
                                if len(closest_pt) < len(offset_list):
                                    closest_pt.insert(0, offset_list[0].PointAtStart)
                                    closest_pt.append(offset_list[-1].PointAtEnd)
                                res_poly_line = ghc.PolyLine(closest_pt, self.factor)
                            else:
                                self.message1("Distance data list must be equal to the number of multi line segments!")
                        else:
                            res_poly_line = ghc.OffsetCurve(Curve, Distance[0], None, 1)
                        Double = 'F' if Double is None else Double.upper()
                        Rescur_list = self.double_line(Curve, res_poly_line) if Double == 'T' else res_poly_line
                        return Rescur_list
                    else:
                        self.message2("Please enter a hem")
                finally:
                    self.Message = 'Line segment offset'


        # 线段点线转换
        class Dotted_Line_Conversion(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@点线转换", "HAE_StartToStrat,EndToEnd",
                                                                   """Start and start connection, end and end connection of curve set""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("8f4035c7-a253-4efb-8a12-c39d503bf27d")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Multiple curves")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Start_Curve", "S", "Line segment of starting point")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "End_Curve", "E", "End line segment")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Result_Curve", "A", "All segment sets")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Tree_Result", "T", "Line segments are output in a tree structure")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKRSURBVEhL7ZVdSxRRGMcn7YXuoigtKbtQdua8zKys2gqFppvRi0ZQmIEKBQUR4VWQXvgJuugTdNvMOTOzb5Rd+QW67CbBnT0zs7rr2ht+gOmc5RCoa6640U0/+F88589zDnPO8zyj/GdfdL1fPoYI6wWO32/kNvpV20fSag7Q9vugHcxCNxiCueqQRtgcMP2T0j44qh0kdVK4JENFNYu3dOL14Gx5BNjBcD1ppDiiZ6rD2GIJZSFqkan1Uc1wQCfB7wMgKd7Gpo9Rutorrq6esLuagNlqn+awO4gUX6BMuU2m7wRYYRxS/yWww3Gcro5DyuaNt94Jae8JdMPz0PKeDS4sHZZL24iiFsNdu6jRoDueW++Opdk56TQMsv27iHqqDJsPpmEKu/w99guw2GW8uPkQmmxCz3+bQmRFl9YWAA2eqE54SoaNIxJRtqqizEobypYHAPEnpVVDbAoIm4GEjcql3dFI2ANIOMOrY0pf/DktSlDcbfK1f1z4hvmlAzvBDeTwquM+zG1M8+J4rNpesrbBn9AoSyHiPxIPDKzPRxOfoiOKZbWKL9BzX5Fh+h3YLV3hTfngvhW1Cn9wKdqlarbRZS6fBjZ7KsMt1JpwcXOCN9c9/OHHJO9yKK3G0XiTQepdlWHzge8KBuLjQYYNA6zSBZwOY0Ki2eTyTsQ0BdR/HudXJZf2BFheu+h46K6NwSwX9eb1j2tnpL0TjRY6ocVmNerdBPnvcT5djXriG8eBG8Y1Pgx5BV2X6Qo/bCzGp4EM69P1hv8XeAnCbGVU1HVdOUKVUfHvQDa7JlNrB2j51U4ZHhzVLp5FNHiF0+UUzpdTkHhzIF9pl3YTiKJD0FnV9PR6jxCipb836P4BivILbfdLrpUGntoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def get_points(self, origin_curves):
                """
                分解线段，使得线段集的起点和起点连接，终点和终点连接
                """
                start_points = [s_point.PointAtStart for s_point in origin_curves]
                end_points = [e_point.PointAtEnd for e_point in origin_curves]
                format_start_points = list(zip(start_points, start_points[1:] + start_points[:1])[0:-1])
                format_end_points = list(zip(end_points, end_points[1:] + end_points[:1])[0:-1])
                start_lines = [rg.LineCurve(s[0], s[1]) for s in format_start_points]
                end_lines = [rg.LineCurve(e[0], e[1]) for e in format_end_points]
                all_lines = start_lines + end_lines
                tree_branch = [start_lines] + [end_lines]
                tree = Grasshopper.DataTree[rg.LineCurve]()
                for sub, leaf in enumerate(tree_branch):
                    tree.AddRange(leaf, Grasshopper.Kernel.Data.GH_Path(sub))
                return start_lines, end_lines, all_lines, tree

            def RunScript(self, Curves):
                if Curves:
                    Start_Curve, End_Curve, Result_Curve, Tree_Result = self.get_points(Curves)
                    return Start_Curve, End_Curve, Result_Curve, Tree_Result
                else:
                    pass


        # 最近点连线
        class PCLINE(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@最近点连线", "HAE_PCLINE", """The nearest segment from the geometry to the specified segment""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("7f05f3bb-8ff1-4a7d-8c6e-315f0bb6bf69")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "A geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "RefCurve", "C", "curve")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Line", "L", "The line between the geometric object and the nearest point of this line segment")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Close_Point", "P", "Nearest point")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAC8SURBVEhL7c4xDgFBFIDhpdNrFUIlEkJBI1xA4Qg6jWh0DqCj2U7vBiqlQi0OIApR6ESl4X8zppCdlek070++7MzuvOxEmqb9pxw6qJpdeDW07DK9Ck54fcQIaQU3s0ce3na4oYsxZECesu95yPsp5NwcAzywRqIMnliane0Md7NfrnDJj+52mWwL+djHDDI8RANND3k/gpyboI0LNvBWwhHuZnKbkBZwMwcUkFoWdRTNLrwyZE7TtK+i6A0ySS+PMwgz8wAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self._switch = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def __get_line_point(self, curve, point):
                self._switch = False
                recent_par = curve.ClosestPoint(point)[1]
                nearest_point = curve.PointAt(recent_par)
                return nearest_point

            def __get_line_curve(self, cur_one, cur_two):
                self._switch = True
                line_data = [cur_one.ClosestPoints(cur_two)[1], cur_one.ClosestPoints(cur_two)[2]]
                return line_data

            def RunScript(self, Geo, RefCurve):
                try:
                    if Geo and RefCurve:
                        new_point = None
                        if isinstance(Geo, (rg.Line, rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve)) is True:
                            new_point = self.__get_line_curve(Geo, RefCurve)
                        elif isinstance(Geo, (rg.Point3d)) is True:
                            new_point = self.__get_line_point(RefCurve, rg.Point(Geo).Location)
                        else:
                            self.message1('The battery does not support this geometric type!')
                        Line = rg.Line(new_point[0], new_point[1]) if self._switch is True else rg.Line(new_point, rg.Point(Geo).Location)
                        Point = new_point
                        return Line, Point
                    else:
                        self.message2('Please ensure that the parameters are correctly connected!')
                finally:
                    self.Message = 'Nearest point connection'


        # Curve
        class VectorLineTaking(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "ZN@PDWL", "ZN_VectorLineTaking", """Draw straight line in point direction.""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("69142382-49fc-4abe-8502-b1c7b585b980")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "Starting point of straight line")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Direction", "D", "Line size and direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Whole", "W", "Two terminal direction (default open, t), close input f")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line", "L", "Generated Lines")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACWSURBVEhL7dYxCsJAFEXRXyhBMREEETdkkz42Yq+LsrKxzArchpWV6dyD3hexEKZ8KYS5cCCZ4jNVfuKfm2D0efS1xgEXXFHAWoUnXjjrwF2DB27Y68DZDrr5BjMsYOs7vO7fzOXhyfLwZHl4sjz8pxXm2GKQmx9xRwd9cu210M21MEodOJtCO/QEbaIlrI1h/wOIiHgDjy0m97DfZzoAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def create_line(self, start, vector):
                if self.factor is False:
                    line = rg.Line(start, vector)
                else:
                    line = rg.Line(rg.Line.PointAt(rg.Line(start, vector), 1), -vector * 2)
                return line

            def RunScript(self, Point, Direction, Whole):
                Direction = rg.Vector3d(0, 0, 1) if Direction is None else Direction
                Whole = 't' if Whole is None or 'T' == Whole.upper() else 'f'
                if Point:
                    self.factor = True if Whole == 't' else False
                    Line = self.create_line(Point, Direction)
                    return Line
                else:
                    pass


        # 求线长度
        class LineLength(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@求线长度", "HAE_GeneratedLines", """Find the line length and reserve the specified decimal places.""", "Hero",
                                                                   "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c683174a-8426-4e49-9fa3-0d986603bb70")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "List of line segments for length")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Decimal", "N", "Retain * decimal")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Length", "L", "segment length.")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANNSURBVEhLrVTLLmRRFK3v8AXeRAwxQCQ1ljAy8AOGBgbMDNpIIkIiEYTqSKs2oNXjFtV1CYkwEIJU6Q7VjY563Fe9H6vP3uWWQqFb7GQN9lnnrHXO3vtei81ms66vr39aWlr6cJCu5bPNNu7z+bBi/4ovKx8L0rUsLCyMfnO4cOq/RODnL/h/BP8LdObi8vd9fnW/FsT5RRAOlweWubm5Uae0iWw2j/cHnX1+3rMlXsAGbg9i8aQwySKdTr+JTCaDXC6HoaEhtLW1wWq1IpFI8BrxWcEnU2lIm98fDIxYgg+mUql/AoUYEFgsFvT393Nuchlhkkim3m9Asbe3h87OTnR0dMDpdPKayb9ikH4kVIpkMsmg8Hq9qKysxP7+PlZXVxEKhXjdjLTY/8xAN+Kifg9C5UCxsbGBqqoqHBwccE5BBvPz85ienobD4eBexhNJYeB924CaZ4rb7XZUV1fj+PiYc+JI7Pr6mktF/ZiammLumYGmx0QpCoJPQbG4uIja2lr4/X7O4/E4g+L8/BxdXV2or69ns3w+J6Yy8bIBHczn81x7ipmZGTQ2NuLq6orzUnEqVUNDAyYnJzEyMsJr9OKiwQIZiC9O1QxBFMRpms7OznjzxMQEmpubcXNzw3ksFmNQ7OzscLOp6RS3t7fFshqxOCRPGQMi6eYDAwMYHBxEa2srwuEwC5SKS5LE4ru7u5zTxegjI76sgaLqgojz13h0dISKigr09PRA13Uul2EYRfG1tTWepMPDQ85NzgSZ6UbssUFU0QRREBgeHuaJaG9vRzAY5EkhEYrl5WXU1NTg5OSEc1p/CjLRdANu04D+epGoWnSXZRkul4trqyhKsdliIFBXV4dAIMA5va4cyETV9HIGOjRN4xubcXp6itnZWf6QSieJ9pUTJ5QxkBCOKIIoGJigIPGmpiZ0d3fzJFE/VFV9tO8pyERRNWGw9WAQCkcFofFhU4Aa3tLSwv2gPycFlczc8xLobFRRHxvchSKCUFmAQM+kue7t7UVfXx/GxsZ4/EjA3PMSaE8kqrxuQIhGo6IfGb45lYbyUv4lFA2kEoM/dxFRtwLxAMpNlK6/DipPSPTURQaituOyvA33pg/SlvxhcG/KkLd38Bc5RMF1fyEJ8AAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def RunScript(self, Curve, Number):
                digit = ".%uF" % Number if Number else ".1F"
                Length = [format(float(crv.GetLength()), digit) for crv in Curve]
                # return outputs if you have them; here I try it for you:
                return Length


        # 根据线长排序
        class ZYLLenght(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@根据线长排序", "HAE_LLenght", """Sort according to the length of the curve, from small to large.""",
                                                                   "Hero",
                                                                   "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e93bc482-0f62-42b6-bf53-97caa94435bc")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Segments to be sorted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "Sorted Segments")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Lenght", "L", "Length after sorting")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAOlSURBVEhLxZXbT1NZFMYbEv4DXiCEF3wxmZg4D8rDxHgjSmIiGi/jAyNGnTgXmakYHCKGKlLLjHHG6JMJMQYTBiqioyYOmZmA1jIRCBm17TmnLVRpeYAEWjic3k77zVq7tFAKatDElXznsvfK/u291tp7Gx4/Gdrp8vot9ucvszW4RKvod7j9FsPz4VdXkwAmJyc/upI0sGFg2GHmH1mW4HQ6P5pkWRaQDMAlKxh57cfoe8j3JoDXYyn50m9qS7fzOC5JWQBMTEzA7fUhkUiSEhSwlCVpjfyfI1o6h5U9+S1Ej0w7fSgeL3jcRYBRxOJxxGIxSJIEh8OBcDiM+HxbWgy9casTP9abYbJcx+VrN3G85iz+6rXjz79tOFj9g/Bxe0eWADyj0Gl24bCG4uJi5OfnY3x8nOYDRKPRjNjON/+Cit2HcPjYSdTUnsUXmyvQ2XUf7Z3dWLuuTPisDNA0FBYWIi8vb0WA+effsOfgEXz93Wmcrr+A7RV70XXvETrvPsDnZVuFTw5AIUBc16Fpc5kVBAIB4RyJRDJia54HHP+WAecF4E73Q1rFHwTYInzcnk8B4CTPzWUDOGGc7LTYmlsIcKA6BfgpDXiAjjv33wGIEUBVMwC/378ioFIAalFLgG2LARvTgCVlqhAxSmWoqrNZAK57jRKfFtvFll9zAFZK8GJAzj5Q3CMU4yhmZxcAY2Nj0CkvHLa02C5aUoBj3xDgjEkAOP6/W+9hPQF4s70FMPPBAN7hywLC4QhmZkIoKioSAJXysZw1Wa6gcv9hATjFgJ17UhttHqDTEhT3IsAkfcgE0LQwQqEgSkpKxEarq6tDU1MTTCYTGhsb0dramgJcuoLd+77C0RNGGOsasW1HpZh9e8ddrN+wGXFawjIAL4VAQ3B6GgUFBTAYDDkqLS0VgIYLLdi+60scqv4eJ2rqsXFTBdrau3DrthVrPitDTIcYLxugeCn+KqYJUFVVhfLy8hwZjUZx4PUPvMDDnqfo6f0Xvc+G0P3oHzgkL1463ejo7sGsOgdJ8WQDJAJMB4MIkvgEzTmiSTw4TyBCB6Iej9I/n08RJHTeoKpQMqFjinwk2b0A4MRyDlSqEq71UChEyZ7JFbVz37sUDIboApsHDP8nmQcHB+FwybD1D+CJrV/cWgpdQKuV7PGJ8cSNZusfMjc0nENfX5+oGq6YAB3TTpdr1XKRMndyn23gqt1uh8/nQ1tbG6xWK6ampkTnhyqZTOJ/lvFWWS2o6H0AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def bubbling(self, Curve):
                Length = [i.GetLength() for i in Curve]
                for i in range(1, len(Length)):
                    for j in range(0, len(Length) - 1):
                        if Length[j] > Length[j + 1]:
                            Length[j], Length[j + 1] = Length[j + 1], Length[j]
                            Curve[j], Curve[j + 1] = Curve[j + 1], Curve[j]
                return Curve, Length

            def RunScript(self, Curve):
                Faces, Length = self.bubbling(Curve)
                return Curve, Length


        # 指定线段 取顶线底线
        class ZLine(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@指定线段", "HAE_ZLine",
                                                                   """In the line segment list, take the specified line segment (top line or bottom line) according to the Z coordinate of the line segment And unifies the direction of the line.""",
                                                                   "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("4904712b-7881-400e-a4d6-0b53069c48bc")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Line()
                self.SetUpParam(p, "Lines", "L", "Line List")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Dir", "D", "True - unifies straight lines into positive direction ->->; False: Unify the line as negative direction<-<-. The default is False.")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line1", "T", "Final top line")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Line2", "Endline", "Specify line segments")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANUSURBVEhLvZbLTxNRFMb9G+AfUBKFGDE+tizZGBITEpduSdwYdiaG4MqwMAGsLS8fsZ3SdgoW8BkBF4D4oFBpS9tpa6el4CO0RoFEHn193nPK9AHixoZJTs453733+93OTOb22PhbzyV3ePXOzJy34uEVvsfmPQFdNpdDMpmseOSErwAoHQnRhEJBBAKBigX5EYQByWQCgeBnqPFviFYgyIf8yDf/C9bWEI4sI5PNAdkscv8RtJ58yC+RWCsFxLCbSuPglUMqldqry6/DdPIhvzxgUQBEoQEWXG68ffcRM7MfOa9+/c5GK6tfseRXRAThExFf+cJ6bHlFzP2AGTGX5seWV4WeRuhztBwQUZeRymRx+cpVnDx9HnVnLuL4qXr03Jd4VzdvdaCm7hyPnRD6tes3WO99IO3Nv4Ca2rNov93N+gFAOBJFKp3Be6cXFquMkdFR3OsZwNOXb3iBaymMR0YLrDYZOkM/LMPPWQ9GVmCxPYHD4cDAw8ewDD1lPQ+gh7wPMP1+ASZJwtCQjG6dHmMvJnjBoi8sdAuG7DIMvf2wDT9j3R+KwWS2wC5b0ds/gEF5lPUDABLoGUy9W4DRJMEujLruFgGfvCE8Ng1Clm3Q9/TBurdTAhgFWLZZ0dM3APO/ADu7KQGYLwOMPh/nBS5vUOhFgHYrfMGoAFhLACOsHzUgwcL2zi6mZudhKgAMRYBnH8A+xvrSPoBkGxHfIAKoRw5QsbW9cwAw8uw1G7k8ijDSAP0Y1ACKCqM5D+hlgEN8LXIIhlUkSwEk/N7a5mcgSWbxmtrRpTPAMfaKjegZ8OsowAYBMAsjugggDdrEa2pjgNEyjHQm83dAdXV1RSKVThcBcwVAhAdbWlrgdrvR2dnJtaqqhaxFqa6F1pPHxsYm+5UBlFAe0NzczJNdLhf0ej3XmkZZi8N68vj58xf7FQCbm0SM8mBDQwNPbmpqwuTkJNeaptVaT9npdJb15LG+vp4H0IGz6I90TE9Pw+3182BtbS1PplxfX1+otayFz+dDW1sb65SpJ508AuEY/EoIP36II3N2brGjvf2W2O0ED1ZVVfEiyqU1ZS2ob2xs5N23trZypp508lAURZzJofyZPOv06Oh+x+NxHqxEFP9V5PAHN6zyZbcF+NAAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def Flip(self, line, CX):
                if CX == True:
                    if (line.Direction)[0] < 0:
                        line.Flip()
                elif CX == False:
                    if (line.Direction)[0] > 0:
                        line.Flip()
                return line

            def Z_direction(self, Lines, Dir):
                ptZ = [cur.PointAt(0.5).Z for cur in Lines]
                max_z = ptZ.index(max(ptZ))
                min_z = ptZ.index(min(ptZ))
                Line1 = self.Flip(Lines[max_z], Dir)
                Line2 = self.Flip(Lines[min_z], Dir)
                return Line1, Line2

            def RunScript(self, Lines, Direc):
                if Lines:
                    Topline, Endline = self.Z_direction(Lines, Direc)
                    # return outputs if you have them; here I try it for you:
                    return Topline, Endline


        # 合并曲线
        class CurveJoin(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@合并曲线", "HAE_Curve_Join", """Curve Merge Operation (Multi Process)""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3aaa7084-475b-40dc-a140-0b7c6d8d7d65")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "A set of assembly line segments")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Tolerance")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "New_Curve", "C", "Merged Polyline")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGBSURBVEhL1dZNKwVRHMfx4zF5fogsZGNlQSIPC6QUdrK0YsfbYecNWNmjlI2yQJ4K5T0I2Yrvb07ndmY698zc3NT91afOqTPzn7nzPzPX/GcGMBwxhG4oPdA8tM7pRyoHuI94wRmUCzwjtM7ZQyotaItYwjWUO8witM7R+SrKFC7t0Fxh1A6rlxn4BcbssHqprQL1aLXDUvIK6MHW2WF+1MNPUOe4xAqs4RFunxTKOt4xn8xsW/oFxu3QLEPrVpNZJH0Y9OiWd/AJnVxX7BcYwSK+sAWt94/X+VI5wkPGCX6gjaV9oB2sqJDu4BXfOEX22EOk0gm9Y0S/ZQN28YYJhO5Az+UD22iEjnPn6EA0m9BvO53Myj8DPSMV2UhmBaMu0gtrLpnZxLpI3XaLwl2kfm6yw1Ly9kEzCu+DUPIK/Dm1X2ASfoGKvwfq296IFdxAUYctILTOaUcq+iZnd6NP3+BjKOfQyzC0ztlHKuph/bMoR3tD7xtFV6d5aJ3TZYwxvy/1aW+oB697AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.factor = None

            def _join_curve(self, curve_list):
                curves = [_ for _ in rg.Curve.JoinCurves(curve_list, self.factor, False)]
                return curves

            def RunScript(self, Curve, Tolerance):
                self.factor = 0.001 if Tolerance is None else Tolerance
                trunk = [list(_) for _ in Curve.Branches]
                if len(trunk) > 0:
                    bole = ghp.run(self._join_curve, trunk)
                    all_bole = [_ for _ in bole]
                    New_Curve = ght.list_to_tree(all_bole, True, [0])
                    return New_Curve
                else:
                    return None


        # 圆弧拾取
        class ArcPick(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@圆弧拾取", "HAE_ArcPick", """Simple arc picking plug-in to rebuild a new arc through parameter modification""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("172cbb19-2b9e-44c7-8f70-417f01d23444")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Curve", "C", "Curve data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Precision of filtering curvature")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Radius", "R", "Specify the normalized radius of the arc (filter circles by radius)")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Result", "RC", "Final arc segment")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHKSURBVEhLxdVPKGVhHMbxGyJp/G1iFjaSLCxmwSgWRNlIRMrKjmQzCwtTYkbkz1YjaxssbJSsbChZiCwQio1iwUKmZmQz833ee97rHe657j2uPPXpnt8573nfe95z3nNC751JTKPYVG+QZfzFHWZRjqSmERrAukcRlHZ8Dm8GSwdO4A5wjkxkOftWUYWEMgrbwYWz/RVKDjRlV7DHBhBXvkEnaDp0FSVe/Rt5cJONYdhBfiBmaqCGD6jXDi+7mAtvRk0T/kDndmqHX3agRn2mekwu0sKbvtFN17nXUPtnqYMa7JsqWBahPgZN9SS6aTrYY6pgqYD6OEaKdrjZgw6Wmip4DvCsnwzc4BZ6zl8TOxPNpvLyAb9wiZdupl/GoPWzBA3QgkjUqTrXs65FFCTzUMfWGv57ZLehA7WmSjx6R2kW3EEkkl6M45OpgsV9xZyhG0mN7uUGprztqNEVbOEIh96vFl8hkhLdA3cOZQV6RftFi2oBI0jVjlj5ArfzU6TDL5XYhNpqLRUgZvTxcAcQTdME2qArbEA/9LGxbfQmKMOLsQPoX7V6v7aTaPSvv0Nvg7iSjxl8NFU41RiCVuk6tIh+ogtq75NQ6B8itYJa+UxZQQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _judge_curve(self, index_curve, curves):
                for _ in curves:
                    if isinstance(_, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.Line, rg.LineCurve, rg.ArcCurve)) is False:
                        return index_curve

            def filter_by_line(self, wait_curves):
                wait_curves = wait_curves if isinstance(wait_curves, (list)) is True else [wait_curves]
                count = 0
                fit_curve_list = []
                while len(wait_curves) > count:
                    start_pt, end_pt, mid_pt = wait_curves[count].PointAtStart, wait_curves[count].PointAtEnd, ghc.CurveMiddle(wait_curves[count])
                    new_line = rg.Line(start_pt, end_pt)
                    ref_mid_pt = ghc.CurveMiddle(new_line)
                    curvature = abs(mid_pt.DistanceTo(ref_mid_pt))
                    if self.tol < curvature:
                        fit_curve_list.append(wait_curves[count])
                    count += 1
                return fit_curve_list

            def rebuild_circle(self, arc_curve):
                base_pts = map(lambda arc_line: ghc.DivideCurve(arc_line, 3, False)['points'][0:3], arc_curve)
                new_circle = map(lambda pts: rg.Circle(pts[0], pts[1], pts[2]), base_pts)
                filter_cir = [_ for _ in new_circle if _.Radius > self.r]
                if len(filter_cir) != 0:
                    min_cir = filter_cir[0]
                    for other_cir in filter_cir:
                        if other_cir.Radius < min_cir.Radius:
                            min_cir = other_cir
                    return [min_cir]

            def _join_handle(self, curve_list):
                temp_line = [_ for _ in rg.Curve.JoinCurves(curve_list, 0.001, False)]
                false_fun = map(lambda x: None if x.IsClosed is False else x, temp_line)
                temp_line = filter(None, false_fun) if filter(None, false_fun) else [temp_line[0]]

                explode_line = map(lambda line_single: ghc.Explode(line_single, True)['segments'], temp_line)
                filtered_curve = map(self.filter_by_line, explode_line)
                rebu_cir = map(self.rebuild_circle, filtered_curve)
                return rebu_cir

            def RunScript(self, Curve, Tolerance, Radius):
                try:
                    self.tol = 0.001 if Tolerance is None else Tolerance
                    self.r = 5 if Radius is None else Radius
                    tree_leaf = [list(_) for _ in Curve.Branches]
                    if len(tree_leaf) == 0:
                        self.message2("Curve data cannot be empty!")
                    else:
                        filter_list = []
                        for _ in range(len(tree_leaf)):
                            if len(tree_leaf[_]) == 0:
                                self.message2("The {} curve data is empty".format(_ + 1))
                            elif self._judge_curve(_, tree_leaf[_]) is not None:
                                self.message1("The {} curve data module has wrong data!!".format(_ + 1))
                            else:
                                filter_list.append(tree_leaf[_])
                        join_curve = [_ for _ in ghp.run(self._join_handle, filter_list)]
                        return ght.list_to_tree(join_curve)
                finally:
                    self.Message = 'Arc Pick'


        # 曲线筛选
        class FilterCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲线筛选", "HAE_FilterCurve", """Select curves by curvature""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("0bf1b87f-be62-4681-95cc-a2cacce8a98c")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve List Data")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Tolerance", "T", "Curvature tolerance")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve_Result", "CR", "Curves Greater Than Curvature (Curve Results)")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Line_Result", "LR", "Curves Less Than Curvature (Straight Line Results)")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAXKSURBVEhLvZVpTFRnFIbHWqw1cQlKbP1RjSIqahNcWgtpamraAAVRa7TRqijUphWVaqxLYht+WNQuSoKlwaXVBqg1FoVUU8cFi0pLXRgGZmUQmGEYmH25y2y8Pd83opa2pr96k5N7595zznPOe86XUfyvV3V19SSlUjkZ7nuTlh+/kDz6i8aUcSV1KaOLlSmKDcdSdpccT25oaOA+/2b19fWTa2pqXniQMnYtWLDg2e7u7tPBYFDsj0ryJbVFmlh0NzpulxrjttYjbu1pbCw9D6fTERVFUfL7/fKTLBQKBTo6Or6m1E9zQF5eXpogiGDXdVMvnj+oxvCdOozd0oJhq64hf/85SF4Hfe0HBT/RqEiex2azhefOnTudA97NzX0DARfqKPmYw3ehOKjBiGI9hmxvwnulVyH7neiPRkDVQ5Kkvxl7z0wQBAQCAYTDYZAigdmzZ8/hgH0frl5U22jA+C/VUHyuwdBSPRT7VNhwvA5BSk7ZIcsyomGqLhpChO7s9+M2AGKQSCQCs9n8CPDimu3LJhap8MweHYYfoOTFKuSeqkOIumKy9EdC/O4JyGjv8cMvyFyGaCTMJWH2OIB18AAwlwNG5pfmJuwxIH5rKxQ7VFh/gir32hElWSJhGQFRxu4fjEjadhPPbVRixpZL+KSiCTIlDofkh9INBsyaNWseB4x5/9DahMJGDFt9HflMc5acqhOFAFUnYcVXd6BY/jNGrruI+NxaKJZUYfjS77G59FfyC0Ig3VlyZmwGbNidnZ3CzJkz53PAiDX71w3LrUZecTVETx9PzipBRMSZehMUy85ibO55JKyrxpAlFZhfWIMOmwfLPq1F7U09SUgQ8h8MSE5OfokDnsr6eH1+aS38DivCQZIkENsGQMa28gYoFp/CuNVVGJJ9AnMKzsLcY6dvYZScacCub67wZwZgRueAz4TOgTBjxoyXOSAta+UqqzWW3Ofz8eQxQBDbyuqgyCiDIv0IUj6oRJfFhqDgAW0ASk7XY2+5kgMGYlg826r29nZx+vTpCzhg+dLFb/XaeriD1+vlVbDn/oiEHy83QfHKPiwsrISluweS3wW3y4GQ6MObm8txob6Zz4H5szgWzwZuMpnEadOmpXJATk5ONutgMIANT/C5kbntO6wrqoKtx4q+vl5oje1YveckNh84g0gopvtgQFtbm/QQkJ2dnWOxWLiDx+P5i0ySGIDLaceOQ9VILyjDil3fIvujcnx27CJCMlvPGIDFsjgWz4ZtNBqlpKSkNA7IyspaQnvLHdxuN6/iYVVkbF0RlWHrc0BrMsPlcnPdxQdDZX4slsWxeDZsg8EgTZ069dV/BLAqmDP7zWwgiUzVhuhcSGJsy3gB9I0Z82dxAwC9Xi8/BGRmZi7r6uriTi6XC15yDIpeiAHqxBcLFOg5JPkRlgkkMjlIa4GBfXReJHpHUlJnLJ4BdTqdnJiY+BoHZGRkvE0Hg9NdLicN0o7Ldy24Z7DhvqWPvzd09uL31m4o/+jEHU0XBL8Xan0XrW0Pzly8DZWmnb9zOBy8a61W+wiQnp6+nA4Gp/vcdtQ09kGp9uCW1onzt50Q/R4cu+bAwRormtocOFqrQcWFJhyq+A07D/+CVdurkL2lEu2dVlphJ1dCo9EEp0yZspADSKIVrAOn0wmPsxfnbnugpA6ajVZU3rDjpzo9Co9qcfKijmbrgbm7F/PWnITylg57j1zFO4UVKCpTwtbbB7s91jEBQrRFr3NAamrqSvoH4sPxelywu3y40uqDzuzFfasbZ29YcP2eFRpTD/ykvSj4cONuB5ykua3PiYraJqi0Zj4TpgI7yTQDTJgwYREHxMXFpZSUlNDg9VA1N0PdrIJR2wxtqxpajRodbRqYDBoYdBq0tLRwMxm1aKW7VtOCrvsG/k2lUqGZ4lny4uLiRkqdyAF0DSVLi4+PLxg/fnxBQkLCJmb0/J/tsZiCUaNGbaJ89GejGPInDRdeIfUoK/YAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.tol = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def find_curvature(self, o_curve):
                start_pt, end_pt, mid_pt = o_curve.PointAtStart, o_curve.PointAtEnd, ghc.CurveMiddle(o_curve)
                ref_line = rg.Line(start_pt, end_pt)
                ref_mid = ghc.CurveMiddle(ref_line)
                curvature = abs(mid_pt.DistanceTo(ref_mid))
                return o_curve if curvature >= self.tol else None

            def RunScript(self, Curve, Tolerance):
                try:
                    self.tol = 0.001 if Tolerance is None else Tolerance
                    if len(Curve) > 0:
                        result_cur = ghp.run(self.find_curvature, Curve)
                        index_fit_cur = []
                        index_line_cur = []
                        for index_c in range(len(result_cur)):
                            if result_cur[index_c] is None:
                                index_line_cur.append(Curve[index_c])
                            else:
                                index_fit_cur.append(Curve[index_c])
                        Curve_Result, Line_Result = index_fit_cur, index_line_cur
                        return Curve_Result, Line_Result
                    else:
                        self.message2("The curve list is empty!")
                finally:
                    self.Message = 'Filter Curve (Curvature)'


        # 曲线按照参照平面排序
        class LineSortByXYZ(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "HAE@曲线排序", "HAE_LineSortByXYZ",
                                                                   """Sort the curve list. When the axis input end is empty, sort by line length. Enter x, y, z to sort by x, y, z axis coordinates. CP can specify a plane""", "Hero", "Line")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ff552258-2c50-4fe8-b032-9ec25ef804b5")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Curve List")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "axis")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "CP", "CP", "Sort by coordinate axis XYZ, default to world XY")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Sort_Curve", "C", "Sorted curve list")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                p2 = self.marshal.GetInput(DA, 2)
                result = self.RunScript(p0, p1, p2)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADfSURBVEhL7dS9DsFQGIfxug8RQgwmC4uBgbswWOxmNh8jdldhlBgY3ITFYrdYbDz/Jke0HFXRIOmT/IYifU/ibZ24n6yABbLu1YfLY48zdsjA1MAohBo8VXCCbm4cUYaa4fa7IFNcS6CFPlbQD5YYoAlVRS8EHfhhXWhAx72KoCE0QKeIpK8NCNqiu62xZRsQtEWerXmWbYBOqM9srFvj7///5EieAz3JbYyxgQasMYGecFXHW1tjKkHvHt3cOKAI5d8iDQ9dGnqL6gZbJGHyb9HLW+MvhzlS7lVctDnOBW5zXVOZwwLKAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.dict_axis = {'X': 'x_coordinate', 'Y': 'y_coordinate', 'Z': 'z_coordinate'}

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def _sort_by_length(self, list_data):
                for f in range(len(list_data)):
                    for s in range(len(list_data) - 1 - f):
                        first_line = list_data[s].GetLength()
                        second_line = list_data[s + 1].GetLength()
                        if first_line > second_line:
                            list_data[s], list_data[s + 1] = list_data[s + 1], list_data[s]
                return list_data

            def _other_by_xyz(self, data, axis, coord_pl):
                for index1 in range(len(data)):
                    min_index = index1
                    for index2 in range(min_index + 1, len(data)):
                        first = ghc.PlaneCoordinates(ghc.CurveMiddle(data[min_index]), coord_pl)[self.dict_axis[axis]]
                        second = ghc.PlaneCoordinates(ghc.CurveMiddle(data[index2]), coord_pl)[self.dict_axis[axis]]
                        if first > second:
                            min_index = index2
                    if min_index != index1:
                        data[index1], data[min_index] = data[min_index], data[index1]
                return data

            def RunScript(self, Curve, Axis, CP):
                try:
                    CP = ghc.XYPlane(rg.Point3d(0, 0, 0)) if CP is None else CP
                    if Curve:
                        if Axis is None:
                            self.message3("Axis coordinate is not entered, it will be sorted by length!")
                            Sort_Curve = self._sort_by_length(Curve)
                            return Sort_Curve
                        else:
                            Axis = Axis.upper()
                            if Axis in ['X', 'Y', 'Z']:
                                Sort_Curve = self._other_by_xyz(Curve, Axis, CP)
                                return Sort_Curve
                            else:
                                self.message2("Please enter correct axis coordinates!")
                    else:
                        self.message2("The curve list is empty!!")
                finally:
                    self.Message = "Curve sorting"

    else:
        pass
except:
    pass

import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Line_Group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYe_Niko"

    def get_Id(self):
        return System.Guid("99e47d1b-376c-4606-8812-cd6625f02566")
