import RPi.GPIO as GPIO
from time import sleep
from collections import deque

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

class StepperMotors:

  def __init__(self, pin_sets, sequence, delayAfterStep):
    print(pin_sets)
    self.pin_sets = pin_sets
    GPIO.setmode(GPIO.BOARD)
    self.positions = [0 for x in range(len(pin_sets))]
    self.degrees_per_step = 0.0875
    self.dq = [deque(sequence) for i in range(len(pin_sets))]
    for pin_group in self.pin_sets:
      print(pin_group)
      for pin in pin_group:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    self.delayAfterStep = delayAfterStep

  def doStep(self, directions):
    for j, pin_group in enumerate(self.pin_sets):
      self.dq[j].rotate(directions[j])
      for k in range(4):
        GPIO.output(pin_group[k], self.dq[j][0][k])
        self.positions[j] += self.degrees_per_step
    sleep(self.delayAfterStep)

