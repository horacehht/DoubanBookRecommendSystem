import sys
from Login import Login
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Login()
    demo.show()
    sys.exit(app.exec_())