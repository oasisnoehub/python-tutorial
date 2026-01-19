import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (180, 70, 230)
LIGHT_BLUE = (100, 200, 255)
GRAY = (100, 100, 100)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("塞尔达传说：王国之泪 - 简化版")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        self.speed = 4
        self.health = 10
        self.max_health = 10
        self.direction = "down"
        self.has_sword = False
        self.has_bow = False
        self.keys = 0
        self.rupees = 0
        self.invincible = 0
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 更新方向
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
        
        # 检查碰撞
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # 地图边界
        if (new_x < 0 or new_x > game_map.width * TILE_SIZE - self.width or
            new_y < 0 or new_y > game_map.height * TILE_SIZE - self.height):
            return
        
        # 检查地图碰撞
        tile_x1 = int(new_x // TILE_SIZE)
        tile_x2 = int((new_x + self.width - 1) // TILE_SIZE)
        tile_y1 = int(new_y // TILE_SIZE)
        tile_y2 = int((new_y + self.height - 1) // TILE_SIZE)
        
        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if 0 <= y < game_map.height and 0 <= x < game_map.width:
                    tile = game_map.tiles[y][x]
                    # 不可通过的方块
                    if tile in ["#", "T", "R", "W", "D", "C"]:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if player_rect.colliderect(tile_rect):
                            return
        
        # 可以移动
        self.x = new_x
        self.y = new_y
        
        # 检查与物品的碰撞
        self.check_item_collisions(game_map.items)
        
        # 检查与敌人的碰撞
        self.check_enemy_collisions(game_map.enemies)
        
        # 检查与门的碰撞
        self.check_door_collision(game_map)
        
        # 检查与宝箱的碰撞
        self.check_chest_collision(game_map)
    
    def check_item_collisions(self, items):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for item in items[:]:
            item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
            if player_rect.colliderect(item_rect):
                if item.type == "sword":
                    self.has_sword = True
                    game_map.message = "获得剑！按Z攻击"
                    game_map.message_timer = 120
                elif item.type == "bow":
                    self.has_bow = True
                    game_map.message = "获得弓！按X射击"
                    game_map.message_timer = 120
                elif item.type == "key":
                    self.keys += 1
                    game_map.message = f"获得钥匙！现在有{self.keys}把钥匙"
                    game_map.message_timer = 120
                elif item.type == "heart":
                    self.health = min(self.max_health, self.health + 4)
                    game_map.message = "生命值恢复！"
                    game_map.message_timer = 120
                elif item.type == "rupee":
                    self.rupees += 5
                    game_map.message = f"+5卢比！总计: {self.rupees}"
                    game_map.message_timer = 120
                
                items.remove(item)
    
    def check_enemy_collisions(self, enemies):
        if self.invincible > 0:
            return
            
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                self.take_damage(1)
                break
    
    def check_door_collision(self, game_map):
        for y in range(game_map.height):
            for x in range(game_map.width):
                if game_map.tiles[y][x] == "D":
                    door_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                    if player_rect.colliderect(door_rect):
                        if self.keys > 0:
                            self.keys -= 1
                            game_map.tiles[y][x] = "."
                            game_map.message = "门打开了！"
                            game_map.message_timer = 120
                        else:
                            game_map.message = "门锁着！需要钥匙"
                            game_map.message_timer = 120
                        return
    
    def check_chest_collision(self, game_map):
        for y in range(game_map.height):
            for x in range(game_map.width):
                if game_map.tiles[y][x] == "C":
                    chest_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                    if player_rect.colliderect(chest_rect):
                        game_map.game_state = "VICTORY"
                        game_map.message = "你找到了宝藏！游戏胜利！"
                        game_map.message_timer = 240
    
    def take_damage(self, amount):
        self.health -= amount
        self.invincible = 60  # 1秒无敌时间
        
        if self.health <= 0:
            self.health = 0
            game_map.game_state = "GAME_OVER"
            game_map.message = "游戏结束！按R重新开始"
            game_map.message_timer = 300
    
    def update(self):
        if self.invincible > 0:
            self.invincible -= 1
    
    def draw(self, screen, camera_x, camera_y):
        # 绘制玩家
        player_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        
        # 根据方向改变颜色
        if self.direction == "up":
            color = (0, 200, 0)
        elif self.direction == "down":
            color = (0, 180, 0)
        elif self.direction == "left":
            color = (0, 160, 0)
        elif self.direction == "right":
            color = (0, 140, 0)
        else:
            color = GREEN
        
        # 受伤时闪烁
        if self.invincible > 0 and self.invincible % 10 < 5:
            color = RED
        
        pygame.draw.rect(screen, color, player_rect)
        
        # 绘制眼睛
        if self.direction == "up":
            eye_x = player_rect.x + player_rect.width // 2
            eye_y = player_rect.y + 10
        elif self.direction == "down":
            eye_x = player_rect.x + player_rect.width // 2
            eye_y = player_rect.y + player_rect.height - 10
        elif self.direction == "left":
            eye_x = player_rect.x + 10
            eye_y = player_rect.y + player_rect.height // 2
        else:  # right
            eye_x = player_rect.x + player_rect.width - 10
            eye_y = player_rect.y + player_rect.height // 2
        
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 2)

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        
        if enemy_type == "bokoblin":
            self.color = RED
            self.health = 4
            self.speed = 2
        elif enemy_type == "keese":
            self.color = PURPLE
            self.health = 2
            self.speed = 3
        elif enemy_type == "octorok":
            self.color = BROWN
            self.health = 3
            self.speed = 1
        
        self.direction = random.choice(["up", "down", "left", "right"])
        self.move_timer = random.randint(30, 90)
        self.attack_timer = 0
        
    def update(self, game_map):
        # 移动
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.direction = random.choice(["up", "down", "left", "right"])
            self.move_timer = random.randint(30, 90)
        
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -1
        elif self.direction == "down":
            dy = 1
        elif self.direction == "left":
            dx = -1
        elif self.direction == "right":
            dx = 1
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 检查碰撞
        enemy_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # 地图边界
        if (new_x < 0 or new_x > game_map.width * TILE_SIZE - self.width or
            new_y < 0 or new_y > game_map.height * TILE_SIZE - self.height):
            self.direction = random.choice(["up", "down", "left", "right"])
            self.move_timer = random.randint(30, 90)
            return
        
        # 检查地图碰撞
        tile_x1 = int(new_x // TILE_SIZE)
        tile_x2 = int((new_x + self.width - 1) // TILE_SIZE)
        tile_y1 = int(new_y // TILE_SIZE)
        tile_y2 = int((new_y + self.height - 1) // TILE_SIZE)
        
        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if 0 <= y < game_map.height and 0 <= x < game_map.width:
                    tile = game_map.tiles[y][x]
                    if tile in ["#", "T", "R", "W", "D", "C"]:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if enemy_rect.colliderect(tile_rect):
                            self.direction = random.choice(["up", "down", "left", "right"])
                            self.move_timer = random.randint(30, 90)
                            return
        
        # 可以移动
        self.x = new_x
        self.y = new_y
        
        # 攻击冷却
        if self.attack_timer > 0:
            self.attack_timer -= 1
        
    def take_damage(self, amount):
        self.health -= amount
        
    def is_dead(self):
        return self.health <= 0
    
    def draw(self, screen, camera_x, camera_y):
        enemy_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        
        pygame.draw.rect(screen, self.color, enemy_rect)
        
        # 绘制眼睛
        pygame.draw.circle(screen, WHITE, 
                          (enemy_rect.x + enemy_rect.width // 3, 
                           enemy_rect.y + enemy_rect.height // 3), 
                          4)
        pygame.draw.circle(screen, BLACK, 
                          (enemy_rect.x + enemy_rect.width // 3, 
                           enemy_rect.y + enemy_rect.height // 3), 
                          2)

class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.type = item_type
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        
    def draw(self, screen, camera_x, camera_y):
        item_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        
        if self.type == "sword":
            pygame.draw.rect(screen, (200, 200, 200), item_rect)
            pygame.draw.rect(screen, BROWN, 
                            (item_rect.x + item_rect.width // 2 - 5, 
                             item_rect.y + 5, 
                             10, item_rect.height - 10))
        elif self.type == "bow":
            pygame.draw.ellipse(screen, (150, 100, 50), item_rect)
        elif self.type == "key":
            pygame.draw.rect(screen, YELLOW, item_rect)
            pygame.draw.rect(screen, YELLOW, 
                            (item_rect.x + item_rect.width // 2 - 10, 
                             item_rect.y + item_rect.height // 2 - 3, 
                             20, 6))
        elif self.type == "heart":
            # 绘制心形
            points = [
                (item_rect.x + item_rect.width // 2, item_rect.y + 5),
                (item_rect.x + 5, item_rect.y + item_rect.height // 2),
                (item_rect.x + item_rect.width // 2, item_rect.y + item_rect.height - 5),
                (item_rect.x + item_rect.width - 5, item_rect.y + item_rect.height // 2)
            ]
            pygame.draw.polygon(screen, RED, points)
        elif self.type == "rupee":
            points = [
                (item_rect.x + item_rect.width // 2, item_rect.y),
                (item_rect.x + item_rect.width - 5, item_rect.y + item_rect.height // 3),
                (item_rect.x + item_rect.width - 5, item_rect.y + 2 * item_rect.height // 3),
                (item_rect.x + item_rect.width // 2, item_rect.y + item_rect.height),
                (item_rect.x + 5, item_rect.y + 2 * item_rect.height // 3),
                (item_rect.x + 5, item_rect.y + item_rect.height // 3)
            ]
            pygame.draw.polygon(screen, (0, 200, 255), points)

class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 8
        self.height = 8
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen, camera_x, camera_y):
        proj_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        pygame.draw.rect(screen, YELLOW, proj_rect)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.player = None
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.camera_x = 0
        self.camera_y = 0
        self.game_state = "PLAYING"
        self.message = ""
        self.message_timer = 0
        
        self.generate_map()
        
    def generate_map(self):
        # 生成随机地图
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    row.append("#")  # 墙
                else:
                    rand = random.random()
                    if rand < 0.7:
                        row.append(".")  # 草地
                    elif rand < 0.8:
                        row.append("T")  # 树
                    elif rand < 0.85:
                        row.append("W")  # 水
                    elif rand < 0.9:
                        row.append("R")  # 岩石
                    else:
                        row.append("#")  # 墙
            self.tiles.append(row)
        
        # 玩家起始位置
        player_x, player_y = 5, 5
        self.player = Player(player_x * TILE_SIZE + TILE_SIZE // 4, 
                            player_y * TILE_SIZE + TILE_SIZE // 4)
        
        # 钥匙位置
        self.add_item_at_random("key")
        
        # 门位置
        self.tiles[self.height//2][self.width-2] = "D"
        
        # 宝箱位置
        self.tiles[self.height//2][self.width-3] = "C"
        
        # 添加物品
        self.add_item_at_position(3, 7, "sword")
        self.add_item_at_position(15, 3, "bow")
        
        # 添加心
        for _ in range(3):
            self.add_item_at_random("heart")
        
        # 添加卢比
        for _ in range(5):
            self.add_item_at_random("rupee")
        
        # 生成敌人
        for _ in range(8):
            self.add_enemy_at_random()
    
    def add_item_at_random(self, item_type):
        x = random.randint(2, self.width-3)
        y = random.randint(2, self.height-3)
        if self.tiles[y][x] == ".":
            self.items.append(Item(x * TILE_SIZE + TILE_SIZE // 4,
                                  y * TILE_SIZE + TILE_SIZE // 4,
                                  item_type))
    
    def add_item_at_position(self, x, y, item_type):
        self.items.append(Item(x * TILE_SIZE + TILE_SIZE // 4,
                              y * TILE_SIZE + TILE_SIZE // 4,
                              item_type))
    
    def add_enemy_at_random(self):
        x = random.randint(2, self.width-3)
        y = random.randint(2, self.height-3)
        if self.tiles[y][x] == ".":
            enemy_type = random.choice(["bokoblin", "keese", "octorok"])
            self.enemies.append(Enemy(x * TILE_SIZE + TILE_SIZE // 4,
                                      y * TILE_SIZE + TILE_SIZE // 4,
                                      enemy_type))
    
    def update_camera(self):
        # 将相机中心对准玩家
        self.camera_x = self.player.x - SCREEN_WIDTH // 2 + self.player.width // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2 + self.player.height // 2
        
        # 限制相机范围
        self.camera_x = max(0, min(self.camera_x, self.width * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.height * TILE_SIZE - SCREEN_HEIGHT))
    
    def update(self):
        if self.game_state != "PLAYING":
            if self.message_timer > 0:
                self.message_timer -= 1
            return
        
        # 更新玩家
        self.player.update()
        
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.update(self)
            if enemy.is_dead():
                self.enemies.remove(enemy)
                # 敌人有几率掉落物品
                if random.random() < 0.3:
                    item_type = random.choice(["heart", "rupee"])
                    self.items.append(Item(enemy.x, enemy.y, item_type))
        
        # 更新弹射物
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # 检查弹射物是否击中敌人
            proj_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if proj_rect.colliderect(enemy_rect):
                    enemy.take_damage(1)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # 检查弹射物边界
            if (projectile.x < 0 or projectile.x > self.width * TILE_SIZE or
                projectile.y < 0 or projectile.y > self.height * TILE_SIZE):
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
        
        # 更新相机
        self.update_camera()
        
        # 更新消息计时器
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""
    
    def draw(self, screen):
        # 绘制地图
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * TILE_SIZE - self.camera_x,
                    y * TILE_SIZE - self.camera_y,
                    TILE_SIZE, TILE_SIZE
                )
                
                tile = self.tiles[y][x]
                
                if tile == "#":  # 墙
                    pygame.draw.rect(screen, BROWN, rect)
                elif tile == "T":  # 树
                    pygame.draw.rect(screen, (0, 100, 0), rect)
                    pygame.draw.circle(screen, (0, 150, 0), 
                                      (rect.x + TILE_SIZE//2, rect.y + TILE_SIZE//3), 
                                      TILE_SIZE//2)
                elif tile == "W":  # 水
                    pygame.draw.rect(screen, BLUE, rect)
                elif tile == "R":  # 岩石
                    pygame.draw.rect(screen, GRAY, rect)
                elif tile == "D":  # 门
                    pygame.draw.rect(screen, (100, 50, 0), rect)
                    pygame.draw.circle(screen, YELLOW, 
                                      (rect.x + TILE_SIZE//2, rect.y + TILE_SIZE//2), 
                                      5)
                elif tile == "C":  # 宝箱
                    pygame.draw.rect(screen, (150, 75, 0), rect)
                    pygame.draw.rect(screen, (180, 90, 0), 
                                    (rect.x, rect.y, TILE_SIZE, TILE_SIZE//3))
                else:  # 草地
                    pygame.draw.rect(screen, GREEN, rect)
        
        # 绘制物品
        for item in self.items:
            item.draw(screen, self.camera_x, self.camera_y)
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen, self.camera_x, self.camera_y)
        
        # 绘制弹射物
        for projectile in self.projectiles:
            projectile.draw(screen, self.camera_x, self.camera_y)
        
        # 绘制玩家
        self.player.draw(screen, self.camera_x, self.camera_y)
        
        # 绘制UI
        self.draw_ui(screen)
        
        # 绘制消息
        if self.message:
            self.draw_message(screen)
        
        # 绘制游戏状态
        if self.game_state == "GAME_OVER":
            self.draw_game_over(screen)
        elif self.game_state == "VICTORY":
            self.draw_victory(screen)
    
    def draw_ui(self, screen):
        # 绘制生命值
        heart_size = 30
        for i in range(self.player.max_health // 2):
            x = 20 + i * (heart_size + 5)
            y = 20
            
            # 绘制心形
            if i < self.player.health // 2:
                color = RED
            else:
                color = (100, 0, 0)
            
            points = [
                (x + heart_size // 2, y + 5),
                (x + 5, y + heart_size // 2),
                (x + heart_size // 2, y + heart_size - 5),
                (x + heart_size - 5, y + heart_size // 2)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (150, 0, 0), points, 2)
        
        # 绘制钥匙数量
        font = pygame.font.Font(None, 36)
        key_text = font.render(f"钥匙: {self.player.keys}", True, YELLOW)
        screen.blit(key_text, (SCREEN_WIDTH - 150, 20))
        
        # 绘制卢比数量
        rupee_text = font.render(f"卢比: {self.player.rupees}", True, (0, 200, 255))
        screen.blit(rupee_text, (SCREEN_WIDTH - 150, 60))
        
        # 绘制控制说明
        controls = [
            "移动: 方向键",
            "攻击: Z",
            "射击: X",
            "背包: I",
            "暂停: P"
        ]
        
        for i, control in enumerate(controls):
            control_text = font.render(control, True, WHITE)
            screen.blit(control_text, (SCREEN_WIDTH - 200, 100 + i * 30))
    
    def draw_message(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(self.message, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        
        # 半透明背景
        bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
                             text_rect.width + 20, text_rect.height + 10)
        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)
        
        screen.blit(text, text_rect)
    
    def draw_game_over(self, screen):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # 游戏结束文本
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        game_over_text = font_large.render("游戏结束", True, RED)
        restart_text = font_small.render("按R重新开始，按ESC退出", True, WHITE)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 30))
    
    def draw_victory(self, screen):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # 胜利文本
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        victory_text = font_large.render("胜利！", True, YELLOW)
        congrats_text = font_small.render("你找到了宝藏！", True, WHITE)
        restart_text = font_small.render("按R重新开始，按ESC退出", True, WHITE)
        
        screen.blit(victory_text, 
                   (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 80))
        screen.blit(congrats_text, 
                   (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 50))

# 创建游戏地图
game_map = GameMap(20, 15)

# 主游戏循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # 重新开始游戏
            if event.key == pygame.K_r and (game_map.game_state == "GAME_OVER" or game_map.game_state == "VICTORY"):
                game_map = GameMap(20, 15)
            
            # 切换背包/暂停
            if event.key == pygame.K_i:
                if game_map.game_state == "PLAYING":
                    game_map.game_state = "INVENTORY"
                elif game_map.game_state == "INVENTORY":
                    game_map.game_state = "PLAYING"
            
            if event.key == pygame.K_p:
                if game_map.game_state == "PLAYING":
                    game_map.game_state = "PAUSED"
                elif game_map.game_state == "PAUSED":
                    game_map.game_state = "PLAYING"
            
            # 玩家攻击
            if event.key == pygame.K_z and game_map.game_state == "PLAYING":
                if game_map.player.has_sword:
                    # 简单攻击逻辑：检查攻击范围内的敌人
                    attack_range = TILE_SIZE
                    player_rect = pygame.Rect(game_map.player.x, game_map.player.y, 
                                            game_map.player.width, game_map.player.height)
                    
                    # 根据方向调整攻击范围
                    if game_map.player.direction == "up":
                        attack_rect = pygame.Rect(game_map.player.x, game_map.player.y - attack_range,
                                                 game_map.player.width, attack_range)
                    elif game_map.player.direction == "down":
                        attack_rect = pygame.Rect(game_map.player.x, game_map.player.y + game_map.player.height,
                                                 game_map.player.width, attack_range)
                    elif game_map.player.direction == "left":
                        attack_rect = pygame.Rect(game_map.player.x - attack_range, game_map.player.y,
                                                 attack_range, game_map.player.height)
                    else:  # right
                        attack_rect = pygame.Rect(game_map.player.x + game_map.player.width, game_map.player.y,
                                                 attack_range, game_map.player.height)
                    
                    # 检查攻击是否击中敌人
                    for enemy in game_map.enemies[:]:
                        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                        if attack_rect.colliderect(enemy_rect):
                            enemy.take_damage(2)
            
            # 玩家射击
            if event.key == pygame.K_x and game_map.game_state == "PLAYING":
                if game_map.player.has_bow:
                    # 创建弓箭
                    arrow_speed = 10
                    arrow_dx, arrow_dy = 0, 0
                    
                    if game_map.player.direction == "up":
                        arrow_dy = -arrow_speed
                    elif game_map.player.direction == "down":
                        arrow_dy = arrow_speed
                    elif game_map.player.direction == "left":
                        arrow_dx = -arrow_speed
                    elif game_map.player.direction == "right":
                        arrow_dx = arrow_speed
                    
                    game_map.projectiles.append(Projectile(
                        game_map.player.x + game_map.player.width // 2,
                        game_map.player.y + game_map.player.height // 2,
                        arrow_dx, arrow_dy
                    ))
    
    # 获取按键状态（仅在游戏进行时）
    if game_map.game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        
        # 玩家移动
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        
        if dx != 0 or dy != 0:
            game_map.player.move(dx, dy, game_map)
    
    # 更新游戏状态
    game_map.update()
    
    # 绘制
    screen.fill(BLACK)
    game_map.draw(screen)
    
    # 如果游戏暂停，显示暂停画面
    if game_map.game_state == "PAUSED":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        pause_text = font.render("游戏暂停", True, WHITE)
        screen.blit(pause_text, 
                   (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 50))
        
        font_small = pygame.font.Font(None, 36)
        continue_text = font_small.render("按P继续游戏", True, WHITE)
        screen.blit(continue_text, 
                   (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 30))
    
    # 如果打开背包，显示背包画面
    if game_map.game_state == "INVENTORY":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, 200))
        screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)
        
        inventory_text = font_large.render("背包", True, YELLOW)
        screen.blit(inventory_text, 
                   (SCREEN_WIDTH // 2 - inventory_text.get_width() // 2, 50))
        
        # 显示物品
        y_offset = 150
        items = [
            ("剑", game_map.player.has_sword),
            ("弓", game_map.player.has_bow)
        ]
        
        for item_name, has_item in items:
            color = GREEN if has_item else RED
            status = "已获得" if has_item else "未获得"
            item_text = font.render(f"{item_name}: {status}", True, color)
            screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, y_offset))
            y_offset += 50
        
        # 显示钥匙和卢比
        key_text = font.render(f"钥匙: {game_map.player.keys}", True, YELLOW)
        rupee_text = font.render(f"卢比: {game_map.player.rupees}", True, (0, 200, 255))
        
        screen.blit(key_text, (SCREEN_WIDTH // 2 - key_text.get_width() // 2, y_offset + 30))
        screen.blit(rupee_text, (SCREEN_WIDTH // 2 - rupee_text.get_width() // 2, y_offset + 70))
        
        # 提示
        hint_text = font.render("按I关闭背包", True, WHITE)
        screen.blit(hint_text, 
                   (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 
                    SCREEN_HEIGHT - 100))
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

pygame.quit()
sys.exit()