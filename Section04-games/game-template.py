# 第9课：小游戏模板
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("自定义小游戏模板")

clock = pygame.time.Clock()

# 玩家
player_rect = pygame.Rect(275, 350, 50, 50)
player_speed = 5

# 敌人列表（可扩展）
enemies = [pygame.Rect(random.randint(0, 550), random.randint(-400, 0), 50, 50) for _ in range(3)]
enemy_speed = 5

# 分数
score = 0
font = pygame.font.Font(None, 36)

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 50))

    # 玩家移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.x < 550:
        player_rect.x += player_speed

    # 敌人移动和碰撞
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > 400:
            enemy.y = random.randint(-400, 0)
            enemy.x = random.randint(0, 550)
            score += 1
        if player_rect.colliderect(enemy):
            print("碰撞了！ 游戏结束")
            running = False
        pygame.draw.rect(screen, (0, 255, 0), enemy)

    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    # 显示分数
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
