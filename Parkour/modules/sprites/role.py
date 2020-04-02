#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import pygame
from consts import FPS, BASE_HEIGHT


class Role(pygame.sprite.Sprite):
    def __init__(self, images, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images['run'][0]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        #
        self.state = 'run'
        self.is_up = False
        self.init_speed()
        self.a_speed = 10 * FPS / 1000
        self.base_height = BASE_HEIGHT

        # 切换形态
        self.role_idx = 0
        self.role_idx_cycle = itertools.cycle(
            [i for i in range(len(self.images['run']))])
        self.role_idx_change_count = 0
        self.role_run_speed = 3

        self.jump2 = False

    def init_speed(self):
        self.up_speed = 10
        self.down_speed = 0
        self.slide_speed = 18

    def update(self):
        if self.state == 'run':
            self.run()
        elif self.state == 'jump':
            self.jump_state()
        elif self.state == 'slide':
            self.slide_state()

    def run(self):
        self.role_idx_change_count += 1
        if self.role_idx_change_count % self.role_run_speed == 0:
            self.role_idx = next(self.role_idx_cycle)
            self.image = self.images['run'][self.role_idx]
            self.change_rect_mask()
            self.rect.bottom = self.base_height
            self.role_idx_change_count = 0

    def jump_state(self):
        if self.is_up:
            # 上升速度越来越小
            self.up_speed -= self.a_speed
            self.rect.top -= self.up_speed
            # 上升速度小于等于0, 改为下降状态
            if self.up_speed <= 0:
                self.is_up = False
                self.init_speed()

        else:
            # 下降速度越来越大
            self.down_speed += self.a_speed
            self.rect.bottom += self.down_speed

            if self.rect.bottom >= self.base_height:
                self.rect.bottom = self.base_height
                self.state = 'run'
                self.init_speed()
                self.jump2 = False

    def jump(self):
        if self.state == 'run':
            self.state = 'jump'
            self.is_up = True
            if not self.images.get('jump'):
                self.image = self.images['run'][3]
            else:
                self.image = self.images['jump'][0]
            self.change_rect_mask()
        elif self.state == 'jump' and not self.jump2:
            self.jump2 = True
            self.is_up = True
            self.up_speed = max(self.up_speed, 5)

    def slide_state(self):
        self.slide_speed -= self.a_speed
        if self.slide_speed <= 0:
            self.init_speed()
            self.state = 'run'

    def slide(self):
        if self.images.get('slide'):
            self.state = 'slide'
            self.image = self.images['slide'][0]
            self.change_rect_mask()
            self.rect.bottom = self.base_height

    def change_rect_mask(self):
        left, top = self.rect.left, self.rect.top
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = left, top

    def draw(self, screen):
        screen.blit(self.image, self.rect)