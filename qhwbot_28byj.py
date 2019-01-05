from qbot import QBot
import time
import math
import numpy as np
import RPi.GPIO as GPIO
from stepper import Stepper
from steppers import Steppers
from distancesensor_28byj import *

################################################################################
#                                                                              #
# Hardware Robot based on Raspberry Pi and 28byj steppers                      #
#   see: https://www.raspberrypi.org/                                          #
#                                                                              #
################################################################################


class QHwBot_28byj(QBot):
    def __init__(self, sensor_sectors=4, turn_sectors=4):
        GPIO.setmode(GPIO.BOARD)
        self.lidar = DistanceSensor()
        self.sensor_sectors = sensor_sectors
        self.turn_sectors = turn_sectors
        self.stepper1 = Stepper((7,11,13,15))
        self.stepper2 = Stepper((31,33,35,37))
        self.motors = Steppers((self.stepper1, self.stepper2))

    def move(self, action):
        rotation_degrees = 360/self.turn_sectors               #turns are proportional to turn sectors defined above
        travel_duration = 90                              #forward moves are a 90 degree rotation of both wheels
        if action == 0:
            #go forward
            self.stepper1.setTarget(self.stepper1.getPosition()+rotation_degrees)
            self.stepper2.setTarget(self.stepper2.getPosition()-rotation_degrees)
        elif action == 1:
            #turn left
            self.stepper1.setTarget(self.stepper1.getPosition()+rotation_degrees)
            self.stepper2.setTarget(self.stepper2.getPosition()+rotation_degrees)
        elif action == 2:
            #turn right
            self.stepper1.setTarget(self.stepper1.getPosition()-rotation_degrees)
            self.stepper2.setTarget(self.stepper2.getPosition()-rotation_degrees)
        while self.motors.hasSteps():
            self.motors.move()

    def get_distance(self):
        obs = self.lidar.get_observation(self.sensor_sectors, 360/self.sensor_sectors)[...,1]
        return obs

    def reset(self):
        pass

    def goal(self):
        return 100.0            # millimeters



