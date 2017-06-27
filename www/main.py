from flask import Flask, send_from_directory, render_template
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/css/<path:path>')
def static_css(path):
    return send_from_directory('css',path)

@app.route('/js/<path:path>')
def static_js(path):
    return send_from_directory('js',path)

@app.route('/img/<path:path>')
def static_img(path):
    return send_from_directory('img',path)


@app.route('/')
def main():
    return render_template("page.html",hello = "hello world")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
