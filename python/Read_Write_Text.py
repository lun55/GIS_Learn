def ReadText(path):
    """
        本程序用于打开文件
        path: 写入文件的路径
    """
    # w+ 模式是先写后读，w会将原有内容清空,因此一般使用r+,如果不创建新的文件，就在原文件内容后面追加新的内容
    with open(path,'r+',encoding='utf-8') as f:
        data = f.read()
        return data


def Writetext(path,data):
    """
        本程序用于将字符串写入文件
        path: 写入文件的路径
        data: 要写入的内容
    """
    with open(path,'w',encoding='utf-8') as f:
        f.write(data)
        print(data)

if __name__ == "__main__":
    data = ReadText(r"C:\Users\LMQ\Desktop\新建 文本文档 (2).txt")
    Writetext('q.csv',data.replace(' ',','))