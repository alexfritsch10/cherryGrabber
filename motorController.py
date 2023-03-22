import RPi.GPIO as GPIO          
from time import sleep

class MotorController:
    def __init__(self, hz:int=1000):
        
        # frquenzy for the motor operation
        self.hz = hz
        
        # setup right motor
        self.in1_1 = 24
        self.in1_2 = 23
        self.en1 = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1_1,GPIO.OUT)
        GPIO.setup(self.in1_2,GPIO.OUT)
        GPIO.setup(self.en1,GPIO.OUT)
        GPIO.output(self.in1_1,GPIO.LOW)
        GPIO.output(self.in1_2,GPIO.LOW)
        self.p1 = GPIO.PWM(self.en1, self.hz)
        self.p1.start(15)

        # setup left motor
        self.in2_1 = 17
        self.in2_2 = 27
        self.en2 = 22

        GPIO.setup(self.in2_1,GPIO.OUT)
        GPIO.setup(self.in2_2,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)
        GPIO.output(self.in2_1,GPIO.LOW)
        GPIO.output(self.in2_2,GPIO.LOW)
        self.p2=GPIO.PWM(self.en2, self.hz)
        self.p2.start(15)
        self.currentSpeed = 15

    def forward(self):
        print("forward with both motors")
        GPIO.output(self.in1_1,GPIO.LOW)
        GPIO.output(self.in1_2,GPIO.HIGH)
        
        GPIO.output(self.in2_1,GPIO.LOW)
        GPIO.output(self.in2_2,GPIO.HIGH)
        self.currentSpeed = 15
    
    def backard(self):
        print("Backward with both motors")
        GPIO.output(self.in1_1,GPIO.HIGH)
        GPIO.output(self.in1_2,GPIO.LOW)
        
        GPIO.output(self.in2_1,GPIO.HIGH)
        GPIO.output(self.in2_2,GPIO.LOW)
        self.currentSpeed = 15
    
    def stop(self):
        print("Stop both motors")
        GPIO.output(self.in1_1,GPIO.LOW)
        GPIO.output(self.in1_2,GPIO.LOW)
        
        GPIO.output(self.in2_1,GPIO.LOW)
        GPIO.output(self.in2_2,GPIO.LOW)
        self.currentSpeed = 0
             
    def steer(self, angle:int):
        print("Steering")
        # the angle can't be 0
        if angle == 0:
            return
        
        # calculate the steering time, based on the steering angle
        steerTime = abs(angle) * 0.05

        if angle > 0:
            # steer right by speeding up the left motor 
            self.p2.ChangeDutyCycle(self.currentSpeed + 5)
            sleep(steerTime)
            self.p2.ChangeDutyCycle(self.currentSpeed)
        else:
            # steer left by speeding up the right motor 
            self.p1.ChangeDutyCycle(self.currentSpeed + 5)
            sleep(steerTime)
            self.p1.ChangeDutyCycle(self.currentSpeed)


    # changes orientation of the robot, by turning both wheels in different directions 
    def detect(self):
        print("Detecting")
        # left motor backward
        GPIO.output(self.in1_1,GPIO.LOW)
        GPIO.output(self.in1_2,GPIO.HIGH)
        self.p1.ChangeDutyCycle(30)
        
        # right motor forward
        GPIO.output(self.in2_1,GPIO.HIGH)
        GPIO.output(self.in2_2,GPIO.LOW)
        self.p2.ChangeDutyCycle(30)

        sleep(0.4)
        
        # stop both motors
        self.stop()
