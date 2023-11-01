"""
    使用高德API获取POI数据
"""
import requests
import pandas as pd
def getHTML(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status() # 如果网页链接失败则会产生一次异常
        r.encoding = r.apparent_encoding
        return r
    except:
        return "产生异常"   

i = 1 # 翻页计数
data = pd.DataFrame()

while True:
    url = "https://restapi.amap.com/v3/place/text?key=4a12f4b4fc0aa18d60e8f075034b87a1&types=050100&city=320100&citylimit=true&offset=25&page="+str(i)
    print(url)

    status = eval(getHTML(url).text)['status'] # 读取状态码 结果状态值，值为0或1
    count = eval(getHTML(url).text)['count'] # 读取搜索方案数目
    if count == '0' or status == '0':  # 中止条件
        print("Stop")
        break   

    i += 1 
    POIs = eval(getHTML(url).text)['pois'] # 将str转换为dict类型，并从中提取出pois对应的值
    data0 = pd.DataFrame(POIs) # 将列表的形式的值转为DataFrame表单
    data = pd.concat([data,data0]) # 将将表单追加到表单中

print(data[['address','pname','cityname','type','adname','name','location']])
data[['address','pname','cityname','type','adname','name','location']].to_excel(r"C:\Users\LMQ\Desktop\新建文本文档.xlsx",index=None) # 将数据存储为Exel文件