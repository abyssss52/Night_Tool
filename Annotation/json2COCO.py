#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：json2COCO.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/7/25
'''

import sys
import os
import shutil
import time
import json
from tqdm import tqdm
import argparse

from sklearn.model_selection import train_test_split

START_BOUNDING_BOX_ID = 1

# 注意下面的dict存储的是实际检测的类别，需要根据自己的实际数据进行修改
# 这里以自己的数据集person和hat两个类别为例，如果是VOC数据集那就是20个类别
# 注意类别名称和json文件中的标注名称一致
# 注意按照自己的数据集名称修改编号和名称
PRE_DEFINE_CATEGORIES = {"Headlight": 0, "CHNSingle": 1, "CHNDouble": 2}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", default="G:/Public_Data_Sets/ChineseLP/Chinese_Anno")
    parser.add_argument("--json_path", default="G:/Public_Data_Sets/ChineseLP/Chinese_Anno")
    parser.add_argument("--new_coco_path", default="G:/Public_Data_Sets/ChineseLP/COCO")

    args = parser.parse_args()

    return args

def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.' % (filename))

def convert(labelme_json_dir, labelme_json_list, COCO_json_file, COCO_json_dict):

    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    num = 0
    for labelme_json_file in labelme_json_list:
        #         print("Processing %s"%(line))
        num += 1
        if num % 50 == 0:
            print("processing ", num, "; file ", labelme_json_file)

        labelme_json_path = os.path.join(labelme_json_dir, labelme_json_file)

        with open(labelme_json_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        ## The filename must be a number
        filename, _ = os.path.splitext(labelme_json_file)
        image_id = get_filename_as_int(filename)
        # size = get_and_check(root, 'size', 1)
        width = data['imageWidth']
        height = data['imageHeight']

        image = {'file_name': (filename + '.jpg'), 'height': height, 'width': width,
                 'id': image_id}
        COCO_json_dict['images'].append(image)
        ## Currently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for shapes in data['shapes']:
            shape_type = shapes['shape_type']
            if shape_type == 'rectangle':
                category = shapes['label'].split('#')[0]
                if category not in categories:
                    print(category)
                    continue
                    # new_id = len(categories)
                    # categories[category] = new_id
                category_id = categories[category]
                bbox = shapes['points']
                xmin = bbox[0][0]
                ymin = bbox[0][1]
                xmax = bbox[1][0]
                ymax = bbox[1][1]
                assert (xmax > xmin)
                assert (ymax > ymin)
                o_width = abs(xmax - xmin)
                o_height = abs(ymax - ymin)
                # if (o_width < 30 and o_height < 30):
                #     print('原木截面宽：%d, 高：%d' % (o_width, o_height))
                #     continue
                ann = {'segmentation': [],
                       'area': o_width * o_height,
                       'iscrowd': 0,
                       'image_id': image_id,
                       'bbox': [xmin, ymin, o_width, o_height],
                       'category_id': category_id,
                       'id': bnd_id,
                       'ignore': 0,
                       }
                COCO_json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'ChineseLP', 'id': cid, 'name': cate}
        COCO_json_dict['categories'].append(cat)
    json_fp = open(COCO_json_file, 'w', encoding='utf-8')
    json_str = json.dumps(COCO_json_dict, ensure_ascii=False, indent=4)
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
    for json_file in os.listdir(args.json_path):
        file_name, suffix = os.path.splitext(json_file)
        if suffix == '.json':
            os.rename(os.path.join(args.json_path, file_name + '.jpg'), os.path.join(args.json_path, str(file_idx).zfill(12) + '.jpg'))
            os.rename(os.path.join(args.json_path, file_name + '.json'), os.path.join(args.json_path, str(file_idx).zfill(12) + '.json'))
            total_files.append(str(file_idx).zfill(12) + '.json')
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
        json_dict["info"] = {"description": "PF Chinese License Plate Dataset",
                             "url": "www.pingfang.net",
                             "version": "1.0",
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
            shutil.copy(os.path.join(args.json_path, file_name + '.jpg'), os.path.join(args.new_coco_path, categoryName, file_name + '.jpg'))
        convert(args.json_path, files_collection[i], json_dir, json_dict)