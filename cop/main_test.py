import cv2 as cv
import numpy as np

cv.namedWindow("Display window", cv.WINDOW_NORMAL)
cv.resizeWindow("Display window", 500, 500)

c = 4 

img_path = 'photo_2023-08-31_17-55-36.jpg'

img = cv.imread(img_path,0)


def find_contours_of_cards(image):
    blurred = cv.GaussianBlur(image, (3, 3), 0)
    T, thresh_img = cv.threshold(blurred, 215, 255, 
                                  cv.THRESH_BINARY)
    (cnts, _) = cv.findContours(thresh_img, 
                                cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)
    return cnts


print(find_contours_of_cards(img))

cv.imshow("Display window", img)

k = cv.waitKey(5000)
cv.destroyAllWindows()
















# img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# ret, thresh = cv.threshold(img_gray, 100, 155, cv.THRESH_BINARY)

# contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

# image_copy = img.copy()
# cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
