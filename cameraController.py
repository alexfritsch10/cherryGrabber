from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
from time import sleep
#import cv2

class CameraController:
    
    def __init__(self, resolution: tuple = (1920, 1088)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.rawCapture = PiRGBArray(self.camera)
        # warm up the camera
        sleep(0.1)
        
    def clearBuffer(self):
        self.rawCapture.truncate(0)
    
    # takes image and optionally crops it
    def takeImage(self, cropToRelevantArea:bool=False) -> np.ndarray:
        self.camera.capture(self.rawCapture, format="bgr")
        if cropToRelevantArea:
            imageThird = int(self.camera.resolution[1] / 3)
            #cv2.imshow("cropped Image", self.rawCapture.array[imageThird:, :])
            #cv2.waitKey()
            return self.rawCapture.array[imageThird:, :]
        return self.rawCapture.array
