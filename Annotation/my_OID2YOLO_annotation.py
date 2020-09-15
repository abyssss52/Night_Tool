import os
import argparse


def convert_OID_annotation(data_path, anno_path):
    classes = ['human face']
    bbox_num = 0

    for i in classes:
        images_path = os.path.join(data_path, 'Clothing')
        images = os.listdir(images_path)

        images.remove('Label')  # 去文件中文件夹的名称

        with open(anno_path, 'a') as f:
            for image in images:
                image_path = os.path.join(images_path, image)
                annotation = image_path
                img_name, img_type = os.path.splitext(image)  # 分割文件名和文件格式
                label_path = os.path.join(images_path, 'Label', img_name + '.txt')
                with open(label_path, 'r') as l:
                    lines = l.readlines()
                    bboxes = [line.strip().split(' ')[len(i.split(' ')):] for line in lines]
                    for bbox in bboxes:
                        class_idx = classes.index(i)
                        annotation += ' ' + ','.join(
                            [str(int(float(bbox[0])+0.5)), str(int(float(bbox[1])+0.5)), str(int(float(bbox[2])+0.5)), str(int(float(bbox[3])+0.5)),
                             str(class_idx)])            # tensorflow-yolov3
                        bbox_num += 1
                        # annotation += ' ' + ' '.join(
                        #     [str(class_idx), str(round(float(bbox[0]))), str(round(float(bbox[1]))), str(round(float(bbox[2]))),
                        #      str(round(float(bbox[3])))])  # YOLOv3_tinyTensorFlow
                print(annotation)
                f.write(annotation + "\n")
        return len(images), bbox_num


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/home/night/PycharmProjects/Data/OID/Dataset/")
    # parser.add_argument("--train_annotation", default="/home/night/PycharmProjects/Data/OID/OIDv4_train.txt")
    # parser.add_argument("--test_annotation",  default="/home/night/PycharmProjects/Data/OID/OIDv4_test.txt")
    parser.add_argument("--train_annotation", default="/home/night/PycharmProjects/Object_Detection/tensorflow-yolov3-change/data/dataset/OIDv4_clothing_train.txt")
    parser.add_argument("--test_annotation",  default="/home/night/PycharmProjects/Object_Detection/tensorflow-yolov3-change/data/dataset/OIDv4_clothing_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    train_img_num, train_bbox_num = convert_OID_annotation(os.path.join(flags.data_path, 'train'), flags.train_annotation)
    test_img_num, test_bbox_num = convert_OID_annotation(os.path.join(flags.data_path, 'validation'), flags.test_annotation)
    print('=> The number of image for train is: %d\tThe number of bbox for train is:%d\nThe number of image for test is:%d\tThe number of bbox for test is:%d' %(train_img_num, train_bbox_num, test_img_num, test_bbox_num))





