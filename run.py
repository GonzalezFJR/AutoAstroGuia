import SerialReader
import ServoControler
import ObjectFinder
import LaserControler
import LedControler

from SerialReader import GPSread
import time, os, sys

### Create a servo control
print('>> [Initializing] Servo controler...')
servo = ServoControler.ServoControl()

### Create laser controler
print('>> [Initializing] Laser controler...')
laser = LaserControler.Laser()

### Create laser controler
# RED : bluetood not connected - waiting
# GREE: standby - receiving commands
# BLUE: working
print('>> [Initializing] LED controler...')
led = LedControler.Led()
led.Red()

### Get GPS coordinates
print('>> [Initializing] GPS...')
lat, lon, alt, month, day, h, minute, sec, year, utcoffset = [43.36, -5.85, 200, 10, 1, 21, 30, 0, 2021, 2]
gps = GPSread(servoCtrl=servo, led=led, maxtime=120)
lat, lon, alt, month, day, h, minute, sec, year, utcoffset = gps
t0 = time.time()

### Create the object finder
print('>> [Initializing] Object finder...')
o = ObjectFinder.ObjectFinder(lat, lon, alt, month, day, h, minute, sec, year, utcoffset)

# Create a serial reader and command parser
print('>> [Initializing] Serial reader...')
s  = SerialReader.SerialReader(led)
cp = SerialReader.CommandParser()

print('>> [Initializing] Done! Listening...')

#############################################################################################
#############################################################################################

def ResetGPS():
  s.Disconnect()
  gps = GPSread(servoCtrl=servo, led=led, maxtime=180)
  lat, lon, alt, month, day, h, minute, sec, year, utcoffset = gps
  print('Set GPS values to: ')
  print(' >> Latitude  = ', lat)
  print(' >> Longitude = ', lon)
  print(' >> Altitude  = ', alt)
  print(' >> Date      = %i-%i-%i %i:%i:%i'%(day, month, year, h, minute, sec))
  o.SetCoor(lat, lon, alt)
  o.SetTime(day, month, year, h, minute, sec, utcoffset)
  s.Connect()
  cp.command=''

def GetCommand():
  command = {}
  while command == {}:
    command = cp.read(s.read(verbose=False))
  return command

def InterpretCommand(command):
  if command == {}: return
  else:
    print(">> [Command] ", command)
  if 'auto' in command:
    # auto: laserON, laserOFF, GPS
    for c in command['auto']:
      if   c == 'GPS'     : ResetGPS() 
      elif c == 'LASER'   : laser.ChangeStatus() 
      #elif c == 'LASERON' : laser.On()
      #elif c == 'LASEROFF': laser.Off()
  if 'known' in command:
    # known: AZM, ALT, DEC, RA
    if 'ALT' in command['known']: servo.GoToAlt(command['known']['ALT'])
    if 'AZM' in command['known']: servo.GoToAzm(command['known']['AZM'])
    if 'DEC' in command['known'] and 'RA' in command['known']:
      dec = command['known']['DEC']
      ra  = command['known']['RA' ]
      alt, azm = o.ToAltAzm(ra, dec)
      alt, azm = o.TransformCoordinates(alt, azm)
      servo.GoTo(alt, azm)
  if 'arrows' in command:
    # arrows: not yet implemented
    print('Sorry, arrows are not implemented yet...')
    pass
  if 'other' in command:
    # This is the name of an object!
    name = command['other'][0]
    res = o.GetLaserAngleForObj(name)
    if res != None: # Object found!
      alt, azm = res
      servo.GoTo(alt, azm)
    else:
      print('Object "%s" not found!!'%name)
      


##########################################################################
##########################################################################
while 1:
  c = GetCommand()
  InterpretCommand(c)
