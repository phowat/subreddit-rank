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


def count_in_day(posts): 
    one_day = 60 * 60 * 24
    day_count = 0 
    oldest_post = 0
    now = int(time.time())
    for post in posts:
        post_age = int((now - post.created_utc) / one_day)
        if oldest_post == post_age:
            day_count += 1
        elif day_count > 0 or post_age > 6:
            break
        else:
            oldest_post = post_age
            day_count += 1

    return (day_count, oldest_post)
    
@app.route('/')
def hello_world():
    sublist = ""
    subs = sorted(reddit.user.subreddits(), 
            key=lambda x: x.subscribers, reverse=True)
    subreddits = []
    for sub in subs:
        (day_count, oldest_post) = count_in_day(sub.new())
        
        subreddits.append({
            "display_name": sub.display_name,
            "subscribers": sub.subscribers,
            "public_description": sub.public_description,
            "over18": sub.over18,
            "activity_count":day_count,
            "oldest_post":oldest_post,
        })
    return render_template('index.html', subreddits=subreddits)
