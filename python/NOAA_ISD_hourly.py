"""
    本程序用于对NOAA ISD hourly 气象站数据的数据清洗
    时间分辨率:3小时
"""
import pandas as pd
import UTC_to_Zone

data = pd.read_csv(r"D:\下载\588470_FZ.csv",encoding='utf-8')
data = data[['DATE','WND','AA1']] # 要保留的数据列 包括日期、风、降水量

# inplace=True表示对原DataFrame进行修改,false时将返回一个新的DataFrame，不会修改源数据。
# subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
data.dropna(subset=['AA1'],inplace=True)
data.reset_index(drop=True,inplace=True) # 将行序号重置为0,1,2，方便后续的处理
data['begindate'] = data['DATE']
data['WindDriction'] = data['DATE']
Results = []
print(data.index)           
for i in range(len(data)):
    # 筛选出2023年9月4日到6日之间的有效数据
    if data['DATE'].iloc[i][0:7] == '2023-09' and (0000 < int(data['AA1'].iloc[i].split(',')[1]) < 9999) and (4 <= int(data['DATE'].iloc[i][8:10]) <= 6):
        # data.drop(index=i,inplace=True)   # 不知为何，使用drop时会发生索引的越界
        data['begindate'].iloc[i] = UTC_to_Zone.UTC_to_Zone(data['DATE'].iloc[i],2)
        data['DATE'].iloc[i] = UTC_to_Zone.UTC_to_Zone(data['DATE'].iloc[i],8) # 将UTC时间转为北京时间
        data['AA1'].iloc[i] = int(data['AA1'].iloc[i].split(',')[1])*0.1  # 将降水量乘比例因子得到真实降水量
        data['WindDriction'].iloc[i] = data['WND'].iloc[i].split(',')[0]
        data['WND'].iloc[i] = int(data['WND'].iloc[i].split(',')[3])*0.1  # 将风速乘比例因子得到真实风速
        Results.append(data.iloc[i])

data = pd.DataFrame(Results)
data.reset_index(drop=True,inplace=True)
data['3h'] = data['AA1']
data['3h'].iloc[0] = 0.3
for i in range(len(data)):
    if i != 0 :
        data['3h'].iloc[i] = float(data['AA1'].iloc[i]) - float(data['3h'].iloc[i-1])

print(data)

data.to_csv('p1.csv',index=None) # 将清洗后的数据保存为CSV文件
