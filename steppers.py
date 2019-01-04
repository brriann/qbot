import RPi.GPIO as GPIO
import time
from stepper import Stepper

class Steppers:

    def __init__(self, motors):
        self.motors = motors

    def move(self):
        if self.hasSteps():
            for motor in self.motors:
                motor.doStep()
        time.sleep(Stepper.delay)

    def hasSteps(self):
        for motor in self.motors:
            if motor.hasSteps():
                return True
        return False


GPIO.setmode(GPIO.BOARD)
j = Stepper((19,21,23,24))
k = Stepper((7,11,13,15))
j.setTarget(60)
k.setTarget(30)
x = Steppers((j,k))

while x.hasSteps(): 
    x.move()

GPIO.cleanup()
