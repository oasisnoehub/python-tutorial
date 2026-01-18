# 第1课：第一个 Pygame 窗口
import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("我的第一个游戏")

# 游戏循环
running = True
while running:
    # 遍历事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出 Pygame
pygame.quit()
