#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Game "The Snake"
Author : Yuri Shvetsov
Title : Snake in Python with lib. Pyglet
Date Accomplished On : 16/07/2018
'''

import pyglet
from pyglet import clock
from pyglet.window import key
import random

WAITING_TO_START = 0
GAME = 1
PAUSE = 2
RESET = 3
GAME_OVER = 4

CELL_SIZE = 10
PADDING = (20, 80)

COLOR_BLUE = (0, 180, 240)
COLOR_BLUE_T = (0, 195, 255, 255)
COLOR_GREEN = (0, 210, 50)
COLOR_RED = (200, 50, 50)
COLOR_RED_T = (200, 40, 40, 255)


class Snake:

    def __init__(self, *args, **kwargs):
        self.direction = 'right'
        self.state = WAITING_TO_START
        self.score = 0
        self.save_hiscore()
        self.snake = [(19, 20), (20, 20), (21, 20)]
        self.new_fruit()
        self.BLOCK_KEY = True

#################################     INFO    #################################

    def border_line_draw(self):
        pyglet.graphics.vertex_list(4,
                    ('v2i', (20, 80, 420, 80, 420, 480, 20, 480)),
                    ('c3B', COLOR_BLUE * 4)).draw(pyglet.gl.GL_LINE_LOOP)

    def image_view(self):
        if self.state == WAITING_TO_START:
            pyglet.resource.image('image.png').blit(20, 80)

        else:
            return

    def game_over_draw(self):
        if self.state == GAME_OVER:
            pyglet.text.Label(text='GAME OVER', font_name="Courier",
                                font_size=45, color=COLOR_RED_T,
                                bold=True, x=55, y=300).draw()
            pyglet.text.Label(text='Press ENTER to continue...',
                                font_name="Courier", font_size=18,
                                color=COLOR_RED_T, bold=False,
                                x=40, y=270).draw()
        else:
            return

    def pause_draw(self):
        if self.state == PAUSE:
            pyglet.text.Label(text='Pause...', font_name="Courier",
                                font_size=18, color=COLOR_RED_T,
                                bold=False, x=313, y=20).draw()
        else:
            return

    def scores_draw(self):
        pyglet.text.Label(text='Score: ' + str(self.score),
                            font_name="Courier", font_size=24,
                            color=(255, 255, 255, 255), x=18, y=50).draw()
        pyglet.text.Label(text='Hi-Score: ' + str(self.high_score),
                            font_name="Courier", font_size=24,
                            color=COLOR_BLUE_T, x=18, y=20).draw()

    def save_hiscore(self):
        # with...
        f = open('high_score.txt', 'r')
        lines = f.readlines()

        if self.score > int(lines[0]):
            lines[0] = str(self.score)

        self.high_score = int(lines[0])

        f.close()

        save_changes = open('high_score.txt', 'w')
        save_changes.writelines(lines[0])
        a = open('high_score.txt', 'w')

        save_changes.close()

################################     SQUARES    ###############################

    def square_draw(self, coords, color):
        x = coords[0] * 10 - 10; y = coords[1] * 10 - 10
        if color == 'green':
            square = pyglet.graphics.vertex_list(4,
                    ('v2i', (20+x, 80+y, 30+x, 80+y, 30+x, 90+y, 20+x, 90+y)),
                    ('c3B', COLOR_GREEN * 4))
        elif color == 'red':
            square = pyglet.graphics.vertex_list(4,
                ('v2i', (20+x, 80+y, 30+x, 80+y, 30+x, 90+y, 20+x, 90+y)),
                ('c3B', COLOR_RED * 4))
        return square.draw(pyglet.gl.GL_POLYGON)

    def fruit_draw(self):
        if self.state == GAME or self.state == PAUSE:
            self.square_draw(self.fruit, 'red')

    def random_cell(self):
        return tuple( (random.randint(1, 40), random.randint(1, 40)) )

    def new_fruit(self):
        self.fruit = self.random_cell()
        if self.fruit in self.snake:
            return self.new_fruit()

    def snake_draw(self):
        if self.state == GAME or self.state == PAUSE:
            for i in self.snake:
                self.square_draw(i, 'green')

    def snake_move(self):
        if self.direction == 'right':
            if self.snake[-1][0] != 40:
                self.snake.append(tuple((self.snake[-1][0] + 1,
                                            self.snake[-1][1])))
            else: self.state = GAME_OVER
        elif self.direction == 'down':
            if self.snake[-1][1] != 1:
                self.snake.append(tuple((self.snake[-1][0],
                                            self.snake[-1][1] - 1)))
            else: self.state = GAME_OVER
        elif self.direction == 'left':
            if self.snake[-1][0] != 1:
                self.snake.append(tuple((self.snake[-1][0] - 1,
                                            self.snake[-1][1])))
            else: self.state = GAME_OVER
        elif self.direction == 'up':
            if self.snake[-1][1] != 40:
                self.snake.append(tuple((self.snake[-1][0],
                                            self.snake[-1][1] + 1)))
            else: self.state = GAME_OVER
        self.BLOCK_KEY = True


    def snake_eat(self):
        if self.snake[-1] != self.fruit:
            self.snake.pop(0)
        else:
            self.new_fruit()
            self.score += 10
            if self.score > self.high_score:
                self.save_hiscore()

    def reset(self):
        self.direction = 'right'
        self.state = GAME
        self.score = 0
        self.snake = [(19, 20), (20, 20), (21, 20)]
        self.new_fruit()

    def change_dir(self, change_to):
        if not self.BLOCK_KEY:
            return

        if not self.state == GAME:
            return

        if ((self.direction == 'right' and change_to != 'left') or
        (self.direction == 'down' and change_to != 'up') or
        (self.direction == 'left' and change_to != 'right') or
        (self.direction == 'up' and change_to != 'down')):
            self.direction = change_to

        self.BLOCK_KEY = False

    def check_crash(self):
        if self.snake[-1] in self.snake[:-1]:
            self.state = GAME_OVER

    def update(self):
        if self.state == GAME:
            self.check_crash()
            self.snake_move()
            self.snake_eat()
        elif self.state == RESET:
            self.reset()
        elif self.state == PAUSE:
            return


class Window(pyglet.window.Window):

    def __init__(self, caption='Snake', resizable=False, vsync=True,
                 *args, **kwargs):
        super(Window, self).__init__(440, 500, *args, **kwargs)
        self.game = Snake()
        pyglet.clock.schedule_interval(self.update, 1 / 8.0)

    def on_draw(self):
        self.clear()
        self.game.image_view()
        self.game.game_over_draw()
        self.game.pause_draw()
        self.game.scores_draw()
        self.game.fruit_draw()
        self.game.snake_draw()
        self.game.border_line_draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.D:
            self.game.change_dir('right')
        elif symbol == key.S:
            self.game.change_dir('down')
        elif symbol == key.A:
            self.game.change_dir('left')
        elif symbol == key.W:
            self.game.change_dir('up')
        elif symbol == key.ENTER:
            if self.game.state == GAME_OVER:
                self.game.state = RESET
            elif self.game.state == WAITING_TO_START:
                self.game.state = GAME
            elif self.game.state == GAME:
                self.game.state = PAUSE
            elif self.game.state == PAUSE:
                self.game.state = GAME

    def update(self, dt):
        self.game.update()


if __name__ == "__main__":
    window = Window()
    pyglet.app.run()
