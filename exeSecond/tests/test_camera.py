import cv2 as cv
video=cv.VideoCapture(1)
while cv.waitKey(1)<0:
    hasFrame,frame=video.read()
    if not hasFrame:
        cv.waitKey()
        break
    cv.imshow("Image 1", frame)