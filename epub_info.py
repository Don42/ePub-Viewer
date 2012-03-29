#!/usr/bin/python
# Script to output metadata of an ePub file
import tempfile
import os
import sys
import zipfile
import xml.etree.ElementTree as etree
import shutil
from BeautifulSoup import BeautifulSoup

def main():
  provider = ContentProvider()
  if len(sys.argv) == 2:
    #Load Book
    provider.prepareBook(sys.argv[1])

class ContentProvider():
  def __init__(self):
    blub = ""

  def prepareBook(self, filepath):
    #Clear any old files from the cache
    tmp = tempfile.mkdtemp()

    #Extract book
    zipfile.ZipFile(filepath).extractall(tmp)
    #Set permissions
    os.system("chmod 700 "+ tmp)

    if os.path.exists(tmp+"/META-INF/container.xml"):
      tree = etree.parse(tmp+"/META-INF/container.xml")
      root = tree.getroot()

      full_path = (root[0])[0].attrib.get("full-path")

      if os.path.exists(tmp+"/"+full_path):
        soup = BeautifulSoup(open(tmp+"/"+full_path))
        print("Title: "+soup.find("dc:title").string)



      shutil.rmtree(tmp) # delete directory

main()
