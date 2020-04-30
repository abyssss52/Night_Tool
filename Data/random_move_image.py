# ------------------------------------------------------------------------------
# Copyright (c) Abyssss
# Licensed under the MIT License.
# For moving image randomly
# ------------------------------------------------------------------------------

import shutil
import random
import os
import argparse




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Random Moving Images')
    parser.add_argument('--ori_images_path', default='/home/night/Datasets/face/face_mask/incorrect_image', type=str,
                        help='The path of original images')
    parser.add_argument('--new_images_path', default='/home/night/Datasets/face/face_mask/train/face', type=str,
                        help='The new path of those images')
    parser.add_argument('--img_num', default=871, type=int, help='The number of images I need to move.')

    args = parser.parse_args()

    image_path = args.ori_images_path
    new_image_path = args.new_images_path
    image_list = os.listdir(image_path)
    random.shuffle(image_list)

    for i in range(args.img_num):
        shutil.move(os.path.join(image_path,image_list[i]), new_image_path)
