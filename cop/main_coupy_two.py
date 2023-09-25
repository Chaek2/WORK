import numpy as np
import cv2 as cv
import math


def SimpleWay(rotateImage, angle):
    imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]
    centreY, centreX = imgHeight//2, imgWidth//2
    rotationMatrix = cv.getRotationMatrix2D((centreY, centreX), angle, 1.0)
    rotatingimage = cv.warpAffine(
        rotateImage, rotationMatrix, (imgWidth, imgHeight))
    return rotatingimage

def nothing(*arg):
    pass

cv.namedWindow("DisplayR", cv.WINDOW_NORMAL)
cv.resizeWindow("DisplayR", 500, 500)
cv.namedWindow("DisplayN", cv.WINDOW_NORMAL)
cv.resizeWindow("DisplayN", 500, 500)

crange = [0,0,0, 0,0,0]

fn = 'C:\\Users\\Anton\\Desktop\\Working\\WORK\\2wo\\photo_2023-09-13_16-43-07.jpg'
im = cv.imread(fn)

area1 = 2400
area2 = 10000

hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV )
while True:
    img = im
    cnts=[]
    h_min = np.array((0, 40, 31), np.uint8)
    h_max = np.array((35, 255, 255), np.uint8)
    thresh = cv.inRange(hsv, h_min, h_max)
    contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        area = int(rect[1][0]*rect[1][1])
        if area > area1 and area < area2:
            cv.drawContours(img,[box],-1,(255,0,0),2)
            cv.drawContours(im,[box],-1,(255,0,0),2)
            cnts.append(box)
    cnts1=cnts[0]
    
    t1 = 0
    t2 = 0 

    if math.sqrt((cnts1[0][0]-cnts1[1][0])**2+(cnts1[0][1]-cnts1[1][1])**2) > math.sqrt((cnts1[0][0]-cnts1[3][0])**2+(cnts1[0][1]-cnts1[3][1])**2):
        # #неч
        t1 = [cnts1[0][0],cnts1[3][1]]
        t2 = [cnts1[3][0],cnts1[0][1]]
    else:
        #ч 
        t1 = [cnts1[0][0],cnts1[1][1]]
        t2 = [cnts1[1][0],cnts1[0][1]]

    angle = math.degrees(math.atan((t1[1]-t2[1])/(t2[0]-t1[0])))
    img = SimpleWay(img,angle)
    print(angle)
    cv.imshow('DisplayR', img) 
    cv.imshow('DisplayN', im) 
    
    # break
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()

