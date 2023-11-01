import GetPoi_keywords as gp
"""
    使用四叉树分割算法，递归调用方式，好厉害！！！
"""
def Quadrangle(key,polygon,keywords):
    """
    :param key:高德地图密钥
    :param polygon: 矩形左上跟右下坐标的列表
    :param keywords: poi关键词
    :return:
    """
    #准备一个空列表，存放切割后的子区域
    PolygonList = []
    for i in range(len(polygon)):
        currentMinlat = round(polygon[i][0],6)#当前区域的最小经度    小数读取到6位
        currentMaxlat = round(polygon[i][2],6)#当前区域的最大经度
        currentMaxlon = round(polygon[i][1],6)#当前区域的最大纬度
        currentMinlon = round(polygon[i][3],6)#当前区域的最小纬度

        cerrnt_list = [currentMinlat, currentMaxlon, currentMaxlat, currentMinlon]
        #将多边形输入获取函数中，判断区域内poi的数量
        status = gp.Get_times_polygon(key,cerrnt_list,keywords)
        #如果数量大于800，那么返回False，对区域进行切分,否则返回区域的坐标对
        if status != False:
            print('该区域poi数量小于200，正在写入数据')
        else:
            PolygonList = []
            #左上矩形
            PolygonList.append([
                currentMinlat, #左经
                currentMaxlon, #上纬
                (currentMaxlat+currentMinlat)/2, #右经
                (currentMaxlon+currentMinlon)/2]) #下纬
            #右上矩形
            PolygonList.append([
                (currentMaxlat+currentMinlat)/2,#左经
                currentMaxlon, #上纬
                currentMaxlat, #右经
                (currentMaxlon+currentMinlon)/2#下纬
            ])
            #左下矩形
            PolygonList.append([
                currentMinlat,#左经
                (currentMaxlon+currentMinlon)/2,#上纬
                (currentMaxlat+currentMinlat)/2,#右经
                currentMinlon#下纬
            ])
            #右下矩形
            PolygonList.append([
                (currentMaxlat+currentMinlat)/2,#左经
                (currentMaxlon+currentMinlon)/2,#上纬
                currentMaxlat,#右经
                currentMinlon#下纬
            ])
            print(len(PolygonList))
            if len(PolygonList) == 0:
                break
            else:
                Quadrangle(key,PolygonList,keywords)


#这里修改为自己的高德密钥
key ='4a12f4b4fc0aa18d60e8f075034b87a1'

#这里修改自己的poi类型
keywords = '餐饮服务'

#这里输入想要查询的城市
city = '福州'

#调用高德查询行政区的API接口来返回矩形坐标对
Retance = gp.get_city_scope(key,city)

#存储区域矩形的列表
input_polygon = []
input_polygon.append(Retance)

Quadrangle(key,input_polygon,keywords)

