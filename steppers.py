import RPi.GPIO as GPIO
import time
from stepper import Stepper

class Steppers:

    def __init__(self, motors):
        self.motors = motors

    def move(self):
        done = False
        while not done:
            done = True                     # speculative
            for motor in self.motors:
                if motor.has_steps():
                    motor.do_step()
                    done = False            # not really done!
            time.sleep(Stepper.delay)
