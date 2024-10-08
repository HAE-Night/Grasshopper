# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Display_group
# @Time : 2023/1/6 18:28

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
from itertools import chain
import math
import copy
import initialization
import Geometry_group

Result = initialization.Result
Message = initialization.message()
try:
    if Result is True:

        # 显示点序指向
        class ShowPointLine(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ShowPointLine", "Z2", """Show point order and line orientation""", "Scavenger", "I-Display")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("875036ee-b5d1-432a-8b7d-8fa790922611")

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
                self.SetUpParam(p, "Geo", "G", "Sequence of points to be analyzed")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Format", "F", "Whether to format the dot order")
                Factor = True
                p.SetPersistentData(gk.Types.GH_Boolean(Factor))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "F_Center", "C", "Whether to arrange according to geometric center point")
                Center_Factor = False
                p.SetPersistentData(gk.Types.GH_Boolean(Center_Factor))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "Size", "S", "Font display size")
                SIZE_FONT = 40
                p.SetPersistentData(gk.Types.GH_Number(SIZE_FONT))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "_place", "*", "placeholder（Each center point）")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJCSURBVEhLYxiSYLdLKP8CY+u4fn3TVqgQ5eD///+M882tHaYamM2coGv8fJGh1f9WbcP5UGnywWRTG7XZhpatE3VNrkzWNf0/FYj7tY3+9+kY/683NDWBKiMftBiZWXTpGP2YrGPyv0vLEIwnAg1v1TK4BpRmhKiiEDQZmwVM1jX53w21YBrQF03aho1QacrAHEtH+cn6ppcnaBv/B1kConu0jf7W6JtqQ5WQD2bZ28tM0jO9DXJxPzBY6rQM+ju0DV+2ahvchiohH8yxcpGaqG92E2Q4KHLrdAwqQeJl+sZmdbrGkWBF5IL59vYSk/RNr4EMnwIyXMugFipFOZhr4yE6Sd/s8nSgwaAkWUetyASBhc7OwsAIvQA3XEufejl1qbe34BR9s7MzgAaDgqZR26ADKkU5WOXiwj9Z3+wU2HA90//12oY9UCnKQZ+trSQwQi/CDdcynACVog6YAbSgU8vw0TwDC2DuNJgMFSYbiAHxBA4BufPsPJKngGxQ8mOqNzaWa9IxAqdzSoAYG5fIbR3PSf9tUk7+t04+9l/VruY/Ewvbbqg8xaBf273vv3PBw/+2aaeB+Ox/l8JH/xXMsv8D5RIgSigA7DwSF0Cutk07A/TBCTC2z7z43yR8HdACxmVQZeQDYPCctEo89N8u/SzCgqwr/41CVoAsmAdVRhEoVbYqAQeLfeYlsOHO+ff/S2oGg4LIE6KEMsDGyMiyRd4k879J2FqwyyW1wIZPhEhTD8QCMaiyngnE3iAB8gEDAwAN2OWI7onDpQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pts, self.lines, self.bbox, self.factor, self.show_cen, self.size = (None for _ in range(6))

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def _get_lines(self, pts):
                new_pts, line_list = None, None
                if type(pts) is not list:
                    new_pts = pts
                    return new_pts, line_list
                else:
                    if pts:
                        ply_line = rg.PolylineCurve(pts)
                        # center_pt = ght.tree_to_list(Geometry_group.GeoCenter().RunScript(ght.list_to_tree([ply_line])))[0]
                        center_pt = Geometry_group.GeoCenter().center_box(ply_line)
                        sc_trf = rg.Transform.Scale(center_pt, 0.8)
                        copy_ply_line = ply_line.Duplicate()
                        copy_ply_line.Transform(sc_trf)
                        res_ply_line = copy_ply_line if self.factor else ply_line

                        new_pts = [_.Location for _ in res_ply_line.ToNurbsCurve().Points]
                        loop_items = zip(new_pts, new_pts[1:] + new_pts[:1])[:len(new_pts) - 1]
                        line_list = ghp.run(lambda pt_list: rg.Line(pt_list[0], pt_list[1]), loop_items)
                    else:
                        new_pts, line_list = [], []

                return new_pts, line_list

            def _get_all_pts(self, obj):
                _obj_pt = []
                if isinstance(obj, (rg.Curve, rg.Line)):
                    _obj_pt = [_.Location for _ in obj.ToNurbsCurve().Points]
                elif isinstance(obj, (rg.Brep)):
                    _obj_pt = [_.Location for _ in obj.Vertices]
                elif isinstance(obj, (rg.Point3d)):
                    _obj_pt = obj
                elif isinstance(obj, (rg.Point)):
                    _obj_pt = obj.Location

                if self.show_cen:
                    if _obj_pt:
                        _obj_pt = Geometry_group.GeoCenter().center_box(obj)
                    # _obj_pt = ght.tree_to_list(Geometry_group.GeoCenter().RunScript(ght.list_to_tree([obj])))[0]

                return _obj_pt

            def _do_main(self, data):
                _gener = map(self._get_all_pts, data)
                pt_list = []
                if len(_gener) == 1:
                    pt_list = _gener[0]
                else:
                    for _ in _gener:
                        if isinstance(_, (list, tuple)):
                            pt_list += _
                        else:
                            pt_list.append(_)

                set_of_pts, set_of_line = self._get_lines(pt_list)
                set_of_pts = set_of_pts if type(set_of_pts) is not rg.Point3d else [set_of_pts]
                if set_of_pts:
                    center_pt = rg.PointCloud(set_of_pts).GetBoundingBox(True).Center
                else:
                    center_pt = rg.Point3d(0, 0, 0)
                return set_of_pts, set_of_line, center_pt

            def RunScript(self, Geo, Format, F_Center, Size):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    origin_data = [list(_) for _ in Geo.Branches]
                    _place = gd[object]()
                    self.factor = Format
                    self.show_cen = F_Center
                    self.size = Size

                    if origin_data:
                        list_pts, list_line, cen_pts = zip(*ghp.run(self._do_main, origin_data))
                    else:
                        self.message2("The sequence of points to be parsed is empty！")
                        list_pts, list_line, cen_pts = (None for _ in range(3))

                    self.pts = list_pts
                    self.lines = list_line
                    self.bbox = rg.BoundingBox(cen_pts) if cen_pts else rg.BoundingBox.Empty
                    if cen_pts:
                        cen_pts = ght.list_to_tree([[_] for _ in cen_pts])
                        _place = cen_pts

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return _place
                finally:
                    if not self.show_cen:
                        self.Message = 'Display point order'
                    else:
                        self.Message = 'Display Geometry order'

            def DrawViewportWires(self, args):
                try:
                    for f_lines in self.lines:
                        if f_lines:
                            for line in f_lines:
                                args.Display.DrawArrow(line, System.Drawing.Color.FromArgb(0, 255, 255))
                    for f_items in self.pts:
                        if f_items:
                            for sub_index in range(len(f_items)):
                                args.Display.Draw2dText(str(sub_index), System.Drawing.Color.Green, f_items[sub_index], True, self.size)
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


        # 曲线显示方向
        class CurvesDirection(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Crv Dir", "Z1", """Display curve direction""",
                                                                   "Scavenger", "I-Display")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("e83cf93b-04ac-4105-98c0-3c35462fc7f3")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.primary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "showing Curve direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIbSURBVEhL7ZRLaBNRFIZ/sKUFWx+INJm5SYq29pF53JkJTWgjbZCYRUFxoS7FVxFLUSjFZdE+YqZpmyJVK1a7c9WFiEHoouBGkSLuu3DdjWtd2OtJPAjuUjMb0Q8Oc+ecn/k59565+M8/wHPEmgvQbhQhrhQQObmOaJjSqcaWkE/Py1VRPeTR1j4PoVYRU2SmxtGi9PgFNXD9g+o9Pa/QcOAmS/+cPKLHFiFyyxBjOTSV4+fWVO7OF5W5ta1EVL5nWWA0HBapj8bwI9XpXFJnoh3KtazXnX3uMNcDoZki0wgYJWhvpluPq3RX/F2vI19JKa96IyNUCggfmnyKiHqI0KRImaa0rGdkskkx7nneQZYhm83u5+XeyUPbzkPf4VcYhtFt2+aStO23juPcSyaTbUND6VOOlCss2Ruz0Kee0ITRGCc4VcW2bd2yrCmKsuc4JTLcpR7Pcrl2ZqBbjxFV9Fzm1G8M9vcnyOCz60hFZsp13QyXaoe2aasE8W0SR0Oc+kVfIjFqm+aLnp7uomHEF0zTnOBS7cxADFa2if74zTF0NHE6WKYRvruG9orJp/sIpzkdLHTgt0s0tit0JnPQN+geu/gA2hEuB8MstBP08VXqpHqHFaDvUmzMQUz4CA8sInaIpfXhIxYik2s+RJkMvla6qgStvy9AbNFgjLK0fgroai0ikv7Zhf5yCWKHDNa5HDzngX28/KsBfgDbzJHADW3KrgAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pts = []

            def RunScript(self, C):
                C.Flatten()
                self.c = C.Branches[0]

                if not self.c: return
                self.bb = rg.BoundingBox()
                Plist = []
                Tlist = []

                self.c = list(filter(None, self.c))
                for i in range(len(self.c)):
                    if not self.c[i]: return
                    # 检测曲线是否闭合 不闭合则终点也进行标注
                    if self.c[i].IsClosed == True:
                        n = 4
                    else:
                        n = 3

                    pt = map(self.c[i].PointAt, self.c[i].DivideByCount(n, True))  # 平切成N曲线 - 返回点
                    for k in range(len(pt)):
                        self.bb.Union(pt[k])  # 更新box边框
                        self.pts = rs.CurveClosestPoint(self.c[i], pt[k])  # 获取最近点
                        self.tg = rs.CurveTangent(self.c[i], self.pts)  # 切线
                        Plist.append(pt[k])
                        Tlist.append(self.tg)
                parts = len(self.c)
                self.p = [Plist[(i * len(Plist)) // parts:((i + 1) * len(Plist)) // parts] for i in range(parts)]
                self.t = [Tlist[(i * len(Plist)) // parts:((i + 1) * len(Plist)) // parts] for i in range(parts)]
                return

            def DrawViewportWires(self, arg):
                if not self.c: return
                for i in range(len(self.c)):
                    if not self.c[i]: return
                    for j in range(4):
                        arg.Display.DrawDirectionArrow(self.p[i][j], self.t[i][j], System.Drawing.Color.Red)

            def get_ClippingBox(self):
                return self.bb


        # 显示面方向
        class BrepDirection(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_BrepDirection", "Z3", """show Orientation of surface (multiple surfaces)""", "Scavenger", "I-Display")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("c7ac0f7b-73d4-42c6-8f4e-e3930e3a5be0")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "A surface or multiple surface to show direction")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "*", "*", "A placeholder ,output the center point of the object ")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIwSURBVEhLYxgFgw90Msia9DPInOtkkLrQQQKexCB7o51BOg1qDG4AVLRnBoPcf6AlROE+IJ7CIAumWxkkbaHGYAedDNKOE4CKgfT/DiJxN9SSFgYJT6gxuEEbg/RuoFexGoQLTwaqB7o8F2oEbgBUpNHFIPOvC4shuDDIMcAg3Qw1Aj9oZ5AqBoUlNoOwYZBDehikf7cyyGlBjcAPgClhCSnBA4pgoKMuQrUTBkBNGyeSYAEoYtsYpC5BtRMGwLCcBoowbIZhw6CUBgyiP+0MMrpQI/ADoKYQUlMQyMfAYNoGNQI/qGcQ5QH64mUv0OvYDMOFIclUOh9qDH4AzAeVU4G5GJtBuDAso7UxSHhAjcENZjJIcgHLoMegFIJsCCi88WGQBcD4+NbBIGkDNQo3ABoYAvIFKHzRyxwYBgUjDAMNBvqC9+tUBlFQfKyHGoMfAOPCqZtB2rODQcYd6CpXoK+cgS51BIo7tDLI2IMKNSC2BiZTy2Z+fYdM32mzKiwq4v8zMLBAjaAusMs5Uu9Z+fh5UO2rmsLef0JQYQSIj9/PEVF1JyOq7klxePX9IpJx1e0cz6yjj/xLH/z3KbjyIqTq8bSQ8jtOUOMZGLwztwi6pe094J5++Ixb2n7COBUZHzjtlrpvr1fmkVfeBdf++xbd/O+eefyra8qudqjxlIPEumuRQaW3/rulHbnlGLsuSVxPjxsqRTmon3KFxzfn+CbnxN2tkpKSXFBhKGBgAAC+mdcMRIBuXAAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.vector_surface, self.bb_pts, self.brep_trunk = (None for _ in range(3))

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

            def _get_data(self, obj):
                # 数据集合列表
                set_list = []
                # 获取所有面
                origin_faces = ghc.DeconstructBrep(obj)['faces']
                if type(origin_faces) is not list:
                    origin_faces = [origin_faces]
                # 遍历面并获取每个面的朝向
                for face in origin_faces:
                    pl_list = ghc.SurfaceFrames(face, 10, 10)['frames']
                    if pl_list:
                        for pl in pl_list:
                            prune_vector = pl.ZAxis
                            prune_vector.Unitize()
                            prune_vector *= 0.8
                            set_list.append((pl.Origin, pl.ZAxis))
                return set_list

            def _get_center_obj(self, objs):
                # 获取物体的中心点
                pt_list = []
                for _ in objs:
                    if _:
                        pt_list.append(_.GetBoundingBox(True).Center)
                return pt_list

            def temp_fun(self, data):
                # 临时方法
                temp_data = list(chain(*map(self._get_data, data)))
                return temp_data

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    _cen_pt = gd[object]()
                    j_bool_f1 = self.parameter_judgment(self.Params.Input[0].VolatileData)[0]
                    re_mes = Message.RE_MES([j_bool_f1], ['B end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        temp_pt_vect, center_pts, brep_trunk = None, None, None
                    else:
                        # 将数据传入temp函数
                        brep_trunk, brep_path = self.Branch_Route(Brep)
                        temp_pt_vect = list(chain(*ghp.run(self.temp_fun, brep_trunk)))
                        _cen_pt = map(self._get_center_obj, brep_trunk)
                        center_pts = list(chain(*_cen_pt))
                        _cen_pt = ght.list_to_tree(_cen_pt)
                    # 将绘制图像全局变量命名
                    self.vector_surface = temp_pt_vect
                    self.bb_pts = rg.BoundingBox(center_pts) if center_pts else rg.BoundingBox.Empty
                    self.brep_trunk = brep_trunk

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return _cen_pt
                finally:
                    self.Message = 'Display face orientation'

            def DrawViewportWires(self, args):
                try:
                    for item in self.vector_surface:
                        args.Display.DrawDirectionArrow(item[0], item[1], System.Drawing.Color.FromArgb(67, 15, 137))
                    if self.brep_trunk:
                        breps = list(chain(*self.brep_trunk))
                        for brep in breps:
                            args.Display.DrawBrepWires(brep, System.Drawing.Color.FromArgb(0, 150, 0))
                except:
                    pass

            def get_ClippingBox(self):
                return self.bb_pts


        # 显示点向量
        class PointVector(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_PointVector", "Z4", """Display point vector""", "Scavenger", "I-Display")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b0e4682f-691c-4715-861f-b57a16858298")

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "PointA", "P", "Vector display origin")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "The vector to display")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Size", "S", "The magnitude of the vector ")
                p.SetPersistentData(gk.Types.GH_Integer(1))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "ActualVector", "A", "Actual vector (original Size multiplied by size) ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "UnitVector", "UV", "Unit vector (original Size multiplied by size) ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "UnitRVector", "R", "The inverse vector of the unit vector (original Size multiplied by size)")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI6SURBVEhLvZXPa9RAFMffJLus292qYJcKzWTdsgcPIuoieFLQk3c9CXoVxIN4FXvw0N0km3bdVl1B6EFsErW7XbU/wEpvXjwUVPTgwYOC6EWSqG3aZnyTzn+Q0Q88HjPfx3uZN5MZ+C8MzsX7yNP1+0o/WuOej4UkAY+pxPFX4BVj0ENDT5zwJXieKiLSkXN/VuHJBgPvNwMn2PE4TuZlMOCF+8msvwVzmwxmsQB6Pi7Mx8MiJD2KE96ARWzPMhr6ZCwb9XFwBpa2riYeaQ0crFm7KhcS8V8wsae8t6HQH21FX7Vzo6fFtFyMjH7lAZTZBKHMVvT5Zr56QkhyMIcPF+pE+2aDxm4DZU0s1FT1R2a+cnwMTmVEWDpwFWNTmHwcRlgD7S7ozFTox8lCRc4paxWrJYNogYnJ62gtLNZQtRkhy6Gh0nYHvzxJjkUmuc/oN4WcHrMweshS6EqdUIMn56tp8yKKdl2ESACvKO4MQm/xPeFF+MbjUb6c6DLBPbGnsWWW2JNxhV4UkjwMlXamMbmFR9jG41tX6CUhyQPb9ZC36x7+jG3YvXDuWjOfe80OMICknVLAIkt3YHC5PPP+LDzf/kC66xHpRmtZLzwiQtLRgVq2ZvWHoBt9gRd4G/P3BG9l4vpv4Q3LirCULMbHoI/JnVA8Wn8YuCHLu79GREQ6iq5fIm4YwjNRBN8U4gafYCHOiZD0qE5wnvQ2v0N/m5Fe9Dnj+CeFJI9i5+tQdjU+Wpp6V9yZAfgLJ3j+4e4qOocAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.line = []

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

            # 单对单
            def AmplificationVector(self, PVS_Zip):
                PointA, VectorB, Size = PVS_Zip
                Vector = copy.deepcopy(VectorB)
                # 单对单处理向量
                if not PointA:
                    Message.message2(self, "输入参数PointA有空值")
                    return None, None, None, None
                elif not Vector:
                    Message.message2(self, "输入参数Vector有空值")
                    return None, None, None, None
                else:
                    ActualVector = rg.Vector3d.Multiply(Size, Vector)
                    line = rg.Line(PointA, ActualVector)
                    Vector.Unitize()
                    UnitVector = rg.Vector3d.Multiply(Size, Vector)
                    Vector.Reverse()
                    UnitRVector = rg.Vector3d.Multiply(Size, Vector)
                    return line, ActualVector, UnitVector, UnitRVector

            # 列表对列表
            def temp(self, tuple_data):
                List_PointA, List_Vector, List_Size, new_geo_path = tuple_data
                P_len = len(List_PointA)
                V_len = len(List_Vector)
                S_len = len(List_Size)

                if P_len > 0 and V_len > 0:
                    # 子树大小进行匹配
                    Len_difference = P_len - V_len
                    if Len_difference > 0:
                        List_Vector += [List_Vector[-1]] * Len_difference
                        if P_len > S_len:
                            List_Size += [List_Size[-1]] * (P_len - S_len)
                    elif Len_difference < 0:
                        List_PointA += [List_PointA[-1]] * abs(Len_difference)
                        if V_len > S_len:
                            List_Size += [List_Size[-1]] * (V_len - S_len)
                    else:
                        if V_len > S_len:
                            List_Size += [List_Size[-1]] * (V_len - S_len)
                    PVS_Zip = zip(List_PointA, List_Vector, List_Size)
                    List_info = ghp.run(self.AmplificationVector, PVS_Zip)
                    list_line, list_ActualVector, list_UnitVector, list_UnitRVector = zip(*List_info)

                else:
                    Message.message3(self, "输入参数Point和Vector有空树")
                    list_ActualVector = []
                    list_UnitVector = []
                    list_UnitRVector = []
                    list_line = []
                ungroup_data = map(lambda x: self.split_tree(x, new_geo_path), [list_ActualVector, list_UnitVector, list_UnitRVector, list_line])

                return ungroup_data

            def RunScript(self, PointA, Vector, Size):
                try:
                    List_PointA, Path_Point = self.Branch_Route(PointA)
                    List_Vector, Path_Vector = self.Branch_Route(Vector)
                    List_Size, Path_Size = self.Branch_Route(Size)

                    # 兴建一个最新的数据地址(以最长的数据为准)
                    new_geo_path = Path_Point
                    result, result1, result2 = (gd[object]() for _ in range(3))
                    re_mes = Message.RE_MES([List_PointA, List_Vector, List_Size], ['P end', 'V end', "S end"])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object]()
                    else:
                        # 判断点和向量长度大小进行匹配
                        P_len = len(List_PointA)
                        V_len = len(List_Vector)
                        S_len = len(List_Size)
                        Len_difference = P_len - V_len
                        # 进行父树结构匹配
                        if Len_difference > 0:
                            List_Vector += [List_Vector[-1]] * Len_difference
                            new_geo_path = Path_Point
                            if P_len > S_len:
                                List_Size += [List_Size[-1]] * (P_len - S_len)
                        elif Len_difference < 0:
                            List_PointA += [List_PointA[-1]] * abs(Len_difference)
                            new_geo_path = Path_Vector
                            if V_len > S_len:
                                List_Size += [List_Size[-1]] * (V_len - S_len)
                        else:
                            if V_len > S_len:
                                List_Size += [List_Size[-1]] * (V_len - S_len)
                        origin_list = zip(List_PointA, List_Vector, List_Size, new_geo_path)
                        tree_info = zip(*ghp.run(self.temp, origin_list))

                        tree_ActualVector, tree_UnitVector, tree_UnitRVector, tree_line = ghp.run(lambda single_tree: self.format_tree(single_tree), tree_info)

                        self.line, line_path = self.Branch_Route(tree_line)
                        return tree_ActualVector, tree_UnitVector, tree_UnitRVector
                finally:
                    self.Message = 'Display vector'

            def DrawViewportWires(self, arg):
                try:
                    for _ in self.line:
                        for __ in _:
                            if __ is None:
                                pass
                            else:
                                arg.Display.DrawArrow(__, System.Drawing.Color.Green)
                except Exception as e:
                    Message.message1(self, e)


    else:
        pass
except:
    pass

import GhPython
import System
