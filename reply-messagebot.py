"""
Reply-Message-Bot

Status: Not Working/Not Tested/Not Finished 
"""
from peewee import *
import praw
import time
from _mysql import *

#--------------------------------------------------------------------------------------------
# Database stuff
#--------------------------------------------------------------------------------------------

# Insert your db credentials
db = MySQLDatabase('reddit', host='localhost', user='root', passwd='')
done = []
class Submissions(Model):
    subid = TextField()

    class meta:
        database = db

db.connect()
Submissions.create_table(True)

def is_added(submission_id):
    try:
        submissions = Submissions.get(Submissions.subid == submission_id)
        return True
    except:
        return False

def add_id(submission_id):
    if not is_added(submission_id):
        Submissions(subid=submission_id).save()

def flush():
    sub = Submissions.select()
    for x in sub:
        x.delete_instance()

def is_done(submission_id):
    if not submission_id in done and not is_added(submission_id):
        return True
#-------------------------------------------------------------------------------------------
# Bot code
#-------------------------------------------------------------------------------------------

user_name = raw_input('What is the bots name?: ')
password = raw_input('What is the bots password?: ')
USERAGENT = 'A bot that finds your username when mentioned and messages you a link to that thread'
recip = raw_input('Who is this message going to?: ')
MAXPOSTS = 100
WAIT = 30
SUBREDDIT = raw_input('What subreddit do you want to search?: ')
r = praw.Reddit(USERAGENT)
r.login(user_name,password)

def find_name():

    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=1)
    for comment in posts:
        postingid = comment.id
        if not is_done(postingid):
            try:
                comment_poster = comment.author.name
            except AttributeError:
                comment_poster = 'USER NO LONGER EXISTS'
            post_link = comment.permalink
            body = comment.body.lower()
            print(body)

while True:
    find_name()
    time.wait(WAIT)
