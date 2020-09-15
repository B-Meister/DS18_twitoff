"""SQLAlchemy models and utility functions for TwitOff!"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter Users corresponding to Tweets in the database"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Tweets has a max of 280 characters
    # Increased limits to 350 for all attachments/links/etc.
    text = DB.Column(DB.Unicode(350))

    # Creating a user id that is the same as the one we created in User class, relates the database
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # back referencing that acts as a join and allows us to know name associated with tweet
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    # creating base Twitter users
    # IF we run multiple times then we will get error
    # because these 2 users already exist in database
    jack = User(id=1, name='jackblack')
    elon = User(id=1, name='elonmusk')
    DB.session.add(jack)
    DB.session.add(elon)
    DB.session.commit()


def insert_tweets():
    tweet1 = Tweet(id=1, text="What if we went to Pluto", user_id=1)
    tweet2 = Tweet(id=2, text="Nachos are the best", user_id=2)
    tweet3 = Tweet()
    tweet4 = Tweet()
    tweet5 = Tweet()
    tweet6 = Tweet()
    DB.session.add(tweet1)
    DB.session.add(tweet2)
    DB.session.add(tweet3)
    DB.session.add(tweet4)
    DB.session.add(tweet5)
    DB.session.add(tweet6)
    DB.session.commit()


