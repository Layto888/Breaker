
import random
from laylib.resources import Resources
from laylib.util import xIntersect
from body import Body
from constants import *
import pygame as pg


class Engine(object):
    """regroup all game"""

    def __init__(self):
        self.left = self.right = False
        self.screen = pg.display.get_surface()
        self.boundary = self.screen.get_rect()
        self.gameDone = False
        self.restart = False
        self.clock = pg.time.Clock()
        self.dt = 0.05
        self.fps = 0.0
        self.res = None

    # create the pattern of bricks, colors, of the actual level,
    # self.levels is loaded from levels file.
    def build_level(self):
        # there's 7 levels
        self.level %= 7
        # get configuration of level:
        this_level = self.levels[self.level]['map']  # get the map
        # start positions of the first brick
        start_x, start_y = self.levels[self.level]['cnf'][0:2]
        # thikness of drawables stuffs
        this_thikness = self.levels[self.level]['cnf'][2]
        this_pad_w = self.levels[self.level]['cnf'][3]
        this_pad_vel = self.levels[self.level]['cnf'][4]
        this_ball_vel = self.levels[self.level]['cnf'][5]
        self.level_title = self.levels[self.level]['cnf'][6]

        # 1 - create the pad
        for i in range(PAD_SIZE):
            x_pos = self.boundary.w / 2 - (PAD_W / 2)
            y_pos = self.boundary.h - (PAD_H + 5)
            self.pad.append(Body(TYPE_PADDLE, x_pos, y_pos, BAL_COL))
            self.pad[i].shape.w = this_pad_w
            self.pad[i].thikness = this_thikness
            self.pad[i].xvel = this_pad_vel

        # 2 - create ball and let make it start from the center of the pad
        for i in range(BALL_SIZE):
            x_pos = self.pad[0].shape.x + (PAD_W / 2)
            y_pos = self.pad[0].shape.y - (CIRCLE_RADIUS + 1)
            self.ball.append(Body(TYPE_CIRCLE, x_pos, y_pos, BAL_COL))
            self.ball[i].xvel = self.ball[i].yvel = -this_ball_vel
            self.ball[i].thikness = this_thikness
        del x_pos, y_pos

        # 3 - build the level
        x_pos = start_x
        y_pos = start_y
        i = 0
        for row in this_level:
            for brick in row:
                if brick == 'n':  # normal
                    self.color = NORMAL_BRICK
                elif brick == 's':  # solid
                    self.color = SOLID_BRICK
                elif brick == 'r':  # rock
                    self.color = ROCK_BRICK
                elif brick == 'b':  # bonus
                    self.color = BONUS_BRICK
                elif brick == ' ':  # empty space
                    x_pos += BRICK_W + 3
                    continue
                self.brick.append(Body(TYPE_BRICK, x_pos, y_pos, self.color))
                self.brick[i].thikness = this_thikness
                i += 1
                x_pos += BRICK_W + 3
            y_pos += BRICK_H + 1
            x_pos = start_x

    def key_up(self, key):
        if key == pg.K_LEFT:
            self.left = False
        elif key == pg.K_RIGHT:
            self.right = False
        elif key == pg.K_SPACE:
            self.restart = False
        elif key == pg.K_ESCAPE:
            self.gameDone = True

    def key_down(self, key):
        if key == pg.K_LEFT:
            self.left = True
        elif key == pg.K_RIGHT:
            self.right = True
        elif key == pg.K_SPACE:
            if not self.gameOver:
                self.restart = True
        elif key == pg.K_RETURN:
            if self.gameOver:
                self.new_game()

    def event_listener(self):
        ev = pg.event.poll()
        if ev.type == pg.QUIT:
            self.gameDone = True
        elif ev.type == pg.KEYDOWN:
            self.key_down(ev.key)
        elif ev.type == pg.KEYUP:
            self.key_up(ev.key)

    def new_game(self):
        self.lives = 3
        self.score = 0
        self.gameOver = False
        self.level = 0
        self.gameDone = False
        self.restart = False
        self.next_level()  # go to the level 1.

    def next_level(self):
        # destroy old stuffs and create new ones, to set theirs positions.
        self.pad = []
        self.ball = []
        self.brick = []
        # create some bricks
        self.build_level()
        # prepare next level
        self.level += 1
        # play some background random mp3 music
        this_music = random.choice(self.music_titles)
        pg.mixer.music.load(this_music)
        pg.mixer.music.play()

    def draw(self):
        if not self.gameOver:
            self.screen.fill(BACK_COL)
            # draw the pad list
            for pd in self.pad:
                pd.draw()
            # draw the ball list
            for bl in self.ball:
                bl.draw()
            # draw the bricks list
            for br in self.brick:
                br.draw()
        else:  # game over
            self.screen.fill(WHITE)
            self.res.print_font(
                self.fnt[2], 'Game is over now, go home...', (260, 250), DARK)
            self.res.print_font(
                self.fnt[1], 'press Enter to play', (440, 500), DARK)
            self.res.print_font(
                self.fnt[0], 'By : A.Amine', (1000, 700), DARK)
        # draw all string stuffs
        self.res.print_font(self.fnt[0], str(
            "{0:.2f} FPS".format(self.fps)), (1005, 2), DARK)
        self.res.print_font(self.fnt[0], self.level_title, (5, 2), DARK)
        self.res.print_font(self.fnt[0], str(
            "{} X Points".format(self.score)), (560, 2), DARK)
        self.res.print_font(self.fnt[0], str(
            "{} X Balls".format(self.lives)), (465, 2), DARK)

        pg.display.update()

    # this update the whole logic of game.
    def update(self, dt):
        """ Update the whole game  """

        if not self.gameOver:
            for pd in self.pad:
                if self.left and not self.right:
                    pd.side = -1
                elif self.right and not self.left:
                    pd.side = 1
                else:
                    pd.side = 0
                pd.update(dt)

            # update ball / bricks
            for bl in self.ball:
                if bl.alive:
                    if bl.ypos > self.boundary.h:
                        self.death(bl)
                        break
                    for pd in self.pad:
                        # check for ball/pad collision
                        if pd.shape.colliderect(bl.shape):
                            bl.yvel *= -1
                            bl.ypos = pd.shape.y - (bl.shape.h + 1)
                            self.snd[0].play()
                    for br in self.brick:
                        # check for collision ball / bricks -> update state.
                        if br.shape.colliderect(bl.shape):
                            bl.yvel *= -1
                            if xIntersect(bl.shape, br.shape):
                                bl.xvel *= -1
                            bl.angle = random.uniform(MIN_ANGLE, MAX_ANGLE)
                            self.snd[random.randint(1, 6)].play()
                            # check here type of brick
                            self.kill_bricks_type(br)
                            self.score += 1
                # else ball fall down : we reset it if no game over
                else:
                    bl.xpos = pd.xpos + pd.shape.w / 2
                    bl.ypos = pd.ypos - (bl.shape.w + 1)
                    bl.alive = self.restart
                bl.update(dt)

                # check for win and next level
                if not self.brick:
                    self.snd[8].play()
                    self.next_level()

    # this will siwtch type of brick by changing the color & duration of
    # bricks.
    def kill_bricks_type(self, brick):
        if brick.duration > 0:
            if brick.color is NORMAL_BRICK:
                brick.alive = False
            elif brick.color is SOLID_BRICK:
                brick.color = NORMAL_BRICK
            elif brick.color is ROCK_BRICK:
                brick.color = SOLID_BRICK
            elif brick.color is BONUS_BRICK:
                brick.alive = False

                self.snd[7].play()
                self.lives += 1
            brick.duration -= 1
            # - create new group of bricks and remove the dead one : Method 1.
            # - or just set br.alive to false and make condition in draw:
            # if br.alive->draw without removing the dead bricks from
            # the list of brick: Method 2

        self.brick = [br for br in self.brick if br.alive]

    def death(self, body):
        if not self.lives:
            self.gameOver = True
        else:
            self.lives -= 1
            body.alive = False

    def load_game(self, dataFolder, persistenceLayer):
        self.res = Resources(dataFolder)
        data = self.res.get_res_info(persistenceLayer)
        self.img = self.res.load_img_list(data['imgList'])
        self.snd = self.res.load_snd_list(data['sndList'])
        self.fnt = self.res.load_fnt_list(data['fntList'])
        self.music_titles = self.res.get_music_list(data['mscList'])
        print(self.res.__dict__)

    def load_levels(self, dataFolder, fileLevels):
        res = Resources(dataFolder)
        self.levels = res.get_res_info(fileLevels)
        del res

    def destroy_game(self):
        if self.img:
            del self.img
        if self.snd:
            del self.snd
        if self.fnt:
            del self.fnt
        if self.res:
            del self.res

    def main_loop(self):

        self.new_game()

        while not self.gameDone:
            self.fps = self.clock.get_fps()
            self.event_listener()
            self.update(self.dt)
            self.draw()
            self.clock.tick()
            if self.fps > 0.0:
                self.dt = DEFAULT_FPS / self.fps
