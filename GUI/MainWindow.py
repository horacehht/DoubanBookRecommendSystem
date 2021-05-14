import sys
import res
import re
import pymysql
import datetime
import pandas as pd
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextBrowser, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QIcon
from algorithm.Recommend import RecommendItemCF
from UserWindow import UserWindow
from BookInfo import BookInfo
from SearchWindow import SearchWindow


class MainWindow(QWidget):
    def __init__(self, user):
        super(MainWindow, self).__init__()
        self.user = user
        self.setWindowTitle("豆瓣书籍推荐系统")
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

        # 读取用户数据存入user_df
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

        # 读取书籍数据存入books_df
        sql_f2 = "SELECT * FROM books"
        try:
            self.cur.execute(sql_f2)
            results2 = self.cur.fetchall()
            columnDes2 = self.cur.description  # 获取连接对象的描述信息
            columnNames2 = [columnDes2[i][0] for i in range(len(columnDes2))]  # 获取列名
            # 得到的results为二维元组，逐行取出，转化为列表，再转化为df
            self.books_df = pd.DataFrame([list(i) for i in results2], columns=columnNames2)
        except Exception as e:
            print(e)
        self.books_df = self.books_df.iloc[:, [0, 1, 3, 4, 5]]  # 选取了书名，作者，出版年份，评分， 评分人数

        # 传给UserWindow的参数
        self.user_index = self.user_df[self.user_df['nickname'] == self.user].index[0]
        self.user_read_num = self.user_df.iloc[self.user_index][1]
        self.user_read_books = list(eval(self.user_df.iloc[self.user_index][2]).keys())

        self.welcome_label = QLabel("<h1>欢迎您! " + self.user + "</h1>", self)
        self.recommend_label = QLabel("<h1>根据您的喜好为您推荐以下书籍: </h1>", self)
        self.recommend_table = QTableWidget(self)
        self.hot_books_label = QLabel("<h1>热门书籍:</h1>", self)
        self.hot_books_table = QTableWidget(self)

        hot_books_ori = self.books_df[self.books_df.score > 8.5]
        self.hot_books = hot_books_ori[hot_books_ori.rating_num > 50000]  # 选取评分大于8.5，评论人数大于50000的书籍
        self.hot_books = self.hot_books.sort_values(by=['rating_num'], ascending=True)  # 按评论人数进行排序

        self.user_window_button = QPushButton("个人主页", self)
        self.user_window_button.clicked.connect(self.show_user_window)

        self.search_button = QPushButton("书籍搜索", self)
        self.search_button.clicked.connect(self.show_search_window)

        self.book_info_button = QPushButton("书籍详细信息", self)
        self.book_to_know_label = QLabel("<h2>您要查询哪本书的详细信息?</h2>", self)
        self.book_to_know_line = QLineEdit(self)
        self.book_to_know_line.setPlaceholderText("请在此处填入想查询详细信息的书籍")
        self.book_info_button.clicked.connect(lambda: self.show_book_info(self.book_to_know_line.text()))
        # book_name = self.book_to_know_line.text()，然后再传给show_book_info(book_name)居然就搜索不到了，太诡异了
        start = datetime.datetime.now()
        # 算法部分
        # 准备训练数据
        sql_f3 = "SELECT * FROM douban_book_users WHERE read_num<=50"  # 滤除读书多的用户，不然书籍多了，算法算的很久
        # <= 50，96个用户，5秒加载完毕。<= 100，176个用户，24秒加载完毕。
        self.train = dict()
        self.cur.execute(sql_f3)
        results3 = self.cur.fetchall()
        for i in range(len(results3)):
            # 因为read_book_and_score这个字段有些数据是不闭合的，所以要检查一下
            self._user = results3[i][1]  # 提取每个用户名
            if results3[i][3][-1] == '}':
                self.new_json = eval(results3[i][3])  # 转换成字典dict形式
                self.train.setdefault(self._user, self.new_json)
            else:
                self.new_json = eval(results3[i][3] + '}')
                self.train.setdefault(self._user, self.new_json)
        # 算法推荐
        self.algorithm = RecommendItemCF(self.train)
        self.algorithm.ItemSimilarity()  # 算物品相似度
        self.rec_books = self.algorithm.recommend(self.user)  # 获得推荐书籍
        end = datetime.datetime.now()
        print("算法运行时间:" + str((end-start).seconds) + "秒")
        print(self.rec_books)

        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.h_layout = QHBoxLayout()

        self.h1_layout.addWidget(self.welcome_label)
        self.h1_layout.addWidget(self.user_window_button)
        self.v1_layout.addLayout(self.h1_layout)
        self.v1_layout.addWidget(self.recommend_label)
        self.v1_layout.addWidget(self.recommend_table)

        self.h3_layout.addWidget(self.hot_books_label)
        self.h3_layout.addWidget(self.search_button)

        self.h2_layout.addWidget(self.book_to_know_label)
        self.h2_layout.addWidget(self.book_to_know_line)
        self.h2_layout.addWidget(self.book_info_button)

        self.v2_layout.addLayout(self.h2_layout)
        self.v2_layout.addLayout(self.h3_layout)
        self.v2_layout.addWidget(self.hot_books_table)

        self.h_layout.addLayout(self.v1_layout)
        self.h_layout.addLayout(self.v2_layout)

        self.setLayout(self.h_layout)

        self.rec_books_table_init()
        self.set_rec_books_table()
        self.hot_books_table_init()
        self.set_hot_books_table()

    def rec_books_table_init(self):
        self.recommend_table.setColumnCount(5)
        self.recommend_table.setHorizontalHeaderLabels(['书名', '作者', '出版年份', '评分', '评分人数'])
        self.recommend_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recommend_table.setRowCount(0)

    def set_rec_books_table(self):
        row = self.recommend_table.rowCount()
        # self.recommend_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 表格不可编辑
        for book in self.rec_books:
            empty = self.books_df[self.books_df.book_name == book].empty
            if empty:
                rec_book_name = "《" + book + "》"
                rec_book_author = "未知"
                rec_book_year = "未知"
                rec_book_score = "未知"
                rec_book_rating_num = "未知"
                # 说明书库里没有这本书，直接跳过不插入此本
            else:
                book_index = self.books_df[self.books_df.book_name == book].index[0]
                rec_book_name = "《" + self.books_df.iloc[book_index][0] + "》"
                if pd.isna(self.books_df.iloc[book_index][1]):
                    rec_book_author = ''
                else:
                    rec_book_author = self.books_df.iloc[book_index][1]
                if pd.isna(self.books_df.iloc[book_index][2]):
                    rec_book_year = ''
                else:
                    rec_book_year = self.books_df.iloc[book_index][2]
                if pd.isna(self.books_df.iloc[book_index][3]):
                    rec_book_score = '0'
                else:
                    rec_book_score = str(self.books_df.iloc[book_index][3])
                if pd.isna(self.books_df.iloc[book_index][4]):
                    rec_book_rating_num = '0'
                else:
                    rec_book_rating_num = str(self.books_df.iloc[book_index][4])
            self.recommend_table.insertRow(row)
            self.recommend_table.setItem(row, 0, QTableWidgetItem(rec_book_name))
            self.recommend_table.setItem(row, 1, QTableWidgetItem(rec_book_author))
            self.recommend_table.setItem(row, 2, QTableWidgetItem(rec_book_year))
            self.recommend_table.setItem(row, 3, QTableWidgetItem(rec_book_score))
            self.recommend_table.setItem(row, 4, QTableWidgetItem(rec_book_rating_num))

    def hot_books_table_init(self):
        self.hot_books_table.setColumnCount(5)
        self.hot_books_table.setHorizontalHeaderLabels(['书名', '作者', '出版年份', '评分', '评分人数'])
        self.hot_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hot_books_table.setRowCount(0)

    def set_hot_books_table(self):
        row = self.hot_books_table.rowCount()
        # self.hot_books_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 表格不可编辑
        for i in range(len(self.hot_books)):
            self.hot_books_table.insertRow(row)
            hot_book_name = "《" + self.hot_books.iloc[i][0] + "》"
            hot_book_author = self.hot_books.iloc[i][1]
            hot_book_year = self.hot_books.iloc[i][2]
            hot_book_score = str(self.hot_books.iloc[i][3])
            hot_book_rating_num = str(self.hot_books.iloc[i][4])

            self.hot_books_table.setItem(row, 0, QTableWidgetItem(hot_book_name))
            self.hot_books_table.setItem(row, 1, QTableWidgetItem(hot_book_author))
            self.hot_books_table.setItem(row, 2, QTableWidgetItem(hot_book_year))
            self.hot_books_table.setItem(row, 3, QTableWidgetItem(hot_book_score))
            self.hot_books_table.setItem(row, 4, QTableWidgetItem(hot_book_rating_num))

    def show_user_window(self):
        """展示个人中心界面"""
        self.user_window = UserWindow(self.user, self.user_read_num, self.user_read_books)
        self.user_window.show()

    def show_search_window(self):
        """展示搜索界面"""
        self.search_window = SearchWindow()
        self.search_window.show()

    def show_book_info(self, book_name):
        """展示书籍详细信息窗口"""
        self.book_info_window = BookInfo(book_name, self.user)
        self.book_info_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow("土豆")
    mainwindow.show()
    sys.exit(app.exec_())