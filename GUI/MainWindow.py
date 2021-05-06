import sys
import res
import pymysql
import pandas as pd
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextBrowser, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QHeaderView
from PyQt5.QtGui import QIcon
from algorithm import Recommend


class MainWindow():
    def __init__(self, user):
        super(MainWindow, self).__init__()
        self.setWindowTitle("豆瓣电影推荐系统")
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.resize(1400, 800)
        # 数据库操作
        self.conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="doubanbook",  # 数据库名
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        sql_f1 = "SELECT * FROM douban_book_users"
        try:
            self.cur.execute(sql_f1)
            results1 = self.cur.fetchall()
            columnDes1 = self.cur.description  # 获取连接对象的描述信息
            columnNames1 = [columnDes1[i][0] for i in range(len(columnDes1))]  # 获取列名
            # 得到的results为二维元组，逐行取出，转化为列表，再转化为df
            self.user_df = pd.DataFrame([list(i) for i in results1], columns=columnNames1)
        except Exception as e:
            print(e)
        self.user_df = self.user_df.iloc[:, [1, 2, 3]]  # 选取了名字，读书数量，读的书及相应评分

        sql_f2 = "SELECT * FROM douban_book_release"
        try:
            self.cur.execute(sql_f2)
            results2 = self.cur.fetchall()
            columnDes2 = self.cur.description  # 获取连接对象的描述信息
            columnNames2 = [columnDes2[i][0] for i in range(len(columnDes2))]  # 获取列名
            # 得到的results为二维元组，逐行取出，转化为列表，再转化为df
            self.books_df = pd.DataFrame([list(i) for i in results2], columns=columnNames2)
        except Exception as e:
            print(e)
        self.books_df = self.books_df.iloc[:, [0, 1, 3, 4, 5]]  # 选取了书名。作者，出版年份，评分， 评分人数
        self.user = user
        self.user_book_num = self.user_df[self.user_df[]]