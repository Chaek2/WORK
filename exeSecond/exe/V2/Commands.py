from PIL import Image
import numpy as np
import cv2 as cv
import math

def Ang(image_main, angle):
    rows, cols = image_main.shape[:2]
    M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
    img = cv.warpAffine(image_main, M, (cols, rows))
    return img

def angleSearch():
    with Image.open("PT0.jpg") as img_main:
        img_main.load()
    x,y = img_main.size
    box = (x/2-70,y/2-70,x/2+70,y/2+70)
    im = img_main.crop(box)
    image_main = np.array(im)

    hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
    h_min = np.array((0, 27, 0), np.uint8)
    h_max = np.array((255, 255, 255), np.uint8)
    image_first = cv.inRange(hsv, h_min, h_max)

    cnts = []

    contours = cv.findContours(
        image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
    )[0]
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        area = int(rect[1][0] * rect[1][1])
        if area > 290 and area < 800:
            cnts.append(box)
    try:
        cnts1 = cnts[2]
        t1 = 0
        t2 = 0

        if math.sqrt(
            (cnts1[0][0] - cnts1[1][0]) ** 2 + (cnts1[0][1] - cnts1[1][1]) ** 2
        ) < math.sqrt(
            (cnts1[0][0] - cnts1[3][0]) ** 2 + (cnts1[0][1] - cnts1[3][1]) ** 2
        ):
            # #неч
            t1 = [cnts1[0][0], cnts1[3][1]]
            t2 = [cnts1[3][0], cnts1[0][1]]
        else:
            # ч
            t1 = [cnts1[0][0], cnts1[1][1]]
            t2 = [cnts1[1][0], cnts1[0][1]]
        angle = math.degrees(math.atan((t1[1] - t2[1]) / (t2[0] - t1[0])))
        x, y = image_main.shape[:2]
        xs = y/2-cnts1[0][1]
        ys = y/2-cnts1[2][1]
            
        xt = 0
        if xs > 0:
            if abs(xs) > abs(ys):
                xt = xs
            else:
                xt = ys
        else:
            if abs(xs) < abs(ys):
                xt = xs
            else:
                xt = ys
        if xt < 0:
            image_main = self.RotateImage(image_main, 180)
            if angle < 180:
                angle +=180
            elif angle > 180:
                angle-=180       
        cv.imwrite("TM0.jpg", Ang(image_main,angle)) 

        return angle
    except:
        return 0

def CheckAngle(angle):





    return 0