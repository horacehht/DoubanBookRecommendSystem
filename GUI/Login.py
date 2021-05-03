import res  # 导入资源文件
import sys
import pymysql
from Sign import SignWindow
from MainWindow import MainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton, \
    QGridLayout, QApplication, QMessageBox


class Login(QWidget):
    def __init__(self):
        super().__init__()
        # 数据库操作
        self.account_presence = False  # 账号是否存在的状态量
        self.conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="doubanbook",  # 数据库名
            charset="utf8"
        )
        self.cur = self.conn.cursor()

        # 界面设置
        self.resize(400, 200)  # 窗口尺寸
        self.setWindowTitle('豆瓣书籍推荐系统')  # 设置窗口标题
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.user_label = QLabel('用户名:', self)  # 文本设置
        self.pwd_label = QLabel('密码:', self)
        self.user_line = QLineEdit(self)  # 单行文本编辑器
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('登录', self)  # 按钮
        self.signin_button = QPushButton('注册', self)

        # 布局实例化
        self.g_layout = QGridLayout()  # 网格布局
        self.h_layout = QHBoxLayout()  # 水平布局
        self.v_layout = QVBoxLayout()  # 垂直布局

        self.layout_init()
        self.button_init()
        self.editline_init()
        self.sign_up_window = SignWindow()

    def layout_init(self):
        """布局设置，目的是使init方法看起来简洁"""
        # 加入控件
        self.g_layout.addWidget(self.user_label, 0, 0, 2, 1)
        self.g_layout.addWidget(self.user_line, 0, 1, 2, 1)
        self.g_layout.addWidget(self.pwd_label, 1, 0, 2, 1)
        self.g_layout.addWidget(self.pwd_line, 1, 1, 2, 1)

        self.h_layout.addWidget(self.login_button)  # 添加登录按钮
        self.h_layout.addWidget(self.signin_button)  # 添加注册按钮

        self.v_layout.addLayout(self.g_layout)  # 将布局添加到框的末尾
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def button_init(self):
        """按钮状态的初始化及信号槽连接"""
        # 按钮状态设置
        self.login_button.setEnabled(False)  # 登入状态初始不可点击
        self.signin_button.setEnabled(True)  # 注册可以点击
        # 槽函数连接
        self.login_button.clicked.connect(self.log_in)
        self.signin_button.clicked.connect(self.sign_up_page)


    def editline_init(self):
        """文本输入框初始化及信号槽连接"""
        # setPlaceholderText是占位文字，无文字时显示
        self.user_line.setPlaceholderText('请输入用户名')  # 在输入框显示浅灰色的提示文本
        self.pwd_line.setPlaceholderText('请输入密码')
        self.pwd_line.setEchoMode(QLineEdit.Password)  # 不回显密码

        # 文本更改时发出信号
        self.user_line.textChanged.connect(self.check_line)
        self.pwd_line.textChanged.connect(self.check_line)

    def check_line(self):
        """检查用户是否输入"""
        if self.user_line.text() and self.pwd_line.text():
            # 用户输入了账户密码
            self.login_button.setEnabled(True)
        else:
            # 不满足其一
            self.login_button.setEnabled(False)

    def log_in(self):
        """登录函数"""
        # 在数据库中查询有无此账号
        user = self.user_line.text()
        pwd = self.pwd_line.text()
        sql = "SELECT * FROM USERINFO WHERE username = %s" % user
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            if results:
                # 有该账号
                self.account_presence = True
            else:
                self.account_presence = False
        except Exception as e:
            # print(e)
            pass
        # 有
        if self.account_present:
            QMessageBox.information(self, '通知', '成功登录!')
            self.close() # 关闭注册界面
            self.MainWindow = MainWindow(self.user_line.text())
            self.MainWindow.show()
        # 无账号则提示需要注册
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("提示")
            msg_box.setText("系统中无此账号！您需要注册")
            msg_box.addButton('好的', QMessageBox.AcceptRole)
            msg_box.exec_()

    def sign_up_page(self):
        """跳出注册界面"""
        self.sign_up_window.exec_()
