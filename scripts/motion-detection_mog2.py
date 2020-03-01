"""Detect objects in motion and mark them with rectangles."""

import imutils
import cv2
from computervision.utils import combine_rects

# minimum object size for motion detection in square pixels
MIN_CONTOUR_AREA = 1500

# capture from camera
cap = cv2.VideoCapture(0)
# create a BackgroundSubtractactor object for detecting motions
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

while 1:
    # read and resize frame
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    # apply background substractor, add threshold and dilate
    fgmask = fgbg.apply(frame)
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=1)

    # find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    rects = combine_rects([cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > MIN_CONTOUR_AREA])

    for r in rects:
        if r:
            x, y, w, h = r
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    cv2.imshow('fgbg', fgmask)
    cv2.imshow('thresh', thresh)
    k = cv2.waitKey(30) & 0xff
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
