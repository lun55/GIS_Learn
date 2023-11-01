"""
    矢量裁剪栅格影像
"""
from osgeo import gdal

def mask(inputpath,shppath,outpath,dataType,Nodatavalue):
    """
        用于栅格图像的掩膜
        :params inputpath 要处理的栅格路径
        :params shppath 矢量掩膜文件路径
        :params outpath 文件输出路径
        :params dataType 栅格的数据类型——gdal.GDT_Int16、gdal.GDT_Float32
        :params Nodatavalue 栅格的无效值
    """
    data = gdal.Open(inputpath)
    try:
        ds = gdal.Warp(
            outpath, # 文件输出路径
            data,
            format = 'GTiff',
            cutlineDSName = shppath,      
            cropToCutline = True, # 保证裁剪后影像大小跟矢量文件的图框大小一致
            outputType = dataType, # gdal.GDT_Int16,
            dstNodata = Nodatavalue)
        print(outpath + "   裁切成功")
    except:
        print(outpath + "   裁切失败")    

if __name__ == "__main__":
    inputpath = 'POI2022_1.tif'
    shppath = r"D:\GISData\China\FZ\FZCounry_P.shp"
    outpath = "POI2022_cut.tif"
    dataType = gdal.GDT_Int16
    Nodatavalue = -1
    mask(inputpath,shppath,outpath,dataType,Nodatavalue)