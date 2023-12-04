from flask import Flask, request, redirect, render_template_string
import requests
import playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        vibe = request.form['vibe']
        while (True):
            topic="-".join(keyword.split())
            r = requests.head(f"https://relatedwords.io/{topic}")
            
            if (r.status_code == 200):
                break
        url=playlist.generate_playlist(cid,cs,keyword,topic)
        return redirect(url) 
    return render_template_string('''
        <html>
            <body>
                <form method="post">
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
