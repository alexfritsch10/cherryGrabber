from motorController import MotorController
from cameraController import CameraController
from sonicController import SonicController
from utils import calculateNextCommand, logCommand
from cherryFinder import CherryFinder

motors = MotorController()
print("Motor Setup Complete")
camera = CameraController()
print("Camera Setup Complete")
sonic = SonicController()
print("Sonic Setup Complete")
cherryFinder = CherryFinder()

# if this is set to True, the image will be cropped to the
# lower two thirds. This is an optional optimization, because
# the cherries will never be in the upper third (cherries 
# are on camera level) 
cropImage = True

while(True):
    
    image = camera.takeImage(cropImage)
    
     # prepare camera for next image
    camera.clearBuffer()
    
    # detect cherry on image
    found, xCoordCherry = cherryFinder.find(image)
    
    if found:
        currentSpeed = motors.currentSpeed
        distance = sonic.calculateDistance()
        imageWidth = camera.camera.resolution[0]
        command, angle = calculateNextCommand(currentSpeed, distance, imageWidth, xCoordCherry)
        logCommand(command, angle)
        
        if command == "forward":
            motors.forward()
        elif command == "stop":
            motors.stop()
        elif command == "steer":
            motors.steer(angle)
        elif command == "collect":
            # this should activate the vacuum motor
            continue
    else:
        motors.detect()
        
    

    