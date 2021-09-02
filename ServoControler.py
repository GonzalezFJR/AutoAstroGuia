import RPi.GPIO as GPIO
import time

'''
 servo1 connected to pin 11
 servo2 connected to pin 12
 The first controls the altitude angle and the second points the azimuth

 Altitude goes from 0 to 180
 Azimuth  goes from -90 to 90
 Calibrate azimuth  with north
 Calibrate altitude with whatever angle

'''

PIN_SERVO_1 = 16
PIN_SERVO_2 = 18

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set servos to their pins
GPIO.setup(PIN_SERVO_1,GPIO.OUT)
GPIO.setup(PIN_SERVO_2,GPIO.OUT)

class ServoControl:
  def __init__(self, pin1=PIN_SERVO_2, pin2=PIN_SERVO_1, verbose=False):
    ''' Initialize servos and angles '''
    self.servo1 = GPIO.PWM(pin1,50) 
    self.servo2 = GPIO.PWM(pin2,50) 
    self.servo1.start(0)
    self.servo2.start(0)
    self.alt0 = 0
    self.alt_last  = 0
    self.azm0 = 0
    self.azm_last  = 0
    self.verbose = verbose
    self.step = 10 # from 0 to 100
    self.slow = True
    self.GoToStandbyPosition()

  def SetStep(self, step=10):
    self.step = step

  def SetVerbose(self, verbose=True):
    ''' Set verbose '''
    self.verbose = verbose

  def SetAlt0(self, alt0=''):
    ''' Calibrate altitude angle '''
    if alt0 == '': alt0 = self.alt_last
    self.alt0 = alt0
    if self.verbose: print('Calibrating altitude angle to %1.2fo'%self.alt0)

  def SetAzm0(self, azm0=''):
    ''' Calibrate azimuth angle... 0 should be north '''
    if azm0 == '': azm0 = self.azm_last
    self.azm0 = azm0
    if self.verbose: print('Calibrating azimuth angle to %1.2fo'%self.azm0)

  def LocalAzimuth(self, ang=0):
    ''' Calculates local (calibrated) values
        Azimuth goes from -90 to 90
    '''
    azm0 = self.azm0
    ang = azm0 + ang
    if ang >  90: ang = ang - 180
    if ang < -90: ang = ang + 180
    return ang

  def LocalAltitude(self, ang=0):
    ''' Calculates local (calibrated) values
        Altitude goes from 0 to 180
    '''
    return self.azm0 + ang

  def GoToAlt(self, alt):
    ''' Change the altitude '''
    oalt = self.LocalAltitude(alt)
    if alt <  10: alt = 10
    if alt > 170: alt = 170
    self.MoveServo(self.servo1, oalt, self.alt_last)
    self.alt_last = alt
    return oalt

  def GoToAzm(self, azm):
    ''' Change the azm '''
    oazm = self.LocalAltitude(azm)
    self.MoveServo(self.servo2, oazm, self.azm_last)
    self.azm_last = azm
    return oazm

  def GoTo(self, alt, azm):
    ''' Moves to alt, azm '''
    self.GoToAlt(alt)
    self.GoToAzm(azm)

  def MoveServo(self, servo, angle, initial_angle):
    if self.slow:
      i = initial_angle
      f = angle
      nextAngle = i
      step = self.step/10 # degrees
      while abs(nextAngle - f) > step:
        sign = ((f-i)/abs(f-i))
        nextAngle = i + step*sign
        servo.ChangeDutyCycle(2+(nextAngle/18))
        i = nextAngle
        time.sleep(0.01)
        servo.ChangeDutyCycle(2+(nextAngle/18))
      servo.ChangeDutyCycle(2+(angle/18))
    else:
      servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.05)
    servo.ChangeDutyCycle(0)

  def GoToAngleRaw(self, alt, azm):
    ''' Input must be in degrees and in correct ranges '''
    self.GoToAlt(alt)
    self.GoToAzm(azm)
    if self.verbose: print('Pointing to [%1.2fo, %1.2fo]'%(alt, azm))

  def GoToAngle(self, alt, azm):
    ''' Input must be in degrees and in correct ranges '''
    azm = azm+90 # azm is introduced between -90 and 90
    self.GoToAngleRaw(alt, azm)

  def Clean(self):
    ''' Clean things up at the end '''
    self.servo1.stop()
    self.servo2.stop()
    GPIO.cleanup()
    print("Finishing servo control")

  ########## Interaction
  def GoToStandbyPosition(self):
    ''' Goes to STANDBY by looking to the zenit '''
    self.GoToAzm(90)
    self.GoToAlt(89)
    time.sleep(0.1)
    self.GoToAlt(91)
    time.sleep(0.1)
    self.GoToAlt(90)

  def SayYes(self):
    ''' Says yes '''
    for i in range(3):
      self.GoToAlt(65)
      time.sleep(0.01)
      self.GoToAlt(40)
      time.sleep(0.1)

  def SayNo(self):
    ''' Says no '''
    self.GoToAlt(90)
    for i in range(3):
      self.GoToAzm(75)
      time.sleep(0.05)
      self.GoToAzm(105)
      time.sleep(0.1)

  ########## Commands
  def MoveArrows(self, arrows):
    ''' Move the servo in given steps according to arrows '''
    pass

if __name__=='__main__':
  servo = ServoControl()
  while(1):
   servo.SayNo()
   time.sleep(1)
   servo.SayYes()
   time.sleep(1)
  
