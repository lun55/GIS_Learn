import datetime
def UTC_to_Zone(Date,hours):
    """
        将格林时间转为北京时间
        时间格式为2023-09-05T09:00:00时,采用 '%Y-%m-%dT%H:%M:%S'
    """
    dataEachUtcTime = datetime.datetime.strptime(Date,r'%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=hours)
    return dataEachUtcTime
    
print(UTC_to_Zone('2023-09-05T21:00:00',8))