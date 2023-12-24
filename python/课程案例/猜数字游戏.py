"""
    编写一个“猜数字游戏”的程序,在1到1000 之间随机产生一个数，然后请用户循环猜测 (输入) 这个数字，对于每
    个答案只回答“猜大了”或 “猜小了”，直到猜测准确为止，输出用户的猜测次数。
"""
import random
i = 0
x = random.randint(1,1000)
while True:
    y = eval(input("请输入数字："))
    i = i + 1
    if y < x:
        print('猜小了')
    elif y > x:
        print('猜大了')
    elif y == x:
        print(f"您的猜测次数为：{i}")
        break 