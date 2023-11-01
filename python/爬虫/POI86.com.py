import requests
import re
import time
import pandas

# 获取当前街道页面
root_url = "https://www.poi86.com/poi/amap/street/7086/1.html"
res = requests.get(root_url)
html = res.text

#存储当前街道的POI
street_poi = []

# 获取所有POI的URL
links = re.finditer(r'href="/poi/amap2/(.*)"',html)

# 进入每个POI页面
for link in links:
    now_POI = link.group()[7:-1]
    now_URL = "https://www.poi86.com/" + now_POI
    now_res = requests.get(now_URL)
    html = now_res.text
    ## 获取每个POI的地点名、所属省份、所属城市、所属区县、乡镇街道、详细地址、所属分类、X坐标、Y坐标

    poi_name = re.findall('<h1>(.*)</h1>',html)[0]  ## 使用<h1>标签匹配地点名

    ## 首先获取list-group类下的内容
    list_group = re.findall('<ul class="list-group">(.*)</ul>',html,re.S)### re.S匹配换行符

    ## 省份、城市、区县、街道为一种格式，共用一种re表达式
    poi_pro_city_town_street = re.findall('数据">(.*)</a>',list_group[0])
    province = poi_pro_city_town_street[0]
    city = poi_pro_city_town_street[1]
    town = poi_pro_city_town_street[2]
    street = poi_pro_city_town_street[3]

    ## 详细地址、所属分类、X坐标、Y坐标为一种格式，公用一种re表达式
    poi_add_type_X_Y = re.findall('span> (.*)</li>',list_group[0])
    address = poi_add_type_X_Y[-8]
    type = poi_add_type_X_Y[-6]
    X = poi_add_type_X_Y[-5].split(",")[0]
    Y = poi_add_type_X_Y[-5].split(",")[1]

    ## 写入当前poi的信息
    poi_inf = []
    poi_inf.append(poi_name)
    poi_inf.append(province)
    poi_inf.append(city)
    poi_inf.append(town)
    poi_inf.append(street)
    poi_inf.append(address)
    poi_inf.append(type)
    poi_inf.append(X)
    poi_inf.append(Y)
    street_poi.append(poi_inf)

# 将当前街道POI信息写入文件
column_list = ['名称','省份','城市','区县','街道','地址','分类','X','Y']
pandas.DataFrame(data=street_poi,columns=column_list).to_excel(r"C:\Users\HP\Desktop\poi.xlsx")
