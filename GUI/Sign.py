import res
import sys
import pymysql
import json
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from random import randint

class SignWindow(QDialog):
    def __init__(self):
        super().__init__()
        # 数据库操作
        self.conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="doubanbook",  # 数据库名
            charset="utf8"
        )
        self.cur = self.conn.cursor()

        self.setWindowTitle('注册')  # 设置窗口标题
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.user_label = QLabel('用户名:', self)  # 文本设置
        self.pwd_label = QLabel('密码:', self)
        self.for_sure_label = QLabel('确认密码:', self)
        self.user_line = QLineEdit(self)  # 单行文本编辑器
        self.user_line.setPlaceholderText("请输入您的昵称")
        self.pwd_line = QLineEdit(self)
        self.pwd_line.setPlaceholderText("请输入密码")
        self.for_sure_line = QLineEdit(self)
        self.for_sure_line.setPlaceholderText("请二次确认密码")
        self.register_button = QPushButton('注册', self)  # 注册按钮

        self.user_h_layout = QHBoxLayout()  # 水平布局
        self.pwd_h_layout = QHBoxLayout()
        self.for_sure_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()  # 垂直排列小部件

        self.layout_init()
        self.button_init()
        self.editline_init()

    def layout_init(self):
        """布局初始化"""
        # 添加控件
        self.user_h_layout.addWidget(self.user_label)
        self.user_h_layout.addWidget(self.user_line)
        self.pwd_h_layout.addWidget(self.pwd_label)
        self.pwd_h_layout.addWidget(self.pwd_line)
        self.for_sure_h_layout.addWidget(self.for_sure_label)
        self.for_sure_h_layout.addWidget(self.for_sure_line)

        # 嵌套布局
        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.for_sure_h_layout)
        self.all_v_layout.addWidget(self.register_button)

        self.setLayout(self.all_v_layout)

    def button_init(self):
        """按钮初始化及信号槽连接"""
        self.register_button.setEnabled(False)
        self.register_button.clicked.connect(self.check_input)

    def editline_init(self):
        """输入框初始化及信号槽连接"""
        # 不回显密码
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.for_sure_line.setEchoMode(QLineEdit.Password)

        # 输入框文本改变时发出信号，检查是否为空
        self.user_line.textChanged.connect(self.check_line)
        self.pwd_line.textChanged.connect(self.check_line)
        self.for_sure_line.textChanged.connect(self.check_line)

    def check_line(self):
        """检查用户是否输入"""
        if self.user_line.text() and self.pwd_line.text() and self.for_sure_line:
            # 如果都输入了文字，按钮可按
            self.register_button.setEnabled(True)
        else:
            self.register_button.setEnabled(False)

    def check_input(self):
        """检查用户按下注册时的账户密码的输入"""
        if self.pwd_line.text() != self.for_sure_line.text():
            QMessageBox.critical(self, '错误', '两次输入的密码不一致！')
            # 清空输入密码栏
            self.pwd_line.clear()
            self.for_sure_line.clear()
            return
        user_input = self.user_line.text()
        pwd_input = self.pwd_line.text()
        # 在数据库中查询是否有该账号
        sql_f1 = "SELECT * FROM douban_book_users WHERE nickname = '%s'" % user_input
        try:
            self.cur.execute(sql_f1)
            result = self.cur.fetchone()
            if result:
                # 如果存在这个账号
                QMessageBox.critical(self, '通知', '用户名已存在，请更换！')
            else:
                # 如果找不到该用户，就说明还没注册过
                QMessageBox.information(self, '通知', '注册成功！')
                random_id = str(randint(1, 200000))
                # 查询生成的这个id有没有跟原来数据库中的id重复了，没有重复的话就插入，重复的就再生成一次再查，直到没有重复
                sql_f2 = "SELECT * FROM douban_book_users WHERE id = '%s'" % random_id
                while 1:
                    try:
                        self.cur.execute(sql_f2)
                        result = self.cur.fetchone()
                        if result:
                            random_id = str(randint(1, 200000))
                            continue
                        else:
                            break
                    except Exception as e:
                        print(e)
                # 这样id就不是重复的了

                # 将该数据插入数据库
                sql_i = """INSERT INTO douban_book_users(id, nickname, read_num, read_book_and_score, password)
                                VALUES(%s, %s, %s, %s, %s)"""
                read_books = 0  # 新用户读的书默认为0
                book_and_score = dict()  # 新用户没有看过书，生成一个空字典
                read_str = json.dumps(book_and_score, ensure_ascii=False)
                data = (random_id, user_input, read_books, read_str, pwd_input)
                try:
                    # 执行sql语句
                    self.cur.execute(sql_i, data)
                    # 提交执行
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()  # 发生错误则回滚
                # 注册完成
        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

        # 清空三个输入框内的文字
        self.user_line.clear()
        self.pwd_line.clear()
        self.for_sure_line.clear()
