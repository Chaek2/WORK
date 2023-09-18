import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(400,600)
        
        ComboBox = QComboBox()
        ComboBox.addItems(["QLCC6/8", "SOT-89"])
        ComboBox.currentIndexChanged.connect( self.index_changed )
        ComboBox.currentTextChanged.connect( self.text_changed )




        self.setCentralWidget(ComboBox)

    #QComboBox "QLCC6/8", "SOT-89"
    def index_changed(self, i):
        print(i)
    def text_changed(self, s):
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()