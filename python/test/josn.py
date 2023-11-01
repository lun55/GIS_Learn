import requests
import pandas as pd
import json

p1 = open(r"C:\Users\LMQ\Desktop\test\POI\p1.txt",mode='r',encoding='utf-8')
p2 = open(r"C:\Users\LMQ\Desktop\test\POI\p2.txt",mode='r',encoding='utf-8')
p3 = open(r"C:\Users\LMQ\Desktop\test\POI\p3.txt",mode='r',encoding='utf-8')
p4 = open(r"C:\Users\LMQ\Desktop\test\POI\p4.txt",mode='r',encoding='utf-8')
p5 = open(r"C:\Users\LMQ\Desktop\test\POI\p5.txt",mode='r',encoding='utf-8')
p6 = open(r"C:\Users\LMQ\Desktop\test\POI\p6.txt",mode='r',encoding='utf-8')
p7 = open(r"C:\Users\LMQ\Desktop\test\POI\p7.txt",mode='r',encoding='utf-8')
p8 = open(r"C:\Users\LMQ\Desktop\test\POI\p8.txt",mode='r',encoding='utf-8')

data1 = pd.DataFrame(eval(p1.readline())['pois'])
data2 = pd.DataFrame(eval(p2.readline())['pois'])
data3 = pd.DataFrame(eval(p3.readline())['pois'])
data4 = pd.DataFrame(eval(p4.readline())['pois'])
data5 = pd.DataFrame(eval(p5.readline())['pois'])
data6 = pd.DataFrame(eval(p6.readline())['pois'])
data7 = pd.DataFrame(eval(p7.readline())['pois'])
data8 = pd.DataFrame(eval(p8.readline())['pois'])

data = pd.DataFrame()
data = pd.concat([data1,data2,data3,data4,data5,data6,data7,data8])
print(data[['address','pname','cityname','type','adname','name','location']])
data[['address','pname','cityname','type','adname','name','location']].to_excel(r"C:\Users\LMQ\Desktop\test\POI\p.xlsx",index=None)
