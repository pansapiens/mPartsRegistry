#!/usr/bin/env python
# use this with the XML from http://partsregistry.org/das/protein_annotations/entry_points
# like:
# $ extract_ids_das.py entry_points.xml >part_id_list.py
#
# This generates a list all all ids currently in the Registry that can be
# imported, for instance to use for 'suggest' features or the 'random part'
# feature

# TODO: tie this into App Engine's cron to fetch the updated parts list daily
#       and plug it into the datastore

import sys
from BeautifulSoup import BeautifulStoneSoup

das = BeautifulStoneSoup(open(sys.argv[1]))
parts = das.dasep.entry_points.findAll("segment")
ids = []
for p in parts:
  ids.append(p['id'])

sys.stdout.write("ALL_PART_IDS = ")
sys.stdout.write(str(ids))
