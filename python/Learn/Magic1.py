# 魔法函数的使用

class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name: %s)' % self.name
    __repr__=__str__

##动态返回一个属性
class Student2(object):
    def __init__(self):
        self.name = 'Michael'
    def __getattr__(self, attr):   #动态返回一个属性
        if attr=='score':
            return 100
        if attr=='age':
            return 25

        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)



s = Student('Tom')
print(s)

s2=Student2()
print(s2.name," ",s2.score," ",s2.age,"\n")

s2.score=90
s2.age=40
print(s2.name," ",s2.score," ",s2.age,"\n")


class Fib(object):
    def __init__(self):
        self.a, self.b = 1, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 1000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

##    def __getitem__(self, n):
##        a, b = 1, 1
##        for x in range(n):
##            a, b = b, a + b
##        return a
##测试fib
print("fib测试")
f=Fib()
for n in f:
    print(n," ",end="")
##print("\nf[10]:",f[10])  

class Fib2(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if n.step==None:
                step = 1
            else:
                step=n.step
            print(start,stop,step)

            if start is None:
                start = 0
                
            a, b = 1, 1
            L = []
            for x in range(stop):
               if x>=start and ((x-start)%step ==0): ##切片
                    L.append(a)                                  
               a, b = b, a + b
            return L
    



f2=Fib2()
print("\nf2[10]:",f2[10])
print(f2[5:10])
print(f2[5:10:2])

##如果需要打印出f2[5:10:2]
