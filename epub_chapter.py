#!/usr/bin/python
#Script to Output the chapters of a book

import tempfile
import os
import sys
import zipfile
import shutil
from bs4 import BeautifulSoup as BS

def main():
  if len(sys.argv) == 2:
    provider = ContentProvider(sys.argv[1])
    provider.createIndex()
    for item in provider.index:
      print(item)
    del provider

class ChapterItem():
  id    = ""
  href  = ""
  title = ""

  def __init__(self):
    blub=""

  def __str__(self):
    return self.title +" " + self.id +" "+ self.href

class ContentProvider():

  def __init__(self, path):
    #Create tmp directory
    self.tmp_path = tempfile.mkdtemp()
    #Extract book
    zipfile.ZipFile(path).extractall(self.tmp_path)
    #Set permissions
    os.system("chmod 700 "+ self.tmp_path)

    #find OPF Path
    if os.path.exists(self.tmp_path+"/META-INF/container.xml"):
      container = BS(open(self.tmp_path+"/META-INF/container.xml"))
      odf_path = container.find("rootfile")["full-path"]

      if os.path.exists(self.tmp_path+"/"+odf_path):
        self.odf = BS(open(self.tmp_path+"/"+odf_path))

  def __del__(self):
    shutil.rmtree(self.tmp_path)

  def createIndex(self):
    manifest = self.odf.manifest
    spine    = self.odf.spine
    guide    = self.odf.guide
    self.index = []

    itemrefs = spine.findAll("itemref")

    for itemref in itemrefs:
      if itemref['linear'] == "yes":
        item = ChapterItem()
        item.id = itemref['idref']
        item.href = manifest.find(id = item.id)['href']
        item.title= guide.find(href = item.href)['title']
        self.index.append(item)


main()
