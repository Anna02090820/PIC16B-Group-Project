from flask import Flask, request, redirect, render_template_string
import requests
import playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    This function repeatedly takes user input from the form 
    until the input is valid. The valid input is then used to 
    call the generate playlist function. After successfully creating
    a playlist, this function returns a call to redirect the user to the
    playlist Spotify page.
    """
    if request.method == 'POST':
        keyword = request.form['keyword'].lower() #gets keyword from form
        mood = request.form['mood'].lower() #gets mood from form
        while (True):
            #app repeatedly takes user input until both are valid
            topic="-".join(keyword.split()) #formats keyword into a topic
            r = requests.head(f"https://relatedwords.io/{topic}") #checks to see if the user topic can be found on relatedwords.io
            
            if (r.status_code == 200 and mood in ["hype","agitated","sorrowful","chill"] ):
                #if user topic and mood are valid break out of while loop
                break
        url=playlist.generate_playlist(keyword,topic,mood) #calls generate playlist function 
        return redirect(url) #redirects the user to the generated playlist on Spotify
    return render_template_string('''
        <html>
            <style>
            body  {
              background-image: linear-gradient(darkgreen, black);
              font-family: arial;
              display:flex; 
              flex-direction:column; 
              justify-content:center;
              min-height:100vh;
              color: white;
              text-align: center;
            }
            </style>
            
            <title> Playlist Generator </title>
            
            <div class="container"><br>
            <center>
            <h2>
            Enter a Topic to Generate a Spotify Playlist
            🎵🕺
            </h2>
            </center>
            </div>
            
            <form action = ""method="post" style="text-align:center" novalidate>
            Topic: <input type="text" name="keyword">
            <br>
            Mood: <input type="text" name="mood">
            <br>
            <br>
            <input type="submit" value="Generate Playlist"/>
            </form>
            </html>
    ''') #template string used to format the flask webpage

if __name__ == '__main__':
    app.run(debug=True)
