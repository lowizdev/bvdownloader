import requests
import re
import sys
from bs4 import BeautifulSoup


#  url = "https://www.bludv.tv/jumanji-bem-vindo-selva-2018-torrent-download-bluray-720p-e-1080p-legendado-dublado-dual-audio/"
url = sys.argv[1] 

#  pure_html = requests.get(url)
html = requests.get(url).text

bs = BeautifulSoup(html, "lxml")

#  print(bs.find_all("a"))

all_anchors = bs.find_all("a", href=re.compile("magnet.*"))

#  Might want to have a refactor / rewrite of the patterns.
#  Patterns work on the presented tests

ptrn_1080 = re.compile(".*1080p?\\.png.*")
ptrn_720 = re.compile(".*720p?\\.png.*")

ptrn_dub = re.compile(".*DUBLADO.*")
#  Find a way to difference Dual Audio and Subbed

separator = "##############################"

for anchor in all_anchors:
    #  print(anchor)
    if(ptrn_1080.match(str(anchor))):
        print("Res.: 1080p")
    elif(ptrn_720.match(str(anchor))):
        print("Res.: 720p")
    
    if(ptrn_dub.match(str(anchor))):
        print("Dublado")
    
    print("\nMagnet Link: " + anchor["href"]+"\n")
    print(separator)

