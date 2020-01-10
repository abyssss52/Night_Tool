from pycocotools.coco import COCO
import numpy as np
import requests
from io import BytesIO
import matplotlib.pyplot as plt
# mpl.use('Agg')
from PIL import Image

# 注释地址
annotation_file = "/home/night/PycharmProjects/Data/COCO/annotations_trainval2017/annotations/person_keypoints_val2017.json"
coco = COCO(annotation_file)

# 通过输入类别的名字、大类的名字或是种类的id，来筛选得到图片所属类别的id
CatIds = coco.getCatIds(catNms=['person'])

# 通过图片的id或是所属种类的id得到图片的id
imgIds = coco.getImgIds(catIds=CatIds)

# 该种类的图片数量
imgs_num = len(imgIds)
print(imgs_num)

# 得到图片的id信息后，就可以用loadImgs得到图片的信息了
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]
print(img)

# 从flickr下载图片，展示出来
response = requests.get(img['flickr_url'])
image = Image.open(BytesIO(response.content))
plt.imshow(image)
plt.axis('off')
# plt.show()


# 通过注释的id，得到注释的信息
annIds = coco.getAnnIds(imgIds=img['id'], catIds=CatIds, iscrowd=False)
anns = coco.loadAnns(annIds)
for annotation in anns:
    if annotation['num_keypoints'] != 0:
        print(annotation['keypoints'])
        print(annotation['num_keypoints'])
coco.showAnns(anns)
plt.show()