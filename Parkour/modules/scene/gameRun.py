#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:29:50
@Description: Define scene of game running.
'''

import random
import pygame

from ..tool import Scene
import consts as cfg
from modules.sprites import Role, Floor


class GameRunScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.next_scene = 'gameOver'
        self.next_loading_time = 0

    def startup(self, current_time, persist, sources):
        self.start_time = current_time
        self.role_name = '2'
        self.persist = persist
        self.persist['previous_scene'] = self.persist['current_scene']
        self.persist['current_scene'] = self.persist['next_scene']
        self.persist['next_scene'] = self.next_scene
        self.persist['next_loading_time'] = self.next_loading_time

        self.role, self.floor_sprites = self.init_sprites(
            self.role_name, sources)
        self.sources = sources
        self.set_sources(sources)
        if self.bgm:
            self.bgm.play(-1)

    def set_sources(self, sources):
        self.bg_image = random.choice(list(sources['bg'].values()))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.left, self.bg_rect.top = (0, 0)
        self.bgm = sources['sounds']['bgm']

    def press(self, event):
        key_list = {
            cfg.JUMP_KEY_CODE: {
                'sound': 'jump',
                'func': self.role.jump
            },
            cfg.SLIDE_KEY_CODE: {
                'sound': 'slid',
                'func': self.role.slide
            }
        }
        for key, values in key_list.items():
            if event['key_press'].get(key) and not self.key_press.get(key):
                self.sources['sounds'][values['sound']].play()
                values['func']()
                self.key_press[key] = True
            if event['key_up'].get(key):
                self.key_press[key] = False

    def update(self, current_time, screen, event):
        self.press(event)
        self.role.current_floor = None
        for floor in self.floor_sprites:
            is_del = floor.update()
            if floor.rect.left <= (
                    self.role.rect.right - self.role.rect.width /
                    4) and floor.rect.right >= self.role.rect.centerx:
                self.role.current_floor = floor
            if is_del:
                self.floor_sprites.remove(floor)

        if self.role.update():
            self.done = True

        for floor in self.floor_sprites:
            if pygame.sprite.collide_mask(self.role, floor):
                self.done = True
                print(self.role.rect, floor.rect)

        if not self.done:
            screen.fill(cfg.BLACK)
            if self.bg_image:
                screen.blit(self.bg_image, self.bg_rect)
            self.role.draw(screen)
            for floor in self.floor_sprites:
                floor.draw(screen)

    def init_sprites(self, role_name, sources):
        role_images = sources['mc'][role_name]
        role_pos = [
            cfg.SCREEN_WIDTH * 0.15,
            cfg.BASE_HEIGHT - role_images['run'][0].get_height()
        ]
        role = Role(role_images, role_pos)

        floor_first_pos = [0, cfg.BASE_HEIGHT]
        floor_imgae = sources['tools']['floor']
        imgae_width = floor_imgae.get_width()
        floor_sprites = pygame.sprite.Group()
        x = 0
        y = cfg.BASE_HEIGHT
        for width_level, height_level, gap_level in cfg.FLOOR_LIST:
            y = cfg.BASE_HEIGHT + height_level * cfg.FLOOR_GAP_HEIGHT
            floor = Floor(floor_imgae, (x, y), width_level)
            x += imgae_width * width_level + gap_level * cfg.FLOOR_GAP_WIDTH
            floor_sprites.add(floor)
        return role, floor_sprites
