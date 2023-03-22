import RPi.GPIO as GPIO
import time

class SonicController:
    
    def __init__(self):
        print("Got initialized")
        self.trigger = 26
        self.echo = 16
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trigger, GPIO.LOW) 

    def calculateDistance(self):
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)
        while GPIO.input(self.echo)==0: 

            start_time = time.time() 

        while GPIO.input(self.echo)==1: 

            Bounce_back_time = time.time() 

        pulse_duration = Bounce_back_time - start_time 

        distance = round(pulse_duration * 17150, 2) 

        print (f"Distance: {distance} cm")
        
        return distance
        
        
#getter = SonicController()
#getter.calculateDistance()