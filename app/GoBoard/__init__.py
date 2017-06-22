
import numpy as np

CHECK_NONE = 0
CHECK_ALIVE = 1
CHECK_BLANK = 2
CHECK_DEAD = -1

BOARD_WHITE = 1
BOARD_BLACK = -1
BOARD_BLANK = 0


class GoBoard(object):

    def __init__(self):
        self.board_size = (19, 19)

        # contain state of space on board
        # BOARD_WHITE = 1  : the white stone is on
        # BOARD_BLACK = -1 : the black stone is on
        # BOARD_BLANK = 0  : there is no stone
        self.board = np.zeros(self.board_size, dtype=np.int)

        # contain the number of captured stones
        self.captured = {'white': 0, 'black': 0}

        # contain the forbidden position to set (because of the rule of pae)
        self.forbidden = None

    @staticmethod
    def board_value_to_name(value):
        if value == BOARD_WHITE:
            return 'white'
        elif value == BOARD_BLACK:
            return 'black'
        elif value == BOARD_BLANK:
            return 'blank'
        return 'unknown'

    @staticmethod
    def board_name_to_value(name):
        if name == 'white':
            return BOARD_WHITE
        elif name == 'black':
            return BOARD_BLACK
        elif name == 'blank':
            return BOARD_BLANK
        return BOARD_BLANK  # Let's assume default value is blank

    def set(self, x, y, stone):
        # Return value: True or False
        #    True: success to set stone.
        #    False: failed to set stone. violation against some rules

        # if there is forbidden position
        if self.forbidden:
            if self.forbidden[0] == x and self.forbidden[1] == y:  # this position if forbidden
                return False
            self.forbidden = None  # forbidden position can't continue over one turn

        if self.check_out_of_range(x, y):  # check out of range
            return False

        # check if there is already a stone
        if self.board[x, y] == BOARD_WHITE or self.board[x, y] == BOARD_BLACK:
            return False

        # convert name to integer value
        board_value = self.board_name_to_value(stone)

        # set stone
        self.board[x, y] = board_value

        # By default, the color of stone is white and hostile color is black
        dead_friendly, dead_hostile = self.check_surrounded_all()
        hostile_name = 'black'

        if board_value == BOARD_BLACK:  # check if the assumption that the color of stone is white was wrong
            dead_hostile, dead_friendly = dead_friendly, dead_hostile
            hostile_name = 'white'

        # If this setting stone can't kill any hostile and the set stone is killed instantly
        if len(dead_hostile) == 0 and len(dead_friendly) > 0:
            self.board[x, y] = BOARD_BLANK  # reverse setting stone
            return False

        # make killed hostiles captured
        for dead in dead_hostile:
            dx, dy = dead
            self.board[dx, dy] = BOARD_BLANK
            # print('{},{} was captured!'.format(dx, dy))

        self.captured[hostile_name] += len(dead_hostile)

        # If killed hostile is single
        if len(dead_hostile) == 1:
            # the position that killed hostile was should be set to forbidden position ( because of rule of pae )
            self.forbidden = [dead_hostile[0][0], dead_hostile[0][1]]

        return True

    def check_surrounded_all(self):

        # Default is DEAD, but if any blank or friendly is around, it's alive
        is_alive_check = np.array([[CHECK_DEAD for _ in range(self.board_size[0])] for _ in range(self.board_size[1])])
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[x, y] == BOARD_BLANK:  # the start of making alive is BLANK
                    self.make_around_alive(x, y, is_alive_check)

        dead_whites = []
        dead_blacks = []

        # check dead stones
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if is_alive_check[x, y] == CHECK_DEAD:
                    stone_color = self.board[x, y]

                    if stone_color == BOARD_WHITE:
                        dead_whites.append([x, y])

                    elif stone_color == BOARD_BLACK:
                        dead_blacks.append([x, y])

        return dead_whites, dead_blacks

    def make_around_alive(self, x, y, is_alive_check):
        # make around blank, friendly stone alive

        if is_alive_check[x, y] == CHECK_ALIVE:  # skip if already alive
            return

        is_alive_check[x, y] = CHECK_ALIVE  # make it alive
        cv = self.board[x, y]

        for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nx, ny = x + offset[0], y + offset[1]

            if self.check_out_of_range(nx, ny):
                continue

            nv = self.board[nx, ny]

            # because the value of white is 1 and the value of black is -1,
            # multiplication of value with hostiles always be -1
            if cv * nv != -1: # only if not hostile.
                # recursively, DFS
                self.make_around_alive(nx, ny, is_alive_check)

    def check_out_of_range(self, x, y):

        if 0 <= x < self.board_size[0] and 0 <= y < self.board_size[1]:
            return False

        return True