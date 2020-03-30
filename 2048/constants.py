#!/usr/bin/env python3
# -*- coding: utf-8 -*-

FPS = 60
MATRIX_SHAPE = (4, 4)  # 矩阵形状
CELL_SIZE = 80  # 方格大小
MARGIN = 10  # 方格的margin
PADDING = 10  # 方格的padding
SCREEN_WIDTH = (CELL_SIZE + MARGIN) * MATRIX_SHAPE[0] + MARGIN  # 屏幕宽度
SCREEN_HEIGHT = (CELL_SIZE + MARGIN) * MATRIX_SHAPE[1] + MARGIN  # 屏幕高度
FONT_SIZE = CELL_SIZE - PADDING

BACKGROUND_COLOR = "#92877d"  # 背景颜色
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"  # 空方格颜色

# 方格的背景颜色
BACKGROUND_COLOR_DICT = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#eee4da",
    8192: "#edc22e",
    16384: "#f2b179",
    32768: "#f59563",
    65536: "#f67c5f",
}

# 方格中字体颜色
CELL_COLOR_DICT = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
    4096: "#776e65",
    8192: "#f9f6f2",
    16384: "#776e65",
    32768: "#776e65",
    65536: "#f9f6f2",
}
