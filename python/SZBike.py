"""
    使用深圳市API获取共享单车数据
"""
import requests,json
import pandas as pd
import time
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


def spater(start,end,filename):
    timesum = 0
    for i in range(start,end): 
        start_time = time.time() 
        
        if getHTML(str(i))=="产生异常":
            print(getHTML(str(i)))
        else:
            df1 = pd.DataFrame(getHTML(str(i))['data'],columns=['USER_ID','COM_ID','START_TIME','END_TIME','START_LAT','START_LNG','END_LAT','END_LNG'])
            
            if i==start:        
                df1.to_csv(r"C:\\Users\\LMQ\\Desktop\\"+filename+".csv",index=None)       
            else:
                df = pd.read_csv(r"C:\\Users\\LMQ\\Desktop\\"+filename+".csv")
                df = pd.concat([df,df1])
                df.to_csv(r"C:\\Users\\LMQ\\Desktop\\"+filename+".csv",index=None)
        print()
        end_time = time.time()
        timesum += end_time - start_time
        print(f"{(i-start)/(end-start)*100:0.1f}%"+f"------>运行时间：{end_time - start_time:.001f} 秒; 总时间：{timesum:.001f}\r",end='')

if __name__ == "__main__":
    spater(300,400,'共享单车2')