#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：change_image_suffix.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/4/1
'''

import cv2
import os
import shutil


image_path = 'F:/Codes/VSProjects/Work/AICoreLib_container/x64/Release/AILIB/imgs_container'
# image_path = 'G:/Public_Data_Sets/新箱号/闸口/问题箱号/20220406'
for file in os.listdir(image_path):
    file_name, suffix = os.path.splitext(file)
    if suffix == '.png' or suffix == '.bmp':
        shutil.move(os.path.join(image_path, file), os.path.join(image_path, file_name + '.jpg'))