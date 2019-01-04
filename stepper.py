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
  
  delay = 0.0005
  degrees_per_step = 0.0875

  def __init__(self, pins):
    self.pins = pins
    self.position = 0.0
    self.target = None
    self.dq = deque(Stepper.halfStepSequence)
    for pin in pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)

  def setTarget(self, target):
    self.target = target % 180 - 180 if target >= 0 else target % -180 + 180

  def hasSteps(self):
    print(self.position, self.target, abs(self.position-self.target), Stepper.degrees_per_step)
    return abs(self.position - self.target) >= Stepper.degrees_per_step

  def doStep(self):
    if self.hasSteps():
      direction = 1 if self.target >= self.position else -1  # backwards? ...not sure
      self.dq.rotate(direction)
      for i in range(4):
        GPIO.output(self.pins[i], self.dq[0][i])
      self.position += Stepper.degrees_per_step * direction

