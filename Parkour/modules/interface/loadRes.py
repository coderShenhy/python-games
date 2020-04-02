#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import consts as cfg


def load_background():
    bg_size = cfg.BACKGROUND_IMAGES.get('size')
    if bg_size:
        cfg.BACKGROUND_IMAGES.pop('size')
    return {
        key: pygame.transform.smoothscale(
            pygame.image.load(value).convert_alpha().subsurface(
                pygame.Rect(*bg_size)), (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        for key, value in cfg.BACKGROUND_IMAGES.items()
    }


def load_player():
    mc_images = dict()
    for name, values in cfg.MC_IMAGES.items():
        mc_images[name] = {}
        if values.get('image'):
            img_path = values.pop('image')
            image = pygame.image.load(img_path).convert_alpha()
            for k, v in values.items():
                if all([isinstance(i, str) for i in v]):
                    mc_images[name][k] = [
                        pygame.image.load(value).convert_alpha() for value in v
                    ]
                if all([isinstance(i, tuple) for i in v]):
                    mc_images[name][k] = [
                        image.subsurface(pygame.Rect(*rect)) for rect in v
                    ]
        else:
            for k, v in values.items():
                mc_images[name][k] = [
                    pygame.image.load(value).convert_alpha() for value in v
                ]
    for name, values in mc_images.items():
        for k, v in values.items():
            mc_images[name][k] = [
                pygame.transform.smoothscale(
                    i, (int(i.get_width() / 1.5), int(i.get_height() / 1.5)))
                for i in v
            ]
    return mc_images


def load_nums():
    image = pygame.image.load(cfg.NUM_IMAGES.get('image')).convert_alpha()
    nums = {
        k: image.subsurface(pygame.Rect(*v))
        for k, v in cfg.NUM_IMAGES.get('num', {}).items()
    }
    return nums


def load_resouces():
    background_images = load_background()
    mc_images = load_player()
    nums = load_nums()

    tool1 = pygame.image.load(cfg.TOOL_IMAGE.get('image'))
    cfg.TOOL_IMAGE.pop('image')
    tool2 = pygame.image.load(cfg.TOOL_IMAGE2.get('image'))
    cfg.TOOL_IMAGE2.pop('image')
    tools = {
        k: tool1.subsurface(pygame.Rect(*v))
        for k, v in cfg.TOOL_IMAGE.items()
    }
    tools.update({
        k: tool2.subsurface(pygame.Rect(*v))
        for k, v in cfg.TOOL_IMAGE2.items()
    })

    sounds = {
        key: pygame.mixer.Sound(value)
        for key, value in cfg.SOUNDS.items()
    }
    for k, v in sounds.items():
        v.set_volume(0.2)

    return {
        'bg': background_images,
        'mc': mc_images,
        'sounds': sounds,
        'nums': nums,
        'tools': tools
    }
