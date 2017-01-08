# -*- coding: utf-8 -*-
import win32con


class KeyCodes(object):
    """
    Ноль-символ и VirtualCode специальных клавиш. Именно такую пару можно вставлять прямо в текстовую
    строку, подаваемую на вход type_text(). Ноль-символ говорит о том, что за ним идет не литера, а коды
    специальной клавиши.

    https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx ("MSDN: Virtual-Key Codes")
    """
    ENTER = chr(0) + chr(win32con.VK_RETURN)
    ESC = chr(0) + chr(win32con.VK_ESCAPE)
    TAB = chr(0) + chr(win32con.VK_TAB)
    LEFT = chr(0) + chr(win32con.VK_LEFT)
    UP = chr(0) + chr(win32con.VK_UP)
    RIGHT = chr(0) + chr(win32con.VK_RIGHT)
    DOWN = chr(0) + chr(win32con.VK_DOWN)
    PAGE_UP = chr(0) + chr(win32con.VK_PRIOR)
    PAGE_DOWN = chr(0) + chr(win32con.VK_NEXT)
    HOME = chr(0) + chr(win32con.VK_HOME)
    END = chr(0) + chr(win32con.VK_END)
    BACKSPACE = chr(0) + chr(win32con.VK_BACK)
    DELETE = chr(0) + chr(win32con.VK_DELETE)
    F1 = chr(0) + chr(win32con.VK_F1)
    F2 = chr(0) + chr(win32con.VK_F2)
    F3 = chr(0) + chr(win32con.VK_F3)
    F4 = chr(0) + chr(win32con.VK_F4)
    F5 = chr(0) + chr(win32con.VK_F5)
    F6 = chr(0) + chr(win32con.VK_F6)
    F7 = chr(0) + chr(win32con.VK_F7)
    F8 = chr(0) + chr(win32con.VK_F8)
    F9 = chr(0) + chr(win32con.VK_F9)
    F10 = chr(0) + chr(win32con.VK_F10)
    F11 = chr(0) + chr(win32con.VK_F11)
    F12 = chr(0) + chr(win32con.VK_F12)
