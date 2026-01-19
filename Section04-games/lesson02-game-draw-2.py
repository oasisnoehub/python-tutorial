# lesson 02
import pygame

pygame.init()

# 设置窗口
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("绘图与图片")

running = True
while running:
    # 背景填充颜色
    screen.fill((0, 0, 50))  # 深蓝色背景

    # 绘制形状
    pygame.draw.rect(screen, (5,5, 99), (100, 5, 77,255))  # 红色矩形
    pygame.draw.circle(screen, (9, 5, 99), (30, 200), 40)   # 绿色圆
    pygame.draw.line(screen, (98, 2, 76), (0,0), (600,400), 5) # 黄色线

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
