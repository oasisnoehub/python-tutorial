# lesson 5 : collision detection
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Collision Detection")

clock = pygame.time.Clock()

# 玩家
player_rect = pygame.Rect(275, 350, 50, 50)

# 障碍物
enemy_rect = pygame.Rect(random.randint(0, 550), 0, 50, 50)
enemy_speed = 5

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 50))

    # 玩家移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.x < 550:
        player_rect.x += 5

    # 敌人下落
    enemy_rect.y += enemy_speed
    if enemy_rect.y > 400:
        enemy_rect.y = 0
        enemy_rect.x = random.randint(0, 550)

    # 碰撞检测
    if player_rect.colliderect(enemy_rect):
        print("碰撞了！")
        enemy_rect.y = 0
        enemy_rect.x = random.randint(0, 550)

    # 绘制角色和敌人
    pygame.draw.rect(screen, (255, 0, 0), player_rect)
    pygame.draw.rect(screen, (0, 255, 0), enemy_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
