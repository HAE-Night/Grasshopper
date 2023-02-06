# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : _do_main
# @Time : 2023/1/10 14:45

import datetime
import os
import shutil
import time
import tkinter
from tkinter import filedialog as tf
from tkinter import messagebox as tm
from multiprocessing.dummy import Pool
from itertools import chain
import sys

from PyPDF2 import PdfMerger

root = tkinter.Tk()
root.withdraw()


class TestPdfMerge:
    """C、D类型文件"""

    def __init__(self):
        self.pdf_list = []

    def _get_all_pdf(self, file_path: str):
        """循环遍历获取文件夹所有Pdf"""
        sub_path = []
        for f_path in os.listdir(file_path):
            abso_path = os.path.join(file_path, f_path)
            if os.path.isdir(abso_path):
                self._get_all_pdf(abso_path)
            elif os.path.isfile(abso_path):
                if abso_path.endswith('pdf'):
                    sub_path.append(abso_path)
        self.pdf_list.append(sub_path)

    def pdf_class(self, list_data: list):
        """Pdf分类"""
        res_list = [_ for _ in list_data if 'BAR' not in _]
        if res_list:
            assembly_data = []
            cutting_data = []
            other_data = []
            if res_list:
                for sub_data in list_data:
                    if "ASSEMBLY" in sub_data:
                        assembly_data.append(sub_data)
                    elif "CUTTING" in sub_data:
                        cutting_data.append(sub_data)
                    else:
                        other_data.append(sub_data)
            other_data = self.second_sort(other_data)
            total_list = assembly_data + cutting_data + other_data
            return total_list

    @staticmethod
    def second_sort(alphabet_list: list):
        """Pdf排序"""
        if alphabet_list:
            origin_data_file = list(map(lambda x: x.split('\\')[-1], alphabet_list))
            origin_dir = list(map(lambda x: '\\'.join(x.split('\\')[0: -1]), alphabet_list))
            ch_list = []
            en_list = []

            def __check_str(word_name: str):
                for _char in word_name:
                    if '\u4e00' <= _char <= '\u9fa5':
                        return True
                return False

            for o_index, items in enumerate(origin_data_file):
                if __check_str(items):
                    ch_list.append(origin_dir[o_index] + "\\" + items)
                else:
                    en_list.append(origin_dir[o_index] + "\\" + items)
            set_of_list = ch_list + en_list
            return set_of_list


class TypeABE:
    """A、B、E类型文件"""

    def __init__(self, ta_path):
        self.ta_path = ta_path

    def _group_pdf(self, sources_path):
        """A、B、E类型文件夹子pdf合并主方法"""
        list_dir = [os.path.join(self.ta_path, _) for _ in os.listdir(self.ta_path)]
        abe_pool_pond = Pool(10)

        group_pdf, list_pdf = list(zip(*abe_pool_pond.map(self._find_pdf_file, list_dir)))
        save_dir_list = []
        for num_index, num in enumerate(group_pdf):
            number_no = '-'.join(num.split('\\')[-1].split('-')[0: 2])
            if number_no in sources_path[num_index]:
                save_dir = '\\'.join(sources_path[num_index].split("\\") + [num])
                save_dir_list.append(save_dir)
        zip_list = list(zip(save_dir_list, list_pdf))
        abe_pool_pond.map(self._merge_pdf, zip_list)
        return save_dir_list

    def _merge_pdf(self, tuple_data):
        """合并Pdf"""
        target_file, source_file = tuple_data
        if not os.path.exists(target_file):
            file_merger = PdfMerger()
            for pdf in source_file:
                file_merger.append(pdf, import_outline=False)
            file_merger.write(target_file)

    def _find_pdf_file(self, data: str):
        """子类型Pdf"""
        file_list = []
        father_path = None
        now_time = datetime.datetime.now()
        date = "".join(str(now_time).split(" ")[0].split("-"))
        for root, dirs, files in os.walk(data):
            for file in files:
                if file.endswith('pdf'):
                    path = os.path.join(root, file)
                    file_list.append(path)
            father_path = root
        sub_file_path = father_path.split("\\")[-1] + '-' + '加工图' + "-" + date + '-' + '1.pdf'
        return sub_file_path, file_list


Pdf_M = TestPdfMerge()
bool_res = tm.askyesno("Tips", "Is this part a folder of type A, B and E?")
path = tf.askdirectory(title="Folders to be merged")

dir_path = [os.path.join(path, sub) for sub in os.listdir(path)]

if bool_res:
    bool_dir_path = [True if 'BAR DWG' in _ else False for _ in dir_path]
    target_dir = None
    sources_dir = []
    factor = any(bool_dir_path)
    if factor:
        for target_index in range(len(dir_path)):
            if bool_dir_path[target_index]:
                target_dir = dir_path[target_index]
            else:
                sources_dir.append(dir_path[target_index])
        group_pdf_list = (TypeABE(target_dir)._group_pdf(sources_dir))
    else:
        tm.showerror("Error", "The file storing the working drawing is not found!")
        sys.exit()

Pdf_M._get_all_pdf(path)
move_pdf_list = [_ for _ in Pdf_M.pdf_list if len(_) == 1]
pdf_list = [_ for _ in Pdf_M.pdf_list if _ not in move_pdf_list]

"""----------------剔除非对象Pdf文件----------------"""
for add_pdf in move_pdf_list:
    ident = '-'.join(add_pdf[0].split('\\')[-1].split('-')[0: 2])
    pdf_file = add_pdf[0].split('\\')[-1]
    for target_dir in pdf_list:
        if target_dir:
            if ident in target_dir[0] and 'BAR' not in target_dir[0]:
                pdf_dir = '\\'.join(target_dir[0].split('\\')[0: -1])
                if not os.path.exists(os.path.join(pdf_dir, pdf_file)):
                    shutil.copy(add_pdf[0], pdf_dir)
"""-----------------------------------------------"""

pool_pond = Pool(10)
sort_done_list = [_ for _ in pool_pond.map(Pdf_M.pdf_class, pdf_list) if _ is not None]
sort_done_list = list(chain(*sort_done_list))

f_save_path = sort_done_list[0].split("/")[0: -1]
s_save_path = sort_done_list[0].split("/")[-1].split("\\")[0] + "\\" + "Merged_File.pdf"
save_path = '\\'.join(f_save_path) + "\\" + s_save_path

file_merger = PdfMerger()
for pdf in sort_done_list:
    file_merger.append(pdf, import_outline=False)
file_merger.write(save_path)
tm.showinfo("Tips", f"Pdf merger has been completed; File location is in {save_path}")
sys.exit()
