import cv2
import numpy as np
import imutils

class CherryFinder():
    
    def __init__(self):
        # define the red spectrum of the cherries
        self.lowerRed = np.array([160,100,80])
        self.upperRed = np.array([179,255,255])

        # count the amount of analysed images
        self.imageNumber = 0
        
    # tries to find the cherry on the image. Returns (True, x Coordinate of the cherry)
    # if it could find one, or (False, 0) if not 
    def find(self, image:np.ndarray) -> tuple(bool, float):
        self.imageNumber += 1
                
        # preprocess the image
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "red", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.lowerRed, self.upperRed)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # x coordinate of the center
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            xCoord = int(M["m10"] / M["m00"])

            # only proceed if the radius meets a minimum size
            if radius > 5:
                # draw the circle on the frame,
                cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

                # every time a cherry is detected, it stores the image locally
                fileName = str(self.imageNumber) + ".jpg"  
                cv2.imwrite(fileName, image)

                return True, xCoord
        return False, 0
