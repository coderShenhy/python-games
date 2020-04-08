#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 11:45:19
@Description: Define scene of game over
'''

from ..tool import Scene
import consts as cfg
import pygame


class GameOverScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.next_scene = 'startMenu'
        self.next_loading_time = 1000

    def startup(self, current_time, persist, sources):
        self.start_time = current_time
        self.persist = persist
        self.persist['previous_scene'] = self.persist['current_scene']
        self.persist['current_scene'] = self.persist['next_scene']
        self.persist['next_scene'] = self.next_scene
        self.persist['next_loading_time'] = self.next_loading_time

    def update(self, current_time, screen, event):
        if current_time - self.start_time >= 1500:
            self.done = True

        screen.fill(cfg.BLACK)
        self.fill_text(screen)

    def fill_text(self, screen, text='Game Over'):
        font_size = 24
        font = pygame.font.SysFont('arial', font_size)
        font_width, font_height = font.size(str(text))
        screen.blit(font.render(str(text), True, cfg.WHITE),
                    ((cfg.SCREEN_WIDTH - font_width) / 2,
                     (cfg.SCREEN_HEIGHT - font_height) / 2))

    def press(self):
        # 按键返回开始页面
        pass

    def show_score(self):
        # 计算分数
        pass
