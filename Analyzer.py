import tweepy
import numpy as np
import time
from tqdm import tqdm

from secrets import consumer_key, consumer_secret, access_token, access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getUserFavorites(api, username, limit):
    res = np.array([])
    itr = tweepy.Cursor(api.favorites, user=username).items(limit)

    while True:
        try:
            for favorite in tqdm(itr, unit="tweet", desc=username):
                res = np.append(res, favorite)

            np.save( res, "./downloaded/"+username+".db")
            return res
        except tweepy.TweepError as e:
            if e.reason == "Twitter error response: status code = 429":
                print("Rate Limit !")
                time.sleep(15 * 60)
                print("Hi !")
            else:
                raise e

def getAllFavorites(api, usersList, limit):
    res = {}
    for username in tqdm(usersList):
        res[username] = getUserFavorites(api, username, limit)
    return res

def get_friends(api, username, limit):
    itr = tweepy.Cursor(api.friends, screen_name=username).items(limit)

    while True:
        try:
            for friend in itr:
                getUserFavorites(api, friend._json['screen_name'], 10000)
        except tweepy.TweepError as e:
            if e.reason == "Twitter error response: status code = 429":
                print("Rate Limit !")
                time.sleep(15 * 60)
                print("Hi !")
            else:
                raise e

usersList = ['sadeghhayeri']
# data = getAllFavorites(api,usersList, 1000)
get_friends(api, "sadeghhayeri", 100)
