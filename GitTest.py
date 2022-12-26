# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : GitTest
# @Time : 2022/10/31 9:37

import time
import re

def runtime(func):
    time_start = time.time()
    func()
    time_end = time.time()
    return time_end - time_start


def powers(limit):
    new_list = []
    for i in range(limit):
        new_list.append(i ** 2)
    return new_list


print(runtime(lambda: powers(5000000)))