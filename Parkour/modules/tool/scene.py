#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author: coderShy
@LastEditors: coderShy
@LastEditTime: 2020-04-08 10:34:05
@Description: Define scene abstract base class
'''
from abc import abstractmethod


class Scene():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.next_scene = None
        self.next_loading_time = 0
        self.persist = {}
        self.bgm = None
        self.bg_image = None
        self.key_press = {}

    @abstractmethod
    def startup(self, current_time, persist, sources):
        '''abstract method'''

    def cleanup(self):
        self.done = False
        return self.persist

    @abstractmethod
    def update(self, screen, event, current_time):
        '''abstract method'''

    @abstractmethod
    def set_sources(self, sources):
        '''abstract method'''
