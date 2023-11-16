from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QInputDialog, QLineEdit, QPushButton, QVBoxLayout, QComboBox
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
        self.btn.clicked.connect(self.Click)

        self.btn1 = QPushButton("Вывести")
        self.btn1.clicked.connect(self.Clicks)

        self.btnl = QPushButton("Свет")
        self.btnl.clicked.connect(self.Click_light)

        self.btns = QPushButton("Настройки")
        self.btns.clicked.connect(self.Click_settings)

        self.btnup = QPushButton("вверх")
        self.btnup.clicked.connect(self.Click_Up)
        self.btndown = QPushButton("вниз")
        self.btndown.clicked.connect(self.Click_Down)
        self.btnleft = QPushButton("влево")
        self.btnleft.clicked.connect(self.Click_Left)
        self.btnright = QPushButton("вправо")
        self.btnright.clicked.connect(self.Click_Right)

        self.grid.addWidget(self.camdown,0,0,3,3)

        self.grid.addWidget(self.labX,2,0)
        self.grid.addWidget(self.labY,2,2)
        self.grid.addWidget(self.txtX,2,1)
        self.grid.addWidget(self.txtY,2,3)

        self.grid.addWidget(self.btn,3,0,1,4)
        self.grid.addWidget(self.btn1,4,0,1,4)
        self.grid.addWidget(self.btnl,5,0,1,4)
        self.grid.addWidget(self.btns,6,0,1,4)


        self.grid.addWidget(self.btnup,2,6)
        self.grid.addWidget(self.btndown,3,6)
        self.grid.addWidget(self.btnleft,3,5)
        self.grid.addWidget(self.btnright,3,7)

        self.setLayout(self.grid)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()   

        self.show()

    def Click(self):
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
            engine.perform("G0 X"+str(centerXY[0])+" Y"+str(centerXY[1]))

    def Clicks(self):
        global centerXY
        try:
            with open("XY.pickle", "rb") as f:
                centerXY = pickle.load(f)
        except:
            pass
        if centerXY is not None:
            self.txtX.setText(str(round(centerXY[0], 2)).replace('.',','))
            self.txtY.setText(str(round(centerXY[1], 2)).replace('.',','))

    def Click_Left(self):
        x = float(self.txtX.text().replace(',','.'))
        x+=0.1
        self.Wolk(x,float(self.txtY.text().replace(',','.')))

    def Click_Right(self):
        x = float(self.txtX.text().replace(',','.'))
        x-=0.1
        self.Wolk(x,float(self.txtY.text().replace(',','.')))

    def Click_Down(self):
        y = float(self.txtY.text().replace(',','.'))
        y-=0.1
        self.Wolk(float(self.txtX.text().replace(',','.')),y)

    def Click_Up(self):
        y = float(self.txtY.text().replace(',','.'))
        y+=0.1
        self.Wolk(float(self.txtX.text().replace(',','.')),y)

    def Wolk(self,x,y):
        self.txtX.setText(str(round(x, 2)).replace('.',','))
        self.txtY.setText(str(round(y, 2)).replace('.',','))
        self.Click()

    def Click_light(self):
        global light
        if not light:
            engine.perform("M804")
            light = True
        elif light:
            engine.perform("M805")
            light = False

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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    sys.exit(app.exec_())

