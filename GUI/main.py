import sys
from GUI.Login import Login
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
demo = Login()
demo.show()
sys.exit(app.exec_())