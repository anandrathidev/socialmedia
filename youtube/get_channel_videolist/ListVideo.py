# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 23:00:56 2023

@author: ananduser
"""

import scrapetube
import sys
import requests
import html_to_json
import sqlite3
from datetime import datetime
import dateutil
import configparser
import json 
config = configparser.ConfigParser()
try:
    config.read('youtube.ini')
except:
    print("cant read youtube.ini or not found")
    quit()

logpath = config['DEFAULT']['logpath']
channel_List = json.loads(config['channels']['channels'])

def get_channelID_from_meta(meta):
    for attrib in meta:
        #print(f"_attributes {attrib}" )
        if 'itemprop' in attrib['_attributes']:
           #print(f"_attributes {attrib}" )
           if attrib['_attributes']['itemprop'] == 'channelId':
               print(f"channel id {attrib['_attributes']['content']}" )
               return  attrib['_attributes']['content']
           
    return  None
    
def get_channelurl_from_meta(meta):
    for attrib in meta:
        if  'property' in attrib['_attributes']:
           if attrib['_attributes']['property'] == 'og:url':
               return  attrib['_attributes']['content']
    return  None
    
class YoutubeData:
    def __init__(self, dbname):
        self.dbname = dbname

    def connect(self,):
        self.con = sqlite3.connect(self.dbname)
        
    def commit(self,):
        self.con.commit()

    def close(self,):
        self.con.close()
        
        
    def create_youtube_table(self, ):
        self.connect()
        cur = self.con.cursor()        
        try:
            cur.execute("CREATE TABLE youtube ( \
                    name TEXT, \
                    channel TEXT, \
                    videoid TEXT, \
                    title TEXT, \
                    isposted INTEGER, \
                    pubdate TEXT, \
                    postdate TEXT, \
                    UNIQUE(videoid) )") 
            
        except Exception as e:
            print(f"CREATE TABLE youtube failed error {e}")
        self.con.commit()
        self.close()

    def Insert(self, 
               name,
               channel, 
               videoid, 
               title, 
               pubdate, 
               postdate ):
        self.connect()
        cur = self.con.cursor()
        try:
            dtpubdate = dateutil.parser.isoparse(pubdate)
            data = (name, channel, videoid, title, 0, dtpubdate.isoformat(), "" )
            datalist = [data]
            cur.executemany("INSERT INTO youtube VALUES(?, ?, ?, ?, ?, ?, ?)", datalist)
            self.commit()
        except sqlite3.IntegrityError as ie:
            print(f"{videoid} already exists with {title.encode('cp1252', errors='ignore')} error {ie}")
            
        except sqlite3.OperationalError as oe:
            print(f"Insert error {oe}")
        self.close()

    def select(self, ):
        self.connect()
        cur = self.con.cursor()
        for row in self.con.execute("SELECT name, channel, videoid, title, isposted, pubdate, postdate from youtube"):
            name, channel, videoid, title, isposted, pubdate, postdate = row
            print(f"name {name} channel {channel}, videoid {videoid}, \
                  title{title.encode('cp1252', errors='ignore')}, \
                  isposted {isposted} , pubdate {pubdate} , postdate {postdate} ")  
        self.close()
                    


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
 

sys.stdout = Logger(logpath)

youtube_data = YoutubeData( config['DEFAULT']['dbname'] )

#youtube_data.create_youtube_table()
youtube_data.select()

import googleapiclient.discovery

print(f" developerKey {config['DEFAULT']['developerKey']} " )
youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=config['DEFAULT']['developerKey']
)


#h2j = Html2JSON(channel_List)
channel_id_list = [ (Html2JSON(channel_url).channel_id,channel_url) for channel_url in channel_List]

for id,churl in channel_id_list:
    if id is None:
        continue
    try:
        videos = list(scrapetube.get_channel(channel_id=id))
    except Exception as e:
        print(f"id : {id} err : {e}")
        
    for video in videos:
        try:
            print(f"videoId {video['videoId']} \n")
        except Exception as e:
            print(f"video : {video} ")
            continue
        request = youtube.videos().list(
            part="snippet",
            id=video['videoId']
        )
        response = request.execute()
        print(response['items'][0]['snippet']['publishedAt'])
        
        #print(f" publishedTimeText {video['publishedTimeText']} \n")
        title=""
        #print(f"keys: {video.keys()}")
        for text in video['title']['runs']:           
            title += str(text['text']) #.encode('unicode'))
        #print(f"text title: {title.encode('cp1252', errors='ignore')} \n")
        youtube_data.Insert(name = churl, 
                            channel = id, 
                            videoid = video['videoId'], 
                            title = title, 
                       pubdate = response['items'][0]['snippet']['publishedAt'], 
                       postdate = "")
            
        #print(f"desctxt: {desctxt.encode('cp1252', errors='ignore')}\n")
        print("https://www.youtube.com/watch?v="+str(video['videoId']))
    #break
    #print("https://www.youtube.com/watch?v="+str(video['videoId']))
#    print(video['videoId'])

youtube_data.select()
