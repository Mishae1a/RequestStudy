#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

args = sys.argv
# 0 为脚本本身 1 为第一个参数
if (len(args) == 1):
    print('参数错误')
    exit

#switch (args[1]):
# wc py竟然没switch
if (args[1] == 'list'):
    import controller.runList
else:
    print('参数错误 请运行 list detail')

