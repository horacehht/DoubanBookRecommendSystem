import sys
from GUI.Login import Login
from SearchWindow import SearchWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
demo = Login()
demo.show()
sys.exit(app.exec_())