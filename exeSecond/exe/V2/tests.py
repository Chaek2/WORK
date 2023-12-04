import numpy as np
import cv2 as cv
import math
from PIL import Image
import time
import Commands

def nothing(*arg):
    pass

cv.namedWindow("Display window", cv.WINDOW_NORMAL)
cv.resizeWindow("Display window", 500, 500)

cv.namedWindow("Display", cv.WINDOW_NORMAL)
cv.resizeWindow("Display", 500, 500)

cv.namedWindow("Dis", cv.WINDOW_NORMAL)
cv.resizeWindow("Dis", 500, 500)

cv.namedWindow("settings")  # создаем окно настроек
cv.resizeWindow("settings", 500, 400)

cv.createTrackbar("h_min_1", "settings", 0, 255, nothing)
cv.createTrackbar("h_min_2", "settings", 23, 255, nothing)
cv.createTrackbar("h_min_3", "settings", 0, 255, nothing)
cv.createTrackbar("h_max_1", "settings", 255, 255, nothing)
cv.createTrackbar("h_max_2", "settings", 255, 255, nothing)
cv.createTrackbar("h_max_3", "settings", 255, 255, nothing)
cv.createTrackbar("area1", "settings", 290, 20000, nothing)
cv.createTrackbar("area2", "settings", 800, 20000, nothing)
cv.createTrackbar("cnt", "settings", 0, 6, nothing)

fn = "PT0.jpg"
# img_main = cv.imread(fn)
with Image.open(fn) as img_main:
    img_main.load()
x,y = img_main.size
dels = 70
box = (x/2-dels,y/2-dels,x/2+dels,y/2+dels)
im = img_main.crop(box)
imgs = np.array(im)
hsv = cv.cvtColor(imgs, cv.COLOR_BGR2HSV)
area1 = 6666
area2 = 10000
# break
while True:
    h_min_1 = cv.getTrackbarPos("h_min_1", "settings")
    h_min_2 = cv.getTrackbarPos("h_min_2", "settings")
    h_min_3 = cv.getTrackbarPos("h_min_3", "settings")
    h_max_1 = cv.getTrackbarPos("h_max_1", "settings")
    h_max_2 = cv.getTrackbarPos("h_max_2", "settings")
    h_max_3 = cv.getTrackbarPos("h_max_3", "settings")
    area1 = cv.getTrackbarPos("area1", "settings")
    area2 = cv.getTrackbarPos("area2", "settings")
    CD = int(cv.getTrackbarPos("cnt", "settings"))
    img = imgs.copy()
    h_min = np.array((h_min_1, h_min_2, h_min_3), np.uint8)
    h_max = np.array((h_max_1, h_max_2, h_max_3), np.uint8)
    thresh = cv.inRange(hsv, h_min, h_max)
    contours = cv.findContours(
        thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
    )[0]
    if len(contours) > 0:
        cnts = []
        i=0
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0] * rect[1][1])
            if area > area1 and area < area2:
                cnts.append(box)
        b = cnts[CD]
        cv.drawContours(thresh, [b], -1, (255, 255, 255), 2)
        cv.drawContours(img, [b], -1, (255, 255, 255), 2)           
    angle = Commands.angleSearch()
    img_m = cv.imread(fn)
    cv.imshow("Display window", img)
    cv.imshow("Display", thresh)
    cv.imshow("Dis", img_m)
    if cv.waitKey(1) == ord("q"):
        break

cv.destroyAllWindows()


# 0 23 0 / 255 255 196 / 2041 7872
# [[ 30  41] 
#  [112  28]
#  [126 111]
#  [ 44 125]]