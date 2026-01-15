import pygame
import sys

# 初始化
pygame.init()

# 窗口设置
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("抓人游戏")

clock = pygame.time.Clock()

# 颜色
WHITE = (255, 255, 255)
RED = (255, 80, 80)      # 抓的人
BLUE = (80, 80, 255)    # 跑的人
BLACK = (0, 0, 0)

# 角色设置
hunter = pygame.Rect(100, 100, 40, 40)
runner = pygame.Rect(600, 400, 40, 40)

hunter_speed = 3   # 抓的人慢
runner_speed = 5   # 跑的人快

font = pygame.font.SysFont(None, 60)
game_over = False

# 游戏主循环
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        # 抓的人（WASD）
        if keys[pygame.K_w]:
            hunter.y -= hunter_speed
        if keys[pygame.K_s]:
            hunter.y += hunter_speed
        if keys[pygame.K_a]:
            hunter.x -= hunter_speed
        if keys[pygame.K_d]:
            hunter.x += hunter_speed

        # 跑的人（方向键）
        if keys[pygame.K_UP]:
            runner.y -= runner_speed
        if keys[pygame.K_DOWN]:
            runner.y += runner_speed
        if keys[pygame.K_LEFT]:
            runner.x -= runner_speed
        if keys[pygame.K_RIGHT]:
            runner.x += runner_speed

        # 边界限制
        hunter.clamp_ip(screen.get_rect())
        runner.clamp_ip(screen.get_rect())

        # 碰撞检测
        if hunter.colliderect(runner):
            game_over = True

    # 绘制
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, hunter)
    pygame.draw.rect(screen, BLUE, runner)

    if game_over:
        text = font.render("抓到了！", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
        

    pygame.display.flip()
