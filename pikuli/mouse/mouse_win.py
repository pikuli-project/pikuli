import time
import win32con
import win32api
from .generic_mouse import *


class MouseWin(GenericMouse):
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
