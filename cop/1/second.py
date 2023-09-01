import numpy as np
import cv2 as cv
import math

def Rotate():    
    fn = 'crop.jpg'
    img = cv.imread(fn)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV )
    h_min = np.array((0, 0, 0), np.uint8)
    h_max = np.array((255, 255, 93), np.uint8)
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
    reference = (0,1) 
    angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv.norm(reference) *cv.norm(usedEdge)))
    print(angle)  
    # return angle  