import sys
sys.path.append(r"E:\Vscode_Project\Jupyter\python")
import GDP_Grid
import numpy as np
from osgeo import gdal


def Guiyihua(inpath,outpath):
    """
        对数据进行无量纲化处理，归一化到[0.5,1]
    """
    dataset,Projection,GeoTransform,data = GDP_Grid.GetRasterinfo(inpath)
    band = dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    print(NoDataValue)
    # data[data != NoDataValue] = 0.5+0.5*(data[data != NoDataValue]-data[data != NoDataValue].min())/(data[data != NoDataValue].max()-data[data != NoDataValue].min())
    data[data != NoDataValue] = (data[data != NoDataValue]-data[data != NoDataValue].min())/(data[data != NoDataValue].max()-data[data != NoDataValue].min())
    #data[data != NoDataValue] = (data[data != NoDataValue].max()-data[data != NoDataValue])/(data[data != NoDataValue].max()-data[data != NoDataValue].min()) # DEMSTD (0,1)
    GDP_Grid.savetif(data,outpath,dataset.RasterXSize,dataset.RasterYSize,GeoTransform,Projection,NoDataValue,gdal.GDT_Float32)

def Preclass(inpath,outpath):
    dataset,Projection,GeoTransform,data = GDP_Grid.GetRasterinfo(inpath)
    band = dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    data = np.where(data >=200,1,data)
    data = np.where((data < 25) & (1 < data),0,data)
    data = np.where((data < 200) & (100 <= data),0.8,data)
    data = np.where((data < 100) & (50 <= data),0.6,data)
    data = np.where((data < 50) & (25 <= data),0.4,data)      
    GDP_Grid.savetif(data,outpath,dataset.RasterXSize,dataset.RasterYSize,GeoTransform,Projection,NoDataValue,gdal.GDT_Float32)
    pass

def Popclass(inpath,outpath):
    dataset,Projection,GeoTransform,data = GDP_Grid.GetRasterinfo(inpath)
    band = dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    data = np.where((data < 1092) & (1 <= data),0.6,data)
    data = np.where((data >=31427) & (data != NoDataValue),1,data)   
    data = np.where((data < 4753) & (1092 <= data),0.7,data)
    data = np.where((data < 14256) & (4753 <= data),0.8,data)
    data = np.where((data < 31427) & (14256 <= data),0.9,data)      
    GDP_Grid.savetif(data,outpath,dataset.RasterXSize,dataset.RasterYSize,GeoTransform,Projection,NoDataValue,gdal.GDT_Float32)
    pass

def GDPclass(inpath,outpath):
    dataset,Projection,GeoTransform,data = GDP_Grid.GetRasterinfo(inpath)
    band = dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    data = np.where((data < 3) & (0 <= data),0.6,data)
    data = np.where(data >=141,1,data)
    data = np.where((data < 22) & (3 <= data),0.7,data)
    data = np.where((data < 64) & (22 <= data),0.8,data)
    data = np.where((data < 141) & (64 <= data),0.9,data)      
    GDP_Grid.savetif(data,outpath,dataset.RasterXSize,dataset.RasterYSize,GeoTransform,Projection,NoDataValue,gdal.GDT_Float32)
    pass


def main():
    pass


if __name__ == "__main__":
    GDPpath = r"D:\GISData\China\FZ\GDP.tif"
    # DemSTD = r"D:\GISData\China\FZ\fzdem_STD.tif"
    Veg = r"D:\GISData\China\FZ\VEGR.tif"
    Precipatition = r"D:\GISData\China\FZ\IdwPre1.tif"
    Pop = r"D:\GISData\China\FZ\FZPDN_P.tif" # 人口无法进行归一化处理，各区人口差异太大，存在极大值的情况，导致其余值为0
    Slope = r"D:\GISData\China\FZ\FZSlopet.tif"
    Result_impaction = r"D:\GISData\China\FZ\Result_impaction.tif"
    #Guiyihua(GDPpath,'GDPguiyi1.tif')
    #Guiyihua(Precipatition,'Precipatition1.tif')
    #Guiyihua(Veg,'Vegguiyi.tif')
    #Popclass(Pop,'Popguiyi2.tif')
    # GDPclass(GDPpath,'GDPNEW.tif')
    # c = 0.5*(0.5*I)
    #Guiyihua(Slope,'Slope.tif')
    dataset,Projection,GeoTransform,data = GDP_Grid.GetRasterinfo(Result_impaction)
    band = dataset.GetRasterBand(1)
    NoDataValue = band.GetNoDataValue()
    print(data[data!=NoDataValue].sum())
    main()
