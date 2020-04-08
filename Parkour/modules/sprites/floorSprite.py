#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:35:17
@Description: Defin floor class
'''

import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, image, position, width=3, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.rect.width = self.rect.width * width
        self.move_speed = 5
        self.width = width

    def update(self):
        self.rect.left -= self.move_speed
        if self.rect.right < 0:
            return True
        return False

    def draw(self, screen):
        for i in range(self.width):
            screen.blit(self.image,
                        (self.rect.left + self.image.get_width() * i,
                         self.rect.top, self.rect.width, self.rect.height))
