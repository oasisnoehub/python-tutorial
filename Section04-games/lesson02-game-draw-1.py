# 第2课：绘制图形和图片
import pygame

pygame.init()

# 设置窗口
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("绘图与图片")

# 加载图片（确保同目录有 player.png）
player_img = pygame.image.load("./images/alien.jpg")
player_x = 100
player_y = 100

running = True
while running:
    # 背景填充颜色
    screen.fill((0, 0, 50))  # 深蓝色背景

    # 绘制图片
    screen.blit(player_img, (player_x, player_y))

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
