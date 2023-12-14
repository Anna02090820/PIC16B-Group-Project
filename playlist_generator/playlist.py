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
from playlist_generator.spiders.related_words_spider import wordsSpider
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner

def get_related_words(keyword,topic):
    
    runner = CrawlerRunner(settings={"FEEDS": {"results.csv": {"format": "csv",'overwrite': True}}})
    d = runner.crawl(wordsSpider, ui=topic)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    
    results=pd.read_csv("results.csv") #gets results from csv file
    related_words=[f"{keyword}"]+list(results["topic"]) +list(results["related_word"]) #adds all entries to one list
    related_words=list(set(related_words)) #makes sure there no overlap
    return related_words

def spotify_authentication():
    cid="45d772a85b0a4c2681a42696ad3b5ef3"
    cs="9471f4a95ba34fb1a7c8414bc801542e"
    sp_oauth=SpotifyOAuth(client_id=cid,
                          client_secret=cs,
                          redirect_uri="http://localhost:2023/callback",
                          scope=["playlist-modify-public","playlist-modify-private"])
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    return sp

def get_playlist_songs(sp,related_words):
    df=pd.DataFrame(columns=["title","artist","release_date","uri",'danceability', 'energy', 'valence']) 
    for word in related_words:
    
        word_results=sp.search(q=f'track:{word}', limit=5)

        for song in word_results["tracks"]["items"]:

            mod_title=" "+re.sub(r'[^\w\s]', '', song["name"].lower())+" "

            if f" {word} " in mod_title:

                track_features = sp.audio_features(song["id"])

                try:
                    track_features[0]['acousticness'] # check if audio features exist
                except:
                    continue

                row=[song["name"],
                        song["artists"][0]["name"],
                        song["album"]["release_date"],
                        song["uri"],
                        track_features[0]['danceability'],
                        track_features[0]['energy'],
                        track_features[0]['valence']]

    #             # for this specific track id call that audio features thing and get those special features

                df.loc[len(df)]=row
    return df
# def filter_df(df):
#     return updated_df

def generate_playlist(keyword,topic,mood):
    related_words=get_related_words(keyword,topic)
    sp=spotify_authentication()
    playlist_df=get_playlist_songs(sp,related_words)
    playlist=sp.user_playlist_create(user=sp.me()["id"],
                                     name=f"{keyword.title()} Playlist",
                                     public=False,
                                     description=f"This is a {keyword.title()} Themed Playlist") # f" This playlist has a {} vibe"
    tracks=playlist_df["uri"].sample(30)
    sp.user_playlist_add_tracks(sp.me()["id"], playlist["id"], tracks)
    
    return playlist["external_urls"]["spotify"]
