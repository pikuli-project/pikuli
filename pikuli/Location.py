# -*- coding: utf-8 -*-
"""
   Point on the screen.
   Contains methods to move point, move cursor to the point,
   user actions emulation (clicks, text input)
"""

import time
from mouse import Mouse
from keyboard import Keyboard
from common_exceptions import FailExit
from logger import PikuliLogger

DRAGnDROP_MOVE_DELAY = 0.005
DELAY_BETWEEN_CLICK_AND_TYPE = 1

logger = PikuliLogger(__name__).logger


class Location(object):

    def __init__(self, x, y, title="New Location"):
        self.title = title
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        try:
            self.x = int(x)
            self.y = int(y)
            self._is_mouse_down = False
            logger.debug('New Location with name "{name}" created ({x}, {y})'.format(
                         name=self.title, x=self.x, y=self.y))
        except:
            raise FailExit('Incorect Location class constructor call:'
                           '\n\tx = {x}\n\ty = {y}\n\ttitle= %{title}'.format(
                               x=x, y=y, title=title))

    def __str__(self):
        return 'Location ({x}, {y})'.format(x=self.x, y=self.y)

    @property
    def coordinates(self):
        return self.x, self.y

    def mouse_move(self, delay=0):
        self.mouse.move(self.x, self.y, delay)
        logger.debug('Mouse moved to ({x}, {y})'.format(x=self.x, y=self.y))

    def offset(self, dx, dy):
        if isinstance(dx, int) and isinstance(dy, int):
            return Location(self.x + dx, self.y + dy)
        else:
            raise FailExit('Location.offset: incorrect offset values')

    def above(self, dy):
        if isinstance(dy, int) and dy >= 0:
            return Location(self.x, self.y - dy)
        else:
            raise FailExit('Location.above: incorrect value')

    def below(self, dy):
        if isinstance(dy, int) and dy >= 0:
            return Location(self.x, self.y + dy)
        else:
            raise FailExit('Location.below: incorrect value')

    def left(self, dx):
        if isinstance(dx, int) and dx >= 0:
            return Location(self.x - dx, self.y)
        else:
            raise FailExit('Location.left: incorrect value')

    def right(self, dx):
        if isinstance(dx, int) and dx >= 0:
            return Location(self.x + dx, self.y)
        else:
            raise FailExit('Location.right: incorrect value')

    def click(self, after_click_delay=0):
        self.mouse.click(self.x, self.y, after_click_delay)
        logger.debug('mouse left click in ({x}, {y})'.format(x=self.x, y=self.y))

    def mouse_down(self):
        self.mouse.key_down(self.x, self.y)
        logger.debug('mouse down in ({x}, {y})'.format(x=self.x, y=self.y))

    def mouse_up(self):
        self.mouse.key_up(self.x, self.y)
        logger.debug('mouse up in ({x}, {y})'.format(x=self.x, y=self.y))

    def right_click(self, after_click_delay=0):
        self.mouse.right_click(self.x, self.y, after_click_delay)
        logger.debug('mouse right click in ({x}, {y})'.format(x=self.x, y=self.y))

    def double_click(self, after_click_delay=0):
        self.mouse.double_click(self.x, self.y, after_click_delay)
        logger.debug('mouse double click in ({x}, {y})'.format(x=self.x, y=self.y))

    def scroll(self, direction=1, count=1, click=True):
        # direction:
        #   1 - forward
        #  -1 - backward
        for _ in range(0, int(count)):
            self.mouse.scroll(self.x, self.y, direction, click)
        logger.debug('scroll in ({x}, {y}) {count} times, {dir_} direction'.format(
                     x=self.x, y=self.y, count=count,
                     dir_='forward' if direction == 1 else 'backward'))

    def drag_to(self, *dest_location):

        delay = DRAGnDROP_MOVE_DELAY
        if len(dest_location) == 1 and isinstance(dest_location[0], Location):
            (dest_x, dest_y) = (dest_location[0].x, dest_location[0].y)
        elif len(dest_location) == 2:
            try:
                (dest_x, dest_y) = (int(dest_location[0]), int(dest_location[1]))
            except ValueError:
                raise FailExit('Location.drag_to: incorrect parameters')
        elif len(dest_location) == 3:
            try:
                (dest_x, dest_y) = (int(dest_location[0]), int(dest_location[1]))
            except ValueError:
                raise FailExit('Location.drag_to: incorrect parameters')
            delay = float(dest_location[2])

        else:
            raise FailExit('')

        self.mouse.drag_to(self.x, self.y, dest_x, dest_y, delay)
        logger.debug('Mouse drag from (%i, %i) to (%i, %i)' %
                     (self.x, self.y, dest_x, dest_y))
        return self

    def drop(self):
        self.mouse.drop()
        logger.debug('Mouse drop')

    def dragndrop(self, *dest_location):
        self.drag_to(*dest_location)
        self.drop()
        return self

    def type(self, text, modifiers=None, click=True, click_type_delay=DELAY_BETWEEN_CLICK_AND_TYPE):
        log = 'Typed "{}"'.format(text)
        log += ' with modifiers "{}"'.format(modifiers) if modifiers is not None else ''
        if click:
            self.click(after_click_delay=click_type_delay)
        self.keyboard.type_text(str(text), modifiers)
        logger.info(log)

    def enter_text(self, text, modifiers=None, click=True,
                   click_type_delay=DELAY_BETWEEN_CLICK_AND_TYPE):
        if click:
            self.click(after_click_delay=click_type_delay)
        self.keyboard.type_text('a', 'CTRL')
        time.sleep(click_type_delay)
        self.keyboard.type_text(str(text), modifiers)
