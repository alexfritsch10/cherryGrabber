# This is the function, where the Maneuvering logic is happening.
# The returned string is the command. Since this function is
# only called, when a cherry is detected, the only reasonable
# returned commands are "forward", "stop", "steer" and "collect".
# Only if the command is "steer", the returned int is relevant
def calculateNextCommand(currentSpeed:int, distance:float, imageWidth:int, xCoordCherry:float) -> tuple(str, int):
    # field of view of the Raspberry Pi Camera Module V1 
    cameraFieldOfView = 53
    
    # calculate the distance between the cherry and the center
    horizontalDeviationPixel = xCoordCherry - (imageWidth/2)
    # convert this distance into a offshit degree
    horizontalDeviationDegree = int(horizontalDeviationPixel / (imageWidth/cameraFieldOfView))

    # determine the next command, based on the speed, the 
    # distance to the next obstacle and the offshit degree
    if currentSpeed == 0:
        if distance > 20:
            return "forward", 0
        else:
            return "collect", 0
    else:
        if distance <= 20:
            return "stop", 0
        else:
            if abs(horizontalDeviationDegree) > 5:
                return "steer", horizontalDeviationDegree
            else:
                return "forward", 0
    
# this method is used to append the command to a txt file
def logCommand(command: str, angle: int):
    logFile = open('commands.txt', 'a')
    logFile.write(command + ', ' + str(angle) + '\n')
    logFile.close()
    
    