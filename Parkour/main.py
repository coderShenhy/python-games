#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random
import pygame
import consts as cfg
from modules.sprites.role import Role
from modules.interface.loadRes import load_resouces


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption('run')
    clock = pygame.time.Clock()
    return screen, clock


def terminate():
    pygame.quit()
    sys.exit()


def press(role, key_press, sources):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_SPACE or key == pygame.K_w:  # 空格键
                if (role.state == 'run'
                        or role.state == 'jump') and not key_press.get(key):
                    sources['sounds']['jump'].play()
                    role.jump()
                    key_press[key] = True
            elif key == pygame.K_s:
                if role.state == 'run' and not key_press.get(key):
                    sources['sounds']['slid'].play()
                    role.slide()
                    key_press[key] = True

        elif event.type == pygame.KEYUP:
            key_press[event.key] = False


def render_background(screen, bg_image):
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0, bg_image.get_width(), bg_image.get_height()))


def main():
    screen, clock = init_game()
    sources = load_resouces()
    bg_image = random.choice(list(sources['bg'].values()))

    role_images = sources['mc']['2']
    role_pos = [
        cfg.SCREEN_WIDTH * 0.15,
        cfg.BASE_HEIGHT - role_images['run'][0].get_height()
    ]
    role = Role(role_images, role_pos)
    key_press = {}
    sources['sounds']['bgm'].play(-1)
    while True:
        press(role, key_press, sources)
        role.update()
        render_background(screen, bg_image)
        role.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)


if __name__ == "__main__":
    main()