import time
from Quartz import CoreGraphics as CG
from AppKit import NSEvent
from .generic_mouse import *


class MouseMac(GenericMouse):
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
