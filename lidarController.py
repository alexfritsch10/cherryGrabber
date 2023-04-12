from rplidar import RPLidar
from time import time

class LidarController:

    def __init__(self, lidarPort:str='/dev/tty.usbserial-0001'):
        # connect to the Lidar
        self.lidar = RPLidar(lidarPort)

    def getMeasurements(self, startDegree:int, endDegree:int, timeLimit:float=1.0) ->list[tuple[float, float]]:
        # possiblity to limit the time of a scan
        startTime = time()
        
        # Clear input before each scan
        self.lidar.clear_input()

        measurements = []

        for measurement in self.lidar.iter_measurments():
            # drop the first two entries --> degree and distance remain
            measurement = measurement[2:]

            # check if the measurement is in desired range
            relevant = self.measurementIsRelevant(measurement[0], startDegree, endDegree)
            if relevant:
                measurements.append(measurement)

            # stop the scan as soon as time limit is reached
            if time() - startTime >= timeLimit:
                print("Time Limit Reached")
                break
        
        measurements = self.cleanAndSortMeasurements(measurements)
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
    
    def cleanAndSortMeasurements(self, measurements:list) -> list[tuple[float, float]]:
        # delete invalid measurements
        measurements = [tup for tup in measurements if tup[1] != 0.0]

        return sorted(measurements, key=lambda x: x[0]) 

    def getDegreeForMinDistance(self, distances:list) -> tuple[int, int]:
        return min(distances, key=self.getSecondElement)

    def getSecondElement(self, tupleItem:tuple) -> float:
        return tupleItem[1]

    def clearLidar(self) -> None:
        # cut connection to Lidar
        self.lidar.stop()
        self.lidar.disconnect()


lidar = LidarController()
measurements = lidar.getMeasurements(270, 90)
print(measurements)
print(lidar.getMinDistance(measurements))
lidar.clearLidar()