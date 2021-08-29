import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import numpy as np
import os, sys, time

pathToCatalogs = './catalogs/'
availableCatalogs = ['messier', 'flamsted', 'IC', 'NamedStars', 'NGC', 'HD']

class ObjectFinder:

  def __init__(self, lat=0, lon=0, alt=0, month=0, day=0, h=0, minut=0, seg=0, year=2020, utcoffset=1):
    ''' Initialize with local values of space and time '''
    self.SetCoor(lat, lon, alt)
    self.SetTime(day,month,year,h,minut,seg,utcoffset)
    self.verbose = False
    self.LoadFromCatalogue = True
    self.pathToCatalogs = pathToCatalogs
    self.availableCatalogs = availableCatalogs
    self.otherCatalogs = availableCatalogs[:]
    self.t0 = time.time()
    for c in ['NGC', 'messier', 'IC', 'HD']: 
      if c in self.otherCatalogs: self.otherCatalogs.pop(self.otherCatalogs.index(c))
    self.ReadCatalogs()

  def ReadCatalogs(self):
    ''' Read all catalogs and store as tables '''
    self.catalogs = {}
    for cat in self.availableCatalogs:
      print('      > Loading catalogue %s...'%cat)
      cattxt = self.pathToCatalogs+cat+'.txt'
      if not os.path.isfile(cattxt):
        print('WARNING: catlog "%s" not found...'%cattxt)
        continue
      tab = np.genfromtxt(cattxt, dtype='str')
      self.catalogs[cat] = tab

  def FindInCatalog(self, name):
    ''' Search for object in catalof and returns ra, dec '''
    catalog = ''
    ra = ''; dec = ''
    if   name.startswith('NGC'): catalog = 'NGC'
    elif name.startswith('IC' ): catalog = 'IC'
    elif name.startswith('HD' ): catalog = 'HD'
    elif name.startswith('M'  ): catalog = 'messier'
    else                       : catalog = self.otherCatalogs
    if not isinstance(catalog, list): catalog = [catalog]
    for cat in catalog:
      tab = self.catalogs[cat]
      if not name.upper() in tab: continue
      ra, dec = tab[np.where(tab==name.upper())[0][0]][1:]
    if ra=='' or dec == '':
      print('WARNING: object "%s" not found in any catalog'%name)
      return None
    else: return float(ra), float(dec)

  def SetVerbose(self, verbose=True):
    self.verbose = verbose

  def SetCoor(self, lat=0, lon=0, alt=0):
    ''' Set local coordinates '''
    self.coor = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=alt*u.m)

  def SetTime(self, day=1, month=1, year=2020, h=0, minut=0, seg=0, utcoffset=1):
    ''' Sets local time '''
    utcoffset=utcoffset*u.hour
    self.time = Time('%i-%i-%i %i:%i:%i'%(year,month,day,h,minut,seg)) - utcoffset

  def UpdateTime(self):
    t = time.time()
    dt = t-self.t0
    self.time += dt*u.second
    self.t0 = t

  def GetSkyCoorFromName(self, name):
    ''' Returns sky coordinates for a named object ''' 
    if self.LoadFromCatalogue:
      res = self.FindInCatalog(name)
      if res == None: # Not found
        return None
      coor = SkyCoord(ra=res[0]*u.degree, dec=res[1]*u.degree)
    else:
      coor = SkyCoord.from_name(name)
    if self.verbose: print('%s: [ra, dec] = [%1.3f, %1.3f]'%(name, coor.ra, coor.dec))
    return coor

  def ToAltAzm(self, coordinates, dec=0):
    if dec != 0: # input is RA, DEC
      coordinates = SkyCoord(ra=coordinates*u.degree, dec=dec*u.degree)
    self.UpdateTime()
    coor = coordinates.transform_to(AltAz(obstime=self.time, location=self.coor))
    alt = coor.alt
    azm = coor.az
    return alt.degree, azm.degree

  def GetLocalSkyCoorFromName(self, name):
    ''' Returns alt, azm for a named object ''' 
    coor = self.GetSkyCoorFromName(name)
    if   coor == None: # Not found
      return None
    return self.ToAltAzm( coor )

  def TransformCoordinates(self, alt, azm):
    ''' Transform sky coordinates to alt in [0, 180], azm in [-90, 90] '''
    if azm>180: 
      azm = azm-180
      alt = 180-alt
    return alt, azm

  def GetLaserAngleForObj(self, name):
    ''' Get alt, azm in good coordinates for a given object '''
    coor = self.GetLocalSkyCoorFromName(name)
    if coor == None: return None
    alt, azm = coor
    return self.TransformCoordinates(alt, azm)


if __name__=='__main__':
  obj = sys.argv[1]
  o = ObjectFinde(43.3, -5.9, 200, 12, 12, 20, 35, 0, 2020, 1)
  coor = o.GetSkyCoorFromName(obj)
  ra = coor.ra.degree; dec = coor.dec.degree
  alt, azm   = o.GetLocalSkyCoorFromName(obj)
  alt2, azm2 = o.GetLaserAngleForObj(obj)
  print('Sky   coordinates: [ra , dec] = [%1.5f, %1.5f]'%(ra, dec))
  print('Local coordinates: [alt, azm] = [%1.5f, %1.5f]'%(alt, azm))
  print('Laser goes to    : [alt, azm] = [%1.5f, %1.5f]'%(alt2, azm2))
