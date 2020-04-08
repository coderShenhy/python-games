#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:30:21
@Description: Define scene of start menu
'''

from ..tool import Scene
import consts as cfg
import pygame


class StartMenuScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.next_scene = 'gameRun'
        self.next_loading_time = 1500

    def startup(self, current_time, persist, sources):
        self.persist = persist
        self.start_time = current_time
        if self.persist['previous_scene']:
            self.persist['previous_scene'] = self.persist['current_scene']
            self.persist['current_scene'] = self.persist['next_scene']
        self.persist['next_scene'] = self.next_scene
        self.persist['next_loading_time'] = self.next_loading_time

    def press(self, event):
        if event['key_press'].get(cfg.CONTINUE_GAME_KEY_CODE):
            self.done = True

    def update(self, current_time, screen, event):
        self.press(event)
        screen.fill(cfg.BLACK)
        self.fill_text(screen)

    def fill_text(self, screen, text='Press Enter To Start'):
        font_size = 24
        font = pygame.font.SysFont('arial', font_size)
        font_width, font_height = font.size(str(text))
        screen.blit(font.render(str(text), True, cfg.WHITE),
                    ((cfg.SCREEN_WIDTH - font_width) / 2,
                     (cfg.SCREEN_HEIGHT - font_height) / 2))
