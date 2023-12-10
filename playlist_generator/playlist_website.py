from flask import Flask, request, redirect, render_template_string
import requests
import playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        while (True):
            topic="-".join(keyword.split())
            r = requests.head(f"https://relatedwords.io/{topic}")
            
            if (r.status_code == 200):
                break
        url=playlist.generate_playlist(keyword,topic)
        return redirect(url) 
    return render_template_string('''
        <html>
            <style>
            body  {
              background-image: url("https://playliststreams.com/wp-content/uploads/2020/04/abstract-spotify-desktop-wallpaper-62370-64314-hd-wallpapers.jpg");
            }
            h2 {
              color: white;
              text-align: center;
            }
            </style>
            
            <title> Playlist Generator </title>
            
            <div class="container"><br>
            <center>
            <h2>
            Enter a Topic to Generate a Spotify Playlist
            🎵🕺</h2>
            </center>
            </div>
            
            <form action = ""method="post" style="text-align:center" novalidate>
            <input type="text" name="keyword">
            <input type="submit" value="Generate Playlist"/>
            </form>
            </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
