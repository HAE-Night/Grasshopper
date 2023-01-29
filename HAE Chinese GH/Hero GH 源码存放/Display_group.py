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
import ghpythonlib.treehelpers as ght
import ghpythonlib.parallel as ghp
import Grasshopper.DataTree as gd
import Curve_group

Result = Curve_group.decryption()
try:
    if Result is True:
        """
            切割 -- primary
        """
        # 显示点序指向
        class ShowPointLine(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-分析点序", "RPP_ShowPointLine", """显示点序与线指向""", "Scavenger", "Display")
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

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "_place", "*", "占位符（各中心点）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFUSURBVEhLzdY7SwNBFIbh0XjBeBdiChEUxFKwCBKQFBF/gI2ljYKlhZ1YWNgo2NsJghYigsRCIgEvmCaCnRaChYX/wFrfb1bNKljs7gn4wQM7S9iZzJmzifvPaUMH+v6QQuw04RwPOEH5lwrO0IzYKeAFRbQiHTKEm8/rRJnAM0b9qJ4e6JskniCHGjJ+VE8/Ek+gVT5iyo9+ZgCJJzjCenD5Ha1c26XiXiD2BEvQSQlHxb7DE2ZxjE5Ezhj0EJ2Ur2zhHqrJJF6hz7QgcqqYDy7dOK6xj/B25KH+iNwH29gNLt0yVOQFPzLIDC7RhUOoBiMwSTeusIpbbMA0e3iDzva0blhmEe/YQbtuWEbHTKdhzo+Mov1uSIZxCrW4Vp2FWdQQJaygF2tQq+uHxSQ62+rQcDQ2K6pWqm3RygexCTWTafRgvYJVgwPo1duQ6N+CUZz7AGLYNfv2JbNQAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pts, self.lines, self.bbox = None, None, None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            def _get_lines(self, pts):
                loop_items = zip(pts, pts[1:] + pts[:1])[:len(pts) - 1]
                line_list = ghp.run(lambda pts: rg.Line(pts[0], pts[1]), loop_items)
                return line_list

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
                _gener = ghp.run(self._get_all_pts, data)
                pt_list = []
                if len(_gener) == 1:
                    pt_list = _gener[0]
                else:
                    for _ in _gener:
                        if isinstance(_, (list, tuple)):
                            pt_list += _
                        else:
                            pt_list.append(_)

                set_of_line = self._get_lines(pt_list)
                center_pt = rg.PointCloud(pt_list).GetBoundingBox(True).Center
                return pt_list, set_of_line, center_pt

            def RunScript(self, Geo):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc

                    origin_data = [list(_) for _ in Geo.Branches]
                    _place = gd[object]()

                    if origin_data:
                        list_pts, list_line, cen_pts = zip(*map(self._do_main, origin_data))
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
                        for line in f_lines:
                            args.Display.DrawArrow(line, System.Drawing.Color.FromArgb(0, 255, 255))
                    for f_items in self.pts:
                        for sub_index in range(len(f_items)):
                            args.Display.DrawDot(f_items[sub_index], str(sub_index), System.Drawing.Color.Wheat, System.Drawing.Color.Black)
                except:
                    pass

            def get_ClippingBox(self):
                return self.bbox

        # 曲线显示方向
        class CurvesDirection(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP-Crv Dir", "RPP_Crv Dir", """显示曲线方向""",
                                                                   "Scavenger", "Curve")
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
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                pass

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFlSURBVEhL3ZW7SgNRFEU3IQQfiNqLCrGyCH6AD7SztUntB4iIAW2irfj4D9FPEKKdoLYhRdCgjWUKiSEQGNdxzsg0NjO30Q2bO3POZS/umRlG/0dH0iPu4faxdMlaZS15O78Ie8JR2jvS24TUpN3Ht3jW9mbWoTRN8BKucYLmHBAtnEda60cqn0ZsacQ7AwhIsSANtPoRaT2KtNI1QDfuhlND5ZM4fL4ejfF8vB5MNvObovQ5w7hGpeG4tBG3AsrGxTNpbQMBZmNajjsBBWDP3qyqdMftOw4LIXzRAICeubXwsBDCpxxg34QpPITwnkEM5qWwEBuPAypeMqUhHStkFoBrH9O+lxIlEPsYs4vwLQe0WHljf/SKLXz4fZdVhJYI7/xyijBKnWJQlza9HFaEXyQQvMt1elz5RWCB4DODOKjJWsOVA2nSt+UXwfbXe0lAKT/4lvwibMRBV6xtbL/de2//eUlfCm+BqTOvCJUAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.pts = []

            def RunScript(self, C):
                self.c = C
                if not self.c: return
                self.bb = rg.BoundingBox()
                self.plist = []
                self.tlist = []

                for i in range(len(self.c)):
                    if not self.c[i]: return
                    # 检测曲线是否闭合 不闭合则终点也进行标注
                    if self.c[i].IsClosed == True:
                        n = 4
                    else:
                        n = 3

                    for j in range(1):
                        self.pt = rs.DivideCurve(self.c[i], n, True)  # 平切成N曲线 - 返回点

                        for k in range(len(self.pt)):
                            self.bb.Union(self.pt[k])  # 更新box边框
                            self.pts = rs.CurveClosestPoint(self.c[i], self.pt[k])  # 获取最近点
                            self.tg = rs.CurveTangent(self.c[i], self.pts)  # 切线
                            self.plist.append(self.pt[k])
                            self.tlist.append(self.tg)

                parts = len(self.c)
                self.p = [self.plist[(i * len(self.plist)) // parts:((i + 1) * len(self.plist)) // parts] for i in
                          range(parts)]
                self.t = [self.tlist[(i * len(self.plist)) // parts:((i + 1) * len(self.plist)) // parts] for i in
                          range(parts)]

            def DrawViewportWires(self, arg):
                if not self.c: return
                for i in range(len(self.c)):
                    if not self.c[i]: return
                    for j in range(4):
                        arg.Display.DrawDirectionArrow(self.p[i][j], self.t[i][j], System.Drawing.Color.White)

            def get_ClippingBox(self):
                return self.bb

        """
            切割 -- secondary
        """

        """
            切割 -- tertiary
        """

    else:
        pass
except:
    pass


import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Display_group"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "1.5"

    def get_AuthorName(self):
        return "ZiYE_Niko"

    def get_Id(self):
        return System.Guid("454e5931-0b6d-4d5f-bb40-0da0d9ddfab3")
