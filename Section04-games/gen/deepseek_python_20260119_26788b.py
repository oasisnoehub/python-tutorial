import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易Levil Devil")

# 颜色定义
BACKGROUND = (20, 20, 40)
PLAYER_COLOR = (0, 200, 100)
PLATFORM_COLOR = (150, 100, 50)
ENEMY_COLOR = (220, 50, 50)
COIN_COLOR = (255, 215, 0)
GOAL_COLOR = (100, 200, 255)
TEXT_COLOR = (255, 255, 255)
DANGER_COLOR = (255, 100, 0)

# 游戏常量
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
ENEMY_SPEED = 2
FONT = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.width = 30
        self.height = 40
        self.x = WIDTH // 4
        self.y = HEIGHT - 150
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.coins = 0
        self.lives = 3
        self.is_invincible = False
        self.invincible_timer = 0
        
    def update(self, platforms, enemies, coins, goal):
        # 处理左右移动
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            
        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            
        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 屏幕边界限制
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        if self.y > HEIGHT:
            self.y = HEIGHT - self.height
            self.lives -= 1
            self.x = WIDTH // 4
            self.y = HEIGHT - 150
            self.vel_y = 0
        
        # 平台碰撞检测
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            platform_rect = pygame.Rect(platform[0], platform[1], platform[2], platform[3])
            
            # 如果玩家正在下落并且与平台顶部碰撞
            if (player_rect.colliderect(platform_rect) and 
                self.vel_y > 0 and 
                player_rect.bottom <= platform_rect.top + 10):
                self.y = platform_rect.top - self.height
                self.vel_y = 0
                self.on_ground = True
                
            # 如果玩家碰到平台侧面
            elif player_rect.colliderect(platform_rect) and not self.on_ground:
                # 如果从左侧碰撞
                if self.vel_x > 0 and player_rect.right >= platform_rect.left and player_rect.left < platform_rect.left:
                    self.x = platform_rect.left - self.width
                # 如果从右侧碰撞
                elif self.vel_x < 0 and player_rect.left <= platform_rect.right and player_rect.right > platform_rect.right:
                    self.x = platform_rect.right
        
        # 无敌状态处理
        if self.is_invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.is_invincible = False
        
        # 敌人碰撞检测
        if not self.is_invincible:
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if player_rect.colliderect(enemy_rect):
                    self.lives -= 1
                    self.is_invincible = True
                    self.invincible_timer = 60  # 1秒无敌时间
                    # 击退效果
                    if enemy.x < self.x:
                        self.x += 50
                    else:
                        self.x -= 50
                    break
        
        # 硬币收集
        for coin in coins[:]:
            coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
            if player_rect.colliderect(coin_rect):
                self.coins += 1
                coins.remove(coin)
        
        # 目标检测
        goal_rect = pygame.Rect(goal.x, goal.y, goal.width, goal.height)
        if player_rect.colliderect(goal_rect):
            return True  # 到达目标
        return False
        
    def draw(self, screen):
        # 如果无敌状态，闪烁效果
        if not self.is_invincible or (self.is_invincible and pygame.time.get_ticks() % 200 < 100):
            pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))
            # 绘制眼睛
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x + self.width * 0.7), int(self.y + self.height * 0.3)), 6)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width * 0.7), int(self.y + self.height * 0.3)), 3)

class Enemy:
    def __init__(self, x, y, width=30, height=30, move_range=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start_x = x
        self.move_range = move_range
        self.direction = 1  # 1表示向右，-1表示向左
        self.speed = ENEMY_SPEED + random.random() * 1.5
        
    def update(self):
        self.x += self.direction * self.speed
        
        # 改变方向
        if self.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.x < self.start_x - self.move_range:
            self.direction = 1
            
    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x, self.y, self.width, self.height))
        # 绘制眼睛
        eye_offset = 5 if self.direction > 0 else -5
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x + self.width//2 + eye_offset), int(self.y + self.height//3)), 5)
        pygame.draw.circle(screen, (0, 0, 0), 
                          (int(self.x + self.width//2 + eye_offset), int(self.y + self.height//3)), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.float_offset = random.random() * 10
        
    def update(self):
        self.float_offset += 0.1
        
    def draw(self, screen):
        # 浮动效果
        float_y = self.y + 5 * (1 + pygame.math.Vector2(0, self.float_offset).normalize().y)
        pygame.draw.circle(screen, COIN_COLOR, (int(self.x + self.width//2), int(float_y)), self.width//2)
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x + self.width//2), int(float_y)), self.width//4)

class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        
    def draw(self, screen):
        pygame.draw.rect(screen, GOAL_COLOR, (self.x, self.y, self.width, self.height))
        # 绘制门把手
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x + self.width * 0.8), int(self.y + self.height * 0.5)), 5)

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.coins = []
        self.platforms = []
        self.goal = None
        self.level = 1
        self.game_state = "playing"  # playing, game_over, level_complete
        self.timer = 0
        self.setup_level()
        
    def setup_level(self):
        # 清空现有对象
        self.enemies = []
        self.coins = []
        self.platforms = []
        
        # 基础平台
        self.platforms.append((0, HEIGHT - 50, WIDTH, 50))  # 地面
        self.platforms.append((100, HEIGHT - 150, 200, 20))  # 平台1
        self.platforms.append((400, HEIGHT - 250, 150, 20))  # 平台2
        self.platforms.append((200, HEIGHT - 350, 150, 20))  # 平台3
        self.platforms.append((500, HEIGHT - 200, 100, 20))  # 平台4
        self.platforms.append((50, HEIGHT - 400, 100, 20))   # 平台5
        
        # 根据关卡调整难度
        platform_count = 5 + self.level
        for i in range(platform_count):
            x = random.randint(50, WIDTH - 150)
            y = random.randint(100, HEIGHT - 200)
            width = random.randint(80, 200)
            self.platforms.append((x, y, width, 15))
        
        # 添加敌人
        enemy_count = 2 + self.level // 2
        for i in range(enemy_count):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 200)
            move_range = random.randint(50, 150)
            self.enemies.append(Enemy(x, y, 30, 30, move_range))
        
        # 添加硬币
        coin_count = 5 + self.level
        for i in range(coin_count):
            # 确保硬币在平台上
            platform = random.choice(self.platforms)
            x = platform[0] + random.randint(10, platform[2] - 25)
            y = platform[1] - 20
            self.coins.append(Coin(x, y))
        
        # 设置目标位置（在最高平台上）
        highest_platform = min(self.platforms, key=lambda p: p[1])
        self.goal = Goal(highest_platform[0] + highest_platform[2] // 2 - 20, 
                        highest_platform[1] - 60)
        
        # 重置玩家位置
        self.player.x = WIDTH // 4
        self.player.y = HEIGHT - 150
        self.player.vel_x = 0
        self.player.vel_y = 0
        
    def update(self):
        if self.game_state == "playing":
            self.timer += 1
            
            # 更新敌人
            for enemy in self.enemies:
                enemy.update()
                
            # 更新硬币
            for coin in self.coins:
                coin.update()
                
            # 更新玩家并检查是否到达目标
            level_complete = self.player.update(self.platforms, self.enemies, self.coins, self.goal)
            
            if level_complete:
                self.game_state = "level_complete"
                
            if self.player.lives <= 0:
                self.game_state = "game_over"
                
        elif self.game_state == "level_complete":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.level += 1
                self.player.coins = 0  # 保留硬币数
                self.setup_level()
                self.game_state = "playing"
                
        elif self.game_state == "game_over":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.__init__()  # 重置游戏
                
    def draw(self, screen):
        # 绘制背景
        screen.fill(BACKGROUND)
        
        # 绘制装饰性星星
        for i in range(20):
            x = (self.timer // 2 + i * 100) % WIDTH
            y = (i * 30) % HEIGHT
            size = (i % 3) + 1
            pygame.draw.circle(screen, (255, 255, 255), (x, y), size)
        
        # 绘制平台
        for platform in self.platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)
            # 平台顶部高光
            pygame.draw.rect(screen, (180, 130, 70), 
                            (platform[0], platform[1], platform[2], 3))
        
        # 绘制目标
        self.goal.draw(screen)
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # 绘制硬币
        for coin in self.coins:
            coin.draw(screen)
            
        # 绘制玩家
        self.player.draw(screen)
        
        # 绘制UI
        # 生命值
        for i in range(self.player.lives):
            pygame.draw.rect(screen, (255, 50, 50), 
                            (20 + i * 35, 20, 25, 25))
            pygame.draw.polygon(screen, (255, 200, 200), 
                               [(20 + i * 35 + 12, 20 + 5),
                                (20 + i * 35 + 5, 20 + 20),
                                (20 + i * 35 + 20, 20 + 20)])
        
        # 硬币计数
        coin_text = FONT.render(f"硬币: {self.player.coins}", True, COIN_COLOR)
        screen.blit(coin_text, (WIDTH - 150, 20))
        
        # 关卡显示
        level_text = FONT.render(f"关卡: {self.level}", True, TEXT_COLOR)
        screen.blit(level_text, (WIDTH // 2 - 50, 20))
        
        # 游戏状态显示
        if self.game_state == "level_complete":
            # 半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            complete_text = FONT.render("关卡完成!", True, (100, 255, 100))
            instruction_text = FONT.render("按空格键进入下一关", True, TEXT_COLOR)
            
            screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))
            
        elif self.game_state == "game_over":
            # 半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            game_over_text = FONT.render("游戏结束!", True, (255, 50, 50))
            score_text = FONT.render(f"最终分数: {self.player.coins * 10}", True, TEXT_COLOR)
            instruction_text = FONT.render("按空格键重新开始", True, TEXT_COLOR)
            
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))
        
        # 控制说明
        controls_text = [
            "控制: 方向键/WASD移动, 空格键跳跃",
            "目标: 收集所有硬币并到达大门"
        ]
        for i, text in enumerate(controls_text):
            control_surface = pygame.font.SysFont(None, 24).render(text, True, (200, 200, 200))
            screen.blit(control_surface, (10, HEIGHT - 60 + i * 25))

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()