import numpy as np
import math
import cv2 as cv
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QComboBox, QListWidget,
    QSlider, QWidget,QPushButton,QFileDialog, QGridLayout
)
from PyQt5.QtGui import QPixmap,QImage

Radius = "Повернуть на "
proccess = 0
menu = 0
angle = 0
url = 'photo/test_photo2.jpg'

app = QApplication([])
mainwindow = QMainWindow()
maingrid = QGridLayout()
widget = QWidget()

#Текстовые поля
lab1 = QLabel('Выберите тип')
maingrid.addWidget(lab1,0,0)

lab2 = QLabel('Загрузите фотографию корпуса')
maingrid.addWidget(lab2,1,0)

lab3 = QLabel('Лог процесса...')
maingrid.addWidget(lab3,7,0)

lab4 = QLabel('Результат:')
maingrid.addWidget(lab4,10,0)

lab5 = QLabel(Radius)
maingrid.addWidget(lab5,11,0)

#Кнопки
button1 = QPushButton("Выберить")
maingrid.addWidget(button1,1,1)

button2 = QPushButton("<< Шаг назад")
button2.clicked.connect(Step(-1))
maingrid.addWidget(button2,6,0)

button3 = QPushButton("Шаг вперёд >>")
button3.clicked.connect(Step(1))
maingrid.addWidget(button3,6,1)

#Картинка
lable_image = QLabel()
pixmap_image = QPixmap(url)
pixmap_image = pixmap_image.scaled(400,400)
lable_image.setPixmap(pixmap_image)
maingrid.addWidget(lable_image,2,0,4,2)

#ComboBox
combobox = QComboBox()
combobox.addItem("QLCC6/8")  
combobox.addItem("SOT-89")  
combobox.setCurrentIndex(menu)
maingrid.addWidget(combobox,0,1)
combobox.currentIndexChanged.connect(ComboBox_Chancged())

#ListBox
listbox = QListWidget()
maingrid.addWidget(listbox,8,0,1,2)

widget.setLayout(maingrid)
mainwindow.setCentralWidget(widget)
mainwindow.show()
app.exec()


#функции
def ComboBox_Chancged(i):
    global proccess, listbox, pixmap_image, lable_image
    proccess = i

def Step(i):
    global menu, url
    if i > 0 and menu < 3:
        menu+=1
    if i < 0 and menu > 0:
        menu-=1
    match menu:
        case 0:
            listbox.addItem('file: '+url)  
            pixmap_image = QPixmap(url)
            pixmap_image = pixmap_image.scaled(400,400)
            lable_image.setPixmap(pixmap_image)
            ImageAngleSearch()
        case 1:
            listbox.addItem('Находим объекты')            
            pixmap_image = QPixmap('Push1.jpg')
            pixmap_image = pixmap_image.scaled(400,400)
            lable_image.setPixmap(pixmap_image)
        case 2:
            listbox.addItem('Поворачиваем')        
            pixmap_image = QPixmap('Push2.jpg')
            pixmap_image = pixmap_image.scaled(400,400)
            lable_image.setPixmap(pixmap_image)

def ImageAngleSearch():
    global proccess, url, log, angle
    image_main = cv.imread(url) 
    hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
    h_min = np.array((0, 40, 31), np.uint8)
    h_max = np.array((35, 255, 255), np.uint8)   
    image_first = cv.inRange(hsv, h_min, h_max)

    cnts=[]
    area1 = 0
    area2 = 0

    if proccess == 0:
        area1 = 3000
        area2 = 10000
    else:
        area1 = 2400
        area2 = 45000

    contours = cv.findContours(image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        area = int(rect[1][0]*rect[1][1])
        if area > area1 and area < area2:
            cv.drawContours(image_first,[box],-1,(255,0,255),2)
            cnts.append(box)

    cv.imwrite('Push1.jpg',image_first)

    if proccess == 1:
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
    image_second = RotateImage(image_first)

    cv.imwrite('Push2.jpg',image_second)

def RotateImage(img):
    global angle
    rows,cols = img.shape[:2]
    M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),angle,1)
    img = cv.warpAffine(img,M,(cols,rows))
    return img

def Director():
    global url, menu
    menu = 0

    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilter("Images (*.png *.jpg)")
    dialog.setDirectory('C:\\Users\\Anton\\Desktop\\Working\\WORK\\test')
    if dialog.exec_():
        fileNames = dialog.selectedFiles()
        url = fileNames[0]   
        Step(0)
