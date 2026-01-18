# 第7课：随机敌人生成
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("多敌人躲避游戏")

clock = pygame.time.Clock()

# 玩家
player_rect = pygame.Rect(275, 350, 50, 50)

# 多个敌人
enemies = []
for _ in range(5):
    enemies.append(pygame.Rect(random.randint(0, 550), random.randint(-400, 0), 50, 50))
enemy_speed = 5

# 分数
score = 0
font = pygame.font.Font(None, 36)

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

    # 敌人移动和碰撞检测
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
