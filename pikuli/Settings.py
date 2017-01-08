# -*- coding: utf-8 -*-

import os
import sys
import tempfile
from logger import PikuliLogger

logger = PikuliLogger('pikuli.Settings').logger


class Settings(object):

    def __init__(self):
        # Paths to images
        self.IMG_ADDITION_PATH = []
        # 0.995 is enough for stability.
        # 0.700 will find in every pixel
        self.min_similarity = 0.995
        self.use_api_for_screenshots = True
        defvals = self.__get_default_values()
        for k in defvals:
            setattr(self, k, defvals[k])
        self.find_failed_dir = os.path.join(tempfile.gettempdir(), 'pikuli_find_failed')
        if not os.path.isdir(self.find_failed_dir):
            os.makedirs(self.find_failed_dir)

    def __get_default_values(self):
        defvals = {}
        for attr in dir(self):
            if '_Settings__def_' in attr:
                defvals[attr.split('_Settings__def_')[-1]] = getattr(self, attr)
        return defvals

    def add_image_path(self, path):
        if path not in self.IMG_ADDITION_PATH:
            self.IMG_ADDITION_PATH.append(path)

    def list_image_path(self):
        for path in self.IMG_ADDITION_PATH:
            yield path

    def set_find_failed_dir(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                raise Exception('pikuli: can not set Settings.FindFailedDir to "%s"'
                                '-- failed to create directory.' % str(path))
        self.find_failed_dir = path

    def get_find_failed_dir(self):
        return self.find_failed_dir


settings = Settings()

try:
    settings.add_image_path(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)))
except AttributeError:
    logger.warning('unable to set default image path. You should use absolute paths')
