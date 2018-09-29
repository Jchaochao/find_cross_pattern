import numpy as np
import cv2
import time
import os

ROOT_DIR = os.path.abspath('../find_cross_pattern/')
#sys.path.append(os.path.join(ROOT_DIR,'images/'))
IMG_DIR = os.path.join(ROOT_DIR,'pics\\')
IMG_PATH = os.path.join(IMG_DIR,'test.jpg')

img = cv2.imread(IMG_PATH,1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur_bar = 0
th1_bar = 19
th2_bar = 34
hough_bar = 2

blur_max = 30
th1_max = 50
th2_max = 50
hough_max = 10

def do_some_change(x):
    print ('change')

    blur = cv2.getTrackbarPos('blur', 'res') * 2 + 1
    th1 = cv2.getTrackbarPos('th1', 'res') * 10
    th2 = cv2.getTrackbarPos('th2', 'res') * 10
    hough = cv2.getTrackbarPos('hough', 'res') * 50 + 300

    blur_img = cv2.GaussianBlur(gray, (blur, blur), 0)
    canny = cv2.Canny(blur_img, th1, th2)
    dst = cv2.bitwise_and(img, img, mask=canny)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, hough)
    print (lines.shape)
    for line in lines:
        rho, theta = tuple(line[0])
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 4000*(-b))
        y1 = int(y0 + 4000*(a))
        x2 = int(x0 - 4000*(-b))
        y2 = int(y0 - 4000*(a)) 
        cv2.line(dst, (x1,y1), (x2,y2), (255,0,0), 1)
        cv2.circle(dst, (x0, y0), 3, (0, 0, 255), -1)

    sacle = 1
    small = cv2.resize(dst, (dst.shape[1] / sacle, dst.shape[0] / sacle), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('res', small)

cv2.namedWindow('res')
cv2.createTrackbar('blur', 'res', blur_bar, blur_max, do_some_change)
cv2.createTrackbar('th1', 'res', th1_bar, th1_max, do_some_change)
cv2.createTrackbar('th2', 'res', th2_bar, th2_max, do_some_change)
cv2.createTrackbar('hough', 'res', hough_bar, hough_max, do_some_change)

do_some_change(0)
while True:
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
        break
    elif key == 113 or key == 97:
        tmp = cv2.getTrackbarPos('blur', 'res')
        tmp = tmp + 1 if key == 113 else tmp - 1
        tmp = max(min(tmp, blur_max), 0)
        cv2.setTrackbarPos('blur', 'res', tmp)
    elif key == 119 or key == 115:
        tmp = cv2.getTrackbarPos('th1', 'res')
        tmp = tmp + 1 if key == 119 else tmp - 1
        tmp = max(min(tmp, th1_max), 0)
        cv2.setTrackbarPos('th1', 'res', tmp)
    elif key == 101 or key == 100:
        tmp = cv2.getTrackbarPos('th2', 'res')
        tmp = tmp + 1 if key == 101 else tmp - 1
        tmp = max(min(tmp, th2_max), 0)
        cv2.setTrackbarPos('th2', 'res', tmp)
    elif key == 114 or key == 102:
        tmp = cv2.getTrackbarPos('hough', 'res')
        tmp = tmp + 1 if key == 114 else tmp - 1
        tmp = max(min(tmp, hough_max), 0)
        cv2.setTrackbarPos('hough', 'res', tmp)
    elif key != 255:
        print (key)
cv2.destroyAllWindows()
