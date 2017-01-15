# -*- coding: utf-8 -*-

import AppKit
import numpy as np
from PIL import Image
from Quartz import CoreGraphics as CG
from logger import PikuliLogger
from common_exceptions import FailExit

logger = PikuliLogger('pikuli.Display ').logger


class Display(object):
    DELAY_KBD_KEY_PRESS = 0.020
    DELAY_BETWEEN_ATTEMTS = 0.5

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
