from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2 as cv
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from camera_moment import img_center


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        video=cv.VideoCapture(1)
        hasFrame,frame=video.read()
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
        self.change_pixmap_signal.emit(frame)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.image_label = QLabel(self)
        self.image_label.setText('sss')
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(500, 500, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())