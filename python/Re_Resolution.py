
# 进行栅格图像的重采样
def Re_Resolution(inpath,outpath,xRes,yRes):
    """
        resampleAlg:重采样方式,算法包括：
                import gdalconst
                gdalconst.GRA_NearestNeighbour:near
                gdalconst.GRA_Bilinear:bilinear
                gdalconst.GRA_Cubic:cubic
                gdalconst.GRA_CubicSpline:cubicspline
                gdalconst.GRA_Lanczos:lanczos
                gdalconst.GRA_Average:average
                gdalconst.GRA_Mode:mode
    """
    from osgeo import gdal,gdalconst
    gdal.Warp(outpath,inpath,xRes=xRes,yRes=yRes,resampleAlg=gdalconst.GRA_Bilinear)
    print("Yes!")
    
if __name__ == "__main__":
    Re_Resolution(r"D:\GISData\China\FZ\fzdem1.tif","fzdem.tif",1000,1000)