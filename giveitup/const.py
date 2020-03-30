#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

FPS = 60
BALL_SIZE = 30
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 288
FLOOR_HEIGHT = 50
BASE_HEIGHT = SCREEN_HEIGHT - FLOOR_HEIGHT
DISK_SIZE = (45, 20)
DISK_HEIGHT = 5
DISK_GAP_WIDTH = 5
DISK_INCREMENT = 25
SPEED = 3
A_SPEED = 5
INIT_SPEED = 3
DISK_LIST = [0, 0, 0, 1, 2, 0, 0, 1, 1, 1, 0, 0, 0, 1] * 10

BALL_POSITION = (150 - BALL_SIZE, BASE_HEIGHT - BALL_SIZE)
FIRST_DISK_POSITION = (BALL_POSITION[0] - (DISK_SIZE[0] - BALL_SIZE) / 2,
                       BASE_HEIGHT)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BALL_IMAGE_PATH = os.path.join(BASE_DIR, 'resources/texture/MC.png')
BACKGROUND_PATH = os.path.join(BASE_DIR, 'resources/texture/bg.png')
DISK_IMAGE_PATH = {
    0: os.path.join(BASE_DIR, 'resources/texture/CL0.png'),
    10: os.path.join(BASE_DIR, 'resources/texture/CLG0.png'),
}
BGM_PATH = [
    os.path.join(BASE_DIR, 'resources/Audio', bgm)
    for bgm in os.listdir(os.path.join(BASE_DIR, 'resources/Audio'))
]
AUDIO_PATHS = {
    'jump': os.path.join(BASE_DIR, 'resources/Sound/jump.wav'),
    'jump2': os.path.join(BASE_DIR, 'resources/Sound/jump2.wav'),
    'die': os.path.join(BASE_DIR, 'resources/Sound/die.wav'),
    'ready': os.path.join(BASE_DIR, 'resources/Sound/ready.ogg'),
}
