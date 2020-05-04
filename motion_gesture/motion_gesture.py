import cv2
import numpy
import matplotlib.pyplot as plt

# min_YCrCb = numpy.array([0,133,77],numpy.uint8)
# max_YCrCb = numpy.array([255,173,127],numpy.uint8)
min_YCrCb = numpy.array([0, 140, 100], numpy.uint8)
max_YCrCb = numpy.array([255, 175, 120], numpy.uint8)
# 140 175 cr
# 100 120 cb

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
image = None
cropped_image = None

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        visual = image.copy()
        cv2.rectangle(visual, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("main", visual)
        cropped_image = image.copy()
        cropped_image = cropped_image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("cropped", cropped_image)
        print(type(cropped_image))
        plot_skin_arrange(cropped_image)
pass

def plot_skin_arrange(image):
    h = image.shape[0]
    w = image.shape[1]
    NormR = []
    NormG = []
    for y in range(0,h):
        for x in range(0,w):
            # print(image[y,x]) B G R
            pixel = image[y,x]
            channel_sum = pixel[0] + pixel[1]+pixel[2]
            NormR.append(pixel[2] / channel_sum)
            NormG.append(pixel[1] / channel_sum)
            pass
        pass
    pass
    plt.scatter(NormR,NormG)
    plt.show()
pass

# camera = cv2.VideoCapture('memebiboy.mp4')
camera = cv2.VideoCapture(0)

cv2.namedWindow("main")
cv2.setMouseCallback("main", click_and_crop)

if __name__ == "__main__":
    while camera.isOpened():
        ret, frame = camera.read()

        if not ret:
            print('no video')
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = camera.read()

        crcb = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB)

        mask = cv2.inRange(crcb, min_YCrCb, max_YCrCb)
        cv2.imshow("main", frame)

        key = cv2.waitKey(10)
        if key == ord('c'):
            # cropping
            image = frame.copy()
            while True:
                key = cv2.waitKey(10)
                if key == ord('q'):
                    key = None
                    break
                pass
            pass

        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
pass
