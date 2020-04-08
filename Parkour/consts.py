#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:32:50
@Description: Define constants
'''
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

RESOURCES_PATH = os.path.join(BASE_DIR, 'resources')

ORIGINAL_CAPTION = 'run'
FPS = 60
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 350
FLOOR_HEIGHT = 100
FLOOR_GAP_WIDTH = 150
FLOOR_GAP_HEIGHT = 30
BASE_HEIGHT = SCREEN_HEIGHT - FLOOR_HEIGHT
# floor_width_level, floor_height_level, floor_gap_level
FLOOR_LIST = [(6, 0, 1), (2, -1, 2), (3, 0, 1), (2, 1, 1)] * 10

BACKGROUND_PATH = os.path.join(RESOURCES_PATH, 'background')
BACKGROUND_IMAGES = {
    i: os.path.join(BACKGROUND_PATH, p)
    for i, p in enumerate(os.listdir(BACKGROUND_PATH))
}
BACKGROUND_IMAGES['size'] = (0, 0, 507, 160)

MC_IMAGES_PATH = os.path.join(RESOURCES_PATH, 'role', 'mc4', 'right')
MC_IMAGES = {
    '0': {
        'run': [
            os.path.join(MC_IMAGES_PATH, '1.PNG'),
            os.path.join(MC_IMAGES_PATH, '2.PNG'),
            os.path.join(MC_IMAGES_PATH, '3.PNG'),
            os.path.join(MC_IMAGES_PATH, '4.PNG'),
            os.path.join(MC_IMAGES_PATH, '5.PNG'),
            os.path.join(MC_IMAGES_PATH, '6.PNG'),
            os.path.join(MC_IMAGES_PATH, '7.PNG'),
            os.path.join(MC_IMAGES_PATH, '8.PNG'),
            os.path.join(MC_IMAGES_PATH, '9.PNG'),
            os.path.join(MC_IMAGES_PATH, '10.PNG'),
            os.path.join(MC_IMAGES_PATH, '11.PNG'),
            os.path.join(MC_IMAGES_PATH, '12.PNG'),
        ]
    },
    '2': {
        'image':
        os.path.join(RESOURCES_PATH, 'role', 'mc2.png'),
        'run': [
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '1.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '2.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '3.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '4.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '5.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '6.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '7.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '8.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '9.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '10.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '11.PNG'),
            os.path.join(RESOURCES_PATH, 'role', 'mc3', 'run', '12.PNG'),
        ],
        'jump': [(135, 394, 127, 117)],
        'slide': [(155, 220, 129, 72)],
    },
    '1': {
        'image':
        os.path.join(RESOURCES_PATH, 'role', 'mc1.PNG'),
        'run': [
            (0, 0, 105, 113),
            (105, 0, 104, 113),
            (209, 0, 104, 113),
            (313, 0, 107, 113),
            (420, 0, 109, 113),
            (529, 0, 115, 113),
            (644, 0, 116, 113),
            (761, 0, 108, 113),
            (869, 0, 103, 113),
            (1, 112, 108, 109),
            (110, 113, 115, 102),
        ],
        'jump': [
            os.path.join(RESOURCES_PATH, 'role', '0.PNG'),
            os.path.join(RESOURCES_PATH, 'role', '4.PNG'),
            os.path.join(RESOURCES_PATH, 'role', '12.PNG'),
        ],
        'slide': [(863, 159, 125, 72)],
    }
}
NUM_IMAGES = {
    'image': os.path.join(RESOURCES_PATH, 'num.png'),
    'num': {
        0: (1, 354, 21, 23),
        1: (22, 354, 17, 23),
        2: (39, 354, 21, 23),
        3: (60, 354, 21, 23),
        4: (81, 354, 21, 23),
        5: (102, 354, 21, 23),
        6: (123, 354, 21, 23),
        7: (144, 354, 21, 23),
        8: (165, 354, 21, 23),
        9: (186, 354, 21, 23),
    }
}

TOOL_IMAGE = {
    'image': os.path.join(RESOURCES_PATH, 'ld2.png'),
    'coin': (2, 255, 35, 34),
    'thorn': (4, 126, 53, 126)
}

TOOL_IMAGE2 = {
    'image': os.path.join(RESOURCES_PATH, 'item', 'it2.png'),
    'floor': (74, 5, 120, 320),
    'spine1': (535, 2, 130, 436),
    'spine2': (665, 73, 173, 364),
    'fire': (205, 334, 61, 129)
}

SOUNDS_PATH = os.path.join(RESOURCES_PATH, 'sound')
AUDIO_PATH = os.path.join(RESOURCES_PATH, 'audio')
AUDIOS = {
    'bgm': os.path.join(AUDIO_PATH, 'bgm.mp3'),
}
SOUNDS = {
    'die': os.path.join(SOUNDS_PATH, 'die.wav'),
    'jump': os.path.join(SOUNDS_PATH, 'jump.wav'),
    'slid': os.path.join(SOUNDS_PATH, 'slid.wav'),
    'bgm': os.path.join(SOUNDS_PATH, 'bgm.wav'),
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

JUMP_KEY_CODE = 32  # 空格
SLIDE_KEY_CODE = 83  # s
CONTINUE_GAME_KEY_CODE = 13  # 回车
