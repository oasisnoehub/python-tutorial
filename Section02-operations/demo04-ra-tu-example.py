turtle_distance = 0
rabbit_distance = 0

print("🏁 比赛开始！")

for round in range(1, 6):
    turtle_distance += 2
    rabbit_distance += 5

    print("\n第", round, "轮")
    print("🐢", "🐢" * turtle_distance)
    print("🐇", "🐇" * rabbit_distance)

print("\n🏁 比赛结束！")

if turtle_distance > rabbit_distance:
    print("🏆 乌龟赢了！")
else:
    print("🏆 兔子赢了！")
