"""Prediction of User based on tweet embeddings."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


def predict_user(user0_name, user1_name, tweet_text):
    """
    Determine and retrun which user is more likely to say a given Tweet.

    Example run: predict_user('jackblack', 'elonmusk', 'Tesla, woohoo!')
    Returns 0 (user0_name) or 1 (user1_name)
    """

    # makes sure the users being compared are the inputted users
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    # makes the embedding array for the users so BASILICA can analyze
    user0_embeddings = np.array([tweet.embedding for tweet in user0.tweets])
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])

    # puts both embeddings into a single array to analyze
    embeddings = np.vstack([user0_embeddings, user1_embeddings])
    #
    labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # fits a LR model, training on embeddings and uses labels test
    log_reg = LogisticRegression().fit(embeddings, labels)
    # pulls BASILICA embeddings for the user-inputted text
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
