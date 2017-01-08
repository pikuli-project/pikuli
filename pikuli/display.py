# -*- coding: utf-8 -*-

from platform_configurator import Platform

if not Platform.is_(Platform.os_ubuntu):
    import numpy as np

from abc import ABCMeta, abstractmethod
from platform_configurator import platform_dependent, \
    implementation_for, Platform
from common_exceptions import FailExit
from logger import PikuliLogger
from PIL import Image
from Settings import settings

logger = PikuliLogger('pikuli.Display ').logger

if Platform.is_(Platform.os_mac):
    import AppKit
    from Quartz import CoreGraphics as CG

if Platform.is_(Platform.os_win):
    from PIL import ImageGrab
    import win32con
    import win32api
    import win32gui
    import win32ui


@platform_dependent
class IDisplay(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def take_screenshot(self, x, y, w, h, hwnd=None):
        """
        Args:
            x:
            y:
            w:
            h:
            hwnd:

        Returns:

        """

    @abstractmethod
    def get_monitor_info(self, n):
        """
        Args:
            n:

        Returns:

        """

    @abstractmethod
    def _monitor_hndl_to_screen_n(self, m_hndl):
        """

        Args:
            m_hndl:

        Returns:

        """


class _GenericDisplay(IDisplay):
    DELAY_KBD_KEY_PRESS = 0.020
    DELAY_BETWEEN_ATTEMTS = 0.5


@implementation_for(Platform.os_mac)
class MacDisplay(_GenericDisplay):

    def _monitor_hndl_to_screen_n(self, m_hndl):
        raise NotImplementedError

    def get_monitor_info(self, n):
        monitors = AppKit.NSScreen.screens()
        if n == 0:
            raise NotImplementedError
        elif n <= len(monitors):
            monitor = monitors[n - 1]
            sf = monitor.backingScaleFactor()
            return (monitor.deviceDescription()['NSScreenNumber'], None,
                    (int(monitor.frame().origin.x),
                     int(monitor.frame().origin.y),
                     int(monitor.frame().size.width * sf + monitor.frame().origin.x),
                     int(monitor.frame().size.height * sf + monitor.frame().origin.y)),
                    sf)
        else:
            raise FailExit('Pikuli.helpers.MacDisplay.get_monitor_info(): wrong monitor number specified: {}'.format(n))

    def take_screenshot(self, x, y, w, h, hwnd=None):
        """
        get area screenshot
        Args:
            x, y: top-left corner of a rectangle
            w, h: rectangle dimensions
            hwnd: for compatibility

        Returns: numpy array

        http://stackoverflow.com/questions/37359192/cannot-figure-out-numpy-equivalent-for-cv-mat-step0
        """
        [x, y, w, h] = map(int, [x, y, w, h])
        driver_cache_size = 64  # bytes

        # align width to the nearest value that divisible by driver_cache_size
        if w % driver_cache_size != 0:
            w = driver_cache_size * (int(w / driver_cache_size) + 1)

        image_ref = CG.CGWindowListCreateImage(CG.CGRectMake(x, y, w, h),  # CG.CGRectInfinite,
                                               CG.kCGWindowListOptionOnScreenOnly,
                                               CG.kCGNullWindowID,
                                               CG.kCGWindowImageDefault)
        pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image_ref))

        height = CG.CGImageGetHeight(image_ref)
        width = CG.CGImageGetWidth(image_ref)

        image = Image.frombuffer("RGBA", (width, height),
                                 pixeldata, "raw", "RGBA", 0, 1).convert('RGB')
        return np.array(image)


@implementation_for(Platform.os_win)
class WinDisplay(_GenericDisplay):

    def _monitor_hndl_to_screen_n(self, m_hndl):
        """
        Converts monitor handle to number (from 1)
        0 - virtual monitor
        """
        minfo = win32api.GetMonitorInfo(m_hndl)  # For example for primary monitor:
        # {'Device': '\\\\.\\DISPLAY1', 'Work': (0, 0, 1920, 1040), 'Flags': 1, 'Monitor': (0, 0, 1920, 1080)}
        screen_n = int(minfo['Device'][len(r'\\.\DISPLAY'):])
        if screen_n <= 0:
            raise FailExit('can not obtain Screen number from win32api.GetMonitorInfo() = {}'.format(minfo))
        return screen_n

    def _take_screenshot_with_native_api(self, x, y, w, h, hwnd):
        if hwnd is None:
            scr_hdc = win32gui.CreateDC('DISPLAY', None, None)
        else:
            scr_hdc = win32gui.GetDC(hwnd)
        mem_hdc = win32gui.CreateCompatibleDC(scr_hdc)
        new_bitmap_h = win32gui.CreateCompatibleBitmap(scr_hdc, w, h)
        win32gui.SelectObject(mem_hdc, new_bitmap_h)  # Returns 'old_bitmap_h'. It will be deleted automatically.

        win32gui.BitBlt(mem_hdc, 0, 0, w, h, scr_hdc, x, y, win32con.SRCCOPY)

        bmp = win32ui.CreateBitmapFromHandle(new_bitmap_h)
        bmp_info = bmp.GetInfo()
        if bmp_info['bmHeight'] != h or bmp_info['bmWidth'] != w:
            raise FailExit('bmp_info = {bmp}, but (w, h) = ({w}, {h})'.format(
                bmp=bmp_info, width=w, height=h))
        if bmp_info['bmType'] != 0 or bmp_info['bmPlanes'] != 1:
            raise FailExit('bmp_info = {bmp}: bmType !=0 or bmPlanes != 1'.format(bmp=str(bmp_info)))
        if bmp_info['bmBitsPixel'] % 8 != 0:
            raise FailExit('bmp_info = {bmp}: bmBitsPixel mod. 8 is not zero'.format(bmp=str(bmp_info)))

        bmp_arr = list(bmp.GetBitmapBits())

        if len(bmp_arr) == w * h * 4:
            del bmp_arr[3::4]  # Delete alpha channel. TODO: Is it fast enough???
        elif len(bmp_arr) != w * h * 3:
            raise FailExit('An error occurred while read bitmap bits')

        result = np.array(bmp_arr, dtype=np.uint8).reshape((h, w, 3))

        win32gui.DeleteDC(mem_hdc)
        win32gui.DeleteObject(new_bitmap_h)

        if not hwnd:
            win32gui.DeleteDC(scr_hdc)
        else:
            win32gui.ReleaseDC(hwnd, scr_hdc)

        return result

    def _take_screenshot_without_native_api(self, x, y, w, h):
        initial_area = ImageGrab.grab(bbox=(x, y, w + x, h + y))
        r, g, b = initial_area.split()
        initial_area = Image.merge("RGB", (b, g, r))
        return np.array(initial_area.getdata(), dtype=np.uint8).reshape((h, w, 3))

    def get_monitor_info(self, n):
        """
        Returns a sequence of tuples. For each monitor found, returns a handle to the monitor,
        device context handle, and intersection rectangle:
        (hMonitor, hdcMonitor, PyRECT)
        """
        monitors = win32api.EnumDisplayMonitors(None, None)
        if n >= 1:
            for m in monitors:
                if self._monitor_hndl_to_screen_n(m[0]) == n:
                    break
        elif n == 0:
            # (x1, y1, x2, y2) = (m[2][0], m[2][1], m[2][2], m[2][3])
            x_max = max(map(lambda m: m[2][2], monitors))
            y_max = max(map(lambda m: m[2][3], monitors))
            m = (None, None, (0, 0, x_max, y_max))
        else:
            raise FailExit('wrong screen number "{}"'.format(n))
        return m + (1,)

    def take_screenshot(self, x, y, w, h, hwnd=None):
        """
        get area screenshot
        Use native api is much faster but sometimes it works incorrect.
        In this case you can change 'use_api_for_screenshots' parameter
        to False in settings class to take scrrenshots with ImageGrab
        module.
        Args:
            x:
            y: top-left corner of a rectangle
            w:
            h: rectangle dimensions
            hwnd: for compatibility

        Returns: numpy array
        """
        x, y, w, h = map(int, [x, y, w, h])
        if hwnd:
            (x, y) = win32gui.ScreenToClient(hwnd, (x, y))

        if settings.use_api_for_screenshots:
            return self._take_screenshot_with_native_api(x, y, w, h, hwnd=hwnd)
        else:
            return self._take_screenshot_without_native_api(x, y, w, h)
