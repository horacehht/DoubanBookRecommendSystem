from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox


class SignWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('注册')  # 设置窗口标题
        self.setWindowIcon(QIcon(':res/douban.ico'))  # 设置窗口图标
        self.signup_user_label = QLabel('用户名:', self)  # 文本设置
        self.signup_pwd_label = QLabel('密码:', self)
        self.signup_pwd2_label = QLabel('确认密码:', self)
        self.signup_user_line = QLineEdit(self)  # 单行文本编辑器
        self.signup_pwd_line = QLineEdit(self)
        self.signup_pwd2_line = QLineEdit(self)
        self.signup_button = QPushButton('注册', self)  # 注册按钮

        self.user_h_layout = QHBoxLayout()  # 水平布局
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()  # 垂直排列小部件

        self.layout_init()
        self.lineedit_init()
        self.pushbutton_init()


    def layout_init(self):
        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)
        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)


