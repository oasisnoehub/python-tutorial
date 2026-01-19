# lesson 03
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("控制角色移动")

# 角色位置
player_x = 300
player_y = 200


player_speed = 9

running = True
while running:
    screen.fill((0, 0, 50))

    # 绘制角色（用矩形代替图片）
    player_rect = pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))

    # 获取键盘按键
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
