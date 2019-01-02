from qbot import QBot
import time
import math
import numpy as np
from GPIO_multi_stepper import *
from distancesensor_28byj import *

################################################################################
#                                                                              #
# Hardware Robot based on Raspberry Pi and 28byj steppers                      #
#   see: https://www.raspberrypi.org/                                          #
#                                                                              #
################################################################################


class QHwBot_28byj(QBot):
    def __init__(self, sensor_sectors=4, turn_sectors=4):
        self.lidar = LidarSensor(sensor_sectors, 360/sensor_sectors)
        self.sensor_sectors = sensor_sectors
        self.turn_sectors = turn_sectors
        self.pins = ((7,11,13,15),(31,33,35,37))
        self.motors = StepperMotors(self.pins, halfStepSequence, 0.0005)

    def move(self, action):
        rotation_degrees = 360/self.turn_sectors               #turns are proportional to turn sectors defined above
        travel_duration = 90                              #forward moves are a 90 degree rotation of both wheels
        if action == 0:
            #go forward
            for i in range(1024):
                self.motors.doStep((1,-1))
        elif action == 1:
            #turn left
            for i in range(1024):
                self.motors.doStep((-1,-1))
        elif action == 2:
            #turn right
            for i in range(1024):
                self.motors.doStep((1,1))

    def get_distance(self):
#        return self.lidar.get_observation()[...,1]
#         obs = [0 for x in range(self.sensor_sectors)]
#         return obs

    def reset(self):
        pass

    def goal(self):
        return 100.0            # millimeters



