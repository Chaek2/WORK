import numpy as np
import cv2 as cv
import math

def Rap():
    def nothing(*arg):
        pass

    cv.namedWindow("Display window", cv.WINDOW_NORMAL)
    cv.resizeWindow("Display window", 500, 500)

    cv.namedWindow("result", cv.WINDOW_NORMAL)
    cv.resizeWindow("result", 500, 500)

    cv.namedWindow( "settings" ) # создаем окно настроек

    cv.createTrackbar('h1', 'settings', 0, 255, nothing)
    cv.createTrackbar('s1', 'settings', 0, 255, nothing)
    cv.createTrackbar('v1', 'settings', 0, 255, nothing)
    cv.createTrackbar('h2', 'settings', 255, 255, nothing)
    cv.createTrackbar('s2', 'settings', 255, 255, nothing)
    cv.createTrackbar('v2', 'settings', 93, 255, nothing) #92-102
    crange = [0,0,0, 0,0,0]


    fn = 'crop.jpg'
    img = cv.imread(fn)
    immgs = img.copy()

    crange = [0,0,0, 0,0,0]

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV )
    while True:

        img = immgs.copy()

        h1 = cv.getTrackbarPos('h1', 'settings')
        s1 = cv.getTrackbarPos('s1', 'settings')
        v1 = cv.getTrackbarPos('v1', 'settings')
        
        h2 = cv.getTrackbarPos('h2', 'settings')
        s2 = cv.getTrackbarPos('s2', 'settings')
        v2 = cv.getTrackbarPos('v2', 'settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)
        thresh = cv.inRange(hsv, h_min, h_max)
        contours0 = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
        cnts = []
        for cnt in contours0:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0]*rect[1][1])
            if area > 300 and area < 1000:
                cv.drawContours(img,[box],-1,(255,0,0),2)
                cnts = box
        edge1 = np.int0((cnts[1][0] - cnts[0][0],cnts[1][1] - cnts[0][1]))
        edge2 = np.int0((cnts[2][0] - cnts[1][0], cnts[2][1] - cnts[1][1]))

        usedEdge = edge1
        if cv.norm(edge2) > cv.norm(edge1):
            usedEdge = edge2
        reference = (1,0) 

        angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv.norm(reference) *cv.norm(usedEdge)))
        print(angle)
        
        cv.imshow('result', thresh) 
        cv.imshow('Display window', img) 
        # break
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

Rap()
