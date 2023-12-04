'''
Various functions to filter through the created playlist dataframe by mood   
'''

# import sqlite3 # is this needed?
import pandas as pd

def query_find_happy(df, conn):
    '''
    Filter songs for a hype mood (i.e. positive emotion)
    Return filtered dataframe
    ''' 
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.3 AND energy <= 0.7
    AND valence >= 0.7
    AND danceability >= 0.7
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_hype(df, conn):
    '''
    Filter songs for a hype mood (i.e. positive emotion and high arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.3 AND energy <= 0.9
    AND valence >= 0.5 AND valence <= 0.9
    AND danceability = 0.5 AND danceability <= 0.9 
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_energetic(df, conn):
    '''
    Filter songs for a energetic mood (i.e. high arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.5 
    AND valence >= 0.3 AND valence <= 0.7
    AND danceability >= 0.5 AND danceability <= 0.9
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_agitated(df, conn):
    '''
    Filter songs for an agitated >:( mood (i.e. negative emotion and high arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.5 
    AND valence >= 0.1 AND valence <= 0.5
    AND danceability >= 0.7
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_melancholic(df, conn):
    '''
    Filter songs for a melancholic mood (i.e. negative emotion and low arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy <= 0.5 
    AND valence <= 0.3
    AND danceability >= 0.1 AND danceability <= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_sorrowful(df, conn):
    '''
    Flter songs for a sorrowful mood (i.e. negative emotion)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.1 AND energy <= 0.5 
    AND valence >= 0.1 AND valence <= 0.5
    AND danceability >= 0.1 AND danceability <= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_calm(df, conn):
    '''
    Filter songs for a calm mood (i.e. low arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy <= 0.3 
    AND valence >= 0.3 AND valence <= 0.7
    AND danceability <= 0.3
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_comfort(df, conn):
    '''
    Filter songs for a comfortable mood (i.e. positive emotion and low arousal)
    Return filtered dataframe
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.1 AND energy <= 0.5
    AND valence >= 0.5 AND valence <= 0.9
    AND danceability >= 0.1 AND danceability <= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df
