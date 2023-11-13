import numpy as np
import cv2 as cv
from PIL import Image

fn = "2wo/photo_2023-09-13_16-42-11.jpg"
# fn = "2wo/test_photo1.jpg"

with Image.open(fn) as img1:
    img1.load()
x,y = img1.size
box = (x/2-400,y/2-300,x/2+400,y/2+300)
imgs = img1.crop(box)
imgs.save('Push0.jpg')

img = cv.imread("Push0.jpg")
cv.imshow("DisplayN", img)
cv.waitKey(0)
cv.destroyAllWindows()