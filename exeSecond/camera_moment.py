import cv2 as cv

num_cam=1

def VIDIO():
    try:
        video=cv.VideoCapture(num_cam)
        hasFrame,frame=video.read()
        return frame
    except:
        pass


def img():
    try:
        video=cv.VideoCapture(num_cam)
        hasFrame,frame=video.read()
        cv.imwrite("DOWN.jpg", frame)  
    except:
        pass

def test():
    try:
        video=cv.VideoCapture(num_cam)
        while 1:
            hasFrame,frame=video.read()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            height, width = gray.shape[:2]
            start_p_v=(0,int(height/2))
            end_p_v=(width,int(height/2))
            start_p_h=(int(width/2),0)
            end_p_h=(int(width/2),height)
            circ = (int(width/2),int(height/2))
            cv.line(gray,start_p_v,end_p_v,(0,255,0),2)
            cv.line(gray,start_p_h,end_p_h,(0,255,0),2)
            cv.circle(gray,circ,3,(255,0,0),2)
            cv.imshow("Display window", gray)
            if cv.waitKey(1) == ord("q"):
                break
    except:
        pass