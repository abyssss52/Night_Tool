#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Night_Tool 
@File ：JSON2Darknet.py
@Author ：night
@license: (C) Copyright 2021-2221, Shenzhen Pingfang Science And Technology Co, Ltd. 
@Date ：2021/11/4
'''

import os
import numpy as np
import cv2
import shutil
import json
import random


class darknetTool():
    def __init__(self, help_=False):
        if help_:
            self.getHelp()

    def getAllImagePath(self, folder, recursion=False):
        expandName = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "bmp", "BMP"]
        imagePathList = []
        if not recursion:
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder, item)):
                    continue
                if item.rsplit(".",1)[-1] in expandName:
                    imagePathList.append(os.path.join(folder, item))
            return imagePathList
        else:
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder, item)):
                    subPathList = self.getAllImagePath(os.path.join(folder, item), True)
                    imagePathList.extend(item for item in subPathList)
                else:
                    if item.rsplit(".",1)[-1] in expandName:
                        imagePathList.append(os.path.join(folder, item))
            return imagePathList

    def getAllJsonFilePath(self, folder):
        jsonPathList = []
        for item in os.listdir(folder):
            if item.rsplit(".",1)[-1] == 'json':
                jsonPathList.append(os.path.join(folder, item))
        return jsonPathList

    def getAllTxtPath(self, folder):
        txtPathList = []
        for item in os.listdir(folder):
            if item.rsplit(".",1)[-1] == 'txt':
                txtPathList.append(os.path.join(folder, item))
        return txtPathList

    def fromJsonFileToSearchImage(self, jsonPathList, imageFolder):
        imagePathList = []
        for item in jsonPathList:
            with open(item, "r", encoding='utf-8') as f:
                jsonData = json.load(f)
                imageName = jsonData["imagePath"].rsplit("\\",1)[-1]
            jsonName = item.rsplit("\\",1)[-1]
            imagePath = os.path.join(imageFolder, imageName)
            # print(imagePath)
            imagePathList.append(imagePath)
        return imagePathList

    def copyAllLabeledImageToNewFolder(self, imagePathList, saveFolder):
        for item in imagePathList:
            imageName = item.rsplit("\\",1)[-1]
            savePath = os.path.join(saveFolder, imageName)
            print("copyAllLabeledImageToNewFolder: srcPath", item)
            print("copyAllLabeledImageToNewFolder: dstPath", savePath)
            shutil.copyfile(item, savePath)

    def renameAllLabeledImageAndTxt(self, txtFolder, labeledImageFolder,  n=5, startN=0):
        # extendName是图像后缀名，n用于zfill(n)，00001.jpg
        i = startN
        imagePathList = self.getAllImagePath(labeledImageFolder)
        if (len(imagePathList[0].split("\\")[-1])-4) == n:
            n += 1
        for imagePath in imagePathList:
            i += 1
            imageName_dst = str(i).zfill(n) + "." + imagePath.rsplit(".",1)[-1]
            image_srcPath = imagePath
            image_dstPath = os.path.join(labeledImageFolder, imageName_dst)
            txtName_src = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] +".txt"
            txtName_dst = str(i).zfill(n) + ".txt"
            txt_srcPath = os.path.join(txtFolder, txtName_src)
            txt_dstPath = os.path.join(txtFolder, txtName_dst)
            try:
                if not os.path.exists(image_dstPath):
                    os.rename(image_srcPath, image_dstPath)
                if not os.path.exists(txt_dstPath):
                    os.rename(txt_srcPath, txt_dstPath)
                print("renameAllLabeledImageAndTxt")
                print("image_srcPath:", image_srcPath)
                print("image_dstPath:", image_dstPath)
                print("txt_srcPath:", txt_srcPath)
                print("txt_dstPath:", txt_dstPath)
            except:
                print("ERROR:renameAllLabeledImageAndTxt error")
                print("image_srcPath:", image_srcPath)
                print("image_dstPath:", image_dstPath)
                print("txt_srcPath:", txt_srcPath)
                print("txt_dstPath:", txt_dstPath)

    def changeLabelFromJsonToTxt(self, jsonPath, txtSaveFolder):
        with open(jsonPath, "r", encoding='utf-8') as f:
            jsonData = json.load(f)
            img_h = jsonData["imageHeight"]
            img_w = jsonData["imageWidth"]
            txtName = jsonPath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
            txtPath = os.path.join(txtSaveFolder, txtName)
            with open(txtPath, "w") as f:
                for item in jsonData["shapes"]:
                    label = item["label"]
                    pt1 = item["points"][0]
                    pt2 = item["points"][1]
                    xCenter = (pt1[0] + pt2[0]) / 2
                    yCenter = (pt1[1] + pt2[1]) / 2
                    obj_h = pt2[1] - pt1[1]
                    obj_w = pt2[0] - pt1[0]
                    f.write(" {} ".format(label))
                    f.write(" {} ".format(xCenter / img_w))
                    f.write(" {} ".format(yCenter / img_h))
                    f.write(" {} ".format(obj_w / img_w))
                    f.write(" {} ".format(obj_h / img_h))
                    f.write(" \n")

    def showLabelFromJson(self, jsonPath, imageFolder):
        cv2.namedWindow("img", 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        with open(jsonPath, "r") as f:
            jsonData = json.load(f)
            imageName = jsonData["imagePath"].rsplit("\\",1)[-1]
            imagePath = os.path.join(imageFolder, imageName)
            img = cv2.imread(imagePath)
            print("showLabelFromJson: image path:", imagePath)
            for item in jsonData["shapes"]:
                label = item["label"]
                p1 = (int(item["points"][0][0]), int(item["points"][0][1]))
                p2 = (int(item["points"][1][0]), int(item["points"][1][1]))
                cv2.putText(img, label, (p1[0], p1[1] - 10), font, 1.2, (0, 0, 255), 2)
                cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
                cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyWindow("img")

    def showLabelFromTxt(self, imagePath, txtFolder):
        # label xcenter ycenter w h
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("showLabelFromTxt: image path:", imagePath)
        img = cv2.imread(imagePath)
        h, w = img.shape[:2]
        cv2.namedWindow("img", 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        with open(txtPath, "r") as f:
            lines = f.readlines()
            for line in lines:
                tempL = line.split(" ")
                label = tempL[1]
                obj_w = float(tempL[7])
                obj_h = float(tempL[9])
                topLeftx = (float(tempL[3]) - obj_w / 2) * w
                topLefty = (float(tempL[5]) - obj_h / 2) * h
                bottomRightx = (float(tempL[3]) + obj_w / 2) * w
                bottomRighty = (float(tempL[5]) + obj_h / 2) * h
                p1 = (int(topLeftx), int(topLefty))
                p2 = (int(bottomRightx), int(bottomRighty))
                cv2.putText(img, label, (p1[0], p1[1] - 10), font, 1.2, (0, 255, 255), 2)
                cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
                cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyWindow("img")

    def imageAugment_smooth(self, imagePath, txtFolder, labeledImageFolder,n=5):
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("smooth: image path:", imagePath)
        img = cv2.imread(imagePath)
        imageName_smooth = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_smooth." + imagePath.rsplit(".",1)[-1]
        imagePath_smooth = os.path.join(labeledImageFolder, imageName_smooth)#平滑图像保存路径
        txtName_smooth = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_smooth.txt"
        txtPath_smooth = os.path.join(txtFolder, txtName_smooth)#标签保存路径
        shutil.copyfile(txtPath, txtPath_smooth)
        print("imageAugment_smooth: source txtPath", txtPath)
        print("imageAugment_smooth: dst txtPath", txtPath_smooth)
        print("imageAugment_smooth: source imagePath", imagePath)
        print("imageAugment_smooth: dst imagePath", imagePath_smooth)
        dst = cv2.blur(img, (n, n))
        cv2.imwrite(imagePath_smooth, dst)

    def imageAugment_flip(self, imagePath, txtFolder, labeledImageFolder,flag=0):
        # flag = 0水平翻转 flag = 1，竖直翻转, flag=2 水平翻转+竖直翻转
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("imageAugment_flip: image path:", imagePath)
        img = cv2.imread(imagePath)
        if flag == 0:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipx." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipx.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)
        elif flag == 1:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipy." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipy.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)
        elif flag == 2:
            imageName_flip = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_flipxy." + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
            imagePath_flip = os.path.join(labeledImageFolder, imageName_flip)
            txtName_flip = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_flipxy.txt"
            txtPath_flip = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_flip)

        # 打开原来的txt标签文件，修改原来的x坐标为 xcenter’= 1 - xcenter
        with open(txtPath, "r") as fsrc:
            with open(txtPath_flip, "w") as f:
                lines = fsrc.readlines()
                for line in lines:
                    temp = line.split(" ")
                    label, xcenter, ycenter, objw, objh = temp[1], temp[3], temp[5], temp[7], temp[9]
                    if flag == 0:
                        xcenter = 1 - float(xcenter)
                    elif flag == 1:
                        ycenter = 1 - float(ycenter)
                    elif flag == 2:
                        xcenter = 1 - float(xcenter)
                        ycenter = 1 - float(ycenter)
                    f.write(" {} ".format(label))
                    f.write(" {} ".format(xcenter))
                    f.write(" {} ".format(ycenter))
                    f.write(" {} ".format(objw))
                    f.write(" {} ".format(objh))
                    f.write(" \n")
        if flag == 0:
            dst = cv2.flip(img, 1)
        elif flag == 1:
            dst = cv2.flip(img, 0)
        elif flag == 2:
            dst = cv2.flip(img, 1)
            dst = cv2.flip(dst, 0)
        cv2.imwrite(imagePath_flip, dst)

    def imageAugment_gamma(self, imagePath, txtFolder, labeledImageFolder,gamma=2):
        txtName = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + ".txt"
        txtPath = os.path.join(txtFolder, txtName)
        print("imageAugment_gamma: image path:", imagePath)
        img = cv2.imread(imagePath)
        imageName_gamma = imagePath.rsplit("\\",1)[-1].rsplit(".",1)[0] + "_gamma{}.".format(gamma) + imagePath.rsplit("\\",1)[-1].rsplit(".",1)[-1]
        imagePath_gamma = os.path.join(labeledImageFolder, imageName_gamma)
        txtName_gamma = txtPath.rsplit("\\",1)[-1].split(".txt")[0] + "_gamma{}.txt".format(gamma)
        txtPath_gamma = os.path.join(txtPath.rsplit("\\",1)[0:-1][0], txtName_gamma)
        shutil.copyfile(txtPath, txtPath_gamma)
        print("source txtPath", txtPath)
        print("dst txtPath", txtPath_gamma)
        print("source imagePath", imagePath)
        print("dst imagePath", imagePath_gamma)
        table = []
        for i in range(256):
            table.append(((i / 255.0) ** gamma) * 255)
        table = np.array(table).astype("uint8")
        dst = cv2.LUT(img, table)
        cv2.imwrite(imagePath_gamma, dst)

    def devideTrainSetAndTestSet(self, imagePathList, saveFolder, prePath="", prop=0.8):
        trainTxt = saveFolder + "/train.txt"
        testTxt = saveFolder + "/test.txt"
        with open(trainTxt, "w") as ftrain:
            with open(testTxt, "w") as ftest:
                for item in imagePathList:
                    imagePath = prePath + item.rsplit("\\",1)[-1]
                    if random.random() < prop:
                        ftrain.write(imagePath)
                        ftrain.write("\n")
                    else:
                        ftest.write(imagePath)
                        ftest.write("\n")

    def getHelp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t ")
        print("parameter：")
        print("\t _\t \t _")
        print("return:")
        print("\t _\t \t _")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t getAllImagePath(folder,recursion=False)")
        print("parameter：")
        print("\t folder:\t \t search path")
        print(
            "\t recursion = False:\t \t default parameters,if recursion = True it will  recursively search the folder")
        print("return:")
        print("\t imagePathLIst\t \t  image file path list")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t getAllJsonPath(self,folder)")
        print("parameter：")
        print("\t folder\t \t folde rcontains json file ")
        print("return:")
        print("\t jsonPathLIst\t \t  json file path list")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t fromJsonFileToSearchImage(jsonPathList,imageFolder,extendName = '.jpg')")
        print("parameter：")
        print("\t jsonPathList \t \t jsonPathList")
        print("\t imageFolder\t \t 存放图片的文件夹")
        print("\t extendName\t \t 图片扩展名")
        print("return:")
        print("\t imagePathList\t \t 标注过的图片的路径")
        print("================================================================================\n")

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Function:\t changeLabelFromJsonToTxt(self,jsonPath,txtSaveFolder)")
        print("txt文件内的保存模式为：label xcenter ycenter width height,坐标全是相对坐标")
        print("parameter：")
        print("\t jsonPath:\t \t json file path")
        print("\t txtSaveFolder\t \t txt file save folder")
        print("return:")
        print("\t None\t \t ")
        print("================================================================================\n")


if __name__ == "__main__":
    rootPath = r"K:\\imageData\\golden_pad\\bonding-balls-dataset\\"
    srcImageFolder = rootPath + "image"# 存放原始图片的文件夹,有标注过的和没标注过的图片
    jsonFolder = rootPath + "label"# labelme标注的json文件保存的文件夹
    labeledImageFolder = rootPath + "/temp/labeledImage"# 筛选出所有标注过的图片
    txtFolder = rootPath +"/temp/txtLabel"# txt文件保存的路径
    objFolder = rootPath +"/temp/obj"# 把图片和对应的txt文件放在一起，可以直接拿去训练的那种
    trainAndTestFileSaveFolder = rootPath +"/temp"
    prePath = "bondingBall/obj/"

    # 创建文件夹
    try:
        if not os.path.exists(labeledImageFolder):
            os.makedirs(labeledImageFolder)
        if not os.path.exists(txtFolder):
            os.makedirs(txtFolder)
        if not os.path.exists(objFolder):
            os.makedirs(objFolder)
    except:
        print("os.makedirs failed!")

    # 初始化类
    tool = darknetTool()

    # 获取所有原始标注文件
    jsonPathList = tool.getAllJsonFilePath(jsonFolder)

    # 从json标签文件复查标注
    # for item in jsonPathList:
    #    tool.showLabelFromJson(item,imageFolder)

    # 从json标注文件查找图片，并保存到labeledImageFolder
    srcLabeledImagePathList = tool.fromJsonFileToSearchImage(jsonPathList, srcImageFolder)
    tool.copyAllLabeledImageToNewFolder(srcLabeledImagePathList, labeledImageFolder)

    # json格式转为txt格式
    for item in jsonPathList:
        tool.changeLabelFromJsonToTxt(item, txtFolder)
    txtPathList = tool.getAllTxtPath(txtFolder)
    # 获取在labeledImageFolder中的图片的路径
    dstLabeledImagePathList = tool.getAllImagePath(labeledImageFolder)

    # 从txt标签文件查看标注结果
    # 所有标注的图片路径都在dstLabeledImagePathList，通过图片路径去找对应的txt文件
    # 所有的txt文件都在txtFolder文件夹下
    # for imagePath in dstLabeledImagePathList:
    #     tool.showLabelFromTxt(imagePath,txtFolder)

    # 数据增强
    # 均值滤波
    for imagePath in dstLabeledImagePathList:
        tool.imageAugment_smooth(imagePath, txtFolder, labeledImageFolder,n=3)  # n=9是滤波核大小
    # 水平翻转
    for imagePath in dstLabeledImagePathList:
        tool.imageAugment_flip(imagePath, txtFolder, labeledImageFolder, flag=0)  # flag=0 水平翻转
    # 竖直翻转
    for imagePath in dstLabeledImagePathList:
        tool.imageAugment_flip(imagePath, txtFolder, labeledImageFolder, flag=1)  # flag=1 竖直翻转
    # 中心对称
    for imagePath in dstLabeledImagePathList:
        tool.imageAugment_flip(imagePath, txtFolder, labeledImageFolder, flag=2)  # flag=2 中心对称
    # gamma变换
    for imagePath in dstLabeledImagePathList:
        #tool.imageAugment_gamma(imagePath, txtFolder, labeledImageFolder, gamma=0.5)
        tool.imageAugment_gamma(imagePath, txtFolder, labeledImageFolder, gamma=0.8)
        tool.imageAugment_gamma(imagePath, txtFolder, labeledImageFolder, gamma=1.2)
        #tool.imageAugment_gamma(imagePath, txtFolder, labeledImageFolder, gamma=2)

    #图片重命名
    # 图片和标签重命名为00001.jpg 00001.txt.......（可选）
    # n=5表示zfill（）的位数，n=5则为00001.jpg...，n=3则为001.jpg....
    tool.renameAllLabeledImageAndTxt(txtFolder, labeledImageFolder,  n=8, startN=0)

    #检查转换的最终结果
    dstLabeledImagePathList = tool.getAllImagePath(labeledImageFolder)
    # for imagePath in dstLabeledImagePathList:
    #     tool.showLabelFromTxt(imagePath,txtFolder)

    #划分训练集和测试集
    imagePathList = tool.getAllImagePath(labeledImageFolder)
    # prePath = "data/obj/"则train.txt文件中的路径就会是data/obj/00001.jpg,data/obj/00002.jpg......
    # prop=0.8表示80%的数据用来训练，其余的做验证集
    tool.devideTrainSetAndTestSet(imagePathList, trainAndTestFileSaveFolder, prePath=prePath, prop=0.9)



