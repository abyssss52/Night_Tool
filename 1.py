#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：1.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/1/2
'''

import os
import time
import numpy as np
import cv2
# a = [[7,1],[8,2],[9,-1],[6,0]]
# head=3
# head=a[head][1]
# print(a)

# # time1 = time.time()
# date = time.strftime("%Y/%m/%d", time.localtime())
# print(type(date))

# def augment_hsv(img, hgain=5, sgain=30, vgain=30):
#     hsv_augs = np.random.uniform(-1, 1, 3) * [hgain, sgain, vgain]  # random gains
#     hsv_augs *= np.random.randint(0, 2, 3)  # random selection of h, s, v
#     hsv_augs = hsv_augs.astype(np.int16)
#     img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.int16)
#
#     img_hsv[..., 0] = (img_hsv[..., 0] + hsv_augs[0]) % 180
#     img_hsv[..., 1] = np.clip(img_hsv[..., 1] + hsv_augs[1], 0, 255)
#     img_hsv[..., 2] = np.clip(img_hsv[..., 2] + hsv_augs[2], 0, 255)
#
#     cv2.cvtColor(img_hsv.astype(img.dtype), cv2.COLOR_HSV2BGR, dst=img)  # no return needed
#
# # for image in os.listdir('I:/testData/Wood/Fifth/COCO/test2022'):
# for image in os.listdir('/media/li/G1/Projects/Defect_Detection/YOLOX/datasets/COCO/test2022'):
#     # while(1):
#     if image.endswith('jpg'):
#         # img = cv2.imread(os.path.join('I:/testData/Wood/Fifth/COCO/test2022', image))
#         img = cv2.imread(os.path.join('/media/li/G1/Projects/Defect_Detection/YOLOX/datasets/COCO/test2022', image))
#         cv2.imshow('result_ori', img)
#         cv2.namedWindow('result_ori', 0)
#         # augment_hsv(img)
#         # cv2.imshow('result', img)
#         # cv2.namedWindow('result_ori', 0)
#         # cv2.waitKey(0)

# img = cv2.imread('F:/Codes/VSProjects/Work/AICoreLib_container/x64/Release/AILIB/imgs_container/20220622112424639_right_Camera(1).jpg')
# height, width = img.shape[:2]
# size = (int(width * 0.2), int(height * 0.2))
# # 缩放
# img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
#
# # BGR转化为HSV
# HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
#
# # 鼠标点击响应事件
# def getposHsv(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print("HSV is", HSV[y, x])
#
#
# def getposBgr(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print("Bgr is", img[y, x])
#
#
# cv2.imshow("imageHSV", HSV)
# cv2.imshow('image', img)
# cv2.setMouseCallback("imageHSV", getposHsv)
# cv2.setMouseCallback("image", getposBgr)
# cv2.waitKey(0)


list = [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]]
for i, lic_no in enumerate(list):
    lic_no[1] = 100
print(list)