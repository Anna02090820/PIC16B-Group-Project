# Spotify Playlist Generator
## Overview

### Summary
The Spotify Playlist Generator is a Python-based project designed to create personalized Spotify playlists for users. It is intended for music enthusiasts who desire a customized listening experience, tailored to their mood and specific themes. By inputting keywords, users can generate playlists where the songs’ names contain many related words in the keyword topic, and the users are also able to filter out the songs according to their desired mood to get a more personalized playlist. The project stands out for its ability to interpret user input, leverage web scraping for related words, and interact with the Spotify API to curate relevant playlists. This makes it a highly desirable product for users seeking a more engaged and personalized approach to music curation on Spotify.

### Key Python packages and tools utilized in the project:
Pandas: For data handling and manipulation.  
Spotipy: A lightweight Python library for the Spotify Web API, enabling interaction with Spotify's music catalog.  
Regular Expressions: For parsing and manipulating strings.  
Scrapy: A powerful web scraping framework used to extract related words from the internet.  
Flask: To create a web application interface for the playlist generator.  
SQLite3: Assuming the use of SQLite for SQL operations in filtering songs based on mood.  

### Key tasks and features in the project:
Web Scraping for Related Words: Utilizing Scrapy to extract words related to the user's input keyword from websites like "relatedwords.io".  
Song Retrieval Based on Words: Using Spotipy to find songs that include the related words in their titles or other metadata, thereby ensuring the relevance of the playlist to the user's input.  
Mood-Based Filtering: Implementing mood-based filters (like hype, agitated, sorrowful, chill) to refine the playlist according to the emotional tone desired by the user.  
Visualization of Mood in Playlist: An innovative aspect could be the visualization of the mood distribution within the generated playlist, possibly using libraries like Matplotlib or Seaborn for graphical representation.  

The combination of these features in a user-friendly web interface via Flask makes the Spotify Playlist Generator a robust tool for music curation, offering a unique and interactive experience for users.

## Technical component 1: scrapy
### Description and Logic of Web Scraping
In the Spotify Playlist Generator project, Scrapy, a fast high-level web crawling and web scraping framework, plays a pivotal role. The primary purpose of using Scrapy is to automate the process of extracting related words from the internet, which is crucial for building personalized playlists. The specific target for scraping is the website "relatedwords.io", known for its extensive repository of words and phrases associated with a given keyword. 

The logic behind this scraping process is straightforward yet effective. When a user inputs a keyword, such as a mood, genre, or artist, the Scrapy spider, named `wordsSpider` in the project, is triggered. This spider navigates to the "relatedwords.io" website, constructs a URL based on the user-provided keyword, and begins the scraping process. It fetches the first set of words closely related to the keyword, which are often direct synonyms or closely associated terms. Subsequently, the spider digs deeper, following links on the page to gather a broader range of related words and phrases. This comprehensive list of words becomes the foundation for searching and assembling songs in the Spotify playlist.

## Technical component 2: spotify API
After using Scrapy to find words related to the user topic, we began to work with the Spotify API. To use this resource, our group first created a Spotify developer account and created a Spotify app that provided us with a unique client ID and client secret. To facilitate working with the API we used the Python library, Spotipy. This library includes many easy-to-use functions that are helpful when sifting through and extracting Spotify data. In particular, we used the authentication function, search, audio features, create playlist, and add tracks to playlist functions. 

The process of working with the Spotify API is as follows. First, we were granted access to Spotify song data after calling the authentication function with our unique client ID and client secret. For each word related to the user topic, we used the search function to find various songs that contained that word in its title. From each song found, we made use of the audio features function to extract song data including the artist name, danceability, valence, etc. At this point, we briefly took a break from working with the spotipy library to filter the song data based on mood using SQL.

For a more personalized experience, we added the option to create a related words playlist based on mood as well. We classified four moods based on Thayer’s traditional classification of mood. This model classifies mood based on stress/valence, ranging from to positive or negative emotions, and energy, ranging from low to high energy. Based on these two parameters, we decided to filter songs based on the energy and valence features from Spotify API's audio features. According to the Spotify API, energy is the perceptual measure of intensity and activity, and valence is the musical positiveness in a track, both measured from 0.0 to 1.0. The four moods denote the four quadrants in Thayer’s model of mood: hype (positive valence, high energy); agitated (negative valence, high energy); sorrowful (negative valence, low energy); chill (positive valence, low energy).

To execute song filtering by mood, we opted to use an SQL database and create dataframes using SQL queries. We opted for this for a faster runtime, especially if the related words song dataframe was really large. For simplicity’s sake, for high valence or energy, the SQL query will fetch for values `>= 0.5`; SQL will also fetch for values `<= 0.5` for low valence or energy. The return of these mood filter functions is a dataframe that has all the results based on the SQL query. Finally, there is a final function defined as `user_input` that will be implemented into the larger `playlist.py` script to call upon the correct function based on user input. The function is called under the `generate_playlist` function, where the SQL connection is established for the filtering function to be executed.

Once we have a filtered set of songs, we are ready to create our Spotify playlist. We first used the create playlist function to create a playlist that has the user topic as its title and contains a brief description describing the mood of the songs in the playlist. Lastly, we used the add songs to playlist filter to add the filtered songs to our playlist.
Code snippet: example of 1 filtering function

## Technical component 3: flask
After coding all the components for creating a Spotify playlist, we decided to make a Flask app to allow users to easily run our code. The Flask app that we created has two text boxes, one for entering a topic and the other for entering a playlist mood. If a user inputs an invalid topic or mood, the Flask app will not deploy the code that generates the playlist. Instead, it will wait until the user changes their input to something valid. Once the form receives valid inputs and the user clicks the generate playlist button, the Flask app will run the code to create the playlist from start to finish. 

The Flask app generates the playlist in the background using a couple of helper functions. Upon providing valid inputs and clicking the generate playlist button, the Flask app calls the generate_playlist function with the topic and mood as parameters. Within this function, many other functions are called. The first function call is get_related_words which runs the Scrapy spider to find at most 100 words related to the user’s topic. Next, it calls the spotify_authentication function to allow access to the Spotify API and calls get_playlist_songs to find songs that have words related to the user topic in their title. The next function called excludes any songs that have a different mood than the user-specified one. The next few function calls create the user playlist with a relevant name and description and add songs to the playlist. Lastly, the generate function will return the URL of this playlist and our flask app redirects the user to this site.

This project was a fun way to apply the concepts we have learned in class to create an interesting product. It was especially rewarding to be able to experience our finished product by being able to listen to the playlists created. One of our main difficulties with this project was that in working with the Spotify API, there was a rate limit in which we can call on the API, and if we call on it often, we get a 429 error. The only remedy we were able to find was to wait about an hour or so after every call, and even longer if there are calls happening during the wait time.

There are no direct ethical ramifications for our product since we are not using the user’s information or account. There can be debate on the artists that may be randomly playlisted through this playlist generator and whether they should be given a platform, but at the end of the day, our project is intended to create lighthearted playlists for users and is focused on serving the user.

## Guidelines for Using the Flask App
1. Start the Flask App:
   Navigate to the project directory in your terminal or command prompt.
   Run the Flask app by executing python playlist_website.py.

2. Access the Web Interface:
   Open a web browser and go to http://localhost:5000 (or the address provided in the terminal).

3. Input Data:
   Enter a Topic (keyword related to your desired playlist, e.g., a genre, mood, artist).
   Choose a Mood (like 'hype', 'chill', etc.) that matches your desired playlist theme.

4. Generate Playlist:
   Click the "Generate Playlist" button to process your input.
   The app will create a Spotify playlist and redirect you to its Spotify page.

5. View Your Playlist:
   The redirected Spotify page will display your newly created playlist.

Thank you!



