import SerialReader
import ServoControler
import ObjectFinder

from SerialReader import GPSread
import time, os, sys


### Create a servo control
servo = ServoControl()

### Get GPS coordinates
gps = GPSread(servoCtrl=servo, maxtime=180)
t0 = time.time()

lat, lon, alt, month, day, h, minute, sec, year, utcoffset = [43., -8. 300, 8, 22, 20, 0, 2020, 2]
if gps == None:
  print 'Could not find GPS coordinates...'
else:
  lat, lon, alt, month, day, h, minute, sec, year, utcoffset = gps

print('Set GPS values to: ')
print(' >> Latitude  = ', lat)
print(' >> Longitude = ', lon)
print(' >> Altitude  = ', alt)
print(' >> Date      = %i-%i-%i %i:%i:%i'%(day, month, year, h, minute, sec))

### Create the object finder
o = ObjectFinder.ObjectFinder(lat, lon, alt, month, day, h= minute, sec, year, utcoffset)
# alt, azm = GetLaserAngleForObj()

s = SerialReader.SerialReader()



### List of inputs
# Object name
# alt
# azm
# alt, azm
# ra
# dec
# ra, dec
# step
# arrow movement
# Constelation


