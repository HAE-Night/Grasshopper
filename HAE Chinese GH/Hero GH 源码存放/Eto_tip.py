# -*- ecoding: utf-8 -*-
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : Eto_tip
# @Time : 2022/8/3 11:32

import initialization

import Rhino
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import os

import time
import getpass
import base64



Result = initialization.Result
file_list, key_list = ([] for _ in range(2))

env_path = os.environ['userprofile'] + r'\AppData\Roaming\Grasshopper\Libraries'
def recursive_listdir(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_list.append(file_path)
        elif os.path.isdir(file_path):
            recursive_listdir(file_path)

recursive_listdir(env_path)

file_str_list = [_.split("\\")[-1] for _ in file_list]
for file_index, file_data in enumerate(file_str_list):
    if "-KEY" in file_data:
        key_list.append(file_list[file_index])


def eto_decryption():
    with open(key_list[0], 'r') as f:
        data = f.read()
        origin_data_list = data.split("\n")[0]
    data_list = [i for i in origin_data_list]
    re_reversed_list1 = data_list[0:10]
    re_reversed_list1.reverse()
    re_reversed_list2 = data_list[10:]
    re_reversed_list2.reverse()
    result_list = re_reversed_list1 + re_reversed_list2
    result = ''.join(result_list)
    try:
        origin_data = str(base64.b64decode(result))
        origin_list = origin_data.split('-')
    except TypeError:
        return False

    now_time = int(time.time())
    over_second = int(origin_list[-2]) - now_time
    time_Array = time.localtime(int(origin_list[-2]))
    Style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
    if over_second > 0:
        over_day = int(round((over_second / 60 / 60 / 24), 0))
        text = 'Scavenger plugin will expire in {}!!!'.format(Style_time) if over_day <= 10 else None
    else:
        text = 'Scavenger plugin has expired!!!'
    return text

if Result:
    result_text = eto_decryption()

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
