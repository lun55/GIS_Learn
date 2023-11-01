import requests
import json
import csv
import re
from Coordin_transformlat import gcj02towgs84

def Get_poi_polygon(key,polygon,keywords,page):
    '''
    这是一个能够从高德地图获取poi数据的函数
    key：为用户申请的高德密钥
    polygon：目标城市四个点的坐标
    keywords：POI数据的类型
    page：当前页数
    '''
    #设置header
    header = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}

    #将输进来的矩形进行格式化
    Polygonstr = str(polygon[0]) + ',' + str(polygon[1]) + '|' + str(polygon[2]) + ',' + str(polygon[3])

    #构建url
    url = 'https://restapi.amap.com/v3/place/polygon?polygon={}&key={}&keywords={}&page={}'.format(Polygonstr, key, keywords, page)
    print(url)
    #用get函数请求数据
    r = requests.get(url, headers=header)

    #设置数据的编码为'utf-8'
    r.encoding = 'utf-8'

    # 将请求得到的数据按照'utf-8'编码成字符串
    data = r.text
    return data

def Get_times_polygon(key,polygon,keywords):
    '''
    这是一个控制Get_poi_polygon申请次数的函数
    '''
    page = 1
    # 执行以下代码，直到count为0的时候跳出循环
    while True:
        # 调用第一个函数来获取数据
        result = Get_poi_polygon(key,polygon, keywords, page)
        # json.loads可以对获取回来JSON格式的数据进行解码
        content = json.loads(result)
        pois = content['pois']
        count = content['count']
        print(count)
        #如果区域内poi的数量大于800，则认为超过上限，返回False请求对区域进行切割
        if int(count) > 200:
            return False
        else:
            for i in range(len(pois)):
                name = pois[i]['name']
                location = pois[i]['location']
                if 'address' not in pois[i].keys():
                    address = str(-1)
                else:
                    address = pois[i]['address']
                adname = pois[i]['adname']
                result = gcj02towgs84(location)
                lng = result[0]
                lat = result[1]
                row = [name, address, adname, lng, lat]
                #调用写入函数来保存数据
                writecsv(row, keywords)
            if count == '0':
                break
                # 递增page
            page = page + 1

def writecsv(poilist,keywords):
    """
    这是写入成csv文件的函数
    :param poilist:
    :param keywords:
    :return: 输出的结果存放在代码文件夹下
    """
    with open('{}.csv'.format(keywords),'a',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(poilist)

def get_city_scope(key, cityname):
    """
        获取研究区域的空间范围坐标
    """
    parameters = 'key={}&keywords={}&subdistrict={}&output=JSON&extensions=all'.format(key, cityname, 0)
    url = 'https://restapi.amap.com/v3/config/district?'
    # 设置header
    header = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
    res = requests.get(url,params=parameters)
    jsonData = res.json()
    if jsonData['status'] == '1':
        district = jsonData['districts'][0]['polyline']
        district_list = re.split(';|\|',district)
        xlist, ylist = [], []
        for d in district_list:
            xlist.append(float(d.split(',')[0]))
            ylist.append(float(d.split(',')[1]))
        xmax = max(xlist)
        xmin = min(xlist)
        ymax = max(ylist)
        ymin = min(ylist)
        return [xmin, ymax, xmax, ymin]
    else:
        print ('fail to acquire: {}'.format(jsonData['info']))

