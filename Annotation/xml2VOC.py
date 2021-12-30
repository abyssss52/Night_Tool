#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：xml2VOC.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/12/20
'''


# Script to convert labelimg annotations to voc format
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os
import shutil
import json
from PIL import Image
# import pdb
import argparse
import cv2
from tqdm import tqdm
from sklearn.model_selection import train_test_split




def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="I:/testData/Defect/20211112/damage_en")   # 第一次训练集'I:\\testData\\Defect\\2021_11_05\\damage_en'
    parser.add_argument("--old_annotation_path", default="I:/testData/Defect/20211112/damage_en")    # 第一次训练集'I:\\testData\\Defect\\2021_11_05\\damage_en'
    parser.add_argument("--new_annotation_path",
                        default="G:\\Public_Data_Sets\\AutoDefect\\VOC2007")

    args = parser.parse_args()

    return args


def create_root(image_file_name, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "VOC2007"
    ET.SubElement(root, "filename").text = image_file_name
    ET.SubElement(root, "path").text = ""

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "PF Defect Database"
    ET.SubElement(source, "annotation").text = "PASCAL VOC2007"
    ET.SubElement(source, "image").text = "PFKJ"
    ET.SubElement(source, "flickrid").text = ""

    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    ET.SubElement(root, "segmented").text = "0"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(args, image_file_name, width, height, voc_labels):
    root = create_root(image_file_name, width, height)
    root = create_object_annotation(root, voc_labels)

    prettyXml(root, '    ', '\n')

    tree = ET.ElementTree(root)
    image_name = image_file_name.split(".jpg")[0]
    tree.write(os.path.join(os.path.join(args.new_annotation_path, 'Annotations'), image_name + '.xml'), short_empty_elements=False)    # "{}/{}.xml".format(args.new_annotation_path, image_name)



def xml2voc(args, annotation_name):

    image_name, suffix = os.path.splitext(annotation_name)
    # image_name = annotation_name.split(".txt")[0]
    image_file_name = image_name + '.jpg'
    # image_file_name = "{}.jpg".format(image_name)
    image_file_path = os.path.join(args.image_path, image_file_name)
    # img = Image.open(image_file_path)
    # w, h = img.size

    # 读取xml文件
    prueba = os.path.join(args.old_annotation_path, annotation_name)
    tree = ET.ElementTree(file=prueba)
    root = tree.getroot()
    width = root.findall('size')[0].find('width').text
    height = root.findall('size')[0].find('height').text
    voc_labels = []  # 用来存放所有labels
    ObjectSet = root.findall('object')
    for Object in ObjectSet:
        voc = []
        ObjName = Object.find('name').text
        # 解决标注员标注腐蚀标签名错误
        if ObjName == 'Corroison':
            ObjName = 'Corrosion'

        BndBox = Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)

        voc.append(ObjName)
        voc.append(x1)
        voc.append(y1)
        voc.append(x2)
        voc.append(y2)
        voc_labels.append(voc)

    # 生成xml
    create_file(args, image_file_name, width, height, voc_labels)

    # 复制图片到 VOC2007/JPEGImages/下
    shutil.copy2(image_file_path, os.path.join(os.path.join(args.new_annotation_path, 'JPEGImages'), image_file_name))

    print("Processing complete for file: {}".format(annotation_name))

    return voc_labels


def main(args):
    success_count = 0
    failure_count = 0
    labels_dict = {'Corrosion': 0, 'Concave': 0, 'Convex': 0, 'Deformation': 0, 'Pole': 0, 'Edge': 0, 'Pillar': 0, 'Hole': 0}
    # 2.创建要求文件夹
    if not os.path.exists(args.new_annotation_path):
        os.makedirs(args.new_annotation_path)
    if not os.path.exists(os.path.join(args.new_annotation_path, 'Annotations')):
        os.makedirs(os.path.join(args.new_annotation_path, 'Annotations'))
    if not os.path.exists(os.path.join(args.new_annotation_path, 'JPEGImages')):
        os.makedirs(os.path.join(args.new_annotation_path, 'JPEGImages'))
    if not os.path.exists(os.path.join(args.new_annotation_path, 'ImageSets', 'Main')):
        os.makedirs(os.path.join(args.new_annotation_path, 'ImageSets', 'Main'))

    for filename in os.listdir(args.old_annotation_path):
        if filename.endswith('xml'):
            try:
                labels_list = xml2voc(args, filename)
                success_count += 1
                for i in range(len(labels_list)):
                    labels_dict[labels_list[i][0]] = int(labels_dict[labels_list[i][0]]) + 1;
            except:
                print("No")
                failure_count += 1

        else:
            print("Skipping file: {}".format(filename))

    # split files for txt
    total_files = os.listdir(os.path.join(args.new_annotation_path, 'Annotations'))
    total_files = [i.split("/")[-1].split(".xml")[0] for i in total_files]

    # split
    train_files, val_files = train_test_split(total_files, test_size=0.2, random_state=52)
    txt_path = os.path.join(args.new_annotation_path, 'ImageSets', 'Main')
    # train
    with open(os.path.join(txt_path, 'trainval.txt'), 'w') as f:
        for file in train_files:
            f.write(file + "\n")
    # val
    with open(os.path.join(txt_path, 'test.txt'), 'w') as f:
        for file in val_files:
            f.write(file + "\n")

    print("成功转换{}个annotations,转换失败{}个annotations".format(success_count, failure_count))
    print("腐蚀标签{}个，凹标签{}个，凸标签{}个，箱面变形标签{}个，拉杆变形标签{}个，棱变形标签{}个，柱变形标签{}个，洞标签{}个"
          .format(labels_dict['Corrosion'], labels_dict['Concave'], labels_dict['Convex'], labels_dict['Deformation'], labels_dict['Pole'], labels_dict['Edge'], labels_dict['Pillar'], labels_dict['Hole']))

if __name__ == "__main__":
    args = parse_args()
    main(args)