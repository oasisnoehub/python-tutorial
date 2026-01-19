import pygame
import random
import math
import sys
from enum import Enum

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 64
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

# 游戏状态
class GameState(Enum):
    PLAYING = 1
    INVENTORY = 2
    PAUSED = 3
    GAME_OVER = 4
    VICTORY = 5

# 方向枚举
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# 物品类型
class ItemType(Enum):
    SWORD = 1
    BOW = 2
    SHIELD = 3
    KEY = 4
    HEART = 5
    RUPPEE = 6

# 敌人类型
class EnemyType(Enum):
    BOKOBLIN = 1
    KEESE = 2
    OCTOROK = 3

# 地图类
class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.generate_map()
        
    def generate_map(self):
        # 生成随机地图
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # 边缘是墙
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    row.append("#")  # 墙
                else:
                    # 随机生成地形
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
        
        # 添加一些特殊位置
        # 玩家起始位置
        self.tiles[5][5] = "."
        
        # 钥匙位置
        self.tiles[random.randint(2, self.height-3)][random.randint(2, self.width-3)] = "K"
        
        # 门位置
        self.tiles[self.height//2][self.width-2] = "D"
        
        # 宝箱位置
        self.tiles[self.height//2][self.width-3] = "C"
        
        # 多个敌人位置
        for _ in range(10):
            x = random.randint(2, self.width-3)
            y = random.randint(2, self.height-3)
            if self.tiles[y][x] == ".":
                self.tiles[y][x] = "E"
    
    def draw(self, screen, camera_x, camera_y):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * TILE_SIZE - camera_x,
                    y * TILE_SIZE - camera_y,
                    TILE_SIZE, TILE_SIZE
                )
                
                tile = self.tiles[y][x]
                color = GREEN  # 草地
                
                if tile == "#":  # 墙
                    color = BROWN
                    pygame.draw.rect(screen, color, rect)
                    # 添加纹理
                    pygame.draw.rect(screen, (BROWN[0]-20, BROWN[1]-20, BROWN[2]-20), 
                                    (rect.x+5, rect.y+5, TILE_SIZE-10, TILE_SIZE-10))
                elif tile == "T":  # 树
                    color = (0, 100, 0)
                    pygame.draw.rect(screen, color, rect)
                    # 树冠
                    pygame.draw.circle(screen, (0, 150, 0), 
                                      (rect.x + TILE_SIZE//2, rect.y + TILE_SIZE//3), 
                                      TILE_SIZE//2)
                elif tile == "W":  # 水
                    color = BLUE
                    pygame.draw.rect(screen, color, rect)
                    # 水波纹
                    for i in range(3):
                        pygame.draw.circle(screen, LIGHT_BLUE, 
                                          (rect.x + 15 + i*15, rect.y + 15 + (i%2)*10), 
                                          5)
                elif tile == "R":  # 岩石
                    color = GRAY
                    pygame.draw.rect(screen, color, rect)
                    # 岩石纹理
                    for i in range(5):
                        pygame.draw.circle(screen, (GRAY[0]-20, GRAY[1]-20, GRAY[2]-20), 
                                          (rect.x + 10 + i*10, rect.y + 10 + (i%3)*15), 
                                          5)
                elif tile == "K":  # 钥匙
                    pygame.draw.rect(screen, GREEN, rect)
                    # 绘制钥匙
                    key_rect = pygame.Rect(rect.x + 20, rect.y + 20, 24, 8)
                    pygame.draw.rect(screen, YELLOW, key_rect)
                    pygame.draw.circle(screen, YELLOW, (rect.x + 32, rect.y + 34), 10)
                elif tile == "D":  # 门
                    color = (100, 50, 0)
                    pygame.draw.rect(screen, color, rect)
                    # 门把手
                    pygame.draw.circle(screen, YELLOW, 
                                      (rect.x + TILE_SIZE//2, rect.y + TILE_SIZE//2), 
                                      5)
                elif tile == "C":  # 宝箱
                    color = (150, 75, 0)
                    pygame.draw.rect(screen, color, rect)
                    # 宝箱盖子
                    pygame.draw.rect(screen, (180, 90, 0), 
                                    (rect.x, rect.y, TILE_SIZE, TILE_SIZE//3))
                elif tile == "E":  # 敌人位置
                    pygame.draw.rect(screen, GREEN, rect)
                else:  # 草地
                    pygame.draw.rect(screen, color, rect)
                    # 草地纹理
                    for i in range(4):
                        pygame.draw.line(screen, (0, 200, 0), 
                                        (rect.x + i*16, rect.y), 
                                        (rect.x + i*16, rect.y + TILE_SIZE), 
                                        1)

# 玩家类
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        self.speed = 5
        self.direction = Direction.DOWN
        self.health = 12
        self.max_health = 12
        self.has_sword = False
        self.has_bow = False
        self.has_shield = False
        self.keys = 0
        self.rupees = 0
        self.attack_cooldown = 0
        self.invincibility_frames = 0
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 更新方向
        if dx > 0:
            self.direction = Direction.RIGHT
        elif dx < 0:
            self.direction = Direction.LEFT
        elif dy > 0:
            self.direction = Direction.DOWN
        elif dy < 0:
            self.direction = Direction.UP
        
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
                    if tile in ["#", "T", "R", "W"]:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if player_rect.colliderect(tile_rect):
                            return
        
        # 可以移动
        self.x = new_x
        self.y = new_y
    
    def attack(self, enemies, projectiles):
        if self.attack_cooldown > 0 or not self.has_sword:
            return
            
        self.attack_cooldown = 15
        
        # 根据方向创建攻击区域
        attack_rect = None
        if self.direction == Direction.UP:
            attack_rect = pygame.Rect(self.x, self.y - TILE_SIZE, self.width, TILE_SIZE)
        elif self.direction == Direction.DOWN:
            attack_rect = pygame.Rect(self.x, self.y + self.height, self.width, TILE_SIZE)
        elif self.direction == Direction.LEFT:
            attack_rect = pygame.Rect(self.x - TILE_SIZE, self.y, TILE_SIZE, self.height)
        elif self.direction == Direction.RIGHT:
            attack_rect = pygame.Rect(self.x + self.width, self.y, TILE_SIZE, self.height)
        
        # 检查攻击是否击中敌人
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if attack_rect.colliderect(enemy_rect):
                enemy.take_damage(2)
    
    def shoot(self, projectiles):
        if not self.has_bow:
            return
            
        # 创建弓箭
        arrow_speed = 10
        arrow_dx, arrow_dy = 0, 0
        
        if self.direction == Direction.UP:
            arrow_dy = -arrow_speed
        elif self.direction == Direction.DOWN:
            arrow_dy = arrow_speed
        elif self.direction == Direction.LEFT:
            arrow_dx = -arrow_speed
        elif self.direction == Direction.RIGHT:
            arrow_dx = arrow_speed
        
        projectiles.append(Projectile(
            self.x + self.width // 2,
            self.y + self.height // 2,
            arrow_dx, arrow_dy
        ))
    
    def take_damage(self, amount):
        if self.invincibility_frames > 0:
            return
            
        self.health -= amount
        self.invincibility_frames = 30
        
        if self.health <= 0:
            self.health = 0
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1
    
    def draw(self, screen, camera_x, camera_y):
        # 绘制玩家
        player_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        
        # 根据方向改变玩家颜色
        color = GREEN
        if self.direction == Direction.UP:
            color = (0, 200, 0)
        elif self.direction == Direction.DOWN:
            color = (0, 180, 0)
        elif self.direction == Direction.LEFT:
            color = (0, 160, 0)
        elif self.direction == Direction.RIGHT:
            color = (0, 140, 0)
        
        # 受伤时闪烁
        if self.invincibility_frames > 0 and self.invincibility_frames % 6 < 3:
            color = RED
        
        pygame.draw.rect(screen, color, player_rect)
        
        # 绘制玩家眼睛（根据方向）
        eye_offset = 5
        eye_x, eye_y = 0, 0
        
        if self.direction == Direction.UP:
            eye_x = player_rect.x + player_rect.width // 2
            eye_y = player_rect.y + 10
        elif self.direction == Direction.DOWN:
            eye_x = player_rect.x + player_rect.width // 2
            eye_y = player_rect.y + player_rect.height - 10
        elif self.direction == Direction.LEFT:
            eye_x = player_rect.x + 10
            eye_y = player_rect.y + player_rect.height // 2
        elif self.direction == Direction.RIGHT:
            eye_x = player_rect.x + player_rect.width - 10
            eye_y = player_rect.y + player_rect.height // 2
        
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 2)
        
        # 如果有剑，绘制剑
        if self.has_sword and self.attack_cooldown > 0:
            sword_rect = None
            sword_color = (200, 200, 200)
            
            if self.direction == Direction.UP:
                sword_rect = pygame.Rect(
                    player_rect.x + player_rect.width // 2 - 3,
                    player_rect.y - 30,
                    6, 30
                )
            elif self.direction == Direction.DOWN:
                sword_rect = pygame.Rect(
                    player_rect.x + player_rect.width // 2 - 3,
                    player_rect.y + player_rect.height,
                    6, 30
                )
            elif self.direction == Direction.LEFT:
                sword_rect = pygame.Rect(
                    player_rect.x - 30,
                    player_rect.y + player_rect.height // 2 - 3,
                    30, 6
                )
            elif self.direction == Direction.RIGHT:
                sword_rect = pygame.Rect(
                    player_rect.x + player_rect.width,
                    player_rect.y + player_rect.height // 2 - 3,
                    30, 6
                )
            
            if sword_rect:
                pygame.draw.rect(screen, sword_color, sword_rect)
                pygame.draw.rect(screen, (150, 150, 150), 
                                (sword_rect.x + 1, sword_rect.y + 1, 
                                 sword_rect.width - 2, sword_rect.height - 2))

# 敌人类
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        
        if enemy_type == EnemyType.BOKOBLIN:
            self.color = RED
            self.health = 4
            self.speed = 2
        elif enemy_type == EnemyType.KEESE:
            self.color = PURPLE
            self.health = 2
            self.speed = 3
        elif enemy_type == EnemyType.OCTOROK:
            self.color = BROWN
            self.health = 3
            self.speed = 1
        
        self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        self.move_timer = random.randint(30, 90)
        self.attack_cooldown = 0
        
    def update(self, player, game_map):
        # 移动计时器
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
            self.move_timer = random.randint(30, 90)
        
        # 移动
        dx, dy = 0, 0
        if self.direction == Direction.UP:
            dy = -1
        elif self.direction == Direction.DOWN:
            dy = 1
        elif self.direction == Direction.LEFT:
            dx = -1
        elif self.direction == Direction.RIGHT:
            dx = 1
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 检查碰撞
        enemy_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # 地图边界
        if (new_x < 0 or new_x > game_map.width * TILE_SIZE - self.width or
            new_y < 0 or new_y > game_map.height * TILE_SIZE - self.height):
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
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
                    if tile in ["#", "T", "R", "W"]:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if enemy_rect.colliderect(tile_rect):
                            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
                            self.move_timer = random.randint(30, 90)
                            return
        
        # 可以移动
        self.x = new_x
        self.y = new_y
        
        # 攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 检查是否攻击玩家
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if enemy_rect.colliderect(player_rect) and self.attack_cooldown == 0:
            player.take_damage(1)
            self.attack_cooldown = 60
    
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
        
        # 绘制生命条
        if self.health < 4:
            health_width = enemy_rect.width * self.health / 4
            health_rect = pygame.Rect(
                enemy_rect.x,
                enemy_rect.y - 10,
                health_width,
                5
            )
            pygame.draw.rect(screen, RED, health_rect)
            pygame.draw.rect(screen, BLACK, health_rect, 1)

# 物品类
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
        
        if self.type == ItemType.SWORD:
            pygame.draw.rect(screen, (200, 200, 200), item_rect)
            # 剑柄
            pygame.draw.rect(screen, BROWN, 
                            (item_rect.x + item_rect.width // 2 - 5, 
                             item_rect.y + 5, 
                             10, item_rect.height - 10))
        elif self.type == ItemType.BOW:
            pygame.draw.ellipse(screen, (150, 100, 50), item_rect)
        elif self.type == ItemType.SHIELD:
            pygame.draw.rect(screen, BLUE, item_rect)
            pygame.draw.circle(screen, YELLOW, 
                              (item_rect.x + item_rect.width // 2, 
                               item_rect.y + item_rect.height // 2), 
                              10)
        elif self.type == ItemType.KEY:
            pygame.draw.rect(screen, YELLOW, item_rect)
            # 钥匙齿
            pygame.draw.rect(screen, YELLOW, 
                            (item_rect.x + item_rect.width // 2 - 10, 
                             item_rect.y + item_rect.height // 2 - 3, 
                             20, 6))
        elif self.type == ItemType.HEART:
            # 绘制心形
            pygame.draw.polygon(screen, RED, [
                (item_rect.x + item_rect.width // 2, item_rect.y + 5),
                (item_rect.x + 5, item_rect.y + item_rect.height // 2),
                (item_rect.x + item_rect.width // 2, item_rect.y + item_rect.height - 5),
                (item_rect.x + item_rect.width - 5, item_rect.y + item_rect.height // 2)
            ])
        elif self.type == ItemType.RUPPEE:
            pygame.draw.polygon(screen, (0, 200, 255), [
                (item_rect.x + item_rect.width // 2, item_rect.y),
                (item_rect.x + item_rect.width - 5, item_rect.y + item_rect.height // 3),
                (item_rect.x + item_rect.width - 5, item_rect.y + 2 * item_rect.height // 3),
                (item_rect.x + item_rect.width // 2, item_rect.y + item_rect.height),
                (item_rect.x + 5, item_rect.y + 2 * item_rect.height // 3),
                (item_rect.x + 5, item_rect.y + item_rect.height // 3)
            ])

# 弹射物类
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
        
    def is_out_of_bounds(self, game_map):
        return (self.x < 0 or self.x > game_map.width * TILE_SIZE or
                self.y < 0 or self.y > game_map.height * TILE_SIZE)
    
    def draw(self, screen, camera_x, camera_y):
        proj_rect = pygame.Rect(
            self.x - camera_x,
            self.y - camera_y,
            self.width, self.height
        )
        pygame.draw.rect(screen, YELLOW, proj_rect)

# 游戏类
class Game:
    def __init__(self):
        self.state = GameState.PLAYING
        self.map = GameMap(20, 15)
        self.player = Player(5 * TILE_SIZE + TILE_SIZE // 4, 5 * TILE_SIZE + TILE_SIZE // 4)
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.camera_x = 0
        self.camera_y = 0
        self.message = ""
        self.message_timer = 0
        self.generate_enemies()
        self.generate_items()
        
    def generate_enemies(self):
        # 从地图中生成敌人
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.tiles[y][x] == "E":
                    enemy_type = random.choice(list(EnemyType))
                    self.enemies.append(Enemy(
                        x * TILE_SIZE + TILE_SIZE // 4,
                        y * TILE_SIZE + TILE_SIZE // 4,
                        enemy_type
                    ))
    
    def generate_items(self):
        # 在地图上放置一些物品
        # 剑
        self.items.append(Item(
            3 * TILE_SIZE + TILE_SIZE // 4,
            7 * TILE_SIZE + TILE_SIZE // 4,
            ItemType.SWORD
        ))
        
        # 弓
        self.items.append(Item(
            15 * TILE_SIZE + TILE_SIZE // 4,
            3 * TILE_SIZE + TILE_SIZE // 4,
            ItemType.BOW
        ))
        
        # 盾牌
        self.items.append(Item(
            8 * TILE_SIZE + TILE_SIZE // 4,
            12 * TILE_SIZE + TILE_SIZE // 4,
            ItemType.SHIELD
        ))
        
        # 一些心
        for _ in range(3):
            x = random.randint(2, self.map.width-3)
            y = random.randint(2, self.map.height-3)
            if self.map.tiles[y][x] == ".":
                self.items.append(Item(
                    x * TILE_SIZE + TILE_SIZE // 4,
                    y * TILE_SIZE + TILE_SIZE // 4,
                    ItemType.HEART
                ))
        
        # 一些卢比
        for _ in range(5):
            x = random.randint(2, self.map.width-3)
            y = random.randint(2, self.map.height-3)
            if self.map.tiles[y][x] == ".":
                self.items.append(Item(
                    x * TILE_SIZE + TILE_SIZE // 4,
                    y * TILE_SIZE + TILE_SIZE // 4,
                    ItemType.RUPPEE
                ))
    
    def update_camera(self):
        # 将相机中心对准玩家
        self.camera_x = self.player.x - SCREEN_WIDTH // 2 + self.player.width // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2 + self.player.height // 2
        
        # 限制相机范围
        self.camera_x = max(0, min(self.camera_x, self.map.width * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map.height * TILE_SIZE - SCREEN_HEIGHT))
    
    def check_collisions(self):
        # 检查玩家与物品的碰撞
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        
        for item in self.items[:]:
            item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
            if player_rect.colliderect(item_rect):
                if item.type == ItemType.SWORD:
                    self.player.has_sword = True
                    self.show_message("你获得了剑！按Z攻击")
                elif item.type == ItemType.BOW:
                    self.player.has_bow = True
                    self.show_message("你获得了弓！按X射击")
                elif item.type == ItemType.SHIELD:
                    self.player.has_shield = True
                    self.show_message("你获得了盾牌！")
                elif item.type == ItemType.KEY:
                    self.player.keys += 1
                    self.show_message(f"你获得了钥匙！现在有 {self.player.keys} 把钥匙")
                elif item.type == ItemType.HEART:
                    self.player.health = min(self.player.max_health, self.player.health + 4)
                    self.show_message("生命值恢复！")
                elif item.type == ItemType.RUPPEE:
                    self.player.rupees += 5
                    self.show_message(f"+5 卢比！总计: {self.player.rupees}")
                
                self.items.remove(item)
        
        # 检查玩家与门的碰撞
        door_x, door_y = 0, 0
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.tiles[y][x] == "D":
                    door_x, door_y = x, y
                    break
        
        door_rect = pygame.Rect(door_x * TILE_SIZE, door_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if player_rect.colliderect(door_rect):
            if self.player.keys > 0:
                self.player.keys -= 1
                self.map.tiles[door_y][door_x] = "."
                self.show_message("门打开了！")
            else:
                self.show_message("门锁着！需要钥匙")
        
        # 检查玩家与宝箱的碰撞
        chest_x, chest_y = 0, 0
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.tiles[y][x] == "C":
                    chest_x, chest_y = x, y
                    break
        
        chest_rect = pygame.Rect(chest_x * TILE_SIZE, chest_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if player_rect.colliderect(chest_rect):
            self.state = GameState.VICTORY
            self.show_message("你找到了宝藏！游戏胜利！")
        
        # 检查弹射物与敌人的碰撞
        for projectile in self.projectiles[:]:
            proj_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
            
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if proj_rect.colliderect(enemy_rect):
                    enemy.take_damage(1)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
        
        # 检查弹射物边界
        for projectile in self.projectiles[:]:
            if projectile.is_out_of_bounds(self.map):
                self.projectiles.remove(projectile)
    
    def show_message(self, text):
        self.message = text
        self.message_timer = 120  # 2秒（60帧/秒）
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        # 更新玩家
        self.player.update()
        
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.map)
            if enemy.is_dead():
                self.enemies.remove(enemy)
                # 敌人有几率掉落物品
                if random.random() < 0.3:
                    item_type = random.choice([ItemType.HEART, ItemType.RUPPEE])
                    self.items.append(Item(enemy.x, enemy.y, item_type))
        
        # 更新弹射物
        for projectile in self.projectiles:
            projectile.update()
        
        # 检查碰撞
        self.check_collisions()
        
        # 更新相机
        self.update_camera()
        
        # 更新消息计时器
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""
        
        # 检查游戏结束
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
    
    def draw(self, screen):
        # 绘制地图
        self.map.draw(screen, self.camera_x, self.camera_y)
        
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
            font = pygame.font.SysFont(None, 36)
            text = font.render(self.message, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            
            # 半透明背景
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
                                 text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect, border_radius=5)
            pygame.draw.rect(screen, WHITE, bg_rect, 2, border_radius=5)
            
            screen.blit(text, text_rect)
        
        # 绘制游戏状态
        if self.state == GameState.GAME_OVER:
            self.draw_game_over(screen)
        elif self.state == GameState.VICTORY:
            self.draw_victory(screen)
    
    def draw_ui(self, screen):
        # 绘制生命值
        heart_size = 30
        for i in range(self.player.max_health // 4):
            x = 20 + i * (heart_size + 5)
            y = 20
            
            # 空的心
            pygame.draw.polygon(screen, (100, 0, 0), [
                (x + heart_size // 2, y + 5),
                (x + 5, y + heart_size // 2),
                (x + heart_size // 2, y + heart_size - 5),
                (x + heart_size - 5, y + heart_size // 2)
            ])
            
            # 填充的心（根据当前生命值）
            if self.player.health >= (i + 1) * 4:
                fill_color = RED
            elif self.player.health > i * 4:
                # 部分填充
                fill_amount = self.player.health - i * 4
                fill_color = RED
                # 这里简化处理，实际应该绘制部分心形
            else:
                fill_color = None
            
            if fill_color:
                pygame.draw.polygon(screen, fill_color, [
                    (x + heart_size // 2, y + 5),
                    (x + 5, y + heart_size // 2),
                    (x + heart_size // 2, y + heart_size - 5),
                    (x + heart_size - 5, y + heart_size // 2)
                ])
        
        # 绘制钥匙数量
        font = pygame.font.SysFont(None, 36)
        key_text = font.render(f"钥匙: {self.player.keys}", True, YELLOW)
        screen.blit(key_text, (SCREEN_WIDTH - 150, 20))
        
        # 绘制卢比数量
        rupee_text = font.render(f"卢比: {self.player.rupees}", True, (0, 200, 255))
        screen.blit(rupee_text, (SCREEN_WIDTH - 150, 60))
        
        # 绘制物品栏
        items_y = SCREEN_HEIGHT - 60
        item_spacing = 70
        
        # 剑
        sword_rect = pygame.Rect(20, items_y, 50, 50)
        pygame.draw.rect(screen, (100, 100, 100), sword_rect, border_radius=5)
        if self.player.has_sword:
            pygame.draw.rect(screen, (200, 200, 200), 
                            (sword_rect.x + 15, sword_rect.y + 10, 20, 30))
            pygame.draw.rect(screen, BROWN, 
                            (sword_rect.x + 22, sword_rect.y + 15, 6, 20))
        sword_text = font.render("Z", True, WHITE)
        screen.blit(sword_text, (sword_rect.x + 20, sword_rect.y + 55))
        
        # 弓
        bow_rect = pygame.Rect(20 + item_spacing, items_y, 50, 50)
        pygame.draw.rect(screen, (100, 100, 100), bow_rect, border_radius=5)
        if self.player.has_bow:
            pygame.draw.ellipse(screen, (150, 100, 50), 
                               (bow_rect.x + 10, bow_rect.y + 15, 30, 20))
        bow_text = font.render("X", True, WHITE)
        screen.blit(bow_text, (bow_rect.x + 20, bow_rect.y + 55))
        
        # 盾牌
        shield_rect = pygame.Rect(20 + 2 * item_spacing, items_y, 50, 50)
        pygame.draw.rect(screen, (100, 100, 100), shield_rect, border_radius=5)
        if self.player.has_shield:
            pygame.draw.rect(screen, BLUE, 
                            (shield_rect.x + 10, shield_rect.y + 10, 30, 30))
            pygame.draw.circle(screen, YELLOW, 
                              (shield_rect.x + 25, shield_rect.y + 25), 10)
        shield_text = font.render("S", True, WHITE)
        screen.blit(shield_text, (shield_rect.x + 20, shield_rect.y + 55))
        
        # 控制说明
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
    
    def draw_game_over(self, screen):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # 游戏结束文本
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
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
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
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

# 主游戏循环
def main():
    game = Game()
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
                if event.key == pygame.K_r and (game.state == GameState.GAME_OVER or game.state == GameState.VICTORY):
                    game = Game()
                
                # 切换背包/暂停
                if event.key == pygame.K_i:
                    if game.state == GameState.PLAYING:
                        game.state = GameState.INVENTORY
                    elif game.state == GameState.INVENTORY:
                        game.state = GameState.PLAYING
                
                if event.key == pygame.K_p:
                    if game.state == GameState.PLAYING:
                        game.state = GameState.PAUSED
                    elif game.state == GameState.PAUSED:
                        game.state = GameState.PLAYING
        
        # 获取按键状态（仅在游戏进行时）
        if game.state == GameState.PLAYING:
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
            
            game.player.move(dx, dy, game.map)
            
            # 玩家攻击
            if keys[pygame.K_z]:
                game.player.attack(game.enemies, game.projectiles)
            
            # 玩家射击
            if keys[pygame.K_x]:
                game.player.shoot(game.projectiles)
        
        # 更新游戏状态
        game.update()
        
        # 绘制
        screen.fill(BLACK)
        game.draw(screen)
        
        # 如果游戏暂停，显示暂停画面
        if game.state == GameState.PAUSED:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            font = pygame.font.SysFont(None, 72)
            pause_text = font.render("游戏暂停", True, WHITE)
            screen.blit(pause_text, 
                       (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - 50))
            
            font_small = pygame.font.SysFont(None, 36)
            continue_text = font_small.render("按P继续游戏", True, WHITE)
            screen.blit(continue_text, 
                       (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 + 30))
        
        # 如果打开背包，显示背包画面
        if game.state == GameState.INVENTORY:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 50, 200))
            screen.blit(overlay, (0, 0))
            
            font_large = pygame.font.SysFont(None, 72)
            font = pygame.font.SysFont(None, 36)
            
            inventory_text = font_large.render("背包", True, YELLOW)
            screen.blit(inventory_text, 
                       (SCREEN_WIDTH // 2 - inventory_text.get_width() // 2, 50))
            
            # 显示物品
            y_offset = 150
            items = [
                ("剑", game.player.has_sword),
                ("弓", game.player.has_bow),
                ("盾牌", game.player.has_shield)
            ]
            
            for item_name, has_item in items:
                color = GREEN if has_item else RED
                status = "已获得" if has_item else "未获得"
                item_text = font.render(f"{item_name}: {status}", True, color)
                screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, y_offset))
                y_offset += 50
            
            # 显示钥匙和卢比
            key_text = font.render(f"钥匙: {game.player.keys}", True, YELLOW)
            rupee_text = font.render(f"卢比: {game.player.rupees}", True, (0, 200, 255))
            
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

if __name__ == "__main__":
    main()