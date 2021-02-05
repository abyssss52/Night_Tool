#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File         :   NMS.py
@Modify Time  :   2021/2/5 上午11:34
@Author       :   night
@Version      :   1.0
@License      :   (C)Copyright 2019-2021, Real2tech
@Desciption   :   None

'''

import numpy as np

def nms(boxes, scores, iou_threshold, max_output_size, soft_nms=False):
    keep = []
    order = scores.argsort()[::-1]  # 按得分从大到小排序
    num = boxes.shape[0]
    suppressed = np.zeros((num), dtype=np.int)  # 抑制
    for _i in range(num):
        if len(keep) >= max_output_size:
            break
        i = order[_i]
        if suppressed[i] == 1:
            continue
        keep.append(i)
        ####boxes左上和右下角坐标####
        xi1 = boxes[i, 0]
        yi1 = boxes[i, 1]
        xi2 = boxes[i, 2]
        yi2 = boxes[i, 3]
        areas1 = (xi2 - xi1 + 1) * (yi2 - yi1 + 1)  # box1面积
        for _j in range(_i + 1, num):  # start，stop
            j = order[_j]
            if suppressed[i] == 1:
                continue
            xj1 = boxes[j, 0]
            yj1 = boxes[j, 1]
            xj2 = boxes[j, 2]
            yj2 = boxes[j, 3]
            areas2 = (xj2 - xj1 + 1) * (yj2 - yj1 + 1)  # box2面积

            xx1 = np.maximum(xi1, xj1)
            yy1 = np.maximum(yi1, yj1)
            xx2 = np.minimum(xi2, xj2)
            yy2 = np.minimum(yi2, yj2)

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)

            int_area = w * h  # 重叠区域面积

            inter = 0.0

            if int_area > 0:
                inter = int_area * 1.0 / (areas1 + areas2 - int_area)  # IOU
            ###softnms
            if soft_nms:
                sigma = 0.6
                if inter >= iou_threshold:
                    scores[j] = np.exp(-(inter * inter) / sigma) * scores[j]
            ###nms
            else:
                if inter >= iou_threshold:
                    suppressed[j] = 1
    return keep  # 返回保留下来的下标