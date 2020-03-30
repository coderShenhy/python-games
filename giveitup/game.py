#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pygame
from const import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, position, disk_group):
        pygame.sprite.Sprite.__init__(self)
        self.disk_group = disk_group
        self.rect = pygame.Rect(*position, BALL_SIZE, BALL_SIZE)
        self.is_up = False
        self.init_speed()

        self.move_disk = False
        self.min_height = BASE_HEIGHT
        self.can_jump = False
        self.step = 1
        self.change_up_speed = False
        self.move_speed = (DISK_SIZE[0] + DISK_GAP_WIDTH) / 10
        self.move_width = (DISK_SIZE[0] + DISK_GAP_WIDTH) * self.step
        self.current_disk_index = 0

    def init_speed(self, up_speed=1):
        self.up_speed = INIT_SPEED * up_speed
        self.init_a_speed(up_speed)
        self.down_speed = 0

    def init_a_speed(self, a_speed=1):
        self.a_speed = A_SPEED * FPS / 1000 * a_speed

    def change_speed(self, step, change_up_speed):
        self.step = step
        self.change_up_speed = change_up_speed

    def update(self):
        if self.is_up:
            # 上升速度越来越小
            self.up_speed -= self.a_speed
            self.rect.top -= self.up_speed
            # 上升速度小于等于0, 改为下降状态
            if self.up_speed <= 0:
                self.down()
        else:
            # 下降速度越来越大
            self.down_speed += self.a_speed
            self.rect.bottom += self.down_speed

            if self.rect.bottom >= self.min_height - 1:
                self.rect.bottom = self.min_height - 1
                self.up()
                if not self.next_disk:  # 游戏胜利
                    return True
                if not self.current_disk.show:  # 跳到空地
                    return False

    def up(self):
        self.can_jump = False
        if self.change_up_speed:  # 如果要改变速度, 就改变速度
            self.change_up_speed = False
            self.init_speed(SPEED)
        else:
            self.init_speed()
        self.is_up = True
        self.move_disk = True

    def down(self):
        self.init_speed()
        if self.min_height - self.rect.bottom >= BALL_SIZE * 1.2:
            self.init_a_speed(SPEED)
        self.is_up = False
        self.can_jump = True

    @property
    def current_disk(self):
        try:
            return self.disk_group.sprites()[self.current_disk_index]
        except:
            return None

    @property
    def next_disk(self):
        try:
            return self.disk_group.sprites()[self.current_disk_index + 1]
        except:
            return None

    def set_min_height(self):
        self.min_height = self.current_disk.rect.top

    def draw(self, screen):
        for disk in self.disk_group:
            disk.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


class Disk(pygame.sprite.Sprite):
    def __init__(self, position, height, level, show=True):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(*position, DISK_SIZE[0], height)
        self.height = height
        self.level = level
        self.show = show

    def draw(self, screen):
        if not self.show:
            return
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Give it up!')
    return screen


def press(ball):
    if not ball.next_disk:
        return
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == 32 and ball.can_jump:
                if ball.current_disk.level < ball.next_disk.level:
                    step = 1
                    change_speed = True
                else:
                    step = 2
                    change_speed = False
                ball.change_speed(step, change_speed)
                ball.move_width = (DISK_SIZE[0] + DISK_GAP_WIDTH) * ball.step


def init_disk_sptite(FIRST_DISK_POSITION):
    disk_group = pygame.sprite.Group()
    disk_group.add(Disk(FIRST_DISK_POSITION, DISK_HEIGHT, 0))
    for index, i in enumerate(DISK_LIST):
        if i == -1:
            show = False
        else:
            show = True
        if i <= 0:
            height = DISK_HEIGHT
        else:
            height = DISK_INCREMENT * i + DISK_HEIGHT
        disk_group.add(
            Disk((FIRST_DISK_POSITION[0] + (DISK_SIZE[0] + DISK_GAP_WIDTH) *
                  (index + 1), FIRST_DISK_POSITION[1] - height + DISK_HEIGHT),
                 height, i, show))
    return disk_group


def move_disk(ball):
    if ball.move_disk:  # 可以移动柱子
        speed = ball.move_speed * ball.step  # 柱子移动的速度
        for disk in ball.disk_group:  # 移动所有柱子
            disk.rect.left -= speed if ball.move_width > speed else ball.move_width
            if disk.rect.right < 0:  # 删除超过屏幕的柱子
                ball.disk_group.remove(disk)
                ball.current_disk_index -= 1
        ball.move_width -= speed  # 柱子移动的宽度还剩多少

        if ball.move_width < speed:  # 柱子移动完成
            ball.current_disk_index += ball.step
            ball.step = 1
            ball.move_disk = False
            ball.move_width = (DISK_SIZE[0] + DISK_GAP_WIDTH) * ball.step
            ball.set_min_height()  # 设置基础高度


def end_game(screen, ball, win, clock):
    while True:
        if win:
            text = 'You Win'
        else:
            text = 'Press Enter To Restart!'

        font_size = 32
        font = pygame.font.SysFont('arial', font_size)
        font_width, font_height = font.size(text)
        screen.blit(font.render(text, True, (255, 255, 255)),
                    ((SCREEN_WIDTH - font_width) / 2,
                     (SCREEN_HEIGHT - font_height) / 2.5))
        ball.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击关闭按钮退出
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    return
        # 更新画布
        pygame.display.update()
        clock.tick(FPS)


def start_game(screen, ball, clock):
    while True:
        screen.fill((0, 0, 0))
        text = 'Press Space To start!'
        font_size = 32
        font = pygame.font.SysFont('arial', font_size)
        font_width, font_height = font.size(text)
        screen.blit(font.render(text, True, (255, 255, 255)),
                    ((SCREEN_WIDTH - font_width) / 2,
                     (SCREEN_HEIGHT - font_height) / 2.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击关闭按钮退出
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    return
        ball.draw(screen)
        # 更新画布
        pygame.display.update()
        clock.tick(FPS)


def main():
    screen = init_game()
    disk_group = init_disk_sptite(FIRST_DISK_POSITION)
    ball = Ball(BALL_POSITION, disk_group)
    clock = pygame.time.Clock()
    start_game(screen, ball, clock)
    win = False
    while True:
        screen.fill((0, 0, 0))
        move_disk(ball)  # 移动柱子
        press(ball)  # 监控按键
        win = ball.update()  # 移动MC
        if win is not None:
            break
        if ball.next_disk:
            if pygame.sprite.spritecollide(ball, ball.disk_group,
                                           False):  # 判断是否撞柱子
                break
        ball.draw(screen)

        # 更新画布
        pygame.display.update()
        clock.tick(FPS)
    end_game(screen, ball, win, clock)


if __name__ == "__main__":
    while True:
        main()