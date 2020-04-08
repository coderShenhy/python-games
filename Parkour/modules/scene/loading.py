#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:31:04
@Description: Define scene of loading
'''
from ..tool import Scene
import consts as cfg
import pygame


class LoadingScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.next_loading_time = 0

    def startup(self, current_time, persist, sources):
        self.persist = persist
        self.next_scene = self.persist.get('next_scene')
        self.loading_time = self.persist.get('next_loading_time')
        self.persist['next_loading_time'] = self.next_loading_time
        self.start_time = current_time

    def update(self, current_time, screen, event):
        if current_time - self.start_time >= self.loading_time:
            self.done = True

        screen.fill(cfg.BLACK)
        self.fill_text(screen)

    def fill_text(self, screen, text='Loading...'):
        font_size = 14
        font = pygame.font.SysFont('arial', font_size)
        font_width, font_height = font.size(str(text))
        screen.blit(font.render(str(text), True, cfg.WHITE),
                    ((cfg.SCREEN_WIDTH - font_width) / 2,
                     (cfg.SCREEN_HEIGHT - font_height - 20)))
