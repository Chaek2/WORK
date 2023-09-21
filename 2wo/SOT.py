import numpy as np
import cv2 as cv
import math

def Rap():
    def nothing(*arg):
        pass

    cv.namedWindow("Display window", cv.WINDOW_NORMAL)  
    cv.resizeWindow("Display window", 500, 500)

    cv.namedWindow("Display", cv.WINDOW_NORMAL)  
    cv.resizeWindow("Display", 500, 500)

    cv.namedWindow( "settings" ) # создаем окно настроек

    cv.createTrackbar('area1', 'settings', 2400, 10000, nothing)#4000
    cv.createTrackbar('area2', 'settings', 40000, 90000, nothing)

    fn = 'C:\\Users\\Anton\\Desktop\\Working\\WORK\\2wo\\photo_2023-09-13_16-43-05.jpg'
    imgs = cv.imread(fn)
    hsv = cv.cvtColor(imgs, cv.COLOR_BGR2HSV)
    area1 = 2400
    area2 = 40000
    # break
    while True:
        area1 = cv.getTrackbarPos('area1', 'settings')
        area2 = cv.getTrackbarPos('area2', 'settings')
        img = imgs
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        thresh = cv.inRange(hsv, h_min, h_max)
        contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
        if len(contours) > 0:
            print('-'*40)
            cnts = []
            for cnt in contours:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                area = int(rect[1][0]*rect[1][1])
                if area > area1 and area < area2:
                    cv.drawContours(thresh,[box],-1,(255,0,0),2)
                    cv.drawContours(img,[box],-1,(255,0,0),2)
                    cnts.append(box)
                    print(box)
        cv.imshow('Display window', img) 
        cv.imshow('Display', thresh) 
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

Rap()
