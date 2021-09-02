'''
  By default, connect laser to pin 16 (eath to pin 14)
'''

LASER_PIN = 7

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set laser to its pin
GPIO.setup(LASER_PIN,GPIO.OUT)

class Laser:
  def __init__(self):
    self.Off()
    self.status = 0

  def Off(self):
    GPIO.output(LASER_PIN, GPIO.LOW)
    self.status = 0

  def OFF(self):
    self.Off()

  def off(self):
    self.Off()

  def On(self):
    GPIO.output(LASER_PIN, GPIO.HIGH)
    self.status = 1

  def ON(self):
    self.On()

  def on(self):
    self.On()

  def ChangeStatus(self):
    self.Off() if self.status else self.On()

if __name__=='__main__':
  l = Laser()
  while 1:
    l.On()
    time.sleep(1)
    l.Off()
    time.sleep(1)
