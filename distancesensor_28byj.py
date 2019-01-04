from GPIO_multi_stepper import *
import numpy as np
import VL53L1X
import math
import time

################################################################################
#                                                                              #
# Distance Sensor using SparkFun                                               #
#   see: https://www.sparkfun.com/products/14722                               #
#                                                                              #
################################################################################

class DistanceSensor:
    
    pins = (19,21,23,24)

    def __init__(self):
        self.position = 0.0  # 0 is forward
        self.lidar = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.lidar.open() # Initialise the i2c bus and configure the sensor
        self.motors = StepperMotors((DistanceSensor.pins,))  # ...a list of pin sets, of length 1 (only 1 motor)

    def get_reading(self, position):
        self.seek_position(position)
        return self.get_position(), self.read_distance()

    def read_distance(self):
        distance_in_mm = 0
        self.lidar.start_ranging(3) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
        for n in range(5):
            distance_in_mm += self.lidar.get_distance()
        distance_in_mm /= 5.0
        self.lidar.stop_ranging() # Stop ranging
        return distance_in_mm

    def get_observation(self, count, degrees):
        observation = []
        target = 0
        for i in range(self.sweep_count):
            observation.append(self.get_reading(target))
            target += self.sweep_degrees
        self.seek_position(0)
        return np.array(observation)

    def get_position(self):
        return self.motors.positions[0]
    
    def seek_position(self, position):
        # store the position as an integer and it'll never drift
        steps = math.floor((position-self.get_position())/self.motors.degrees_per_step)
        direction = 1 if steps > 1 else -1
        for x in range(abs(steps)):
            self.motors.doStep(((direction),))

j = LidarSensor()
j.seek_position(30)
j.seek_position(-30)
j.seek_position(0)

