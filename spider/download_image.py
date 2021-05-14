import pymysql
import os
import requests
import random
import pandas as pd

conn = pymysql.connect(  # 连接本地数据库
        host="localhost",
        user="root",  # 要填root
        password="htht0928",  # 填上自己的密码
        database="doubanbook",  # 数据库名
        charset="utf8"
    )
cur = conn.cursor()

# 请求头
headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Connection': 'close'},
    {
        'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        'Connection': 'close'},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        'Connection': 'close'},
    {
        'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        'Connection': 'close'},
    {
        'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        'Connection': 'close'},
    {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        'Connection': 'close'},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        'Connection': 'close'}
    ]

# http代理接入服务器地址端口
proxyHost = "http-proxy-t3.dobel.cn"
proxyPort = "9180"

#账号密码
proxyUser = "HORACEC0JB9ONL0"
proxyPass = "t7PG9y5o"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}


def visit(targetUrl):
    """访问网址，返回响应"""
    session = requests.Session()
    session.keep_alive = False
    res = session.get(targetUrl, proxies=proxies, headers=random.choice(headers))
    return res


if __name__ == '__main__':
    sql_f = "SELECT * FROM books"
    try:
        cur.execute(sql_f)
        results = cur.fetchall()
        columnDes = cur.description  # 获取连接对象的描述信息
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
        # 得到的results为二维元组，逐行取出，转化为列表，再转化为df
        books_df = pd.DataFrame([list(i) for i in results], columns=columnNames)
    except Exception as e:
        print(e)
    books_df = books_df.dropna(axis=0, subset=["cover_url"])  # 去除cover_url有缺失值的行
    if 'books_cover' in os.listdir(os.getcwd()):
        pass
    else:
        os.mkdir('books_cover')
    os.chdir('books_cover')
    for i in len(books_df):
        while True:  # 直到下了这张图片
            try:
                img = visit(books_df.iloc[i][10])  # 获取图片链接
                if img.status_code == 200:
                    img = img.content
                    break
            except:
                pass

        try:
            print("正在保存第" + str(i + 1) + "张图片...")
            with open(books_df[i][0] + '.jpg', 'wb') as f:
                f.write(img)
        except:
            print('保存失败!')