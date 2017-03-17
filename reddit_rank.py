import requests
import requests.auth
import pprint
import praw
from flask import Flask, render_template
from os import environ
app = Flask(__name__)
reddit = praw.Reddit(
    client_id=environ["REDDIT_CLIENT_ID"],
    client_secret=environ["REDDIT_CLIENT_SECRET"],
    password=environ["REDDIT_PASSWORD"],
    user_agent=environ["REDDIT_USER_AGENT"],
    username=environ["REDDIT_USERNAME"])


@app.route('/')
def hello_world():
    sublist = ""
    subs = sorted(reddit.user.subreddits(), 
            key=lambda x: x.subscribers, reverse=True)
#    for sub in subs:
#        sublist += "{} - {} <br>".format(sub.display_name, sub.subscribers)
    return render_template('index.html', subreddits=subs)
