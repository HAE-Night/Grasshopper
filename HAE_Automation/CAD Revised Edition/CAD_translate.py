# -*-coding:utf-8 -*-

"""
# File     : CAD_case.py
# Time     ：2023/1/31 10:10
# Author   ：ZIYE Night
# version  ：python 3.10
# py文件说明：
    CAD文件 TEXT翻译
"""
import copy
import http.client
import hashlib
import urllib
import random
import json
import tkinter
import tkinter.messagebox
from copy import copy
from tkinter import *

import win32com.client as win32

global blocknames
blocknames = {'file_path': ""}


def baiduTranslate(translate_text, appid, secretKey, flag=0):
    """
    :param translate_text: 待翻译的句子，len(q)<2000
    :param flag: 1:原句子翻译成英文；0:原句子翻译成中文
    :return: 返回翻译结果。
    For example:
    q=我今天好开心啊！
    result = {'from': 'zh', 'to': 'en', 'trans_result': [{'src': '我今天好开心啊！', 'dst': "I'm so happy today!"}]}
    """

    # appid = '20221102001431296'  # 填写你的appid
    # secretKey = 'qh7tyxi9wo4PW5Y19clo'  # 填写你的密钥
    httpClient = None
    myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'  # 通用翻译API HTTP地址
    fromLang = 'auto'  # 原文语种

    if flag:
        toLang = 'auto'  # 译文语种
    else:
        toLang = 'zh'  # 译文语种

    salt = random.randint(3276, 65536)
    sign = appid + translate_text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # return result
        return result['trans_result'][0]['dst']

    except Exception as e:
        tkinter.messagebox.showerror('错误', '请输入正确的百度API和密钥')
        print(e)
    finally:
        if httpClient:
            httpClient.close()


class CAD_Link(object):
    # Autocad 2022的ProgramID
    ProgramID = "AutoCAD.Application.23.1"
    # 获取CAD程序
    Acadapp = win32.Dispatch(ProgramID)
    # 指定当前CAD页面
    doc = Acadapp.ActiveDocument
    AcadA = doc.Application


class CAD_operation(object):
    def __init__(self):
        pass

    # 存入数据
    def Selection_block(self, appid, secretKey):
        # 新建选择集
        try:
            CAD_Link.doc.SelectionSets.Item("S1").Delete()
        except:
            print("删除选择失败")

        slt = CAD_Link.doc.SelectionSets.Add("S1")
        # CAD软件中框选拾取图元并添加到选择集中
        CAD_Link.doc.Utility.Prompt("选择目标块-方便程序获取块的名称.")
        print('报错前')
        slt.SelectOnScreen()
        print ('bacuo')
        for slt_ in slt:
            if slt_.objectname in ['AcDbMText', 'AcDbText']:
                Value = copy(slt_.TextString)
                # print('翻以前内容:{},翻译后内容:{}'.format(Value, baiduTranslate(Value, appid, secretKey)))
                slt_.TextString = baiduTranslate(Value, appid, secretKey)


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 窗口方法
    def Cad_text(self):
        appid = self.init_data_entry_A.get()
        secretKey = self.init_data_entry_B.get()
        print(appid, secretKey)
        if appid == '' or secretKey == '':
            tkinter.messagebox.showerror('错误', '请输入百度API和密钥')
            return
        CAD_operation().Selection_block(appid, secretKey)

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("CAD内容翻译")  # 窗口名
        self.init_window_name.geometry('320x160+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # 标签d
        self.init_data_label_A = Label(self.init_window_name, text="百度APPID: ", bg="cyan", anchor='e', height=1,
                                       width=20)
        self.init_data_label_A.grid(row=1, column=0)
        self.init_data_label_B = Label(self.init_window_name, text="密钥", bg="cyan", anchor='e', height=1, width=20)
        self.init_data_label_B.grid(row=2, column=0)
        # 按钮
        self.init_data_botton1 = Button(self.init_window_name, text="选取翻译内容并翻译", height=2, justify=CENTER,
                                        command=self.Cad_text).grid(row=3, column=0)

        # 文本框：
        # self.init_data_entry_API =
        self.init_data_entry_A = Entry(self.init_window_name, bd=3, width=23)  # 百度APPID
        self.init_data_entry_A.grid(row=1, column=1)
        self.init_data_entry_B = Entry(self.init_window_name, bd=3, width=23)  # 密钥
        self.init_data_entry_B.grid(row=2, column=1)


if __name__ == '__main__':
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    # CAD = CAD_operation()
    # CAD.Selection_block()  # 选择内容操作
