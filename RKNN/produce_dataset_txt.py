import os
data_path = '/home/night/PycharmProjects/RKNN/mobilenetv2/data'
image_list = os.listdir(data_path)
with open('/home/night/PycharmProjects/RKNN/mobilenetv2/data/dataset.txt', 'w') as f:
    for image in image_list:
        f.write(image)
        f.write('\n')