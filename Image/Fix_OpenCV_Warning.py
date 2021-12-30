#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool
@File ：Fix_OpenCV_Warning.pym
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/12/30
@Description: 为了解决训练是，OpenCV读图报warning的问题
'''

import os
import cv2
from tqdm import tqdm

ori_img_path = '/media/li/G1/Projects/Defect_Detection/YOLOX/datasets/VOCdevkit/VOC2007/JPEGImages'


if os.path.exists(ori_img_path + '_1'):
    print('保存路径已存在！')
else:
    os.mkdir(ori_img_path + '_1')


for image_file in tqdm(os.listdir(ori_img_path)):
    img = cv2.imread(os.path.join(ori_img_path, image_file), 1)
    cv2.imwrite(os.path.join(ori_img_path + '_1', image_file), img)