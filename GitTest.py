# -- coding: utf-8 --
# -------------------------------
# @Author : 水密菠罗
# @Email : smblscr47@163.com
# -------------------------------
# @File : GitTest
# @Time : 2022/10/31 9:37

import time


def runtime(func):
    time_start = time.time()
    func()
    time_end = time.time()
    return time_end - time_start


def powers(limit):
    return [i ** 2 for i in range(limit)]


print(runtime(lambda: powers(5000000)))
