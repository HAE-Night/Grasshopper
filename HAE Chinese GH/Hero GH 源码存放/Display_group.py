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
                                                                   "RPP_ShowPointLine", "Z2", """显示点序与线指向""", "Scavenger", "I-Display")
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
                self.SetUpParam(p, "Geo", "G", "需要分析的点序列")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Format", "F", "是否格式化点序")
                Factor = True
                p.SetPersistentData(gk.Types.GH_Boolean(Factor))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "_place", "*", "占位符（各中心点）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                p1 = self.marshal.GetInput(DA, 1)
                result = self.RunScript(p0, p1)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJCSURBVEhLYxiSYLdLKP8CY+u4fn3TVqgQ5eD///+M882tHaYamM2coGv8fJGh1f9WbcP5UGnywWRTG7XZhpatE3VNrkzWNf0/FYj7tY3+9+kY/683NDWBKiMftBiZWXTpGP2YrGPyv0vLEIwnAg1v1TK4BpRmhKiiEDQZmwVM1jX53w21YBrQF03aho1QacrAHEtH+cn6ppcnaBv/B1kConu0jf7W6JtqQ5WQD2bZ28tM0jO9DXJxPzBY6rQM+ju0DV+2ahvchiohH8yxcpGaqG92E2Q4KHLrdAwqQeJl+sZmdbrGkWBF5IL59vYSk/RNr4EMnwIyXMugFipFOZhr4yE6Sd/s8nSgwaAkWUetyASBhc7OwsAIvQA3XEufejl1qbe34BR9s7MzgAaDgqZR26ADKkU5WOXiwj9Z3+wU2HA90//12oY9UCnKQZ+trSQwQi/CDdcynACVog6YAbSgU8vw0TwDC2DuNJgMFSYbiAHxBA4BufPsPJKngGxQ8mOqNzaWa9IxAqdzSoAYG5fIbR3PSf9tUk7+t04+9l/VruY/Ewvbbqg8xaBf273vv3PBw/+2aaeB+Ox/l8JH/xXMsv8D5RIgSigA7DwSF0Cutk07A/TBCTC2z7z43yR8HdACxmVQZeQDYPCctEo89N8u/SzCgqwr/41CVoAsmAdVRhEoVbYqAQeLfeYlsOHO+ff/S2oGg4LIE6KEMsDGyMiyRd4k879J2FqwyyW1wIZPhEhTD8QCMaiyngnE3iAB8gEDAwAN2OWI7onDpQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pts, self.lines, self.bbox, self.factor = (None for _ in range(4))

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
                if pts:
                    ply_line = rg.PolylineCurve(pts)
                    center_pt = ght.tree_to_list(Geometry_group.GeoCenter().RunScript(ght.list_to_tree([ply_line])))[0]
                    sc_trf = rg.Transform.Scale(center_pt, 0.8)
                    copy_ply_line = ply_line.Duplicate()
                    copy_ply_line.Transform(sc_trf)
                    res_ply_line = copy_ply_line if self.factor else ply_line

                    new_pts = [_.Location for _ in res_ply_line.ToNurbsCurve().Points]
                    loop_items = zip(new_pts, new_pts[1:] + new_pts[:1])[:len(new_pts) - 1]
                    line_list = ghp.run(lambda pt_list: rg.Line(pt_list[0], pt_list[1]), loop_items)

                return new_pts, line_list

            def _get_all_pts(self, obj):
                _obj_pts = []
                if isinstance(obj, (rg.Curve, rg.Line)):
                    _obj_pts = [_.Location for _ in obj.ToNurbsCurve().Points]
                elif isinstance(obj, (rg.Brep)):
                    _obj_pts = [_.Location for _ in obj.Vertices]
                elif isinstance(obj, (rg.Point3d)):
                    _obj_pts = obj
                elif isinstance(obj, (rg.Point)):
                    _obj_pts = obj.Location
                return _obj_pts

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
                if set_of_pts:
                    center_pt = rg.PointCloud(set_of_pts).GetBoundingBox(True).Center
                else:
                    center_pt = rg.Point3d(0, 0, 0)
                return set_of_pts, set_of_line, center_pt

            def RunScript(self, Geo, Format):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    origin_data = [list(_) for _ in Geo.Branches]
                    _place = gd[object]()
                    self.factor = Format

                    if origin_data:
                        list_pts, list_line, cen_pts = zip(*ghp.run(self._do_main, origin_data))
                    else:
                        self.message2("待解析的点序列为空！")
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
                    self.Message = '显示点序'

            def DrawViewportWires(self, args):
                try:
                    for f_lines in self.lines:
                        if f_lines:
                            for line in f_lines:
                                args.Display.DrawArrow(line, System.Drawing.Color.FromArgb(0, 255, 255))
                    for f_items in self.pts:
                        if f_items:
                            for sub_index in range(len(f_items)):
                                args.Display.Draw2dText(str(sub_index), System.Drawing.Color.Green, f_items[sub_index], True, 100)
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox


        # 曲线显示方向
        class CurvesDirection(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Crv Dir", "Z1", """显示曲线方向""",
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
                self.SetUpParam(p, "Curve", "C", "显示方向的曲线")
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
                                                                   "RPP_BrepDirection", "Z3", """显示面（多重曲面）的朝向""", "Scavenger", "I-Display")
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
                self.SetUpParam(p, "Brep", "B", "要显示方向的面或者多重曲面")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "*", "*", "占位符，输出物体中心点")
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
                self.vector_surface, self.bb_pts, self.breps = None, None, None

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def _get_data(self, obj):
                zip_list = []

                origin_data = ghc.DeconstructBrep(obj)['faces']
                for face in origin_data if isinstance(origin_data, (tuple, list)) else [origin_data]:
                    pl_list = ghc.SurfaceFrames(face, 10, 10)['frames']
                    if pl_list:
                        for pl in pl_list:
                            prune_vector = pl.ZAxis
                            prune_vector.Unitize()
                            prune_vector *= 0.8
                            zip_list.append((pl.Origin, pl.ZAxis))
                return zip_list

            def _get_center_obj(self, objs):
                pt_list = []
                for _ in objs:
                    if _:
                        pt_list.append(_.GetBoundingBox(True).Center)
                return pt_list

            def temp_fun(self, data):
                temp_data = list(chain(*map(self._get_data, data)))
                return temp_data

            def RunScript(self, Brep):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    temp_pt_vect, center_pts, _cen_pt = None, None, gd[object]()
                    trunk_list = [list(_) for _ in Brep.Branches]
                    if trunk_list:
                        temp_pt_vect = list(chain(*map(self.temp_fun, trunk_list)))
                        _cen_pt = map(self._get_center_obj, trunk_list)
                        center_pts = list(chain(*_cen_pt))
                        _cen_pt = ght.list_to_tree(_cen_pt)
                    else:
                        Message.message2(self, "B端为空！！")

                    self.vector_surface = temp_pt_vect
                    self.bb_pts = rg.BoundingBox(center_pts) if center_pts else rg.BoundingBox.Empty
                    self.breps = list(chain(*trunk_list))

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return _cen_pt
                finally:
                    self.Message = '显示面朝向'

            def DrawViewportWires(self, args):
                material = Rhino.Display.DisplayMaterial(Rhino.DocObjects.Material.DefaultMaterial)
                material.Emission = System.Drawing.Color.FromArgb(255, 0, 150, 0)
                material.Transparency = 0.5
                try:
                    for item in self.vector_surface:
                        args.Display.DrawDirectionArrow(item[0], item[1], System.Drawing.Color.FromArgb(67, 15, 137))
                    for brep in self.breps:
                        args.Display.DrawBrepShaded(brep, material)
                except:
                    pass

            def get_ClippingBox(self):
                return self.bb_pts


    else:
        pass
except:
    pass

import GhPython
import System
