#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 11:55:28
@Description: Define control of game
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import consts as cfg
from modules.interface.loadRes import load_resouces


class Control:
    def __init__(self):
        self.done = False
        self.screen, self.clock = self.init_game()
        self.sources = load_resouces()
        self.init_event()
        self.scene = None
        self.scene_dict = {}
        self.scene_name = None
        self.current_time = 0.0

    def init_game(self):
        pygame.init()
        screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pygame.display.set_caption(cfg.ORIGINAL_CAPTION)
        clock = pygame.time.Clock()
        return screen, clock

    def setup_scene(self, scene_dict, start_scene):
        self.scene_dict = scene_dict
        self.scene_name = start_scene
        self.scene = self.scene_dict[self.scene_name]
        self.game_info = {
            'current_time': 0.0,
            'previous_scene': None,
            'current_scene': self.scene_name,
            'next_scene': None,
            'next_loading_time': 0
        }
        self.scene.startup(self.current_time, self.game_info, self.sources)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.scene:
            if self.scene.done:
                self.flip_scene()
            self.scene.update(self.current_time, self.screen, self.event)

    def flip_scene(self):
        previous, self.scene_name = self.scene_name, self.scene.next_scene
        persist = self.scene.cleanup()
        if persist.get('next_loading_time', 0) > 0:
            self.scene_name = 'loading'
        self.scene = self.scene_dict[self.scene_name]
        self.scene.startup(self.current_time, persist, self.sources)

    def event_loop(self):
        self.init_event()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                else:
                    self.event['key_press'][event.key] = True
            elif event.type == pygame.KEYUP:
                self.event['key_up'][event.key] = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event['mouse_pos'] = pygame.mouse.get_pos()
                self.event['mouse_click'] = pygame.mouse.get_pressed()

    def init_event(self):
        self.event = {
            'key_press': {},
            'key_up': {},
            'mouse_pos': None,
            'mouse_click': (0, 0, 0),
        }

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pygame.display.update()
            self.clock.tick(cfg.FPS)
        print('game exit')
