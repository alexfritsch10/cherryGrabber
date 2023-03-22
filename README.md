# cherryGrabber

This robot is able to detect cherries (red foam balls with a diameter of around 3cm) in it's environment. After it detects a cherry, it drives up to it and stops in front of it with a distance of around 15cm. 

## Prerequisites
Make sure to have Python installed (at least version 3.7). Connect the Raspberry Pi Camera Module (Version 1 or Version 2). Then connect the motors and sensors and shown here:

![alt text](https://github.com/alexfritsch10/cherryGrabber/blob/main/images/circuits.svg?raw=true)

## Project Setup
```
git clone https://github.com/alexfritsch10/cherryGrabber.git
cd cherryGrabber
pip3 install requirements.txt

```

## Run the robot 

```
python3 robot.py
```