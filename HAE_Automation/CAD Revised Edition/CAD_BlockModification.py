# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Copy
# @Time : 2023/2/17 10:24
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# File     : CAD_Win_Text.py
# Time     ：2023/2/1 9:35
# Author   ：ZIYE Night
# version  ：python 3.10
# py文件说明：
        对当前CAD文件 进行文本核对以及修改
"""
import time
from copy import copy
import tkinter as tk

from tkinter import *
from tkinter import messagebox

import win32com.client as win32


class CAD_Link(object):
    # Autocad 2020的ProgramID
    ProgramID = "AutoCAD.Application.23.1"
    # 获取CAD程序
    Acadapp = win32.Dispatch(ProgramID)
    # 指定当前活动文档
    doc = Acadapp.ActiveDocument
    AcadA = doc.Application


blocknames = {}


class CAD_BlockText(object):
    def __int__(self):
        ...

    def Selection_block(self):
        # 新建选择集
        try:
            CAD_Link.doc.SelectionSets.Item("S1").Delete()
        except:
            print("Delete selection failed")

        slt = CAD_Link.doc.SelectionSets.Add("S1")
        # CAD软件中框选拾取图元并添加到选择集中
        CAD_Link.doc.Utility.Prompt("选择目标块-方便程序获取块的名称.")
        slt.SelectOnScreen()

        for slt_ in slt:
            if slt_.objectname == "AcDbBlockReference":
                name = slt_.EffectiveName

                """修改字典错误命名方式"""
                blocknames[name] = name
            else:
                continue


class CAD_TKGUI(object):
    def __init__(self, init_window_name):
        """删除定义全局变量"""
        self.init_window_name = init_window_name

    def TKset_init(self):
        self.init_window_name.title("CAD文字修改_v1.2")  # 窗口名
        self.init_window_name.geometry('480x320+10+10')  # 窗口大小以及定位点

        # 标签
        # self.init_data_label1 = Label(self.init_window_name, text="选择需要改动文本的图层").grid(row=0, column=1, sticky="w")
        self.init_data_label_A = Label(self.init_window_name, text="楼层编号: ", bg="cyan", anchor='e', height=1, width=20)
        self.init_data_label_A.grid(row=1, column=0)
        self.init_data_label_B = Label(self.init_window_name, text="方向编号: ", bg="cyan", anchor='e', height=1, width=20)
        self.init_data_label_B.grid(row=2, column=0)

        self.init_data_label_C = Label(self.init_window_name, text="图纸标题: ", bg="cyan", anchor='e', height=1, width=20)
        self.init_data_label_C.grid(row=3, column=0)

        # 按钮
        self.init_data_botton1 = Button(self.init_window_name, text="选择需要改动文本的图层", height=2, justify=CENTER, command=CAD_BlockText().Selection_block). \
            grid(row=0, column=0)
        self.init_data_botton2 = Button(self.init_window_name, text="开始核查", height=2, justify=CENTER, command=self.Cad_text). \
            grid(row=4, column=3)

        # 文本框：
        self.init_data_entry_A = Entry(self.init_window_name, bd=3, width=23)  # 楼层
        self.init_data_entry_A.grid(row=1, column=1)
        self.init_data_entry_B = Entry(self.init_window_name, bd=3, width=23)  # 方向
        self.init_data_entry_B.grid(row=2, column=1)

        self.init_data_entry_C = Entry(self.init_window_name, bd=3, width=23)  # 标题
        self.init_data_entry_C.grid(row=3, column=1)

        addr = tk.StringVar(value='不用填写，选择块后显示当前块名')
        self.set_data_entry_A = Entry(self.init_window_name, bd=2, width=26, textvariable=addr)  # 图块
        self.set_data_entry_A.grid(row=0, column=1)

        self.log_data_Text = Text(self.init_window_name, width=66, height=12)  # 日志框
        self.log_data_Text.grid(row=8, column=0, columnspan=10)

        # 窗口方法

    def Cad_text(self):
        if blocknames:
            flooy = self.init_data_entry_A.get()
            direction = self.init_data_entry_B.get()
            title = self.init_data_entry_C.get()
            self.set_data_entry_A.delete(0, END)
            self.set_data_entry_A.insert(0, str(blocknames))
            """块对应方法"""
            self.cad_block([[flooy, direction], title])
        else:
            self.Check('请先选取指定图块，在进行核查')

    def cad_block(self, floor):
        Nameblock = blocknames
        # 新建选择集
        try:
            CAD_Link.doc.SelectionSets.Item("SS1").Delete()
        except:
            print("Delete selection failed")

        slt = CAD_Link.doc.SelectionSets.Add("SS1")
        # CAD软件中框选拾取图元并添加到选择集中
        CAD_Link.doc.Utility.Prompt("选取当前楼层的所有图块.")
        slt.SelectOnScreen()

        """主方法修改"""
        for i in slt:
            if i.objectname == "AcDbBlockReference" and i.EffectiveName in Nameblock:  # i.EffectiveName == 'TGA.TTLB.PROJECTDATA'
                b = i.GetAttributes()  # 获取属性
                NibsText = [i for i in b if 'NIB' in i.TextString]
                sum = 0
                for NT_ in NibsText:
                    fl = copy(floor)  # 直接赋值 会导致参数递增
                    te = NT_.TextString
                    sum += 1
                    if 'LVL' in te:
                        """数据分流---->Data_1"""
                        no_change = te.split('-')[0: -1]
                        temp_str = ')'.join([fl[-1], te.split('-')[-1].split(')')[-1]])
                        no_change.append(temp_str)
                        NT_newname_1 = '-'.join(no_change)
                        NT_.TextString = NT_newname_1
                        self.write_log_to_Text(f'第{sum}个进行了修改，{te} -->> {NT_newname_1}')
                    else:
                        """数据分流---->Data_2"""
                        if te.split('-')[0:2] == fl[0]:
                            self.write_log_to_Text('该组信息正确，无需更改')
                            continue
                        else:
                            new_no = ''.join([te.split('-')[0][0], fl[-1]])
                            temp_list = te.split('-')[1:]
                            temp_list.insert(0, new_no)
                            NT_newname_2 = '-'.join(temp_list)
                            NT_.TextString = NT_newname_2
                            self.write_log_to_Text(f'第{sum}个进行了修改，{te} -->> {NT_newname_2}')

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        LOG_LINE_NUM = 0
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 20:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)

    # 提示窗口
    def Check(self, str_):
        Bool_ = messagebox.showwarning(title='警告', message=str_)


if __name__ == '__main__':
    tsy = '程序开始前，取消CAD中的选取，选否程序停止运行'
    Bool_ = messagebox.askyesno(title='提示', message=tsy)
    if Bool_:
        init_window = tk.Tk()
        Windows = CAD_TKGUI(init_window)
        # 设置根窗口默认属性
        Windows.TKset_init()

        init_window.mainloop()
