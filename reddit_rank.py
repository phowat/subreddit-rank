import requests
import requests.auth
import pprint
import praw
from flask import Flask, render_template
from os import environ
import time 

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
    now = int(time.time())
    one_day = 60 * 60 * 24
    subreddits = []
    for sub in subs:
        day_count = 0
        for post in sub.new():
            post_age = now - post.created_utc 
            if post_age > one_day: 
                break
            day_count += 1
        
        subreddits.append({
            "display_name": sub.display_name,
            "subscribers": sub.subscribers,
            "public_description": sub.public_description,
            "over18": sub.over18,
            "activity_count":day_count,
        })
    return render_template('index.html', subreddits=subreddits)
