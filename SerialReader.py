'''
 Class to connect with an android app
 I'm using BlueTooth Serial Controller
 To reset a command, send 'START'
 To finish a command, send 'SEND'
'''

import serial
import time
import os, sys

serialName = '/dev/rfcomm0'
timeSleep = 0.001
resetCommandKey = 'START'
endCommandKey = 'SEND'
keywords = [ '<-', '-^-', '->', '-V-']

class SerialReader:
  def __init__(self):
    self.initialize()

  def initialize(self):
    self.ser = ''
    while(self.ser == ''):
      self.connect()
      time.sleep(0.5)

  def connect(self):
    try:
      self.ser = serial.Serial(serialName,9600,timeout=1)
      line = self.ser.readline().decode("utf-8")
    except:
      self.ser = ''
      print('Cannot link with app. Waiting...')

  def read(self, verbose=0):
    if verbose: print('reading...')
    command = ''
    line = ''
    while line == '':
    time.sleep(timeSleep)
      try:
        line = self.ser.readline().decode("utf-8")
        line = line.replace(' ', '')
      except:
        self.initialize()
    if verbose: print('[command] = ', command)
    return command

  '''
  def read(self, verbose=0):
    print('reading...')
    command = ''
    line = ''
    while line != endCommandKey:
      time.sleep(timeSleep)
      try:
        line = self.ser.readline().decode("utf-8")
      except:
        self.initialize()
      if verbose: print('[reading] : ', line)

      if ',' in line: 
        if line.endswith(','): line = line[:-1]
        lines = line.split(',')
        arrowSignal = [command]
        for l in lines:
          if l in keywords: arrowSignal.append(l)
        return lines

      if   line == resetCommandKey: command = ''
      elif line == endCommandKey: pass
      else                : 
        command+=line
        if command.endswith(endCommandKey): line = endCommandKey
    while command.endswith(endCommandKey): command = command[:-4]
    if verbose: print('[command] = ', command)
    return command
  '''

##################################################################
### GPS reader
import pynmea2, time

def GPSread(servoCtrl=None, verbose=False, maxtime=60):
  s = SerialReader(verbose=verbose)
  phrase = ''
  t0 = time.time()
  while not phrase.startswith('$GPRMC'):
    phrase = ''
    t = time.time()-t0
    if t > maxtime: break
    r = s.read()
    phrase = r 
    if isinstance(phrase, list) and len(phrase) == 1: phrase = phrase[0]
  if phrase == '':
    print('Unable to connect... returning None')
    return None
  p = pynmea2.parse(phrase)
  lat = p.latitude
  lon = p.longitude
  alt = 200#p.altitude
  d = p.datetime
  if verbose:
    print('Latitude  = ', lat)
    print('Longitude = ', lon)
    print('Altitude  = ', alt)
    print('Date      = ', d)
  return [lat, lon, alt, d.month, d.day, d.hour, d.minute, d.second, d.year, 0]
  #lat, lon, alt, month, day, h, minute, sec, year, utcoffset = GPSreader()


##################################################################
###
def GetArrows(command):
  ''' Command must be a string '''
  arrows   = ['<-', '-^-', '->', '-V-']
  arr = []
  for a in arrows: 
    n = command.count(a)
    for i in range(n): arr.append(a)
    command = command.replace(a, '')
  return arr, command

def IsValueCommand(command):
  ''' Command must be a string '''
  keywords = ['STEP', 'AZM', 'ALT', 'DEC', 'RA']
  for k in keywords:
    if k in command: return k
  return False

def SearchForValue(command, k):
  ''' For example, command = "M55STEP4.5", k = "STEP"... returns [4.5, "M55"] '''
  other = []
  precommand = command[:command.index(k)]
  if precommand != '': other.append(precommand)
  postcommand = command[command.index(k)+len(k):]
  val = ''
  for c in postcommand:
    if c.isdigit() or c=='.': val += c
    else: break
  postcommand = postcommand[len(val):]
  val = float(val)
  if postcommand != '': other.append(postcommand)
  return val, other

def GetListsOfCommands(command):
  keywords = ['STEP', 'AZM', 'ALT', 'DEC', 'RA']
  if   isinstance(command, list) and len(command) == 1 and ',' in command[0]: command = command[0].split(',')
  elif isinstance(command, str ) and ',' in command: command = command.split(',')
  if not isinstance(command, list): command = [command]
  keycommands = {}
  arrowcommands = []
  goto = []
  othercommands = []
  while len(command) > 0:
    commands = command
    command = []
    for c in commands:
      if c == '': continue
      arrowcommands, c = GetArrows(c)
      k = IsValueCommand(c)
      if not k: 
        if c != '': goto.append(c)
        continue
      else:
        value, other = SearchForValue(c, k)
        keycommands[k] = value
        command += other
  return arrowcommands, keycommands, goto

if __name__=='__main__':
  command = sys.argv[1]
  arrowcommands, keycommands, goto = GetListsOfCommands(command)
  for a in arrowcommands: print(' >> Moving to ', a)
  for k in keycommands  : print(' >> Executing [%s] (%1.4f)'%(k, keycommands[k]))
  for g in goto         : print(' >> GoTo %s'%g)
