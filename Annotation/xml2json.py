#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：xml2json.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/7/8
'''

import xml.etree.ElementTree as ET
import os
import json
import cv2
from io import BytesIO
import base64
from PIL import Image
import numpy as np


def makefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:  # 创建一个params.json文件
        f.write(content)  # 将json_str写到文件中

    # if os.path.exists(path):
    #     if os.path.isdir(path):
    #         #**
    #     else:
    #         print('please input the dir name')
    # else:
    #     print('the path is not exists')


def toJson(image_name, imageHeight, imageWidth, shape_type, label, points, xml_path, json_path):
    print(image_name)
    imagePath = os.path.join(xml_path, image_name + '.jpg')
    coco = dict()
    coco['version'] = "5.0.1"
    coco['flags'] = dict()
    coco['shapes'] = [1]
    coco['shapes'][0] = dict()
    coco['shapes'][0]['label'] = label
    coco['shapes'][0]['points'] = points
    coco['shapes'][0]['group_id'] = None
    coco['shapes'][0]['shape_type'] = "rectangle"
    coco['shapes'][0]['flags'] = dict()

    coco['imagePath'] = image_name + '.jpg'

    img = img = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    coco['imageData'] = new_image_string

    coco['imageHeight'] = imageHeight
    coco['imageWidth'] = imageWidth

    makefile(os.path.join(json_path, image_name + '.json'), json.dumps(coco, ensure_ascii=False, indent=4))  # imagePath[:-4] + "_1.json"


def parseXmlFiles(xml_path, json_path):
    for f in os.listdir(xml_path):
        if not f.endswith('.xml'):
            continue
        image_name, _ = os.path.splitext(f)
        size = dict()
        size['width'] = None
        size['height'] = None
        size['depth'] = None

        xml_file = os.path.join(xml_path, f)
        print(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        imagePath = ""
        imageHeight = 0
        imageWidth = 0
        shape_type = "rectangle"
        label = "normal"
        points = [[0, 0], [0, 0]]
        for elem in root:
            if elem.tag == 'folder' or elem.tag == 'filename' or elem.tag == 'source' or elem.tag == 'segmented':
                continue
            elif elem.tag == 'path':
                imagePath = elem.text.encode('utf-8').decode('utf-8')
            elif elem.tag == 'size':
                for subelem in elem:
                    if subelem.tag == 'width':
                        imageWidth = subelem.text.encode('utf-8').decode('utf-8')
                    elif subelem.tag == 'height':
                        imageHeight = subelem.text.encode('utf-8').decode('utf-8')
            elif elem.tag == 'object':
                for subelem in elem:
                    if subelem.tag == 'bndbox':
                        for item in subelem:
                            if item.tag == 'xmin':
                                points[0][0] = int(item.text)
                            if item.tag == 'ymin':
                                points[0][1] = int(item.text)
                            if item.tag == 'xmax':
                                points[1][0] = int(item.text)
                            if item.tag == 'ymax':
                                points[1][1] = int(item.text)
                    elif subelem.tag == 'name':
                        label = subelem.text.encode('utf-8').decode('utf-8')
        toJson(image_name, imageHeight, imageWidth, shape_type, label, points, xml_path, json_path)


if __name__ == '__main__':
    xml_path = 'G:/Public_Data_Sets/多国车牌/老挝/LAO_Anno'  # 这是xml文件所在的地址
    json_path = 'G:/Public_Data_Sets/多国车牌/老挝/json'
    parseXmlFiles(xml_path, json_path)