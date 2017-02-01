# -*- coding: utf-8 -*-

import time
from pikuli.common_exceptions import FailExit
import win32con
import win32api
from key_codes_win import KeyCodes


DELAY_KBD_KEY_PRESS = 0.050
DELAY_BETWEEN_CLICK_AND_TYPE = 0.3


class KeyboardWin(object):
    def __init__(self):
        self.key_codes = {
            """
            VirtualCoded of keys as modifiers.
            (bVk, bScan_press, bScan_release) XT-keyboard scancodes. They could be multibyte.
            """

            'ALT': (win32con.VK_MENU, 0, 0),
            'CTRL': (win32con.VK_CONTROL, 0, 0),
            'SHIFT': (win32con.VK_SHIFT, 0, 0),
        }
        """
            Bitmask of modifiers. It used in the function type_text()
            ALT   = 0x01
            CTRL  = 0x02
            SHIFT = 0x04
            rev  = {0x01: 'ALT', 0x02: 'CTRL', 0x04: 'SHIFT'}
        """
        self.rev = {}
        for (m, i) in (lambda l: zip(l, range(len(l))))(['ALT', 'CTRL', 'SHIFT']):
            setattr(self, m, 2 ** i)
            self.rev[getattr(self, m)] = m

    def press_key(self, char, scancode):
        win32api.keybd_event(char, scancode,
                             win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(DELAY_KBD_KEY_PRESS)

    def release_key(self, char, scancode):
        win32api.keybd_event(char, scancode,
                             win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(DELAY_KBD_KEY_PRESS)

    def type_char(self, char):
        self.press_key(char, 0)
        self.release_key(char, 0)

    def type_text(self, string, modifiers=None):
        """
        https://mail.python.org/pipermail/python-win32/2013-July/012862.html
        https://msdn.microsoft.com/ru-ru/library/windows/desktop/ms646304(v=vs.85).aspx
        ("MSDN: keybd_event function")
        http://stackoverflow.com/questions/4790268/how-to-generate-keystroke-combination-in-win32-api
        http://stackoverflow.com/questions/11906925/python-simulate-keydown
        http://stackoverflow.com/questions/21197257/keybd-event-keyeventf-extendedkey-explanation-required
        """
        string = str(string)

        if modifiers is not None:
            if not isinstance(modifiers, int):
                raise FailExit('incorrect modifiers = "{}"'.format(modifiers))
            for k in self.rev:
                if modifiers & k != 0:
                    self.press_key(self.key_codes[self.rev[k]][0],
                                   self.key_codes[self.rev[k]][1])
        spec_key = False
        for char in string:
            char_code = ord(char)
            if spec_key:
                spec_key = False
                self.type_char(char_code)

            elif char_code == 0:
                spec_key = True
                continue

            elif 0x20 <= char_code <= 0x7E:
                code = win32api.VkKeyScan(char)
                if code & 0x100 != 0 and modifiers is None:
                    self.press_key(self.key_codes['SHIFT'][0], self.key_codes['SHIFT'][1])

                self.type_char(code)

                if code & 0x100 != 0 and modifiers is None:
                    self.release_key(self.key_codes['SHIFT'][0], self.key_codes['SHIFT'][1])

            else:
                raise FailExit('unknown symbol "{symbol}" in "{string}"'.format(
                    symbol=str(char), string=string))

        if modifiers is not None:
            for k in self.rev:
                if modifiers & k != 0:
                    self.release_key(self.key_codes[self.rev[k]][0],
                                     self.key_codes[self.rev[k]][1])
