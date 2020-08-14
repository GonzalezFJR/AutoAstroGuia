'''
  By default, connect laser to pin 16 (eath to pin 14)
'''

LASER_PIN = 16

import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set servos to their pins
GPIO.setup(LASER_PIN,GPIO.OUT)

class Laser:
  def __init__(self):
    self.Off()

  def Off(self):
    GPIO.output(LASER_PIN, GPIO.LOW)

  def OFF(self):
    self.Off()

  def off(self):
    self.Off()

  def On(self):
    GPIO.output(LASER_PIN, GPIO.HIGH)

  def ON(self):
    self.On()

  def on(self):
    self.On()
