# -*- coding: utf-8 -*-

import time
from pikuli.common_exceptions import FailExit
from Quartz import CoreGraphics as CG
from key_codes_mac import KeyCodes

DELAY_KBD_KEY_PRESS = 0.050
DELAY_BETWEEN_CLICK_AND_TYPE = 0.3


class KeyboardMac(object):
    def __init__(self):
        self.keys = KeyCodes()

    def press_key(self, key_code, scancode):
        CG.CGEventPost(
            CG.kCGHIDEventTap,
            CG.CGEventCreateKeyboardEvent(None, key_code, True))

    def release_key(self, key_code, scancode):
        CG.CGEventPost(
            CG.kCGHIDEventTap,
            CG.CGEventCreateKeyboardEvent(None, key_code, False))

    def type_char(self, char):
        self.press_key(self.keys.get_code(char), 0)
        self.release_key(self.keys.get_code(char), 0)
        time.sleep(DELAY_KBD_KEY_PRESS)

    def type_text(self, string, modifiers=None):
        string = str(string)

        if modifiers is not None:
            if not isinstance(modifiers, basestring):
                raise FailExit('incorrect modifiers = "{}"'.format(modifiers))
            self.press_key(self.keys.get_code(modifiers), 0)
            time.sleep(DELAY_KBD_KEY_PRESS)

        for char in string:
            if char.lower() == char:
                self.type_char(char)
            else:
                if modifiers is None:
                    self.press_key(self.keys.get_code('SHIFT'), 0)
                    time.sleep(DELAY_KBD_KEY_PRESS)
                self.type_char(char)
                if modifiers is None:
                    self.release_key(self.keys.get_code('SHIFT'), 0)
                    time.sleep(DELAY_KBD_KEY_PRESS)

        if modifiers is not None:
            self.release_key(self.keys.get_code(modifiers), 0)
