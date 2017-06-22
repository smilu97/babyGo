
import pygame as pg
from ..GoBoard import GoBoard
import random
from ..GoBoard import MyRule

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BACKGROUND_COLOR = (244, 229, 66)

STONE_SIZE = 30

img_stone_white = pg.transform.scale(pg.image.load('./images/stone_white.png'), (STONE_SIZE, STONE_SIZE))
img_stone_black = pg.transform.scale(pg.image.load('./images/stone_black.png'), (STONE_SIZE, STONE_SIZE))
bg_image = pg.image.load('./images/board.jpg')

padding = 30

# font = pg.font.SysFont('monospace', 15)

class Visualizer(object):

    def __init__(self):

        self.board = GoBoard()
        self.pad_width = STONE_SIZE * self.board.board_size[1] + padding * 2
        self.pad_height = STONE_SIZE * self.board.board_size[0] + padding * 2
        self.bg_image = pg.transform.scale(bg_image, (self.pad_width, self.pad_height))
        self.turn = 'black'

        self.randomer_T = 50
        self.randomer_clock = self.randomer_T
        self.dt = 0

        self.rule = MyRule
        self.scoring = False

        self.randoming = False

    def run_game(self):

        pg.init()
        self.gamepad = pg.display.set_mode((self.pad_width, self.pad_height))
        pg.display.set_caption('Babygo Visualizer')

        self.clock = pg.time.Clock()

        keep_running = True

        self.render()

        while keep_running:

            keep_running = self.assign_event(pg.event.get())
            # self.render()  # not always update screen
            self.dt = self.clock.tick(20)
            self.update()

        pg.quit()

    def toggle_scoring(self):

        self.scoring = not (self.scoring)
        if self.scoring:
            self.update_scoring()

    def update_scoring(self):
        self.scores, self.cluster_num, self.cluster_type, self.cluster_size = self.rule.get_score(self.board)

    def assign_event(self, events):

        for event in events:
            if event.type == pg.QUIT:
                return False

            if event.type == pg.MOUSEBUTTONUP:
                pos = event.pos
                x = int((pos[1] - padding) / STONE_SIZE)
                y = int((pos[0] - padding) / STONE_SIZE)
                self.set_stone(x, y)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    while True:
                        x = random.randint(0, 18)
                        y = random.randint(0, 18)
                        if self.set_stone(x, y):
                            break
                if event.key == pg.K_s:
                    self.toggle_scoring()

                if event.key == pg.K_p:
                    self.toggle_turn()

                if event.key == pg.K_r:
                    self.randoming = not self.randoming

        return True

    def set_stone(self, x, y):

        if self.board.set(x, y, self.turn):
            print('x: {}, y: {} of {}'.format(x, y, self.turn))
            self.toggle_turn()
            self.update_scoring()
            self.render()
            return True

        return False

    def toggle_turn(self):
        if self.turn == 'white': self.turn = 'black'
        elif self.turn == 'black': self.turn = 'white'

    def update(self):
        if self.randoming:
            self.randomer_clock -= self.dt
        while self.randomer_clock < 0:
            self.randomer_clock += self.randomer_T
            for _ in range(19*19):
                x = random.randint(0,18)
                y = random.randint(0,18)
                if self.set_stone(x, y):
                    break

    def render(self):

        self.gamepad.blit(self.bg_image, (0, 0))

        for x in range(self.board.board_size[0]):
            pos_x = x * STONE_SIZE + STONE_SIZE / 2
            pg.draw.line(self.gamepad, BLACK, (padding, pos_x + padding), (self.pad_width - padding, pos_x + padding), 1)

        for y in range(self.board.board_size[1]):
            pos_y = y * STONE_SIZE + STONE_SIZE / 2
            pg.draw.line(self.gamepad, BLACK, (pos_y + padding, padding), (pos_y + padding, self.pad_height - padding), 1)

        hwa_points = [[3, 3], [3, 9], [3, 15], [9, 3], [9, 9], [9, 15], [15, 3], [15, 9], [15, 15]]
        for point in hwa_points:
            pos_x = int(point[0] * STONE_SIZE + STONE_SIZE / 2) + padding
            pos_y = int(point[1] * STONE_SIZE + STONE_SIZE / 2) + padding
            pg.draw.circle(self.gamepad, BLACK, (pos_y, pos_x), 3, 3)

        for x in range(self.board.board_size[0]):
            for y in range(self.board.board_size[1]):
                current_block = self.board.board_value_to_name(self.board.board[x, y])
                if current_block == 'white' or current_block == 'black':
                    pos_x = int(x * STONE_SIZE) + padding
                    pos_y = int(y * STONE_SIZE) + padding
                    img = img_stone_white if current_block == 'white' else img_stone_black
                    self.gamepad.blit(img, (pos_y, pos_x))

        if self.scoring:
            for x in range(self.board.board_size[0]):
                for y in range(self.board.board_size[1]):
                    current_cluster_num = self.cluster_num[x, y]
                    if current_cluster_num != 0:
                        current_cluster_type = self.cluster_type[current_cluster_num]
                        current_type = 'none'
                        if current_cluster_type[0] == 1 and current_cluster_type[1] == 0:
                            current_type = 'white'
                        elif current_cluster_type[0] == 0 and current_cluster_type[1] == 1:
                            current_type = 'black'

                        if current_type != 'none':
                            size = 5
                            color = WHITE if current_type == 'white' else BLACK
                            pos_x = int(x * STONE_SIZE + padding + STONE_SIZE / 2)
                            pos_y = int(y * STONE_SIZE + padding + STONE_SIZE / 2)
                            rect = (pos_y - size, pos_x - size, size*2, size*2)
                            pg.draw.rect(self.gamepad, color, rect, 1)

        pg.display.update()
