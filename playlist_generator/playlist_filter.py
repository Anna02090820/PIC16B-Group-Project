'''
Various functions to filter through the created related words dataframe by 4 moods
'''

import pandas as pd

def query_find_hype(df, conn):
    '''
    Filter songs for a hype mood (i.e. positive emotion and high arousal)
    Arguments:
        df: dataframe of all songs from related words
        conn: SQL connection needed for command
    Returns:
        df: dataframe of "hype" songs
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.5
    AND valence >= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_agitated(df, conn):
    '''
    Filter songs for an agitated >:( mood (i.e. negative emotion and high arousal)
    Arguments:
        df: dataframe of all songs from related words
        conn: SQL connection needed for command
    Returns:
        df: dataframe of "agitated" songs
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy >= 0.5 
    AND valence <= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_sorrowful(df, conn):
    '''
    Filter songs for a sorrowful mood (i.e. negative emotion and low arousal)
    Arguments:
        df: dataframe of all songs from related words
        conn: SQL connection needed for command
    Returns:
        df: dataframe of "sorrowful" songs
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy <= 0.5
    AND valence <= 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df


def query_find_chill(df, conn):
    '''
    Filter songs for a chill mood (i.e. positive emotion and low arousal)
    Arguments:
        df: dataframe of all songs from related words
        conn: SQL connection needed for command
    Returns:
        df: dataframe of "chill" songs
    '''
    cmd = \
    """
    SELECT S.title, S.artist, S.release_date, S.uri, S.danceability, S.energy, S.valence
    FROM songs S
    WHERE energy <= 0.5
    AND valence > 0.5
    """
    # read sql command as pandas
    df = pd.read_sql_query(cmd, conn)
    return df

def user_input(mood, df, conn):
    '''
    Take in user input and perform function based on input
    Arguments:
        mood: user input of mood
        df: dataframe of all songs from related words
        conn: SQL connection needed for command
    Returns:
        df: dataframe of "chill" song
    '''
    mood = lower(mood)
    
    if mood == "hype":
        return query_find_hype(df, conn)
    elif mood == "agitated":
        return query_find_agitated(df, conn)
    elif mood == "sorrowful":
        return query_find_sorrowful(df, conn)
    elif mood == "chill":
        return query_find_chill(df, conn)
    else:
        return "Mood not applicable. Please try again."
