from laylib.environment import *
from engine import *
from level_format import *

# res = Resources('data')
# res.save_res_info(data, 'resources.dat', False)
# res.save_res_info(levels, 'levels.dat', True)


def main():

    # init global environment
    game = Environment(

        1080,  # width
        720,   # height
        False,  # full screen
        'Game Demo'  # window title
    )

    # create instance & load all stuffs.
    game.load_complete(

        Engine(),  # game instance
        'data',    # the data folder path.
        'resources.dat',  # persistence layer file
        'levels.dat')     # all game levels

    # go play !
    game.gInstance.main_loop()
    # quit game
    game.destroy()


if __name__ == "__main__":
    main()
