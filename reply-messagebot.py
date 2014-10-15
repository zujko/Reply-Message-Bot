"""
Reply-Message-Bot

Status: Not Working/Not Tested/Not Finished 
"""
from peewee import *
import praw
import time
import sqlite3


# --------------------------------------------------------------------------------------------
# Database stuff
#--------------------------------------------------------------------------------------------
done = []

# Insert your db credentials
connection = sqlite3.connect('test.db')


def is_done(submission_id):
    if submission_id in done:
        return True
    else:
        return False

#-------------------------------------------------------------------------------------------
# Bot code
#-------------------------------------------------------------------------------------------
replytxt = 'COMMENT REPLY'
user_name = 'BOT USERNAME'
password = 'BOT PASSWORD'
USERAGENT = 'A bot that finds your username when mentioned and messages you a link to that thread'
recip = 'someuser'
MAXPOSTS = 100
WAIT = 30
SUBREDDIT = 'SUBREDDIT'
r = praw.Reddit(USERAGENT)
r.login(user_name, password)

def find_name():
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for comment in posts:
        postingid = comment.id
        if not is_done(postingid):
            try:
                comment_poster = comment.author.name
            except AttributeError:
                comment_poster = 'USER NO LONGER EXISTS'
            post_link = comment.permalink
            body = comment.body.lower()
           # message(post_link)
           # print('messaged')
            reply(comment)
            print('replied')
            

def reply(comment):
    comment.reply(replytxt)

def message(link):
    r.send_message(recip, 'You\'ve been mentioned!', 'Here is the link! ' + link, captcha=None)


while True:
    find_name()
    time.sleep(WAIT)
