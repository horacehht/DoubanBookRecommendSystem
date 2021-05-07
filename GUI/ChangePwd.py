import res
import sys
import pymysql
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QApplication


class ChangePwdPage(QDialog):
    def __init__(self, user):
        super(ChangePwdPage, self).__init__()
        self.user = user
        # 数据库操作
        self.conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="doubanbook",  # 数据库名
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        sql_f = "SELECT * FROM douban_book_users WHERE nickname = %s"
        # 获取该用户的真实密码
        try:
            data = self.user
            self.cur.execute(sql_f, data)
            result = self.cur.fetchone()
            self.true_pwd = result[4]

        except Exception as e:
            print(e)

        self.setWindowTitle('更改密码')  # 设置窗口标题
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标

        self.ori_pwd_label = QLabel('原密码:', self)
        self.new_pwd_label = QLabel('新密码', self)
        self.for_sure_label = QLabel('再次确认密码:', self)

        self.ori_pwd_line = QLineEdit(self)
        self.ori_pwd_line.setPlaceholderText("请输入你的原密码")
        self.new_pwd_line = QLineEdit(self)
        self.new_pwd_line.setPlaceholderText("请输入你的新密码")
        self.for_sure_line = QLineEdit(self)
        self.for_sure_line.setPlaceholderText("请再次输入新密码")

        self.change_button = QPushButton('修改', self)  # 更改按钮

        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.button_init()
        self.editline_init()

    def layout_init(self):
        """布局初始化"""
        self.h1_layout.addWidget(self.ori_pwd_label)
        self.h1_layout.addWidget(self.ori_pwd_line)
        self.h2_layout.addWidget(self.new_pwd_label)
        self.h2_layout.addWidget(self.new_pwd_line)
        self.h3_layout.addWidget(self.for_sure_label)
        self.h3_layout.addWidget(self.for_sure_line)

        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.addLayout(self.h3_layout)
        self.v_layout.addWidget(self.change_button)

        self.setLayout(self.v_layout)

    def button_init(self):
        """按钮初始化及信号槽连接"""
        self.change_button.setEnabled(False)
        self.change_button.clicked.connect(self.check_input)

    def editline_init(self):
        """输入框初始化及信号槽连接"""
        self.ori_pwd_line.setEchoMode(QLineEdit.Password)
        self.new_pwd_line.setEchoMode(QLineEdit.Password)
        self.for_sure_line.setEchoMode(QLineEdit.Password)

        self.ori_pwd_line.textChanged.connect(self.check_line)
        self.new_pwd_line.textChanged.connect(self.check_line)
        self.for_sure_line.textChanged.connect(self.check_line)

    def check_line(self):
        """检查用户是否输入"""
        if self.ori_pwd_line.text() and self.new_pwd_line.text() and self.for_sure_line.text():
            self.change_button.setEnabled(True)
        else:
            self.change_button.setEnabled(False)

    def check_input(self):
        """检查用户输入是否符合要求"""
        if not self.true_pwd == self.ori_pwd_line.text():
            # 如果输入的原密码跟真实密码不符
            QMessageBox.critical(self, '通知', '原密码输入错误!')
            self.ori_pwd_line.clear()
        else:
            # 相符的话则要检查新密码和确认密码是否一致
            if not self.new_pwd_line.text() == self.for_sure_line.text():
                QMessageBox.critical(self, '通知', '新密码和确认密码不一致!')
                self.new_pwd_line.clear()
                self.for_sure_line.clear()
            else:
                QMessageBox.information(self, '通知', '更改成功!')
                self.new_pwd = self.new_pwd_line.text()
                sql_update = 'UPDATE douban_book_users SET password = %s WHERE nickname = %s'
                try:
                    data = (self.new_pwd, self.user)
                    self.cur.execute(sql_update, data)
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
                self.ori_pwd_line.clear()
                self.new_pwd_line.clear()
                self.for_sure_line.clear()
                self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user = "阿哲"
    page = ChangePwdPage(user)
    page.show()
    sys.exit(app.exec_())