# -*- coding: utf-8 -*-


class KeyCodes(object):
    """ Holder for Macintosh keyboard codes.
    """

    def __init__(self):
        self.codes = {
            'LEFT_ALT': {'code': 0x3A, 'modifier': None},  # Left ALT key
            'RIGHT_ALT': 0x3D,  # Right ALT key
            'LEFT_SHIFT': 0x38,  # Left SHIFT key
            'RIGHT_SHIFT': 0x3C,  # Right SHIFT key
            'CTRL': 0x3B,  # Left CONTROL key
            'LEFT_CONTROL': 0x3B,  # Left CONTROL key
            'RIGHT_CONTROL': 0x3E,  # Right CONTROL key
            'LEFT_COMMAND': 0x37,  # Left COMMAND key
            'RIGHT_COMMAND': 0x36,  # Right COMMAND key
            'BACKSPACE': 0x33,  # BACKSPACE key
            'TAB': 0x30,  # TAB key
            'CLEAR': 0x47,  # CLEAR key
            'RETURN': 0x24,  # ENTER key
            'SHIFT': 0x3C,  # SHIFT key
            'CONTROL': 0x3B,  # CTRL key
            'ALT': 0x3A,  # ALT key
            'CAPS_LOCK': 0x39,  # CAPS LOCK key
            'ESCAPE': 0x35,  # ESC key
            'PAGE_UP': 0x74,  # PAGE UP key
            'PAGE_DOWN': 0x79,  # PAGE DOWN key
            'END': 0x77,  # END key
            'HOME': 0x73,  # HOME key
            'LEFT': 0x7B,  # LEFT ARROW key
            'UP': 0x7E,  # UP ARROW key
            'RIGHT': 0x7C,  # RIGHT ARROW key
            'DOWN': 0x7D,  # DOWN ARROW key
            'INSERT': 0x72,  # INS key
            'DELETE': 0x75,  # DEL key
            'KEY_ ': 0x31,  # SPACEBAR
            'KEY_0': 0x1D,  # 0 key
            'KEY_1': 0x12,  # 1 key
            'KEY_2': 0x13,  # 2 key
            'KEY_3': 0x14,  # 3 key
            'KEY_4': 0x15,  # 4 key
            'KEY_5': 0x17,  # 5 key
            'KEY_6': 0x16,  # 6 key
            'KEY_7': 0x1A,  # 7 key
            'KEY_8': 0x1C,  # 8 key
            'KEY_9': 0x19,  # 9 key
            'KEY_A': 0x00,  # A key
            'KEY_B': 0x0B,  # B key
            'KEY_C': 0x08,  # C key
            'KEY_D': 0x02,  # D key
            'KEY_E': 0x0E,  # E key
            'KEY_F': 0x03,  # F key
            'KEY_G': 0x05,  # G key
            'KEY_H': 0x04,  # H key
            'KEY_I': 0x22,  # I key
            'KEY_J': 0x26,  # J key
            'KEY_K': 0x28,  # K key
            'KEY_L': 0x25,  # L key
            'KEY_M': 0x2E,  # M key
            'KEY_N': 0x2D,  # N key
            'KEY_O': 0x1F,  # O key
            'KEY_P': 0x23,  # P key
            'KEY_Q': 0x0C,  # Q key
            'KEY_R': 0x0F,  # R key
            'KEY_S': 0x01,  # S key
            'KEY_T': 0x11,  # T key
            'KEY_U': 0x20,  # U key
            'KEY_V': 0x09,  # V key
            'KEY_W': 0x0D,  # W key
            'KEY_X': 0x07,  # X key
            'KEY_Y': 0x10,  # Y key
            'KEY_Z': 0x06,  # Z key
            'KEY_*': 0x43,  # Multiply key
            'KEY_+': 0x45,  # Add key
            'KEY_-': 0x4E,  # Subtract key
            'KEY_,': 0x2B,  # For any country/region, the ',' key
            'KEY_.': 0x2F,  # For any country/region, the '.' key
            'NUMPAD0': 0x52,  # Numeric keypad 0 key
            'NUMPAD1': 0x53,  # Numeric keypad 1 key
            'NUMPAD2': 0x54,  # Numeric keypad 2 key
            'NUMPAD3': 0x55,  # Numeric keypad 3 key
            'NUMPAD4': 0x56,  # Numeric keypad 4 key
            'NUMPAD5': 0x57,  # Numeric keypad 5 key
            'NUMPAD6': 0x58,  # Numeric keypad 6 key
            'NUMPAD7': 0x59,  # Numeric keypad 7 key
            'NUMPAD8': 0x5B,  # Numeric keypad 8 key
            'NUMPAD9': 0x5C,  # Numeric keypad 9 key
            'DECIMAL': 0x41,  # Decimal key
            'KEY_DIVIDE': 0x4B,  # Divide key'
            'F1': 0x7A,  # F1 key
            'F2': 0x78,  # F2 key
            'F3': 0x63,  # F3 key
            'F4': 0x76,  # F4 key
            'F5': 0x60,  # F5 key
            'F6': 0x61,  # F6 key
            'F7': 0x62,  # F7 key
            'F8': 0x64,  # F8 key
            'F9': 0x65,  # F9 key
            'F10': 0x6D,  # F10 key
            'F11': 0x67,  # F11 key
            'F12': 0x6F,  # F12 key
            'OEM_1': 0x29,  # For the US standard keyboard, the ';:' key
            'OEM_PLUS': 0x18,  # For any country/region, the '+' key
            'OEM_MINUS': 0x1B,  # For any country/region, the '-' key
            'KEY_/': 0x2C,  # For the US standard keyboard, the '/?' key
            'OEM_3': 0x32,  # For the US standard keyboard, the '`~' key
            'OEM_4': 0x21,  # For the US standard keyboard, the '[{' key
            'OEM_5': 0x2A,  # For the US standard keyboard, the '\|' key
            'OEM_6': 0x1E,  # For the US standard keyboard, the ']}' key
            'OEM_7': 0x27  # For the US standard keyboard, the ''"'
        }

    def get_code(self, char_name):
        if len(char_name) == 1:
            key = 'KEY_{}'.format(char_name.upper())
        else:
            key = char_name.upper()
        if key in self.codes:
            return self.codes[key]
        else:
            return None
