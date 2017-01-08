# -*- coding: utf-8 -*-

"""
   Region - descendant class of BaseRegion.
"""

import datetime
import os
import time

from common_exceptions import FailExit, FindFailed
from Location import Location
from BaseRegion import BaseRegion, logger, DELAY_BETWEEN_CV_ATTEMPT
from Match import Match
from Pattern import Pattern
from Screen import Screen
from Settings import settings


class Region(BaseRegion):
    def offset(self, *args, **kwargs):
        """
        Return area moved relates to self.
        Option 1 (Sikuli-like):
            loc_offs := args[0] - Location type; where to move; (w,h) don't change
        Option 2:
            x_offs := args[0] - int; where to move by x
            y_offs := args[1] - int; where to move by y
            (w,h) don't change
        """
        if len(kwargs) != 0:
            raise FailExit('Unknown keys in kwargs = %s' % str(kwargs))

        offset_title = 'Offset of {}'.format(self.title)
        if len(args) == 2 and \
                (isinstance(args[0], int) or isinstance(args[0], float)) and \
                (isinstance(args[1], int) or isinstance(args[1], float)):
            return Region(self.x + int(args[0]),
                          self.y + int(args[1]),
                          self.w, self.h, find_timeout=self._find_timeout,
                          title=offset_title)
        elif len(args) == 1 and isinstance(args[0], Location):
            return Region(self.x + args[0].x,
                          self.y + args[0].y,
                          self.w, self.h, find_timeout=self._find_timeout,
                          title=offset_title)
        else:
            raise FailExit('Incorrect offset() method call:\n\targs = {}'.format(args))

    def right(self, length=None):
        """
        Return right area relates to self, do not including self.
        Height of new area is equal to height of self.
        Width of new area is equal to 'length' or till the end of the screen
        """
        right_title = 'Region right of {}'.format(self.title)
        try:
            if length is None:
                scr = Region(*Screen(self.screen_number).area)
                reg = Region(self.x + self.w, self.y,
                             (scr.x + scr.w - 1) - (self.x + self.w) + 1,
                             self.h, find_timeout=self._find_timeout,
                             title=right_title)
            elif isinstance(length, int) and length > 0:
                reg = Region(self.x + self.w, self.y,
                             length,
                             self.h, find_timeout=self._find_timeout,
                             title=right_title)
            else:
                raise FailExit('Incorrect length: type is {type}; value is {length}'.format(
                    typr=str(type(length)), length=str(length)))
        except FailExit:
            raise FailExit('Incorrect right() method call:\n\tlength = {length}'.format(
                length=length))
        return reg

    def left(self, length=None):
        """
        Return left area relates to self, do not including self.
        Height of new area is equal to height of self.
        Width of new area is equal to 'length' or till the end of the screen
        if 'length' is not set
        """
        left_title = 'Region left of {}'.format(self.title)
        try:
            if length is None:
                scr = Region(*Screen(self.screen_number).area)
                reg = Region(scr.x, self.y, (self.x - 1) - scr.x + 1,
                             self.h, find_timeout=self._find_timeout,
                             title=left_title)
            elif isinstance(length, int) and length > 0:
                reg = Region(self.x - length, self.y, length,
                             self.h, find_timeout=self._find_timeout,
                             title=left_title)
            else:
                raise FailExit('Incorrect length: type is {type}; value is {length}'.format(
                               typr=str(type(length)), length=str(length)))
        except FailExit:
            raise FailExit('Incorrect left() method call:\n\tlength = {length}'.format(
                length=length))
        return reg

    def above(self, length=None):
        """
        Return top area relates to self, do not including self.
        Width of new area is equal to width of self.
        Height of new area is equal to 'length' or till the end of the screen
        if 'length' is not set
        """
        try:
            if length is None:
                scr = Region(*Screen(self.screen_number).area)
                reg = Region(self.x, scr.y, self.w, (self.y - 1) - scr.y + 1,
                             find_timeout=self._find_timeout,
                             title='Region top of %s' % self.title)
            elif isinstance(length, int) and length > 0:
                reg = Region(self.x, self.y - length, self.w, length,
                             find_timeout=self._find_timeout,
                             title='Region top of %s' % self.title)
            else:
                raise FailExit('Incorrect length: type is {type}; value is {length}'.format(
                    typr=str(type(length)), length=str(length)))
        except FailExit:
            raise FailExit('Incorrect above() method call:\n\tlength = {length}'.format(
                length=length))
        return reg

    def below(self, length=None):
        """
        Return bottom area relates to self, do not including self.
        Width of new area is equal to width of self.
        Height of new area is equal to 'length' or till the end of the screen
        if 'length' is not set
        """
        try:
            if length is None:
                scr = Region(*Screen(self.screen_number).area)
                reg = Region(self.x, self.y + self.h, self.w, (scr.y + scr.h - 1) - (self.y + self.h) + 1,
                             find_timeout=self._find_timeout,
                             title='Region bottom of %s' % self.title)
            elif isinstance(length, int) and length > 0:
                reg = Region(self.x, self.y + self.h, self.w, length,
                             find_timeout=self._find_timeout,
                             title='Region bottom of %s' % self.title)
            else:
                raise FailExit('Incorrect length: type is {type}; value is {length}'.format(
                    typr=str(type(length)), length=str(length)))
        except FailExit:
            raise FailExit('Incorrect below() method call:\n\tlength = {length}'.format(
                length=length))
        return reg

    def nearby(self, length=0):
        """
        Return area around self, including self.
        """
        try:
            if isinstance(length, int) and ((length >= 0) or
                                            (length < 0 and
                                            (-2 * length) < self.w and
                                            (-2 * length) < self.h)):
                reg = Region(self.x - length, self.y - length, self.w + 2 * length,
                             self.h + 2 * length, find_timeout=self._find_timeout,
                             title='Nearby region of {}'.format(self.title))
            else:
                raise FailExit('Incorrect length: type is {type}; value is {length}'.format(
                    typr=str(type(length)), length=str(length)))
        except FailExit:
            raise FailExit('Incorrect nearby() method call:\n\tlength = {length}'.format(
                length=length))
        return reg

    def find_all(self, pattern, delay_before=0):
        err_msg = 'Incorrect find_all() method call:' \
                  '\n\tpattern = {pattern}\n\tdelay_before = {delay}'.format(
                      pattern=str(pattern).split(os.pathsep)[-1], delay=delay_before)
        try:
            delay_before = float(delay_before)
        except ValueError:
            raise FailExit(err_msg)

        if isinstance(pattern, str):
            pattern = Pattern(pattern)
        if not isinstance(pattern, Pattern):
            raise FailExit(err_msg)

        time.sleep(delay_before)
        results = self._find(pattern, self.search_area)
        self._last_match = map(lambda pt: Match(pt[0], pt[1],
                                                pattern.get_w, pattern.get_h,
                                                pt[2], pattern), results)
        logger.info('total found {count} matches of "{file}"'.format(
                    count=len(self._last_match), file=pattern.get_filename(full_path=False)))
        return self._last_match

    def _wait_for_appear_or_vanish(self, pattern, timeout, condition):
        """
            pattern - could be String or List.
                      If isinstance(pattern, list), the first element will return.
                      It can be used when it's necessary to find one of the several images
        """
        fail_exit_text = 'bad "pattern" argument; it should be a string (path to image file) or Pattern object: {}'

        if not isinstance(pattern, list):
            pattern = [pattern]

        for (_i, p) in enumerate(pattern):
            if isinstance(p, str):
                pattern[_i] = Pattern(p)
            elif not isinstance(p, Pattern):
                raise FailExit(fail_exit_text.format(p))

        if timeout is None:
            timeout = self._find_timeout
        else:
            try:
                timeout = float(timeout)
                if timeout < 0:
                    raise ValueError
            except ValueError:
                raise FailExit('Incorrect argument: timeout = {}'.format(timeout))

        prev_field = None
        elaps_time = 0
        while True:
            if prev_field is None or (prev_field != self.search_area).all():
                for ptn in pattern:
                    results = self._find(ptn, self.search_area)
                    if condition == 'appear':
                        if len(results) != 0:
                            # Found something. Choose one result with best 'score'.
                            # If several results has the same 'score' a first found result will choose
                            res = max(results, key=lambda x: x[2])
                            logger.info(' "%s" has been found in(%i, %i)' % (
                                ptn.get_filename(full_path=False), res[0], res[1]))
                            return Match(int(res[0] / self.scaling_factor),
                                         int(res[1] / self.scaling_factor),
                                         int(ptn.get_w / self.scaling_factor),
                                         int(ptn.get_h / self.scaling_factor),
                                         res[2], ptn)
                    elif condition == 'vanish':
                        if len(results) == 0:
                            logger.info('"{}" has vanished'.format(ptn.get_filename(full_path=False)))
                            return
                    else:
                        raise FailExit('unknown condition: "{}"'.format(condition))

            time.sleep(DELAY_BETWEEN_CV_ATTEMPT)
            elaps_time += DELAY_BETWEEN_CV_ATTEMPT
            if elaps_time >= timeout:
                logger.warning('{} hasn`t been found'.format(ptn.get_filename(full_path=False)))
                failed_images = ', '.join(map(lambda _p: _p.get_filename(full_path=False), pattern))
                raise FindFailed('Unable to find "{file}" in {region}'.format(
                    file=failed_images, region=str(self)))

    def find(self, image_path, timeout=None, similarity=settings.min_similarity,
             exception_on_find_fail=True):
        """
        Waits for pattern appear during timeout (in seconds)
        if timeout = 0 - one search iteration will perform
        if timeout = None - default value will use

        Returns Region if pattern found.
        If pattern did not found returns None if exception_on_find_fail is False
        else raises FindFailed exception
        """
        logger.info(' try to find "{img}" with similarity {s}'.format(
            img=str(image_path).split(os.path.sep)[-1], s=similarity))
        try:
            self._last_match = self._wait_for_appear_or_vanish(Pattern(image_path, similarity), timeout, 'appear')
        except FailExit:
            self._last_match = None
            raise
        except FindFailed as ex:
            if exception_on_find_fail:
                self.save_as_jpg(os.path.join(
                    settings.find_failed_dir,
                    '%s_%s.jpg' % (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                                   str(image_path).split('/')[-1])))
                raise ex
            else:
                return None
        else:
            return self._last_match

    def wait_vanish(self, image_path, timeout=None, similarity=settings.min_similarity):
        """
        Waits for pattern vanish during timeout (in seconds).
        If pattern already vanished before method call it return True

        if timeout = 0 - one search iteration will perform
        if timeout = None - default value will use
        """
        logger.info('Check if "{file}" vanish during {t} with similarity {s}'.format(
            file=str(image_path).split(os.path.sep)[-1],
            t=timeout if timeout else str(self._find_timeout),
            s=similarity))
        try:
            self._wait_for_appear_or_vanish(Pattern(image_path, similarity), timeout, 'vanish')
        except FailExit:
            raise FailExit('Incorrect wait_vanish() method call:'
                           '\n\tregion = {region}\n\timage_path = {path}\n\ttimeout = {t}'.format(
                               region=str(self), path=image_path, t=timeout))
        except FindFailed:
            logger.info('"{}" not vanished'.format(str(image_path).split(os.path.sep)[-1]))
            return False
        else:
            logger.info('"{}" vanished'.format(str(image_path).split(os.path.sep)[-1]))
            return True
        finally:
            self._last_match = None

    def exists(self, image_path):
        self._last_match = None
        try:
            self._last_match = self._wait_for_appear_or_vanish(image_path, 0, 'appear')
        except FailExit:
            raise FailExit('Incorrect exists() method call:'
                           '\n\tregion = {region}\n\timage_path = {path}'.format(
                               region=str(self), path=image_path))
        except FindFailed:
            return False
        else:
            return True

    def wait(self, image_path=None, timeout=None):
        """
        For compatibility with Sikuli.
        Wait for pattern appear or just wait
        """
        if image_path is None:
            if timeout:
                time.sleep(timeout)
        else:
            try:
                self._last_match = self._wait_for_appear_or_vanish(image_path, timeout, 'appear')
            except FailExit:
                self._last_match = None
                raise FailExit('Incorrect wait() method call:'
                               '\n\tregion = {region}\n\timage_path = {path}\n\ttimeout = {t}'.format(
                                   region=str(self), path=image_path, t=timeout))
            else:
                return self._last_match
