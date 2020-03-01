import imutils
import cv2
from utils import combine_rects

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

while 1:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    fgmask = fgbg.apply(frame)
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=1)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    rects = []
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 1500:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # (x, y, w, h) = cv2.boundingRect(c)
        rects.append(cv2.boundingRect(c))

    rects = combine_rects(rects)

    for r in rects:
        if r:
            x, y, w, h = r
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    cv2.imshow('thresh', thresh)
    k = cv2.waitKey(30) & 0xff
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
