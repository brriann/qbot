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
    def __init__(self, sensor_sectors=4, turn_sectors=4, sensor_sector_degrees=30):
        GPIO.setmode(GPIO.BOARD)
        self.sensor_sectors = sensor_sectors
        self.turn_sectors = turn_sectors
        self.sensor_sector_degrees = sensor_sector_degrees
        self.stepper1 = Stepper((7,11,13,15))
        self.stepper2 = Stepper((31,33,35,37))
        self.stepper3 = Stepper((19,21,23,24))
        self.motors = Steppers((self.stepper1, self.stepper2, self.stepper3))
        self.lidar = DistanceSensor(self.stepper3)


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
        self.moveMotors()

    def moveMotors(self):
        while self.motors.hasSteps():
            self.motors.move()

    def get_observation(self, sector_count, degrees_per_sector):
        observation = []
        target = -(sector_count-1)//2
        for i in range(self.sensor_sectors):
            observation.append(lidar.get_reading(target))
            target += (degrees_per_sector)
            self.stepper3.setTarget(target)
            self.moveMotors()

    def get_distance(self):
        obs = self.get_observation(self.sensor_sectors, self.sensor_sector_degrees)[...,1]
        return obs

    def reset(self):
        pass

    def goal(self):
        return 100.0            # millimeters



