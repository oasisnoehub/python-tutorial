# Example
players = ["turtle", "rabbit"]
speeds = {
    "turtle": 2,
    "rabbit": 5
}

# for name in players:
#      print("{} ".format(name))

for name in players:
    print("{} 的速度是 {}".format(name, speeds[name]))
