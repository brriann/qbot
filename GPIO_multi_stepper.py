import RPi.GPIO as GPIO
from time import sleep
from collections import deque

class StepperMotors:
  
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

  def __init__(self, pin_sets):
    self.pin_sets = pin_sets
    GPIO.setmode(GPIO.BOARD)
    self.positions = [0 for x in range(len(pin_sets))]
    self.degrees_per_step = 0.0875
    self.dq = [deque(StepperMotors.halfStepSequence) for i in range(len(pin_sets))]
    for pin_group in self.pin_sets:
      for pin in pin_group:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

  def doStep(self, directions):
    for j, pin_group in enumerate(self.pin_sets):
      self.dq[j].rotate(directions[j])
      for k in range(4):
        GPIO.output(pin_group[k], self.dq[j][0][k])
        self.positions[j] += self.degrees_per_step * directions[j]
    sleep(StepperMotors.delay)

