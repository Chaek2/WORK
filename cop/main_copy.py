import numpy as np
import cv2 as cv
from PIL import Image


cv.namedWindow("Display window", cv.WINDOW_NORMAL)
cv.resizeWindow("Display window", 500, 500)

cv.namedWindow("Display", cv.WINDOW_NORMAL)
cv.resizeWindow("Display", 500, 500)

# cv.namedWindow("out", cv.WINDOW_NORMAL)
# cv.resizeWindow("out", 500, 500)

# hsv_min = np.array((0, 54, 5), np.uint8)
# hsv_max = np.array((187, 255, 253), np.uint8)

# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-50.jpg' # имя файла, который будем анализироватьx
fn = 'photo_2023-08-31_17-55-53.jpg' # имя файла, который будем анализировать

img = cv.imread(fn,0)

ret,thresh = cv.threshold(img,60,255,0)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV 132
# thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
# contours0, hierarchy = cv.findContours( thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)

# перебираем все найденные контуры в цикле
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
        
        crop = img[min(y_l)-20:max(y_l)+20,min(x_l)-20:max(x_l)+20]

        im = Image.fromarray(crop)
        im.save('crop.jpg') 
        
        
        cv.drawContours(img,[box],-1,(255,0,0),2)
        # out = cv.addWeighted( crop, 1, crop, 0, -60)
        # print(type(out))
        # im = Image.fromarray(out)
        # im.save('out.jpg') 

        

cv.imshow('Display window', img) # вывод обработанного кадра в окно

cv.imshow('Display', crop) # вывод обработанного кадра в окно

# cv.imshow('out', out) # вывод обработанного кадра в окно

cv.waitKey(4000)
cv.destroyAllWindows()