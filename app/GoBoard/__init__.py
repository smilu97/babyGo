
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
        self.board = np.zeros(self.board_size, dtype=np.int)
        self.captured = {'white': 0, 'black': 0}
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

        if self.forbidden:
            if self.forbidden[0] == x and self.forbidden[1] == y:
                return False
            self.forbidden = None

        if self.check_out_of_range(x, y):
            return False

        if self.board[x, y] == BOARD_WHITE or self.board[x, y] == BOARD_BLACK:
            return False

        board_value = self.board_name_to_value(stone)
        self.board[x, y] = board_value

        # By default, the color of stone is white and hostile color is black
        dead_friendly, dead_hostile = self.check_surrounded_all()
        hostile_name = 'black'

        if board_value == BOARD_BLACK:  # check if the assumption that the color of stone is white was wrong
            dead_hostile, dead_friendly = dead_friendly, dead_hostile
            hostile_name = 'white'

        if len(dead_hostile) == 0 and len(dead_friendly) > 0:
            self.board[x, y] = BOARD_BLANK
            return False

        for dead in dead_hostile:
            dx, dy = dead
            self.board[dx, dy] = BOARD_BLANK
            # print('{},{} was captured!'.format(dx, dy))

        self.captured[hostile_name] += len(dead_hostile)

        if len(dead_hostile) == 1:
            self.forbidden = [dead_hostile[0][0], dead_hostile[0][1]]

        return True

    def check_surrounded_all(self):

        # Default is DEAD, but if any blank or friendly is around, it's alive
        is_alive_check = np.array([[CHECK_DEAD for _ in range(self.board_size[0])] for _ in range(self.board_size[1])])
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[x, y] == BOARD_BLANK:
                    self.make_around_alive(x, y, is_alive_check)

        dead_whites = []
        dead_blacks = []

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

        if is_alive_check[x, y] == CHECK_ALIVE:
            return

        is_alive_check[x, y] = CHECK_ALIVE
        cv = self.board[x, y]

        offsets = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for offset in offsets:
            nx, ny = x + offset[0], y + offset[1]

            if self.check_out_of_range(nx, ny):
                continue

            nv = self.board[nx, ny]

            if cv * nv != -1:
                self.make_around_alive(nx, ny, is_alive_check)

    def check_out_of_range(self, x, y):

        if 0 <= x < self.board_size[0] and 0 <= y < self.board_size[1]:
            return False

        return True