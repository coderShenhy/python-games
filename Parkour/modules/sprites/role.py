#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:34:53
@Description: Define role
'''
import itertools
import pygame
from consts import FPS, BASE_HEIGHT, SCREEN_HEIGHT


class Role(pygame.sprite.Sprite):
    def __init__(self, images, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images['run'][0]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.rect.top -= 1
        #
        self.state = 'run'  # 定义主角运动状态
        self.is_up = False  # 跳跃状态
        self.init_speed()  # 初始化速度
        self.a_speed = 10 * FPS / 1000
        self.base_height = BASE_HEIGHT

        # 切换形态
        self.role_idx = 0
        self.role_idx_cycle = itertools.cycle(
            [i for i in range(len(self.images['run']))])
        self.role_idx_change_count = 0
        self.role_run_speed = 3
        if not self.images.get('jump'):
            self.jump_image = self.images['run'][3]
        else:
            self.jump_image = self.images['jump'][0]
        self.jump2 = False

        self.current_floor = None

    def init_speed(self):
        self.up_speed = 10
        self.down_speed = 0
        self.slide_speed = 18

    def update(self):
        self.set_base_height()

        if self.state == 'run':
            self.run()
        elif self.state == 'jump':
            if self.jump_state():
                return True
        elif self.state == 'slide':
            self.slide_state()
        elif self.state == 'down':
            if self.down_state():
                return True

    def run(self):  # 奔跑状态切换图片
        self.role_idx_change_count += 1
        if self.role_idx_change_count % self.role_run_speed == 0:
            self.role_idx = next(self.role_idx_cycle)
            self.image = self.images['run'][self.role_idx]
            self.change_rect_mask()
            self.rect.bottom = self.base_height - 1
            self.role_idx_change_count = 0

    def jump_state(self):
        if self.is_up:
            # 上升速度越来越小
            self.up_state()

        else:
            # 下降速度越来越大
            if self.down_state():
                return True

    def up_state(self):
        self.up_speed -= self.a_speed
        self.rect.top -= self.up_speed
        # 上升速度小于等于0, 改为下降状态
        if self.up_speed <= 0:
            self.is_up = False
            self.init_speed()

    def down_state(self):
        self.down_speed += self.a_speed
        self.rect.bottom += self.down_speed

        if self.rect.bottom >= self.base_height - 1:
            self.rect.bottom = self.base_height - 1
            if self.base_height == SCREEN_HEIGHT:
                return True

            self.state = 'run'
            self.init_speed()
            self.jump2 = False

    def jump(self):
        if self.state != 'jump':  # 跳
            self.state = 'jump'
            self.is_up = True
            self.image = self.jump_image
            self.change_rect_mask()
        elif not self.jump2:  # 二段跳
            self.jump2 = True
            self.is_up = True
            self.up_speed = max(self.up_speed, 5)

    def slide_state(self):  # 滑动状态
        self.slide_speed -= self.a_speed
        if self.slide_speed <= 0:
            self.init_speed()
            self.state = 'run'

    def slide(self):
        if self.images.get('slide'):  # 滑动
            self.state = 'slide'
            self.image = self.images['slide'][0]
            self.change_rect_mask()
            self.rect.bottom = self.base_height

    def change_rect_mask(self):
        left, top = self.rect.left, self.rect.top
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = left, top

    def set_base_height(self):
        if self.current_floor:
            self.base_height = self.current_floor.rect.top
        else:
            self.base_height = SCREEN_HEIGHT
            if self.state != 'jump' and self.state != 'down':
                self.image = self.jump_image
                self.change_rect_mask()
                self.state = 'down'

    def draw(self, screen):
        screen.blit(self.image, self.rect)