"""
    用于将全国主要商圈位置边界数据转化为矢量地图
"""
import pandas as pd
import numpy as np
from shapely.geometry import Polygon
import geopandas as gp
data = pd.read_excel(r"C:\Users\LMQ\Desktop\全国主要商圈位置边界数据.xlsx") # 读取数据
polygons = [] # 全部商圈图形集合
points = [] # 用来临时存储不同商圈边界坐标集合
GDF = gp.GeoDataFrame()

for i in range(len(data)):
    edges = data['边界'].iloc[i].split(',') # 将坐标数据进行分割
    edges = list(np.float32(np.asarray(edges))) 
    print(len(edges))
    for j in range(0,int(len(edges)),2):
        points.append(edges[j:j+2])
    print(f"坐标对个数：{len(points)}")
    polygons.append(Polygon(points)) # 将坐标串转为面状图形
    points = [] # 坐标集合清空

GDF = gp.GeoDataFrame(data[['id','名称','城市编码']]) # 创建一个GeoDataframe列表
GDF['geometry'] = polygons # 向创建的表中加入几何图形
GDF.plot()  # 图形的可视化显示
#GDF.to_file(r"C:\Users\LMQ\Desktop\test\city.json",driver = 'GeoJSON') # 转化为GeoJSON格式的矢量文件
GDF.columns=['id','name','code','geometry'] # 将列名改为英文，中文报错
GDF.to_file(r"C:\Users\LMQ\Desktop\test\city") # 转化为shp格式的矢量文件