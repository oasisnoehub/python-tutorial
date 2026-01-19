import pygame
import sys
import random
import math

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易版塞尔达传说")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
BROWN = (160, 120, 80)
YELLOW = (255, 255, 0)
PURPLE = (180, 50, 230)
LIGHT_BLUE = (100, 200, 255)

# 玩家类
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.sword_length = 900
        self.sword_width = 10
        self.sword_angle = 0
        self.is_attacking = False
        self.attack_cooldown = 0
        self.direction = "down"
        self.invincible = 0
        self.rupees = 0
        self.keys = 0
        
    def move(self, dx, dy, walls):
        # 尝试移动
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 创建玩家矩形用于碰撞检测
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # 检查与墙壁的碰撞
        can_move_x, can_move_y = True, True
        
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                # 如果x方向有碰撞
                if dx != 0:
                    player_rect.x = self.x
                    if not pygame.Rect(player_rect.x, new_y, self.width, self.height).colliderect(wall.rect):
                        can_move_x = False
                # 如果y方向有碰撞
                if dy != 0:
                    player_rect.y = self.y
                    if not pygame.Rect(new_x, player_rect.y, self.width, self.height).colliderect(wall.rect):
                        can_move_y = False
        
        # 更新位置
        if can_move_x:
            self.x = new_x
        if can_move_y:
            self.y = new_y
            
        # 更新方向
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
            
        # 限制玩家在屏幕内
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
    
    def attack(self):
        if self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 20  # 攻击冷却时间
    
    def update(self):
        # 更新攻击状态
        if self.is_attacking:
            self.sword_angle += 15
            if self.sword_angle >= 90:
                self.is_attacking = False
                self.sword_angle = 0
        
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 更新无敌时间
        if self.invincible > 0:
            self.invincible -= 1
    
    def draw(self, screen):
        # 绘制玩家身体
        body_color = GREEN
        if self.invincible > 0 and self.invincible % 4 < 2:
            body_color = WHITE  # 闪烁效果
        
        pygame.draw.rect(screen, body_color, (self.x, self.y, self.width, self.height))
        
        # 绘制玩家眼睛（根据方向）
        eye_offset = 5
        if self.direction == "right":
            pygame.draw.circle(screen, BLUE, (self.x + self.width - eye_offset, self.y + eye_offset), 5)
        elif self.direction == "left":
            pygame.draw.circle(screen, BLUE, (self.x + eye_offset, self.y + eye_offset), 5)
        elif self.direction == "down":
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y + self.height - eye_offset), 5)
        else:  # up
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y + eye_offset), 5)
        
        # 绘制剑（如果正在攻击）
        if self.is_attacking:
            sword_x, sword_y = self.x + self.width // 2, self.y + self.height // 2
            
            # 根据方向调整剑的位置
            if self.direction == "right":
                sword_x = self.x + self.width
                sword_y = self.y + self.height // 2
                angle_rad = math.radians(self.sword_angle)
            elif self.direction == "left":
                sword_x = self.x
                sword_y = self.y + self.height // 2
                angle_rad = math.radians(-self.sword_angle)
            elif self.direction == "down":
                sword_x = self.x + self.width // 2
                sword_y = self.y + self.height
                angle_rad = math.radians(self.sword_angle + 90)
            else:  # up
                sword_x = self.x + self.width // 2
                sword_y = self.y
                angle_rad = math.radians(-self.sword_angle + 90)
            
            # 计算剑的末端位置
            end_x = sword_x + self.sword_length * math.cos(angle_rad)
            end_y = sword_y + self.sword_length * math.sin(angle_rad)
            
            # 绘制剑
            pygame.draw.line(screen, LIGHT_BLUE, (sword_x, sword_y), (end_x, end_y), self.sword_width)
        
        # 绘制生命值条
        health_width = 100
        health_height = 10
        health_x = self.x + self.width // 2 - health_width // 2
        health_y = self.y - 20
        
        # 背景（红色）
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        # 当前生命值（绿色）
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, GREEN, (health_x, health_y, health_width * health_ratio, health_height))
        # 边框
        pygame.draw.rect(screen, WHITE, (health_x, health_y, health_width, health_height), 1)
    
    def get_sword_rect(self):
        # 返回剑的攻击范围矩形
        if not self.is_attacking or self.sword_angle < 30 or self.sword_angle > 60:
            return pygame.Rect(0, 0, 0, 0)
        
        if self.direction == "right":
            return pygame.Rect(self.x + self.width, self.y, self.sword_length, self.height)
        elif self.direction == "left":
            return pygame.Rect(self.x - self.sword_length, self.y, self.sword_length, self.height)
        elif self.direction == "down":
            return pygame.Rect(self.x, self.y + self.height, self.width, self.sword_length)
        else:  # up
            return pygame.Rect(self.x, self.y - self.sword_length, self.width, self.sword_length)

# 敌人类
class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 2
        self.health = 30
        self.enemy_type = enemy_type
        self.color = RED if enemy_type == "basic" else PURPLE
        
        # 不同类型的敌人有不同的属性
        if enemy_type == "fast":
            self.speed = 4
            self.health = 20
            self.color = (255, 150, 50)  # 橙色
        elif enemy_type == "tough":
            self.speed = 1
            self.health = 60
            self.color = (100, 0, 0)  # 深红色
    
    def update(self, player_x, player_y, walls):
        # 计算到玩家的方向
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 如果玩家在附近，则朝玩家移动
        if distance < 300:
            if distance > 0:
                dx, dy = dx/distance, dy/distance
                
                # 尝试移动
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                
                # 检查与墙壁的碰撞
                enemy_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                can_move = True
                
                for wall in walls:
                    if enemy_rect.colliderect(wall.rect):
                        can_move = False
                        break
                
                if can_move:
                    self.x = new_x
                    self.y = new_y
    
    def draw(self, screen):
        # 绘制敌人身体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 绘制敌人眼睛
        pygame.draw.circle(screen, WHITE, (self.x + self.width//3, self.y + self.height//3), 4)
        pygame.draw.circle(screen, WHITE, (self.x + 2*self.width//3, self.y + self.height//3), 4)
        pygame.draw.circle(screen, BLACK, (self.x + self.width//3, self.y + self.height//3), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 2*self.width//3, self.y + self.height//3), 2)
        
        # 绘制生命值条
        health_width = 30
        health_height = 5
        health_x = self.x + self.width // 2 - health_width // 2
        health_y = self.y - 10
        
        # 背景（深红色）
        pygame.draw.rect(screen, (100, 0, 0), (health_x, health_y, health_width, health_height))
        # 当前生命值（红色）
        health_ratio = self.health / 30
        if self.enemy_type == "fast":
            health_ratio = self.health / 20
        elif self.enemy_type == "tough":
            health_ratio = self.health / 60
            
        health_color = (int(255 * (1 - health_ratio)), int(255 * health_ratio), 0)
        pygame.draw.rect(screen, health_color, (health_x, health_y, health_width * health_ratio, health_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 墙壁类
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)
        # 添加一些纹理
        for i in range(0, self.rect.width, 10):
            for j in range(0, self.rect.height, 10):
                pygame.draw.rect(screen, (140, 100, 60), 
                                (self.rect.x + i, self.rect.y + j, 8, 8))

# 物品类
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.item_type = item_type  # "rupee", "heart", "key"
        self.collected = False
        
        # 设置物品颜色
        if item_type == "rupee":
            self.color = BLUE
        elif item_type == "heart":
            self.color = RED
        elif item_type == "key":
            self.color = YELLOW
    
    def draw(self, screen):
        if not self.collected:
            if self.item_type == "rupee":
                # 绘制菱形（卢比形状）
                points = [
                    (self.x + self.width//2, self.y),
                    (self.x + self.width, self.y + self.height//2),
                    (self.x + self.width//2, self.y + self.height),
                    (self.x, self.y + self.height//2)
                ]
                pygame.draw.polygon(screen, self.color, points)
            elif self.item_type == "heart":
                # 绘制心形
                pygame.draw.circle(screen, self.color, (self.x + self.width//3, self.y + self.height//3), self.width//3)
                pygame.draw.circle(screen, self.color, (self.x + 2*self.width//3, self.y + self.height//3), self.width//3)
                pygame.draw.polygon(screen, self.color, [
                    (self.x, self.y + self.height//3),
                    (self.x + self.width, self.y + self.height//3),
                    (self.x + self.width//2, self.y + self.height)
                ])
            elif self.item_type == "key":
                # 绘制钥匙
                pygame.draw.rect(screen, self.color, (self.x + self.width//3, self.y, self.width//3, self.height))
                pygame.draw.circle(screen, self.color, (self.x + self.width//2, self.y + self.height//3), self.width//3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 门类
class Door:
    def __init__(self, x, y, width, height, locked=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.locked = locked
        self.open = False
    
    def draw(self, screen):
        if self.open:
            # 绘制打开的门
            pygame.draw.rect(screen, (120, 80, 40), self.rect)
        else:
            # 绘制关闭的门
            pygame.draw.rect(screen, (100, 60, 20), self.rect)
            
            if self.locked:
                # 绘制锁
                lock_rect = pygame.Rect(
                    self.rect.x + self.rect.width//2 - 5,
                    self.rect.y + self.rect.height//2 - 10,
                    10, 20
                )
                pygame.draw.rect(screen, YELLOW, lock_rect)
                pygame.draw.circle(screen, YELLOW, 
                                  (self.rect.x + self.rect.width//2, 
                                   self.rect.y + self.rect.height//2 + 5), 5)

# 初始化游戏对象
def init_game():
    global player, enemies, walls, items, doors, game_over, game_win, current_room
    
    # 创建玩家
    player = Player(100, 100)
    
    # 创建墙壁
    walls = [
        # 边界墙
        Wall(0, 0, WIDTH, 20),
        Wall(0, 0, 20, HEIGHT),
        Wall(0, HEIGHT-20, WIDTH, 20),
        Wall(WIDTH-20, 0, 20, HEIGHT),
        
        # 内部墙
        Wall(200, 100, 20, 200),
        Wall(400, 300, 300, 20),
        Wall(100, 400, 200, 20),
        Wall(500, 100, 20, 150),
        Wall(300, 200, 150, 20),
    ]
    
    # 创建门
    doors = [
        Door(600, 250, 40, 20, True),
        Door(700, 500, 20, 40, False),
    ]
    
    # 创建敌人
    enemies = [
        Enemy(300, 300, "basic"),
        Enemy(500, 200, "fast"),
        Enemy(200, 500, "tough"),
        Enemy(600, 400, "basic"),
    ]
    
    # 创建物品
    items = [
        Item(150, 150, "rupee"),
        Item(250, 250, "heart"),
        Item(350, 350, "rupee"),
        Item(450, 450, "key"),
        Item(550, 150, "heart"),
        Item(650, 350, "rupee"),
    ]
    
    # 游戏状态
    game_over = False
    game_win = False
    current_room = 1

# 绘制游戏界面
def draw_game():
    # 绘制背景
    screen.fill((50, 100, 50))  # 草地颜色
    
    # 绘制墙壁
    for wall in walls:
        wall.draw(screen)
    
    # 绘制门
    for door in doors:
        door.draw(screen)
    
    # 绘制物品
    for item in items:
        item.draw(screen)
    
    # 绘制敌人
    for enemy in enemies:
        enemy.draw(screen)
    
    # 绘制玩家
    player.draw(screen)
    
    # 绘制UI
    draw_ui()
    
    # 如果游戏结束，显示游戏结束画面
    if game_over:
        draw_game_over()
    
    # 如果游戏胜利，显示胜利画面
    if game_win:
        draw_game_win()

# 绘制UI
def draw_ui():
    # 绘制玩家状态
    font = pygame.font.SysFont(None, 36)
    
    # 绘制卢比数量
    rupee_text = font.render(f"卢比: {player.rupees}", True, BLUE)
    screen.blit(rupee_text, (10, 10))
    
    # 绘制钥匙数量
    key_text = font.render(f"钥匙: {player.keys}", True, YELLOW)
    screen.blit(key_text, (10, 50))
    
    # 绘制房间编号
    room_text = font.render(f"房间: {current_room}", True, WHITE)
    screen.blit(room_text, (WIDTH - 120, 10))
    
    # 绘制操作说明
    font_small = pygame.font.SysFont(None, 24)
    controls = [
        "方向键: 移动",
        "空格键: 攻击",
        "R: 重新开始",
        "ESC: 退出游戏"
    ]
    
    for i, text in enumerate(controls):
        control_text = font_small.render(text, True, WHITE)
        screen.blit(control_text, (WIDTH - 200, 50 + i * 30))

# 绘制游戏结束画面
def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 36)
    
    game_over_text = font_large.render("游戏结束", True, RED)
    restart_text = font_medium.render("按 R 键重新开始", True, WHITE)
    quit_text = font_medium.render("按 ESC 键退出游戏", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 50))

# 绘制游戏胜利画面
def draw_game_win():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 50, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 36)
    
    win_text = font_large.render("恭喜通关！", True, YELLOW)
    stats_text = font_medium.render(f"收集卢比: {player.rupees}/6", True, WHITE)
    restart_text = font_medium.render("按 R 键重新开始", True, WHITE)
    quit_text = font_medium.render("按 ESC 键退出游戏", True, WHITE)
    
    screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, HEIGHT//2 - 30))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 80))

# 更新游戏状态
def update_game():
    global game_over, game_win
    
    if game_over or game_win:
        return
    
    # 更新玩家
    player.update()
    
    # 更新敌人
    for enemy in enemies:
        enemy.update(player.x, player.y, walls)
    
    # 检查玩家与敌人的碰撞
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    
    for enemy in enemies[:]:
        if player_rect.colliderect(enemy.get_rect()) and player.invincible == 0:
            player.health -= 10
            player.invincible = 30  # 无敌时间
            
            if player.health <= 0:
                game_over = True
    
    # 检查玩家攻击
    if player.is_attacking:
        sword_rect = player.get_sword_rect()
        
        for enemy in enemies[:]:
            if sword_rect.colliderect(enemy.get_rect()):
                enemy.health -= 20
                
                if enemy.health <= 0:
                    enemies.remove(enemy)
    
    # 检查玩家与物品的碰撞
    for item in items[:]:
        if not item.collected and player_rect.colliderect(item.get_rect()):
            item.collected = True
            
            if item.item_type == "rupee":
                player.rupees += 1
            elif item.item_type == "heart":
                player.health = min(player.max_health, player.health + 30)
            elif item.item_type == "key":
                player.keys += 1
    
    # 检查玩家与门的碰撞
    for door in doors:
        if player_rect.colliderect(door.rect):
            if door.locked and player.keys > 0:
                door.locked = False
                player.keys -= 1
                door.open = True
            elif not door.locked:
                door.open = True
                
                # 如果玩家到达最后一个门，游戏胜利
                if door.rect.x > 600:
                    if player.rupees >= 4:  # 收集至少4个卢比才能通关
                        game_win = True
    
    # 检查是否所有敌人都被击败
    if not enemies and current_room == 1:
        # 打开所有门
        for door in doors:
            door.locked = False

# 初始化游戏
init_game()

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_r:
                init_game()  # 重新开始游戏
            
            if event.key == pygame.K_SPACE and not game_over and not game_win:
                player.attack()
    
    # 获取按键状态
    keys = pygame.key.get_pressed()
    
    # 处理玩家移动
    if not game_over and not game_win:
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        
        player.move(dx, dy, walls)
    
    # 更新游戏状态
    update_game()
    
    # 绘制游戏
    draw_game()
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()