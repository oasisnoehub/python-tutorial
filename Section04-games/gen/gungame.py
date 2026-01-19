import pygame
import random
import math
import sys

# 初始化Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频

# 游戏常量
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 70, 230)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
LIGHT_BLUE = (100, 200, 255)
DARK_RED = (139, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("双人射击大战 - 枪械动画版")
clock = pygame.time.Clock()

# 加载字体
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

# 玩家类
class Player:
    def __init__(self, x, y, color, controls, player_num):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.controls = controls  # 控制键字典
        self.player_num = player_num
        self.angle = 0  # 枪口角度
        self.gun_length = 50  # 枪管长度
        self.gun_width = 12  # 枪管宽度
        self.recoil = 0  # 后坐力效果
        self.recoil_speed = 0.8  # 后坐力恢复速度
        self.shoot_cooldown = 0  # 射击冷却
        self.score = 0
        self.ammo = 30  # 弹药量
        self.max_ammo = 30
        self.reload_time = 0  # 装弹时间
        self.is_reloading = False
        self.kill_count = 0
        
        # 枪械类型
        self.gun_type = "rifle"  # rifle, shotgun, pistol
        self.gun_color = (150, 150, 150)  # 枪械颜色
        
        # 玩家图像组件
        self.body_color = color
        self.head_color = (color[0]*0.8, color[1]*0.8, color[2]*0.8)
        
    def move(self, keys, obstacles):
        dx, dy = 0, 0
        
        # 玩家1控制（WASD）
        if self.player_num == 1:
            if keys[self.controls["up"]]:
                print("W键被按下了！")
                dy -= 1
            if keys[self.controls["down"]]:
                print("S键被按下了！")
                dy += 1
            if keys[self.controls["left"]]:
                print("A键被按下了！")
                dx -= 1
            if keys[self.controls["right"]]:
                print("D键被按下了！")
                dx += 1
        # 玩家2控制（方向键）
        else:
            if keys[self.controls["up"]]:
                dy -= 1
            if keys[self.controls["down"]]:
                dy += 1
            if keys[self.controls["left"]]:
                dx -= 1
            if keys[self.controls["right"]]:
                dx += 1
        
        # 标准化对角线移动速度
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/√2
            dy *= 0.7071
        
        # 计算新位置
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 边界检查
        new_x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, new_x))
        new_y = max(self.height//2, min(SCREEN_HEIGHT - self.height//2, new_y))
        
        # 障碍物碰撞检测
        player_rect = pygame.Rect(new_x - self.width//2, new_y - self.height//2, self.width, self.height)
        can_move = True
        
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                can_move = False
                break
        
        if can_move:
            self.x = new_x
            self.y = new_y
    
    def aim(self, mouse_pos=None, other_player=None):
        if mouse_pos and self.player_num == 1:
            # 玩家1使用鼠标瞄准
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            self.angle = math.atan2(dy, dx)
        elif other_player and self.player_num == 2:
            # 玩家2自动瞄准玩家1
            dx = other_player.x - self.x
            dy = other_player.y - self.y
            self.angle = math.atan2(dy, dx)
        else:
            # 默认瞄准右边
            self.angle = 0
    
    def shoot(self, bullets, sound_on=True):
        if self.shoot_cooldown > 0 or self.ammo <= 0 or self.is_reloading:
            return False
        
        # 根据枪械类型创建子弹
        if self.gun_type == "rifle":
            # 步枪：单发高速子弹
            bullet_speed = 15
            bullet_size = 8
            bullet_color = YELLOW
            bullet_damage = 20
            self.recoil = 10
            self.shoot_cooldown = 10  # 射击冷却
            self.ammo -= 1
            
            # 创建子弹
            bullets.append(Bullet(
                self.x + math.cos(self.angle) * (self.gun_length + 20),
                self.y + math.sin(self.angle) * (self.gun_length + 20),
                self.angle,
                bullet_speed,
                bullet_size,
                bullet_color,
                bullet_damage,
                self.player_num
            ))
            
        elif self.gun_type == "shotgun":
            # 散弹枪：多发扩散子弹
            bullet_speed = 12
            bullet_size = 6
            bullet_color = ORANGE
            bullet_damage = 15
            self.recoil = 15
            self.shoot_cooldown = 30  # 较长冷却
            self.ammo -= 1
            
            # 创建5发散弹
            for i in range(-2, 3):
                spread_angle = self.angle + i * 0.15  # 扩散角度
                bullets.append(Bullet(
                    self.x + math.cos(self.angle) * (self.gun_length + 20),
                    self.y + math.sin(self.angle) * (self.gun_length + 20),
                    spread_angle,
                    bullet_speed,
                    bullet_size,
                    bullet_color,
                    bullet_damage,
                    self.player_num
                ))
                
        elif self.gun_type == "pistol":
            # 手枪：单发中等速度子弹
            bullet_speed = 12
            bullet_size = 7
            bullet_color = LIGHT_BLUE
            bullet_damage = 25
            self.recoil = 8
            self.shoot_cooldown = 20  # 中等冷却
            self.ammo -= 1
            
            bullets.append(Bullet(
                self.x + math.cos(self.angle) * (self.gun_length + 20),
                self.y + math.sin(self.angle) * (self.gun_length + 20),
                self.angle,
                bullet_speed,
                bullet_size,
                bullet_color,
                bullet_damage,
                self.player_num
            ))
        
        # 射击音效
        if sound_on:
            pygame.mixer.Sound.play(shoot_sound)
        
        return True
    
    def reload(self):
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_time = 90  # 1.5秒装弹时间
            pygame.mixer.Sound.play(reload_sound)
    
    def update(self):
        # 更新后坐力
        if self.recoil > 0:
            self.recoil -= self.recoil_speed
            if self.recoil < 0:
                self.recoil = 0
        
        # 更新射击冷却
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # 更新装弹
        if self.is_reloading:
            self.reload_time -= 1
            if self.reload_time <= 0:
                self.ammo = self.max_ammo
                self.is_reloading = False
    
    def draw(self, screen):
        # 绘制玩家身体（椭圆）
        body_rect = pygame.Rect(
            self.x - self.width//2,
            self.y - self.height//3,
            self.width,
            self.height * 2//3
        )
        pygame.draw.ellipse(screen, self.body_color, body_rect)
        
        # 绘制玩家头部（圆形）
        head_radius = self.width // 2
        pygame.draw.circle(screen, self.head_color, (int(self.x), int(self.y - self.height//3)), head_radius)
        
        # 计算枪械位置（考虑后坐力）
        gun_recoil_offset = self.recoil
        gun_end_x = self.x + math.cos(self.angle) * (self.gun_length - gun_recoil_offset)
        gun_end_y = self.y + math.sin(self.angle) * (self.gun_length - gun_recoil_offset)
        gun_start_x = self.x + math.cos(self.angle + math.pi) * 10  # 枪托位置
        gun_start_y = self.y + math.sin(self.angle + math.pi) * 10
        
        # 绘制枪管
        pygame.draw.line(screen, self.gun_color, 
                        (gun_start_x, gun_start_y), 
                        (gun_end_x, gun_end_y), 
                        self.gun_width)
        
        # 绘制枪身
        gun_body_width = self.gun_width + 4
        gun_body_length = self.gun_length * 0.6
        gun_body_end_x = self.x + math.cos(self.angle) * gun_body_length
        gun_body_end_y = self.y + math.sin(self.angle) * gun_body_length
        
        pygame.draw.line(screen, (100, 100, 100), 
                        (gun_start_x, gun_start_y), 
                        (gun_body_end_x, gun_body_end_y), 
                        gun_body_width)
        
        # 绘制枪口闪光（射击时）
        if self.recoil > 5:
            flash_size = int(self.recoil * 2)
            for i in range(3):
                flash_x = gun_end_x + math.cos(self.angle) * (i * 5)
                flash_y = gun_end_y + math.sin(self.angle) * (i * 5)
                pygame.draw.circle(screen, YELLOW, (int(flash_x), int(flash_y)), flash_size - i*2)
        
        # 绘制玩家编号
        player_text = font_small.render(f"P{self.player_num}", True, WHITE)
        screen.blit(player_text, (self.x - player_text.get_width()//2, self.y - self.height//2 - 20))
        
        # 绘制装弹动画
        if self.is_reloading:
            reload_progress = 1 - (self.reload_time / 90)
            reload_width = 60
            reload_height = 8
            reload_x = self.x - reload_width//2
            reload_y = self.y + self.height//2 + 10
            
            # 装弹进度条背景
            pygame.draw.rect(screen, GRAY, (reload_x, reload_y, reload_width, reload_height))
            # 装弹进度条
            pygame.draw.rect(screen, YELLOW, (reload_x, reload_y, int(reload_width * reload_progress), reload_height))
            
            reload_text = font_small.render("装弹中...", True, YELLOW)
            screen.blit(reload_text, (self.x - reload_text.get_width()//2, reload_y + 15))

# 子弹类
class Bullet:
    def __init__(self, x, y, angle, speed, size, color, damage, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.size = size
        self.color = color
        self.damage = damage
        self.owner = owner  # 子弹属于哪个玩家
        self.trail = []  # 弹道轨迹
        self.trail_length = 8  # 轨迹长度
        self.active = True
        
        # 弹头特效
        self.tip_color = WHITE
        self.glow_size = size + 3
        
    def update(self, obstacles):
        if not self.active:
            return False
        
        # 保存轨迹点
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        # 移动子弹
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # 检查边界
        if (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
            self.y < -50 or self.y > SCREEN_HEIGHT + 50):
            self.active = False
            return False
        
        # 检查障碍物碰撞
        bullet_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        for obstacle in obstacles:
            if bullet_rect.colliderect(obstacle.rect):
                # 击中障碍物，创建击中效果
                obstacle.create_hit_effect(self.x, self.y, self.angle)
                self.active = False
                return False
        
        return True
    
    def draw(self, screen):
        if not self.active:
            return
        
        # 绘制弹道轨迹
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            radius = int(self.size * (i / len(self.trail)))
            if radius > 0:
                # 创建半透明表面绘制轨迹
                trail_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                trail_color = (*self.color[:3], alpha//2)
                pygame.draw.circle(trail_surface, trail_color, (radius, radius), radius)
                screen.blit(trail_surface, (trail_x - radius, trail_y - radius))
        
        # 绘制子弹发光效果
        glow_surface = pygame.Surface((self.glow_size*2, self.glow_size*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color[:3], 100), (self.glow_size, self.glow_size), self.glow_size)
        screen.blit(glow_surface, (self.x - self.glow_size, self.y - self.glow_size))
        
        # 绘制子弹主体
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # 绘制弹头
        tip_x = self.x + math.cos(self.angle) * self.size
        tip_y = self.y + math.sin(self.angle) * self.size
        pygame.draw.circle(screen, self.tip_color, (int(tip_x), int(tip_y)), self.size//2)

# 障碍物类
class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.hit_effects = []  # 击中效果
        
    def create_hit_effect(self, x, y, angle):
        # 创建击中墙壁的效果
        self.hit_effects.append({
            'x': x,
            'y': y,
            'angle': angle,
            'life': 15  # 效果持续时间
        })
    
    def update(self):
        # 更新击中效果
        for effect in self.hit_effects[:]:
            effect['life'] -= 1
            if effect['life'] <= 0:
                self.hit_effects.remove(effect)
    
    def draw(self, screen):
        # 绘制障碍物
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, 3)  # 边框
        
        # 绘制纹理
        for i in range(0, self.width, 15):
            for j in range(0, self.height, 15):
                pygame.draw.rect(screen, (90, 90, 90), 
                                (self.x + i, self.y + j, 8, 8))
        
        # 绘制击中效果
        for effect in self.hit_effects:
            life = effect['life']
            size = life
            alpha = min(255, life * 20)
            
            # 火花效果
            for i in range(5):
                spark_angle = effect['angle'] + math.pi + random.uniform(-0.5, 0.5)
                spark_length = random.randint(5, 15)
                spark_x = effect['x'] + math.cos(spark_angle) * spark_length * (1 - life/15)
                spark_y = effect['y'] + math.sin(spark_angle) * spark_length * (1 - life/15)
                
                spark_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                spark_color = (255, random.randint(150, 255), 50, alpha)
                pygame.draw.circle(spark_surface, spark_color, (size, size), size//2)
                screen.blit(spark_surface, (spark_x - size, spark_y - size))

# 血包类
class HealthPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.active = True
        self.pulse = 0
        self.pulse_speed = 0.1
        
    def update(self):
        self.pulse += self.pulse_speed
        if self.pulse > math.pi * 2:
            self.pulse -= math.pi * 2
    
    def draw(self, screen):
        if not self.active:
            return
            
        pulse_size = int(math.sin(self.pulse) * 3)
        current_radius = self.radius + pulse_size
        
        # 绘制血包发光效果
        glow_surface = pygame.Surface((current_radius*2, current_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 50, 50, 100), 
                          (current_radius, current_radius), current_radius)
        screen.blit(glow_surface, (self.x - current_radius, self.y - current_radius))
        
        # 绘制血包主体
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        
        # 绘制十字标志
        cross_width = self.radius
        pygame.draw.rect(screen, WHITE, 
                        (self.x - cross_width//2, self.y - 3, cross_width, 6))
        pygame.draw.rect(screen, WHITE, 
                        (self.x - 3, self.y - cross_width//2, 6, cross_width))

# 弹药箱类
class AmmoBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        self.active = True
        self.float_offset = 0
        self.float_speed = 0.05
        
    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * 3
    
    def draw(self, screen):
        if not self.active:
            return
            
        draw_y = self.y + self.float_offset
        
        # 绘制弹药箱
        box_rect = pygame.Rect(self.x - self.width//2, draw_y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, (100, 80, 50), box_rect)
        pygame.draw.rect(screen, (150, 120, 80), box_rect, 2)
        
        # 绘制子弹图标
        for i in range(3):
            bullet_x = self.x - 6 + i * 6
            bullet_rect = pygame.Rect(bullet_x - 2, draw_y - 3, 4, 8)
            pygame.draw.rect(screen, YELLOW, bullet_rect)
            pygame.draw.circle(screen, YELLOW, (bullet_x, draw_y + 5), 2)

# 创建音效
try:
    shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=bytearray([0]*44)))  # 临时空音效
    reload_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=bytearray([0]*44)))
    hit_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=bytearray([0]*44)))
    health_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=bytearray([0]*44)))
    ammo_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=bytearray([0]*44)))
except:
    # 如果创建音效失败，创建空对象
    class DummySound:
        def play(self): pass
    shoot_sound = reload_sound = hit_sound = health_sound = ammo_sound = DummySound()

# 创建游戏对象
def create_game():
    # 创建玩家
    player1_controls = {"up": pygame.K_w, "down": pygame.K_s, 
                       "left": pygame.K_a, "right": pygame.K_d}
    player2_controls = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                       "left": pygame.K_LEFT, "right": pygame.K_RIGHT}
    
    player1 = Player(200, 350, BLUE, player1_controls, 1)
    player2 = Player(800, 350, RED, player2_controls, 2)
    
    # 设置玩家2的枪械类型为散弹枪
    player2.gun_type = "shotgun"
    player2.gun_color = ORANGE
    
    # 创建障碍物
    obstacles = [
        Obstacle(300, 200, 150, 40),
        Obstacle(500, 300, 40, 200),
        Obstacle(200, 500, 200, 40),
        Obstacle(700, 150, 40, 150),
        Obstacle(600, 500, 150, 40),
        Obstacle(400, 100, 40, 150),
        Obstacle(150, 200, 40, 150),
        Obstacle(800, 400, 150, 40),
    ]
    
    # 创建血包
    health_packs = [
        HealthPack(100, 100),
        HealthPack(900, 600),
        HealthPack(900, 100),
        HealthPack(100, 600),
    ]
    
    # 创建弹药箱
    ammo_boxes = [
        AmmoBox(500, 100),
        AmmoBox(500, 600),
        AmmoBox(300, 400),
        AmmoBox(700, 400),
    ]
    
    # 子弹列表
    bullets = []
    
    return player1, player2, obstacles, health_packs, ammo_boxes, bullets

# 绘制UI
def draw_ui(screen, player1, player2, game_time, round_num):
    # 绘制半透明背景
    ui_bg = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
    ui_bg.fill((0, 0, 0, 150))
    screen.blit(ui_bg, (0, 0))
    
    # 玩家1状态
    draw_player_status(screen, player1, 20, 20, "left")
    
    # 玩家2状态
    draw_player_status(screen, player2, SCREEN_WIDTH - 20, 20, "right")
    
    # 游戏时间和回合
    time_text = font_medium.render(f"时间: {int(game_time)}", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH//2 - time_text.get_width()//2, 20))
    
    round_text = font_medium.render(f"回合: {round_num}", True, YELLOW)
    screen.blit(round_text, (SCREEN_WIDTH//2 - round_text.get_width()//2, 60))
    
    # 控制说明
    controls_text1 = font_small.render("玩家1: WASD移动, 鼠标瞄准, 左键射击, R装弹", True, LIGHT_BLUE)
    controls_text2 = font_small.render("玩家2: 方向键移动, 自动瞄准, 回车射击, 小键盘0装弹", True, (255, 150, 150))
    
    screen.blit(controls_text1, (SCREEN_WIDTH//2 - controls_text1.get_width()//2, SCREEN_HEIGHT - 60))
    screen.blit(controls_text2, (SCREEN_WIDTH//2 - controls_text2.get_width()//2, SCREEN_HEIGHT - 30))

def draw_player_status(screen, player, x, y, align="left"):
    # 玩家名称和击杀数
    name_color = player.color
    name_text = font_medium.render(f"玩家{player.player_num} (击杀: {player.kill_count})", True, name_color)
    
    if align == "right":
        name_x = x - name_text.get_width()
    else:
        name_x = x
    
    screen.blit(name_text, (name_x, y))
    
    # 生命值条
    health_width = 200
    health_height = 20
    health_x = name_x
    health_y = y + 40
    
    # 生命值条背景
    pygame.draw.rect(screen, (50, 50, 50), (health_x, health_y, health_width, health_height))
    
    # 生命值填充
    health_percent = player.health / player.max_health
    health_fill_width = int(health_width * health_percent)
    
    # 根据生命值改变颜色
    if health_percent > 0.6:
        health_color = GREEN
    elif health_percent > 0.3:
        health_color = YELLOW
    else:
        health_color = RED
    
    pygame.draw.rect(screen, health_color, (health_x, health_y, health_fill_width, health_height))
    pygame.draw.rect(screen, WHITE, (health_x, health_y, health_width, health_height), 2)
    
    # 生命值文本
    health_text = font_small.render(f"{player.health}/{player.max_health}", True, WHITE)
    screen.blit(health_text, (health_x + health_width//2 - health_text.get_width()//2, health_y))
    
    # 弹药显示
    ammo_y = health_y + 30
    ammo_text = font_small.render(f"弹药: {player.ammo}/{player.max_ammo}", True, 
                                  YELLOW if player.ammo > 0 else RED)
    screen.blit(ammo_text, (health_x, ammo_y))
    
    # 枪械类型
    gun_text = font_small.render(f"武器: {player.gun_type}", True, player.gun_color)
    screen.blit(gun_text, (health_x, ammo_y + 25))

# 绘制击中效果
def draw_hit_effect(screen, x, y):
    for i in range(10):
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(5, 20)
        size = random.randint(2, 5)
        life = random.randint(10, 20)
        
        spark_x = x + math.cos(angle) * distance
        spark_y = y + math.sin(angle) * distance
        
        spark_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        spark_color = (255, random.randint(100, 255), 50, 200)
        pygame.draw.circle(spark_surface, spark_color, (size, size), size)
        screen.blit(spark_surface, (spark_x - size, spark_y - size))

# 主游戏函数
def main():
    player1, player2, obstacles, health_packs, ammo_boxes, bullets = create_game()
    
    # 游戏状态
    game_state = "PLAYING"  # PLAYING, PAUSED, GAME_OVER
    game_time = 180  # 3分钟游戏时间
    round_num = 1
    winner = None
    
    # 鼠标位置
    mouse_pos = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    
    # 击中效果
    hit_effects = []
    
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # 暂停/继续
                if event.key == pygame.K_p:
                    if game_state == "PLAYING":
                        game_state = "PAUSED"
                    elif game_state == "PAUSED":
                        game_state = "PLAYING"
                
                # 重新开始
                if event.key == pygame.K_r and game_state == "GAME_OVER":
                    player1, player2, obstacles, health_packs, ammo_boxes, bullets = create_game()
                    game_state = "PLAYING"
                    game_time = 180
                    round_num = 1
                    winner = None
                
                # 玩家装弹
                if event.key == pygame.K_r and game_state == "PLAYING":
                    player1.reload()
                if event.key == pygame.K_KP0 and game_state == "PLAYING":  # 小键盘0
                    player2.reload()
                
                # 切换武器（测试用）
                if event.key == pygame.K_1:
                    player1.gun_type = "rifle"
                    player1.gun_color = (150, 150, 150)
                if event.key == pygame.K_2:
                    player1.gun_type = "shotgun"
                    player1.gun_color = ORANGE
                if event.key == pygame.K_3:
                    player1.gun_type = "pistol"
                    player1.gun_color = LIGHT_BLUE
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game_state == "PLAYING":  # 左键
                    player1.shoot(bullets)
        
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        if game_state == "PLAYING":
            # 更新游戏时间
            game_time -= 1/FPS
            if game_time <= 0:
                game_state = "GAME_OVER"
                if player1.health > player2.health:
                    winner = "玩家1"
                elif player2.health > player1.health:
                    winner = "玩家2"
                else:
                    winner = "平局"
            
            # 玩家移动
            player1.move(keys, obstacles)
            player2.move(keys, obstacles)
            
            # 玩家瞄准
            player1.aim(mouse_pos=mouse_pos)
            player2.aim(other_player=player1)
            
            # 玩家2自动射击
            if keys[pygame.K_RETURN] and game_state == "PLAYING":
                player2.shoot(bullets)
            
            # 更新玩家
            player1.update()
            player2.update()
            
            # 更新障碍物
            for obstacle in obstacles:
                obstacle.update()
            
            # 更新血包
            for health_pack in health_packs:
                health_pack.update()
                
                # 检查玩家是否捡到血包
                if health_pack.active:
                    player1_rect = pygame.Rect(player1.x - player1.width//2, player1.y - player1.height//2, 
                                              player1.width, player1.height)
                    player2_rect = pygame.Rect(player2.x - player2.width//2, player2.y - player2.height//2, 
                                              player2.width, player2.height)
                    
                    if player1_rect.colliderect(health_pack.rect):
                        player1.health = min(player1.max_health, player1.health + 30)
                        health_pack.active = False
                        pygame.mixer.Sound.play(health_sound)
                        
                    if player2_rect.colliderect(health_pack.rect):
                        player2.health = min(player2.max_health, player2.health + 30)
                        health_pack.active = False
                        pygame.mixer.Sound.play(health_sound)
            
            # 更新弹药箱
            for ammo_box in ammo_boxes:
                ammo_box.update()
                
                # 检查玩家是否捡到弹药箱
                if ammo_box.active:
                    player1_rect = pygame.Rect(player1.x - player1.width//2, player1.y - player1.height//2, 
                                              player1.width, player1.height)
                    player2_rect = pygame.Rect(player2.x - player2.width//2, player2.y - player2.height//2, 
                                              player2.width, player2.height)
                    
                    if player1_rect.colliderect(ammo_box.rect):
                        player1.ammo = min(player1.max_ammo, player1.ammo + 15)
                        ammo_box.active = False
                        pygame.mixer.Sound.play(ammo_sound)
                        
                    if player2_rect.colliderect(ammo_box.rect):
                        player2.ammo = min(player2.max_ammo, player2.ammo + 15)
                        ammo_box.active = False
                        pygame.mixer.Sound.play(ammo_sound)
            
            # 更新子弹
            for bullet in bullets[:]:
                if not bullet.update(obstacles):
                    bullets.remove(bullet)
                    continue
                
                # 检查子弹是否击中玩家
                bullet_rect = pygame.Rect(bullet.x - bullet.size//2, bullet.y - bullet.size//2, 
                                         bullet.size, bullet.size)
                
                player1_rect = pygame.Rect(player1.x - player1.width//2, player1.y - player1.height//2, 
                                          player1.width, player1.height)
                player2_rect = pygame.Rect(player2.x - player2.width//2, player2.y - player2.height//2, 
                                          player2.width, player2.height)
                
                # 子弹不能击中发射者
                if bullet.owner == 1:
                    if bullet_rect.colliderect(player2_rect):
                        player2.health -= bullet.damage
                        bullets.remove(bullet)
                        pygame.mixer.Sound.play(hit_sound)
                        
                        # 添加击中效果
                        hit_effects.append({
                            'x': bullet.x,
                            'y': bullet.y,
                            'life': 15
                        })
                        
                        # 检查玩家2是否死亡
                        if player2.health <= 0:
                            player1.kill_count += 1
                            player2.health = player2.max_health
                            player2.x, player2.y = 800, 350
                        
                elif bullet.owner == 2:
                    if bullet_rect.colliderect(player1_rect):
                        player1.health -= bullet.damage
                        bullets.remove(bullet)
                        pygame.mixer.Sound.play(hit_sound)
                        
                        # 添加击中效果
                        hit_effects.append({
                            'x': bullet.x,
                            'y': bullet.y,
                            'life': 15
                        })
                        
                        # 检查玩家1是否死亡
                        if player1.health <= 0:
                            player2.kill_count += 1
                            player1.health = player1.max_health
                            player1.x, player1.y = 200, 350
            
            # 更新击中效果
            for effect in hit_effects[:]:
                effect['life'] -= 1
                if effect['life'] <= 0:
                    hit_effects.remove(effect)
            
            # 检查游戏结束
            if player1.kill_count >= 5 or player2.kill_count >= 5:
                game_state = "GAME_OVER"
                winner = "玩家1" if player1.kill_count >= 5 else "玩家2"
        
        # 绘制
        screen.fill((30, 30, 50))  # 深蓝色背景
        
        # 绘制网格背景
        grid_size = 50
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, (40, 40, 70), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, (40, 40, 70), (0, y), (SCREEN_WIDTH, y), 1)
        
        # 绘制障碍物
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # 绘制血包
        for health_pack in health_packs:
            health_pack.draw(screen)
        
        # 绘制弹药箱
        for ammo_box in ammo_boxes:
            ammo_box.draw(screen)
        
        # 绘制子弹
        for bullet in bullets:
            bullet.draw(screen)
        
        # 绘制玩家
        player1.draw(screen)
        player2.draw(screen)
        
        # 绘制击中效果
        for effect in hit_effects:
            draw_hit_effect(screen, effect['x'], effect['y'])
        
        # 绘制UI
        draw_ui(screen, player1, player2, game_time, round_num)
        
        # 绘制准星（玩家1）
        pygame.draw.circle(screen, WHITE, mouse_pos, 10, 2)
        pygame.draw.line(screen, WHITE, (mouse_pos[0] - 15, mouse_pos[1]), 
                        (mouse_pos[0] - 5, mouse_pos[1]), 2)
        pygame.draw.line(screen, WHITE, (mouse_pos[0] + 5, mouse_pos[1]), 
                        (mouse_pos[0] + 15, mouse_pos[1]), 2)
        pygame.draw.line(screen, WHITE, (mouse_pos[0], mouse_pos[1] - 15), 
                        (mouse_pos[0], mouse_pos[1] - 5), 2)
        pygame.draw.line(screen, WHITE, (mouse_pos[0], mouse_pos[1] + 5), 
                        (mouse_pos[0], mouse_pos[1] + 15), 2)
        
        # 绘制游戏状态
        if game_state == "PAUSED":
            pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 150))
            screen.blit(pause_surface, (0, 0))
            
            pause_text = font_large.render("游戏暂停", True, YELLOW)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            continue_text = font_medium.render("按P继续游戏", True, WHITE)
            screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        elif game_state == "GAME_OVER":
            game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            game_over_surface.fill((0, 0, 0, 200))
            screen.blit(game_over_surface, (0, 0))
            
            if winner == "平局":
                result_text = font_large.render("平局！", True, YELLOW)
            else:
                result_text = font_large.render(f"{winner} 获胜！", True, 
                                                BLUE if winner == "玩家1" else RED)
            
            screen.blit(result_text, (SCREEN_WIDTH//2 - result_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            
            stats_text = font_medium.render(f"玩家1 击杀: {player1.kill_count}  玩家2 击杀: {player2.kill_count}", True, WHITE)
            screen.blit(stats_text, (SCREEN_WIDTH//2 - stats_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
            
            restart_text = font_medium.render("按R重新开始，按ESC退出", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        # 更新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()