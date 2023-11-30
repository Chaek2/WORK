from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QInputDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont, QPixmap, QImage
import sys
import serial.tools.list_ports
import cv2 as cv
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import pickle
import engine
import os

centerXY = []
light = False
take = False
camera = -1

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    def run(self):
        global camera
        cap = cv.VideoCapture(camera)
        while 1:
            ret, frame = cap.read()
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
                p = convert_to_Qt_format.scaled(500, 500, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Калибровка НКМЗ')
        self.setFixedSize(800,600)
        self.grid = QGridLayout()

        self.camdown = QLabel()

        self.labX = QLabel('X')
        self.labY = QLabel('Y')
        self.txtX = QLineEdit()
        self.txtY = QLineEdit()

        self.btn = QPushButton("Запомнить положение")
        self.btn.clicked.connect(self.Click_Save)

        self.btn1 = QPushButton("Вывести")
        self.btn1.clicked.connect(self.Bring_Out)

        self.btnl = QPushButton("Свет")
        self.btnl.clicked.connect(self.Click_light)

        self.btns = QPushButton("Настройки")
        self.btns.clicked.connect(self.Click_settings)

        self.btnforward = QPushButton("вперёд")
        self.btnforward.clicked.connect(self.Click_forward)
        self.btnback = QPushButton("назад")
        self.btnback.clicked.connect(self.Click_Back)
        self.btnleft = QPushButton("влево")
        self.btnleft.clicked.connect(self.Click_Left)
        self.btnright = QPushButton("вправо")
        self.btnright.clicked.connect(self.Click_Right)

        self.btndown = QPushButton("Вниз")
        self.btndown.clicked.connect(self.Click_Down)
        self.btnup = QPushButton("Вверх")
        self.btnup.clicked.connect(self.Click_Up)
        
        self.btntake = QPushButton("Взять/Отпустить")
        self.btntake.clicked.connect(self.Click_Take)

        
        self.btnAccuracy = QPushButton("Точная настройка")
        self.btnAccuracy.clicked.connect(self.Click_Accuracy)

        self.grid.addWidget(self.camdown,0,5,3,3)

        self.grid.addWidget(self.labX,2,0)
        self.grid.addWidget(self.labY,2,2)
        self.grid.addWidget(self.txtX,2,1)
        self.grid.addWidget(self.txtY,2,3)

        self.grid.addWidget(self.btn,3,0,1,4)
        self.grid.addWidget(self.btn1,4,0,1,4)
        self.grid.addWidget(self.btnl,5,0,1,4)
        self.grid.addWidget(self.btns,6,0,1,4)


        self.grid.addWidget(self.btnforward,2,6)
        self.grid.addWidget(self.btnback,3,6)
        self.grid.addWidget(self.btnleft,3,5)
        self.grid.addWidget(self.btnright,3,7)

        self.grid.addWidget(self.btndown,4,5)
        self.grid.addWidget(self.btntake,4,6)
        self.grid.addWidget(self.btnup,4,7)

        self.grid.addWidget(self.btnAccuracy,5,6)

        self.setLayout(self.grid)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()   

        self.show()

    def Click_Save(self):
        global centerXY
        if len(self.txtX.text())>0 and len(self.txtY.text())>0:
            if len(centerXY) == 0:
                centerXY.append(float(self.txtX.text().replace(',','.')))
                centerXY.append(float(self.txtY.text().replace(',','.')))
            elif len(centerXY) == 2:
                centerXY[0] = float(self.txtX.text().replace(',','.'))
                centerXY[1] = float(self.txtY.text().replace(',','.'))
            try:
                with open("XY.pickle", "wb") as f:
                    pickle.dump(centerXY, f, protocol=pickle.HIGHEST_PROTOCOL)
            except:
                pass
            self.Perfomence("G0 X"+str(centerXY[0])+" Y"+str(centerXY[1])+" Z0")

    def Bring_Out(self):
        global centerXY
        try:
            with open("XY.pickle", "rb") as f:
                centerXY = pickle.load(f)
        except:
            pass
        if centerXY is not None:
            self.txtX.setText(str(round(centerXY[0], 1)).replace('.',','))
            self.txtY.setText(str(round(centerXY[1], 1)).replace('.',','))

    def Click_Down(self):
        #Приблизить
        self.Perfomence("G0 Z18")
    def Click_Up(self):
        #Отдалить
        self.Perfomence("G0 Z0")

    def Perfomence(self, string: str):
        engine.perform(string)

    def Click_Take(self):
        global take
        if not take:
            #Включить вакум
            self.Perfomence("M808")
            take = True
        else:
            #Выключить вакум
            self.Perfomence("M809")
            take = False

    def Click_Left(self):
        x = float(self.txtX.text().replace(',','.'))
        x+=0.1
        self.txtX.setText(str(round(x, 1)).replace('.',','))
        self.Click_Save()
    def Click_Right(self):
        x = float(self.txtX.text().replace(',','.'))
        x-=0.1
        self.txtX.setText(str(round(x, 1)).replace('.',','))
        self.Click_Save()
    def Click_Back(self):
        y = float(self.txtY.text().replace(',','.'))
        y-=0.1
        self.txtY.setText(str(round(y, 1)).replace('.',','))
        self.Click_Save()
    def Click_forward(self):
        y = float(self.txtY.text().replace(',','.'))
        y+=0.1
        self.txtY.setText(str(round(y, 1)).replace('.',','))
        self.Click_Save()

    def Click_light(self):
        global light
        if not light: 
            #Включить свет
            self.Perfomence("M804")
            light = True
        elif light:
            #Выключить свет
            self.Perfomence("M805")
            light = False

    def Click_Accuracy(self):
        self.w = Accuracy()

    def Click_settings(self):
        os.remove("sets.pickle")
        quit()

    @pyqtSlot(QImage)
    def update_image(self, cv_img):
        self.camdown.setPixmap(QPixmap.fromImage(cv_img))

class Setting:
    camera_lower = -1
    com_port='COM'

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        global camera
        self.ports = serial.tools.list_ports.comports()
        self.setWindowTitle('Настройки')
        self.setFixedSize(400,300)
        self.grid = QVBoxLayout()

        self.cbmcam = QComboBox()
        self.cbmcom = QComboBox()

        for port in self.CAMERA_PORT():
            self.cbmcam.addItem(str(port))

        for port in self.ports:
            self.cbmcom.addItem(port.device)
        

        self.labcam = QLabel('Камера')
        self.labcom = QLabel('COM порт')

        self.txtcam = QLineEdit()
        
        self.btn = QPushButton("Дальше")
        self.btn.clicked.connect(self.Save)

        self.grid.addWidget(self.labcam)
        self.grid.addWidget(self.cbmcam)
        self.grid.addWidget(self.labcom)
        self.grid.addWidget(self.cbmcom)
        self.grid.addWidget(self.btn)

        self.setLayout(self.grid)
        self.show()
        try:
            sets = Setting()
            with open("sets.pickle", "rb") as f:
                sets = pickle.load(f)
            if sets is not None:
                engine.start(sets.com_port)
                camera = sets.camera_lower
                self.w = App()
                self.hide()
        except:
            pass

    def Save(self):
        global camera
        sets = Setting()
        sets.camera_lower = int(self.cbmcam.currentText())
        sets.com_port = str(self.cbmcom.currentText())
        with open("sets.pickle", "wb") as f:
            pickle.dump(sets, f, protocol=pickle.HIGHEST_PROTOCOL)
        engine.start(sets.com_port)
        camera = sets.camera_lower
        self.w = App()
        self.hide()

    def CAMERA_PORT(self):
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
        
class Accuracy(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Точная настройка')
        self.grid = QVBoxLayout()

        self.X = QHBoxLayout()
        self.Y = QHBoxLayout()
        self.Z = QHBoxLayout()

        self.lX = QLabel('X')
        self.lY = QLabel('Y')
        self.lZ = QLabel('Y')

        self.tX = QLineEdit()
        self.tY = QLineEdit()
        self.tZ = QLineEdit()

        self.bX = QPushButton("X")
        self.bX.clicked.connect(self.CX)

        self.bY = QPushButton("Y")
        self.bY.clicked.connect(self.CY)

        self.bZ = QPushButton("Z")
        self.bZ.clicked.connect(self.CZ)


        self.X.addWidget(self.lX)
        self.X.addWidget(self.tX)
        self.X.addWidget(self.bX)

        self.Y.addWidget(self.lY)
        self.Y.addWidget(self.tY)
        self.Y.addWidget(self.bY)

        self.Z.addWidget(self.lZ)
        self.Z.addWidget(self.tZ)
        self.Z.addWidget(self.bZ)


        self.XW = QWidget()
        self.XW.setLayout(self.X)
        self.YW = QWidget()
        self.YW.setLayout(self.Y)
        self.ZW = QWidget()
        self.ZW.setLayout(self.Z)
        self.grid.addWidget(self.XW)
        self.grid.addWidget(self.YW)
        self.grid.addWidget(self.ZW)

        self.setLayout(self.grid)
        self.show()

    def CX(self):
        engine.perform("G0 X"+self.tX.text().replace(',','.'))
    
    def CY(self):
        engine.perform("G0 Y"+self.tY.text().replace(',','.'))

    def CZ(self):
        engine.perform("G0 Z"+self.tZ.text().replace(',','.'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    sys.exit(app.exec_())


