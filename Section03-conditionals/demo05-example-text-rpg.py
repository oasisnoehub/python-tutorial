player_hp = 10
ai_hp = 10

round_num = 1

while player_hp > 0 and ai_hp > 0:
    print(f"\n===== 第 {round_num} 回合 =====")
    print(f"你 ❤️ {player_hp}    怪物 👾 {ai_hp}")

    # 本回合伤害
    player_damage = 0
    ai_damage = 0

    # ---------- 玩家回合 ----------
    player_action = input("你的行动（attack / defend）：")

    if player_action == "attack":
        player_damage = 2
        print("你准备攻击！")

    elif player_action == "defend":
        print("你进入防御姿态")
    else:
        print("你犹豫了，什么也没做")

    # ---------- AI 决策 ----------
    if ai_hp <= 3:
        ai_action = "defend"
    elif player_hp <= 3:
        ai_action = "attack"
    else:
        ai_action = "attack"

    print(f"怪物选择了：{ai_action}")

    if ai_action == "attack":
        ai_damage = 2

    # ---------- 结算阶段 ----------
    if player_action == "defend":
        ai_damage = max(0, ai_damage - 1)

    if ai_action == "defend":
        player_damage = max(0, player_damage - 1)

    player_hp -= ai_damage
    ai_hp -= player_damage

    print(f"你受到 {ai_damage} 点伤害")
    print(f"怪物受到 {player_damage} 点伤害")

    round_num += 1

# ---------- 游戏结果 ----------
if player_hp > 0:
    print("\n🎉 你击败了 AI 怪物！")
else:
    print("\n💀 你被 AI 怪物打败了")
