import sys
import res
import pandas as pd
import numpy as np
import pymysql
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTextBrowser, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap


class BookInfo(QWidget):
    def __init__(self, name):
        super(BookInfo, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("书籍详细信息")
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.resize(1400, 800)
        self.name = name
        # 书籍信息
        # 数据库操作
        self.conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="doubanbook",  # 数据库名
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        sql_f = "SELECT * FROM douban_book_release"
        try:
            self.cur.execute(sql_f)
            results = self.cur.fetchall()
            columnDes = self.cur.description  # 获取连接对象的描述信息
            columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
            # 得到的results为二维元组，逐行取出，转化为列表，再转化为df
            self.books_df = pd.DataFrame([list(i) for i in results], columns=columnNames)
        except Exception as e:
            print(e)
        self.conn.close()  # 关闭连接

        self.books_detailed = self.books_df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]  # 不选封面链接和读者
        try:
            self.pix = QPixmap(r'../book_covers_release/' + "{}".format(self.name) + '.png')
            self.pic = QLabel(self)
            self.pic.setPixmap(self.pix)
        except Exception as e:
            print(e)

        try:
            # 如果数据缺失，就写成空，下同，但我发现数据里空就是''，而不是NaN，所以可以直接赋值
            self.author = list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].author)[0]
            self.press = list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].press)[0]
            self.publishing_year = list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)]
                                            .publishing_year)[0]
            if list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].score)[0] == 0:
                self.score = str('暂无')
            else:
                self.score = str(list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].score)[0])
            self.rating_num = \
                str(list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].rating_num)[0])
            if list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].page_num)[0] == 0:
                self.page_num = str('未知')
            else:
                self.page_num = \
                    str(list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].page_num)[0])
            self.ISBN = list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].ISBN)[0]

            self.introduction = \
                list(self.books_detailed[self.books_detailed.book_name == "{}".format(self.name)].content_introduction)[0]

            self.name_label = QLabel("<font size=10><b>" + self.name + "</b></font>")
            self.author_label = QLabel("<h2>" + "作者: " + self.author + "</h2>")
            self.press_label = QLabel("<h2>" + "出版社: " + self.press + "</h2>")
            self.publishing_year_label = QLabel("<h2>" + "出版年份: " + self.publishing_year + "</h2>")
            # 上面已经处理过score，str(score)
            self.score_label = QLabel('<strong><font size="15" color="red">' + "评分: " + self.score + "</font></strong>")
            self.rating_num_label = QLabel('<strong><font size="15" color="red">' + "评分人数: " + self.rating_num + "</font></strong>")
            self.page_num_label = QLabel("<h2>" + "书籍页数: " + self.page_num + "</h2>")
            self.ISBN_label = QLabel("<h2>" + "ISBN: " + self.ISBN + "</h2>")

            self.like_button = QPushButton("喜欢这本书", self)

            self.introduction_label = QLabel("<h1><b>书籍简介:</b></h1>", self)
            self.introduction_browser = QTextBrowser(self)
            self.introduction_browser.setText("<h2>" + self.introduction + "</h2>")

            self.v1_layout = QVBoxLayout()
            self.v2_layout = QVBoxLayout()
            self.h_layout = QHBoxLayout()
            self.v_layout = QVBoxLayout()

            self.v1_layout.addWidget(self.author_label)
            self.v1_layout.addWidget(self.press_label)
            self.v1_layout.addWidget(self.publishing_year_label)
            self.v1_layout.addWidget(self.ISBN_label)
            self.v1_layout.addWidget(self.page_num_label)


            self.v2_layout.addWidget(self.score_label)
            self.v2_layout.addWidget(self.rating_num_label)
            self.v2_layout.addWidget(self.like_button)

            self.h_layout.addWidget(self.pic)
            self.h_layout.addLayout(self.v1_layout)
            self.h_layout.addLayout(self.v2_layout)

            self.v_layout.addLayout(self.h_layout)
            self.v_layout.addWidget(self.introduction_label)
            self.v_layout.addWidget(self.introduction_browser)

            self.setLayout(self.v_layout)

        except Exception as e:
            print(e)
            self.resize(200, 200)
            self.no_find = QLabel("<h1>对不起, 没有找到相关书籍!</h1>", self)
            self.h_layout = QHBoxLayout()
            self.h_layout.addWidget(self.no_find)
            self.setLayout(self.h_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    info = BookInfo("不老泉")
    info.show()
    sys.exit(app.exec_())