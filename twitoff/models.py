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
    embedding = DB.Column(DB.PickleType, nullable=False)

    # Creating a user id that is the same as the one we created in User class, relates the database
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # back referencing that acts as a join and allows us to know name associated with tweet
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def tweetTest():
    pass
