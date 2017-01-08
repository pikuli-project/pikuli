# -*- coding: utf-8 -*-

"""
   Screen - representation of physical computer monitors
"""

from common_exceptions import FailExit
from display import IDisplay


class Screen(object):
    def __init__(self, n):
        if isinstance(n, int) and n >= 0:
            # Returns a sequence of tuples. For each monitor found, returns a handle to the monitor,
            # device context handle, and intersection rectangle: (hMonitor, hdcMonitor, PyRECT)
            (mon_hndl, _, mon_rect, _) = IDisplay().get_monitor_info(n)

            self.area = (mon_rect[0],
                         mon_rect[1],
                         mon_rect[2] - mon_rect[0],
                         mon_rect[3] - mon_rect[1])
            self.number = n

        else:
            raise FailExit()

    def __str__(self):
        return 'Screen {number} {area}'.format(
               number=self.number, area=self.area)
