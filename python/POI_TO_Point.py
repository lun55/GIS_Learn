"""
    用于将POI数据转化为矢量地图
    以获取的高德
"""

import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gp
data = pd.read_excel(r"C:\Users\LMQ\Desktop\test\POI\p.xlsx") # 读取数据
print(len(data['location']))

points = []
for i in range(len(data['location'])):
    loc = data['location'].iloc[i].split(",")
    loc = list(np.float32(np.asarray(loc)))
    points.append(Point(loc))

GDT = gp.GeoDataFrame(data)
GDT['geometry'] = points
GDT.plot()
GDT.to_file(r"C:\Users\LMQ\Desktop\test\POI\POI\poi.json",driver='GeoJSON',encoding='utf-8') # 转化为json格式的数据，使用encoding='utf-8'避免中文乱码