#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random
from collections import OrderedDict
import pygame

FPS = 60
SHAPE = 4
CELL_SIZE = 100
CELL_GAP_SIZE = 10
MARGIN = 10  # 方格的margin
PADDING = 10  # 方格的padding
SCREEN_WIDTH = (CELL_SIZE + MARGIN) * SHAPE + MARGIN  # 屏幕宽度
SCREEN_HEIGHT = (CELL_SIZE + MARGIN) * SHAPE + MARGIN  # 屏幕高度

BACKGROUND_COLOR = "#92877d"  # 背景颜色
BACKGROUND_EMPTY_CELL_COLOR = "#9e948a"  # 空方格颜色
BACKGROUND_CELL_COLOR = "#edc22e"  # 方格颜色


def tuple_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


class Logic:
    def __init__(self, shape=4):
        self.shape = int(shape) if shape > 2 else 4  # 初始化形状
        self.tiles = OrderedDict()  # 初始化数据
        self.neighbors = [  # 定义方向矢量
            [1, 0],  # 下
            [-1, 0],  # 上
            [0, 1],  # 右
            [0, -1],  # 左
        ]
        self.click_dict = {'x': {}, 'y': {}}  # 定义鼠标点击坐标转换下标的数据
        self.init_load()  # 初始化加载

    def init_load(self):
        count = 1
        # 生成正确的序列
        for x in range(self.shape):
            for y in range(self.shape):
                mark = tuple([x, y])
                self.tiles[mark] = count
                count += 1
        self.tiles[mark] = 0

        for count in range(1000):  # 随机移动一千次
            neighbor = random.choice(self.neighbors)
            spot = tuple_add(mark, neighbor)

            if spot in self.tiles:
                number = self.tiles[spot]
                self.tiles[spot] = 0
                self.tiles[mark] = number
                mark = spot

        self.init_click_dict()

    def init_click_dict(self):
        # 初始化点击坐标转换下标的数据
        for r in range(self.shape):
            for c in range(self.shape):
                x = MARGIN * (c + 1) + c * CELL_SIZE
                x1 = x + CELL_SIZE
                click_x = tuple(range(x, x1))

                self.click_dict['x'][click_x] = c
                y = MARGIN * (r + 1) + r * CELL_SIZE
                y1 = y + CELL_SIZE
                click_y = tuple(range(y, y1))
                self.click_dict['y'][click_y] = r

    def move(self, mark):
        # 移动数据
        for neighbor in self.neighbors:
            spot = tuple_add(mark, neighbor)

            if spot in self.tiles and self.tiles[spot] is 0:
                self.tiles[spot], self.tiles[mark] = self.tiles[
                    mark], self.tiles[spot]
                break

    def click_to_move(self, x, y):
        # 点击移动
        x1 = None
        for k, v in self.click_dict['x'].items():
            if x in k:
                x1 = v

        if x1 is None:
            return
        y1 = None
        for k, v in self.click_dict['y'].items():
            if y in k:
                y1 = v

        if y1 is None:
            return
        self.move((y1, x1))

    def is_win(self):
        # 游戏结束判定
        if self.tiles[(self.shape - 1, self.shape - 1)] is not 0:
            return False
        values = list(self.tiles.values())
        for index in range(values.__len__() - 1):
            if index + 1 != values[index]:
                return False
        return True


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('数字华容道 -- 0')
    return screen


def draw_num(logic, screen):
    for r in range(logic.shape):
        for c in range(logic.shape):
            num = logic.tiles[(r, c)]
            if num is not 0:
                color = pygame.Color(BACKGROUND_CELL_COLOR)
            else:
                color = pygame.Color(BACKGROUND_EMPTY_CELL_COLOR)

            x = MARGIN * (c + 1) + c * CELL_SIZE
            y = MARGIN * (r + 1) + r * CELL_SIZE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            if num is not 0:
                font_size = int((CELL_SIZE - PADDING) / 1.3)
                font = pygame.font.SysFont('arialBlod', font_size)
                font_width, font_height = font.size(str(num))
                screen.blit(font.render(str(num), True, (255, 255, 255)),
                            (x + (CELL_SIZE - font_width) / 2, y +
                             (CELL_SIZE - font_height) / 2 + 5))


def press(is_game_over, logic, COUNT, counts):
    for event in pygame.event.get():
        if event.type == COUNT and not is_game_over:  # 设置定时器，记录时间
            counts += 1
            pygame.display.set_caption('数字华容道 -- {}'.format(counts))
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标点击
            if event.button == 1 and not is_game_over:
                x, y = event.pos
                logic.click_to_move(int(x), int(y))  # 点击移动
        elif event.type == pygame.KEYDOWN and event.key == 13:  # 游戏结束，回车重开
            return True
    if COUNT:
        return counts


def game_win(screen, logic, clock, text='You Win!'):
    font = pygame.font.SysFont('Blod', int(SCREEN_WIDTH / 4))
    font_width, font_height = font.size(str(text))
    while True:
        if press(True, logic, None, None):
            break
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        draw_num(logic, screen)
        screen.blit(font.render(str(text), True, (0, 0, 0)),
                    ((SCREEN_WIDTH - font_width) / 2,
                     (SCREEN_HEIGHT - font_height) / 2))
        pygame.display.update()
        clock.tick(FPS)


def main():
    screen = init_game()
    clock = pygame.time.Clock()
    logic = Logic(SHAPE)
    COUNT = pygame.USEREVENT + 1
    pygame.time.set_timer(COUNT, 1000)
    seconds = 0  # 记录时间
    while True:
        if logic.is_win():  # 判断游戏是否胜利
            break
        seconds = press(False, logic, COUNT, seconds)  # 监控按键
        screen.fill(pygame.Color(BACKGROUND_COLOR))  # 填充背景
        draw_num(logic, screen)  # 画数字
        pygame.display.update()
        clock.tick(FPS)
    game_win(screen, logic, clock, text='Time:' + str(seconds))


if __name__ == "__main__":
    while True:
        main()