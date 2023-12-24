"""
    函数程序设计举例（一）
    两个球员在一个有四面边界的场地上用球拍击球。开始比赛时，其中一个球员首先发球。接下来球员交替击球，直到可以判定得分为止，这个过程称为回合。当一名球员未能进行一次合法击打时，回合结束。
    未能打中球的球员输掉这个回合。如果输掉这个回合的是发球方，那么发球权交给另一方;如果输掉的是接球方，则仍然由这个回合的发球方继续发球。
    每回合结束,由赢得该回合的一方发球。球员只能在他们自己的发球局中得分。首先达到15分的球员赢得一局比赛。
"""
import random

# 介绍性信息
def printIntro():
    print("这个程序模拟两个选手A和B的某种竞技比赛")
    print("程序运行需要A和B的能力值(以0到1之间的小数表示)")

# 获取程序运行需要的参数
def getInputs():
    probA = eval(input("请输入球员A的能力值(0-1):"))
    probB = eval(input("请输入球员B的能力值(0-1):"))
    n = eval(input('请输入比赛的场次:'))
    return probA,probB,n

# 游戏结束条件
def Gameover(a,b):
    return a == 15 or b == 15 # 判断是否两队员各自的总得分为15

# 模拟一场比赛
def simOneGames(probA,probB):
    scoreA,scoreB = 0,0
    serving = "A"
    while not Gameover(scoreA,scoreB):
        if serving == "A":
            if random.random() < probA:  # random.random()：生成一个0到1的随机符点数: 0 <= n < 1.0
                scoreA  += 1
            else:
                serving = "B"
        else:
            if random.random() < probB:
                scoreB  += 1
            else:
                serving = "A"   
    return scoreA,scoreB       


# 模拟n场比赛
def simNGames(n,probA,probB):
    winA,winB = 0,0
    for i in range(n):
        scoreA,scoreB = simOneGames(probA,probB)
        if scoreA > scoreB:
            winA += 1
        else:
            winB += 1
    return winA,winB

# 输出比赛结果
def printSummary(winsA,winsB):
    n = winsA + winsB
    print("竞技分析开始，共模拟{}场比赛".format(n))
    print('选手A获胜{}场比赛，占比{:0.1%}'.format(winsA,winsA/n))
    print('选手B获胜{}场比赛，占比{:0.1%}'.format(winsB,winsB/n))

if __name__ == "__main__":
    printIntro()
    probA,probB,n = getInputs()
    winA,winB = simNGames(n,probA,probB)
    printSummary(winA,winB)