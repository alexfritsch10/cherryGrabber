import RPi.GPIO as GPIO          

# this is a script to stop both motors in case of an emergency

GPIO.setmode(GPIO.BCM)

# stop right motor
in1_1 = 24
in1_2 = 23

GPIO.setup(in1_1,GPIO.OUT)
GPIO.setup(in1_2,GPIO.OUT)
GPIO.output(in1_1,GPIO.LOW)
GPIO.output(in1_2,GPIO.LOW)

# stop left motor
in2_1 = 17
in2_2 = 27

GPIO.setup(in2_1,GPIO.OUT)
GPIO.setup(in2_2,GPIO.OUT)
GPIO.output(in2_1,GPIO.LOW)
GPIO.output(in2_2,GPIO.LOW)






