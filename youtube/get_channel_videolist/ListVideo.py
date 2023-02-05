# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 06:10:28 2023

@author: arathi
"""

import scrapetube
import sys
import requests
import html_to_json

path = '_list.txt'

channel_List = [
   "www.youtube.com/@Sachwala" ,
   "www.youtube.com/@ZafarHeretic" ,
   "www.youtube.com/@ExMuslimSahil" ,
   "www.youtube.com/@ExMuslimSameer" ,
   "www.youtube.com/@faizalam-theroasterkid" ,
   "www.youtube.com/@Deenibhai" ,
   "www.youtube.com/@exmansari" ,
   "www.youtube.com/@exmuslim_yasmin_khan" ,
   "www.youtube.com/@apostateimam-the12thimamwh98" ,
   "www.youtube.com/@munnabhaiexmuslimofficial" ,
   "www.youtube.com/@AdamSeekerUrdu" ,
   "www.youtube.com/@sajidimam7563" ,
   "www.youtube.com/@iamhaqwalaexmuslim" ,
   "www.youtube.com/@alishahex-muslim6723" ,
   "www.youtube.com/@SachwalaAbdulHamid" ,
   "www.youtube.com/@rihanexmuslim8021" ,
   "www.youtube.com/@AuthenticXMuslim" ,
   "www.youtube.com/@exmuslimbharat2303" ,
   "www.youtube.com/@UncompromisingIndia" ,
   "www.youtube.com/@littlefaizu-thehumanistmur4206" ,
   "www.youtube.com/@imanwalakafir6422" ,
   "www.youtube.com/@exmuslimsuhail" ,
   "www.youtube.com/@sulemanijalebiya" ,
   "www.youtube.com/@exmuslimtahmin" ,
   "www.youtube.com/@exmuslimangel" ,
   "www.youtube.com/@haqookseeker1305" ,
   "www.youtube.com/@Exmuslimdarashikoh" ,
   "www.youtube.com/@bengaliex-muslim"
    ]

channel_List = [
   "https://www.youtube.com/@ExMuslimSameer" 
   ]

def get_channelID_from_meta(meta):
    for attrib in meta:
        #print(f"_attributes {attrib}" )
        if 'itemprop' in attrib['_attributes']:
           #print(f"_attributes {attrib}" )
           if attrib['_attributes']['itemprop'] == 'channelId':
               print(f"content {attrib['_attributes']['content']}" )
               return  attrib['_attributes']['content']
           
    return  None
    
def get_channelurl_from_meta(meta):
    for attrib in meta:
        if  'property' in attrib['_attributes']:
           if attrib['_attributes']['property'] == 'og:url':
               return  attrib['_attributes']['content']
    return  None
    

# Prints the output in the console and into the '_list.txt' file.
class Logger:
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'w')
 
    def write(self, message):
        self.console.write(message)
        self.file.write(message)
 
    def flush(self):
        self.console.flush()
        self.file.flush()

class Html2JSON:
 
    def __init__(self, url):
        r = requests.get(url)
        self.status = r.status_code
        html_string = r.text
        try:
            self.output_json = html_to_json.convert(html_string)
        except :
            self.output_json = None
            self.channel_id = None
            self.channel_url = None
            return

        try:
            meta = self.output_json['html'][0]['body'][0]['meta']
            #print(f"meta = {meta}")
            self.channel_id = get_channelID_from_meta(meta)
            self.channel_url = get_channelurl_from_meta(meta)
        except :
            self.channel_id = None
            self.channel_url = None
            
    def get_channel_id(self, ):
        return self.channel_id

    def get_channel_url(self, ):
        return self.channel_url
 

sys.stdout = Logger(path)

# Strip the: "https://www.youtube.com/channel/"
channel_url = "https://www.youtube.com/@ExMuslimSameer"


h2j = Html2JSON(channel_url)
channel_id_list = [ Html2JSON(channel_url).channel_id for channel_url in channel_List]
print(f"channel_id_list : {channel_id_list}")
for id in channel_id_list:
    videos = scrapetube.get_channel(channel_id=id)
    for video in videos:
        print(f"video : {video['title']}")
        print(f"descriptionSnippet: {video['descriptionSnippet']}")
        print("https://www.youtube.com/watch?v="+str(video['videoId']))
        break
        #print("https://www.youtube.com/watch?v="+str(video['videoId']))
    #    print(video['videoId'])
