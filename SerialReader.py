'''
 Class to connect with an android app
 I'm using BlueTooth Serial Controller
 To reset a command, send 'RESET'
 To finish a command, send 'SEND'

 Flechas:
 [ '<-', '-^-', '->', '-V-']

 'RESET', 'SEND'
 self.com_auto = ['LASERON', 'LASEROFF', 'GPS']
 self.com_arrows = ['<-', '-^-', '->', '-V-']
 self.com_known = ['STEP', 'AZM', 'ALT', 'DEC', 'RA']
 9+16
 M, NGC, IC, HD

'''

import serial
import time, datetime
import os, sys
import pytz

timezone = "Europe/Madrid"
utc_offset = int(datetime.datetime.now(pytz.timezone(timezone)).strftime('%z').replace('0',    ''))

serialName = '/dev/rfcomm0'
timeSleep = 0.001
resetCommandKey = 'RESET'
endCommandKey = 'SEND'

class SerialReader:
  def __init__(self, led=None):
    self.led = led
    if self.led!=None: self.led.Red()
    self.initialize()
    self.t0 = time.time()

  def initialize(self):
    self.ser = ''
    while(self.ser == ''):
      self.connect()
      time.sleep(0.5)

  def connect(self):
    #if int(time.time()-self.t0) % 10 == 0:
    #  self.ser
    try:
      if self.ser == '': self.ser = serial.Serial(serialName,9600,timeout=1)
    except:
      #if self.led!=None: self.led.Red()
      print('Cannot link with app. Waiting...')
      self.led.redblink()
    if self.ser!='':
      try:
        line = self.ser.readline().decode("utf-8")
      except:
        print('Closing serial port...')
        self.ser.close()
        if self.led!=None: self.led.Red()

  def read(self, tmax=5, verbose=0):
    t0 = time.time()
    if verbose: print('reading...')
    line = ''
    while line == '' and (time.time()-t0) < tmax:
      time.sleep(timeSleep)
      try:
        line = self.ser.readline().decode("utf-8")
        line = line.replace(' ', '')
        if self.led!=None: self.led.Green()
      except:
        self.initialize()
    if verbose: print('[command] = ', line)
    if self.led!=None: self.led.Blue()
    return line 

  def Disconnect(self):
    if self.ser != '': self.ser.close()

  def Connect(self):
    if self.ser != '': self.ser.open()

##################################################################
### GPS reader
import pynmea2, time

def GPSread(servoCtrl=None, led=None, verbose=False, maxtime=60):
  if servoCtrl != None: servoCtrl.GoToStandbyPosition()
  s = SerialReader(led=led)
  phrase = ''
  t0 = time.time()
  lat, lon, alt, d = [0, 0, 0, 0]
  #while not (phrase.startswith('$GPRMC,') and (not ',,' in phrase) and (phrase.count(',')>=12)) or not (phrase.startswith('$GPGGA,') and phrase.count(',') >= 14):
  led.blueblink()
  while (lat==0) or (lon==0) or (alt==0) or (d==0):
    t = time.time()-t0
    last_ti = 0
    ti = int(t)
    if not led is None: led.blueblink()
    if ti > last_ti:
      print('     > [%i s] waiting for GPS... (max time = %i s)'%(ti, maxtime))
      last_ti = ti
    if t > maxtime: 
      print('     > GPS NOT FOUND!! ')
      break
    r = s.read()
    phrase = r 
    if not isinstance(phrase, list): phrase = [phrase]
    for pr in phrase:
      if not (pr.startswith('$GPRMC,') or pr.startswith('$GPGGA,')): continue
      p = pynmea2.parse(pr)
      if pr.startswith('$GPRMC'):
        if pr.count(',,') > 1: continue
        if hasattr(p, 'latitude'):  lat = p.latitude
        if hasattr(p, 'longitude'): lon = p.longitude
        if hasattr(p, 'datetime'):  d = p.datetime
      else:
        if pr.count(',,') > 2: continue
        if hasattr(p, 'altitude'): alt = p.altitude
  print('      > GPS OK!')
  print('      > Latitude    ', lat)
  print('      > Longitude   ', lon)
  print('      > Altitude    ', alt)
  print('      > Date        ', d)
  print('      > UTC offset  ', utc_offset)
  if (lat==0) or (lon==0) or (alt==0) or (d==0):
    print('ERROR: could not connect to GPS!')
    if d == 0: d = datetime.datetime(2020,9,1,0,0,0)
    if servoCtrl != None: servoCtrl.SayNo()
  elif servoCtrl != None: servoCtrl.SayYes()
  s.Disconnect()
  return [lat, lon, alt, d.month, d.day, d.hour, d.minute, d.second, d.year, utc_offset]
  #lat, lon, alt, month, day, h, minute, sec, year, utcoffset = GPSreader()


##################################################################
###

class CommandParser:

  def __init__(self):
    self.command = ''
    self.com_auto = ['LASER', 'GPS']
    #self.com_auto = ['LASERON', 'LASEROFF', 'GPS']
    self.com_arrows = ['<-', '-^-', '->', '-V-']
    self.com_known = ['STEP', 'AZM', 'ALT', 'DEC', 'RA']
    self.reset = resetCommandKey
    self.endcom = endCommandKey
    self.ResetValues()

  def ResetValues(self):
    self.arrows = []
    self.known = {}
    self.other = []
    self.auto = []

  def GetDic(self):
    outdic = {}
    if self.arrows != []: outdic['arrows'] = self.arrows
    if self.auto   != []: outdic['auto']   = self.auto
    if self.known  != {}: outdic['known']  = self.known
    if self.other  != []: outdic['other']  = self.other
    return outdic
    
  def read(self, c):
    self.command += c
    if self.reset in self.command: self.command = self.command[self.command.index(self.reset)+len(self.reset):]
    return self.process()

  def process(self):
    self.GetArrows()
    self.GetAutoCommands()
    self.GetKnownCommands()
    outdic = self.GetDic()
    self.ResetValues()
    return outdic

  def GetArrows(self):
    ''' Command must be a string '''
    for a in self.com_arrows: 
      n = self.command.count(a)
      for i in range(n): self.arrows.append(a)
      self.command = self.command.replace(a, '')

  def GetAutoCommands(self):
    ''' Command must be a string '''
    for a in self.com_auto: 
      n = self.command.count(a)
      for i in range(n): self.auto.append(a)
      self.command = self.command.replace(a, '')

  def GetKnownCommands(self):
    if not self.endcom in self.command: return
    else:
      command = self.command[:self.command.index(self.endcom)]
      self.command = self.command[self.command.index(self.endcom)+len(self.endcom):]
    while self.IsValueKnownCommand(command):
      k = self.IsValueKnownCommand(command)
      val, command = self.SearchForValue(k, command)
      self.known[k] = val
    if command != '': self.other.append(command)

  def IsValueKnownCommand(self, command):
    ''' Command must be a string '''
    for k in self.com_known:
      if k in command: return k
    return False

  def SearchForValue(self, k, command):
    ''' For example, command = "M55STEP4.5", k = "STEP"... returns [4.5, "M55"] '''
    other = ''; val = ''
    precommand = command[:command.index(k)]
    if precommand != '': other += (precommand)
    postcommand = command[command.index(k)+len(k):]
    for c in postcommand:
      if c.isdigit() or c=='.': val += c
      else: break
    postcommand = postcommand[len(val):]
    val = float(val) if val != '' else 0
    if postcommand != '': other += (postcommand)
    return val, other

if __name__=='__main__':
  s  = SerialReader()
  cp = CommandParser()
  fullcommands = {}
  while True:
    fullcommands = cp.read(s.read(False))
    if fullcommands != {}: print(fullcommands)
