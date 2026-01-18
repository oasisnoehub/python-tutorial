# lesson 04
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("帧率控制示例")

clock = pygame.time.Clock()  # 创建时钟对象

player_x = 300
player_y = 200
player_speed = 5

running = True
while running:
    # 设置帧率为 60 FPS (修改看看)
    clock.tick(60)

    screen.fill((0, 0, 50))
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))

    # 键盘控制
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
