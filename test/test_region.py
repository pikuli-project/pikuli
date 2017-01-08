# -*- coding: utf-8 -*-

import pytest
from hamcrest import assert_that, equal_to, all_of, \
    instance_of, has_property, calling, raises
from pikuli import Region, Location
from pikuli.common_exceptions import FailExit


X = 311
Y = 128
ID = 3
WIDTH = 303
HEIGHT = 201
FIND_TIMEOUT = 3.1
TITLE = 'New test region'


class TestRegion(object):
    test_region = Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID)

    def test_str(self):
        assert_that(str(self.test_region),
                    equal_to('Region "%s" (%i, %i, %i, %i)' %
                             (TITLE, X, Y, WIDTH, HEIGHT)))

    @pytest.mark.parametrize("id,region,expected", [
        ("Default id", Region(X, Y, WIDTH, HEIGHT), 0),
        ("Custom id", test_region, 3)
    ])
    def test_id(self, id, region, expected):
        assert_that(region.get_id(), equal_to(expected))

    @pytest.mark.parametrize("title,region,expected", [
        ("Default title", Region(X, Y, WIDTH, HEIGHT), 'New Region'),
        ("Custom title", test_region, 'New test region')
    ])
    def test_title(self, title, region, expected):
        assert_that(region.title, equal_to(expected))

    @pytest.mark.parametrize("dimension,value,expected", [
        ("x value", test_region.x, X),
        ("y value", test_region.y, Y),
        ("width", test_region.w, WIDTH),
        ("height", test_region.h, HEIGHT)
    ])
    def test_get_dimensions(self, dimension, value, expected):
        assert_that(value, equal_to(expected))

    @pytest.mark.parametrize("x_offset,y_offset", [
        (0, 0), (15, 11),
    ])
    def test_get_top_left(self, x_offset, y_offset):
        location = self.test_region.get_top_left(x_offset, y_offset)
        assert_that(
            location, all_of(
                has_property('x', X + x_offset),
                has_property('y', Y + y_offset),
                has_property('title', 'Top left corner of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("x_offset,y_offset", [
        (0, 0), (15, 11),
    ])
    def test_get_top_right(self, x_offset, y_offset):
        location = self.test_region.get_top_right(x_offset, y_offset)
        assert_that(
            location, all_of(
                has_property('x', X + x_offset + WIDTH),
                has_property('y', Y + y_offset),
                has_property('title', 'Top right corner of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("x_offset,y_offset", [
        (0, 0), (15, 11),
    ])
    def test_get_bottom_left(self, x_offset, y_offset):
        location = self.test_region.get_bottom_left(x_offset, y_offset)
        assert_that(
            location, all_of(
                has_property('x', X + x_offset),
                has_property('y', Y + y_offset + HEIGHT),
                has_property('title', 'Bottom left corner of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("x_offset,y_offset", [
        (0, 0), (15, 11),
    ])
    def test_get_bottom_right(self, x_offset, y_offset):
        location = self.test_region.get_bottom_right(x_offset, y_offset)
        assert_that(
            location, all_of(
                has_property('x', X + x_offset + WIDTH),
                has_property('y', Y + y_offset + HEIGHT),
                has_property('title', 'Bottom right corner of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("x_offset,y_offset", [
        (0, 0), (15, 11),
    ])
    def test_get_center(self, x_offset, y_offset):
        location = self.test_region.get_center(x_offset, y_offset)
        assert_that(
            location, all_of(
                has_property('x', X + x_offset + int(WIDTH / 2)),
                has_property('y', Y + y_offset + int(HEIGHT / 2)),
                has_property('title', 'Center of {}'.format(TITLE)))
        )

    def test_get_find_timeout(self):
        assert_that(
            self.test_region.get_find_timeout(), equal_to(FIND_TIMEOUT)
        )

    def test_set_find_timeout(self):
        self.test_region.set_find_timeout(FIND_TIMEOUT + 5)
        assert_that(
            self.test_region.get_find_timeout(), equal_to(FIND_TIMEOUT + 5)
        )

    @pytest.mark.parametrize("relation,value,expected", [
        ("top-left", X + 10, X + 10),
        ("center", X + 10, X + 10 - int(test_region.w / 2))
    ])
    def test_set_x(self, relation, value, expected):
        self.test_region.set_x(value, relation=relation)
        assert_that(self.test_region.x, equal_to(expected))

    @pytest.mark.parametrize("relation,value", [
        ("some_relation", X + 10),
        ("center", '10'),
        ("center", 'ten')
    ])
    def test_fail_set_x(self, relation, value):
        assert_that(calling(self.test_region.set_x).with_args(value, relation=relation),
                    raises(FailExit))

    @pytest.mark.parametrize("relation,value,expected", [
        ("top-left", Y + 10, Y + 10),
        ("center", Y + 10, Y + 10 - int(test_region.h / 2))
    ])
    def test_set_y(self, relation, value, expected):
        self.test_region.set_y(value, relation=relation)
        assert_that(self.test_region.y, equal_to(expected))

    @pytest.mark.parametrize("relation,value", [
        ("some_relation", Y + 10),
        ("center", '10'),
        ("center", 'ten')
    ])
    def test_fail_set_y(self, relation, value):
        assert_that(calling(self.test_region.set_y).with_args(value, relation=relation),
                    raises(FailExit))

    @pytest.mark.parametrize("relation,value,expected_x", [
        ("top-left", WIDTH + 10, X),
        ("center", WIDTH + 10, X - 5)
    ])
    def test_set_width(self, relation, value, expected_x):
        reg = Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID)
        reg.set_w(value, relation=relation)
        assert_that(all_of(
            reg, has_property('w', value),
            reg, has_property('x', expected_x))
        )

    @pytest.mark.parametrize("relation,value", [
        ("some_relation", WIDTH + 10),
        ("center", '10'),
        ("center", 'ten')
    ])
    def test_fail_set_width(self, relation, value):
        assert_that(calling(self.test_region.set_w).with_args(value, relation=relation),
                    raises(FailExit))

    @pytest.mark.parametrize("relation,value,expected_y", [
        ("top-left", HEIGHT + 10, Y),
        ("center", HEIGHT + 10, Y - 5)
    ])
    def test_set_height(self, relation, value, expected_y):
        reg = Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID)
        reg.set_h(value, relation=relation)
        assert_that(all_of(
            reg, has_property('h', value),
            reg, has_property('y', expected_y))
        )

    @pytest.mark.parametrize("relation,value", [
        ("some_relation", WIDTH + 10),
        ("center", '10'),
        ("center", 'ten')
    ])
    def test_fail_set_height(self, relation, value):
        assert_that(calling(self.test_region.set_h).with_args(value, relation=relation),
                    raises(FailExit))

    @pytest.mark.parametrize("relation,args,expected", [
        ('top-left',
         [Region(X + 10, Y + 10, WIDTH + 10, HEIGHT + 10)],
         [X + 10, Y + 10, WIDTH + 10, HEIGHT + 10]),
        ('top-left',
         [X + 10, Y + 10, WIDTH + 10, HEIGHT + 10],
         [X + 10, Y + 10, WIDTH + 10, HEIGHT + 10]),
        ('center',
         [X + 10, Y + 10, WIDTH + 10, HEIGHT + 10],
         [X + 10 - int((WIDTH + 10) / 2),
          Y + 10 - int((HEIGHT + 10) / 2),
          WIDTH + 10,
          HEIGHT + 10])
    ])
    def test_set_rect(self, relation, args, expected):
        self.test_region.set_rect(*args, relation=relation)

        assert_that(
            self.test_region, all_of(
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]))
        )

    @pytest.mark.parametrize("region,args,expected", [
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         [Location(13, 14)],
         [test_region.x + 13, test_region.y + 14, WIDTH, HEIGHT]),
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         [13, 14],
         [test_region.x + 13, test_region.y + 14, WIDTH, HEIGHT])
    ])
    def test_offset(self, region, args, expected):
        offset = region.offset(*args)
        assert_that(
            offset, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Offset of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("region,length,expected", [
        # TODO: implement test for length = None
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         51,
         [X + WIDTH, Y, 51, HEIGHT])
    ])
    def test_right(self, region, length, expected):
        right = region.right(length=length)
        assert_that(
            right, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Region right of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("region,length,expected", [
        # TODO: implement test for length = None
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         53,
         [X - 53, Y, 53, HEIGHT])
    ])
    def test_left(self, region, length, expected):
        left = region.left(length=length)
        assert_that(
            left, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Region left of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("region,length,expected", [
        # TODO: implement test for length = None
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         55,
         [X, Y - 55, WIDTH, 55])
    ])
    def test_above(self, region, length, expected):
        above = region.above(length=length)
        assert_that(
            above, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Region top of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("region,length,expected", [
        # TODO: implement test for length = None
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         57,
         [X, Y + HEIGHT, WIDTH, 57])
    ])
    def test_below(self, region, length, expected):
        below = region.below(length=length)
        assert_that(
            below, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Region bottom of {}'.format(TITLE)))
        )

    @pytest.mark.parametrize("region,length,expected", [
        (Region(X, Y, WIDTH, HEIGHT, title=TITLE, id=ID),
         49,
         [X - 49, Y - 49, WIDTH + 2 * 49, HEIGHT + 2 * 49])
    ])
    def test_nearby(self, region, length, expected):
        below = region.nearby(length=length)
        assert_that(
            below, all_of(
                instance_of(Region),
                has_property('x', expected[0]),
                has_property('y', expected[1]),
                has_property('w', expected[2]),
                has_property('h', expected[3]),
                has_property('_find_timeout', FIND_TIMEOUT),
                has_property('title', 'Nearby region of {}'.format(TITLE)))
        )

# TODO: implement platform dependent tests
