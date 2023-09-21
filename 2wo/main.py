import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,QVBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,QHBoxLayout,QWidget,QPushButton,QFileDialog
)
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(400,600)
        
        
        self.label1 = QLabel("Выберите тип")
        
        self.combobox1 = QComboBox()
        self.combobox1.addItem("QLCC6/8")  
        self.combobox1.addItem("SOT-89")  
        # self.combobox1.currentIndexChanged.connect(self.index_changed)




    #QComboBox "QLCC6/8", "SOT-89"
    def index_changed(self, i):
        print(i)
    def text_changed(self, s):
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()