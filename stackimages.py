import cv2
import numpy as np

def stack(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0]) if isinstance(imgArray[0], list) else 1
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1] if rowsAvailable else imgArray[0].shape[1]
    height = imgArray[0][0].shape[0] if rowsAvailable else imgArray[0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                img = imgArray[x][y]
                if img.shape[:2] != (height, width):
                    imgArray[x][y] = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                if len(img.shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
        hor = [np.hstack(imgArray[x]) for x in range(rows)]
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            img = imgArray[x]
            if img.shape[:2] != (height, width):
                imgArray[x] = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
            if len(img.shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
        ver = np.hstack(imgArray)
    return ver
