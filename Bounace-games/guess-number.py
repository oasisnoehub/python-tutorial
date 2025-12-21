import random

def guess_number_game():
    print("🎮 欢迎来到猜数字小游戏！")
    print("我已经想好了一个 1 到 100 之间的数字。")
    print("你能猜到是多少吗？")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        user_input = input("请输入你的猜测（或输入 q 退出）：")

        if user_input.lower() == "q":
            print("👋 游戏结束，下次再来玩吧！")
            break

        if not user_input.isdigit():
            print("❌ 请输入一个有效的数字！")
            continue

        guess = int(user_input)
        attempts += 1

        if guess < secret_number:
            print("📉 太小了！")
        elif guess > secret_number:
            print("📈 太大了！")
        else:
            print(f"🎉 恭喜你！你猜对了！")
            print(f"你一共猜了 {attempts} 次。")
            break

guess_number_game()

