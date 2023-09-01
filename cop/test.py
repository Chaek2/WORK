import cv2 as cv
import numpy as np

cv.namedWindow("Display window", cv.WINDOW_NORMAL)
cv.resizeWindow("Display window", 500, 500)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    cv.imshow('Display window',frame)
    if cv.waitKey(1) == ord('q'):
        break

k = cv.waitKey(5000)
cv.destroyAllWindows()