#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：Frame_extarction.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/12/24
'''

import cv2
import os
import random
from tqdm import tqdm

FRAME_INTE = 2

def Exact_Frame(video_path, image_save_path, img_num, file_idx):
    video_name, suffix = os.path.splitext(os.path.basename(video_path))

    cap = cv2.VideoCapture(video_path)
    count = 0
    index = 0
    frame_num = 0
    frame_idx = []
    # fNum = 0
    # 单个视频随机抽四帧  6s-10s之间  15帧
    # total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("[INFO] {} total frames in video".format(total))
    for i in range(4):
        frame_idx.append(random.randint(90, 150))

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # 每隔FRAME_INTE抽一帧
            if count % FRAME_INTE == 0:
            # # 单个视频随机抽三帧
            # if frame_num in frame_idx:
                if img_num % 10000 == 0:
                    file_idx += 1
                    os.makedirs(image_save_path + '_' + str(file_idx))

                cv2.imwrite(os.path.join(image_save_path + '_' + str(file_idx), video_name + '_' + str(index).zfill(6) + '.jpg'), frame)
                index += 1
                img_num += 1
                print('完成第%d张' % index)
            # fNum += 1
        else:
            break

        frame_num += 1
        count += 1
    print(os.path.basename(video_path)+'视频读取完成')
    # print('这个视频有%d' % fNum)
    cap.release()
    cv2.destroyAllWindows()
    return img_num, file_idx

if __name__ == "__main__":
    img_num = 0
    file_idx = 0
    # 单个视频
    video_path = 'G:/Image_Composite_Editor/Cache/20211224134126_0e9ba65d82fb40e887bfbcb58e22ebdb.mp4'
    image_save_path = 'G:/Image_Composite_Editor/Cache/extract'
    img_num, file_idx = Exact_Frame(video_path, image_save_path, img_num, file_idx)