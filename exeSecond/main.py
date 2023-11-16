from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QInputDialog, QLineEdit, QPushButton
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont, QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from camera_moment import img, img_center

centerXY = []

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        self.change_pixmap_signal.emit(img_center())

class App(QWidget):

   def __init__(self):
      super().__init__()
      self.setWindowTitle('MY')
      self.setFixedSize(500,150)
      self.grid = QGridLayout()

      self.none = QLabel()

      self.image = QLabel()

      self.labX = QLabel('X')
      self.labY = QLabel('Y')
      self.txtX = QLineEdit()
      self.txtY = QLineEdit()
      # self.txtX.textEdited.connect(self.Click)
      # self.txtY.textEdited.connect(self.Click)

      self.btn = QPushButton("Запомнить положение")
      self.btn.clicked.connect(self.Click)

      
      self.grid.addWidget(self.labX,1,0)
      self.grid.addWidget(self.labY,1,2)
      self.grid.addWidget(self.txtX,1,1)
      self.grid.addWidget(self.txtY,1,3)

      self.grid.addWidget(self.btn,2,0,1,4)

      # self.grid.addWidget(self.image,0,4,3,2)

      self.txtX.setValidator(QDoubleValidator())
      self.txtY.setValidator(QDoubleValidator())

      self.grid.addWidget(self.none,2,0)

      self.setLayout(self.grid)

      self.thread = VideoThread()
      self.thread.change_pixmap_signal.connect(self.update_image)
      self.thread.start()

      self.show() 
   
   def Click(self):
      global centerXY
      if len(centerXY) == 0:
         centerXY.append(float(self.txtX.text().replace(',','.')))
         centerXY.append(float(self.txtY.text().replace(',','.')))
      elif len(centerXY) == 2:
         centerXY[0] = float(self.txtX.text().replace(',','.'))
         centerXY[1] = float(self.txtY.text().replace(',','.'))

   @pyqtSlot(np.ndarray)
   def update_image(self, cv_img):
      qt_img = self.convert_cv_qt(cv_img)
      self.image.setPixmap(qt_img)
   
   def convert_cv_qt(self, cv_img):
      rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
      h, w, ch = rgb_image.shape
      bytes_per_line = ch * w
      convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
      p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio)
      return QPixmap.fromImage(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

