import argparse
import time

from cv2 import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--min-area", type=int, default=5000, help="minimum area size")
ap.add_argument("-a", "--max-area", type=int, default=100000, help="maximum area size")
ap.add_argument("-b", "--blur", type=int, default=31, help="blur")
ap.add_argument("-t", "--threshold", type=int, default=10, help="threshold")
ap.add_argument("-d", "--dilation", type=int, default=2, help="dilation")
ap.add_argument("-f", "--file", type=str, default=0, help="file")
args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["file"])
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
diffFrame = None
previousFrame = None
counter = 0
while True:

    grabbed, frame = camera.read()
    frame = imutils.resize(frame, width=500)
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    noblur_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (args["blur"], args["blur"]), 0)
    # if the first frame is None, initialize it
    if previousFrame is None:
        previousFrame = gray
        continue
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(previousFrame, gray)
    thresh = cv2.threshold(frameDelta, args["threshold"], 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=args["dilation"])
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        if cv2.contourArea(c) > args["max_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            str(cv2.contourArea(c)),
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    faces = face_cascade.detectMultiScale(noblur_gray, 1.1, 3, 0)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    previousFrame = gray

    k = cv2.waitKey(17) & 0xFF
    if k == 27:
        break


camera.release()
cv2.destroyAllWindows()
