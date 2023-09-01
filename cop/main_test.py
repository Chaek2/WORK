import numpy as np
import cv2 as cv
from PIL import Image
import math


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
            # fn = 'crop.jpg'
            # img = cv.imread(fn)
            # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV )

            # h_min = np.array((0, 0, 0), np.uint8)
            # h_max = np.array((255, 255, 93), np.uint8)

            # thresh = cv.inRange(hsv, h_min, h_max)
            # contours0 = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
            # cnts = []
            # for cnt in contours0:
            #     rect = cv.minAreaRect(cnt)
            #     box = cv.boxPoints(rect)
            #     box = np.int0(box)
            #     area = int(rect[1][0]*rect[1][1])
            #     if area > 300 and area < 1000:
            #         cv.drawContours(img,[box],-1,(255,0,0),2)
            #         cnts = box
            # edge1 = np.int0((cnts[1][0] - cnts[0][0],cnts[1][1] - cnts[0][1]))
            # edge2 = np.int0((cnts[2][0] - cnts[1][0], cnts[2][1] - cnts[1][1]))

            # usedEdge = edge1
            # if cv.norm(edge2) > cv.norm(edge1):
            #     usedEdge = edge2
            # reference = (1,0) 

            # angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv.norm(reference) *cv.norm(usedEdge)))
            # print(angle)

    cv.destroyAllWindows()


        
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-47.jpg' # имя файла, который будем анализировать
# fn = 'photo_2023-08-31_17-55-50.jpg' # имя файла, который будем анализироватьx
fn = 'photo_2023-08-31_17-55-53.jpg' # имя файла, который будем анализировать
Start(fn)