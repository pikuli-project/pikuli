# -*- coding: utf-8 -*-

import time
from pikuli.common_exceptions import FailExit
from pikuli.logger import PikuliLogger

DELAY_AFTER_MOUSE_MOVEMENT = 0.050
DELAY_IN_MOUSE_CLICK = 0.100
DELAY_IN_SCROLL = 0.005
DELAY_MOUSE_DOUBLE_CLICK = 0.1
DRAGnDROP_MOVE_STEP = 1


class GenericMouse(object):
    def __init__(self, test=False):
        if test:
            self.test_logger = PikuliLogger(name='mouse_test_logger').logger
        self._is_mouse_down = False
        self.drag_event = None
        self.buttons = {'left': {'button': None,
                                 'down_event': None,
                                 'up_event': None
                                 },
                        'right': {'button': None,
                                  'down_event': None,
                                  'up_event': None
                                  }
                        }

    def _test_log(self, message):
        if self.test_logger:
            self.test_logger.debug(str(message))

    def _mouse_event(self, event_type, x, y, mouse_button):
        pass

    def key_down(self, x, y, key='left'):
        if key not in self.buttons:
            raise TypeError('Pikuli.Mouse: incorrect mouse button type')
        self.move(x, y)
        self._mouse_event(self.buttons[key]['down_event'],
                          x, y, self.buttons[key]['button'])
        self._is_mouse_down = True

    def key_up(self, x, y, key='left'):
        if key not in self.buttons:
            raise TypeError('Pikuli.Mouse: incorrect mouse button type')

        self._mouse_event(self.buttons[key]['up_event'],
                          x, y, self.buttons[key]['button'])
        self._is_mouse_down = False

    def click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        self.key_down(x, y)
        time.sleep(DELAY_IN_MOUSE_CLICK)
        self.key_up(x, y)
        time.sleep(delay)

    def right_click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        self.key_down(x, y, 'right')
        time.sleep(DELAY_IN_MOUSE_CLICK)
        self.key_up(x, y, 'right')
        time.sleep(delay)

    def double_click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        self.click(x, y, delay=delay)
        time.sleep(DELAY_MOUSE_DOUBLE_CLICK)
        self.click(x, y, delay=delay)
        time.sleep(delay)

    def scroll(self, x, y, direction=1, click=False):
        if self.position != (x, y):
            self.move(x, y)
            time.sleep(DELAY_IN_MOUSE_CLICK)
        if click:
            self.click(x, y)
        self._scroll_event(direction)
        time.sleep(DELAY_IN_SCROLL)

    def drag_to(self, x_from, y_from, x_to, y_to, delay=0.005):
        if not self._is_mouse_down:
            self.key_down(x_from, y_from)
        time.sleep(delay)

        # Bresenham's line algorithm
        # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        if abs(x_to - x_from) >= abs(y_to - y_from):
            (a1, b1, a2, b2) = (x_from, y_from, x_to, y_to)
            f = lambda x, y: self.move(x, y, 0)  # lambda x, y: self._mouse_event(CG.kCGEventLeftMouseDragged, x, y)
        else:
            (a1, b1, a2, b2) = (y_from, x_from, y_to, x_to)
            f = lambda x, y: self.move(y, x, 0)  # self._mouse_event(CG.kCGEventLeftMouseDragged, y, x)

        k = float(b2 - b1) / (a2 - a1)
        a_sgn = (a2 - a1) / abs(a2 - a1)
        la = 0
        while abs(la) <= abs(a2 - a1):
            a = a1 + la
            b = int(k * la) + b1
            f(a, b)
            la += a_sgn * DRAGnDROP_MOVE_STEP
            time.sleep(delay)

    def drop(self):
        if self._is_mouse_down:
            self.key_up(*self.position)
        else:
            raise FailExit('You try drop ({x}, {y}), but it is not bragged before!'.format(
                x=self.position[0], y=self.position[1]))

    def dragndrop(self, x_from, y_from, x_to, y_to):
        self.drag_to(x_from, y_from, x_to, y_to)
        self.drop()
