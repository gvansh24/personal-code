import cv2
import numpy as np

x = np.zeros([256, 720, 3],dtype=np.uint8)
y = np.zeros([256, 720, 3],dtype=np.uint8)

for row in range(256):
    for col in range(720):
        x[row, col] = (col/4, row, 255)
x = cv2.cvtColor(x, cv2.COLOR_HSV2BGR)

for row in range(256):
    for col in range(720):
        y[row, col] = (col/4, 255, row)
y = cv2.cvtColor(y, cv2.COLOR_HSV2BGR)

while True:

    # cv2.cvtColor(frame,cv2.)
    cv2.imshow("Color 1", x)
    cv2.imshow("Color 2", y)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
