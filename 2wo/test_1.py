import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,QVBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,QHBoxLayout,QWidget,QPushButton
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(400,600)
        #QHBoxLayout
        container = QWidget()
        layout = QHBoxLayout(container)

        #QLabel
        Label = QLabel("My")
        # Label.setFixedSize(120,40)

        #QComboBox
        ComboBox = QComboBox()
        ComboBox.addItem("QLCC6/8")  
        ComboBox.addItem("SOT-89")  
        # ComboBox.setFixedSize(120,40)
        ComboBox.currentIndexChanged.connect(self.index_changed)

        #QHBoxLayout
        container1 = QWidget()
        layout1 = QHBoxLayout(container1)
        layout1.addWidget(Label)
        layout1.addWidget(ComboBox)     
        #QHBoxLayout2
        container2 = QWidget()
        layout2 = QHBoxLayout(container2)
        layout2.addWidget(Label)
        layout2.addWidget(ComboBox)      

        layout.addWidget(container1)
        layout.addWidget(container2)
        # layout.addLayout(layout2)

        self.setCentralWidget(container)
        # self.setCentralWidget(container2)

    def index_changed(self, i): # i — это int
        print(i)

app = QApplication(sys.argv)
w = MainWindow()   
w.show()
app.exec()