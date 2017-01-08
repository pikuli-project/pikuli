# -*- coding: utf-8 -*-

import pytest
import os
import cv2
from matchers import ImageEqualTo
from hamcrest import assert_that, equal_to, all_of, has_property
from pikuli import Pattern

DEFAULT_SIMILARITY = 0.995000
CUSTOM_SIMILARITY = 0.812500
STR_DEFAULT_SIMILARITY = '0.995000'
STR_CUSTOM_SIMILARITY = '0.812500'
PATTERN_IMAGE_PATH = os.path.join('test', 'Data', 'test_pattern.png')


class TestPattern(object):
    default_test_pattern = Pattern(PATTERN_IMAGE_PATH)
    custom_test_pattern = Pattern(PATTERN_IMAGE_PATH,
                                  similarity=CUSTOM_SIMILARITY)

    @pytest.mark.parametrize("pattern, expected_data", [
        (default_test_pattern,
         [os.path.abspath(PATTERN_IMAGE_PATH), STR_DEFAULT_SIMILARITY]),
        (custom_test_pattern,
         [os.path.abspath(PATTERN_IMAGE_PATH), STR_CUSTOM_SIMILARITY])
    ])
    def test_str(self, pattern, expected_data):
        assert_that(str(pattern),
                    equal_to('Pattern of "{}" with similarity = {}'.format(
                        expected_data[0], expected_data[1])))

    @pytest.mark.parametrize("pattern, expected_data", [
        (default_test_pattern, DEFAULT_SIMILARITY),
        (custom_test_pattern, CUSTOM_SIMILARITY)
    ])
    def test_get_similarity(self, pattern, expected_data):
        assert_that(pattern.similarity,
                    equal_to(expected_data))

    def test_get_dimensions(self):
        assert_that(self.default_test_pattern, all_of(
            has_property('w', 44),
            has_property('h', 48),
            has_property('get_w', 44),
            has_property('get_h', 48))
        )

    def test_cv2_pattern(self):
        assert_that(self.default_test_pattern.cv2_pattern,
                    ImageEqualTo(cv2.imread(PATTERN_IMAGE_PATH)))

    @pytest.mark.parametrize("full_path, expected_data", [
        (True, os.path.abspath(PATTERN_IMAGE_PATH)),
        (False, os.path.basename(PATTERN_IMAGE_PATH))
    ])
    def test_get_filename(self, full_path, expected_data):
        assert_that(self.default_test_pattern.get_filename(full_path=full_path),
                    equal_to(expected_data))
