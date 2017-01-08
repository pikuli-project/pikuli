# -*- coding: utf-8 -*-

from hamcrest.core.base_matcher import BaseMatcher


class ImageEqualTo(BaseMatcher):
    def __init__(self, template):
        self.template = template

    def _matches(self, image):
        result = image == self.template
        if isinstance(result, bool):
            return result
        else:
            return result.all()

    def describe_to(self, description):
        description.append_text('Images are identical')
