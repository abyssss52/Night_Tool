#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：Load_brightness_value.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/6/5
'''


import os

file_list_path = 'G:/BrightnessAnalyze/2022-06-02'
with open('G:/BrightnessAnalyze/2022-06-02/all.txt', 'a') as recordf:
    for file in os.listdir(file_list_path):
        f = open(os.path.join(file_list_path, file), encoding='utf-8')
        for txtline in f.readlines():
            if '图片ID' in txtline:
                print(txtline)
                recordf.write(txtline)
        f.close()

# i = 0
# with open('G:/BrightnessAnalyze/2022-06-01/all.txt', 'r') as recordf:
#     for txtline in recordf.readlines():
#         f = open('G:/BrightnessAnalyze/2022-06-01/all_1.txt', 'a')
#         if i % 2 == 1:
#             f.write(txtline)
#         i += 1
