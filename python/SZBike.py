"""
    使用深圳市API获取共享单车数据
"""
import requests,json
import pandas as pd
import time
from threading import Thread
import os

# 获取第i页的数据，每页1000行
def getHTML(i):
    url = "https://opendata.sz.gov.cn/api/29200_00403627/1/service.xhtml"
    try:
        header = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'opendata.sz.gov.cn',
            'Origin': 'https://opendata.sz.gov.cn',
            'Referer': 'https://opendata.sz.gov.cn/maintenance/personal/toApiTest',
            'Cookie': '_trs_uv=k1q8o8my_2368_4sr9; JSESSIONID=bb524432-c11d-4154-a813-7aefbc5a9f2d',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        }
        formdata = {
            "page": i,
            "rows": "1000",
            "appKey": '9d676000c3354c84a3d081594fba6e7a'
        }
        response = requests.get(url, params=formdata, headers=header)
    
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        return {"asd":"asda"}
    except:
        return "产生异常"

# 获取第i页的数据，每页1000行 页数是从第1页开始的
def spater(start,end,file_path):
    timesum = 0
    start_time = time.time()  # 开始时间
    # 如果初值为0，将其设为1，因为页码是从1开始计算的
    if start==0:
        start = 1
    
    for i in range(start,end): 
        data  = getHTML(str(i))

        # 如果触发异常，最多尝试10次
        j = 0
        while j<10 and data=="产生异常":
            time.sleep(2)
            print(f'出错，尝试第{j+1}次')
            data  = getHTML(str(i))
            j += 1

        # 如果尝试10次后依旧失败，则抛出异常
        if j==10:
            raise ValueError('A very specific bad thing happened.')
        
        else:

            bike_df = pd.DataFrame(data['data'],columns=['USER_ID','COM_ID','START_TIME','END_TIME','START_LAT','START_LNG','END_LAT','END_LNG'])

            # 判断是否存在文件
            if os.path.exists(file_path)==False:
                # 先创建一个文件,无列索引        
                bike_df.to_csv(file_path,index=False)       
            else:
                # 数据追加写入，减少内存开支    
                bike_df.to_csv(file_path,header=False, index=False,mode='a')
                # print("第"+str(i)+"页")

    end_time = time.time()  # 结束时间
    timesum = end_time - start_time
    print(f"页码数：{start}——{end}，耗时：{timesum:.001f}\n",end='')


if __name__ == "__main__":
   
    # 文件保存的路径
    bike_path = r'E:\Data\深圳共享单车'

    t = []  # 线程列表 
    # 多线程执行,提高数据下载速度
    for i in range(0,20):
        page_start = i*1000
        page_end = page_start + 1000
        bike_file = os.path.join(bike_path,f"bike{page_start}-{page_end}.csv")
        t.append(Thread(target=spater, args=(page_start, page_end, bike_file), name="Thread-"+str(i)))
        t[i].start()
    for j in t:
        print('a')
        j.join() 
    print('程序执行结束\n')
    