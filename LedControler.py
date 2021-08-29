'''
  By default, connect laser to pin 16 (eath to pin 14)
'''

pRED  = 31
pGREEN= 33
pBLUE = 35

import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Set servos to their pins
GPIO.setup(pRED  ,GPIO.OUT)
GPIO.setup(pGREEN,GPIO.OUT)
GPIO.setup(pBLUE ,GPIO.OUT)

class Led:
  def __init__(self):
    self.Off()
    self.Blink(False)

  def Blink(self, do=True):
    self.blink = do

  def Off(self):
    GPIO.output(pRED,   GPIO.LOW)
    GPIO.output(pBLUE,  GPIO.LOW)
    GPIO.output(pGREEN, GPIO.LOW)

  def Blue(self):
    self.Off()
    GPIO.output(pBLUE,  GPIO.HIGH)

  def Red(self):
    self.Off()
    GPIO.output(pRED,  GPIO.HIGH)

  def Green(self):
    self.Off()
    GPIO.output(pGREEN,  GPIO.HIGH)

  def White(self):
    self.Off()
    GPIO.output(pRED,  GPIO.HIGH)
    GPIO.output(pGREEN,GPIO.HIGH)
    GPIO.output(pBLUE, GPIO.HIGH)


if __name__=='__main__':
  l = Led()
  while 1:
    l.Off()
    time.sleep(1)
    l.Blue()
    time.sleep(1)
    l.Red()
    time.sleep(1)
    l.Green()
    time.sleep(1)
