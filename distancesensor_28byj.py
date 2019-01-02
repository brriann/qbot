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

    def __init__(self, sweep_count = 3, sweep_degrees = 30):
        self.sweep_count = sweep_count
        self.sweep_degrees = sweep_degrees
        self.position = 0.0  # 0 is forward

    def get_reading(self, position):
        self.seek_position(position)
        return self.stepper.position, self.read_distance()

    def read_distance(self):
        distance_in_mm = 0
        self.lidar.start_ranging(3) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
        for n in range(5):
            distance_in_mm += self.lidar.get_distance()
        distance_in_mm /= 5
        self.lidar.stop_ranging() # Stop ranging
        return distance_in_mm

    def get_observation(self):
        observation = []
        target = 0
        for i in range(self.sweep_count):
            observation.append(self.get_reading(target))
            target += self.sweep_degrees
        self.seek_position(0)
        return np.array(observation)

class LidarSensor(DistanceSensor):

    def __init__(self, sweep_count=12, sweep_degrees=30):
        super().__init__(sweep_count, sweep_degrees)
        self.lidar = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.lidar.open() # Initialise the i2c bus and configure the sensor
        self.pins = ((19,21,23,24),)
        self.motors = StepperMotors(self.pins,halfStepSequence, 0.0005)

    def seek_position(self, position):
        print(position)
        current_lidar_pos = self.motors.positions[0]
        # store the position as an integer and it'll never drift
        steps = math.floor((position-current_lidar_pos)/self.motors.degrees_per_step)
        for x in range(steps):
            if position > 0:
                self.motors.doStep(((1),))
            elif position < 0:
                self.motors.dostep(((-1),))
            else:
                pass
        self.position = self.motors.positions[0]
        return self.motors.positions[0]


j = LidarSensor()
print('Seeking 30')
j.seek_position(-30)
time.sleep(1)
print('Seeking 60')
j.seek_position(60)
time.sleep(1)
print('Seeking 90')
j.seek_position(90)
time.sleep(1)
print('Seeking 0')
j.seek_position(0)
time.sleep(1)

