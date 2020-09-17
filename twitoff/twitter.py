""" Retrieve Tweets, embeddings and persist in the database"""

from os import getenv
import tweepy
import basilica
from .models import DB, Tweet, User

TWITTER_USERS = ['jackblack', 'elonmusk', 'nasa', 'SteveMartinToGo',
                 'alyankovic', 'sadserver', 'jk_rowling', 'austen',
                 'common_squirrel', 'conanobrien', 'big_ben_clock']

# Hides API keys in .env
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
# Authorization to use the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(getenv('BASILICA_KEY'))


# create user based on the username with associated tweets
def add_or_update_user(username):
    try:
        # getting the user info from Tweepy API - look at line
        twitter_user = TWITTER.get_user(username)
        # add or update user for the API database
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # grabbing the tweet
        # max of 200 tweets, then remove all replies and retweets
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False,
                                       tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print('ERROR PROCESSING {}: {}'.format(username, e))
    else:
        DB.session.commit()

# How to store a tweet and then basillica analyzes it
# use this code in a Python Repl
# tweet_text = tweets[0].text
# embedding = b.embed_sentence(tweet_text, model='twitter')
# len(embedding)


def insert_example_users():
    # creating base Twitter users
    # IF we run multiple times then we will get error
    # because these users already exist in the database
    DB.drop_all()
    DB.create_all()
    for example in TWITTER_USERS:
        try:
            add_or_update_user(example)
        except Exception as e:
            print('User {} is already in the database').format(example)
        else:
            pass
