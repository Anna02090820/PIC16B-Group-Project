from flask import Flask, request, redirect, render_template_string,flash
import requests
app = Flask(__name__)
app.secret_key = 'generator'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        cid = request.form['cid']
        cs = request.form['cs']
        vibe = request.form['vibe']
        while (True):
            topic="-".join(keyword.lower().split())
            r = requests.head(f"https://relatedwords.io/{topic}")
            
            if (r.status_code == 200):
                break
                
        return redirect("https://www.youtube.com/results?search_query="+keyword) #just to test for now
        # playlist_url = user_playlist_create(user=user,name=f"{user_input.title()}  Playlist",public=False,description=f"This is a {user_input.title()} Themed Playlist")
    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    Enter Your Spotify Client ID: <input type="text" name="cid"/>
                <br>
                    Enter Your Spotify Client Secret: <input type="text" name="cs"/>
                <br>
                    Enter a Topic: <input type="text" name="keyword"/>
                <br>
                    Enter a Playlist Vibe: <input type="text" name="vibe"/>
                <br>
                    <input type="submit" value="Generate Playlist"/>
                </form>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)