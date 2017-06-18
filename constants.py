
# some colors
DARK = (0, 0, 0)
WHITE = (255, 255, 255)
MENU_COL = (230, 230, 230)
BAL_COL = (39, 40, 34)
BACK_COL = (245, 245, 245)

# default the ball
CIRCLE_RADIUS = 7
CIRCLE_VEL = 72.0
BALL_SIZE = 1
# min & max random angle of the ball after collisions. (0.83, 0.98)
MIN_ANGLE = 0.885
MAX_ANGLE = 1.333

# the paddle
PADDLE_VEL = 19.0
PAD_W = 95
PAD_H = 15
PAD_SIZE = 1

# default values bricks
BRICK_W = 45
BRICK_H = 25
BRICK_ROW = 5
BRICK_COL = 20
# brick colors type
BONUS_BRICK = (174, 129, 213)  # give bad or good bonus (1 hit) value : 'b'
SOLID_BRICK = (48, 167, 227)  # 2 hits to break it value : 's'
ROCK_BRICK = (199, 0, 57)    # 3 hits to break it value 'r'
NORMAL_BRICK = (41, 44, 32)    # 1 hit to break it  value 'n'


# enum types of Body()
TYPE_CIRCLE = 0
TYPE_PADDLE = 1
TYPE_BRICK = 2

# fps
DEFAULT_FPS = 30
