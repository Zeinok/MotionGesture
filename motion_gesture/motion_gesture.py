#!/bin/env python3
import argparse
import time
import logging

from cv2 import cv2
import imutils

from direction import Direction

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--min-area", type=int, default=9000, help="minimum area size")
ap.add_argument("-a", "--max-area", type=int, default=75000, help="maximum area size")
ap.add_argument("-b", "--blur", type=int, default=31, help="blur")
ap.add_argument("-t", "--threshold", type=int, default=10, help="threshold")
ap.add_argument("-d", "--dilation", type=int, default=2, help="dilation")
ap.add_argument("-f", "--file", type=str, default=0, help="file")
ap.add_argument("-w", "--wait", type=int, default=100, help="ms to wait")
ap.add_argument("-l", "--log", type=int, default=20, help="log level")
args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["file"])
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
logging.basicConfig(level=args["log"])

previousFrame = None

previous_x, previous_y = -1, -1
previous_dx, previous_dy = 0, 0
largest_area_x = 0
largest_area_y = 0

direction_log = []
last_movement = time.time() * 1000

while True:

    grabbed, frame = camera.read()
    frame = imutils.resize(frame, width=500)
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0)
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

    previousFrame = gray
    frameDelta = cv2.cvtColor(frameDelta, cv2.COLOR_GRAY2RGB)
    # loop over the contours
    largest_area = 0
    largest_area_x, largest_area_y = -1, -1
    for c in cnts:
        # if the contour is too small, ignore it
        area = cv2.contourArea(c)
        if area < args["min_area"]:
            continue
        if area > args["max_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            str(area),
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        if area > largest_area:
            largest_area_x, largest_area_y = x, y
            largest_area = area
        last_movement = time.time() * 1000

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Thresh", thresh)
    
    
    dx, dy = largest_area_x - previous_x, largest_area_y - previous_y
    previous_dx, previous_dy = dx, dy
    previous_x, previous_y = largest_area_x, largest_area_y
    
    dx, dy = previous_dx*0.3 + dx*0.7, previous_dy*0.5 + dy*0.7
    # dx, dy = dx/2, dy/2
    dx, dy = int(dx), int(dy)
    

    if dx!=0 or dy!=0:
        direction = Direction.Null
        if abs(dx)>abs(dy):
            direction = Direction.Left if dx < 0 else Direction.Right
        else:
            direction = Direction.Up if dy < 0 else Direction.Down
        logging.debug("{}, dx={}, dy={}".format(direction, dx, dy))
        direction_log.append(direction)
    
    if time.time() * 1000 - last_movement > args["wait"]:
        if len(direction_log) > 0:
            logging.info("Result: {}".format(max(direction_log, key=direction_log.count)))
            # for e in Direction:
            #     logging.info("Result: {} {}x".format(e, direction_log.count(e)))
            direction_log.clear()

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break


camera.release()
cv2.destroyAllWindows()

