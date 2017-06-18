from math import cos, sin
from random import uniform
from constants import *
import pygame as pg


class Body(object):

    """
    Desc file: Contains generic body class :
    a body could be : paddle witch move left/right,
    ball with two axis movement or brick with 0 quantity of movement
    Author: A.Amine (Goutted)
    """

    # pylint: disable=too-many-instance-attributes
    # They are reasonable in this case.

    def __init__(self, typeB, posx, posy, color=WHITE):
        self.type = typeB
        # using float to correct rounding error position.
        self.xpos, self.ypos = posx, posy
        self.color = color
        self.thikness = 0  # thikness whene drawing the actual body
        self.screen = pg.display.get_surface()
        self.boundary = self.screen.get_rect()
        # switch types:
        if self.type is TYPE_CIRCLE:
            self.alive = False  # tell if the body is alive or not
            self.radius = CIRCLE_RADIUS
            self.shape = pg.Rect(posx, posy, CIRCLE_RADIUS, CIRCLE_RADIUS)
            self.angle = MAX_ANGLE
            self.xvel = self.yvel = - CIRCLE_VEL
        elif self.type is TYPE_PADDLE:
            self.shape = pg.Rect(posx, posy, PAD_W, PAD_H)
            self.xvel = PADDLE_VEL
            self.side = 0
        elif self.type is TYPE_BRICK:
            self.shape = pg.Rect(posx, posy, BRICK_W, BRICK_H)
            self.alive = True
            # how many hits to destroy the brick
            if self.color is NORMAL_BRICK:
                self.duration = 1
            elif self.color is SOLID_BRICK:
                self.duration = 2
            elif self.color is ROCK_BRICK:
                self.duration = 3
            elif self.color is BONUS_BRICK:
                self.duration = 1

    def draw(self):
        if self.type is TYPE_CIRCLE:
            pg.draw.circle(self.screen, self.color,
                           (self.shape.x, self.shape.y),
                           self.radius, self.thikness)
        else:
            pg.draw.rect(self.screen, self.color, self.shape, self.thikness)

    def update(self, dt):
        if self.type is TYPE_CIRCLE:
            # make move the body
            self.xpos += self.xvel * cos(self.angle) * dt
            self.ypos += self.yvel * sin(self.angle) * dt
            # test for collisions ball/wall
            if self.collide_x():  # left & right
                self.xvel *= -1
            if self.collide_y() == 1:  # top
                self.angle = uniform(MIN_ANGLE, MAX_ANGLE + 0.02)
                self.yvel *= -1
        elif self.type is TYPE_PADDLE:
            self.xpos += self.side * self.xvel * dt
            # test for collisions pad/wall
            self.collide_x()
        self.shape.x = int(self.xpos)
        self.shape.y = int(self.ypos)

    # TODO: clean & update theses two shitty functions.
    def collide_x(self):
        if self.xpos <= 0:
            # reset pos to avoid multiple collisions. (clean mvt)
            self.xpos = 1.0
            return 1
        elif self.xpos + self.shape.w >= self.boundary.w:
            self.xpos = self.boundary.w - (self.shape.w + 1)
            return 2

    def collide_y(self):
        if self.ypos <= 0:
            self.ypos = 1.0
            return 1
        elif self.ypos + self.shape.h >= self.boundary.h:
            return 2
