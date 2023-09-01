# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Main
# @Time : 2022/11/5 17:09

import clr

clr.CompileModules(
    "HAE(3.16).ghpy", "initialization.py", "Eto_tips.py", "Curve_group.py", "Surface_group.py", "Plane_group.py", "Vector_group.py", "Data_group.py",
    "Brep_group.py", "Geometry_group.py", "Object_group.py", "Others_group.py", "Math_group.py", "Big_plugin_group.py"
)