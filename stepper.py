import RPi.GPIO as GPIO
from time import sleep
from collections import deque

class Stepper:

  HALF_STEP_SEQUENCE = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1)
  )
  CW = 1
  CCW = -1

  delay = 0.0009
  degrees_per_step = 0.0875

  def __init__(self, pins, orientation=CW):
    self.orientation = orientation
    self.target = 0
    self.pins = pins
    self.dq = deque(Stepper.HALF_STEP_SEQUENCE)
    for pin in pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)

  def do_step(self):
    if self.has_steps():
      direction = self.get_direction()
      self.dq.rotate(direction * self.orientation)   # Steppers rotate CCW :/
      for i in range(4):
        GPIO.output(self.pins[i], self.dq[0][i])

class SeekerStepper(Stepper):

  def __init__(self, pins, orientation=Stepper.CW):
    super().__init__(pins, orientation)
    self.position = 0.0

  def has_steps(self):
    return abs(self.position - self.target) >= Stepper.degrees_per_step

  def get_direction(self):
    return 1 if self.target >= self.position else -1

  def set_target(self, target):
    a = target % 360
    self.target = a if a <= 180 else a - 360

  def get_position(self):
    return self.position

  def do_step(self):
      super().do_step()
      self.position += Stepper.degrees_per_step * self.get_direction()

class RotateStepper(Stepper):

  def has_steps(self):
    return abs(self.target) >= Stepper.degrees_per_step

  def get_direction(self):
    return 1 if self.target > 0.0 else -1

  def set_target(self, degrees):
    self.target = degrees

  def do_step(self):
      super().do_step()
      self.target -= Stepper.degrees_per_step * self.get_direction()
