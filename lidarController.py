from rplidar import RPLidar
from time import time

class LidarController:

    def __init__(self, lidarPort:str='/dev/tty.usbserial-0001'):
        # connect to the Lidar
        self.lidar = RPLidar(lidarPort)

    def getMeasurements(self, startDegree:int, endDegree:int, accuracyFactor:float=1.0) ->list[tuple[float, float]]:
        # Clear input before each scan
        self.lidar.clear_input()

        # check, if the measurements are crossing the degree 0°
        crossesZero = startDegree > endDegree
        if crossesZero:
            measurementsLength = int((360 - startDegree + endDegree) * accuracyFactor)
        else:
            measurementsLength = int((endDegree - startDegree) * accuracyFactor)

        print("Measurement length: %s" %measurementsLength)

        # if crossesZero == True, both of these lists are used
        measurements1 = []
        measurements2 = []
        startTime = time()

        for measurement in self.lidar.iter_measurments():
            # drop the first two entries --> degree and distance remain
            measurement = measurement[2:]
            relevant = self.measurementIsRelevant(measurement[0], startDegree, endDegree)
            if relevant:
                if crossesZero:
                    print(measurement)
                    if startDegree <= measurement[0] <= 360:
                        measurements1.append(measurement)
                    else:
                        measurements2.append(measurement)
                else:
                    measurements1.append(measurement)
            
            # stop the scan as soon as all the values are collected
            if len(measurements1) + len(measurements2) > measurementsLength:
                timeElapsed = time()-startTime
                print("Time Elapsed: %s" %timeElapsed)
                print(len(measurements1))
                print(len(measurements2))
                break
        
        measurements = self.sortCleanAndMergeMeasurements(measurements1, measurements2)
        return measurements

    def measurementIsRelevant(self, degree:float, startDegree:int, endDegree:int) -> bool:
        if startDegree < endDegree:
            # scan does NOT cross the degree 0°
            if startDegree <= degree <= endDegree:
                return True
        else:
            # scan does cross the degree 0°
            if degree >= startDegree or degree <= endDegree:
                return True
        return False
    
    def sortCleanAndMergeMeasurements(self, measurements1:list, measurements2:list) -> list[tuple[float, float]]:
        # delete invalid measurements
        measurements1 = [tup for tup in measurements1 if tup[1] != 0.0]
        measurements2 = [tup for tup in measurements2 if tup[1] != 0.0]

        return sorted(measurements1, key=lambda x: x[0]) + sorted(measurements2, key=lambda x: x[0]) 

    def getMinDistance(self, distances:list) -> tuple[int, int]:
        return min(distances, key=self.getSecondElement)

    def getSecondElement(self, tupleItem:tuple):
        return tupleItem[1]

    def clearLidar(self):
        # cut connection to Lidar
        self.lidar.stop()
        self.lidar.disconnect()


lidar = LidarController()
measurements = lidar.getMeasurements(270, 90, 2)
print(measurements)
print(lidar.getMinDistance(measurements))
lidar.clearLidar()