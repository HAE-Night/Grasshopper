# -*- ecoding: utf-8 -*-
# @ModuleName: Geometry_group
# @Author: invincible
# @Time: 2022/7/8 11:21

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import Grasshopper.DataTree as gd
import Grasshopper.Kernel as gk
import ghpythonlib.parallel as ghp
import ghpythonlib.treehelpers as ght
from Grasshopper.Kernel.Data import GH_Path
import copy
import math
import initialization
from itertools import chain

Result = initialization.decryption()
Message = initialization.message()
try:
    if Result is True:
        # 几何体中心点
        class GeoCenter(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GeoCenter",
                                                                   "A1",
                                                                   """Find the center point of geometric object""",
                                                                   "Scavenger",
                                                                   "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("5a71f66c-d43d-4631-9a69-7c04cafb71a1")

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
                self.SetUpParam(p, "Geometry", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Center", "C", "Central point")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASNSURBVEhL5VV5TNN3FP9tHIqsA8YNa6k4sBwVKEfpRU96cJS2UNohp8BgiBzOwpAhBascCkpADpXB5iJzc9lm0Gii2RWybHOXIVnmH4gzbuiOzGQzbOq+e69tlnVec1n2zz7JSz7v+H6/v+977/t+1P8GDzECfDil4viKjcqk9tpMjkWfGqUHO9Ph/ufwMAtYTQMl0kvTdVnkwFNqMlQuJ8MVCvJ8rcau7zBnvMVhBMuc8Q+EmJ4i8fzRzTqy05zxXokw1gi2IIeLcqd5ekbVqziWPWXypaPNOtKkSRkH+8MO933gu8ojYWRD5s/jVcprwqgwhdPsX6dKKtmq5/W16Xm2Kgk7D2we6KiWr+t4Y4uBPGfgnQD1vof47i6WXt63QXkFeAjIylZt+sujlUoCdmItEFztLhR+v7dMTlAa1Mk7cZEkjm5602Ig9UrOGOp3RbU8cf9Mg5YEe3vHgRrQVyT5Gjb6tVgUWw+6nz3IAXqNPKlnEmrRmc9/Gw2Qxm2vQUpT14Tx7BF3QPj+ajXZqEreh0qHgTc/WCL7Fuhq1AGPZNOoLOUKKhO4PRUR/j4SLHaTJnkKdYyHW76D/DZgx0w9nUWABhi40abJGg0J9KPx0Sel07R7KxRXZqZ6yOGDNtJjzlhg0ah09MnjmQ0Ha9RkTZgfvULKbsYDvby8wtDngnYDf7a3SPKNnet5H7Xp0j9B7k9RYYNliuuvLJ0nuwghu0GOXZ4nVgPvK3CvAnHbbhJdb8pOsQFnYNoMadE6XOuC7YWiL7sLRaeRdxYIlmsUif3IC0I8So4c6ie99s1vgtwig8APjbQTNkWJMMaSmzbXVSDE1KwcKleQelVSC9pdAF9x0WoUHkMOebxZJUvoRp4T4pZ/ZKKT9MGmeIN+kCGQ6f5mEk1RqRizJTftNKz5AKgH1IE0qlO2od0FsPlZuMXnyDvy+Rc2Z6diXyMe7dalLR4/d4aMkN/IKNzg5NnjxJIZ/z743DEA4pfa8tIngfqMVSlJpSyhBu0u2KTmjENL3kBeKWVb4ZViwQNRD/GkYq1Zie+OtZbeGG0pXrbIYmbBbC9kRLCjkzQJkQJRLEM2XZdNOMxgLvpcwGGGqg435BJZfAQOMq9dxZLlFi33lMP7B7BlGQ5qhw+8lUud+YJzqLRquScHS2XXgK5A/a9whyJfhAUXUBGxwrOxba1GARZ+Ldr+jHX0QGH/eskCDMCf/KEtfb292fhIy6XsLmfI7UhhBmlff0ZPysXxI6hznwjNHIDHg6MCivghFPOAJZf7AtTqC0xL75MZn0FYBIhn33rx4p5S2VXgNFx7V5j5McMnnjWSMjF7wGmiKmXsqi6j8JTNlLFgM4nOw2GvmnisHKc7ADrw05fqcwjr8QCx03ZvlIriJnB4wbz/OHl1EI6GO8HdyFvbAJP3F7wNJzIUa/f3IWSFV8PP5kfMa1+R+LuWPO7sJnXKcGNW8kSHgT8H6SAzjVpM3RyEJzpWPTh8NEmRtVt16Wfgx/MDFBUPuwU3W4R38iKL/pjSGfevwA3EF+TeRfzvQFG/A5r0qwIsC8+HAAAAAElFTkSuQmCC"
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

            def Get_different_Center(self, brep, type_str):  # 不同的物体求中心点
                if "Plane" in type_str:
                    center = brep.Origin
                elif "Circle" in type_str or "Box" in type_str or 'Rectangle' in type_str:
                    center = brep.Center
                elif "Point" in type_str:
                    center = brep
                elif "Arc" in type_str or "Curve" in type_str:
                    brep = brep.ToNurbsCurve()
                    center = brep.GetBoundingBox(True).Center
                elif "Line" in type_str:
                    center = brep.BoundingBox.Center
                else:
                    center = brep.GetBoundingBox(True).Center
                return center

            # 求边界框的中心点
            def center_box(self, Box):
                if not Box: return
                type_str = str(type(Box))

                # 群组物体判断
                if 'List[object]' in type_str:
                    bbox = rg.BoundingBox.Empty  # 获取边界框
                    Pt = []
                    for brep in Box:
                        type_str = str(type(brep))
                        if "Circle" in type_str or 'Rectangle' in type_str or "Box" in type_str:
                            bbox.Union(brep.BoundingBox)  # 获取几何边界
                        elif "Plane" in type_str or 'Point' in type_str or 'Arc' in type_str:
                            Pt.append(self.Get_different_Center(brep, type_str))
                            bbox = rg.BoundingBox(Pt)
                        elif "Curve" in type_str:
                            brep = brep.ToNurbsCurve()
                            bbox.Union(brep.GetBoundingBox(True))
                        elif "Line" in type_str:
                            bbox.Union(brep.BoundingBox.Center)
                        else:
                            bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))

                    center = bbox.Center
                else:  # 不是群组
                    center = self.Get_different_Center(Box, type_str)
                return center

            def GeoCenter(self, Geo):
                if Geo:
                    center = ghp.run(self.center_box, Geo)
                    return center
                else:
                    return [None]

            def RunScript(self, Geometry):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        Cenp = gd[object]()
                        Geolist = [list(Branch) for Branch in Geometry.Branches]  # 将树转化为列表
                        Cenpt = ghp.run(self.GeoCenter, Geolist)  # 主方法运行
                        Cenp = self.Restore_Tree(Cenpt, Geometry)  # 还原树分支
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Cenp
                finally:
                    self.Message = 'HAE center point'


        # 几何排序
        class Value_And_Sort(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Value_And_Sort", "A4",
                                                                   """Ordering of geometric objects ，value is selected after the sorting finished, support area and length sorting，but data must be the same in same set；add dot order sort ，enter the axis to be used as a reference in the point order sort （The default is X-axis comparison）""",
                                                                   "Scavenger",
                                                                   "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("a2cd7d1d-1260-43f9-8164-1f356db3927d")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Extract subscript，if no input, default is output all ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Loop", "L", "Ergodic value，on by default，it's going to take a value from 0 to index ，Float close ，in this case, only the value of index+1 will be taken")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

                p = Grasshopper.Kernel.Parameters.Param_Boolean()
                self.SetUpParam(p, "Sort", "S", "Select sort mode，descending by default，select Float in ascending order")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                p.PersistentData.Append(Grasshopper.Kernel.Types.GH_Boolean(True))  # 将默认值设为True
                self.Params.RegisterInputParam(p)

                p = Grasshopper.Kernel.Parameters.Param_String()
                self.SetUpParam(p, "Axis", "A", "Enter when ordering dots，other geometric objects are sorted without input ")
                DEFAULTAXIS = 'x'
                p.SetPersistentData(gk.Types.GH_String(DEFAULTAXIS))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "A_Objects", "AO", "If subscript is entered, the geometric object from 0 to index is retrieved ，if no input, Default is output all ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "A_Values", "A", "If subscript is entered, the value from 0 to index is retrieved，if no input, Default is output all")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "B_Objects", "BO", "If a subscript is entered, the geometric object at the end of index is retrieved，if no input, Default is output all")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "B_Values", "B", "If a subscript is entered, the geometric object at the end of index is retrieved，if no input, Default is output all")
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
                        self.marshal.SetOutput(result[2], DA, 2, True)
                        self.marshal.SetOutput(result[3], DA, 3, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAATRSURBVEhLzZV5TJRHFMA3kFUqupRj10VZFuTa3e/YXWAFQbBdkW4hobCwoCyHFNACcnhU8QAsApVwSFpAjopoUaSlHm2plHqCNJpqtAmtjWnrH7VpjGm0BYXYxtc3H6OJoRCapkl/yeSbN/Nm3jfvvXkj+j8hw2ae7D5Dik0y2f2XONrP7ZQ5zO+hIsFWKpk3KBaLGSKUlZXZ8Bx3iWXZUmH2H8LlRwWBkfNsprIo2EdRXhAdBNhVEjlAq43VabXAsewdjUYzn4zNmpdYj+EvytLAb7HLUwO6hgzTk0prxBPse5AB8vd6PW/W63XHOYYpJGOzYq5YnN1VGA99O1OIgUYylhrO3/i2IRc2x4T+iaI8MjJSwfMc4MY78BRnWYb5jujNBllWRMD9r+ty4HBhAngtcql2d16wpX+XFUb25cJWczhxkbNep2vFE3zJ82yJjueLsT/Ba3jT5BYzoF4sPTJcmQXEPR358eC7SNoml7xgMHIeVdmRgZdjlqrvY5C1er22j2EYLV0mCvTX7eU4roqK0xLRkPEqXMe/P7FtNRzYEA+MUt5F5wi22CzYngW0/vHDvJqJ3zVUnJE5rxlUt26+kw+fl6ZC75tJ0J5nBo27vJvOi9xcHKp85I4HqChQNz76We342CtUnB6pg335QEkaXKleB5/uSIZjmxKhNdcMaoVrL1XxK0lYAQnB6jYqC9RNjPXUjI8aqTgtqu1xYY9vNRYKvj9VvAaOFFmgBQ3ol7h9QBQSgjTDX1Vnw3K1Usiqp6B7uvY++i2Ein9PiK/i/DcNG+BSVRb0l6TA8a2rhQzajwZU7q4HWYVs/UBJKpzdnQ7BfopWukzUODYmb/pj4mLt+MM8OjQVGxtRWndRAow05Asb9O20wodbkqCzIB6ac8yw0MnhJt6BR9dr18MZnA9RKzvpUlHd3bvebQBQO/HwEB2aglOmUX/v9v6NMFiRCQMY3I+3o/83J2KKmqEZT6D1UlxwmW8XFuy9uMIarr2qdpPuo2sFqkcf1Lz94F4AFZ/H19W54+redXCtJgfOla8V3HNy2xo4utGCKWqGJjyB3sd9gKoT5mEjaTorwhvWmuCHpiLh78/sThPc8xH6vwtd1p4XJxjw93E/R/VFXgsd6zVuUiHopJIuWxHIGgxa3fKVBl+jMWihoER5MSmUufljUyFcxhNcKM8Qcv8TTE/i//cxwG25sWggHgx+HoN0DVuZbISkEKaDCBaLZQ7e5madTnsYv99zHHte0KJENWVFwc/tW2AIywIJ7ml0z6niZOhB/x/CALfmxEIjGljq53mBLEhezl29VrMOwhnlc/fAajVJtDz/C6tiV9EhAVtvV+fieiwLI5ieF/dkCO45gf4/tskiZFDLG2ggNx70vsp+wxL5riHUOfdWOoSqPQ7SPQSwVF/BmjRtDYp7faX+Dqk7Q5WZeMnS4SSe4ije4vcwyC35iaBSLvopJtDnHqmmp3elQhjjKcSAEBjoX0HeBCpOi4ubk6QkYZnmRkF08ERp4stQmbIKWyRUpUeTLLqNOm4Se7uklZxXt6fMqYYsMplMEtz8V3TPIMahV6fj3yWBJ3MzQZ7CMDs7cZJC5lQkc1iw0U4stk5OTcEGn0m5Wq32UalULPnS8f8akegvQXjx8z+3HH8AAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.axis = None

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

            def get_value_sort(self, object_list, data_type, sorting):
                temp_objects = map(self._trun_object, object_list)
                origin_data = None
                if data_type == gk.Types.GH_Brep or data_type == gk.Types.GH_Surface:
                    origin_data = [o.GetArea() for o in temp_objects]
                elif data_type == gk.Types.GH_Curve or data_type == gk.Types.GH_Circle or data_type == gk.Types.GH_Arc:
                    origin_data = [o.ToNurbsCurve().GetLength() for o in temp_objects]
                elif data_type == gk.Types.GH_Point:
                    origin_data = eval('[o.{} for o in temp_objects]'.format(self.axis))
                values = sorted(origin_data)
                temp_list = sorted(enumerate(origin_data), key=lambda x: x[1])
                index_list = [t[0] for t in temp_list]
                objects = [object_list[index] for index in index_list]
                if sorting == True:
                    return objects, values
                elif sorting == False:
                    values = values[::-1]
                    objects = objects[::-1]
                    return objects, values

            def is_sametype(self, list_data):
                Curve = [rg.PolyCurve, rg.LineCurve, rg.Curve, rg.ArcCurve, rg.PolylineCurve, rg.Polyline, rg.Line, rg.NurbsCurve]
                temp1 = [type(t) for t in list_data]
                temp1 = set(temp1)
                for x in temp1:
                    if x in Curve:
                        return True, rg.Curve
                    else:
                        copy_list = list_data[::]
                        for i in range(len(list_data)):
                            copy_list[i] = type(list_data[i])
                        temp2 = set(copy_list)
                        if len(temp2) == 1:
                            return True, type(list_data[0])
                        else:
                            return False, 'The data type is inconsistent！！'

            def switch_handing(self, array_data, index, loop):
                if index is None:
                    return array_data, array_data
                else:
                    a_list_data = b_list_data = None
                    if loop == True:
                        a_list_data, b_list_data = array_data[0:index], array_data[index:len(array_data)]
                    elif loop == False:
                        a_list_data, b_list_data = array_data[index], array_data[index]
                    return a_list_data, b_list_data

            def RunScript(self, Geometry, Index, Loop, Sort, Axis):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    A_Objects, A_Values, B_Objects, B_Values = (gd[object]() for _ in range(4))
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        self.axis = Axis.upper()
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_geo = [list(i) for i in structure_tree.Branches][self.RunCount - 1]
                        g_bool, g_type = self.is_sametype(origin_geo)
                        objs, vals = None, None
                        if g_bool is True:
                            objs, vals = self.get_value_sort(origin_geo, g_type, Sort)
                        A_Objects, B_Objects = self.switch_handing(objs, Index, Loop)
                        A_Values, B_Values = self.switch_handing(vals, Index, Loop)
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return A_Objects, A_Values, B_Objects, B_Values
                finally:
                    self.Message = 'Geometric ordering'


        # 几何体的中心平面
        class GeoCenterPlane(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_GeometryPlane", "A2",
                                                                   """Find the central plane of a geometric object""",
                                                                   "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("718640f5-8562-4c71-9690-9d6d8f72ebca")

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
                self.SetUpParam(p, "Geometry", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Geometric object plane（The curve is at the starting point, the surface is at the center, and the geometry is at the center of the largest surface ）")
                self.Params.Output.Add(p)

            def SolveInstance(self, DA):
                p0 = self.marshal.GetInput(DA, 0)
                result = self.RunScript(p0)

                if result is not None:
                    self.marshal.SetOutput(result, DA, 0, True)

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHzSURBVEhLYxgFVAWd/17z9v77xwnlUh9M+/8/dP6/fxZQLllAAogVcOGEo0dLXJeuiMAmhwWzATEqUJUU3Jvtbvgr1VkPA6fbafwq7an7k1+U9DvdXgsopv8r3V7zV7oDkO2iD1eX6270y01X4RfQOCOIqUjAw1DxyOWe5P8nW2L/n0DDp6sC/2/cPOv/zoXN/0/Vhf0/XR30/8Ccqv/bd8z9f6o+HK7uWm/K/+5ox/9A40wgpiIBFz35g4cbo//vqgr7vxMN7yn0/r9i3fT/G6ZV/t+X7fx/04TC//NO7/6/pSPj/67yILi6Y00x/xtCbEAWGENMRQL4LfD6v3zTnP+rlvf/39yd/X/eqV3/tzUl/N9d4vd/Z3U4XB1FFqxcPfn/tIfX/s+8dRbo6uD/e/PcgBb4gy0B49IA8i3Ym+/5f+m2Bf8nvX7yf9a1E//XLOr4v25OIxA3/F83ux6IG/5vmFIOtcCadAt2lQX+39yb93/52unAuJjxf9mW+UA8D0wv3Tr//5Lti/+vWDsNYkEwGRaAwhlkyZ4CLwgGBhkCe0PoIh/yg4hYPLAWuBsoHr/cnYQ1oxGLrwEzahcko5lCTEUC8qJ8G6JttF6GW2i8DCMTx9pqv7RRl3kJNE4fYioq4AJiXiphZiAeBcMfMDAAAINxNy+65216AAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def mes_box(self, info, button, title):
                return rs.MessageBox(info, button, title)

            # 根据树分支和路径还原树形
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [i for i in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # 曲线类的平面
            def Curve_Plane(self, Curve):
                NurbsCurve = Curve.ToNurbsCurve()
                if len(NurbsCurve.Points) - 1 >= 2:
                    # NurbCurve 不是直线使用三点确定平面
                    NurbP = NurbsCurve.Points[1]
                    U = rg.Point3d(NurbP.X, NurbP.Y, NurbP.Z)
                    V = Curve.PointAtEnd
                else:
                    # Curve 是直线使用 UV 方向去得到平面
                    U = rg.Vector3d(Curve.PointAtEnd - Curve.PointAtStart)
                    V = rg.Vector3d.CrossProduct(U, rg.Vector3d(0, 0, 1))
                    if V.Length < 0.01:
                        V = rg.Vector3d.CrossProduct(U, rg.Vector3d(0, 1, 0))
                Plane = rg.Plane(Curve.PointAtStart, U, -V)

                return Plane

            # Brep最大面下标
            def BrepFaces_Max(self, Brep):
                # rg.AreaMassProperties.Compute(face).Area 方法是得到 Brep 各个面的面积
                BrepFaces = [rg.AreaMassProperties.Compute(face).Area for face in Brep.Faces]
                return BrepFaces.index(max(BrepFaces))  # 第一个最大值下标

            # 根据中心点求面 -- U,V与原生不符，却与SEG相符
            def Brep_Plane(self, Brep):
                # Surface
                if Brep.Faces.Count <= 1:
                    Box = Brep.GetBoundingBox(False)
                    Center = Box.Center
                    Normal = Brep.Faces[0].NormalAt(0.5, 0.5)
                else:  # Brep
                    # self.BrepFaces_Max()  求 Brep 立体的最大面的下标
                    BrepFaces = Brep.Faces[self.BrepFaces_Max(Brep)]
                    Box = BrepFaces.GetBoundingBox(False)
                    Center = Box.Center
                    Normal = BrepFaces.NormalAt(0.5, 0.5)
                # 计算法向量并给面的 Z 轴
                Plane = rg.Plane(Center, Normal)
                return Plane

            # 类型对应
            def Type_Correspondence(self, Geometry):
                if 'Point' in str(Geometry):
                    # Geometry 是 Point 类型不属于 Point3d 也转换不了 Point3d
                    #            return rg.Plane(Geometry, rg.Vector3d.XAxis, rg.Vector3d.YAxis)
                    return None
                elif 'Curve' in str(Geometry):
                    return self.Curve_Plane(Geometry)
                elif 'Brep' in str(Geometry):
                    return self.Brep_Plane(Geometry)

            # 对象多进程
            def Object_Multiprocess(self, Geometry_List):
                return ghp.run(self.Type_Correspondence, Geometry_List)

            # 物体操作：
            def Object_Operations(self, Geometry):
                Geometry_Tree = [list(i) for i in Geometry.Branches]
                return ghp.run(self.Object_Multiprocess, Geometry_Tree)

            def RunScript(self, Geometry):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object]()
                    else:
                        sc.doc = Rhino.RhinoDoc.ActiveDoc
                        sc.doc.Views.Redraw()
                        Plane = self.Object_Operations(Geometry)
                        Plane = self.Restore_Tree(Plane, Geometry)
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        return Plane
                finally:
                    self.Message = 'Geometric central plane'


        # Geo|Plane分隔
        class Brep_PLane_Group(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "Geo_PLane_Group", "A3",
                                                                   """Groups geometry according to Plane，all Z-axes direction need to be the same as the first Plane，and the first plane must face outward with its z-axis""",
                                                                   "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3bab47c8-1132-4f8a-bf91-5373b81fc90b")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Brep", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PLane", "P", "Dividing plane-The Z axis of the first dividing plane faces outward")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Brep", "G", "Separated geometric objects")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "I", "Original subscript of geometry")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANkSURBVEhL7VRbSBRRGN5mdy3Tyi1pK40uFrM71zM7a7qbOYoaXV3T1XXLTEUjCwyimyWZZGVUTxnLQHerVeshonpoKyrpQkWU9BRBERG4rmEU+LZ/54xDWBis9NJDH3zwz/ef83/n8s8x/Mc/g0mYqZjJmJMxJ2D+DShMUiNR+zJTVFWBkDZUlGH/WphOh20pyb1YJkYGWQUz3zXoJ7HYFVmT3v1+BolHg9FoXJq1cGavxzH3bXnGwo9M6rTXWoKiqNqjlQXQvb0Uru32g28x+x3LFi0JMI6/1H9IuPrtjBgMnxcuvErQ9NFAUes6NubD8+ZSeNNaDhuy7P26TtXs9+XA6S0e6NhaDF4XE8FykpbEIEWlmwDoUljRpdFBUT61Kgfu7fLAo73FsM5Nf9L1UQ3GOSXJJ1qtrHArug91RlSuc/As0903fK46VsnyREVRhrVYDUpcDNmaUeTZl7xjUUC8ES0j48TL4TJncGA2iQkQQgWiKLa43W7SJLEblLqZD8bxU3IREoHj2M/aoBHIzMyMdyDUynNcmGXZNF2O3cDrZj4lWKwcXt0TjuOCNE0Pr1AHXnmj7HBgc+73OylUq3NjOSL7ANHxDgJ2jquAF6o51Lw+/+nh2j2bPHmB+TR7iMcgYxzdkSrcvilZvVHBWrT1YqDcGY31krGBcNbGMHVf1F1Tnh2sU841eK97cjKvaJN0oM5wKeoauCjfjapJiv9IwJ8RcxdpBoIg1JNYEqSaturVVwHA2Nfe/EsnCcHIPXQn2oxDRa2K4YhGGJzhEVqbsoAuqVy+JPTgQHXwfmt1Q09bLatN1CF2DRxGz6MeHOaP5T8w4EsOYL5jOGHfzrXL+ZYNq/JcLtec6fMyrAg59kiS1JQupTul4w+XOXuG5uMpnrEYUEgQGvERfRA4LmS3s3dpO3Mbd85Dnhd7eI4HpywDvus+fl7qZr1Q2R8NDvhz4XzDGujc5iVvETH4+VQwDBNHKMuymVBRDCZsXI53V2az2abpw0gh36maXHjQWARPmkqgYoRB/V5vNrTXrYCTdSthqZgGWJ6qJccCiqo8UZENoR2F8LipGPCL+k3TTSZTtjUpQbUmJR6zJMS3xMeZGrA8XkuOAWazGaVMTWynZ1rOSXOSr8yyJHboqf/4EwyGHx96tDME8SyiAAAAAElFTkSuQmCC"
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

            # 数据转换成树和原树路径
            def Restore_Tree(self, Before_Tree, Tree):
                Tree_Path = [_ for _ in Tree.Paths]
                After_Tree = gd[object]()
                for i in range(Tree.BranchCount):
                    After_Tree.AddRange(Before_Tree[i], Tree_Path[i])
                return After_Tree

            # Geo 分隔
            def split(self, _brep_dict, _pln_s):
                _A_brep = []
                brep_negative = []
                for brep in range(len(_brep_dict)):
                    if not _brep_dict[brep][0]:
                        continue
                    else:
                        if type(_brep_dict[brep][0]) == rg.Point3d:  # 判断物体的类型
                            brep_centroid = _brep_dict[brep][0]

                        elif type(_brep_dict[brep][0]) == rg.Circle or type(_brep_dict[brep][0]) == rg.Arc \
                                or type(_brep_dict[brep][0]) == rg.Rectangle3d:
                            brep_centroid = _brep_dict[brep][0].Center

                        else:
                            brep_centroid = _brep_dict[brep][0].GetBoundingBox(True).Center  # 获取Brep物体的中心点
                        projection = _pln_s.ClosestPoint(brep_centroid)  # 生成中心点在PLN的投影点，并生成两点向量
                        normal = brep_centroid - projection

                        # 判断法线向量是否与Plane法线向量同向
                        if normal * _pln_s.Normal > 0:
                            _A_brep.append(_brep_dict[brep])
                        else:
                            brep_negative.append(_brep_dict[brep])
                return _A_brep, brep_negative

            # 主函数
            def Brep_Plane_split(self, BPSdatas):
                _brep_list = list(map(self._trun_object, BPSdatas[0]))
                _brep_dict = zip(_brep_list, range(0, len(_brep_list)))
                _plane_list = BPSdatas[1]

                brep_positive, brep_positive_index = [], []  # 返回值保存
                end_brep = []  # 保存剩余数据

                """
                可替换成for循环，针对不同的情况替换调用参数和接收返回值
                """
                if len(_plane_list) == 1:
                    brep_p, brep_nega = self.split(_brep_dict, _plane_list[0])
                    brep_positive.append(brep_p)
                    brep_positive.append(brep_nega)
                else:
                    for _pln in range(len(_plane_list)):
                        if _pln == 0:  # 参数全部brep 第一个pln
                            brep_p, brep_nega = self.split(_brep_dict, _plane_list[_pln])
                            brep_positive.append(brep_p)
                            end_brep.append(brep_nega)
                        elif _pln + 1 == len(_plane_list):  # 参数：最后剩余的brep
                            brep_p, brep_nega = self.split(end_brep[-1], _plane_list[_pln])
                            brep_positive.append(brep_p)
                            brep_positive.append(brep_nega)
                        elif _pln < len(_plane_list):
                            brep_p, brep_nega = self.split(end_brep[-1], _plane_list[_pln])
                            brep_positive.append(brep_p)
                            end_brep.append(brep_nega)
                        else:
                            continue
                brep_positive = map(lambda x: [(BPSdatas[0][_[1]], _[1]) for _ in x], brep_positive)
                return brep_positive

            # 数据整合
            def data_settle(self, __data1, __data2):
                if len(__data1) == len(__data2):
                    return zip(__data1, __data2)
                elif len(__data1) > len(__data2):
                    for i in range(len(__data1) - len(__data2)):
                        __data2.append(__data2[-1])
                    return zip(__data1, __data2)
                elif len(__data1) < len(__data2):
                    for i in range(len(__data1) - len(__data2)):
                        __data1.append(__data1[-1])
                    return zip(__data1, __data2)

            def RunScript(self, Breps, Planes):
                try:
                    re_mes = Message.RE_MES([Breps, Planes], ['Breps', 'Planes'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object]()
                    else:
                        structure_tree = self.Params.Input[0].VolatileData
                        breps_list = self.Branch_Route(structure_tree)[0]
                        paths_list = [_i for _i in structure_tree.Paths]
                        Planes_list = self.Branch_Route(Planes)[0]

                        new_data = self.data_settle(breps_list, Planes_list)
                        BPSdatas = ghp.run(self.Brep_Plane_split, new_data)

                        Geo_Dtree = gd[object]()
                        index_Dtree = gd[object]()

                        # 树形数据结果匹配
                        for _1 in range(len(BPSdatas)):
                            for _2 in range(len(BPSdatas[_1])):
                                GH_PATH = paths_list[_1].AppendElement(_2)
                                BPSdatas_list = list(zip(*BPSdatas[_1][_2]))
                                if BPSdatas_list:
                                    Geo_Dtree.AddRange(BPSdatas_list[0], GH_Path(GH_PATH))
                                    index_Dtree.AddRange(BPSdatas_list[1], GH_Path(GH_PATH))
                                else:
                                    Geo_Dtree.AddRange("", GH_Path(GH_PATH))
                                    index_Dtree.AddRange("", GH_Path(GH_PATH))
                        sc.doc.Views.Redraw()
                        ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                        sc.doc = ghdoc
                        Rhino.RhinoApp.Wait()
                        return Geo_Dtree, index_Dtree
                finally:
                    self.Message = 'Geo|Plane group'


        # 分解几何物体
        class DestructionGeometry(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_DestructionGeometry", "A12",
                                                                   """Decomposition of multiple geometric objects（Brep，Curve etc），noted that the flat output of the line is inconsistent with the curve """, "Scavenger",
                                                                   "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("ed705333-be7c-459f-a18f-25152869e1c1")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geometry", "G", "Geometric object，Supports multiple different geometric objects")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Vertex", "V", "The point from decomposed object ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Edge", "E", "The edge obtained by the decomposition of the object")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Face", "F", "The face obtained from Brep decomposition ，curve return null")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneA", "PA", "The standard central coordinate of a geometric object ")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneB", "PB", "The center coordinates of a geometric object determine the coordinates within the X-axis vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "PlaneC", "PC", "The center coordinates of a geometric object determine the coordinates within the Y-axis vector")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAN+SURBVEhL7ZRZSJRRFMcHisqMilbfjJpE3HNrZlxm/2ZGnaVxsslZHDUd11LLylLbbDEdyyxNszI1pbRASkhIinqo93roqY20ILKEkoTodM7nLZCyGuixH1zud7n3rPd/P8F//gUL2Ews220SN+RpIhPYmliCY87Up5e4EoP3XHDrRo7ZZIf8l8/3q7fLu+4fsEGTS/l03So/f49DXt6Szb2tMIkvMRPv8NgVnde3b4BrZSZozuI+YAA4k6WGy8V6OLpZ+rGrMAVu7EwFj0Nxh5n8NfNw+FalxnWeRoe5qvD+OrsMLuTp4IRTyc/dRSlQpIl6cB6/69Jl98JWr1yBNkt569/BRawKRyfP293a1y1buIlzuVo45VK9aspUfW3O5oCqoPlKiRGOWKVjVFGdTfapPVc75nEqxrPkwRxz9Wu4iDWSnq0G6CxMhrYcDbRs0fAZkyMMMnoyQzm6Q7+eZjjv1vF7h60J78+5tV+6i1O+FHPREuZqZirNko5WdE5OsddwBjNOiwv24JYvjvk0yg2ivEsFyfw+Vgp0V3vNkl6ynxGLKEiI5TZjZu8u5icBZUmBGl2qJ6UWkQ879oMKo2gIqwIKhC2FxgzlBCqsxywOCGRHprPfEvfydqUVL1Ix6ZKGDFCvSTG6qEAnOzKNhT4+sW05Wr6duerwwePpsvHhKivsS42fWD79/UyRKQ/JRFU8I+U0OBRjJMOmTDVsS4oZZkem0ehUtnehmuodcqhNl73vwKqbs9XPK0ySfNyePXXqZ3yqzZIrfaVGOI3OD1sToXerHqpTJTlsn0e81i/xLAoAHxvfRmpplVk8hFsk8ZnZLA1Y1prDPSZ9fzemVmFm446E4NaaTQlt9XZZW4VJ9JL26F3QPTS6lBhE98YQKwxirn5NtiJMT2VT7/GFAmVJLetF6ZIsSbrtOFPfaaZESKo9eP4qvg1bfFAxczUjs4zRQn3NpviN9Tb5Q1JIoS6mD1UySY+Ogn5XWB4XebM2XTpZY018VG6IleerIqRCoWAu8/NnsEXd3UV6vEDpZ3JOd9HgVECtTc5XSIEoAfzh3WUm3nFwY3z/4C4LoPORsuTYnajzJ7f2pOFaN56vDrdj/4cHys1QbYl7yEy8Y0N0YIhbGVGwaJFgMa3LkmM0qPsXWbLQAv4AUpIUZdSErolky3/C72X4H+8QCL4Boz2mS+QkNFMAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def explode_curve__get_plane(self, curve):
                origin_list = curve.DuplicateSegments()
                length_point = len(origin_list)
                if length_point == 1:
                    c_list = [curve]
                    curve_plane = self.get_normal_plane(curve)
                    points = [curve.PointAtStart, curve.PointAtEnd]
                    return points, c_list, None, curve_plane
                elif length_point > 1:
                    c_list = [_ for _ in origin_list]
                    point = []
                    for line in c_list:
                        point.append(line.PointAtStart)
                        point.append(line.PointAtEnd)
                    p_list = [point[i] for i in range(len(point)) if i % 2 != 0]
                    p_list.insert(0, point[0])
                    if curve.IsClosed is True:
                        curve_plane = self.get_polygon_plane(p_list) if length_point != 3 else ghc.XYPlane(ghc.Area(curve)['centroid'])
                    else:
                        curve_plane = self.get_normal_plane(curve)
                    return p_list, c_list, None, curve_plane

            def explode_brep__get_plane(self, brep):
                V, E, F = brep.Vertices, brep.Edges, brep.Faces
                length_brep = len([_ for _ in E])
                vertex_list = [i.Location for i in V]
                brep_plane = self.get_polygon_plane(vertex_list) if length_brep != 3 else ghc.XYPlane(ghc.Area(brep)['centroid'])
                return V, E, F, brep_plane

            def get_polygon_plane(self, points_list):
                x, y, z = 0, 0, 0
                for point in points_list:
                    x += point[0] / len(points_list)
                    y += point[1] / len(points_list)
                    z += point[2] / len(points_list)
                center_point = rg.Point3d(x, y, z)
                single_vertex = list(zip(points_list, points_list[1:] + points_list[:1]))
                vector_list = [i - j for i, j in single_vertex]
                axis_list = vector_list[2:]
                object_plane = rg.Plane(center_point, axis_list[0], axis_list[1])
                return object_plane

            def get_normal_plane(self, single_data):
                point = single_data.PointAtStart
                start_vector = single_data.TangentAtStart
                end_vector = single_data.TangentAtEnd
                if start_vector == end_vector:
                    origin_plane = rg.Plane(point, end_vector)
                    normal_plane = copy.copy(origin_plane)
                    normal_plane.Rotate(math.radians(90), -1 * normal_plane[2])
                else:
                    normal_plane = rg.Plane(point, start_vector, end_vector)
                return normal_plane

            def base_rotate(self, plane, axis):
                dict_axis = {1: 'XAxis', 2: 'YAxis', 3: 'ZAxis'}
                rot_plane = copy.copy(plane)
                angle = math.radians(90)
                rot_plane.Rotate(angle, eval('rot_plane.{}'.format(dict_axis[axis])))
                return rot_plane

            def RunScript(self, Geometry):
                try:
                    re_mes = Message.RE_MES([Geometry], ['Geometry'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                        return gd[object](), gd[object](), gd[object](), gd[object](), gd[object](), gd[object]()
                    else:
                        temp_geo = Geometry
                        Vertex, Edge, Face, Plane = None, None, None, None
                        if isinstance(temp_geo, (rg.Curve, rg.PolyCurve, rg.Polyline, rg.PolylineCurve, rg.NurbsCurve,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_curve__get_plane(temp_geo)
                        elif isinstance(temp_geo, (rg.Brep, rg.Surface, rg.NurbsSurface,)) is True:
                            Vertex, Edge, Face, Plane = self.explode_brep__get_plane(temp_geo)
                        PlaneA, PlaneB, PlaneC = Plane, self.base_rotate(Plane, 1), self.base_rotate(Plane, 2)
                        return Vertex, Edge, Face, PlaneA, PlaneB, PlaneC
                finally:
                    self.Message = 'Geometric decomposition'


        # 数据类型分类
        class TypeClassification(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_TypeClassification", "A11", """GH geometric data type classification""", "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("871bc32c-c64a-454c-b2af-b20ed09c766f")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "List of data types instantiated by Grasshopper")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point", "P", "Point type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Vector type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Line type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Plane type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Brep()
                self.SetUpParam(p, "Brep", "B", "Brep type")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Surface()
                self.SetUpParam(p, "Surface", "S", "Surface type")
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

            def get_Internal_Icon_24x24(self):
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASGSURBVEhLrZULUFRVGMevWDRD0EYqxENUGqQYRHmIINKEA4umxsOKxgnloRsa5CqaCMQrdt0Niikg6A3ZmE1jPjKmxNGpxkZikk1oh0ptTAWXx7Ysy2OF9vT/zt5d2BmckZl+M7/d833n7r3n3vudb4VZ8gj0hhIe/Q+4wR2wFfbBCfgvNMOb8BhMhU5w1uyDRkgnbYH74QYYDemkZfACZPBvmAbvCQ94FtJKy+F8aCd8iWe2OLTxGPwI0oU+hXPhXfGQLFx4M7WhjrkJzkvFnJ0nA33iGrKlbM1SnxAxNZ21cAB+B2e8CCU1c5ycNFUTY4o6i+WwNT1FXmJ40+81O1jJ5tXHxZQD8uMnZYHSBLqTD60ZRxSQJr0oKO/rbVKPjzTRmFjg4vLoB7LEyW5c4GxxGktbFfiUOMWpsUzKVUbDLyuzM3cipPMk8QkReu6UzOORSMVg3wnVmOktGkcs9kyry4y/Vp8t7fw45+lft6x54hA/CFSbx+sPXunWRO3Z4yOmPoe3oL26SiFVzH08msKp0jBwXjlqKrLF4jenizFn9ehwy6vdXV+LKRuLIC14HY/AH/A965DXPm0ojuzUKReFUd+uvjMmE1OcIxaLt9Jo6Mjv0tSIqYfhEuuQ0wGP0IAmqCRTKMhaG5KTk7CCNpCdAq12nsJk6FIOG3itv22xRFXqB67tbm+j5815KT40V74+4nsxJNTwLxoEQ7od+hbefDGu9fSBZ5n/fLcAim2U3rrqpzTqz9VO3imqGNS15/70Y7w4xanG784UPs+W+XosE1Nb4QgNIiGvHn/PBz0+y91ovlyVxQpTovjtTQcvvLqZMZbf0U472o6Xu7vf4dwN5k78riR19RdiOhlSSxGCIF3AuzA5qlSjzmRtinR2bG8yNpRXDB1AqMaHm8t1PUdfu3494dCosaP4xg37He5KDFNdUmWwi5Xp7Et5Ektd5U9zm6GJ5h+CkzApPTZoG1ZQtCsh7BX5+rDt/oIQoNLrJcqRofPl/b3v08GEesK0UTH8T7dcq+V7JiUyYGtRSvQ+WXxoTm5iWEZsiB+9bNpXV2ie0MJm63CKBsYWK02GzrJ+HTU6G770oRo1bascGtTkXWyhBc6EwzkPwDH4AI/A64O6dQrT0J8V/bfpWdrJSwz7OS3Guovx2PZin1wIl8nu55NTUB+jxx7HI+AOLbCAgrKB3jysXFuh1y2n2EaIr2fwmaI0VvlCrL2MVeYRRcXA7W/F0MZJeNU6nKJgrrMzQ3t4B3XeUm00OrRpIn/TyqoOdQY7unvTZPCieY+LaUFtNjWW6Xps1UMVRqt3KGOOxNf3B2lZCXMVXBeIKTt+Eol743YpL+Gu6mxWkBR1Guk51llB+MRiqd15rpX+D2jT1vLkDNALuwR7YAQlbNDG2/9M5LuoFuXB5OjiLTFBLyNt703o9UneK5bTyr+yZu6OK/wG0sH1cHp/mYlQeALS8VWUuFcyId0J/bANvgGz4HMwB9ZBKkWavwylcNZQ+6YmSP2dNg21dCpnA/wNNkKHPx5HBOE/kYKjrqTIRecAAAAASUVORK5CYII="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                pass

            def RunScript(self, Geo):
                try:
                    Point, Vector, Curve, Plane, Brep, Surface = (gd[object]() for _ in range(6))
                    re_mes = Message.RE_MES([Geo], ['Geo'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        temp_point, temp_vetor, temp_curve, temp_plane, temp_brep, temp_surface = ([] for _ in range(6))
                        structure_tree = self.Params.Input[0].VolatileData
                        origin_geo = [list(i) for i in structure_tree.Branches][self.RunCount - 1]
                        for geo in origin_geo:
                            if isinstance(geo, (gk.Types.GH_Point)) is True:
                                temp_point.append(geo)
                            elif isinstance(geo, (gk.Types.GH_Vector)) is True:
                                temp_vetor.append(geo)
                            elif isinstance(geo, (gk.Types.GH_Curve)) is True:
                                temp_curve.append(geo)
                            elif isinstance(geo, (gk.Types.GH_Plane)) is True:
                                temp_plane.append(geo)
                            elif isinstance(geo, (gk.Types.GH_Brep)) is True:
                                temp_brep.append(geo)
                            elif isinstance(geo, (gk.Types.GH_Surface)) is True:
                                temp_surface.append(geo)
                        Point, Vector, Curve, Plane, Brep, Surface = temp_point, temp_vetor, temp_curve, temp_plane, temp_brep, temp_surface

                    return Point, Vector, Curve, Plane, Brep, Surface
                finally:
                    self.Message = "GH data type classification "


        # 物体跟随线排序
        class GeoSortedByCurve(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_ObjectSortedByCurve", "A5", """The order of a set of chaotic geometric objects is determined by the direction of the curve """, "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("54118195-e4ce-423a-b238-3c92d46e8759")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.secondary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "Objects that need to be sorted")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Curve()
                self.SetUpParam(p, "Curve", "C", "Guided curve ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Result", "R", "Sorted objects")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Integer()
                self.SetUpParam(p, "Index", "i", " The subscript of the sorted object in the original list")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAANVSURBVEhLY6ARYIHSNAFCxd6mtwNMVWugfOoCXyOl2qNN0f89DRWLoEKUAQ0JoaBoG621GpJCrkAu06QElw89MY7PgWx2sAIKAVO6i8G7TwsK/ic46J7TlhUp2F8X+d9RSy4XKk85cNCWbaoPtr4nJ8rfMinB+WlfnONLoDAnRJaKwMNAqeJQQ/R/OzWJLKgQRYAbiPUhTDAQnZPu+b093PaBRkWb8Pzvn517Hz0SgsqRDDjj7HVOLczy/u+sI98NEkiw01kGCnstXma/hb9+2Ux98+JX35OHLmDVJACYi/jyvUy+XO1J/h9spjZfmJPTdHtl6P9ib7NjIMkZzx9799y4kt11+bQyWDURgNnPWGVRZ6T9O1sN6QqQACcni6menEgekCnXG+N0Z1me739WBgadf//+sU9+fL8LpIYUwJXvZfz71azc/xFWmmehYmCQ7KS37FRr3H83PYV6EH/Gi8dpEx7c8gFLkgLUJAQ9fI2UZ/BzcRlChRhcdeUbTgINz/MwPATi////n2nCneuJoatWMYMVEAkk+TnZgoE0I4QLAZbq0vn7aiP+d0U7PGWQUJAHie3//5/kAo4lwV7nypHG6P8h5mo7oWIMzroKNXtqIv5PTXT9BOSqrPv3z3LOx3e3Jz58aAxRgR+o2mrItEoI8NgB2cxxdjpn99SE/w+z0JgP5LMlOeguPNES+39igssbIN8QFCxTHj+s6L13c3bv7dsqIAPwglAL9eMPp2b+z/Uw/gLkgrI7DxBbAbFbZ5TD5fOdCf+BxcIlIF8FaDjXlEcP+rtu3LAG8hnqgZaBaLzASVuufWqS688wS821UCGBVGf91vUlgf+3lwf/j7FUmwEU4wImR87JD+93tV+9Co90UgAfEHN7GioXTUt2fQ9KKT2xjretLYziIdJA1165wlN/5owIlEsSYPc2UIqfEO9872hTzP9Zqe4/AoyU6kAS2/79M5378f3DSWQUASDA56GnkNsf5/TwUEPU/7npHn/j7XUmAMVFQZILPryNnPTwbkXP/dtdzVevgpMlSSDQRG3WwfoosIsT7HV7gEIKIPEt//5pTn38oKf//s0Ehvp6wpGIC1hrSFsEmanmAJmSEBEI6L9927L5wgVFKHcwAgYGAHtkM9d0Oy2GAAAAAElFTkSuQmCC"
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
                if result_data:
                    return result_data, result_path
                else:
                    return [[]], [tree_path]

            def format_tree(self, result_tree):
                """匹配树路径的代码，利用空树创造与源树路径匹配的树形结构分支"""
                stock_tree = gd[object]()
                for sub_tree in result_tree:
                    fruit, branch = sub_tree
                    for index, item in enumerate(fruit):
                        path = gk.Data.GH_Path(System.Array[int](branch[index]))
                        if hasattr(item, '__iter__'):
                            for sub_index in range(len(item)):
                                stock_tree.Insert(item[sub_index], path, sub_index)
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

            def center_box(self, Box):
                type_str = str(type(Box))
                if 'List[object]' in type_str:
                    bbox = rg.BoundingBox.Empty
                    for brep in Box:
                        bbox.Union(brep.GetBoundingBox(rg.Plane.WorldXY))  # 获取几何边界
                    center = bbox.Center
                else:
                    center = Box.GetBoundingBox(True).Center if "Box" and "Plane" not in type_str else Box.Origin if "Plane" in type_str else Box.Center
                return center

            def sort_points_on_curve(self, points, curve):
                param_list, index_list = [], []
                for pt_index, point in enumerate(points):
                    if point:
                        param_list.append(curve.ClosestPoint(point)[1])
                        index_list.append(pt_index)
                sorted_list = sorted(zip(param_list, index_list))
                if sorted_list:
                    sorted_params, sorted_indexes = zip(*sorted(zip(param_list, index_list)))
                else:
                    sorted_indexes = None
                return sorted_indexes

            def RunScript(self, Geo, Curve):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Result, Index = (gd[object]() for _ in range(2))
                    structure_tree = self.Params.Input[0].VolatileData
                    re_mes = Message.RE_MES([structure_tree, Curve], ['G end', 'C end'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        temp_geo = [list(i) for i in structure_tree.Branches]
                        if self.RunCount - 1 >= len(temp_geo):
                            origin_geo = temp_geo[-1]
                        else:
                            origin_geo = temp_geo[self.RunCount - 1]

                        gh_geo_list = map(lambda x: self._trun_object(x), origin_geo)
                        if gh_geo_list:
                            center_pt_list = ghp.run(GeoCenter().center_box, gh_geo_list)
                            sorted_indexes = self.sort_points_on_curve(center_pt_list, Curve)
                            if sorted_indexes:
                                Result = [origin_geo[_] for _ in sorted_indexes]
                                Index = sorted_indexes

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Result, Index
                finally:
                    self.Message = 'Objects follow the curve in order '


        # 多重向量偏移
        class Skewing(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_Skewing", "A13", """Multivector displacement""", "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3e8b5fff-1d6e-49d1-b6be-f5c5b36bc816")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "A geometric object to be moved ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Reference plane")
                REF_PLANE = rg.Plane.WorldXY
                p.SetPersistentData(gk.Types.GH_Plane(REF_PLANE))
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "XVector", "X", "X-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "YVector", "Y", "Y-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "ZVector", "Z", "Z-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Res_Geo", "G", "The object after displacement")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Transform", "T", "The total number of vectors after the shift ")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPoSURBVEhLrZRtbFNVGMdvlGTGbQIR12Fg0MX15fbcc+5LX1hZ1rpaurXdZd07bLN02K6jq7KZTSEB53R2Ogg4I2OAwkaGI+gHQgwyZaiDaDZgzOAHlY8mJpqYEL8YE3N8bnsWia8h6y85ued5Of/nPOfce7n7IeKRg7UOcwkzs86j4101v6daPWeZnV06fdbUzeEYfb+38Veb/nEDc2eHYl1uwcSzobuzr0bo/OtRur/BfYGFskOHz3pgpj9ML+1rpZf7n6bjyRA1rS/wsvDy8ZINomo3JTTx0Vjgu1qbuZxfu7aIhbPDZvN6i1bgSNS/yFzZxS+XONIFYoHbzJVdlgqMxatvMVd2WSpwvFO9wVzZJaCU2L8YjNCJZM0cc/2NvbWurp5qZxKmD2Y894G+YJVwMF5P+xq9d/bUlLl6YeyuLq2I+2w+bXRW2reMxoLXbwx30KMdwcWoR94Oy1ZkVv8P9ZtMrv6WLbMGRGjAvZlqInNDUfpl6p4B9qcDEfhW2uBjjNGbw3Ha3/TkV0zinylYmVP8crN78uP9bfT2oV3UX4q/D27CM29H/ZffbK+cPhTxfTKys+qj9Givujj5XN0PCwfi6SLwMlx5MVSuMqkMlYqxAR4Pa/M9obK9Z3vqfvn2rS76QW/jb/vqy99IBYTVWuzfGGrzjr/XXT+/wy1uZa4/4YsK+TPddXQ47Js6mVCvfX14F7S8gw40uy/hdTrE0v4TXKTTw+OBjPUXUi2eWe1Hdm2wnWo/NbiohdYyXMnCyyNRZeuZG3oGxCN08WCcjuwMfAPunEx0mRTm5T32Wovn5/N9TT+e6FTvvpPY+hNc4FUvLi5IJpM5qurMZ6mcZrMpFwwG03elEQ6HH3K5XCtgrFJVNb+h4amVdrv9ERbmcsgG3Uagz2gyff6EwTSzrrhkGyEoIMviZwTjUwohNSIWrogimbJapWpRxEcxxu/KsuwgBJ9XFOmkJEm1kP+SSPC8JImzkPM80+c4o9GZLwjCPG+zFeoR0mEszGCMxmC84vV6cwWe346Q5YzT6cwnCIWwIFx3OBw6EDULCF0tLbUiLaZpgfAYz/PdaeElQFyBnU4zk8MInQLflIjxgkTIEYwtzVhAd2RJmrTBJkAgCZuYhg4CUOAW7HwU8o3aWuhyBOaJtNAS4FgNBRYrKsp4ODs92B9CkcNwDIM6nS7XYjI1I8RPGQyGNYqimDwej4EQ4QR0eA7yzgWDrjVw/nmaFnRwDNbvTgvfCxyDKoviRUkkFywWixvsbUQQoloMmc1+QbAMaHMoiiBvAmIpQshGEDttsymnJQk3aXHo+AXoOD3nOI77A3RXUs9p207rAAAAAElFTkSuQmCC"
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                dict_data = None

            def message1(self, msg1):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

            def message2(self, msg2):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

            def message3(self, msg3):
                return self.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

            def judgment_type(self, obj):
                return False if type(obj) is rg.LinearDimension else True

            def normal_move(self, plane, vector_iter):
                origin_vector = [plane.XAxis, plane.YAxis, plane.ZAxis]
                zip_list = list(zip(origin_vector, vector_iter))
                offset_total_vector = map(lambda total: ghc.Amplitude(total[0], total[1]), zip_list)
                offset_vector = reduce(lambda n1, n2: n1 + n2, offset_total_vector)
                return offset_vector

            def RunScript(self, Object, Ref_Plane, XVector, YVector, ZVector):
                try:
                    New_Objcet, Transform = (gd[object]() for _ in range(2))
                    XVector = [0] if len(XVector) == 0 else XVector
                    YVector = [0] if len(YVector) == 0 else YVector
                    ZVector = [0] if len(ZVector) == 0 else ZVector
                    total_offset_x, total_offset_y, total_offset_z = sum(XVector), sum(YVector), sum(ZVector)
                    zip_vector = (total_offset_x, total_offset_y, total_offset_z)
                    Transform = self.normal_move(Ref_Plane, zip_vector)

                    if Object:
                        if isinstance(Object, (rg.Point3d, rg.Point)) is True:
                            Object = rg.Point(Object)
                        elif isinstance(Object, (rg.Line, rg.LineCurve)) is True:
                            Object = Object.ToNurbsCurve()

                        if self.judgment_type(Object) is True:
                            Object.Translate(Transform)
                            New_Objcet = Object
                            return New_Objcet, Transform
                    else:
                        self.message2("Object null！！")
                    return New_Objcet, Transform
                finally:
                    self.Message = "Multivector displacement"


        # 多向量位移
        class SuperSkewing(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_SuperSkewing", "A14", """Multivector displacement（Superposition state）""", "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("3ab5ab26-b1c2-4f66-b5dd-c85f3d20c1b4")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Geo", "G", "A geometric object to be moved ")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Plane()
                self.SetUpParam(p, "Plane", "P", "Reference plane")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "XVector", "X", "X-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "YVector", "Y", "Y-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Number()
                self.SetUpParam(p, "ZVector", "Z", "Z-axis vector")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.list
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_Geometry()
                self.SetUpParam(p, "Res_Geo", "G", "The object after displacement")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Transform", "T", "The total number of vectors after the offset ")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASHSURBVEhLrVVtTFNXGO42E5YBUzKkuCEIGe3t7bnn3NtPqQ3t6EqBlvL9oYAFtKVYOoUFNk1UxsaKAwJjm8jmVDA4HPrDmEVlAzfRbAFRWdyPOX8uWbIlS8z+LEuWs/eW4+YWpxh5kpN73q/nfd9z73mv4lHQ4NB5Ss2aTCauOJ4bbSn+M1LrOMnklUWzyxC51hugp9orfzemP69i6pVBhjI2aeyVkjuzbzXQ+QN+uq/CfpaZVgZNLkPfTKePXthbS6c7t9LRcAnl1ic5mfnh0Ov1iaIormXiE+z5N5wkTfSauJBMPhxw/1Bq1GTz69alMvODgRDCBOMFIginCMGDsLqZ6V+wcSlITnDQX7DIVMsDp9XmQvVHJElKEwmhkGCSEPICz/NxZoSUGGOk0WBzvpRhiCYIuG+y0OUBazRmLAi3RIw/lQjpg07GIEE34XkTIUK/IAineV4oLzJminKCkWDhDRa6PHAc54TKL1mtQgJUmw4JzsORDQLxdij+fdBVqTXakXy9atP0/q30o2bvAgtdHoBI0IniTnmv1WrXQ9UhIC2EYxsQRWEzJAxwvODzGFTGr7vr6Vi4eC4aeB/sKbW1tBVawrB9aknzCEhJWiP0B8tpR6Xz9u5iq60d1q7CrJygy+iSV3OeKXc44Lm60NtEDzV5Fv0O3RYIW7UU/RCUb+RsnTW5sypEqNu+icokcz1++k3kngXyl10NcFfq4DIG6LXeIO2seulbRnF/JK2OyXij2j7++b46enNgBy3Iwj96NuKZD/wF0+825k0NNLi+GNqWfz66GvPPje8s++l6XzCaBD6Gi6+XZHsZ1RLy9OoKeDwj73eXWPecbCv77dZ7LfR0e+Ufe8uz34m4hQTZ9n/oqXOOftJaPl9vF4uY6h/wqcn8idYy2utzTRwNea98N7gDWq6nXdX2CzhFiZjbA4FTlenweHJJ+g8iNY5ZeZBd6W6k8lCDF3W91orzmPnxEMo3ts31bAfyBrrYH6RD29zfgzpmyfqYSI6LW/t2jePXMx1VPx9u9t75OFT0C7zAy06ckRQOh2O8Xks8c1XIMtsqPB5P9F3J8Pl8T9tstlWw1ni93viKipdXm0ymZ5lZEUPSlBsAHWqOu/SiiptJycjcTAhy63TiV3Crj+kJKRaxcFEUyYTBIMElxIfgMh7R6XRmmF1n9HrpKMyyUvDfLxI8L0niLPi8yvgVCrXaEg8Xep43GpPTowNOmIExMQLrTafTGSvw/BaEtCcsFks8QagEZtdVs9msBFKNgNDlrCwDkm0yFxCPwKBsjRLfBZDrodIpJiowQsdANwED8DoMwIMYa6uxgG7rJGncCEUAQRiKmIIO3JDgBlQ+DP5qORa6HIJ9KEp0F6BIgASLOTlWHs4uHeTPIMkgHEO3UqmM1XJcNUL8hEqlSoSfE+dwOFQwsw5Dh5PgN+nx2BLh/ONkLujgQ4jfFSW+F3AMXhh65ySRnIWhZwdZHnR+2QY/hAJB0HbJe0iKwG8MbBEY6xuA7LjRqD8uSbhKtkPHr0HH0b1CoVD8BeonfnDbfo5FAAAAAElFTkSuQmCC"
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

            def match_lists(self, *lists):
                # 获取最长列表的长度
                max_length = max(len(lst) for lst in lists)

                # 对每个列表进行补零，使其长度与最长列表相等
                padded_lists = []
                for lst in lists:
                    padded_list = lst + [0] * (max_length - len(lst))
                    padded_lists.append(padded_list)

                # 创建一个新列表，将所有列表中的对应元素放入其中
                matched_elements = []
                for elements in zip(*padded_lists):
                    matched_elements.append(elements)

                return matched_elements

            def iter_offset(self, origin_object, vector_list, new_object_list):
                origin_object = rg.Point(origin_object) if type(origin_object) is rg.Point3d else origin_object
                origin_vector = vector_list[0]
                copy_object = origin_object.Duplicate()
                copy_object.Translate(origin_vector)
                new_object_list.append(copy_object)
                vector_list.pop(0)
                if len(vector_list) > 0:
                    return self.iter_offset(new_object_list[-1], vector_list, new_object_list)
                else:
                    return new_object_list

            def trun_to_vector(self, tuple_num):
                x, y, z = tuple_num
                origin_x, origin_y, origin_z = [self.pln.XAxis, self.pln.YAxis, self.pln.ZAxis]
                new_x, new_y, new_z = origin_x * x, origin_y * y, origin_z * z
                res_vector = new_x + new_y + new_z
                return res_vector

            def RunScript(self, Geo, Plane, XVector, YVector, ZVector):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Res_Geo, Transform = (gd[object]() for _ in range(2))
                    self.pln = Plane if Plane else rg.Plane.WorldXY

                    self.xvector = [0] if len(XVector) == 0 else XVector
                    self.yvector = [0] if len(YVector) == 0 else YVector
                    self.zvector = [0] if len(ZVector) == 0 else ZVector
                    if Geo:
                        zip_vector = self.match_lists(self.xvector, self.yvector, self.zvector)
                        total_vector = map(self.trun_to_vector, zip_vector)
                        copy_total_vec = copy.copy(total_vector)
                        Res_Geo = self.iter_offset(Geo, total_vector, [])
                        Transform = copy_total_vec
                    else:
                        self.message2('Data on the G end is empty！')
                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc
                    return Res_Geo, Transform
                finally:
                    self.Message = 'Multivector displacement（Superposition state）'


        # 通过点移动物体
        class MoveByPoint(component):
            def __new__(cls):
                instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                                   "RPP_MoveByPoint", "A15", """Move objects between two points""", "Scavenger", "E-Geometry")
                return instance

            def get_ComponentGuid(self):
                return System.Guid("b3a40dca-116a-4bb8-a3fa-19a3add0b528")

            @property
            def Exposure(self):
                return Grasshopper.Kernel.GH_Exposure.tertiary

            def SetUpParam(self, p, name, nickname, description):
                p.Name = name
                p.NickName = nickname
                p.Description = description
                p.Optional = True

            def RegisterInputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Geometry", "G", "Geometric object")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point A", "A", "Initial point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Point()
                self.SetUpParam(p, "Point B", "B", "Move to the point")
                p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
                self.Params.Input.Add(p)

            def RegisterOutputParams(self, pManager):
                p = Grasshopper.Kernel.Parameters.Param_GenericObject()
                self.SetUpParam(p, "Moved", "M", "The object after moving")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Vector()
                self.SetUpParam(p, "Vector", "V", "Moving vector")
                self.Params.Output.Add(p)

                p = Grasshopper.Kernel.Parameters.Param_Transform()
                self.SetUpParam(p, "Transform", "X", "Transform data")
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
                o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPaSURBVEhL7ZRdTFNXHMA7NWbOGF/2suiDmwQs0EILtJcpkEHbIUi/PwBXRjVq0RayWaRQRzchMxNqaaUtYFGLDkaxQ7oidVtAp9UxyseKc3bYTafD7GnPS7b+d3u8ELjSzWw+7pecnNN7f+3vnpP0Uv7nmYneuLTh6ntVJW5VoX5QxTENKN9o+3xf4bHxhrcrfztr3kJoiLCjeZO3RqHoU3L0HlX+h/3K/KYr6qLqr+r3FERv9q8jtOVca9jfNm5QgUuGwdBuDAYULPiycjtM1srhYo1yFldeiHlGo3GV/7Dytq+KD+elmXCpnA0D8iwYU+VAQFcG5w7Ij8e8pzgl3tE9WpENn5Zh0C3OBDc+O0UZYC+mw7v56fcoFEABihtWO8XYz/7dLOiTs5DTX4qBvSQdHHwGHCrI6kAeGYc01+4vy4RefgpYeUnQI0wFCy8RTnISoZbDDFNgSUCSHfHJ6OAqScadJLggokFLfgJYdqZCNZdtRR4ZhzSv3V+eBX1CGrQXUuG8iI5mM3cbHOEuCRjH1sQCn8nToYefCu07qfCxOA1M+INYi2ig5bHakEfGJsk9NRI/8APFCKuQiAJY3ICGyzYjj4xNmmcZKXu2wOlYQLZyoJqHmZBHpl2Sa14I2PAvxQKx2cxNejogWjlgiR3Rm1gr8shYJTmmy/ECHOYcOeCNF+CxTyCPjFWc2zJMCtjx+eRCQOZejcS8sTVdIvZiIOb2LgbocIjD/gh5ZCyinFbyDpYEfloM4DvAAw+8sjQikLwsoOVlx92BcawCg8sKBpwrpoJHQoceAQ06i5NBz2XeWTwiPNQlZEWuvpUBg9I0OLMrBbwKJnQWUaEL/6Npuez3kUfGyX99g1vKKPVIGcc17C0PdDsS5k/vSjW38qhVTVz6q4SGcAkZ1EEZU9fNSTirYb7y0FGw1WfHXja2UtcK6zJe20hocdm898b1Pw8EJwBfJz65tDKbS8uP1s/d+x3T633vzMw0GqJRHnHrb9kksLaFJR22CL5e9uRkUgSCD2oDgWi2er9zzwVXx7GH96E+FLK1PI6uJ5S4rMXHi0+W/8g2YqZohodGjZEwHJme/N54964cFl4vdbeu65si4V/rJ79B42ho6lFsLHyONxqmgo8bv5v90TA9Od8wNfFL7a3AfM21UTg8fhMMd2bBcDv0CAXUHnfpQf9w396Ln/T+21HZ33tGO+IN6fAfr5sJguYL/x9q35AXBZ4H+HFsbA5/e18fmga1d9AnNZloxK3/Tmcw+FLjVGBON/E1KF1OLXH5+dEyc2V9lcddITjRnE5cIqBQ/gLaC4mr9UMEqQAAAABJRU5ErkJggg=="
                return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

            def __init__(self):
                self.diff_vector = None
                self.xform = None

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

            def convert_goo(self, geo):
                if 'List[object]' in str(geo):
                    return True, [_ for _ in geo]
                else:
                    return False, geo

            def is_goo_list(self, turn_data_list):
                turn_bool, new_obj_list, vector, xform = turn_data_list
                if turn_bool:
                    x_object_list = []
                    for obj in new_obj_list:
                        obj.Transform(xform)
                        x_object_list.append(obj)
                    gh_Geos = [gk.GH_Convert.ToGeometricGoo(_) for _ in x_object_list]
                    ghGroup = gk.Types.GH_GeometryGroup()
                    ghGroup.Objects.AddRange(gh_Geos)
                    return ghGroup, vector, xform
                else:
                    obj = new_obj_list
                    obj.Transform(xform)
                    return obj, vector, xform

            def get_xform(self, set_pt):
                a_pt, b_pt = set_pt
                diff_vector = rg.Vector3d(b_pt) - rg.Vector3d(a_pt)
                xform = rg.Transform.Translation(diff_vector)
                return diff_vector, xform

            def object_move(self, tuple_data):
                obj_list, init_pt_list, move_pt_list, origin_path = tuple_data

                init_pt_list = init_pt_list + [init_pt_list[-1]] * (len(obj_list) - len(init_pt_list)) if len(obj_list) > len(init_pt_list) else init_pt_list
                move_pt_list = move_pt_list + [move_pt_list[-1]] * (len(obj_list) - len(move_pt_list)) if len(obj_list) > len(move_pt_list) else move_pt_list

                dif_vector, xform = zip(*map(self.get_xform, zip(init_pt_list, move_pt_list)))

                bool_reslut, turn_to_object_list = zip(*map(self.convert_goo, obj_list))
                new_tuple_data = zip(bool_reslut, turn_to_object_list, dif_vector, xform)
                group_obj, vector_list, xform_list = zip(*map(self.is_goo_list, new_tuple_data))

                ungroup_data = map(lambda x: self.split_tree(x, origin_path), [group_obj, vector_list, xform_list])
                Rhino.RhinoApp.Wait()
                return ungroup_data

            def RunScript(self, Geometry, Point_A, Point_B):
                try:
                    sc.doc = Rhino.RhinoDoc.ActiveDoc
                    Moved, Vector, Transform = (gd[object]() for _ in range(3))
                    trunk_geo, trunk_path = self.Branch_Route(Geometry)
                    init_pt_trunk, init_trunk_path = self.Branch_Route(Point_A)
                    move_pt_trunk, move_trunk_path = self.Branch_Route(Point_B)

                    trunk_path_list = [len(trunk_path), len(init_trunk_path), len(move_trunk_path)]
                    target_trunk_path = [trunk_path, init_trunk_path, move_trunk_path][trunk_path_list.index(max(trunk_path_list))]

                    g_len, i_len, m_len, target_len = len(trunk_geo), len(init_pt_trunk), len(move_pt_trunk), len(target_trunk_path)

                    re_mes = Message.RE_MES([Geometry, Point_A, Point_B], ['G', 'A', 'B'])
                    if len(re_mes) > 0:
                        for mes_i in re_mes:
                            Message.message2(self, mes_i)
                    else:
                        trunk_geo = trunk_geo + [trunk_geo[-1]] * (target_len - g_len) if target_len > g_len else trunk_geo
                        init_pt_trunk = init_pt_trunk + [init_pt_trunk[-1]] * (target_len - i_len) if target_len > i_len else init_pt_trunk
                        move_pt_trunk = move_pt_trunk + [move_pt_trunk[-1]] * (target_len - m_len) if target_len > m_len else move_pt_trunk

                        zip_list = zip(trunk_geo, init_pt_trunk, move_pt_trunk, target_trunk_path)
                        iter_ungroup_data = zip(*ghp.run(self.object_move, zip_list))
                        Moved, Vector, Transform = ghp.run(lambda single_tree: self.format_tree(single_tree), iter_ungroup_data)

                    sc.doc.Views.Redraw()
                    ghdoc = GhPython.DocReplacement.GrasshopperDocument()
                    sc.doc = ghdoc

                    return Moved, Vector, Transform
                finally:
                    self.Message = 'Moved By Pt'

    else:
        pass
except:
    pass

import GhPython
import System
