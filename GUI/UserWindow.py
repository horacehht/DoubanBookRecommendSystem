import res
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTextBrowser, QVBoxLayout
from PyQt5.QtGui import QIcon


class UserWindow(QWidget):
    def __init__(self, username, num, like_books):
        """
        用户的个人主页
        :param username: 用户名，str
        :param num: 喜欢的书籍数共有多少本，int
        :param like_books: 具体的书名，list
        """
        super(UserWindow, self).__init__()
        self.setWindowTitle("个人主页")
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.resize(400, 200)

        self.user_label = QLabel(self)
        self.num_label = QLabel(self)
        self.browser = QTextBrowser(self)

        self.v_layout = QVBoxLayout()

        self.user_label.setText("<h1>您好！" + username + "</h1>")
        self.num_label.setText("<h1>您在豆瓣喜欢" + str(num) + "本书</h1>")
        try:
            self.browser.append("您最近喜欢的三本书为: ")
            for like_book in like_books[:3]:
                self.browser.append("《" + like_book +"》")

            self.v_layout.addWidget(self.user_label)
            self.v_layout.addWidget(self.num_label)
            self.v_layout.addWidget(self.browser)

        except Exception as e:
            print(e)
            self.v_layout.addWidget(self.user_label)
            self.v_layout.addWidget(self.num_label)

        self.setLayout(self.v_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = 'Horace'
    books = ["a", "b", "c", "d", "e"]
    book_nums = len(books)
    user_page = UserWindow(user, book_nums, books)
    user_page.show()
    sys.exit(app.exec_())