import sys
import res # 导入资源文件
import pandas as pd
import pymysql
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextBrowser, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QHeaderView
from PyQt5.QtGui import QIcon


class SearchWindow(QWidget):
    def __init__(self):
        super(SearchWindow, self).__init__()  # 使用super函数可以实现子类使用父类的方法
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
        sql_f = "SELECT * FROM books"
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

        self.books_df = self.books_df.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.books_df = self.books_df.dropna()
        self.books_df = self.books_df.drop_duplicates(subset='book_name')
        self.changed_df = self.books_df  # 一个副本，依照这个来进行输出，而更改这个的排序方式，就可更改输出的排序
        self.setWindowTitle("书籍搜索")
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.resize(600, 800)
        self.value = 0  # 0代表按书名搜索，1代表按作者搜素
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText('输入想搜索的内容')
        self.search_label = QLabel("搜索方式: ")
        self.name_search_button = QPushButton("书名搜索", self)
        self.name_search_button.clicked.connect(self.value_0)
        self.name_search_button.clicked.connect(lambda: self.Fuzzy_search(self.search_edit.text()))
        self.author_search_button = QPushButton("作者搜索", self)
        self.author_search_button.clicked.connect(self.value_1)
        self.author_search_button.clicked.connect(lambda: self.Fuzzy_search(self.search_edit.text()))

        self.sort_label = QLabel("      显示方式:", self)
        self.default_button = QPushButton("默认", self)
        self.default_button.clicked.connect(self.default_sort)
        self.by_score_button = QPushButton("评分(降序)", self)
        self.by_score_button.clicked.connect(self.score_sort)
        self.score_times = 1
        self.by_ratingnum_button = QPushButton("评论人数(降序)", self)
        self.by_ratingnum_button.clicked.connect(self.ratingnum_sort)
        self.rating_times = 1

        self.search_browser = QTextBrowser(self)

        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.layout_init()

    def layout_init(self):
        """布局设置，目的是使init方法看起来简洁"""
        self.h1_layout.addWidget(self.search_edit)
        self.h1_layout.addWidget(self.search_label)
        self.h1_layout.addWidget(self.name_search_button)
        self.h1_layout.addWidget(self.author_search_button)

        self.h2_layout.addWidget(self.sort_label)
        self.h2_layout.addWidget(self.default_button)
        self.h2_layout.addWidget(self.by_score_button)
        self.h2_layout.addWidget(self.by_ratingnum_button)

        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.addWidget(self.search_browser)

        self.setLayout(self.v_layout)

    def ratingnum_sort(self):
        if self.rating_times % 2 == 1:
            self.changed_df = self.changed_df.sort_values(by=['rating_num'], ascending=False)
            self.Fuzzy_search(self.search_edit.text())
            # 搜索完后按钮文字便问评论人数(升序)
            self.by_ratingnum_button.setText("评论人数(升序)")
        else:
            self.changed_df = self.changed_df.sort_values(by=['rating_num'], ascending=True)
            self.Fuzzy_search(self.search_edit.text())
            self.by_ratingnum_button.setText("评论人数(降序)")
        self.rating_times += 1

    def score_sort(self):
        if self.score_times % 2 == 0:
            self.changed_df = self.changed_df.sort_values(by=['score'], ascending=False)
            self.Fuzzy_search(self.search_edit.text())
            self.by_score_button.setText("评分(升序)")
            self.score_times += 1
        else:
            self.changed_df = self.changed_df.sort_values(by=['score'], ascending=True)
            self.Fuzzy_search(self.search_edit.text())
            self.by_score_button.setText("评分(降序)")
            self.score_times += 1

    def default_sort(self):
        self.changed_df = self.books_df
        self.Fuzzy_search(self.search_edit.text())

    # 通过self.value值判别按下的是书名搜索还是作者搜索按钮
    def value_0(self):
        self.value = 0

    def value_1(self):
        self.value = 1

    def Fuzzy_search(self, keyword):
        """
        模糊搜索功能，书名与作者
        :param keyword: 搜索的关键字
        """
        self.search_browser.clear()
        mark = 1
        self.matched_num = 0
        self.search_by = ['book_name', 'author']
        if keyword == '':
            mark = 0
            self.search_browser.clear()
            self.search_browser.setText("<h2>输入不能为空!</h2>")
        else:
            try:
                self.search_browser.clear()
                if not list(self.changed_df[self.changed_df[self.search_by[self.value]].str.contains('%s' % str(keyword))][self.search_by[self.value]]):
                    # contains是包含，所以达到了模糊搜索的功能
                    self.search_browser.append("<h2>很抱歉,没有找到相关书籍!</h2>")
                # :10是限制显示搜索条数

                self.book_list = list(self.changed_df[self.changed_df[self.search_by[self.value]].str.contains('{}'.format(keyword))].book_name[:10])
                self.score_list = list(self.changed_df[self.changed_df[self.search_by[self.value]].str.contains('{}'.format(keyword))].score[:10])
                self.rating_num_list = list(self.changed_df[self.changed_df[self.search_by[self.value]].str.contains('{}'.format(keyword))].rating_num[:10])
                self.author_list = list(self.changed_df[self.changed_df[self.search_by[self.value]].str.contains('{}'.format(keyword))].author[:10])
            except Exception as e:
                print(e)

            self.matched_num = len(self.book_list) if len(self.book_list) < 10 else 10

        try:
            for i in range(self.matched_num):
                if mark == 0:
                    break  # 如果空就不搜索
                self.book_name = self.book_list[i]
                self.score = str(self.score_list[i])
                self.rating_num = str(self.rating_num_list[i])
                self.author = self.author_list[i]
                self.content = "<h3>" + "《" + self.book_name + "》" + "  评分:" + self.score + "   评论人数:" + \
                               self.rating_num +"</h3>" + '\n' + "<h3>" + "  作者:" + self.author + "</h3>" + "-"*50
                self.search_browser.append(self.content)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    search = SearchWindow()
    search.show()
    sys.exit(app.exec_())

