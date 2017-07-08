from flask import Flask, send_from_directory, render_template
from redis import Redis

import www.counter

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
    return render_template("page.html")

@app.errorhandler(404)
def fourzerofour(e):
    return render_template("404.html",quote="När jag var sexton drömde jag om \
    världsrevolutionen. Nu är jag fyrtio - och planerar för den.")

app.register_blueprint(www.counter.bp)
#url_prefix='/counter/'

def start_server(debug = False):
    app.run(host="0.0.0.0", debug = debug)
