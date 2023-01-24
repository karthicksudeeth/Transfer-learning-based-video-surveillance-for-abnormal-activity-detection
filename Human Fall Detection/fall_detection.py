import cv2
import time

cap = cv2.VideoCapture('fall4.mp4') 
time.sleep(2)  

fgbg = cv2.createBackgroundSubtractorMOG2() 
j = 0 
fall_flag=0 
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
while(1): 
    print("In")
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        areas = []
        for contour in contours:
            ar = cv2.contourArea(contour)
            areas.append(ar)
        max_area = max(areas, default = 0)
        max_area_index = areas.index(max_area)
        cnt = contours[max_area_index]
        M = cv2.moments(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0) 
        if h < w:
            j += 1
        if j > 10:
            print("FALL")
            fall_flag=1
            cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2) 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) 
        if h > w:
            j = 0
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
        cv2.imshow('video', frame)
        result.write(frame)
        if cv2.waitKey(33) == 27:
            break

cap.release()
result.release()
cv2.destroyAllWindows()