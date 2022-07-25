#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：Dynamic_object_detection.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/2/9
'''

import numpy as np
import cv2
import time
import datetime


video_path = 'G:/Image_Composite_Editor/Cache/20211224133512_f05359ba10f64c4e9ed6ee584b63c375.mp4'
cap = cv2.VideoCapture(video_path)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(30,30))
fgbg = cv2.createBackgroundSubtractorMOG2(history = 100, varThreshold = 16, detectShadows=False)
fgmask = np.zeros((640,480))
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame1 = np.zeros((640,480))
# out = cv2.VideoWriter(datetime.datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S%p")+'.avi',fourcc, 5.0, np.shape(frame1))

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    for c in contours:
        Area = cv2.contourArea(c)
        if Area < maxArea :
        # if cv2.contourArea(c) < 500:
            (x, y, w, h) = (0,0,0,0)
            continue
        else:
            if Area < 1000:
                (x, y, w, h) = (0,0,0,0)
                continue
            else:
                maxArea = Area
                m=c
                # (x, y, w, h) = cv2.boundingRect(m)
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # out.write(frame)
    cv2.imshow('frame',frame)
    cv2.imshow('result', fgmask)
    k = cv2.waitKey(30)&0xff
    if k==27:
        break
# out.release()
cap.release()
cv2.destoryAllWindows()
