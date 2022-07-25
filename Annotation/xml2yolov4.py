# coding: utf-8
import xml.etree.ElementTree as ET
import pickle
import shutil
import os
from os import listdir, getcwd
from os.path import join
import glob



# classes = ["xiangmen","xiangtou","topTruckN   umPos","truckhead", "topTruckNumNeg","twoDimensionalCode"]  #车顶号选用
# xml_image_path = "I:/testData/Wood/Third/traindata/traindata"
# xml_save_path = 'I:/testData/Wood/Third/traindata/车头车号检测第三次优化/labels/'
# image_save_path = 'I:/testData/Wood/Third/traindata/车头车号检测第三次优化/images/'
# txt_save_path = 'I:/testData/Wood/Third/traindata/车头车号检测第三次优化/txt/'

# xml_image_path = "I:/testData/Wood/Wood_Final/traindata"
# xml_save_path = 'I:/testData/Wood/Wood_Final/TruckNum_Final/labels/'
# image_save_path = 'I:/testData/Wood/Wood_Final/TruckNum_Final/images/'
# txt_save_path = 'I:/testData/Wood/Wood_Final/TruckNum_Final/txt/'

# xml_image_path = "I:/testData/Wood/Wood_Final/traindata"
# xml_save_path = 'I:/testData/Wood/Wood_Final/WoodNum_Final/labels/'
# image_save_path = 'I:/testData/Wood/Wood_Final/WoodNum_Final/images/'
# txt_save_path = 'I:/testData/Wood/Wood_Final/WoodNum_Final/txt/'

xml_image_path = "G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_en"
xml_save_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/labels/'
image_save_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/images/'
txt_save_path = 'G:/Public_Data_Sets/大铲湾岸桥/车顶号/车顶车架20211214最终整合版/DachanwanRoofNum_Final/txt/'

# classes = ["TopNum","SideNum","Wood"]
# classes = ["horizon","vertical",'topPos','topNeg','breakage','door_small_box','qianfen','qianfen_Locked','tank','reefer','electronic_shut',
           # 'spreader','containerbody','container_corner_pos','dangerous']
# classes = ['Wood']   # 原木检测
# classes = ["TruckHead","SideNum"]

classes = ['xiangmen', 'xiangtou', 'topTruckNumPos', 'truckhead', 'topTruckNumNeg', 'twoDimensionalCode', 'chejia', 'tailTruckNum']   # 大铲湾车顶号

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


# def convert_annotation(image_name):
#     if os.path.exists(xml_path+image_name[:-3] + 'xml'):
#         in_file = open(xml_path + image_name[:-3] + 'xml',encoding = 'UTF-8-sig')  # xml文件路径
#     else:
#         os.remove(xml_path + image_name)
#     if os.path.exists(txtsaved_path):
#         out_file = open(txtsaved_path + image_name[:-3] + 'txt', 'w', encoding = 'UTF-8')  # 转换后的txt文件存放路径
#         f = open(xml_path + image_name[:-3] + 'xml',"r", encoding = 'UTF-8-sig')
#         xml_text = f.read()
#         # print(xml_text)
#         root = ET.fromstring(xml_text)
#         f.close()
#         size = root.find('size')
#         w = int(size.find('width').text)
#         h = int(size.find('height').text)
#
#
#         for obj in root.iter('object'):
#             cls = obj.find('name').text
#             # #此处输出cls出现编码的\uffef问题，为解码方式存在错误会在头文件里出现bom字符，解决办法就是先编码utf8再解utf8sig即可
#             # clse = cls.encode('utf-8').decode('utf-8-sig')
#             # if clse == 'TopNum#11100':
#             #     clse = 'SideNum#11100'
#             #     print(image_name)
#             # clsa = cls.split('#')[0]
#             clsa = cls.encode('utf-8').decode('utf-8-sig').split('#')[0]
#             if clsa not in classes:
#                 print(clsa)
#                 continue
#             cls_id = classes.index(clsa)
#             xmlbox = obj.find('bndbox')
#             b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
#                  float(xmlbox.find('ymax').text))
#             bb = convert((w, h), b)
#             out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
#
#
#     else:
#         os.makedirs(txtsaved_path)


def convert_annotation(image_name):
    try:
        shutil.copy2(os.path.join(xml_image_path, image_name + '.jpg'), os.path.join(image_save_path, image_name + '.jpg'))
        shutil.copy2(os.path.join(xml_image_path, image_name + '.xml'), os.path.join(xml_save_path, image_name + '.xml'))
        if os.path.exists(txt_save_path):
            out_file = open(os.path.join(txt_save_path, image_name + '.txt'), 'w', encoding = 'UTF-8')  # 转换后的txt文件存放路径
            f = open(os.path.join(xml_image_path, image_name + '.xml'),"r", encoding = 'UTF-8-sig')
            xml_text = f.read()
            # print(xml_text)
            root = ET.fromstring(xml_text)
            f.close()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)


            for obj in root.iter('object'):
                cls = obj.find('name').text
                # #此处输出cls出现编码的\uffef问题，为解码方式存在错误会在头文件里出现bom字符，解决办法就是先编码utf8再解utf8sig即可
                # clse = cls.encode('utf-8').decode('utf-8-sig')
                # if clse == 'TopNum#11100':
                #     clse = 'SideNum#11100'
                #     print(image_name)
                # clsa = cls.split('#')[0]
                clsa = cls.encode('utf-8').decode('utf-8-sig').split('#')[0]
                if clsa not in classes:
                    # print(clsa)
                    continue
                cls_id = classes.index(clsa)
                if cls_id == 4:
                    print(image_name)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
            return (image_name + '.jpg')
        else:
            os.makedirs(txt_save_path)
            txt = ''
            return txt
    except:
        os.remove(os.path.join(xml_image_path, image_name + '.xml'))
        print(image_name + '.xml')


wd = getcwd()

if __name__ == '__main__':
    total_txt_list = []
    for file in os.listdir(xml_image_path):
        file_name, suffix = os.path.splitext(file)
        # print(suffix)
        if suffix == '.xml':
            txt_file = convert_annotation(file_name)
            total_txt_list.append(txt_file)
    # for image_path in glob.glob(xml_image_path):  # 每一张图片都对应一个xml文件这里写xml对应的图片的路径
    #     image_name = image_path.split('\\')[-1]
    #     convert_annotation(image_name)

        # #删除为空的txt结果
        # if not os.path.getsize(txtsaved_path + image_name.split('.')[0] + '.txt'):
        #     os.remove(txtsaved_path + image_name.split('.')[0] + '.txt')
