"""
Reply-Message-Bot

github.com/z-ko
"""
from peewee import *
import praw
import time


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
    Ids.create_table()  #Create table subid
except OperationalError:    #If it already exists, pass
    pass
    

def addid(submission_id):
    """
    Add the comment id to the database.
    """
    idnum = Ids()
    idnum.subid = submission_id
    idnum.save()
        

def is_done(submission_id):
    """ 
    Check if the comment id is already in the database
    return True if the comment id is in the database.
    Otherwise, return False
    """ 
    try:
        Ids.get(Ids.subid == submission_id)
        return True
    except DoesNotExist:
        return False
      
      

#-------------------------------------------------------------------------------------------
# Bot code
#-------------------------------------------------------------------------------------------
user_name = 'BOT USERNAME'
password = 'BOT PASSWORD'
USERAGENT = 'A bot that finds your username when mentioned and messages you a link to that thread'
recip = 'USER TO FIND IN COMMENTS AND MESSAGE'
MAXPOSTS = 100
WAIT = 30
SUBREDDIT = 'SUBREDDIT'
replytxt = ('/u/%s has been notified of your comment. \n\n-%s' % (recip, user_name))

r = praw.Reddit(USERAGENT)
r.login(user_name, password)

def find_name():
    """
    Get comments from specified subreddit.

    Loop through all comments, on each loop,
    get the comment id and poster username.
 
    If the comment id is not in the database and
    the comment poster is not the bot's username,
    get the comment body and split it.

    If the username we are looking for is in the list,
    get the link then message the user we are looking for
    and reply to the comment.  
    """
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for comment in posts:
        postingid = comment.id
        try:
            comment_poster = comment.author.name
        except AttributeError:
            comment_poster = 'USER NO LONGER EXISTS'
        if not is_done(postingid) and comment_poster != user_name: 
            body = comment.body.lower()
            lst = body.split()
            if recip in lst or '/u/'+recip in lst or 'u/'+recip in lst:
                print('user found')
                post_link = comment.permalink
                message(post_link, comment_poster)
                print('message sent')
                reply(comment)
                print('replied')
                addid(postingid)
                
                 

def reply(comment):
    """
    Reply to comment with replytxt
    """
    comment.reply(replytxt)

def message(link, poster):
    """
    Send a message to recip
    """
    r.send_message(recip,'/u/'+ poster + ' mentioned you in a comment!', 'Here is the link! %s \n\n-%s' % (link, user_name), captcha=None)


while True:
    find_name()
    print('waiting')
    time.sleep(WAIT)
