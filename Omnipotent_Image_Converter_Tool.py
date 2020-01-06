#! /usr/bin/env python
# coding=utf-8
#================================================================
#
#   Editor      : Pycharm
#   File name   : Omnipotent_Image_Converter_Tool.py
#   Author      : night
#   Description : 用于储存常用工具
#   Date        : 2020.01.06
#
#================================================================

import numpy as np
import cv2
from PIL import Image
import os
import shutil


# jpeg转jpg
def jpeg2jpg(img_path):
    wrong_img = 0     # 记录无法读取的照片数量
    jpg_num = 0       # 记录原jpg图数量
    jpeg_num = 0      # 记录被转换数量
    imgList = os.listdir(img_path)

    if not os.path.exists(os.path.join(img_path, 'SourceImage')):
        os.mkdir(os.path.join(img_path, 'SourceImage'))
    for name in imgList:
        try:
            org_img_path = os.path.join(img_path, name)
            # img = Image.open(org_img_path)  # 尝试打开图片
            img = cv2.imread(org_img_path)
            img_name, img_type = os.path.splitext(name)  # 分割文件名和文件格式

            if img_type == '.jpg':
                jpg_num += 1
                continue
            else:
                jpeg_num += 1
                new_img_path = os.path.join(img_path, img_name + '.jpg')
                # img.save(new_img_path, quality=100)  # 转换格式
                cv2.imwrite(new_img_path, img)
                shutil.move(org_img_path, os.path.join(img_path, 'SourceImage', name))  # 移动原图片
        except IOError:
            print('file %s can not be opened' % name)
            wrong_img += 1

    print("无法读取的图片数量：", wrong_img)
    print("原jpg图数量：", jpg_num)
    print("转换照片数量：", jpeg_num)


# PIL Image转换成OpenCV格式
def PILtoCV(img_PIL):
    img_CV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img_CV


# OpenCV图片转换为PIL image
def CVtoPIL(img_CV):
    img_PIL = Image.fromarray(cv2.cvtColor(img_CV, cv2.COLOR_BGR2RGB))
    return img_PIL


# 图片字节流转换为cv image
def bytes_to_cvimage(img_bytes):
    img_CV = cv2.cvtColor(np.asarray(img_bytes), cv2.COLOR_RGB2BGR)
    return img_CV





# if __name__ == "__main__":
    # jpeg2jpg("/home/night/PycharmProjects/Picture_Classification/Tensorflow-Resnet-Image-Classification/data/train/change")