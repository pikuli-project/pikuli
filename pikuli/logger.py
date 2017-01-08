# -*- coding: utf-8 -*-

import logging


class PikuliLogger(object):
    def __init__(self, name=__name__, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('~# %(asctime)s %(levelname)s %(name)s: %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
