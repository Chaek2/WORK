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
    cnts = []
    try:
        with Image.open("exeSecond/exe/V2/PH/PT0.jpg") as img_main:
            img_main.load()
        x,y = img_main.size
        boxes = (x/2-70,y/2-70,x/2+70,y/2+70)
        im = img_main.crop(boxes)
        img_main = np.array(img_main)
        image_main = np.array(im)

        hsv = cv.cvtColor(image_main, cv.COLOR_BGR2HSV)
        h_min = np.array((0, 27, 0), np.uint8)
        h_max = np.array((255, 255, 255), np.uint8)
        image_first = cv.inRange(hsv, h_min, h_max)
        # cv.imwrite("exeSecond/exe/V2/PH/TM0.jpg", image_first)

        contours = cv.findContours(
            image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
        )[0]
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            boxcp = cv.boxPoints(rect)
            box = np.int0(boxcp)
            area = int(rect[1][0] * rect[1][1])
            # if area > 290 and area < 800:
            if area > 525 and area < 1516:
                cnts.append(box)
    except Exception as e:
        print('ERROR_0: '+str(e))
        return 0
    if len(cnts) > 0:
        try:
            # if len(cnts) > 2: cnts1 = cnts[2]
            # elif len(cnts) > 1: cnts1 = cnts[1]
            # else:
            #     print("ERROR_0.1")
            #     return 0
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
        except Exception as e:
            print('ERROR_1: '+str(e))
            return 0
        try:
            x, y = image_main.shape[:2]
            xs = y/2.0-cnts1[0][1]
            ys = y/2.0-cnts1[2][1]
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
                image_main = Ang(image_main, 180)
                if angle < 180:
                    angle +=180
                elif angle > 180:
                    angle-=180
        except Exception as e:
            print('ERROR_2: '+str(e))
            return 0       
        # cv.imwrite("exeSecond/exe/V2/PH/TM1.jpg", Ang(image_main,angle))
        # cv.imwrite("exeSecond/exe/V2/PH/TM2.jpg", Ang(img_main,angle))
        return angle
    print("Нет элементов")
    return 0

def SearchCounter():
    try:
        with Image.open("TM1.jpg") as img_main:
            img_main.load()
        img_main = np.array(img_main)
        hsv = cv.cvtColor(img_main, cv.COLOR_BGR2HSV)
        height, width = hsv.shape[:2]
        X=int(height/2)
        Y=int(width/2)

        h_min = np.array((0, 23, 0), np.uint8)
        h_max = np.array((255, 255, 196), np.uint8)
        image_first = cv.inRange(hsv, h_min, h_max)
        contours = cv.findContours(
            image_first.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
        )[0]
        if len(contours) > 0:
            cnts = []
            for cnt in contours:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                area = int(rect[1][0] * rect[1][1])
                if area > 2041 and area < 7872:
                    x1 = abs(box[0][0]-box[3][0])
                    y1 = abs(box[1][1]-box[3][1])
                    return round((X-x1)/100,1)/2,round((Y-y1)/100,1)/2
    except:
        print("ERROR_3")

# print(angleSearch())