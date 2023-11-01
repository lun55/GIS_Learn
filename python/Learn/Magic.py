# 定义了一个数据类Length，一个带有量纲的数据类型
class Length:
    __metric = {"mm" : 0.001, "cm" : 0.01, "m" : 1, "km" : 1000,
                "in" : 0.0254, "ft" : 0.3048, "yd" : 0.9144,
                "mi" : 1609.344 } # 给出进制的单位
    
    def __init__(self, value, unit = "m" ):
        self.value = value
        self.unit = unit

    def Converse2Metres(self): # 将长度的单位转换为米
        return self.value * Length.__metric[self.unit]
    
    def __add__(self, other): # 重构加法，即1+1的运算  x._add_() 这种带有双下划线的方法称为magic方法或dunder方法
        l = self.Converse2Metres() + other.Converse2Metres() # 先统一成相同的单位，即米单位，进行两个量的加法的运算
        return Length(l / Length.__metric[self.unit], self.unit ) # 再进行单位的转换，返回Length类型的值，使返回的值的单位与输入的单位相同
    
    def __str__(self): # 重写python内置函数str()
        return str(self.Converse2Metres()) # 返回类型必须是一个字符串，不能是int,float啥的
    
    def __repr__(self): # 重写python内置函数repr()，一般repr()函数返回给定对象的可打印表示字符串。
        return "Length(" + str(self.value) + ", '" + self.unit + "')"


"""
    Write a class with the name Ccy, similar to the previously defined Length class.Ccy should contain values in various currencies, e.g. "EUR", "GBP" or "USD". An instance should contain the amount and the currency unit. The class, you are going to design as an exercise, might be best described with the following example session:

    from currencies import Ccy
    v1 = Ccy(23.43, "EUR")
    v2 = Ccy(19.97, "USD")
    print(v1 + v2)
    print(v2 + v1)
    print(v1 + 3) # an int or a float is considered to be a EUR value
    print(3 + v1)
    Live Python trai
    搞定
"""

class Ccd:
    _metric = {"EUR":7.7330,"GBP":8.8764,"USD":7.3177,'CNY':1} # 分别为欧元、英镑以及美元，我们将基本单位设为人民币

    def __init__(self,value,unit = 'CNY') -> None: # 这里的箭头是用来为函数添加元函数,描述函数的返回类型，从而方便开发人员开发使用
        self.value = value
        self.unit = unit

    def converse2CNY(self):
        return self.value*Ccd._metric[self.unit]
    
    def __add__(self,other):
        
        if type(other) is int or type(other) is float:
            c = self.converse2CNY() + other
        elif type(other) is Ccd:
            c = self.converse2CNY() + other.converse2CNY()
        return Ccd(c/Ccd._metric[self.unit],self.unit)
    
    def __radd__(self,other):
        return Ccd.__add__(self,other)
    
    def __str__(self):
        return str(self.value) + self.unit
def func(x,y):
   	print(x,y)

if __name__ == "__main__":
    x = Length(4) # 类似类型int(),float()等等，x为Length类的实例，默认单位为米
    print(x)
    y = eval(repr(x))
    z = Length(4.5, "yd") + Length(1) # 这里的Length(1)就是Length._add()的参数
    print(repr(z))
    print(z)

    v1 = Ccd(23.43, "EUR")
    v2 = Ccd(19.97, "USD")
    print(v1 + v2)
    print(v2 + v1)
    print(v1 + 3) # an int or a float is considered to be a CNY value
    print(3 + v1)

    a = "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    b = "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    print(a is b)
    
    
