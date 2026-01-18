import pgzrun
import random

# 设置窗口尺寸
WIDTH = 1100
HEIGHT = 800
TITLE = "星际收集者 - Python 课程演示"

# --- 游戏角色设置 ---
# 如果你没有图片，pgzero 会显示一个色块，或者你可以找一个图标命名为 'alien.png'
alien = Actor('alien') 
alien.pos = (WIDTH // 5, HEIGHT // 5)

star = Actor('star')
star.pos = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))

score = 0
game_over = False

def draw():
    screen.clear()
    screen.fill((30, 30, 60))  # 深蓝色背景
    
    if game_over:
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30)
    else:
        alien.draw()
        star.draw()
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")

def update():
    global score, game_over
    
    if game_over:
        return

    # 键盘控制逻辑
    if keyboard.left and alien.left > 0:
        alien.x -= 5
    if keyboard.right and alien.right < WIDTH:
        alien.x += 5
    if keyboard.up and alien.top > 0:
        alien.y -= 5
    if keyboard.down and alien.bottom < HEIGHT:
        alien.y += 5

    # 碰撞检测逻辑
    # 逻辑原理：if alien_rect.colliderect(star_rect)
    if alien.colliderect(star):
        score += 1
        place_star()
        # 如果你有声音文件 'collect.wav'，取消下面这行的注释
        # sounds.collect.play()

def place_star():
    """随机重置星星的位置"""
    star.x = random.randint(50, WIDTH-50)
    star.y = random.randint(50, HEIGHT-50)

def time_up():
    """游戏限时结束"""
    global game_over
    game_over = True

# 设置 15 秒游戏倒计时
clock.schedule(time_up, 15.0)

pgzrun.go()
