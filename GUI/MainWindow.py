import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextBrowser, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QHeaderView
from PyQt5.QtGui import QIcon
from algorithm import Recommend


class MainWindow():
    def __init__(self):
        super.__init__()