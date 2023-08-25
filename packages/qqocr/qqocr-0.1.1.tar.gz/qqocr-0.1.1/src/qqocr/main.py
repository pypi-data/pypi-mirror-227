import cv2
import numpy as np
import os
import dill

from typing import Callable
from collections import defaultdict


def cal_diff(image1, image2):
    image_and = cv2.bitwise_and(image1, image2)
    return np.sum(image_and) / np.sum(image2)

def split(binary):
    char_list = []
    canvas = np.zeros_like(binary)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 or h > 15:
            char_image = binary[y:y + h, x:x + w]
            canvas[y:y + h, x:x + w] = binary[y:y + h, x:x + w]
            char_list.append((cv2.resize(char_image, (50, 50)), x))

    char_list.sort(key=lambda c: c[1])
    char_list = tuple(zip(*char_list))[0]
    return char_list


class QQOcr:
    model = {'data': defaultdict(list), 'function': None}
    dataset = None
    binary_function = None

    def set_binary(self, function: Callable):
        """设置二值化方法"""
        self.binary_function = function

    def load_dataset(self, dir_path: str):
        """加载数据集"""
        assert os.path.isdir(dir_path)

        images = [(cv2.imread(os.path.join(dir_path, filename)), filename)
                  for filename in os.listdir(dir_path)
                  if not filename.endswith('.txt')]

        with open(os.path.join(dir_path, 'label.txt'), 'r') as file:
            labels = {line.strip().split('\t')[0]: line.strip().split('\t')[1]
                      for line in file.readlines()}

        self.dataset = [(image, labels[filename]) for image, filename in images]

    def learn(self, equalization=True):
        assert self.dataset is not None

        if self.binary_function is not None:
            for image, label in self.dataset:
                binary = self.binary_function(image)
                char_list = split(binary)
                for char_image, char in zip(char_list, label):
                    self.model['data'][char].append(char_image)
        else:
            raise RuntimeError('The split and binary methods cannot both be None.')

        if equalization:
            for char in self.model['data'].keys():
                canvas = np.zeros((50, 50), np.uint64)
                for image in self.model['data'][char]:
                    canvas += image

                canvas = np.floor_divide(canvas, len(self.model['data'][char]))
                canvas = np.uint8(canvas)
                self.model['data'][char] = canvas

    def save_model(self, path: str):
        assert path.endswith('.qmodel')

        self.model['function'] = self.binary_function
        with open(path, 'wb') as file:
            dill.dump(self.model, file)

    def load_model(self, path: str):
        assert path.endswith('.qmodel')

        with open(path, 'rb') as file:
            self.model = dill.load(file)

    def predict(self, image):
        binary = self.model['function'](image)
        char_list = split(binary)
        predict_list = []
        for char_image in char_list:
            predict_char, max_score = '', 0
            for char in self.model['data'].keys():
                templ = self.model['data'][char]
                score = cal_diff(char_image, templ)
                if score > max_score:
                    predict_char, max_score = char, score
            predict_list.append(predict_char)
        return ''.join(predict_list)



