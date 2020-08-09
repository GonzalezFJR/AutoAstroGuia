'''
 Class to connect with an android app
 I'm using BlueTooth Serial Controller
 To reset a command, send 'START'
 To finish a command, send 'SEND'
'''

import serial
import time

serialName = '/dev/rfcomm0'
timeSleep = 0.001
resetCommandKey = 'START'
endCommandKey = 'SEND'
keywords = [ '<-', '-^-', '->', '-V-']

class serialReader:
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

def InterpretCommand(command):
  keywords = ['STEP', 'AZM', 'ALT', 'DEC', 'RA', '<-', '-^-', '->', '-V-']
  pass

if __name__=='__main__':
  pass
