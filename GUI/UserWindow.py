import res
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTextBrowser, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from ChangePwd import ChangePwdPage


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
        self.resize(500, 250)

        self.user_label = QLabel(self)
        self.user_label.setText("<h1>您好！" + username + "</h1>")
        self.num_label = QLabel(self)
        self.num_label.setText("<h1>您在豆瓣读过" + str(num) + "本书</h1>")
        self.browser = QTextBrowser(self)
        self.change_pwd_button = QPushButton("修改密码", self)
        self.change_pwd_button.clicked.connect(self.show_change_page)
        self.change_window = ChangePwdPage(username)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.user_label)
        self.v_layout.addWidget(self.num_label)
        self.v_layout.addWidget(self.browser)
        self.v_layout.addWidget(self.change_pwd_button)

        try:
            self.browser.append("<h2>您最近读过的三本书为: </h2>")
            for like_book in like_books[::-1][:3]:
                self.browser.append("<h3>《" + like_book + "》</h3>")
        except Exception as e:
            print(e)

        self.setLayout(self.v_layout)

    def show_change_page(self):
        self.change_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = '阿哲'
    books = []
    book_nums = len(books)
    user_page = UserWindow(user, book_nums, books)
    user_page.show()
    sys.exit(app.exec_())