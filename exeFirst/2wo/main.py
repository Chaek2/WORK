
        cv.imwrite("Pushs2.jpg", image_second)
        
        image_sec = cv.imread("Pushs2.jpg")
        hsv = cv.cvtColor(image_sec, cv.COLOR_BGR2HSV)
        h_min = np.array((0, 40, 31), np.uint8)
        h_max = np.array((35, 255, 255), np.uint8)
        image_third = cv.inRange(hsv, h_min, h_max)
        contours = cv.findContours(
            image_third.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS
        )[0]
        for cnt in contours:
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0] * rect[1][1])
            if area > area1 and area < area2:
                cnts.append(box)
        cnts1 = cnts[0]
        x, y = image_third.shape[:2]
            
        print(cnts1)
        print(y,y/1.2,y/1.5,y/2,y/3,y/4,y/5)
        cv.circle(image_sec,(cnts1[0][0],cnts1[0][1]),1,(0,0,255),-1)
        cv.circle(image_sec,(cnts1[2][0],cnts1[2][1]),1,(0,0,255),-1)
        # print(t1[1] > y/1.5)
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
            image_sec = self.RotateImage(image_sec, 180)
            if(angle > 0):
                angle +=180
            else:
                angle-=180   
            cv.imwrite("Push2.jpg", image_sec)