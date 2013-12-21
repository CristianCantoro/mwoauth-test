import os
import ConfigParser as configparser
from flask import Flask
from flask_mwoauth import MWOAuth

app = Flask(__name__)
app.secret_key = os.urandom(24)

print """
NOTE: The callback URL you entered when proposing an OAuth consumer
probably did not match the URL under which you are running this development
server. Your redirect back will therefore fail -- please adapt the URL in
your address bar to http://localhost:5000/oauth-callback?oauth_verifier=...etc
"""

BASEDIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILENAME = 'keys.cfg'
CONFIG_FILE = os.path.realpath(
    os.path.join('..', '..', 'wtosm', 'keys.cfg'))

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

consumer_key = config.get('keys', 'consumer_key')
consumer_secret = config.get('keys', 'consumer_secret')

mwoauth = MWOAuth(consumer_key=consumer_key, consumer_secret=consumer_secret)
app.register_blueprint(mwoauth.bp)


@app.route("/")
def gcu():
    username = repr(mwoauth.get_current_user(False))
    return "logged in as: " + username + "<br>" + \
           "<a href=login>login</a> / <a href=logout>logout</a>"

if __name__ == "__main__":
    app.run(debug=True)
