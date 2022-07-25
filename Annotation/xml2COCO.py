#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：xml2COCO.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/1/29
'''

import sys
import os
import shutil
import time
import json
from tqdm import tqdm
import argparse
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from sklearn.model_selection import train_test_split

START_BOUNDING_BOX_ID = 1

# 注意下面的dict存储的是实际检测的类别，需要根据自己的实际数据进行修改
# 这里以自己的数据集person和hat两个类别为例，如果是VOC数据集那就是20个类别
# 注意类别名称和xml文件中的标注名称一致
# 注意按照自己的数据集名称修改编号和名称
PRE_DEFINE_CATEGORIES = {"Wood": 0}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", default="I:/testData/Wood/Fifth/traindata1")   # 第一次训练集'I:\\testData\\Defect\\2021_11_05\\damage_en'
    parser.add_argument("--xml_path", default="I:/testData/Wood/Fifth/traindata1")    # 第一次训练集'I:\\testData\\Defect\\2021_11_05\\damage_en'
    parser.add_argument("--new_coco_path",
                        default="I:/testData/Wood/Fifth/COCO")

    args = parser.parse_args()

    return args


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.' % (filename))


def convert(xml_dir, xml_list, json_file, json_dict):

    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    num = 0
    for line in xml_list:
        #         print("Processing %s"%(line))
        num += 1
        if num % 50 == 0:
            print("processing ", num, "; file ", line)

        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        ## The filename must be a number
        filename, _ = os.path.splitext(line)
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        # image = {'file_name': filename, 'height': height, 'width': width,
        #          'id':image_id}
        image = {'file_name': (filename + '.jpg'), 'height': height, 'width': width,
                 'id': image_id}
        json_dict['images'].append(image)
        ## Currently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text.encode('utf-8').decode('utf-8-sig')
            if category not in categories:
                # print(category)
                continue
                # new_id = len(categories)
                # categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) # - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) # - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert (xmax > xmin)
            assert (ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            if (o_width < 30 and o_height < 30):
                print('原木截面宽：%d, 高：%d' % (o_width, o_height))
                continue
            ann = {'segmentation': [],
                   'area': o_width * o_height,
                   'iscrowd': 0,
                   'image_id': image_id,
                   'bbox': [xmin, ymin, o_width, o_height],
                   'category_id': category_id,
                   'id': bnd_id,
                   'ignore': 0,
                   }
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'Zhangjiagang', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict, ensure_ascii=False, indent=4)
    json_fp.write(json_str)
    json_fp.close()


if __name__ == '__main__':
    category_list = ["train2022", "val2022"]
    total_files = []
    files_collection = []
    file_idx = 0
    date = time.strftime("%Y/%m/%d", time.localtime())
    args = parse_args()

    # 创建annotations文件夹
    if not os.path.exists(args.new_coco_path):
        os.makedirs(args.new_coco_path)
    if not os.path.exists(os.path.join(args.new_coco_path, 'annotations')):
        os.makedirs(os.path.join(args.new_coco_path, 'annotations'))

    # 生成train, val, 目前设定是8:2
    for xml_file in os.listdir(args.xml_path):
        file_name, suffix = os.path.splitext(xml_file)
        if suffix == '.xml':
            os.rename(os.path.join(args.xml_path, file_name + '.jpg'), os.path.join(args.xml_path, str(file_idx).zfill(12) + '.jpg'))
            os.rename(os.path.join(args.xml_path, file_name + '.xml'), os.path.join(args.xml_path, str(file_idx).zfill(12) + '.xml'))
            total_files.append(str(file_idx).zfill(12) + '.xml')
            file_idx += 1

    # split
    train_files, val_files = train_test_split(total_files, test_size=0.2, random_state=52)
    # val_files, test_files = train_test_split(valtest_files, test_size=0.5, random_state=52)
    files_collection.append(train_files)
    files_collection.append(val_files)
    # files_collection.append(test_files)

    for i in range(2):
        json_dict = {"info": {}, "licenses": [], "images": [], "annotations": [],
                     "categories": []}  # , "type": "instances"
        json_dict["info"] = {"description": "PF Zhangjiagang Wood Dataset",
                             "url": "www.pingfang.net",
                             "version": "2.0",
                             "year": 2022,
                             "contributor": "Night",
                             "date_created": date}
        license_dict = {"url": "www.pingfang.net",
                        "id": 1,
                        "name": "PF License"}
        json_dict["licenses"].append(license_dict)


        categoryName = category_list[i]
        json_dir = os.path.join(args.new_coco_path, "annotations", "instances_" + categoryName + ".json")

        # 创建train,val文件夹
        if not os.path.exists(os.path.join(args.new_coco_path, categoryName)):
            os.makedirs(os.path.join(args.new_coco_path, categoryName))


        # print("deal: ", folderName)
        # print("xml dir: ", xml_dir)
        # print("json file: ", json_dir)
        # 把图片存到对应文件夹内
        for file in tqdm(files_collection[i]):
            file_name, _ = os.path.splitext(file)
            shutil.copy(os.path.join(args.xml_path, file_name + '.jpg'), os.path.join(args.new_coco_path, categoryName, file_name + '.jpg'))
        convert(args.xml_path, files_collection[i], json_dir, json_dict)