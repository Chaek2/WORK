import numpy as np
import cv2 as cv
from PIL import Image

def Starts(fn):
    imgs = cv.imread(fn,0)
    ret,thresh = cv.threshold(imgs,60,255,0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        area = int(rect[1][0]*rect[1][1])
        if area > 400:
            x_l = []
            y_l = []
            for x,y in box:
                x_l.append(x)
                y_l.append(y)
            crop = imgs[min(y_l)-20:max(y_l)+20,min(x_l)-20:max(x_l)+20]
            im = Image.fromarray(crop)
            im.save('crop.jpg') 
            