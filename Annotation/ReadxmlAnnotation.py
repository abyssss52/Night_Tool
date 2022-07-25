#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：ReadxmlAnnotation.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/12/10
'''

import os
import cv2
import xml.dom.minidom
import numpy as np

# img_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/标注车顶车架号/DachanwanRoofNum20211110_all'
# Ann_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/标注车顶车架号/DachanwanRoofNum20211110_all'

img_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/images'
Ann_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/labels'
topNumpath = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/topNum'

# img_path = 'G:/Public_Data_Sets/多国车牌/老挝/老挝/老挝车牌图片3'
# Ann_path = 'G:/Public_Data_Sets/多国车牌/老挝/老挝/老挝车牌图片3'
image_list = os.listdir(img_path)
sorted(image_list)

for image in image_list:
    image_pre, ext = os.path.splitext(image)
    if ext == '.jpg':
        print(image)
        # img = cv2.imread(os.path.join(img_path, image))
        img = cv2.imdecode(np.fromfile(os.path.join(img_path, image), dtype=np.uint8), -1)
        xmlfile = os.path.join(Ann_path, image_pre + '.xml')
        try:
            DomTree = xml.dom.minidom.parse(xmlfile)
            annotation = DomTree.documentElement
            # print('xml')
            filenamelist = annotation.getElementsByTagName('filename')
            filename = filenamelist[0].childNodes[0].data

            image_size = annotation.getElementsByTagName('size')
            image_width = image_size[0].getElementsByTagName('width')[0].childNodes[0].data
            image_height = image_size[0].getElementsByTagName('height')[0].childNodes[0].data

            objectlist = annotation.getElementsByTagName('object')
            num = 0;
            for object in objectlist:
                namelist = object.getElementsByTagName('name')
                # print 'namelist:',namelist
                objectname = namelist[0].childNodes[0].data.encode('utf-8').decode('utf-8-sig')

                bndbox = object.getElementsByTagName('bndbox')
                for box in bndbox:
                    x1_list = box.getElementsByTagName('xmin')
                    x1 = int(x1_list[0].childNodes[0].data)
                    y1_list = box.getElementsByTagName('ymin')
                    y1 = int(y1_list[0].childNodes[0].data)
                    x2_list = box.getElementsByTagName('xmax')
                    x2 = int(x2_list[0].childNodes[0].data)
                    y2_list = box.getElementsByTagName('ymax')
                    y2 = int(y2_list[0].childNodes[0].data)
                    # 展示标注框
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    # cv2.putText(img, objectname, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
                    # 截取标注框
                    if (objectname.split('#')[0] == "topTruckNumNeg"):
                        # crop_img = img[y1:y2, x1:x2, :]
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.imencode('.jpg', img)[1].tofile(os.path.join(topNumpath, image_pre + '_' + str(num) + '.jpg'))
            # 展示标注框
            # img = cv2.resize(img, (960,540))
            # cv2.imshow('result', img)
            # cv2.waitKey(0)
        except:
            cv2.imshow('result', img)
            cv2.waitKey(0)
        # objectlist = annotation.getElementsByTagName('object')


    else:
        pass