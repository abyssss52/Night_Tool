#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：Image_Operation.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/12/9
'''
import os
import shutil
import cv2
# import math
import numpy as np
from tqdm import tqdm



def flips(img, ori):
    flip_img = cv2.flip(img, ori)   # ori 1 水平翻转   0 垂直翻转   -1 水平垂直翻转
    return flip_img

def crop(img, ratio, start_point):
    img_list = []
    if ratio != 0 and start_point == 0:
        size = img.shape
        height = size[0]
        width = size[1]

        split_line = int(width * ratio)
        img_num = int(1 / ratio)
        for i in range(img_num):
            img_list.append(img[0:height, i * split_line:(i + 1) * split_line])
    elif start_point != 0 and ratio == 0:
        size = img.shape
        height = size[0]
        width = size[1]

        split_line = start_point
        img_num = int(width / start_point)
        for i in range(img_num):
            img_list.append(img[0:height, i * split_line:(i + 1) * split_line])
    return img_list

# padding最右侧
def padding(img, width, color):
    padding_value = width - img.shape[1]
    pad_img = cv2.copyMakeBorder(img, 0, 0, 0, padding_value, cv2.BORDER_CONSTANT, value=(color, color, color))  # top，bottom，left，right

    return pad_img


# 旋转
def rotate(img, angle):
    # rows, cols, _ = img.shape
    if angle == 270:
        dst = np.rot90(np.rot90(np.rot90(img)))
    if angle == 180:
        dst = np.rot90(np.rot90(img))
    return dst

if __name__=='__main__':
    # img_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架历史数据/extract'
    # save_path = 'G:/Public_Data_Sets/RoofNum20211210'

    # img_path = ['I:/testData/TrainNum/First/12-11', 'I:/testData/TrainNum/First/12-12', 'I:/testData/TrainNum/First/12-13', 'I:/testData/TrainNum/First/12-14', 'I:/testData/TrainNum/First/12-15', 'I:/testData/TrainNum/First/12-16']
    # save_path = 'I:/testData/TrainNum/First/TrainAnno_2'

    # img_path = ['I:/testData/TrainNum/JSQ6/JSQ6_ori']
    # save_path = 'I:/testData/TrainNum/JSQ6/JSQ6_Anno'

    # img_path = ['I:/testData/TrainNum/X/X_ori']
    # save_path = 'I:/testData/TrainNum/X/X_Anno'

    img_path = ['G:/Public_Data_Sets/tmp/posTopNum']
    save_path = 'G:/Public_Data_Sets/tmp/posTopNumflip'

    # 镜像处理
    # for img in os.listdir(img_path):
    #     print(img)
    #     image = cv2.imread(os.path.join(img_path, img))
    #     # print(image.shape[0], image.shape[1])
    #     # cv2.imshow('test', image)
    #     # cv2.waitKey(0)
    #     image = flips(image, 1)
    #     cv2.imwrite(os.path.join(save_path, img), image)

    # 分割图片
    # for j in range(len(img_path)):
    #     for img in tqdm(os.listdir(img_path[j])):
    #         # image = cv2.imread(os.path.join(img_path[i], img))
    #         image = cv2.imdecode(np.fromfile(os.path.join(img_path[j], img), dtype=np.uint8), -1)
    #         image_list = crop(image, 0.5, 0)      # 220
    #         for i in range(len(image_list)):
    #             img_name, suffix = os.path.splitext(img)
    #             cv2.imwrite(os.path.join(save_path, img_name + str(i).zfill(2)+ suffix), image_list[i])


    # 补padding
    # for file in tqdm(os.listdir(img_path)):
    #     file_name, ext = os.path.splitext(file)
    #     if ext == '.jpg':
    #         image = cv2.imdecode(np.fromfile(os.path.join(img_path, file), dtype=np.uint8), -1)
    #         image_padding = padding(image, 1920, 0)
    #         # cv2.imshow("result", image_padding)
    #         # cv2.waitKey(0)
    #         cv2.imwrite(os.path.join(save_path, file), image_padding)
    #         # cv2.imshow("result", image_padding)
    #         # cv2.waitKey(0)
    #     else:
    #         shutil.copy2(os.path.join(img_path, file), os.path.join(save_path, file))


    # 旋转图片
    for j in range(len(img_path)):
        for img in tqdm(os.listdir(img_path[j])):
            image = cv2.imdecode(np.fromfile(os.path.join(img_path[j], img), dtype=np.uint8), -1)
            rotate_image = rotate(image, 180)
            img_name, suffix = os.path.splitext(img)
            cv2.imwrite(os.path.join(save_path, img_name + '_flip'+ suffix), rotate_image)