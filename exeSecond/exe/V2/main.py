from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QInputDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont, QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5 import QtGui
import cv2 as cv
import numpy as np
import pandas as pd
import os
import sys
import time
import pickle

class Setting:
    """
    Класс настроек
    """
    def __init__(self):
        self.CAM = -1
        self.COM = 'COM'

pogr = [0,0]
ispogr = False
camera_XY = [0,0]
box_first_XY = [0,0]
light = False
take = False
sets = Setting()
sets.CAM = -1
sets.COM = ""
A = 0

class VideoThread(QThread):
    """
    Класс работы с камерой (потоковая передача)
    """
    change_pixmap_signal = pyqtSignal(QImage)
    def run(self):
        global sets
        if sets.CAM > -1:
            cap = cv.VideoCapture(sets.CAM)
            while 1:
                try:
                    ret, frame = cap.read()
                    cv.imwrite("PR.jpg", frame)
                    time.sleep(0.1)
                    if ret:                
                        gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                        height, width = gray.shape[:2]
                        start_p_v=(0,int(height/2))
                        end_p_v=(width,int(height/2))
                        start_p_h=(int(width/2),0)
                        end_p_h=(int(width/2),height)
                        circ = (int(width/2),int(height/2))

                        cv.line(frame,start_p_v,end_p_v,(0,255,0),2)
                        cv.line(frame,start_p_h,end_p_h,(0,255,0),2)
                        cv.circle(frame,circ,3,(255,0,0),2)

                        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                        h, w, ch = rgb_image.shape
                        bytes_per_line = ch * w
                        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                        p = convert_to_Qt_format.scaled(400, 300, Qt.KeepAspectRatio)
                        self.change_pixmap_signal.emit(p)
                except:
                    pass

class Settings(QWidget):
    """
    Класс окна настроек
    """
#----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        global sets

        #self.ports = serial.tools.list_ports.comports()
        self.setWindowTitle('Настройки')
        self.setFixedSize(400,300)
        self.grid = QVBoxLayout()

        self.cbmcam = QComboBox()
        self.cbmcom = QComboBox()
        
        self.labcam = QLabel('Камера')
        self.labcom = QLabel('COM порт')
        
        self.btn = QPushButton("Дальше")
        self.btn.clicked.connect(self.Save)

        self.grid.addWidget(self.labcam)
        self.grid.addWidget(self.cbmcam)
        self.grid.addWidget(self.labcom)
        self.grid.addWidget(self.cbmcom)
        self.grid.addWidget(self.btn)

        self.setLayout(self.grid)
#--------------------------------try-----------------------------------------------------------------------------
        try:
            with open("exeSecond/exe/V2/ST/SET.pickle", "rb") as f:
                sets = pickle.load(f)
            self.w = App()
            self.close()
        except:
            for port in self.CAMERA_PORT():
                self.cbmcam.addItem(str(port))
            for port in self.ports:
                self.cbmcom.addItem(port.device)
            self.show()
#--------------------------------defs----------------------------------------------------------------------------
    def Save(self):
        """
        Сохранение настроек
        """
        global sets
        if int(self.cbmcam.currentText()) > -1 and self.cbmcom.currentText() != "": 
            sets.CAM = int(self.cbmcam.currentText())
            sets.COM = str(self.cbmcom.currentText())
            with open("exeSecond/exe/V2/ST/SET.pickle", "wb") as f:
                pickle.dump(sets, f, protocol=pickle.HIGHEST_PROTOCOL)
            self.w = App()
            self.close()

    def CAMERA_PORT(self):
        """
        Вывод работающих камер
        """
        is_working = True
        dev_port = 0
        working_ports = []
        available_ports = []
        while is_working:
            camera = cv.VideoCapture(dev_port)
            if not camera.isOpened():
                is_working = False
            else:
                is_reading, img = camera.read()
                w = camera.get(3)
                h = camera.get(4)
                if is_reading:
                    working_ports.append(dev_port)
                else:
                    available_ports.append(dev_port)
            dev_port +=1
        working_ports = working_ports[:-1]
        return working_ports

class App(QWidget):    
    """
    Класс главного окна
    """
#----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()    
        #engine.start(sets.COM)
        self.Perfomence("M809")
        self.Perfomence("M805")    
        self.setWindowTitle('Калибровка НКМЗ')
        self.setFixedSize(900,800)
        self.grid = QVBoxLayout()

        self.g1 = QHBoxLayout()
        self.w1 = QWidget()
        self.w11 = QWidget()
        self.w11_X = QWidget()
        self.w11_Y = QWidget()
        self.w11_Z = QWidget()
        self.w11_S = QWidget()

        self.g11 = QVBoxLayout() #|

        self.g11_X = QHBoxLayout() #-
        self.g11_Y = QHBoxLayout() #-
        self.g11_Z = QHBoxLayout() #-
        self.g11_S = QHBoxLayout() #-

        self.cam = QLabel('')
        self.cam.setFixedSize(400,300)

        self.LX = QLabel('X')
        self.LX.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LX.setFixedSize(40,38)
        
        self.LY = QLabel('Y')
        self.LY.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LY.setFixedSize(40,38)
        
        self.LZ = QLabel('Z')
        self.LZ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LZ.setFixedSize(40,38)

        self.LL = QLabel('') #Свет
        self.LL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LL.setFixedSize(40,38)
        self.LL.setStyleSheet("background-color: black") 

        self.LP = QLabel('') #Насос
        self.LP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LP.setFixedSize(40,38)
        self.LP.setStyleSheet("background-color: black") 

        self.TX = QLineEdit('0,0')
        self.TX.setFixedSize(145,38) 
        self.TY = QLineEdit('0,0')
        self.TY.setFixedSize(145,38)
        self.TZ = QLineEdit('0,0')
        self.TZ.setFixedSize(145,38)

        self.BL = QPushButton("Свет") #Включение/Выключение света
        self.BL.setFixedSize(145,38)
        self.BL.clicked.connect(self.Click_Light)

        self.BP = QPushButton("Насос") #Включение/Выключение света
        self.BP.setFixedSize(145,38)
        self.BP.clicked.connect(self.Click_Pump)

        self.BW = QPushButton("Идти") #G0 XN YN ZN
        self.BW.setFixedSize(230,38)
        self.BW.clicked.connect(self.Click_Wolk)

        self.BSC = QPushButton("Запомнить расположение камеры") #Запомнить расположение камеры
        self.BSC.setFixedSize(230,38)
        self.BSC.clicked.connect(self.Click_Save_Camera)

        self.BSFC = QPushButton("Запомнить расположение\n первой ячейки") #Запомнить расположение первой ячейки        
        self.BSFC.setFixedSize(230,38)
        self.BSFC.clicked.connect(self.Click_Save_Box)

        self.g11_X.addWidget(self.LX)
        self.g11_X.addWidget(self.TX)
        self.g11_X.addWidget(self.BW)
        self.w11_X.setLayout(self.g11_X)
        
        self.g11_Y.addWidget(self.LY)
        self.g11_Y.addWidget(self.TY)
        self.g11_Y.addWidget(self.BSC)
        self.w11_Y.setLayout(self.g11_Y)

        self.g11_Z.addWidget(self.LZ)
        self.g11_Z.addWidget(self.TZ)
        self.g11_Z.addWidget(self.BSFC)
        self.w11_Z.setLayout(self.g11_Z)

        self.g11_S.addWidget(self.LL)
        self.g11_S.addWidget(self.BL)
        self.g11_S.addWidget(self.LP)
        self.g11_S.addWidget(self.BP)
        self.w11_S.setLayout(self.g11_S)
        
        self.g11.addWidget(self.w11_X)
        self.g11.addWidget(self.w11_Y)
        self.g11.addWidget(self.w11_Z)
        self.g11.addWidget(self.w11_S)
        self.w11.setLayout(self.g11)

        self.g1.addWidget(self.cam)
        self.g1.addWidget(self.w11)
        self.w1.setLayout(self.g1)
        self.w1.setFixedSize(900,400)
#----------------------------------------------------------------------------------------------------------------
        self.g2 = QHBoxLayout()
        self.w2 = QWidget()

        self.g21 = QGridLayout()
        self.w21 = QWidget()

        self.g22 = QGridLayout()
        self.w22 = QWidget()

        self.BC = QPushButton("Камера") #Камера
        self.BC.clicked.connect(self.Click_Camera_XY)
        
        self.BS = QPushButton("Настройки") #Настройки
        self.BS.clicked.connect(self.Click_Setting)

        self.BForward = QPushButton("вперёд")
        self.BForward.clicked.connect(self.Click_forward)
        self.BBack = QPushButton("назад")
        self.BBack.clicked.connect(self.Click_Back)
        self.BLeft = QPushButton("влево")
        self.BLeft.clicked.connect(self.Click_Left)
        self.BRight = QPushButton("вправо")
        self.BRight.clicked.connect(self.Click_Right)

        self.BDown = QPushButton("Вниз")
        self.BDown.clicked.connect(self.Click_Down)
        self.BUp = QPushButton("Вверх")
        self.BUp.clicked.connect(self.Click_Up)

        self.BAR = QPushButton("Поворот: направо")
        self.BAR.clicked.connect(self.Click_A_Right)
        self.BAL = QPushButton("Поворот: налево")
        self.BAL.clicked.connect(self.Click_A_Left)
        
        self.g22.addWidget(self.BForward,0,1)
        self.g22.addWidget(self.BLeft,1,0)
        self.g22.addWidget(self.BBack,1,1)
        self.g22.addWidget(self.BRight,1,2)
        self.g22.addWidget(self.BDown,0,0)
        self.g22.addWidget(self.BUp,0,2)

        self.g22.addWidget(self.BAR,0,3)
        self.g22.addWidget(self.BAL,1,3)

        self.g21.addWidget(self.BC,0,0)
        self.g21.addWidget(self.BS,1,0)

        self.w21.setLayout(self.g21)
        self.w22.setLayout(self.g22)
        self.g2.addWidget(self.w21)
        self.g2.addWidget(self.w22)

        self.w2.setLayout(self.g2)
        self.w2.setFixedSize(900,100)
#----------------------------------------------------------------------------------------------------------------
        self.g3 = QVBoxLayout()
        self.w3 = QWidget()
        self.g31 = QGridLayout()
        self.w31 = QWidget()

        
        self.BH = QPushButton("Дом") #Home
        self.BH.clicked.connect(self.Home)

        self.LG = QLabel('Панель')
        self.LG.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LG.setFixedSize(120,38)
        self.LGY = QLabel('Столбец')
        self.LGY.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LGY.setFixedSize(120,38)

        self.LGX = QLabel('Строка')
        self.LGX.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LGX.setFixedSize(120,38)

        self.CG = QComboBox()
        self.CG.setFixedSize(100,38) 
        for i in range(1,3):
            self.CG.addItem(str(i))

        self.CGX = QComboBox()
        self.CGX.setFixedSize(100,38) 
        for i in range(1,11):
            self.CGX.addItem(str(i))
        self.CGY = QComboBox()
        self.CGY.setFixedSize(100,38) 
        for i in range(1,11):
            self.CGY.addItem(str(i))

        self.BG = QPushButton("Взять")
        self.BG.clicked.connect(self.Click_Grid)

        self.BA = QPushButton("Повернуть") #Угол
        self.BA.clicked.connect(self.SearchAngle)

        self.g31.addWidget(self.LG,0,0)
        self.g31.addWidget(self.CG,0,1)
        self.g31.addWidget(self.LGY,0,2)
        self.g31.addWidget(self.CGY,0,3)
        self.g31.addWidget(self.LGX,0,4)
        self.g31.addWidget(self.CGX,0,5)
        self.g31.addWidget(self.BG,0,6)
        self.g31.addWidget(self.BA,1,6)
        self.g31.addWidget(self.BH,2,6)
        

        self.w31.setLayout(self.g31)
        self.g3.addWidget(self.w31)
        self.w3.setLayout(self.g3)

        self.w3.setLayout(self.g3)
        self.w3.setFixedSize(900,200)

        self.grid.addWidget(self.w1)        
        self.grid.addWidget(self.w2)        
        self.grid.addWidget(self.w3)        
        self.setLayout(self.grid)
        
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()   

        self.show()
        
    @pyqtSlot(QImage)
    def update_image(self, cv_img):
        self.cam.setPixmap(QPixmap.fromImage(cv_img))
#--------------------------------defs--Perfomence--Pump--Light--Home---------------------------------------------
    def Perfomence(self, string: str):
        """
        Отправка запроса действий на плату
        """
        #engine.perform(string)

    def Click_Pump(self):
        """
        Включение\Выключение насоса
        """
        global take, A
        if not take:
            #Включить вакум
            self.Perfomence("G0 Z20 A0")
            time.sleep(1)
            self.Perfomence("G0 A0")
            time.sleep(2)
            self.Perfomence("M808")
            self.LP.setStyleSheet("background-color: green")
            take = True
        else:
            #Выключить вакум
            self.Perfomence("G0 Z17")
            time.sleep(2)
            self.Perfomence("G0 A0")
            time.sleep(3)
            self.Perfomence("G0 A"+(str(A))) 
            time.sleep(4)
            self.Perfomence("M809")
            self.LP.setStyleSheet("background-color: black")
            take = False
        time.sleep(1)
        self.Perfomence("G0 Z0 A0") 

    def Home(self):
        """
        Передвижение в начальную точку (0, 0, 0)
        """
        self.Perfomence("G0 X0 Y0 Z0")
        self.TX.setText(str('0,0').replace('.',',').replace(' ',''))
        self.TY.setText(str('0,0').replace('.',',').replace(' ',''))
        self.TZ.setText(str('0,0').replace('.',',').replace(' ',''))
        time.sleep(1)

    def Click_Light(self):
        """
        Включение\Выключение света
        """
        global light
        if not light: 
            #Включить свет
            self.Perfomence("M804")
            self.LL.setStyleSheet("background-color: green")
            light = True
        elif light:
            #Выключить свет
            self.Perfomence("M805")
            self.LL.setStyleSheet("background-color: black")
            light = False
#--------------------------------------Wolk--Setting--Camera_XY--Save_Camera--Save_Box--Grid---------------------
    def Click_Wolk(self):
        """
        Передвижение по координатам
        """
        self.Perfomence("G0 X"+str(float(self.TX.text().replace(',','.').replace(' ','')))+" Y"+
        str(float(self.TY.text().replace(',','.').replace(' ','')))+
        " Z"+str(float(self.TZ.text().replace(',','.').replace(' ',''))))
    
    def Click_Setting(self):
        """
        Удаление настроек
        """
        os.remove("exeSecond/exe/V2/ST/SET.pickle")
        self.thread.disconnect()
        self.w = Settings()
        self.close()

    def Click_Camera_XY(self):
        """
        Передвижение к координатам камеры
        """
        global camera_XY, pogr
        pogr = [0,0]         
        try:
            with open("exeSecond/exe/V2/ST/XYZ.pickle", "rb") as f:
                camera_XY = pickle.load(f)
        except:
            pass
        if camera_XY != [0,0]:   
            self.TX.setText(str(round(camera_XY[0], 1)+0.0).replace('.',',').replace(' ',''))
            self.TY.setText(str(round(camera_XY[1], 1)+0.0).replace('.',',').replace(' ',''))
            self.TZ.setText(str(round(0.0, 1)).replace('.',',').replace(' ',''))
            self.Perfomence("G0 X"+str(round(float(self.TX.text().replace(',','.').replace(' ','')),1))+" Y"+
            str(round(float(self.TY.text().replace(',','.').replace(' ','')),1))+
            " Z0")
            self.Perfomence("G0 A0")

    def Click_Save_Camera(self):
        """
        Сохранение координат камеры
        """
        global camera_XY
        if float(self.TX.text().replace(',','.').replace(' ','')) > -1 and float(self.TY.text().replace(',','.').replace(' ','')) > -1:
            camera_XY[0] = round(float(self.TX.text().replace(',','.').replace(' ','')),1)
            camera_XY[1] = round(float(self.TY.text().replace(',','.').replace(' ','')),1)
            try:
                with open("exeSecond/exe/V2/ST/XYZ.pickle", "wb") as f:
                    pickle.dump(camera_XY, f, protocol=pickle.HIGHEST_PROTOCOL)
            except:
                pass

    def Click_Save_Box(self):
        """
        Сохранение координат первой ячейки
        """
        global box_first_XY
        if float(self.TX.text().replace(',','.').replace(' ','')) > -1 and float(self.TY.text().replace(',','.').replace(' ','')) > -1:
            box_first_XY[0] = float(self.TX.text().replace(',','.').replace(' ',''))
            box_first_XY[1] = float(self.TY.text().replace(',','.').replace(' ',''))  
            try:
                with open("exeSecond/exe/V2/ST/BOX.pickle", "wb") as f:
                    pickle.dump(box_first_XY, f, protocol=pickle.HIGHEST_PROTOCOL)
            except:
                pass 

    def Click_Grid(self):
        """
        Передвижение по ячейкам 2-х таблиц
        """
        global box_first_XY, pogr, ispogr    
        boxY = [[0,6.5,13.1,19.8,26.3,34.2,40.7,47.3,53.9,60.0],
        [79.8,86.3,92.9,99.6,106.1,114.0,120.5,127.1,133.7,139.8]]
        # boxY = [[0,6.7,13.4,20.1,26.8,35,41.7,48.4,55.1,61.8],
        # [79.8,86.3,92.9,99.6,106.1,114.0,120.5,127.1,133.7,139.8]]
        boxX = [0,6.5,13,19.6,25.9,33.9,40.8,47,53.9,59.8]
        try:
            with open("exeSecond/exe/V2/ST/BOX.pickle", "rb") as f:
                box_first_XY = pickle.load(f)
        except:
            pass            
        if box_first_XY != [0,0]: 
            G = int(self.CG.currentText())-1
            X = int(self.CGX.currentText())-1
            Y = int(self.CGY.currentText())-1
            if ispogr:
                XY1 = box_first_XY[0]+boxX[X]+pogr[0]
                XY2 = box_first_XY[1]+boxY[G][Y]+pogr[1]
                ispogr = False
            else:
                XY1 = box_first_XY[0]+boxX[X]
                XY2 = box_first_XY[1]+boxY[G][Y]
            self.TX.setText(str(XY1).replace('.',',').replace(' ',''))
            self.TY.setText(str(XY2).replace('.',',').replace(' ',''))
            self.Perfomence("G0 X"+str(XY1)+" Y"+str(XY2)+"A0")
#-----------------------------------DULRBF-----------------------------------------------------------------------
    def Click_Down(self):
        zd = round(float(self.TZ.text().replace(',','.').replace(' ',''))+0.1,1)
        self.Perfomence("G0 Z"+str(zd))
        self.TZ.setText(str(zd).replace('.',',').replace(' ',''))
    def Click_Up(self):
        if round(float(self.TZ.text().replace(',','.').replace(' ',''))-0.1,1) > 0:
            zu = round(float(self.TZ.text().replace(',','.').replace(' ',''))-0.1,1)
            self.Perfomence("G0 Z"+str(zu))
            self.TZ.setText(str(zu).replace('.',',').replace(' ',''))
    def Click_Left(self):
        xl = round(float(self.TX.text().replace(',','.').replace(' ',''))+0.1,1)
        self.Perfomence("G0 X"+str(xl))
        self.TX.setText(str(xl).replace('.',',').replace(' ',''))
    def Click_Right(self):
        xr = round(float(self.TX.text().replace(',','.').replace(' ',''))-0.1,1)
        self.Perfomence("G0 X"+str(xr))
        self.TX.setText(str(xr).replace('.',',').replace(' ',''))
    def Click_Back(self):
        yb = round(float(self.TY.text().replace(',','.').replace(' ',''))-0.1,1)
        self.Perfomence("G0 Y"+str(yb))
        self.TY.setText(str(yb).replace('.',',').replace(' ',''))
    def Click_forward(self):
        yf = round(float(self.TY.text().replace(',','.').replace(' ',''))+0.1,1)
        self.Perfomence("G0 Y"+str(yf))
        self.TY.setText(str(yf).replace('.',',').replace(' ',''))
#----------------------------------AL--AR--SearchAngle-----------------------------------------------------------
    def Click_A_Left(self):
        """
        Поворот на 1 градус
        """
        global A
        A += 1
        self.Perfomence("G0 A"+(str(A)))
        print(A)
    def Click_A_Right(self):
        """
        Поворот на -1 градус
        """
        global A
        A -=1
        self.Perfomence("G0 A"+(str(A)))
        print(A)

    def SearchAngle(self):
        """
        Поворот по главному выводу
        """
        global A, camera_XY, pogr, ispogr
        self.Perfomence("G0 A0")
        A=0   
        time.sleep(4)
        ispogr = False
        try:
            image_sa = cv.imread("PR.jpg")
            cv.imwrite("exeSecond/exe/V2/PH/PT0.jpg", image_sa) 
            angle = Commands.angleSearch()
            A = angle
            self.Perfomence("G0 A"+(str(A)))
            time.sleep(2)
            image_sc= cv.imread("PR.jpg")
            cv.imwrite("exeSecond/exe/V2/PH/SC0.jpg", image_sc)
            time.sleep(2)
            px,py = Commands.SearchCounter()
            pogr[0] = px
            pogr[1] = py
            ispogr = True
            PX = round(float(self.TX.text().replace(',','.').replace(' ','')),1)+pogr[0]
            PY = round(float(self.TY.text().replace(',','.').replace(' ','')),1)+pogr[1]
            self.Perfomence("G0 X"+str(PX)+" Y"+str(PY))
            print(A)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
