# -*- coding: utf-8 -*-

"""
   Patten - object represent images using for search
"""

import os
from Settings import settings
from common_exceptions import FailExit
import cv2


class Pattern(object):
    def __init__(self, img_path, similarity=None):
        (self.__similarity, self.__img_path) = (None, None)
        img_path = str(img_path)

        try:
            _path = os.path.abspath(img_path)
            if os.path.exists(_path) and os.path.isfile(_path):
                self.__img_path = _path
            else:
                for _path in settings.list_image_path():
                    _path = os.path.join(_path, img_path)
                    if os.path.exists(_path) and os.path.isfile(_path):
                        self.__img_path = _path
                        break
            if not self.__img_path:
                raise FailExit('image file "{}" not found'.format(_path))

            if not similarity:
                self.__similarity = settings.min_similarity
            elif isinstance(similarity, float) and 0.0 < similarity <= 1.0:
                self.__similarity = similarity
            else:
                raise FailExit('error around "similarity" parameter')

        except FailExit as e:
            raise FailExit('Incorect Pattern class constructor call:\n    img_path = %s'
                           '\n    abspath(img_path) = %s\n    similarity = %s\n    message: %s' %
                           (str(img_path), str(self.__img_path), str(similarity), str(e)))

        self.cv2_pattern = cv2.imread(self.__img_path)
        self.w = int(self.cv2_pattern.shape[1])
        self.h = int(self.cv2_pattern.shape[0])

    def __str__(self):
        return 'Pattern of "%s" with similarity = %f' % (self.__img_path, self.__similarity)

    def similar(self, similarity):
        return Pattern(self.__img_path, similarity)

    def exact(self):
        return Pattern(self.__img_path, 1.0)

    def get_filename(self, full_path=True):
        if full_path:
            return self.__img_path
        else:
            return os.path.basename(self.__img_path)

    @property
    def similarity(self):
        return self.__similarity

    @property
    def get_w(self):
        return self.w

    @property
    def get_h(self):
        return self.h
