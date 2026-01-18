# 第6课：加入得分系统
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("躲避方块游戏 - 得分系统")

clock = pygame.time.Clock()

# 玩家
player_rect = pygame.Rect(275, 350, 50, 50)

# 敌人
enemy_rect = pygame.Rect(random.randint(0, 550), 0, 50, 50)
enemy_speed = 5

# 分数
score = 0
font = pygame.font.Font(None, 36)  # 字体和大小

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 50))

    # 玩家控制
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
        score += 1  # 成功躲过一次加1分

    # 碰撞检测
    if player_rect.colliderect(enemy_rect):
        print("碰撞了！ 游戏结束")
        running = False

    # 绘制
    pygame.draw.rect(screen, (255, 0, 0), player_rect)
    pygame.draw.rect(screen, (0, 255, 0), enemy_rect)

    # 显示分数
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
