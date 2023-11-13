from PIL import Image
import numpy as np
import math
import cv2 as cv
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QComboBox,
    QListWidget,
    QWidget,
    QPushButton,
    QFileDialog,
    QGridLayout,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap

Radius = "Повернуть на "
proccess = 0
menu = 0
angle = 0
url = ""

app = QApplication([])
log = QListWidget()


class MainWindow(QMainWindow):
    lab5 = QLabel(Radius)
    listbox = log
    lable_image = QLabel()
    pixmap_image = QPixmap(url)
    maingrid = QGridLayout()
    wid = QWidget()

    def __init__(self):
        super(MainWindow, self).__init__()
        global Radius, proccess, menu, angle, url, log, s
        self.setWindowTitle("My App")

        # Текстовые поля
        lab1 = QLabel("Выберите тип")
        self.maingrid.addWidget(lab1, 0, 0)
        lab2 = QLabel("Загрузите фотографию корпуса")
        self.maingrid.addWidget(lab2, 1, 0)
        lab3 = QLabel("Лог процесса...")
        self.maingrid.addWidget(lab3, 7, 0)
        lab4 = QLabel("Результат:")
        self.maingrid.addWidget(lab4, 10, 0)
        lab5 = QLabel(Radius)
        self.maingrid.addWidget(lab5, 11, 0)

        # Кнопки
        button1 = QPushButton("Выберить")
        button1.clicked.connect(self.Director)
        self.maingrid.addWidget(button1, 1, 1)
        button2 = QPushButton("<< Шаг назад")
        button2.clicked.connect(self.Back)
        self.maingrid.addWidget(button2, 6, 0)
        button3 = QPushButton("Шаг вперёд >>")
        button3.clicked.connect(self.Forward)
        self.maingrid.addWidget(button3, 6, 1)

        # Картинка
        lable_image = QLabel()
        pixmap_image = QPixmap("")
        # pixmap_image = pixmap_image.scaled(400, 300)
        lable_image.setPixmap(pixmap_image)
        # lable_image.setFixedSize(400,300)
        self.maingrid.addWidget(lable_image, 2, 0, 2, 2)

        # ComboBox
        combobox = QComboBox()
        combobox.addItem("QLCC6/8")
        combobox.addItem("SOT-89")
        combobox.setCurrentIndex(menu)
        combobox.currentIndexChanged.connect(self.ComboBox_Chancged)
        self.maingrid.addWidget(combobox, 0, 1)

        # ListBox
        listbox = log
        self.maingrid.addWidget(listbox, 8, 0, 1, 2)

        self.wid.setLayout(self.maingrid)
        # self.setLayout(self.maingrid)
        self.setCentralWidget(self.wid)
        # self.saveState(1)
#807
    # функции
    def Back(self):
        self.Step(-1)

    def Forward(self):
        self.Step(1)

    def ComboBox_Chancged(self, i):
        global proccess
        proccess = i

    def Step(self, i: int):
        global menu, url, log, angle
        if i > 0 and menu < 2:
            menu += 1
        if i < 0 and menu > 0:
            menu -= 1
        match menu:
            case 0:
                log.addItem("file: " + url)
                self.listbox = log
                with Image.open(url) as img1:
                    img1.load()
                x,y = img1.size
                box = (x/2-200,y/2-200,x/2+200,y/2+200)
                imgs = img1.crop(box)
                imgs.save('Push0.jpg')
                self.pixmap_image = QPixmap("Push0.jpg")
                # self.pixmap_image = self.pixmap_image.scaled(400, 300)
                self.lable_image.setPixmap(self.pixmap_image)
                # self.lable_image.setFixedSize(400,300)
                self.maingrid.addWidget(self.lable_image, 2, 0, 2, 2)
                self.ImageAngleSearch()
            case 1:
                log.addItem("Находим объекты")
                self.listbox = log
                self.pixmap_image = QPixmap("Push1.jpg")
                self.lable_image.setPixmap(self.pixmap_image)
                # self.lable_image.setFixedSize(400,300)
                self.maingrid.addWidget(self.lable_image, 2, 0, 2, 2)
            case 2:
                self.maingrid.removeWidget(self.lab5)
                log.addItem("Поворачиваем")
                self.listbox = log
                self.pixmap_image = QPixmap("Push2.jpg")
                self.lable_image.setPixmap(self.pixmap_image)
                # self.lable_image.setFixedSize(400, 300)
                self.maingrid.addWidget(self.lable_image, 2, 0, 2, 2)
                self.lab5 = QLabel(Radius + str(angle))
                self.maingrid.addWidget(self.lab5, 11, 0)
        self.update()

    def ImageAngleSearch(self):
        global proccess, url, log, angle
        image_main = cv.imread("Push0.jpg")
        hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        image_first = cv.inRange(hsv, h_min, h_max)

        cnts = []
        area1 = 0
        area2 = 0

        if proccess == 0:
            area1 = 6666
            area2 = 20000
        else:
            area1 = 2000
            area2 = 10000

        contours = cv.findContours(
            image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
        )[0]
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0] * rect[1][1])
            if area > area1 and area < area2:
                cv.drawContours(image_main, [box], -1, (0, 255, 0), 3, cv.LINE_AA)
                cnts.append(box)

        cv.imwrite("Push1.jpg", image_main)  

        cnts1 = cnts[0]

        t1 = 0
        t2 = 0

        if math.sqrt(
            (cnts1[0][0] - cnts1[1][0]) ** 2 + (cnts1[0][1] - cnts1[1][1]) ** 2
        ) > math.sqrt(
            (cnts1[0][0] - cnts1[3][0]) ** 2 + (cnts1[0][1] - cnts1[3][1]) ** 2
        ):
            # #неч
            t1 = [cnts1[0][0], cnts1[3][1]]
            t2 = [cnts1[3][0], cnts1[0][1]]
        else:
            # ч
            t1 = [cnts1[0][0], cnts1[1][1]]
            t2 = [cnts1[1][0], cnts1[0][1]]
        angle = math.degrees(math.atan((t1[1] - t2[1]) / (t2[0] - t1[0])))
        
        image_second = self.RotateImage(image_main, None)
        
        cv.imwrite("Push2.jpg", image_second)
        
        self.Rotate180()

    def Rotate180(self):
        print(180)
        global proccess, url, log, angle
        image_main = cv.imread("Push2.jpg")
        hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        image_first = cv.inRange(hsv, h_min, h_max)

        cnts = []
        area1 = 0
        area2 = 0

        if proccess == 0:
            area1 = 6666
            area2 = 20000
        else:
            area1 = 2000
            area2 = 10000

        contours = cv.findContours(
            image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
        )[0]
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0] * rect[1][1])
            if area > area1 and area < area2:
                # cv.drawContours(image_main, [box], -1, (0, 255, 0), 3, cv.LINE_AA)
                cnts.append(box)
                
        cnts1 = cnts[0]
        # cv.circle(image_main,(cnts1[0][0],cnts1[0][1]),2,(0,0,255),-1)
        # cv.circle(image_main,(cnts1[2][0],cnts1[2][1]),2,(0,0,255),-1)
        
        x, y = image_main.shape[:2]
        xs = y/2-cnts1[0][1]
        ys = y/2-cnts1[2][1]
            
        xt = 0
        if xs > 0:
            if abs(xs) > abs(ys):
                xt = xs
            else:
                xt = ys
        else:
            if abs(xs) < abs(ys):
                xt = xs
            else:
                xt = ys
        if xt < 0:
            image_main = self.RotateImage(image_main, 180)
            if(angle > 0):
                angle +=180
            else:
                angle-=180   
            cv.imwrite("Push2.jpg", image_main)
        
        
    def RotateImage(self, img, ang):
        global angle
        if ang is None:
            rows, cols = img.shape[:2]
            M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
            img = cv.warpAffine(img, M, (cols, rows))
        else:
            rows, cols = img.shape[:2]
            M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), ang, 1)
            img = cv.warpAffine(img, M, (cols, rows))
        return img

    def Director(self):
        global url, menu
        menu = 0

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setDirectory("C:\\")
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            url = fileNames[0]
            with Image.open(url) as img1:
                img1.load()
            x,y = img1.size
            box = (x/2-400,y/2-300,x/2+400,y/2+300)
            imgs = img1.crop(box)
            imgs.save('Push0.jpg')
            self.Step(0)


mainwindow = MainWindow()
mainwindow.show()
app.exec()
