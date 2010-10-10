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
  def __init__(self, name=None, add_BBa=True, \
                           auto_fetch=True, \
                           auto_parse=True, \
                           apiurl="http://partsregistry.org"):
    
    # add BBa_ if missing, but not to plasmids (pSB***)
    # TODO: make a list of regexs that shouldn't be BBa_'ed
    if name and add_BBa and name[0:4].lower() != "bba_" and name[0:3].lower() != "psb":
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
    self.deep_subparts = []
    self.specified_subparts = []
    
    # TODO: subparts and features
    
    # specified_subscars
    ## subpart
    ## scar
    ## barcode
    
    # features
    ## feature
    ### id
    ### title
    ### type
    ### direction
    ### startpos
    ### endpos
    
    # parameters
    ## parameter
    ### name
    ### value
    ### units
    ### url
    ### id
    ### m_date
    ### user_id
    ### user_name
    
    # twins
    ## twin
    
    if auto_fetch and name: self.fetch()
    if auto_parse and name: self.parse_xml()
    
  def fetch(self):
    self.xml = fetchurl(self.url)
    return self
  
  def parse_xml(self, xmlstr=None):
    """
    Parse self.xml. If a string is given as an argument (xmlstr)
    then set self.xml to that string, then parse.
    """
    if xmlstr:
      self.xml = xmlstr
      
    part = BeautifulStoneSoup(self.xml)
    self.dom = part
    try:
      if part.part_list.error:
        self.error = part.part_list.error
        return False
    except:
      pass
    
    try:
      self.name = part.part_name.contents[0]
    except:
      pass
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
    try:
      for subpart in part.deep_subparts("subpart"):
        p = Part()
        p.xml = str(subpart)
        p.parse_xml()
        self.deep_subparts.append(p)
    except:
      pass
    
    try:
      for subpart in part.specified_subparts("subpart"):
        p = Part()
        p.xml = str(subpart)
        p.parse_xml()
        self.specified_subparts.append(p)
    except:
      pass

if __name__ == "__main__":
    
  print "\nFetching I13521 ..."
  
  # fetch part automatically via network
  p = Part("I13521")
  
  # use XML from a local file
  """
  p = Part("I13521", auto_fetch=False, auto_parse=False)
  fh = open("testing/I13521.xml", 'r')
  p.parse_xml(fh.read())
  fh.close()
  """
  
  print p.short_desc
  
  print "deep_subparts: ", [sp.name for sp in p.deep_subparts]
  print "specified_subparts", [sp.name for sp in p.specified_subparts]
  
  print "\nWalking the part DOM directly ..."
  print "Name: ", p.dom.part_name.contents[0]
  print "Categories: "
  for c in p.dom.categories("category"):
    print c.contents[0]
  print "Size: %i bp" % (p.size)
  
  print "/nTesting invalid part X0000"
  q = Part("X0000")
  print q.error