# -*- coding: utf-8 -*-

"""
   Match is a result of successful search in the area (Region object)
   It has dimensions of the image using for search
"""

from BaseRegion import BaseRegion
from common_exceptions import FailExit


class Match(BaseRegion):
    def __init__(self, x, y, w, h, score, pattern):
        try:
            super(Match, self).__init__(x, y, w, h, title=pattern.get_filename(full_path=False))
            if not isinstance(score, float) or score <= 0.0 or score > 1.0:
                raise FailExit('not isinstance(score, float) or score <= 0.0 or score > 1.0:')
            self._score = score
            self._pattern = pattern
        except FailExit:
            raise FailExit(
                'Incorrect Match constructor call:\n\tx = {x}\n\ty = {y}\n\tw = {w}\n\th = {h}\n\tscore = {score}'.
                format(file=self._pattern.get_filename(), x=self.x, y=self.y, w=self.w, h=self.h, score=self._score)
            )

    def __str__(self):
        return ('Match of "{file}" in ({x}, {y}, {w}, {h}) with score = {score}'.format(
            file=self._pattern.get_filename(), x=self.x, y=self.y, w=self.w, h=self.h, score=self._score)
        )

    @property
    def score(self):
        """
        Get the similarity score the image or pattern was found. The value is between 0 and 1.
        """
        return self._score

    def get_target(self):
        """
        Get the 'location' object that will be used as the click point.
        Typically, when no offset was specified by Pattern.targetOffset(),
        the click point is the center of the matched region.
        If an offset was given, the click point is the offset relative to the center.
        """
        raise NotImplementedError('TODO here')
