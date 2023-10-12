import numpy as np
import cv2 as cv
import math

fn = "2wo/photo_2023-09-13_16-42-13.jpg"
# fn = "2wo/test_photo1.jpg"
img = cv.imread(fn)
imgm = img.copy()
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h_min = np.array((0, 0, 0), np.uint8)
h_max = np.array((255, 255, 255), np.uint8)
imgs = cv.inRange(hsv, h_min, h_max)

contours = cv.findContours(imgs.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]

for cnt in contours:
    rect = cv.minAreaRect(cnt)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    area = int(rect[1][0] * rect[1][1])
    if area > 16000 and area < 1000000:
        cv.drawContours(imgm, [box], -1, (0, 255, 0), 3, cv.LINE_AA)
        # (x, y, w, h) = cv.boundingRect(cnt)
        # img = img[y:y+h, x:x+w]
    print(area)
cv.imshow("DisplayN", img)
cv.imshow("DisplayS", imgm)
cv.waitKey(0)
cv.destroyAllWindows()