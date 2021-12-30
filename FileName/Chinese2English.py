#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Wood 
@File ：Chinese2English.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/11/22
'''

import shutil
import os
from tqdm import tqdm

CLASS_MAPPING = {
             '海侧左': 'SL',
             '海侧中': 'SM',
             '海侧右': 'SR',
             '陆侧左': 'LL',
             '陆侧中': 'LM',
             '陆侧右': 'LR',
             '左联系梁': 'CBL',
             '左联系梁CL1': 'CBL1',
             '左联系梁CL2': 'CBL2',
             '左联系梁CL3': 'CBL3',
             '左联系梁CL4': 'CBL4',
             '左联系梁CL5': 'CBL5',
             '左联系梁CL6': 'CBL6',
             '左联系梁CL7': 'CBL7',
             '左联系梁CL8': 'CBL8',
             '右联系梁': 'CBR',
             '右联系梁CR1': 'CBR1',
             '右联系梁CR2': 'CBR2',
             '右联系梁CR3': 'CBR3',
             '右联系梁CR4': 'CBR4',
             '右联系梁CR5': 'CBR5',
             '右联系梁CR6': 'CBR6',
             '右联系梁CR7': 'CBR7',
             '右联系梁CR8': 'CBR8'
             }


# ori_path = ['I:/testData/Defect/2021_11_05/damage']
# new_path = 'I:/testData/Defect/2021_11_05/damage_en'

# ori_path = ['I:/testData/Wood/Third/result']
# new_path = 'I:/testData/Wood/Third/result_en'

# ori_path = ['I:/testData/Wood/Forth/wrongimg']
# new_path = 'I:/testData/Wood/Forth/result_en'

# ori_path = ['I:/testData/Wood/Forth/WoodNumAnno']
# new_path = 'I:/testData/Wood/Forth/WoodNumAnno_en'

ori_path = ['G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum20211210_new']
new_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_en'

if not os.path.exists(new_path):
    os.makedirs(new_path)

for file in tqdm(ori_path):
    for name in tqdm(os.listdir(file)):
        file_name, suffix = os.path.splitext(name)
        if CLASS_MAPPING.get(file_name.split('_')[1]) is None:
            print(file_name.split('_')[1])
        else:
            num = len(file_name.split('_'))
            if num != 3:
                print(num)
                print(file_name)
            shutil.copy2(os.path.join(file, name), os.path.join(new_path, file_name.split('_')[0] + '_' + CLASS_MAPPING.get(file_name.split('_')[1]) + '_' + file_name.split('_')[2].zfill(2) + suffix))

