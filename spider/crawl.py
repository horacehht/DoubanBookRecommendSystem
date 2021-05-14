import random
import time

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
from crawl_book import CrawlBook
import pymysql

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


def crawl_tags(page):
    """获取每个标签网页的page页"""
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    res = visit(url)
    html = etree.HTML(res.text)
    tags = html.xpath('//*[@id="content"]//tr/td/a/text()')
    pages_url = ['https://book.douban.com/tag/' + tag + '?=' + str((page-1)*20) + '&type=T' for tag in tags]
    print('已获取' + str(len(pages_url)) + '个标签网页')
    return pages_url


def get_book_urls(tag_url):
    """获取每个标签网页中的第一页，20本书"""
    l = set()
    i = 20
    try:
        res = visit(tag_url)
        html = etree.HTML(res.text)
        books_urls = html.xpath('//*[@id="subject_list"]/ul//li/div[2]/h2/a/@href')
        for book_url in books_urls:
            l.add(book_url)
        print('已获取%d本书' % i)
        i += 20
    except Exception as e:
        print(e)
        print('要停一会!休息2秒')
        time.sleep(2)
    return list(l)


def save_to_mysql(data):
    """data是书籍的信息，json格式，要插入到release这个表"""

    book_name = data.get('book_name')
    author = data.get('author')
    press = data.get('出版社:')
    publishing_year = data.get('出版年:')
    page_num = data.get('页数:')
    price = data.get('定价:')
    ISBN = data.get('ISBN:')
    score = data.get('score')
    rating_num = data.get('rating_num')
    content_introduction = data.get('content_introduction')
    cover_url = data.get('cover_url')
    readers = data.get('readers')
    insert_data = (book_name, author, press, publishing_year, score, rating_num, page_num, price, ISBN,
                   content_introduction, cover_url, readers)
    insert_sql = """
        INSERT INTO books(book_name, author, press, publishing_year, score, rating_num, page_num, price,
        ISBN, content_introduction, cover_url, readers)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        # 执行sql语句
        cur.execute(insert_sql, insert_data)
        # 提交执行
        conn.commit()
        print('《' + book_name + '》' + '信息已存储成功!')
    except Exception as e:
        print(e)
        conn.rollback()
        print('存储失败!')


if __name__ == '__main__':
    tags_url = crawl_tags(1)  # 获取第一页
    for page in tags_url:
        book_urls = get_book_urls(page)  # 某个标签的第一页的书链接
        for book_url in book_urls:
            try:
                res = visit(book_url)  # 对那一页的一本书进行访问
                book = CrawlBook(res)  # 建立一个书对象，data存放其信息，以json存储
                save_to_mysql(book.data)  # 将该书信息插入mysql中，继续第二本
            except Exception as e:
                print(e)
                print('歇一会QAQ，就2秒')
                time.sleep(3)
        # 换到另外一个标签的第1页
    print('爬取完成!')
    conn.close()  # 关闭连接，不然多了，数据库会锁
