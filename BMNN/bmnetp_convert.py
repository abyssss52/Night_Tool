#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：bmnetp_convert.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/5/19
'''

import bmnetp
## compile fp32 model
bmnetp.compile(
    model = "/yolox/Wood/Wood_yolox_l_coco.pt", ## Necessary
    outdir = "xxx", ## Necessary
    target = "BM1684", ## Necessary
    shapes = [[1,3,640,640]], ## Necessary
    net_name = "yolox_l", ## Necessary
    opt = 2, ## optional, if not set, default equal to 1
    dyn = False, ## optional, if not set, default equal to False
    cmp = True, ## optional, if not set, default equal to True
    enable_profile = True ## optional, if not set, default equal to False
)