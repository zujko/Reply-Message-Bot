"""
Reply-Message-Bot

github.com/z-ko
"""
from peewee import *
import praw
import time
import sqlite3


# --------------------------------------------------------------------------------------------
# Database stuff
#--------------------------------------------------------------------------------------------


db = SqliteDatabase('DATABASE FILE')
db.connect()

class CustomModel(Model):
    class Meta:
        database = db

class Ids(CustomModel):
    subid = CharField()

try:
    Ids.create_table()
except OperationalError:
    pass
    

def addid(submission_id):
    idnum = Ids()
    idnum.subid = submission_id
    idnum.save()
    
    
def is_done(submission_id):
    for subiddb in Ids.select():
        if subiddb.subid == submission_id:
            return True 
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
           # print('message sent')
           # reply(comment)
           # print('replied')
            addid(postingid)
                 

def reply(comment):
    comment.reply(replytxt)

def message(link):
    r.send_message(recip, 'You\'ve been mentioned!', 'Here is the link! ' + link, captcha=None)


while True:
    find_name()
    print('waiting')
    time.sleep(WAIT)
