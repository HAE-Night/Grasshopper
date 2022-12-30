# -*- ecoding: utf-8 -*-
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Eto_tip
# @Time : 2022/8/3 11:32

import init__

import Rhino
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms

import time
import getpass
import base64

def decryption():
    designer_names = init__.designer_database
    origin_data_list = []
    now_time = int(time.time())
    for name in designer_names:
        try:
            with open(r'C:\Users\%s\AppData\Roaming\Grasshopper\Libraries\{0}-KEY.licence'.format(name) % getpass.getuser(), 'r') as f:
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
        origin_list = None
        try:
            origin_data = str(base64.b64decode(result))
            origin_list = origin_data.split('-')
        except TypeError:
            pass
        over_second = int(origin_list[2]) - now_time
        time_Array = time.localtime(int(origin_list[2]))
        Style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
        if over_second > 0:
            over_day = int(round((over_second / 60 / 60 / 24), 0))
            text = 'Your component will expire on {}！'.format(Style_time) if over_day <= 10 else None
        else:
            text = 'Your component has expired！'
        return text


result_text = decryption()

if result_text is not None:
    class Tip(forms.Dialog[bool]):
        def __init__(self):
            self.Title = 'Important Notice！'
            self.Padding = drawing.Padding(10)
            self.Resizable = False

            self.m_label = forms.Label(Text=result_text)

            self.DefaultButton = forms.Button(Text="Got it")
            self.DefaultButton.Click += self.OnOKButtonClick

            layout = forms.DynamicLayout()
            layout.Spacing = drawing.Size(2, 10)
            layout.AddRow(self.m_label)
            layout.AddRow(self.DefaultButton)

            self.Content = layout

        def OnOKButtonClick(self, sender, e):
            self.Close(False)


    def Run_Eto():
        dialog = Tip()
        dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


    Run_Eto()
