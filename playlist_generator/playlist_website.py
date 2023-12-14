from flask import Flask, request, redirect, render_template_string
import requests
import playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        mood = request.form['mood'].lower() 
        while (True):
            topic="-".join(keyword.split())
            r = requests.head(f"https://relatedwords.io/{topic}")
            
            if (r.status_code == 200 and mood in ["hype","agitated","sorrowful","chill"] ):
                break
        url=playlist.generate_playlist(keyword,topic,mood)
        return redirect(url) 
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
    ''')

if __name__ == '__main__':
    app.run(debug=True)
