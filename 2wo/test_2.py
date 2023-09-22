
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,QVBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,QHBoxLayout,QWidget,QPushButton
)
from PyQt5.QtGui import QPixmap
log=["1","2","3","4"]
Radius = "Повернуть на 36*"

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(400,600)

        #QVBoxLayout
        mainLayout = QVBoxLayout()

        #Линия 1
        layout1 = QHBoxLayout()
        
        Label1 = QLabel("Выберите тип")
        
        ComboBox1 = QComboBox()
        ComboBox1.addItem("QLCC6/8")  
        ComboBox1.addItem("SOT-89")  
        ComboBox1.currentIndexChanged.connect(self.index_changed)

        layout1.addWidget(Label1)
        layout1.addWidget(ComboBox1)

        widget1 = QWidget()
        widget1.setLayout(layout1)
        mainLayout.addWidget(widget1)

        #Линия 2
        layout2 = QHBoxLayout()
        
        Label2 = QLabel("Загрузите фотографию корпуса")
        
        button2 = QPushButton("Push")
        button2.setCheckable(True)
        button2.clicked.connect(self.PushButton)

        layout2.addWidget(Label2)
        layout2.addWidget(button2)

        widget2 = QWidget()
        widget2.setLayout(layout2)
        mainLayout.addWidget(widget2)

        #3
        Label3 = QLabel()
        image = QPixmap('2wo/test_photo1.jpg')
        image = image.scaled(400,400)
        Label3.setPixmap(image)
        Label3.resize(image.width(),image.height())
        mainLayout.addWidget(Label3)

        #4
        layout4 = QHBoxLayout()
        
        button41 = QPushButton("<< Шаг назад")
        button41.setCheckable(True)
        button41.clicked.connect(self.PushButton)

        button42 = QPushButton("Шаг вперёд >>")
        button42.setCheckable(True)
        button42.clicked.connect(self.PushButton)

        layout4.addWidget(button41)
        layout4.addWidget(button42)

        widget4 = QWidget()
        widget4.setLayout(layout4)
        mainLayout.addWidget(widget4)

        #5
        layout5 = QHBoxLayout()
        
        Label5 = QLabel("Лог процесса...")
    
        layout5.addWidget(Label5)

        widget5 = QWidget()
        widget5.setLayout(layout5)
        mainLayout.addWidget(widget5)

        #6
        global log
        layout6 = QHBoxLayout()

        List6 = QListWidget()
        List6.addItems(log)
        
        layout6.addWidget(List6)

        widget6 = QWidget()
        widget6.setLayout(layout6)
        mainLayout.addWidget(widget6)

        #7
        layout7 = QHBoxLayout()
        
        Label7 = QLabel("Результат:")
    
        layout7.addWidget(Label7)

        widget7 = QWidget()
        widget7.setLayout(layout7)
        mainLayout.addWidget(widget7)

        #8
        layout8 = QHBoxLayout()

        global Radius
        Label8 = QLabel(Radius)
    
        layout8.addWidget(Label8)

        widget8 = QWidget()
        widget8.setLayout(layout8)
        mainLayout.addWidget(widget8)


        widget = QWidget() #Костыль в PyQt6 XD
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    

    def index_changed(self, i):
        print(i)
    def PushButton(self):
        print("Push")

app = QApplication(sys.argv)
w = MainWindow()   
w.show()
app.exec()