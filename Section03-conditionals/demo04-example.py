import time
import random

# 奖品列表（核心：list）
prizes = [
    "🍭 糖果",
    "🎮 游戏机",
    "📘 图书",
    "🧸 玩偶",
    "🍫 巧克力",
    "🎉 神秘大奖"
]

print("🎰 欢迎来到《幸运大转盘》 🎰")
input("👉 按回车开始转盘...")

print("\n奖品飞速旋转中，请盯紧屏幕 👀\n")

# 转盘动画（循环）
for i in range(15):
    current = random.choice(prizes)
    print("🎁", current)
    time.sleep(0.15)

# 最终结果
result = random.choice(prizes)

print("\n🎯 转盘停止！")
print("🎊 恭喜你抽中了：", result)
