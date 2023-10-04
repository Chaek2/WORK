import numpy as np
import cv2 as cv
import math
    
image_main = cv.imread('test\\2_angle_279.jpg')
hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
h_min = np.array((0, 40, 31), np.uint8)
h_max = np.array((35, 255, 255), np.uint8)
image_first = cv.inRange(hsv, h_min, h_max)

cnts = []

area1 = 6666
area2 = 20000

contours = cv.findContours(image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)[0]
for cnt in contours:
    rect = cv.minAreaRect(cnt)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    area = int(rect[1][0] * rect[1][1])
    if area > area1 and area < area2:
        cv.drawContours(image_first, [box], -1, (255, 0, 255), 2)
        cnts.append(box)

cv.imwrite("Pu1.jpg", image_first)
print(cnts)
cnts1 = cnts[0]

t1 = 0
t2 = 0

if math.sqrt(
    (cnts1[0][0] - cnts1[1][0]) ** 2 + (cnts1[0][1] - cnts1[1][1]) ** 2
) > math.sqrt(
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
print(angle)

rows, cols = image_first.shape[:2]
M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
img = cv.warpAffine(image_first, M, (cols, rows))

cv.imwrite("Pu2.jpg", img)
