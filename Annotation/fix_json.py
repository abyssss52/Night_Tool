#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：fix_json.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2022/7/20
'''

import os
import json
from tqdm import tqdm

json_path ='F:/WXWork/1688854995265824/Cache/File/2022-07/test'
for jsonfile in tqdm(os.listdir(json_path)):

    with open(os.path.join(json_path, jsonfile), 'r') as f:
        jsonData = json.load(f)
        # for item in jsonData["shapes"]:
        #     label = item["label"]
        #     print(label)

    string = json.dumps(jsonData, ensure_ascii=False, indent=4)
    with open(os.path.join(json_path, jsonfile), 'w', encoding='utf-8') as f1:
        f1.write(string)