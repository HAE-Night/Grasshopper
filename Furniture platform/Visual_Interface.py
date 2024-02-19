#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： Vmn
# datetime： 2023/9/20 13:13
# ide： PyCharm
import base64
import os
import tkinter as tk
from tkinter import filedialog, END, ttk
from tkinter import messagebox
from Excel_operation import ExcelReader
from Excel_operation import ExcelCopier
from Database_Manipulation import Database_Manipulation
from Address_Function import Address_Selection


def execute_method(Label, sheet_var, sheet_var1):
    #   获取地址Label
    address_pass = Label.cget("text")
    sheet_name = sheet_var.get()
    price_strategy = sheet_var1.get()
    # 在这里执行选中的方法
    if address_pass != "未选择" and sheet_name[0] != "未选择":
        excel_file = ExcelCopier(address_pass,
                                 sheet_name)
        database_Furniture = Database_Manipulation()

        start_index = database_Furniture.Select_Max_ID()

        List_result = excel_file.Get_Excel_Info()
        list_img_index = excel_file.Download_Excel_Image(r"Photos/",
                                                         start_index=start_index)
        address_pass_select = Address_Selection(address_pass)
        file_name = address_pass_select.get_file_name()
        inquiry_code = file_name
        database_Furniture.Insert_ALLData(List_result, start_index, list_img_index, price_strategy=price_strategy,
                                          inquiry_code=inquiry_code)
        messagebox.showinfo("Success", "表格数据添加成功")

    else:
        messagebox.showerror("Error", "请选择文件")


# 地址框（带选择功能）
def open_address_selection(Label, method_dropdown):
    selected_address = filedialog.askopenfilename(filetypes=[("Excel文件", "*.xlsx"), ("All files", "*.*")])
    print(selected_address)
    if selected_address is not None and selected_address != "":
        #   将Label里面的文字清空,并将selected_address设置为Label显示值
        Label.config(text=selected_address)

        #   将选择的excel里面的sheets名设置到下拉框method_dropdown下拉显示
        excel_reader = ExcelReader(selected_address)
        list_sheet = excel_reader.get_sheet_names()
        sheet_name = list_sheet
        method_dropdown.set(sheet_name[0])  # 设置默认选项
        method_dropdown.config(values=sheet_name)

        # 关闭一个已经打开的Excel文件的读取器对象
        excel_reader.close()
    else:
        messagebox.showinfo("Info", "The incoming folder is empty")


def setup_gui():
    root = tk.Tk()
    root.title('Filtrate PDF')

    # 图标二进制
    ico = """
    """
    # 生成临时图标文件myico.ico
    with open('my_ico.ico', 'wb') as f:
        f.write(base64.b64decode(ico))
    root.iconbitmap('my_ico.ico')
    if os.path.isfile('my_ico.ico'):
        os.remove('my_ico.ico')

    # 定义了一个窗口的宽度和高度
    window_width = root.winfo_screenwidth() // 2
    window_height = root.winfo_screenheight() // 2
    root.geometry(f'1100x220')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1000) // 2
    y = (screen_height - window_height - 30) // 2
    root.geometry(f'+{x}+{y}')

    # 地址位置选择显示
    address_label = tk.Label(root, text="未选择")
    address_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="ew")  # 使用grid布局，设置间距和粘性方向

    # 选择地址
    select_address_button = tk.Button(root, text="select address", command=lambda: open_address_selection(
        address_label, method_dropdown
    ))
    select_address_button.grid(row=0, column=4, padx=10, pady=(20, 0), sticky="ew")  # 使用grid布局，设置间距和粘性方向

    execute_button = tk.Button(text="Execute",
                               command=lambda: execute_method(Label=address_label, sheet_var=sheet_var,
                                                              sheet_var1=sheet_var1
                                                              ))

    execute_button.grid(row=0, column=5, columnspan=2, padx=10, pady=(20, 0), sticky="ew")  # 右边距20像素

    # sheets选择下拉框
    sheet_options = ['未选择']
    sheet_var = tk.StringVar()
    sheet_var.set(sheet_options[0])  # 设置默认选项
    method_dropdown = ttk.Combobox(root, textvariable=sheet_var, values=sheet_options, state="readonly")
    method_dropdown.grid(row=1, column=0, columnspan=2, padx=30, pady=(20, 0), sticky="ew")  # 右边距20像素

    # 选择价格区间""
    sheet_options1 = ['MID', "LOWER", "HIGH"]
    sheet_var1 = tk.StringVar()
    sheet_var1.set(sheet_options1[0])  # 设置默认选项
    method_dropdown1 = ttk.Combobox(root, textvariable=sheet_var1, values=sheet_options1, state="readonly")
    method_dropdown1.grid(row=1, column=2, columnspan=2, padx=30, pady=(20, 0), sticky="ew")  # 右边距20像素

    # 设置布局权重，让部件随着窗口大小变化而变化
    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=2)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.mainloop()


setup_gui()
