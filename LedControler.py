'''
  By default, connect laser to pin 16 (eath to pin 14)
'''

pRED  = 11
pGREEN= 13
pBLUE = 15

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
    self.isOff = True
    self.Off()
    self.Blink(False)

  def Blink(self, do=True):
    self.blink = do

  def Off(self):
    GPIO.output(pRED,   GPIO.LOW)
    GPIO.output(pBLUE,  GPIO.LOW)
    GPIO.output(pGREEN, GPIO.LOW)
    self.isOff = True

  def IsOn(self):
    self.isOff = False

  def Blue(self):
    self.Off()
    GPIO.output(pBLUE,  GPIO.HIGH)
    self.IsOn()

  def Red(self):
    self.Off()
    GPIO.output(pRED,  GPIO.HIGH)
    self.IsOn()

  def Green(self):
    self.Off()
    GPIO.output(pGREEN,  GPIO.HIGH)
    self.IsOn()

  def White(self):
    self.Off()
    GPIO.output(pRED,  GPIO.HIGH)
    GPIO.output(pGREEN,GPIO.HIGH)
    GPIO.output(pBLUE, GPIO.HIGH)
    self.IsOn()

  def blueblink(self):
    if self.isOff: self.Blue()
    else: self.Off()

  def redblink(self):
    if self.isOff: self.Red()
    else: self.Off()


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
