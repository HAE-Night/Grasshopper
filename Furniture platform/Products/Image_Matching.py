import glob
import os

import cv2
import numpy


def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1_ = cv2.resize(image1, size)
    image2_ = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1_)
    sub_image2 = cv2.split(image2_)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


class Image_Matching:
    def __init__(self, img_path):
        self.img_path = img_path

    def multiple_image_matching(self, list_image2):
        img1 = cv2.imread(self.img_path)
        sort_list = []
        for image2 in list_image2:
            if os.path.exists(image2) and os.path.isfile(image2):
                img2 = cv2.imread(image2)
                similarity = classify_hist_with_split(img1, img2)
                if type(similarity) == numpy.ndarray:
                    similarity = similarity[0]
                sort_list.append(similarity)
            else:
                sort_list.append(0)

        return sort_list


if __name__ == '__main__':
    x = Image_Matching(r"E:\Desktop/Snipaste_2023-11-10_10-39-03_WrTrdYd.jpg")
    list_png =[r"E:\Desktop\Snipaste_2023-11-10_10-39-03_WrTrdYd.jpg"]
    print(list_png)
    print(x.multiple_image_matching(list_png))
