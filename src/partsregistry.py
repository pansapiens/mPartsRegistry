import urllib2
from xml.dom.minidom import parseString
from BeautifulSoup import BeautifulStoneSoup

# Python wrappers for the Registry of Standard Biological Parts API
#
# See: http://partsregistry.org/Registry_API
#
# Alternative - the DAS API: 
# http://partsregistry.org/DAS_-_Distributed_Annotation_System

def fetchurl(url):
  api_conn = urllib2.urlopen(url)
  xmldata = api_conn.read()
  api_conn.close()
  return xmldata

class Part():
  """
  A simple container class for parts from the Registry.
  Initialize like:
  
  part = Part("B0034")
  
  to pull down XML via the Registry API and populate the object
  with values.
  """
  def __init__(self, name, add_BBa=True, apiurl="http://partsregistry.org"):
    if add_BBa and name[0:4] != "BBa_":
      name = "BBa_" + name
    self.name = name
    self.xml = None
    self.dom = None
    self.error = None
    self.short_desc = None
    self.type = None
    self.status = None
    self.results = None
    self.rating = None
    self.apiurl = apiurl
    self.url = "%s/xml/part.%s" % (self.apiurl, self.name)
    self.entered = None
    self.author = None
    self.best_quality = None
    self.sequences = []
    self.size = None
    self.categories = []
    
    # TODO: subparts and features
    
    self.fetch()
    
  def fetch(self):
    self.xml = fetchurl(self.url)
    self.parse_xml()
    return self
  
  def parse_xml(self):
    part = BeautifulStoneSoup(self.xml)
    self.dom = part
    if part.part_list.error:
      self.error = part.part_list.error
      return False
    
    try:
      self.short_desc = part.part_short_desc.contents[0]
    except:
      pass
    try:
      self.type = part.part_type.contents[0]
    except:
      pass
    try:
      self.status = part.part_status.contents[0]
    except:
      pass
    try:
      self.results = part.part_results.contents[0]
    except:
      pass
    try:
      self.rating = part.part_rating.contents[0]
    except:
      pass
    try:
      self.url = "%s/xml/part.%s" % (self.apiurl, self.name)
    except:
      pass
    try:
      self.entered = part.part_entered.contents[0]
    except:
      pass
    try:
      self.author = part.part_author.contents[0]
    except:
      pass
    try:
      self.best_quality = part.best_quality.contents[0]
    except:
      pass
    
    try:
      for s in part.sequences("seq_data"):
        self.sequences.append(s.contents[0])
    except:
      pass
    try:
      self.size = len(self.sequences[0])
    except:
      pass
    try:  
      for c in part.categories("category"):
        self.categories.append(c.contents[0])
    except:
      pass

if __name__ == "__main__":
    
  print "\nFetching I13521 ..."
  p = Part("I13521")
  print p.short_desc

  print "\nWalking the part DOM directly ..."
  print "Name: ", p.dom.part_name.contents[0]
  print "Categories: "
  for c in p.dom.categories("category"):
    print c.contents[0]
  print "Size: %i bp" % (p.size)
  
  print "/nTesting invalid part X0000"
  q = Part("X0000")
  print q.error