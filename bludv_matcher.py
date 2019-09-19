import requests
import re
import sys
from bs4 import BeautifulSoup

class Overlooker:

    def __init__(self):
        self.requester = Requester()

    #Returns a list of all anchors that contain a specific pattern
    def get_all_anchors_raw(self, url, pattern = re.compile("magnet.*")):
        bs = self.requester.parse_bs4(url)
        all_anchors = bs.find_all("a", href = pattern)
        return all_anchors

    def get_all_urls(self, url):
        pass

    def classify_anchors(self, anchor_list, origin_url, class_ptrn_dict):
        
        classified_anchors = []

        for anchor in anchor_list:
            
            anchor_info = "" # Can be anything really. Might refactor later
            
            for pattern_key in class_ptrn_dict:
                if(class_ptrn_dict[pattern_key].match(str(anchor))):
                    anchor_info += pattern_key + "\n"
            
            new_anchor = Anchor(anchor, anchor_info, origin_url)

            classified_anchors.append(new_anchor)
        
        return classified_anchors
    
    #Builds an url list from urls of a page by some criteria
    def build_url_list(self, url, pattern = None, htmlclass = ""):
        bs = self.requester.parse_bs4(url)
        all_elems = bs.find_all("div", {"class" : htmlclass})
        all_urls = []
        for elem in all_elems:
            #print(str(elem) + "\n\n")
            all_urls.append(self.bsanchor_href_field(elem.find_all("a", href = pattern))[0]) #ATTENTION: Only the first element. Might be subject to change
        return all_urls

    #Takes href item from bs objects
    def bsanchor_href_field(self, elems):
        hrefs = []
        for elem in elems:
            hrefs.append(elem["href"])
                
        return(hrefs)

class Anchor:
    def __init__(self, anchor, anchor_info, url, title = "Unnamed"):
        self.anchor = anchor #Contains all anchor raw info
        self.anchor_info = anchor_info
        self.url = url
        self.title = title
    
    def simple_print(self):
        print(str(self.anchor["href"]) + "\n" + self.anchor_info + "\n" + "URL:" + self.url + "\n")

    def set_title_from_url(self):
        pass

class Requester:

    def make_simple_request(self, url):
        html_result = requests.get(url).text
        return html_result
    
    def make_list_request(self, url_list):
        html_result_list = []
        for url in url_list:
            html_result_list.append(self.make_simple_request(url))
        return html_result_list

    #Returns a bs4 object made up from the html result of a request
    def parse_bs4(self, url, parser = "lxml"):
        bs = BeautifulSoup(self.make_simple_request(url), parser)
        return bs

    def parse_bs4_list(self, url_list, parser = "lxml"):
        list_request = self.make_list_request(url_list)
        list_bs = []
        for req_url in list_request:
            list_bs.append(self.parse_bs4(req_url))
        return list_bs

    
    def ping_test(self, url):
        pass

class PageDownloader:

    def __init__(self):
        pass

    pass

class Writer():
    pass


#url = "https://www.bludv.tv/jumanji-bem-vindo-selva-2018-torrent-download-bluray-720p-e-1080p-legendado-dublado-dual-audio/"
#url = sys.argv[1] 

################

#TODO: Build programatically
ptrns = {
    "Res.1080p" : re.compile(".*1080p?\\.png.*"),
    "Res.720p" : re.compile(".*720p?\\.png.*"),
    "DUB" : re.compile(".*DUBLADO.*")
}

if __name__ == "__main__":

    '''url = "https://www.bludv.tv/jumanji-bem-vindo-selva-2018-torrent-download-bluray-720p-e-1080p-legendado-dublado-dual-audio/"

    test_ovlk = Overlooker()
    raw_anchors = test_ovlk.get_all_anchors_raw(url)

    #print(raw_anchors) #TEST

    anchors = test_ovlk.classify_anchors(raw_anchors, url, ptrns)
    for anchor in anchors:
        print("#" * 36)
        anchor.simple_print()
        print("#" * 36)'''
    
    url2 = "https://www.bludv.tv"

    test_ovlk2 = Overlooker()
    urllist = test_ovlk2.build_url_list(url2, re.compile("https://www.bludv.tv\\/.*\\/"), "post")
    print(urllist)
    
    #print (type(urllist[0][0]))


    #FILTER URLS