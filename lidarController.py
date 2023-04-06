from rplidar import RPLidar


class LidarController:

    def __init__(self, lidarPort:str='/dev/tty.usbserial-0001'):
        # connect to the Lidar
        self.lidar = RPLidar(lidarPort)

    def getDistances(self, startAngle:int=270, endAngle:int=90):
        # Clear input before each scan
        self.lidar.clear_input()

        # look at one scan and remove 'quality' entry in tuples
        reducedScan = []
        for scan in self.lidar.iter_scans():  
            reducedScan = [element[1:] for element in scan]
            break

        
        # measurements per 360° Scan: 193
        degreeDelta = 360/len(reducedScan)

        if startAngle < endAngle:
            # in this case, the list does not cross the 0
            startIdx = int(startAngle / degreeDelta)
            endIdx = int(endAngle / degreeDelta)
            print(startIdx)
            print(endIdx)
            print(reducedScan)

            return reducedScan[startIdx:endIdx]
        else:
            # is this case, the list crosses the 0
            scansLeft = int((360 - startAngle)/degreeDelta)
            scansRight = int(endAngle/degreeDelta) 

            startToZero = reducedScan[-scansLeft:]
            zeroToEnd = reducedScan[:scansRight]

            return startToZero + zeroToEnd

    def getMinDistance(self, distances:list) -> tuple[int, int]:
        return min(distances, key=self.getSecondElement)

    def getSecondElement(self, tupleItem:tuple):
        return tupleItem[1]

    def clearLidar(self):
        # cut connection to Lidar
        self.lidar.stop()
        self.lidar.disconnect()



lidar = LidarController()
print(lidar.getDistances(10, 15))
lidar.clearLidar()