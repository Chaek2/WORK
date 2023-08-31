import numpy as np
import cv2 as cv

cv.namedWindow("Display window", cv.WINDOW_NORMAL)
cv.resizeWindow("Display window", 500, 500)

cv.namedWindow("Display", cv.WINDOW_NORMAL)
cv.resizeWindow("Display", 500, 500)

cv.namedWindow("out", cv.WINDOW_NORMAL)
cv.resizeWindow("out", 500, 500)

hsv_min = np.array((0, 54, 5), np.uint8)
hsv_max = np.array((187, 255, 253), np.uint8)

# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-50.jpg' # имя файла, который будем анализировать
fn = 'photo_2023-08-31_17-55-53.jpg' # имя файла, который будем анализировать

img = cv.imread(fn)


hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV
thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
contours0, hierarchy = cv.findContours( thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)

# перебираем все найденные контуры в цикле
for cnt in contours0:
    rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
    box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
    box = np.int0(box) # округление координат
    area = int(rect[1][0]*rect[1][1]) # вычисление площади
    if area > 500:
        cv.drawContours(img,[box],-1,(255,0,0),2)
        x_l = []
        y_l = []
        for x,y in box:
            x_l.append(x)
            y_l.append(y)
        
        crop = img[min(y_l)-10:max(y_l)+10,min(x_l)-10:max(x_l)+10]
        out = cv.addWeighted( crop, 1, crop, 0, -60)


cv.imshow('Display window', img) # вывод обработанного кадра в окно

cv.imshow('Display', crop) # вывод обработанного кадра в окно

cv.imshow('out', out) # вывод обработанного кадра в окно

cv.waitKey(3000)
cv.destroyAllWindows()