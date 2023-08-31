import cv2 as cv
import numpy as np


#size crop
y=180
x=10
h=900
w=900

hsv_min = np.array((0, 50, 5), np.uint8)
hsv_max = np.array((187, 255, 253), np.uint8)

#search file
i1 = cv.imread('photo_2023-08-31_17-55-36.jpg')

#create window
cv.namedWindow("Display window", cv.WINDOW_NORMAL)

#resize img (center)
crop_img = i1[y:y+h, x:x+w]

#gray = cv.cvtColor(crop_img,cv.COLOR_BGR2GRAY)

hsv = cv.cvtColor( crop_img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV

thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
contours0, hierarchy = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

for cnt in contours0:
        rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        area = int(rect[1][0]*rect[1][1]) # вычисление площади
        if area > 500:
            cv.drawContours(crop_img,[box],0,(255,0,0),2)

#show window
cv.imshow('Display window',crop_img)

#size window
cv.resizeWindow("Display window", 500, 500)




#seconds
k = cv.waitKey(5000)
cv.destroyAllWindows()