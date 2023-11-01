"""
    本程序用于对GDP进行网格化
    思路1:分区域方案
        计算栅格单元的位置进而计算出其在那个行政区划内部,得到不同区域的栅格矩阵,
    根据每个栅格矩阵的值计算每个格点的比值,将区域GDP乘以这个比值,得到栅格单元的GPD的值。
    可能的改进: 1. 使用图形判断函数时,每次都要调用shp文件, 造成资源的浪费
               2. 使用遍历方法计算区域总值, 效率十分低下, 是否有还其他的手段, 比如参考ArcGIS(速度很快)?
    思路1:总区域方案
        直接使用整个区域计算权重,根据权重使用总GDP进行分配
    使用像元中心坐标代表栅格单元的位置
"""

from osgeo import gdal
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# 读取栅格数据
def GetRasterinfo(path):
    """
        用来读取栅格数据的信息
        :param path: 文件路径
        返回值: Dataset,Projection,GeoTransform,data
    """
    Dataset = gdal.Open(path)
    Metadata = Dataset.GetMetadata() # 元数据信息
    Projection = Dataset.GetProjection()  # 数据投影信息
    GeoTransform = Dataset.GetGeoTransform() # 数据仿射变换信息
    data = Dataset.ReadAsArray() # 获取栅格数据
    return Dataset,Projection,GeoTransform,data

# 保存栅格文件
def savetif(dataset, path, RasterXSize, RasterYSize, im_geotrans, im_proj,NoDataValue,datatype):
    """
    将数组保存为tif文件
    :param dataset: 需要保存的数组
    :param path: 需要保存出去的路径，包含文件名
    :param RasterXSize: 数组宽度
    :param RasterYSize: 数组高度
    :param im_geotrans: 仿射矩阵信息
    :param im_proj: 投影信息
    :param NoDataValue 无效值
    :param datatype 数据类型——gdal.GDT_Float32, gdal.GDT_Int16
    """
    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(path, RasterXSize, RasterYSize, 1, datatype) # 波段数为1
    outdataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    outdataset.SetProjection(im_proj)  # 写入投影
    outdataset.GetRasterBand(1).WriteArray(dataset)
    outdataset.GetRasterBand(1).SetNoDataValue(NoDataValue) # 设置无效值
    print("yes")

# 判断点是否在图形范围内
def Filter_images(path_conservation_area, longitude_f, latitude_f):
    """
    用来判断点是否在区域范围内，类似的也可以判断线和面
    :param path_conservation_area: 面数据路径
    :param longitude_f: 经度
    :param latitude_f: 纬度
    :return: True or False
    """
    dataset = gpd.GeoDataFrame.from_file(path_conservation_area) # 使用GeoPandas读取矢量文件！！！
    # 判断点是否在Features内
    for i in range(len(dataset)):
        boundary_shape = dataset['geometry'][i]
        boundary_OBJECTID = dataset['OBJECTID'][i]
        # 将shp区域加载到工作空间
        determine_contain = boundary_shape.contains(Point([longitude_f, latitude_f])) # Returns a Series of dtype('bool') with value True for each aligned geometry that contains other.
        # 判断点是否在区域内
        if determine_contain:
            break
    return determine_contain,boundary_OBJECTID

# 统计计算各区域的总值
def SumCount():
    """
        找出栅格点位于哪个区域内, 再按照不同的区域统计总值
    """
    Dataset,Projection,GeoTransform,Data = GetRasterinfo(r"D:\GISData\China\FZ\Result_GDP.tif")
    print(GeoTransform)
    band = Dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    x_min = GeoTransform[0]
    y_min = GeoTransform[3]
    Resolution = GeoTransform[1]
    SumList = [0,0,0,0,0,0,0,0,0,0,0,0,0] # 用来保存各个区域的统计总值
    for i in range(Dataset.RasterYSize):
         for j in range(Dataset.RasterXSize):
            if Data[i][j] == NoDataValue:
                 continue
            else:
                Lon = x_min + Resolution*j+Resolution/2 # 获取栅格中心经度坐标
                Lat = y_min - Resolution*i-Resolution/2 # 获取栅格中心纬度坐标，需要注意的一点，图像从左上角开始算起，向右经度增大，而向下纬度是减小的
                determine_contain,Feature_OBJECTID = Filter_images(r"D:\GISData\China\FZ\FZCounry_P0.shp",Lon,Lat) # 利用Feature_OBJECTID来匹配区域
                print("进度:{}".format(i/Dataset.RasterYSize),determine_contain)
                if determine_contain:
                   SumList[Feature_OBJECTID-1] += Data[i][j]
    print(SumList) 
    return SumList
    
def CalculaterAreaGDP():
    """
        分区域计算每个栅格的GDP数值,结果更好但很费时
    """
    SumList = [579281, 1019686, 561970, 775717, 460941, 163393, 188128, 529405, 203123, 281304, 261510, 219443, 560569] # 每个区域的人口总量
    GDPList = [1030.11, 1414.04, 2362.19, 1063.28, 671.44, 359.06, 639.84, 881.16, 389.78, 339.2, 659.25, 339.31, 1143.9] # 每个区域的GDP总量
    Dataset,Projection,GeoTransform,Data = GetRasterinfo(r"D:\GISData\China\FZ\FZPDN_P.tif")
    x_min = GeoTransform[0] # 图像的左上角经度   
    y_min = GeoTransform[3] # 图像的左上角纬度  
    Resolution = GeoTransform[1] # 图像的分辨率   
    GDPdata = np.zeros(Data.shape) # 创建一个形状与Data相同的数组，并用0进行填充   
    for i in range(Dataset.RasterYSize):
         for j in range(Dataset.RasterXSize):
            if Data[i][j] == 65535:
                GDPdata[i][j] = -9999  # 将无效区域的值设为-9999
                continue
            else:
                Lon = x_min + Resolution*j+Resolution/2 # 获取栅格中心经度坐标
                Lat = y_min - Resolution*i-Resolution/2 # 获取栅格中心纬度坐标，需要注意的一点，图像从左上角开始算起，向右经度增大，而向下纬度是减小的
                determine_contain,Feature_OBJECTID = Filter_images(r"D:\GISData\China\FZ\FZBounds.shp",Lon,Lat)               
                print("进度:{}%".format(i/Dataset.RasterYSize*100),determine_contain)
                if determine_contain:
                    GDPdata[i][j] = GDPList[Feature_OBJECTID-1]*Data[i][j]/SumList[Feature_OBJECTID-1]
    return GDPdata          

def CalculaterGDP():
    """
        利用整个研究区域计算每个栅格的GDP数值,计算速度快，但存在区域均值化的问题
    """
    Dataset,Projection,GeoTransform,Data = GetRasterinfo(r"D:\GISData\China\FZ\FZPDN_P.tif")
    GDPdata = np.zeros(Data.shape)
    GDP = 11324.48
    for i in range(Dataset.RasterYSize):
         for j in range(Dataset.RasterXSize):
            if Data[i][j] == 65535:
                 GDPdata[i][j] = -9999  # 将无效区域的值设为-9999
                 continue
            else:
                print("进度:{}".format(i/Dataset.RasterYSize))
                GDPdata[i][j] = GDP*Data[i][j]/Data[Data!=65535].sum() # Data[Data!=65535].sum()为Numpy的过滤方法
    return GDPdata   

if __name__ == "__main__":
    # GDPdata = CalculaterGDP() # 按整个区域进行GDP的分配，但将导致区域GDP分布更加均值化
    # GDPdata = CalculaterAreaGDP() # 按各个县级区域进行GDP的分配，GDP分布更为合理，但也更为耗时
    # Dataset,Projection,GeoTransform,Data = GetRasterinfo(r"D:\GISData\China\FZ\FZPDN_P.tif")
    #savetif(GDPdata,'GDP.tif',Dataset.RasterXSize,Dataset.RasterYSize,GeoTransform,Projection,-9999,gdal.GDT_Float32) #对数据进行保存
    SumCount()
    pass
    