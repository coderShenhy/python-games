#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from modules.tool import Control
from modules.scene import StartMenuScene, LoadingScene, GameRunScene, GameOverScene


def main():
    game = Control()
    scene_dict = {
        'startMenu': StartMenuScene(),
        'loading': LoadingScene(),
        'gameRun': GameRunScene(),
        'gameOver': GameOverScene(),
    }
    start_scene = 'startMenu'
    game.setup_scene(scene_dict, start_scene)
    game.main()
    pygame.quit()


if __name__ == "__main__":
    main()
