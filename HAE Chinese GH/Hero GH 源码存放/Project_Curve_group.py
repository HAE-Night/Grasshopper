# coding=utf-8
"""
均分曲线
    Inputs:
        Curve: 请输入一根曲线
        Espacement: 间距（默认300）
        HT_Length: 最后距离曲线的点至少大于（默认20）
        Offset: 偏移起始点在曲线上的位置（默认偏移0）
        Style: 平分样式 默认为：2（0：从起始点开始，1：从结束点开始，2：从中心点开始）
    Output:
        PointAtCurve: 在曲线上的点
        Parameter: 在曲线上的长度
"""
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
from System.Threading import Tasks
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree as gd
from Grasshopper.Kernel.Data import GH_Path
import Rhino.RhinoDoc as rd
import Grasshopper.Kernel as gk
import Rhino.DocObjects.ObjRef as objref
import math
import re
import copy


class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                           "RPP_均分曲线", "RPP_EquipartitionCurve", """根据曲线均分样式均分曲线""",
                                                           "Scavenger", "Project_Curve")
        return instance

    def get_ComponentGuid(self):
        return System.Guid("fd88cdbf-7b74-4bb2-b16f-8db923c58c0f")

    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True

    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Curve()
        self.SetUpParam(p, "Curve", "C", "请输入一根曲线")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Espacement", "L", "间距（默认300）")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "HT_Length", "B", "最后距离曲线的点至少大于（默认20）")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Offset", "O", "偏移起始点在曲线上的位置（默认偏移0）")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Style", "S", "平分样式 默认为：2（0：从起始点开始，1：从结束点开始，2：从中心点开始）")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)

    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "PointAtCurve", "PointAtCurve", "在曲线上的点")
        self.Params.Output.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Parameter", "Parameter", "在曲线上的长度")
        self.Params.Output.Add(p)

    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)

    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFmSURBVEhL7ZbJTsMwFEX7ffwLGyYBX4BA6qA4TpMmziyaoVLDpKzKsp918YtqSEiKUDEbxOLIqmPd8/xeInUkwuVRVtW3XpRph3JHXlwY9esW+brWDuVKQX5DP+SqHcr9F3yJdoFICjjBPZgTQKSlfoEvQw07wNxLGplWgap+yt1GRHtaBRQ6szzYftrIaE+bwE9XMJ2w6b2qnviWQOwYeuYnOeI0A19EmJjue+WKvQI6qCqxI9nbuJRhBcI0RyShlc6YQYEL6xkT7vfCiUEBHWyGJSsymIVrVuDYeMEZq3BprnHFK5zzJ5ywR5yyB9y5K3iyRUO37AkofBEuMWYObJF+7MlbcFntzC8x9kpMRQkelghki8Ik64S26Qt2bwLdoD0sNQfqOYXSKuL9wYqeoPkK5YfSDv8JHQGF0qtmufHgwA6hI6DQuew7zeDzwUPpCGhDV+WKnkA3f0aQGfXml/5VbLZ4A8yKgWyQDeC1AAAAAElFTkSuQmCC"
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

    # 可以作为树分支和路径取出还原模板
    # 取出树分支和路径
    def Branch_Route(self, Tree):
        Tree_list = [_ for _ in Tree.Branches]
        Tree_Path = [_ for _ in Tree.Paths]
        return Tree_list, Tree_Path

    # 根据树分支和路径还原树形
    def Restore_Tree(self, Before_Tree, Tree):
        Tree_list, Tree_Path = self.Branch_Route(Tree)
        After_Tree = gd[object]()
        for i in range(Tree.BranchCount):
            After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
        return After_Tree

    # 处理操作
    def Curve_Offset(self, Curve_Data):
        Curve = Curve_Data[0]
        Espacement, HT_Length, Offset, Style = Curve_Data[1]
        # 可以添加一个选择方式，从中间、头尾开始位置
        C_Length = Curve.GetLength()  # 曲线总长
        if Style == 0:  # 从曲线 开始点(Left) + 间隔 + 起始点偏移 开始
            Left = HT_Length + Offset
            Right = -1
        elif Style == 1:  # 从曲线 结束点(Right) - 间隔 - 结束点偏移 开始
            Left = C_Length + 1
            Right = C_Length - HT_Length - Offset
        else:  # 从曲线中心点(C_Center) 开始
            C_Center = C_Length / 2 - Offset
            Left = C_Center
            Right = C_Center - Espacement

        # 定位点长度位置
        Parameter = []
        # 定位点在曲线的位置
        PointAtCurve = []

        # 根据长度去判断每次偏移 Espacement
        while Left <= C_Length - HT_Length or Right >= 0 + HT_Length:
            # ± HT_Length 确保数据不在指定边缘范围内
            if 0 + HT_Length <= Left <= C_Length - HT_Length:
                Parameter.append(Left / C_Length)
            if 0 + HT_Length <= Right <= C_Length - HT_Length:
                Parameter.append(Right / C_Length)
            Left += Espacement
            Right -= Espacement

        if Style != 0 and Style != 1:
            Parameter.sort()

        # 得到在线上的这个长度
        for i in Parameter:
            PointAtCurve.append(Curve.PointAtLength(i * C_Length))

        return PointAtCurve, Parameter

    # 数据匹配
    def Data_Matching(self, Data, Matching_Data):
        return Matching_Data * len(Data)

    # Curve 多进程
    def Curve_Multiprocess(self, Combined_Data):
        Curve_list = list(Combined_Data[0])
        # 确保有数据
        if Curve_list == []:
            return [None], [None]

        Data = [Combined_Data[1]]
        Data = self.Data_Matching(Curve_list, Data)

        PointAtCurve, Parameter = list(zip(*ghp.run(self.Curve_Offset, zip(Curve_list, Data))))
        # （值，None）
        PointAtCurve = PointAtCurve[0]
        Parameter = Parameter[0]
        return PointAtCurve, Parameter

    # 处理操作
    def Processing_Operations(self, Curve, Espacement, HT_Length, Offset, Style):
        # 数据匹配
        Curve_Tree, Curve_Path = self.Branch_Route(Curve)
        Data = [(Espacement, HT_Length, Offset, Style)]
        Data = self.Data_Matching(Curve_Tree, Data)

        # 进入多进程
        PointAtCurve, Parameter = zip(*ghp.run(self.Curve_Multiprocess, zip(Curve_Tree, Data)))
        # 还原树形结构
        PointAtCurve = self.Restore_Tree(PointAtCurve, Curve)
        Parameter = self.Restore_Tree(Parameter, Curve)
        return PointAtCurve, Parameter

    # 间距、长度、偏移距离
    def RunScript(self, Curve, Espacement, HT_Length, Offset, Style):
        try:
            sc.doc = Rhino.RhinoDoc.ActiveDoc
            sc.doc.Views.Redraw()
            ghdoc = GhPython.DocReplacement.GrasshopperDocument()
            sc.doc = ghdoc

            # 参数定义
            if Espacement == None:
                Espacement = 300
            if HT_Length == None:
                HT_Length = 100
            if Offset == None:
                Offset = 0
            if Style == None:
                Style = 2
            if 'empty tree' in str(Curve):
                self.message2('请输入曲线')
                return gd[object](), gd[object]()
            else:
                return self.Processing_Operations(Curve, Espacement, HT_Length, Offset, Style)
        finally:
            # 预知代码Bug之前（抛异常）可用
            # self.mes_box("开发组测试", 1 | 32, "标题")
            self.Message = 'HAE开发组'


import GhPython
import System


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "RPP_EquipartitionCurve"

    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""

    def get_Id(self):
        return System.Guid("6e5c11c8-01ee-4182-8613-27adc2d3372f")
