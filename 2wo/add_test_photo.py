import math
import numpy as np
import cv2 as cv
from PIL import Image
import random

puth1 = 'photo/test_photo1.jpg'
puth2  = 'photo/test_photo2.jpg'

def SimpleWay(rotateImage, angle):
    imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]
    centreY, centreX = imgHeight//2, imgWidth//2
    rotationMatrix = cv.getRotationMatrix2D((centreY, centreX), angle, 1.0)
    rotatingimage = cv.warpAffine(
        rotateImage, rotationMatrix, (imgWidth+10, imgHeight+10))
    return rotatingimage

ims = cv.imread(puth1)
# cv.imwrite('test\\angle.jpg',ims)

for a in range(0,5):
    i1 = random.randint(0,360)
    i2 = random.randint(0,360)

    img1p = cv.imread(puth1)
    img2p = cv.imread(puth2)

    rows1,cols1 = img1p.shape[:2]
    rows2,cols2 = img2p.shape[:2]
        
    M1 = cv.getRotationMatrix2D(((cols1-1)/2.0,(rows1-1)/2.0),i1,1)
    M2 = cv.getRotationMatrix2D(((cols2-1)/2.0,(rows2-1)/2.0),i1,1)

    img1 = cv.warpAffine(img1p,M1,(cols1,rows1))
    img2 = cv.warpAffine(img2p,M2,(cols2,rows2))

        
    cv.imwrite('test\\1_angle_'+str(i1)+'.jpg',img1)

    cv.imwrite('test\\2_angle_'+str(i2)+'.jpg',img2)

