# -*- coding: utf-8 -*-

import time
from abc import ABCMeta, abstractmethod
from platform_configurator import platform_dependent, \
    implementation_for, Platform
from common_exceptions import FailExit
from logger import PikuliLogger

if Platform.is_(Platform.os_mac):
    from Quartz import CoreGraphics as CG
    from AppKit import NSEvent

if Platform.is_(Platform.os_win):
    import win32con
    import win32api

DELAY_AFTER_MOUSE_MOVEMENT = 0.050
DELAY_IN_MOUSE_CLICK = 0.100
DELAY_IN_SCROLL = 0.005
DELAY_MOUSE_DOUBLE_CLICK = 0.1
DRAGnDROP_MOVE_STEP = 1


@platform_dependent
class Mouse(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _mouse_event(self, event_type, x, y, mouse_button):
        """
        """

    @abstractmethod
    def move(self, x, y, delay=DELAY_AFTER_MOUSE_MOVEMENT):
        """
        Args:
            x:
            y:
            delay:

        Returns:

        """

    @abstractmethod
    def click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        """
        Args:
            x:
            y:
            delay:

        Returns:

        """

    @abstractmethod
    def right_click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        """
        Args:
            x:
            y:
            delay:

        Returns:

        """

    @abstractmethod
    def double_click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
        """
        Args:
            x:
            y:
            delay:

        Returns:

        """

    @abstractmethod
    def key_down(self, x, y, key='left'):
        """
        Args:
            x:
            y:
            key:

        Returns:

        """

    @abstractmethod
    def key_up(self, x, y, key='left'):
        """
        Args:
            x:
            y:
            key:

        Returns:

        """

    @abstractmethod
    def scroll(self, x, y, direction=-1, click=False):
        """
        Args:
            x:
            y:
            direction:
            click

        Returns:

        """

    @abstractmethod
    def drag_to(self, x_from, y_from, x_to, y_to, delay=0.005):
        """

        Args:
            x_from:
            y_from:
            x_to:
            y_to:
            delay:

        Returns:
        """

    @abstractmethod
    def drop(self):
        """
        Returns:

        """

    @abstractmethod
    def dragndrop(self, x_from, y_from, x_to, y_to):
        """
        Returns:

        """


class _GenericMouse(Mouse):
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

if Platform.is_(Platform.os_mac):
    @implementation_for(Platform.os_mac)
    class MacMouse(_GenericMouse):
        def __init__(self):
            self._is_mouse_down = False
            self.buttons = {'left': {'button': CG.kCGMouseButtonLeft,
                                     'down_event': CG.kCGEventLeftMouseDown,
                                     'up_event': CG.kCGEventLeftMouseUp
                                     },
                            'right': {'button': CG.kCGMouseButtonRight,
                                      'down_event': CG.kCGEventRightMouseDown,
                                      'up_event': CG.kCGEventRightMouseUp
                                      }
                            }

        def _mouse_event(self, event_type, x, y, mouse_button=CG.kCGMouseButtonLeft):
            if mouse_button not in [CG.kCGMouseButtonLeft, CG.kCGMouseButtonRight]:
                raise TypeError('Pikuli.MacMouse: incorrect mouse button type')

            evt = CG.CGEventCreateMouseEvent(
                None,
                event_type,
                (x, y),
                mouse_button)
            CG.CGEventPost(CG.kCGHIDEventTap, evt)
            return evt

        @staticmethod
        def _scroll_event(direction=1):
            if direction not in [-1, 1]:
                raise TypeError('Pikuli.MacMouse: incorrect scroll direction type')
            evt = CG.CGEventCreateScrollWheelEvent(
                None, 0, 1, int(direction))
            CG.CGEventPost(CG.kCGHIDEventTap, evt)

        @property
        def position(self):
            location = NSEvent.mouseLocation()
            return int(location.x), int(CG.CGDisplayPixelsHigh(0) - location.y)

        def move(self, x, y, delay=DELAY_AFTER_MOUSE_MOVEMENT):
            self._mouse_event(CG.kCGEventMouseMoved, x, y)
            time.sleep(delay)

        def double_click(self, x, y, delay=DELAY_IN_MOUSE_CLICK):
            event = self._mouse_event(self.buttons['left']['down_event'], x, y,
                                      self.buttons['left']['button'])
            CG.CGEventSetType(event, self.buttons['left']['up_event'])
            CG.CGEventPost(CG.kCGHIDEventTap, event)

            CG.CGEventSetIntegerValueField(event, CG.kCGMouseEventClickState, 2)

            CG.CGEventSetType(event, self.buttons['left']['down_event'])
            CG.CGEventPost(CG.kCGHIDEventTap, event)
            CG.CGEventSetType(event, self.buttons['left']['up_event'])
            CG.CGEventPost(CG.kCGHIDEventTap, event)


@implementation_for(Platform.os_win)
class WinMouse(_GenericMouse):
    def __init__(self):
        self._is_mouse_down = False
        self.buttons = {'left': {'button': None,
                                 'down_event': win32con.MOUSEEVENTF_LEFTDOWN,
                                 'up_event': win32con.MOUSEEVENTF_LEFTUP
                                 },
                        'right': {'button': None,
                                  'down_event': win32con.MOUSEEVENTF_RIGHTDOWN,
                                  'up_event': win32con.MOUSEEVENTF_RIGHTUP
                                  }
                        }

    def _mouse_event(self, event_type, x, y, mouse_button=None):
        win32api.mouse_event(event_type, x, y, 0, 0)

    def _scroll_event(self, direction=1):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,
                             self.position[0],
                             self.position[1],
                             int(direction), 0)
        time.sleep(DELAY_IN_MOUSE_CLICK)

    @property
    def position(self):
        return win32api.GetCursorPos()

    def move(self, x, y, delay=DELAY_AFTER_MOUSE_MOVEMENT):
        win32api.SetCursorPos((x, y))
        time.sleep(delay)
