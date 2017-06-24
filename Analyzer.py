import tweepy
import numpy as np
import time
from tqdm import tqdm
import os

from secrets import consumer_key, consumer_secret, access_token, access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getUserFavorites(api, username, limit):
    res = np.array([])
    itr = tweepy.Cursor(api.favorites, user=username).items(limit)
    print( username )

    while True:
        try:
            for favorite in itr:
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
    for username in usersList:
        res[username] = getUserFavorites(api, username, limit)
    return res

def get_friends(api, username, limit):
    itr = tweepy.Cursor(api.friends, screen_name=username).items()

    while True:
        try:
            for friend in itr:
                get_tweets(api, friend._json['screen_name'], limit)
        except tweepy.TweepError as e:
            if e.reason == "Twitter error response: status code = 429":
                print("Rate Limit !")
                time.sleep(15 * 60)
                print("Hi !")
            else:
                raise e

def get_tweets(api, username, limit):
    if not os.path.isfile("./downloaded/" + username + ".db.ny"):
        itr = tweepy.Cursor(api.user_timeline, screen_name=username).items(limit)
        res = np.array([])
        print( username )

        while True:
            try:
                for status in tqdm(itr):
                    res = np.append(res, status)
                np.save("./downloaded/"+username+".db", res)
                return res
            except tweepy.TweepError as e:
                if e.reason == "Twitter error response: status code = 429":
                    print("Rate Limit !")
                    time.sleep(15 * 60)
                    print("Hi !")
                else:
                    raise e
    else:
        print(username, " exist!")

# data = getAllFavorites(api,usersList, 1000)

while True:
    try:
        get_friends(api, "sadeghhayeri", 5000)
    except:
        print("some errors! start over!")
