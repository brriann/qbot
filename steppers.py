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


