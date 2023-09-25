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

    cv.createTrackbar('R', 'settings', 360, 720, nothing)

    fn = 'C:\\Users\\Anton\\Desktop\\Working\\WORK\\2wo\\photo_2023-09-13_16-43-08.jpg'
    imgs = cv.imread(fn)
    # break
    while True:
        R = cv.getTrackbarPos('R', 'settings')
        thresh = SimpleWay(imgs,R)
        cv.imshow('Display window', imgs) 
        cv.imshow('Display', thresh) 
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

def SimpleWay(rotateImage, angle):
    imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]
    centreY, centreX = imgHeight//2, imgWidth//2
    rotationMatrix = cv.getRotationMatrix2D((centreY, centreX), angle, 1.0)
    rotatingimage = cv.warpAffine(
        rotateImage, rotationMatrix, (imgWidth, imgHeight))
    return rotatingimage

# def SearchRad(Image,processtype):
#     area1 = 0
#     area2 = 0
#     if processtype == 0:
#         area1 = 3000
#         area2 = 10000
#     else:
#         area1 = 2400
#         area2 = 45000
#     h_min = np.array((0, 42, 39), np.uint8)
#     h_max = np.array((35, 255, 255), np.uint8)
#     thresh = cv.inRange(hsv, h_min, h_max)
#     contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
#     if len(contours) > 0:
#         for cnt in contours:
#             rect = cv.minAreaRect(cnt)
#             box = cv.boxPoints(rect)
#             box = np.int0(box)
#             area = int(rect[1][0]*rect[1][1])
#             if area > area1 and area < area2:
#                 print('')
    

Rap()
