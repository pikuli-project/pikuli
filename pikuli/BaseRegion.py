# -*- coding: utf-8 -*-

"""
   BaseRegion - rectangle screen area defines with top-left corner coordinates, width and height.
   BaseRegion don't have any information in visual content on screen.
   Content can be defined using .find() or .findAll() methods, implemented in the descendant class
"""

import cv2
import numpy as np
import platform
from Location import Location
from logger import PikuliLogger
from common_exceptions import FailExit, FindFailed

current_platform = platform.system()

if current_platform == 'Darwin':
    from display_mac import Display
elif current_platform == 'Windows':
    from display_win import Display
else:
    raise NotImplementedError

DELAY_BETWEEN_CV_ATTEMPT = 1.0  # delay between attempts of recognition
DEFAULT_FIND_TIMEOUT = 3.1
logger = PikuliLogger('pikuli.Region  ').logger


class BaseRegion(object):
    def __init__(self, *args, **kwargs):
        """
        Option 1:
            args[0]:
                Region object
                or Screen - whole screen

        Option 2:
            args[0:4] == [x, y, w, h]:
                integers - x,y coordinates, width w, height h;
                           A new rectangle area will build.
                           Area borders belongs to area

        kwargs can contain:
            title        - human-readable id (string)
            id           - id for use in code
            find_timeout - default value used for find() method
                           if don't pass to constructor a DEFAULT_FIND_TIMEOUT will use.
        """

        self.display = Display()
        self.scaling_factor = self.display.get_monitor_info(1)[-1]
        self.drag_location = None
        self.relations = ['top-left', 'center']
        (self.x, self.y, self.w, self.h) = (None, None, None, None)
        self.screen_number = 1
        self._last_match = None

        # human-readable id
        self.title = str(kwargs.get('title', 'New Region'))

        # internal id
        self._id = kwargs.get('id', 0)

        try:
            self.set_rect(*args, **kwargs)
        except FailExit:
            raise FailExit('Incorrect Region class constructor call:\n\targs = {args}\n\tkwargs = {kwargs}'.format(
                           args=args, kwargs=kwargs))

        self._find_timeout = self._verify_timeout(
            kwargs.get('find_timeout', DEFAULT_FIND_TIMEOUT),
            err_msg='pikuli.{}'.format(type(self).__name__))
        logger.debug('New Region with name "{name}" created (x:{x} y:{y} w:{w} h:{h} timeout:{t})'.format(
                     name=self.title, x=self.x, y=self.y, w=self.w, h=self.h, t=self._find_timeout))

    def __str__(self):
        return 'Region "%s" (%i, %i, %i, %i)' % (self.title, self.x, self.y, self.w, self.h)

    @staticmethod
    def _verify_timeout(timeout, allow_none=False,
                        err_msg='pikuli.verify_timeout_argument()'):
        if not timeout and allow_none:
            return None
        try:
            timeout = float(timeout)
            if timeout < 0:
                raise ValueError
        except(ValueError, TypeError) as ex:
            raise FailExit('{msg}: wrong timeout = "{t}" ({ex})'.format(
                msg=err_msg, t=timeout, ex=str(ex)))
        return timeout

    def get_id(self):
        return self._id

    def set_id(self, _id):
        self._id = _id

    def set_x(self, x, relation='top-left'):
        """ 'top-left' -- x - top-left corner coordinate;
            'center'   -- x - center coordinate
        """
        if isinstance(x, int) and relation in self.relations:
            if relation is None or relation == 'top-left':
                self.x = x
            elif relation == 'center':
                self.x = x - int(self.w / 2)
        else:
            raise FailExit('Incorrect Region.set_x() method call:\n\tx = {x}, {type_x}\n\trelation = {r}'.format(
                           x=x, type_x=type(x), r=relation))

    def set_y(self, y, relation='top-left'):
        """ 'top-left' -- y - top-left corner coordinate;
            'center'   -- y - center coordinate
        """
        if isinstance(y, int) and relation in self.relations:
            if relation is None or relation == 'top-left':
                self.y = y
            elif relation == 'center':
                self.y = y - int(self.h / 2)
        else:
            raise FailExit('Incorrect Region.set_y() method call:\n\ty = {y}, {type_y}\n\trelation = {r}'.format(
                           y=y, type_y=type(y), r=relation))

    def set_w(self, w, relation='top-left'):
        if isinstance(w, int) and w > 0 and relation in self.relations:
            if relation == 'center':
                self.x += int((self.w - w) / 2)
            self.w = w
        else:
            raise FailExit('Incorrect Region.set_w() method call:\n\tw = {w}, {type_w}\n\trelation = {r}'.format(
                           w=w, type_w=type(w), r=relation))

    def set_h(self, h, relation='top-left'):
        if isinstance(h, int) and h > 0 and relation in self.relations:
            if relation == 'center':
                self.y += int((self.h - h) / 2)
            self.h = h
        else:
            raise FailExit('Incorrect Region.set_h() method call:\n\th = {h}, {type_h}\n\trelation = {r}'.format(
                           h=h, type_h=type(h), r=relation))

    def set_rect(self, *args, **kwargs):
        try:
            if len(args) == 4 and \
                    isinstance(args[0], int) and \
                    isinstance(args[1], int) and \
                    isinstance(args[2], int) and \
                    isinstance(args[3], int) and \
                    args[2] > 0 and args[3] > 0:
                relation = kwargs.get('relation', 'top-left') or 'top-left'

                self.w = args[2]
                self.h = args[3]
                if relation == 'top-left':
                    self.x = args[0]
                    self.y = args[1]
                elif relation == 'center':
                    self.x = args[0] - int(self.w / 2)
                    self.y = args[1] - int(self.h / 2)
            elif len(args) == 1:
                self._set_from_region(args[0])
            else:
                raise FailExit()

        except FailExit as e:
            raise FailExit('Incorrect Region.set_rect() method call:'
                           '\n\targs = {args}\n\tkwargs = {kwargs}\n\terror message: {msg}'.format(
                               args=str(args), kwargs=str(kwargs), msg=str(e)))

    def _set_from_region(self, reg):
        try:
            self.x = reg.x
            self.y = reg.y
            self.w = reg.w
            self.h = reg.h
            self._find_timeout = reg.get_find_timeout()
        except Exception as ex:
            raise FailExit(str(ex))

    def get_top_left(self, x_offs=0, y_offs=0):
        return Location(self.x + x_offs,
                        self.y + y_offs,
                        title='Top left corner of {}'.format(self.title))

    def get_top_right(self, x_offs=0, y_offs=0):
        return Location(self.x + x_offs + self.w,
                        self.y + y_offs,
                        title='Top right corner of {}'.format(self.title))

    def get_bottom_left(self, x_offs=0, y_offs=0):
        return Location(self.x + x_offs,
                        self.y + y_offs + self.h,
                        title='Bottom left corner of {}'.format(self.title))

    def get_bottom_right(self, x_offs=0, y_offs=0):
        return Location(self.x + x_offs + self.w,
                        self.y + y_offs + self.h,
                        title='Bottom right corner of {}'.format(self.title))

    def get_center(self, x_offs=0, y_offs=0):
        return Location((self.x + x_offs + int(self.w / 2)),
                        (self.y + y_offs + int(self.h / 2)),
                        title='Center of {}'.format(self.title))

    @property
    def center(self):
        return self.get_center()

    def click(self, x_offs=0, y_offs=0):
        self.get_center(x_offs=x_offs, y_offs=y_offs).click()

    @property
    def search_area(self):
        return self.display.take_screenshot(self.x, self.y, self.w, self.h, None)

    def save_as_jpg(self, full_filename):
        cv2.imwrite(full_filename, self.display.take_screenshot(self.x, self.y, self.w, self.h),
                    [cv2.IMWRITE_JPEG_QUALITY, 70])

    def save_as_png(self, full_filename):
        cv2.imwrite(full_filename, self.display.take_screenshot(self.x, self.y, self.w, self.h))

    def _find(self, ps, field):
        res = cv2.matchTemplate(field, ps.cv2_pattern, cv2.TM_CCORR_NORMED)
        loc = np.where(res > ps.similarity)  # 0.995
        return map(lambda x, y, s: (int(x + self.x * self.scaling_factor),
                                    int(y + self.y * self.scaling_factor),
                                    float(s)),
                   loc[1], loc[0], res[loc[0], loc[1]])

    def get_last_match(self):
        if not self._last_match or self._last_match == []:
            raise FindFailed('_last_match() is empty')
        return self._last_match

    def set_find_timeout(self, timeout):
        if not timeout:
            self._find_timeout = DEFAULT_FIND_TIMEOUT
        else:
            self._find_timeout = \
                self._verify_timeout(
                    timeout, err_msg='Incorrect Region.set_find_timeout() method call')

    def get_find_timeout(self):
        return self._find_timeout
