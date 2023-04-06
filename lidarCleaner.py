from rplidar import RPLidar

lidar = RPLidar('/dev/tty.usbserial-0001')
lidar.clear_input()

# Receive Data and print it
try:
    for i, scan in enumerate(lidar.iter_scans()):  # Loop through the Scans
        print(len(scan))
except KeyboardInterrupt:
    pass

# cut connection to Lidar
lidar.stop()
lidar.disconnect()