pip install Flask

from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        playlist_url = url
        return redirect(playlist_url)
    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    Enter a keyword: <input type="text" name="keyword"/>
                    <input type="submit" value="Generate Playlist"/>
                </form>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
