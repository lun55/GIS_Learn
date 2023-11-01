import pandas as pd
from shapely.geometry import Point,Polygon,LineString
import geopandas as gpd
import matplotlib.pyplot as plt

def csv_Point(csvdata,path,Lat,Lon):
    """
        将CSV文件转化为点SHP文件
        csvdata: pandas读取的数据
        path: 文件保存的路径
        Lat: 纬度所在的列名
        Lon: 经度所在的列名
    """
    GDF = gpd.GeoDataFrame(csvdata)
    GDF['geometry'] = gpd.points_from_xy(GDF[Lon],GDF[Lat]) #  x是经度，y是纬度 不要用反了 当数据中本身含有经度和纬度列时，使用GeoPandas本身的方法即可
    GDF.plot()
    plt.show()  # In a normal Python environment, you need to import matplotlib to show the image
    GDF.to_file(path,driver='GeoJSON',encoding = 'utf-8',index=None,crs='4326')

def json_shp(jsonpath,savepath):
    """
        将josN文件转为shp文件
        jsonpath: json文件的路径
        savepath: shp保存的路径

    """
    Gjson = gpd.read_file(jsonpath,encoding='utf-8')
    GDF = gpd.GeoDataFrame(Gjson)
    GDF.to_file(savepath,encoding='utf-8')

def main():
    """
        运行的主程序
    """
    data = pd.read_csv(r"E:\Vscode_Project\q.csv",encoding='utf-8')
    data['lat'] = data['lat']/100
    data['lon'] = data['lon']/100
    print(data)
    csv_Point(data,'FZStatiion.json','lat','lon')
    json_shp('FZStatiion.json','FZStatiion')


if __name__ == "__main__":
    main()