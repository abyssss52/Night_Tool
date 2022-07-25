#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：DuplicateImage.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/5/12
'''


import os
img1_path = 'C:/Users/Microsoft/Downloads/uTools-图片批量处理-20220512151416'
img2_path = 'G:/Public_Data_Sets/AI线扫/广州中心站20220428/carHead'

img1_list = []
img2_list = []
for image in os.listdir(img1_path):
    img_name, suffix = os.path.splitext(image)
    img1_list.append(img_name)

for image in os.listdir(img2_path):
    img_name, suffix = os.path.splitext(image)
    img2_list.append(img_name)


c = [x for x in img1_list if x not in img2_list]  #在list1列表中而不在list2列表中
d = [y for y in img2_list if y not in img1_list]  #在list2列表中而不在list1列表中
print('c的值为:',c)
print('d的值为:',d)
