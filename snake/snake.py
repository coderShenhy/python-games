#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit
from random import choice

import pygame
from pygame.locals import QUIT, KEYDOWN

TITLE = '贪吃蛇--By 打代码的shy'

WIDTH = 660  # 定义画布宽高
HEIGHT = 500
SNAKE_SIZE = 20  # 定义蛇的宽度
BOARD_COLOR = (0, 0, 100)  # 定义边界的颜色


class Vector():
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def copy(self):
        type_self = type(self)
        return type_self(self.x, self.y)

    def move(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __repr__(self):
        type_self = type(self)
        name = type_self.__name__
        return '{}({!r}, {!r})'.format(name, self.x, self.y)


class Snake:
    def __init__(self):
        # 蛇活动的范围
        self.map = {(x, y): 0
                    for x in range(1,
                                   int(WIDTH / SNAKE_SIZE) - 2)
                    for y in range(1,
                                   int(HEIGHT / SNAKE_SIZE) - 2)}
        # 蛇身
        self.body = [
            Vector(5 * SNAKE_SIZE, 5 * SNAKE_SIZE),
            Vector(6 * SNAKE_SIZE, 5 * SNAKE_SIZE)
        ]
        self.head = self.body[-1].copy()  # 蛇头
        self.color = (0, 0, 0)  # 颜色

        # 定义方向的增量字典
        self.direction = {
            'right': Vector(SNAKE_SIZE, 0),
            'left': Vector(-SNAKE_SIZE, 0),
            'up': Vector(0, -SNAKE_SIZE),
            'down': Vector(0, SNAKE_SIZE)
        }
        # 初始化方向
        self.move_direction = 'right'
        self.speed = 4  # 初始化速度
        self.score = 0  # 初始化分数

        # 初始生成食物的位置
        self.food = Vector(0, 0)
        self.food_color = (255, 0, 0)
        self.generate_food()

        # 定义一个标志位，用来判断是否在游戏中
        self.game_started = False

    def generate_food(self):
        empty_pos = [
            pos for pos in self.map.keys()
            if Vector(pos[0] * SNAKE_SIZE, pos[1] *
                      SNAKE_SIZE) not in self.body
        ]
        result = choice(empty_pos)
        self.food.x = result[0] * 20
        self.food.y = result[1] * 20

    def move(self):
        # 取出目前的蛇头
        self.head = self.body[-1].copy()
        # 根据移动的方向和增量计算下一次的蛇头
        self.head.move(self.direction[self.move_direction])
        # 判断移动后蛇是否还活着
        if not self._islive(self.head):
            # 游戏结束 返回False
            return False
        # 游戏继续
        # 添加下一次蛇头
        self.body.append(self.head)
        # 判断是否吃到了食物
        if self.head == self.food:
            self.score += 1
            if self.score % 5 == 0:
                self.speed += 2
            self.generate_food()
        else:
            # 没吃到,把蛇尾删除
            self.body.pop(0)
        return True

    def _islive(self, head):
        return 0 < head.x < WIDTH - SNAKE_SIZE and 0 < head.y < HEIGHT - SNAKE_SIZE and head not in self.body


KEY_DIRECTION_DICT = {
    119: 'up',  # W
    115: 'down',  # S
    97: 'left',  # A
    100: 'right',  # D
    273: 'up',  # UP
    274: 'down',  # DOWN
    276: 'left',  # LEFT
    275: 'right',  # RIGHT
}


def press(events, snake):
    for event in events:
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == 13:
                snake.game_started = True
            if snake.game_started and event.key in KEY_DIRECTION_DICT:
                return direction_check(snake.move_direction,
                                       KEY_DIRECTION_DICT[event.key])


def draw_score(screen, score, position):
    tips_font = pygame.font.SysFont('arial', 20)
    screen.blit(
        tips_font.render('Score: {}'.format(score), True, (0, 0, 205),
                         (255, 255, 255)), position)


def game_continue(screen, snake):
    '''游戏继续'''
    init_board(screen)  # 画边界
    draw_score(screen, snake.score, (500, 0))  # 画分数
    # 画蛇身
    for seg in snake.body:
        pygame.draw.rect(screen, snake.color, [seg[0], seg[1], 20, 20], 0)
    # 画食物
    pygame.draw.rect(screen, snake.food_color,
                     [snake.food[0], snake.food[1], 20, 20], 0)


def game_over(screen, fonts, score):
    '''游戏结束'''
    # 显示游戏结束
    screen.blit(fonts['game_over'], (250, 100))
    draw_score(screen, score, (290, 200))
    screen.blit(fonts['start'], (220, 310))
    snake = Snake()  # 初始化蛇，用于下一次开始
    return snake


def direction_check(move_direction, change_direction):
    # 方向判断
    directions = [['up', 'down'], ['left', 'right']]
    if move_direction in directions[0] and change_direction in directions[1]:
        return change_direction
    elif move_direction in directions[1] and change_direction in directions[0]:
        return change_direction

    return move_direction


def init(fonts):
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    screen.fill((255, 255, 255))
    screen.blit(fonts['welcome'], (177, 100))
    screen.blit(fonts['start'], (195, 310))
    return fps_clock, screen


def init_board(screen):
    board_width = int(WIDTH / SNAKE_SIZE)
    board_height = int(HEIGHT / SNAKE_SIZE)
    color = BOARD_COLOR
    width = 0
    for i in range(board_width):
        pos = i * SNAKE_SIZE, 0, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)
        pos = i * SNAKE_SIZE, (board_height -
                               1) * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)

    # 上下边框占用了 Y: 0 26*20
    for i in range(board_height - 1):
        pos = 0, SNAKE_SIZE + i * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)
        pos = (
            board_width - 1
        ) * SNAKE_SIZE, SNAKE_SIZE + i * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)


def font_setting():
    title_font = pygame.font.SysFont('arial', 32)
    welcome_words = title_font.render('Welcome to My Snake', True, (0, 0, 0),
                                      (255, 255, 255))
    tips_font = pygame.font.SysFont('arial', 24)
    start_game_words = tips_font.render('Press Enter to Start Game', True,
                                        (0, 0, 0), (255, 255, 255))
    gameover_words = title_font.render('GAME OVER', True, (205, 92, 92),
                                       (255, 255, 255))
    win_words = title_font.render('THE SNAKE IS LONG ENOUGH AND YOU WIN!',
                                  True, (0, 0, 205), (255, 255, 255))
    return {
        'welcome': welcome_words,
        'start': start_game_words,
        'game_over': gameover_words,
        'win': win_words
    }


def main():
    pygame.init()
    fonts = font_setting()
    fps_clock, screen = init(fonts)  # 初始化界面字体等

    snake = Snake()  # 创建snake对象
    direction = snake.move_direction  # 获取初始方向
    while True:
        events = pygame.event.get()  # 获取键盘鼠标事件
        new_direction = press(events, snake)  # 通过按键获取新的方向
        if snake.game_started:
            if new_direction:
                snake.move_direction = new_direction  # 修改蛇的方向
            screen.fill((255, 255, 255))
            if not snake.move():
                # 游戏结束
                snake = game_over(screen, fonts, snake.score)
                direction = snake.move_direction
            else:
                # 游戏继续
                game_continue(screen, snake)

        # 画布更新
        pygame.display.update()
        # 根据速度更新
        fps_clock.tick(snake.speed)


if __name__ == '__main__':
    main()
