"""
    使用深圳市API获取共享单车数据
"""
import requests,json
import pandas as pd
import time
import threading
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
    start_time = time.time() 
    for i in range(start,end): 
               
        if getHTML(str(i))=="产生异常":
            print(f"页码数：{start}——{end}"+getHTML(str(i)))
            with open(file_path) as f:
                f.close()
            break
        else:
            bike_df = pd.DataFrame(getHTML(str(i))['data'],columns=['USER_ID','COM_ID','START_TIME','END_TIME','START_LAT','START_LNG','END_LAT','END_LNG'])
            
            # 判断是否存在文件
            if os.path.exists(file_path)==False:
                # 先创建一个文件,无列索引        
                bike_df.to_csv(file_path,index=False)       
            else:
                # 数据追加写入，减少内存开支    
                bike_df.to_csv(file_path,header=False, index=False,mode='a')
                print(i)

    end_time = time.time()
    timesum = end_time - start_time
    print(f"页码数：{start}——{end}，耗时：{timesum:.001f}\r",end='')

# class bikeThread():
#     def run():
#         pass
if __name__ == "__main__":
   
    bike_path = r'C:\Users\LMQ\Desktop\深圳共享单车'
    # for i in range(10):
    bike_file = os.path.join(bike_path,'1')
    spater(1,100,bike_file)