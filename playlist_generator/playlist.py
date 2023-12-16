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
import sqlite3
import playlist_filter # custom module

def get_related_words(keyword,topic):
    """
    This function finds words that are related to a valid user topic. The 
    function uses CrawlerRunner to call our scrapy spider and feed the 
    results into results.csv. Then, the function extracts words from this data
    frame, removes any duplicate words, and returns a list of these unique words.
    """
    
    runner = CrawlerRunner(settings={"FEEDS": {"results.csv": {"format": "csv",'overwrite': True}}}) #gets words related to topic
    d = runner.crawl(wordsSpider, ui=topic)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    
    results=pd.read_csv("results.csv") #gets results from csv file
    related_words=[f"{keyword}"]+list(results["topic"]) +list(results["related_word"]) #adds all entries to one list
    related_words=list(set(related_words)) #makes sure there no overlap
    return related_words

def spotify_authentication():
    """
    This function conducts Spotify authentication. By using our Spotify 
    App's client secret and ID, our code is granted access to working with the
    Spotify API. This function then returns the authenticated Spotipy object.
    """
    cid="45d772a85b0a4c2681a42696ad3b5ef3"
    cs="9471f4a95ba34fb1a7c8414bc801542e"
    sp_oauth=SpotifyOAuth(client_id=cid,
                          client_secret=cs,
                          redirect_uri="http://localhost:2023/callback",
                          scope=["playlist-modify-public","playlist-modify-private"]) #creates authentication object
    sp = spotipy.Spotify(auth_manager=sp_oauth) #initiailizes spotipy with our user authentication
    return sp

def get_playlist_songs(sp,related_words):
    """
    This function gets an initial set of songs from the Spotify API. For each word in related_words,
    the function extracts various songs in the Spotify dataset that contain that word in their title.
    The function then extracts features of the songs. The songs and features are then appended to a dataframe 
    which the function returns.
    """
    df=pd.DataFrame(columns=["title","artist","release_date","uri", 'energy', 'valence']) 
    for word in related_words:
    
        word_results=sp.search(q=f'track:{word}', limit=5) #finds songs

        for song in word_results["tracks"]["items"]:

            mod_title=" "+re.sub(r'[^\w\s]', '', song["name"].lower())+" " 

            if f" {word} " in mod_title: #checks if word is in title not within another word
                track_features = sp.audio_features(song["id"]) #gets audio features of a song
                try:
                    try:
                        track_features[0]['acousticness'] # check if audio features exist
                    except:
                        continue

                    row=[song["name"],
                         song["artists"][0]["name"],
                            song["album"]["release_date"],
                            song["uri"],
                            track_features[0]['energy'],
                            track_features[0]['valence']]

                    # for this specific track id call that audio features thing and get those special features
                    df.loc[len(df)]=row
                    
                except spotipy.exceptions.SpotifyException as e: # handle spotify api errors
                    if (e.http_status == 429):  # Too many requests
                        print("An error occurred:", e)
                        print("Playlist cannot load at this moment. Please try again later.")
                        break
                    else:
                        print("An error occurred:", e)
                except Exception as e: # handle general errors
                    print("An error occurred:", e)
                    break
    return df

def generate_playlist(keyword,topic,mood):
    """
    This function is called with our flask form arguments to generate
    the playlist from start to finish. It finds the words related to the user topic,
    performs Spotify authentication, gets an initial set of songs corresponding to the
    related words, excludes any songs that don't match the user's topic, creates the
    Spotify playlist and uploads songs. The function then returns a link to the generated
    playlist.
    """
    related_words=get_related_words(keyword,topic) #gets words related to user input
    sp=spotify_authentication()                     #user authentication
    playlist_df=get_playlist_songs(sp,related_words) #initial list of spotify songs

    # create SQL database and connection
    conn = sqlite3.connect("related_songs.db")
    playlist_df.to_sql("songs", conn, if_exists="replace")

    # create playlist of mood based on user input
    mood_df = playlist_filter.user_input(mood, playlist_df, conn)
    
    playlist=sp.user_playlist_create(user=sp.me()["id"],
                                     name=f" {mood.title()} {keyword.title()} Playlist",
                                     public=False,
                                     description=f"This is a {mood.title()} {keyword.title()} Themed Playlist") 
                                    #creates user playlist
    tracks=mood_df["uri"]
    sp.user_playlist_add_tracks(sp.me()["id"], playlist["id"], tracks) #adds tracks to playlist

    # close SQL connection
    conn.close()
    
    return playlist["external_urls"]["spotify"] #returns url to playlist
