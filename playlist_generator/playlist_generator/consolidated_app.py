import pandas as pd
import spotipy
import re
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import time
from scrapy import cmdline
import pandas as pd
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from playlist_generator.spiders.related_words_spider import wordsSpider
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner

# Function 1: Scrapy and Get related Words
runner = CrawlerRunner(settings={"FEEDS": {"results.csv": {"format": "csv",'overwrite': True}}})
    d = runner.crawl(wordsSpider, ui=topic)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
results=pd.read_csv("results.csv") #gets results from csv file
related_words=[f"{keyword}"]+list(results["topic"]) +list(results["related_word"]) #adds all entries to one list
related_words=list(set(related_words)) #makes sure there no overlap

# Function 2: Spotify authentication 
cid="45d772a85b0a4c2681a42696ad3b5ef3"
cis="9e9848f1081e459ebc686f6f62b5902d"

sp_oauth=SpotifyClientCredentials(client_id=cid,client_secret=cis)
#sp_oauth=SpotifyOAuth(client_id=cid,client_secret=cis,redirect_uri="http://localhost:2023/callback",scope=["playlist-modify-public","playlist-modify-private"])
#this line doesn't work in deepnote for some reason but it works in jupyter lab
sp = spotipy.Spotify(auth_manager=sp_oauth)

#add rows of the columns associated with the song features
df=pd.DataFrame(columns=["title","artist","release_date","uri",'danceability', 'energy', 'valence']) 
for word in related_words:
    word_results=sp.search(q=f"track:{word}", limit=5)

    for song in word_results["tracks"]["items"]:

        mod_title=" "+re.sub(r'[^\w\s]', '', song["name"].lower())+" "
        #checks that the actual word is in title, not just the word plus some letters

        if f" {word} " in mod_title:

            track_features = sp.audio_features(song["id"])
            #track features isn't working on my computer anymore for some reason??

            try:
                track_features[0]['acousticness'] # check if audio features exist
            except:
                continue

            row=[
            song["name"],
            song["artists"][0]["name"],
            song["album"]["release_date"],
            song["uri"],
            track_features[0]['danceability'],
            track_features[0]['energy'],
            track_features[0]['valence']             
            ]

            # for this specific track id call that audio features thing and get those special features

            df.loc[len(df)]=row

df.to_csv('songs.csv')


# Function 3: 
