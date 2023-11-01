"""
    本程序用于将POI数据进行网格化
    构建一个栅格网络, 再根据点的经纬度信息判断点在栅格单元中的位置, 统计栅格单元中兴趣点的数量, 最终实现POI网格化的构建。
	难点：网格的大小应设为多少
"""
import geopandas as gpd
from osgeo import gdal,osr
import GDP_Grid
import numpy as np
import MaskRaster

def Point_Num_2Grid(AreaPath,Pointpath,outpath,resolution,Nodatavalue):
    """
        根据网格单元内的点的数量，生成栅格图像

        :param AreaPath 面矢量文件，用定义栅格图像的空间范围
        :param Pointpath 点矢量文件
        :param outpath 栅格图像的输出路径
        :param resolution 栅格图像的空间分辨率
        :param Nodatavalue 栅格图像的无效值
    """
    AreaGDF = gpd.read_file(AreaPath) # 读取矢量文件
    bounds = AreaGDF.total_bounds # 获取整个区域的边界，返回一个数组 numpy.ndarray，minx, miny, maxx, maxy
    minx,miny,maxx,maxy = bounds[0],bounds[1],bounds[2],bounds[3]

    PoiGDF = gpd.read_file(Pointpath)
    PoiGDF = PoiGDF.to_crs(AreaGDF.crs) # 进行投影转换，使其坐标系与边界矢量文件相同

    # 进行栅格图像的相关设置
    columns = int((maxx - minx)/resolution) + 1 # 定义栅格单元的行数 加1是使得栅格图像能完整覆盖整个矢量范围
    row = int((maxy - miny)/resolution) + 1 # 定义栅格单元的列数
    Rasterdata = np.zeros((row, columns)) # 定义数组，给定其形状与初始值

    # 判断POI的位置，从而对其进行栅格化
    for i in range(len(PoiGDF)): 
        lat, lon = PoiGDF['geometry'][i].y, PoiGDF['geometry'][i].x # 获取POI的坐标
        X = int((lon - minx)/resolution)
        Y = int((maxy - lat)/resolution)
        Rasterdata[Y][X] += 1
    im_geotrans = (minx,resolution,0,maxy,0,-resolution) #（左上角x坐标， 水平分辨率，旋转参数， 左上角y坐标，旋转参数，-垂直分辨率）注意最后一个参数应该为负值

    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(int(str(PoiGDF.crs).split(':')[1]))  # 定义输出的坐标系与边界矢量文件相同
    im_proj = srs.ExportToWkt()

    try:
        # 保存栅格图像
        GDP_Grid.savetif(Rasterdata,outpath,columns,row,im_geotrans,im_proj,Nodatavalue,gdal.GDT_Int16)
        print("成功")
    except:
        print("失败")


if __name__ == "__main__":
    AreaPath = r"D:\GISData\China\FZ\FZCounry_P.shp"
    Pointpath = r"D:\GISData\China\福州——POI2022餐饮.shp"
    outpath = "POI2022_500.tif"
    resolution = 500 # 分辨率的大小设置很重要，不同的空间尺度下表现出的信息有所不同
    Nodatavalue = -1
    Point_Num_2Grid(AreaPath,Pointpath,outpath,resolution,Nodatavalue)
    MaskRaster.mask(outpath,AreaPath,'POI2022_500_cut.tif',gdal.GDT_Int16,Nodatavalue)
    
    