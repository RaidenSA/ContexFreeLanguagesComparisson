import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QPlainTextEdit, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication

class Ui_MainWindow(object):

    def setupUi(self, windowMain):
        windowMain.setWindowTitle("Синтаксический анализ КС языков")
        windowMain.setGeometry(100, 100, 1200, 800)
        self.label_string = QLabel(windowMain)
        self.label_string.setText('Входная строка:')
        self.label_string.setFont(QFont("Times", 11, QFont.Bold))
        self.label_string.move(50, 70)
        self.label_string.adjustSize()
        self.textbox_word = QLineEdit(windowMain)
        self.textbox_word.setGeometry(250, 60, 130, 50)
        self.textbox_word.setText("abc")
        self.label_file = QLabel(windowMain)
        self.label_file.setText('Файл для чтения грамматики:')
        self.label_file.setFont(QFont("Times", 11, QFont.Bold))
        self.label_file.move(400, 70)
        self.label_file.adjustSize()
        self.textbox_file = QLineEdit(windowMain)
        self.textbox_file.setGeometry(770, 60, 130, 50)
        self.textbox_file.setText("input.txt")
        self.label_algorithm = QLabel(windowMain)
        self.label_algorithm.setText('Выбор алгоритма:')
        self.label_algorithm.setFont(QFont("Times", 11, QFont.Bold))
        self.label_algorithm.move(50, 150)
        self.label_algorithm.adjustSize()
        self.combo = QComboBox(self)
        self.combo.addItems(["алгоритм Кока-Янгера-Касами", "алгоритм Эрли"])
        self.combo.setGeometry(300, 140, 250, 40)
        self.plainText = QPlainTextEdit(windowMain)
        self.plainText.setGeometry(50, 250, 800, 500)
        self.plainText.setReadOnly(True)
        self.button_start = QPushButton(windowMain)
        self.button_start.setGeometry(1000, 50, 150, 70)
        self.button_start.setText("Начать анализ")
        self.button_show_grammar = QPushButton(windowMain)
        self.button_show_grammar.setGeometry(1000, 150, 180, 70)
        self.button_show_grammar.setText("Показать грамматику")
        self.button_exit = QPushButton(windowMain)
        self.button_exit.setGeometry(1000, 250, 150, 70)
        self.button_exit.setText("Выход")
        self.button_exit.clicked.connect(QCoreApplication.instance().quit)