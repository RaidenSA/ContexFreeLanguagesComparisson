import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import uigram
import cyk
import early

class Connection(QMainWindow, uigram.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        relative_path = self.textbox_file.text()
        self.button_start.clicked.connect(lambda: self.begin())
        self.button_show_grammar.clicked.connect(lambda: self.show_gr(self.textbox_file.text()))
        
        
    def show_gr (self,relative_path):
        global_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_path)
        flag = 0
        try:
            savefile = open(global_path, 'r')
            flag = 1
        except FileNotFoundError:
            try:
                savefile = open(relative_path, 'r')
                flag = 1
            except:
                flag = 0
                error = "\nЭтого файла не существует - " + str(relative_path)
                self.plainText.appendPlainText(error)
                
        if flag:
            grammar = savefile.read()
            self.plainText.appendPlainText('\nТекущая грамматика:\n' + grammar)
            flag = 0
            savefile.close()
        
    
    def begin (self):
        curr_text = self.combo.currentText()
        if (curr_text == 'алгоритм Кока-Янгера-Касами'):
            outstring = cyk.start(self.textbox_word.text(),self.textbox_file.text())
            self.plainText.appendPlainText(outstring)
        else:
            outstring = early.start(self.textbox_word.text(),self.textbox_file.text())
            self.plainText.appendPlainText(outstring)
    
app = QApplication(sys.argv)
form = Connection()
form.show()
app.exec()