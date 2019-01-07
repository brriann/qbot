import RPi.GPIO as GPIO
from time import sleep
from collections import deque

class Stepper:

  halfStepSequence = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1)
  )

  delay = 0.001
  degrees_per_step = 0.0875

  def __init__(self, pins):
    self.pins = pins
    self.dq = deque(Stepper.halfStepSequence)
    for pin in pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)

  def do_step(self):
    if self.has_steps():
      direction = self.get_direction()
      self.dq.rotate(direction)
      for i in range(4):
        GPIO.output(self.pins[i], self.dq[0][i])

class SeekerStepper(Stepper):

  def __init__(self, pins):
    super().__init__(self, pins)
    self.position = 0.0

  def has_steps(self):
    return abs(self.position - self.target) >= Stepper.degrees_per_step

  def get_direction():
    return 1 if self.target >= self.position else -1

  def set_target(self, target):
    a = target % 360
    self.target = a if a <= 180 else a - 360

  def get_position(self):
    return self.position

  def do_step(self):
      super().do_step(self)
      self.position += Stepper.degrees_per_step * direction

class RotateStepper(Stepper):

  def has_steps(self):
    return abs(self.target) >= Stepper.degrees_per_step

  def get_direction():
    return 1 if self.target > 0.0 else -1

  def set_rotation(self, degrees):
    self.target = degrees

  def do_step(self):
      super().do_step(self)
      self.target -= Stepper.degrees_per_step * self.get_direction()
