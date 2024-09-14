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
from itertools import chain
from urllib import urlopen
import datetime
import System

import rhinoscriptsyntax as rs
import Grasshopper.Kernel as gk
import ghpythonlib.treehelpers as ght
import Rhino.Geometry as rg
import math
from Grasshopper import DataTree as gd
from _winreg import CreateKey, HKEY_CURRENT_USER, CloseKey, OpenKey, QueryValueEx, SetValueEx, REG_SZ

clr.AddReference("System.Management")
import System.Management

# 定义全局变量
Mac_Array = []


class message:
    def message1(self, component, msg1):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error, msg1)

    def message2(self, component, msg2):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg2)

    def message3(self, component, msg3):
        return component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark, msg3)

    def mes_box(self, info, button, title):
        return rs.MessageBox(info, button, title)

    # 参数报错警告
    def RE_MES(self, parameter, para_name):
        remes = []
        for i_parameter in range(len(parameter)):
            if not parameter[i_parameter] or 'empty tree' == str(parameter[i_parameter]):
                remes.append("Think twice before you leap, lacking necessary parameters:{}!".format(para_name[i_parameter]))
        return remes


class TreeOperation:
    def Branch_Route(self, Tree):
        """分解Tree操作，树形以及多进程框架代码"""
        Tree_list = [list(_) for _ in Tree.Branches]
        Tree_Path = [_ for _ in Tree.Paths]
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


class HAE_Text(gk.Types.GH_GeometricGoo[rg.TextEntity], gk.IGH_BakeAwareData, gk.IGH_PreviewData):
    """自定义Text方法"""

    def __init__(self, Text):
        self.Text = Text

    def IsValid(self):
        return self.Text is not None and self.Text != ""

    def TypeName(self):
        return "HAE-Text"

    def TypeDescription(self):
        return "HAE-Text"

    def BoundingBox(self):
        if self.Text is None:
            return rg.BoundingBox.Empty
        return self.Text.GetBoundingBox(True)

    def Duplicate(self):
        if self.Text is not None:
            return HAE_Text(self.Text.Duplicate())
        return None

    def DuplicateGeometry(self):
        if self.Text is not None:
            return HAE_Text(self.Text.Duplicate())
        return None

    def Transform(self, xform):
        if self.Text is not None:
            self.Text.Transform(xform)
            return HAE_Text(self.Text)
        return None

    def get_Boundingbox(self):
        if self.Text is None:
            return rg.BoundingBox.Empty
        return self.Text.GetBoundingBox(True)

    def CastTo(self, T, Q):
        return False, self.Text

    def ToString(self):
        if self.Text is None:
            return None
        return "Text:{}".format(self.Text.Text)

    def DrawViewportWires(self, args):
        if self.Text is None:
            return None
        args.Pipeline.DrawAnnotation(self.Text, args.Color)

    def DrawViewportMeshes(self, args):
        pass

    def get_ClippingBox(self):
        if self.Text is None:
            return rg.BoundingBox.Empty
        return self.Text.GetBoundingBox(True)

    def Write(self, writer):
        writer.SetString("HAETextData", self.Text)
        return True

    def Read(self, reader):
        self.Text = reader.GetString("HAETextData")
        return True

    def BakeGeometry(self, doc, att, id):
        id = System.Guid.Empty
        if att is None:
            att = doc.CreateDefaultAttributes()

        id = doc.Objects.AddText(self.Text, att)

        return True, id

    @staticmethod
    def __implicit__(Text):
        return HAE_Text(Text)


class HAE_Leader(gk.Types.GH_GeometricGoo[rg.Leader], gk.IGH_BakeAwareData, gk.IGH_PreviewData):
    """自定义Leader方法"""

    def __init__(self, Leader):
        self.Leader = Leader

    def IsValid(self):
        return self.Leader is not None and self.Leader != ""

    def TypeName(self):
        return "HAE-Leader"

    def TypeDescription(self):
        return "HAE-Leader"

    def BoundingBox(self):
        if self.Leader is None:
            return rg.BoundingBox.Empty
        return self.Leader.GetBoundingBox(True)

    def Duplicate(self):
        if self.Leader is not None:
            return HAE_Leader(self.Leader.Duplicate())
        return None

    def DuplicateGeometry(self):
        if self.Leader is not None:
            return HAE_Leader(self.Leader.Duplicate())
        return None

    def Transform(self, xform):
        if self.Leader is not None:
            self.Leader.Transform(xform)
            return HAE_Leader(self.Leader)
        return None

    def get_Boundingbox(self):
        if self.Leader is None:
            return rg.BoundingBox.Empty
        return self.Leader.GetBoundingBox(True)

    def CastTo(self, T, Q):
        return False, self.Leader

    def ToString(self):
        if self.Leader is None:
            return None
        return "Leader:{}".format(self.Leader.Text)

    def DrawViewportWires(self, args):
        if self.Leader is None:
            return None
        args.Pipeline.DrawAnnotation(self.Leader, args.Color)

    def DrawViewportMeshes(self, args):
        pass

    def get_ClippingBox(self):
        if self.Leader is None:
            return rg.BoundingBox.Empty
        return self.Leader.GetBoundingBox(True)

    def Write(self, writer):
        writer.SetString("HAELeaderData", self.Leader)
        return True

    def Read(self, reader):
        self.Leader = reader.GetString("HAELeaderData")
        return True

    def BakeGeometry(self, doc, att, id):
        id = System.Guid.Empty
        if att is None:
            att = doc.CreateDefaultAttributes()

        id = doc.Objects.Add(self.Leader, att)

        return True, id

    @staticmethod
    def __implicit__(Leader):
        return HAE_Leader(Leader)


class HAE_AngularDim(gk.Types.GH_GeometricGoo[rg.AngularDimension], gk.IGH_BakeAwareData, gk.IGH_PreviewData):
    """自定义Angular方法"""

    def __init__(self, Dim):
        self.Dim = Dim

    def IsValid(self):
        return self.Dim is not None and self.Dim != ""

    def TypeName(self):
        return "HAE-Dim"

    def TypeDescription(self):
        return "HAE-Dim"

    def BoundingBox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def Duplicate(self):
        if self.Dim is not None:
            return HAE_AngularDim(self.Dim.Duplicate())
        return None

    def DuplicateGeometry(self):
        if self.Dim is not None:
            return HAE_AngularDim(self.Dim.Duplicate())
        return None

    def Transform(self, xform):
        if self.Dim is not None:
            self.Dim.Transform(xform)
            return HAE_AngularDim(self.Dim)
        return None

    def get_Boundingbox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def CastTo(self, T, Q):
        return False, self.Dim

    def ToString(self):
        if self.Dim is None:
            return None
        text = self.Dim.PlainUserText
        if text == '<>' or text is None:
            text = round(math.degrees(self.Dim.NumericValue), 2)
        return "Dim:{}".format(text)

    def DrawViewportWires(self, args):
        if self.Dim is None:
            return None
        args.Pipeline.DrawAnnotation(self.Dim, args.Color)

    def DrawViewportMeshes(self, args):
        pass

    def get_ClippingBox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def Write(self, writer):
        writer.SetString("HAEDimData", self.Dim)
        return True

    def Read(self, reader):
        self.Dim = reader.GetString("HAEDimData")
        return True

    def BakeGeometry(self, doc, att, id):
        id = System.Guid.Empty
        if att is None:
            att = doc.CreateDefaultAttributes()

        id = doc.Objects.Add(self.Dim, att)

        return True, id

    @staticmethod
    def __implicit__(Dim):
        return HAE_AngularDim(Dim)


class HAE_LinearDim(gk.Types.GH_GeometricGoo[rg.LinearDimension], gk.IGH_BakeAwareData, gk.IGH_PreviewData):
    """自定义Linear方法"""

    def __init__(self, Dim):
        self.Dim = Dim

    def IsValid(self):
        return self.Dim is not None and self.Dim != ""

    def TypeName(self):
        return "HAE-Dim"

    def TypeDescription(self):
        return "HAE-Dim"

    def BoundingBox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def Duplicate(self):
        if self.Dim is not None:
            return HAE_LinearDim(self.Dim.Duplicate())
        return None

    def DuplicateGeometry(self):
        if self.Dim is not None:
            return HAE_LinearDim(self.Dim.Duplicate())
        return None

    def Transform(self, xform):
        if self.Dim is not None:
            self.Dim.Transform(xform)
            return HAE_LinearDim(self.Dim)
        return None

    def get_Boundingbox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def CastTo(self, T, Q):
        return False, self.Dim

    def ToString(self):
        if self.Dim is None:
            return None
        text = self.Dim.PlainUserText
        if text == '<>' or text is None:
            text = round(self.Dim.NumericValue, 2)
        return "Dim:{}".format(text)

    def DrawViewportWires(self, args):
        if self.Dim is None:
            return None
        args.Pipeline.DrawAnnotation(self.Dim, args.Color)

    def DrawViewportMeshes(self, args):
        pass

    def get_ClippingBox(self):
        if self.Dim is None:
            return rg.BoundingBox.Empty
        return self.Dim.GetBoundingBox(True)

    def Write(self, writer):
        writer.SetString("HAEDimData", self.Dim)
        return True

    def Read(self, reader):
        self.Dim = reader.GetString("HAEDimData")
        return True

    def BakeGeometry(self, doc, att, id):
        id = System.Guid.Empty
        if att is None:
            att = doc.CreateDefaultAttributes()

        id = doc.Objects.Add(self.Dim, att)

        return True, id

    @staticmethod
    def __implicit__(Dim):
        return HAE_LinearDim(Dim)


def _get_macaddress(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    Mac_Array.append(ipconfig_list['MACAddress'])


def _get_baseboard(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    return ipconfig_list['SerialNumber']


def _get_cpu(data):
    ipconfig_list = {}
    for _ in data:
        ipconfig_list[_.Name] = _.Value
    return ipconfig_list['ProcessorId']


class Unpack():
    def __init__(self):
        self.dir_list = []
        self.fweu = None

    def _decryption_fun(self, encrypted_data):
        data_list = [i for i in encrypted_data]
        re_reversed_list1 = data_list[0:10]
        re_reversed_list1.reverse()
        re_reversed_list2 = data_list[10:]
        re_reversed_list2.reverse()
        result_list = re_reversed_list1 + re_reversed_list2
        result = ''.join(result_list)
        return result

    def detecting_max_addr(self, info_addr, base_addr):
        bool_addr_list = []
        for single_info in info_addr:
            bool_addr_list.append(single_info in base_addr)
        return any(bool_addr_list)

    def _confuse(self, encrypt_str):
        encrypt_list = [i for i in encrypt_str]
        reversed_list1 = encrypt_list[0:10]
        reversed_list1.reverse()
        reversed_list2 = encrypt_list[10:]
        reversed_list2.reverse()
        result_list = reversed_list1 + reversed_list2
        result = ''.join(result_list)
        return result

    def _open_key(self, regedit_str, time_key):
        try:
            lock_key = OpenKey(HKEY_CURRENT_USER, regedit_str)
        except:
            self._create_key(regedit_str, time_key)
            lock_key = OpenKey(HKEY_CURRENT_USER, regedit_str)
        return QueryValueEx(lock_key, "Time")[0], QueryValueEx(lock_key, "Bool")[0]

    def _create_key(self, file_path, value):
        key = CreateKey(HKEY_CURRENT_USER, file_path)
        SetValueEx(key, "Time", 0, REG_SZ, value)
        SetValueEx(key, "Bool", 1, REG_SZ, True)
        return value, True

    def _network_time(self):
        url = "https://www.baidu.com"
        try:
            url_time = urlopen(url).headers['Date']
            url_time = datetime.datetime.strptime(url_time, "%a, %d %b %Y %H:%M:%S GMT")
            now_time = time.time()
            offset_time = datetime.datetime.fromtimestamp(now_time) - datetime.datetime.utcfromtimestamp(now_time)
            format_time = url_time + offset_time
            real_time = int(time.mktime(format_time.timetuple()))
        except IOError:
            real_time = int(time.time())
        return real_time

    def decryption(self):
        select_1 = "SELECT * FROM WIN32_NetworkAdapterConfiguration"
        select_2 = "SELECT * FROM Win32_Processor"
        select_3 = "SELECT * FROM Win32_BaseBoard"
        arrInfo = System.Management.ManagementObjectSearcher(select_1)
        cpuInfo = System.Management.ManagementObjectSearcher(select_2)
        boardInfo = System.Management.ManagementObjectSearcher(select_3)

        prop_list = [strInfo_1.Properties for strInfo_1 in arrInfo.Get()]
        cpu_info_list = [strInfo_2.Properties for strInfo_2 in cpuInfo.Get()]
        board_list = [strInfo_3.Properties for strInfo_3 in boardInfo.Get()]
        board_ser = _get_baseboard(board_list[0])

        map(_get_macaddress, prop_list)
        Mac_Address = filter(None, Mac_Array)
        cpu_ser = map(_get_cpu, cpu_info_list)

        now_time = self._network_time()
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
        for file_index, file_data in enumerate(file_str_list):
            if "-KEY" in file_data:
                self.dir_list.append(file_list[file_index])

        def file_open(file):
            with open(file, 'r') as f:
                tuple_data = f.read().split('\n')
            if len(tuple_data) == 2:
                data, temp_time = tuple_data
                result_data = self._decryption_fun(data)
                __regedit_str = r"SOFTWARE\HAE\Scavenger"
                try:
                    origin_data = str(base64.b64decode(result_data))
                    origin_list = origin_data.split('-')
                except TypeError:
                    return False

                try:
                    # 如果存在注册表，则提取时间
                    lock_key = OpenKey(HKEY_CURRENT_USER, __regedit_str)
                    key_time = QueryValueEx(lock_key, "Time")[0]
                    key_bool = QueryValueEx(lock_key, "Bool")[0]
                except:
                    # 不存在，则新建一个注册表
                    key = CreateKey(HKEY_CURRENT_USER, __regedit_str)
                    key_time = temp_time
                    SetValueEx(key, "Time", 0, REG_SZ, key_time)
                    SetValueEx(key, "Bool", 1, REG_SZ, True)

                result_date = base64.b64decode(self._decryption_fun(key_time))
                if int(now_time) < int(result_date):
                    rs.MessageBox('Detected abnormal system time, please change the time and then load Scavenger plug-in!!!', 0 | 16, 'Warning By HAE')
                    lock_in_key = CreateKey(HKEY_CURRENT_USER, __regedit_str)
                    SetValueEx(lock_in_key, "Bool", 1, REG_SZ, False)
                    return False
                else:
                    # 更新键值
                    updata_key = CreateKey(HKEY_CURRENT_USER, __regedit_str)
                    now_time_cip = base64.b64encode(str(now_time).encode('utf-8'))
                    cip_time_str = self._confuse(now_time_cip)
                    SetValueEx(updata_key, "Time", 0, REG_SZ, cip_time_str)
                    SetValueEx(updata_key, "Bool", 0, REG_SZ, True)

                    # 获取新的键值对
                    key_1 = OpenKey(HKEY_CURRENT_USER, __regedit_str)
                    key_1_bool = QueryValueEx(key_1, "Bool")[0]
                    key_1_time = QueryValueEx(key_1, "Time")[0]

                    if key_1_bool == 'True':
                        board_serial_num = origin_list[-3]
                        cpu_serial_num = origin_list[-4]
                        mac_addr_list = origin_list[1:-4]

                        mac_factor = self.detecting_max_addr(mac_addr_list, Mac_Address)
                        if board_ser == board_serial_num and cpu_serial_num == cpu_ser[0]:
                            if int(origin_list[-2]) > now_time:
                                return True
                            else:
                                rs.MessageBox('Your Scavenger plugin has expired! Please contact HAE to obtain new authorization', 0 | 48, 'Tip By HAE')
                                return False
                        else:
                            rs.MessageBox('Your hardware device has been updated, please re-authorize Scavenger!!!', 0 | 16, 'Warning By HAE')
                            return False
                    else:
                        rs.MessageBox('Your Scavenger certificate has expired. Please contact HAE for re authorization!', 0 | 16, 'Warning By HAE')
                        return False
            else:
                rs.MessageBox('No Licence files detected', 0 | 48, 'Tip By HAE')
                return False

        if len(self.dir_list) > 1:
            rs.MessageBox('Cannot contain two Licence files!!!', 0 | 16, 'Warning By HAE')
            return False
        elif not self.dir_list:
            rs.MessageBox('No Licence files detected', 0 | 48, 'Tip By HAE')
            return False
        else:
            bool_factor = file_open(self.dir_list[0])
            return bool_factor


Result = Unpack().decryption()
