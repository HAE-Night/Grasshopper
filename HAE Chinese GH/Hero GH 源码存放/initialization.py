# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : __init__
# @Time : 2022/11/17 10:31

import Grasshopper, GhPython
import clr
import os
import time
import base64
import binascii

clr.AddReference("System.Management")
import System.Management

designer_database = ['Niko', 'Nancy', 'Landon', 'Levi', 'Jiang', 'Claire', 'Bella', 'Lauren', 'Night', 'Mary', 'John', 'kiki', 'Radish', 'Juhair', 'Mohamed Shoman', 'Ivan', 'Hasir', 'Hari', 'Nikki',
                     'Zubair', 'Riyas', 'Najeeb', 'Roberto', 'Mohamed Gomaa', 'Leo', 'James', 'Mia', 'Bynn', 'Vince', 'Noora', 'Xin', 'Jim', 'Lydia', 'Jim']
Mac_Array = []


class message:
    def message1(self, component, msg1):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

    def message2(self, component, msg2):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

    def message3(self, component, msg3):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

    # 参数报错警告
    def RE_MES(self, parameter, para_name):
        remes = []
        for i_parameter in range(len(parameter)):
            if not parameter[i_parameter] or 'empty tree' == str(parameter[i_parameter]):
                remes.append("Think twice before you leap, lacking necessary parameters:{}!".format(para_name[i_parameter]))
        return remes


def _get_macaddress(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    Mac_Array.append(ipconfig_list['MACAddress'])

def _get_cpu(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    return ipconfig_list['ProcessorId']

def decryption():
    select_1 = "SELECT * FROM WIN32_NetworkAdapterConfiguration"
    select_2 = "SELECT * FROM Win32_Processor"
    arrInfo = System.Management.ManagementObjectSearcher(select_1)
    cpuInfo = System.Management.ManagementObjectSearcher(select_2)
    prop_list = [strInfo_1.Properties for strInfo_1 in arrInfo.Get()]
    cpu_info_list = [strInfo_2.Properties for strInfo_2 in cpuInfo.Get()]

    map(_get_macaddress, prop_list)
    Mac_Address = filter(None, Mac_Array)
    cpu_ser = map(_get_cpu, cpu_info_list)

    origin_data_list = []
    now_time = int(time.time())
    env_path = os.environ['userprofile'] + r'\AppData\Roaming\Grasshopper\Libraries'


    file_list = []
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
    filter_list = []
    dir_list = []
    for file_index, file_data in enumerate(file_str_list):
        if "-KEY" in file_data:
            dir_list.append(file_list[file_index])
    with open(dir_list[0], 'r') as f:
        data = f.read()
        origin_data_list = data
#    for name in designer_database:
#        try:
#            with open(os.environ['userprofile'] + r'\AppData\Roaming\Grasshopper\Libraries\{0}-KEY.licence'.format(name), 'r') as f:
#                data = f.read()
#                origin_data_list.append(data)
#        except:
#            pass
#    if len(origin_data_list) == 1:
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
    if cpu_ser[0] in origin_list and origin_list[1] in Mac_Address and int(origin_list[-1]) > now_time:
        return True
    else:
        return False
#    print(origin_list[1] in Mac_Address)
#    if origin_list[1] in Mac_Address and int(origin_list[-1]) > now_time:
#        return True
#    else:
#        return False
#    elif len(origin_data_list) > 1 or len(origin_data_list) == 0:
#        return False


Result = decryption()
