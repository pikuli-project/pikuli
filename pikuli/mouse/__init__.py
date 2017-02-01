import platform

current_platform = platform.system()

if current_platform == 'Darwin':
    from mouse_mac import MouseMac as Mouse
elif current_platform == 'Windows':
    from mouse_win import MouseWin as Mouse
else:
    raise NotImplementedError
