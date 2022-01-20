from bs4 import BeautifulSoup
import requests
import os
from bs4 import BeautifulSoup
import urllib.request
import shutil

def fLinkGet(URL,dirPath,fName):
  for f in os.listdir(dirPath):
    os.remove(os.path.join(dirPath, f))
  html_doc = urllib.request.urlopen(URL)
  soup = BeautifulSoup(html_doc, 'html.parser')
  
  dir = dirPath
  shutil.rmtree(dir)
  if not os.path.exists(dir):
    os.mkdir(dir)
  i=0
  for link in soup.find_all('a'):
    filename = "{}-{}.html".format(fName,i)
    linkUrl = ""
    for links in link.get('href'):
      if "https://" in str(links) or "http://" in str(links):
        linkUrl = link.get('href')
      else:
        linkUrl = URL + str(links)
  
      with open("{}/{}".format(dir,filename),"w+") as f:
        vLink = linkUrl.rstrip(linkUrl[-1])
        r = requests.get(vLink)
        f.write(r.text)
        print(vLink)
        f.close()
    