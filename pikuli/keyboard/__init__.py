import platform

current_platform = platform.system()

if current_platform == 'Darwin':
    from keyboard_mac import KeyboardMac as Keyboard
elif current_platform == 'Windows':
    from keyboard_win import KeyboardWin as Keyboard
else:
    raise NotImplementedError