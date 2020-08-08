import os, sys, pickle
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

class ObjectPointer:

  def __init__(self, lat=0, lon=0, alt=0, month=0, day=0, h=0, minut=0, seg=0, year=2020, utcoffset=1):
    ''' Initialize with local values of space and time '''
    self.SetCoor(lat, lon, alt)
    self.SetTime(day,month,year,h,minut,seg,utcoffset)
    self.verbose = False
    self.LoadCatalog()

  def SetVerbose(self, verbose=True):
    self.verbose = verbose

  def LoadCatalog(self, name='.catalog'):
    ''' Load pickle file with stored coordinates '''
    self.catalogFileName = name
    self.catalog = {}
    if os.path.isfile(name): 
      with open(name, 'rb') as f: self.catalog = pickle.load(f)
    print('catalog = ', self.catalog)

  def SetCoor(self, lat=0, lon=0, alt=0):
    ''' Set local coordinates '''
    self.coor = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=alt*u.m)

  def SetTime(self, day=1, month=1, year=2020, h=0, minut=0, seg=0, utcoffset=1):
    ''' Sets local time '''
    utcoffset=utcoffset*u.hour
    self.time = Time('%i-%i-%i %i:%i:%i'%(year,month,day,h,minut,seg)) - utcoffset

  def GetSkyCoorFromName(self, name):
    ''' Returns sky coordinates for a named object '''
    name = name.replace(' ', '').upper()
    if name in self.catalog: 
      coor  = self.catalog[name]
    else:
      coor = SkyCoord.from_name(name)
      self.catalog[name] = coor
      with open(self.catalogFileName, 'wb') as f: pickle.dump(self.catalog, f)
    ra = coor.ra.degree
    dec = coor.dec.degree
    if self.verbose: print('%s: [ra, dec] = [%1.3f, %1.3f]'%(name, coor.ra, coor.dec))
    return coor

  def ToAltAzm(self, coordinates):
    coor = coordinates.transform_to(AltAz(obstime=self.time, location=self.coor))
    alt = coor.alt
    azm = coor.az
    return alt.degree, azm.degree

  def GetLocalSkyCoorFromName(self, name):
    ''' Returns alt, azm for a named object ''' 
    return self.ToAltAzm( self.GetSkyCoorFromName(name))

  def TransformCoordinates(self, alt, azm):
    ''' Transform sky coordinates to alt in [0, 180], azm in [-90, 90] '''
    if azm>180:
      azm = azm-180
      alt = 180-alt
    return alt, azm

### Test
obj = 'arcturus'
o = ObjectPointer(43.3, -5.9, 200, 8, 10, 20, 35, 0, 2021, 1)
M33 = o.GetSkyCoorFromName(obj)
for obj in ['M33', 'M34']: o.GetSkyCoorFromName(obj)
#print('%s = '%obj, M33)
#alt, azm = o.GetLocalSkyCoorFromName(obj)
#print('alt = ', alt, ', azm = ', azm)
#alt2, azm2 = o.TransformCoordinates(alt, azm)
#print('Local coordinates: alt = ', alt2, ', azm = ', azm2)
