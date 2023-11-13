from PyQt5.QtWidgets import QApplication, QMainWindow

import sys



def aplication():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle('test')
    window.setGeometry(700,300,200,200)    
    window.setToolTip('str')

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    aplication()
