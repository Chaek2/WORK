
import numpy as np
import math
import cv2 as cv
import sys
from PIL import Image
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,QVBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,QHBoxLayout,QWidget,QPushButton,QFileDialog
)
from PyQt5.QtGui import QPixmap,QImage

log=[]
Radius = "Повернуть на "
menu = 1
processtype = 1
angle = None
url = '2wo\\test_photo1.jpg'

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(400,600)

        #QVBoxLayout
        self.mainLayout = QVBoxLayout()

        #Линия 1
        global menu
        self.layout1 = QHBoxLayout()
        self.Label1 = QLabel("Выберите тип")
        self.ComboBox1 = QComboBox()
        self.ComboBox1.addItem("QLCC6/8")  
        self.ComboBox1.addItem("SOT-89")  
        self.ComboBox1.setCurrentIndex(menu)
        self.ComboBox1.currentIndexChanged.connect(self.index_changed)
        self.layout1.addWidget(self.Label1)
        self.layout1.addWidget(self.ComboBox1)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.layout1)
        self.mainLayout.addWidget(self.widget1)

        #Линия 2
        self.layout2 = QHBoxLayout()
        self.Label2 = QLabel("Загрузите фотографию корпуса")
        self.button2 = QPushButton("Push")
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.FindImage)
        self.layout2.addWidget(self.Label2)
        self.layout2.addWidget(self.button2)
        widget2 = QWidget()
        widget2.setLayout(self.layout2)
        self.mainLayout.addWidget(widget2)

        #3
        self.Label3 = QLabel()
        self.image = QPixmap(url)
        self.image = self.image.scaled(400,320)
        self.Label3.setPixmap(self.image)
        self.Label3.resize(self.image.width(),self.image.height())
        self.mainLayout.addWidget(self.Label3)

        #4
        self.layout4 = QHBoxLayout()
        self.button41 = QPushButton("<< Шаг назад")
        self.button41.setCheckable(True)
        self.button41.clicked.connect(self.StepBack)
        self.button42 = QPushButton("Шаг вперёд >>")
        self.button42.setCheckable(True)
        self.button42.clicked.connect(self.StepForward)
        self.layout4.addWidget(self.button41)
        self.layout4.addWidget(self.button42)
        self.widget4 = QWidget()
        self.widget4.setLayout(self.layout4)
        self.mainLayout.addWidget(self.widget4)

        #5
        self.layout5 = QHBoxLayout()
        self.Label5 = QLabel("Лог процесса...")
        self.layout5.addWidget(self.Label5)
        self.widget5 = QWidget()
        self.widget5.setLayout(self.layout5)
        self.mainLayout.addWidget(self.widget5)

        #6
        global log
        self.layout6 = QHBoxLayout()
        self.List6 = QListWidget()
        self.List6.addItems(log)
        self.layout6.addWidget(self.List6)
        self.widget6 = QWidget()
        self.widget6.setLayout(self.layout6)
        self.mainLayout.addWidget(self.widget6)

        #7
        self.layout7 = QHBoxLayout()
        self.Label7 = QLabel("Результат:")
        self.layout7.addWidget(self.Label7)
        self.widget7 = QWidget()
        self.widget7.setLayout(self.layout7)
        self.mainLayout.addWidget(self.widget7)

        #8
        global Radius
        self.layout8 = QHBoxLayout()
        self.Label8 = QLabel(Radius)
        self.layout8.addWidget(self.Label8)
        self.widget8 = QWidget()
        self.widget8.setLayout(self.layout8)
        self.mainLayout.addWidget(self.widget8)

        #end
        self.widget = QWidget() #Костыль в PyQt6 XD
        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)

    

    def index_changed(self, i):
        global processtype, menu
        menu = 0
        processtype = i
        self.image = QPixmap(url)
        self.SetImage()
    def StepBack(self):
        global menu,url, angle
        if menu > 0:
            menu-=1
            match menu:
                case 0:
                    angle = None
                    self.image = QPixmap(url)
                    self.SetImage()
                case 1:
                    angle = None
                    self.ImageBlack()
                case 2:
                    angle = None
                    self.CounterImage()
        print('Back')
    def StepForward(self):
        global menu, url
        if menu < 3:
            menu+=1
            match menu:
                case 1:
                    angle = None
                    log.append('Убираем лишнее')
                    self.ImageBlack()
                case 2:
                    angle = None
                    log.append('Рисуем контуры')
                    self.CounterImage()
                case 3:
                    log.append('Поворачиваем изображение')
                    self.RotateImage()
                
        print('Forward')
    def FindImage(self):
        global url, menu, log
        menu = 0
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setDirectory('C:\\Users\\Anton\\Desktop\\Working\\WORK\\2wo')
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            url = fileNames[0]
            self.image = QPixmap(url)
            self.SetImage()
    def ImageBlack(self):
        global log
        imgs = cv.imread(url)    
        hsv = cv.cvtColor(imgs, cv.COLOR_BGR2HSV)
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        img = cv.inRange(hsv, h_min, h_max)
        im = Image.fromarray(img)
        im.save('bro1.jpg') 
        self.image = QPixmap('bro1.jpg')
        self.SetImage()
    def CounterImage(self):
        global processtype,url, log
        area1 = 0
        area2 = 0
        imgs = cv.imread(url)
        hsv = cv.cvtColor(imgs, cv.COLOR_BGR2HSV)
        if processtype == 0:
            area1 = 3000
            area2 = 10000
        else:
            area1 = 2400
            area2 = 45000
        h_min = np.array((0, 42, 39), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        thresh = cv.inRange(hsv, h_min, h_max)
        contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
        if len(contours) > 0:
            for cnt in contours:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                area = int(rect[1][0]*rect[1][1])
                if area > area1 and area < area2:
                    cv.drawContours(imgs,[box],-1,(255,0,255),2)
        im = Image.fromarray(imgs)
        im.save('bro2.jpg') 
        self.image = QPixmap('bro2.jpg')
        self.SetImage()
    
    def RotateImage(self):
        global processtype,url, log, angle
        imgs = cv.imread('bro2.jpg')
        self.AngleRotate()
        imgs = self.SimpleWay(imgs,angle)
        im = Image.fromarray(imgs)
        im.save('bro3.jpg') 
        self.image = QPixmap('bro3.jpg')
        self.SetImage()

    def SimpleWay(self,rotateImage, angle):
        imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]
        centreY, centreX = imgHeight//2, imgWidth//2
        rotationMatrix = cv.getRotationMatrix2D((centreY, centreX), angle, 1.0)
        rotatingimage = cv.warpAffine(
            rotateImage, rotationMatrix, (imgWidth, imgHeight))
        return rotatingimage
    
    def SetImage(self):
        global url, log, angle, Radius
        self.Label3.close()
        self.widget6.close()
        self.widget8.close()
        
        self.Label3 = QLabel()
        self.image = self.image.scaled(400,320)
        self.Label3.setPixmap(self.image)
        self.Label3.resize(self.image.width(),self.image.height())

        self.mainLayout.removeWidget(self.Label3)
        self.mainLayout.removeWidget(self.widget4)
        self.mainLayout.removeWidget(self.widget5)
        self.mainLayout.removeWidget(self.widget6)
        self.mainLayout.removeWidget(self.widget6)
        self.mainLayout.removeWidget(self.widget7)
        self.mainLayout.removeWidget(self.widget8)

        self.mainLayout.addWidget(self.Label3)
        self.mainLayout.addWidget(self.widget4)
        self.mainLayout.addWidget(self.widget5)
        
        self.layout6 = QHBoxLayout()
        self.List6 = QListWidget()
        self.List6.addItems(log)
        self.layout6.addWidget(self.List6)
        self.widget6 = QWidget()
        self.widget6.setLayout(self.layout6)
        self.mainLayout.addWidget(self.widget6)

        self.mainLayout.addWidget(self.widget7)
        self.layout8 = QHBoxLayout()
        if angle is None:
            self.Label8 = QLabel(Radius)
        else:
            self.Label8 = QLabel(Radius+str(angle))
        self.layout8.addWidget(self.Label8)
        self.widget8 = QWidget()
        self.widget8.setLayout(self.layout8)
        self.mainLayout.addWidget(self.widget8)
            
        self.update()
    
    def AngleRotate(self):
        global processtype, angle
        area1 = 0
        area2 = 0
        im = cv.imread('bro2.jpg')
        hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
        if processtype == 0:
            area1 = 3000
            area2 = 10000
        else:
            area1 = 2400
            area2 = 10000
        hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV )
        cnts=[]
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        thresh = cv.inRange(hsv, h_min, h_max)
        contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0]*rect[1][1])
            if area > area1 and area < area2:
                cnts.append(box)
        cnts1=cnts[0]
        
        t1 = 0
        t2 = 0 

        if math.sqrt((cnts1[0][0]-cnts1[1][0])**2+(cnts1[0][1]-cnts1[1][1])**2) > math.sqrt((cnts1[0][0]-cnts1[3][0])**2+(cnts1[0][1]-cnts1[3][1])**2):
            # #неч
            t1 = [cnts1[0][0],cnts1[3][1]]
            t2 = [cnts1[3][0],cnts1[0][1]]
        else:
            #ч 
            t1 = [cnts1[0][0],cnts1[1][1]]
            t2 = [cnts1[1][0],cnts1[0][1]]
        angle = math.degrees(math.atan((t1[1]-t2[1])/(t2[0]-t1[0])))
        

app = QApplication(sys.argv)
w = MainWindow()   
w.show()
app.exec()