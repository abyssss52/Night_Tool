#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File         :   my_OID2VOC_annotation.py
@Modify Time  :   2020/9/15 下午3:58
@Author       :   night
@Version      :   1.0
@License      :   (C)Copyright 2019-2020, Real2tech
@Desciption   :   None

'''
# Script to convert OID annotations to voc format
import os
import xml.etree.ElementTree as ET
from PIL import Image
# import pdb
import argparse



CLASS_MAPPING = {
    'human face': 'face'
    # Add your remaining classes here.
}


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
    parser.add_argument("--image_path", default="/home/night/Datasets/OIDv6/validation/human_face")
    parser.add_argument("--old_annotation_path", default="/home/night/Datasets/OIDv6/validation/human_face/labels/")
    parser.add_argument("--new_annotation_path",
                        default="/home/night/Datasets/OIDv6/validation/human_face/voc_labels/")

    args = parser.parse_args()

    return args




def create_root(image_file_name, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = ""
    ET.SubElement(root, "filename").text = image_file_name
    ET.SubElement(root, "path").text = ""

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "OIDv6"

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
    tree.write(os.path.join(args.new_annotation_path, image_name + '.xml'), short_empty_elements=False)    # "{}/{}.xml".format(args.new_annotation_path, image_name)



def read_file(args, annotation_name):

    image_name = annotation_name.split(".txt")[0]
    image_file_name = "{}.jpg".format(image_name)
    image_file_path = os.path.join(args.image_path, image_file_name)
    img = Image.open(image_file_path)


    w, h = img.size

    prueba = os.path.join(args.old_annotation_path, annotation_name)

    with open(prueba) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            voc.append(float(data[1]))
            voc.append(float(data[2]))
            voc.append(float(data[3]))
            voc.append(float(data[4]))
            voc_labels.append(voc)
        create_file(args, image_file_name, w, h, voc_labels)
    print("Processing complete for file: {}".format(annotation_name))


def main(args):
    success_count = 0
    failure_count = 0
    if not os.path.exists(args.new_annotation_path):
        os.makedirs(args.new_annotation_path)
    for filename in os.listdir(args.old_annotation_path):
        if filename.endswith('txt'):
            try:
                read_file(args, filename)
                success_count += 1
            except:
                print("No")
                failure_count += 1

        else:
            print("Skipping file: {}".format(filename))

    print("成功转换{}个annotations,转换失败{}个annotations".format(success_count, failure_count))


if __name__ == "__main__":
    args = parse_args()
    main(args)