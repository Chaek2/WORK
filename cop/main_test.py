import numpy as np
import cv2 as cv
from PIL import Image


def Start(fn):

    imgs = cv.imread(fn,0)
    ret,thresh = cv.threshold(imgs,60,255,0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        area = int(rect[1][0]*rect[1][1]) # вычисление площади
        if area > 400:
            
            x_l = []
            y_l = []
            for x,y in box:
                x_l.append(x)
                y_l.append(y)
            
            crop = imgs[min(y_l)-20:max(y_l)+20,min(x_l)-20:max(x_l)+20]

            im = Image.fromarray(crop)
            im.save('crop.jpg') 
            
    cv.destroyAllWindows()


        
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-50.jpg' # имя файла, который будем анализироватьx
fn = 'photo_2023-08-31_17-55-53.jpg' # имя файла, который будем анализировать
Start(fn)