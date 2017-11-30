#---------- IMPORTS ----------
import os
import time
import configparser
import json
import tweepy

#---------- CFG ----------
TOKEN_FILENAME = "tokens.ini"

def Get_Tokens(filename=TOKEN_FILENAME):
    """Gets tokens from a local INI file and return them in a dict"""
    #if no token file is found create one with the appropriate paths
    if not os.path.isfile(filename):
        config_write = open(filename,"w+")
        config = configparser.ConfigParser()
        config.add_section("TOKENS")
        config.set("TOKENS","access_token","")
        config.set("TOKENS","access_token_secret","")
        config.set("TOKENS","consumer_key","")
        config.set("TOKENS","consumer_secret","")
        config.write(config_write)
        print("ERROR: file ", filename, " not found. It has been created in the working directory, please enter the appropriate token values")
        quit()
    #if the file exists get the token values from it
    config = configparser.ConfigParser()
    tokens = {}
    config.read(TOKEN_FILENAME)    
    tokens["access_token"] = config.get("TOKENS","access_token")
    tokens["access_token_secret"] = config.get("TOKENS","access_token_secret")
    tokens["consumer_key"] = config.get("TOKENS","consumer_key")
    tokens["consumer_secret"] = config.get("TOKENS","consumer_secret")
    return tokens

def Get_All_Tweets_From_User(screen_name, write_to_file = False, filename = None):
    #Tweepy authentication
    tokens = Get_Tokens()
    auth = tweepy.OAuthHandler(tokens["consumer_key"], tokens["consumer_secret"])
    auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])
    api = tweepy.API(auth)
    #Download most recent tweets and set the oldest ID to be equal to the last tweet
    tweets = []
    print("Fetching tweets from",screen_name,"...")
    newtweets = api.user_timeline(screen_name = screen_name,count=200)
    #Exctract the raw JSON data from the tweepy status object
    for tweet in newtweets:
        tweets.append(tweet._json)
    oldest = newtweets[-1].id - 1
    #Concinue to extract the previous 200 tweets until the api returns nothing
    while (len(newtweets) > 0):
        newtweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        if len(newtweets)==0:
            break
        oldest = newtweets[-1].id - 1
        for tweet in newtweets:
            tweets.append(tweet._json)
        print("current tweet count: ",len(tweets))
    #dump tweets to a JSON file
    if filename==None:
        filename = screen_name + ".txt"
    if write_to_file:
        Write_Tweets_To_File(tweets,filename)
    return tweets

def Write_Tweets_To_File(tweets,filename):
    """Writes tweets to a file line by line to resemble the twitter stream"""
    f = open(filename,"w+")
    for tweet in tweets:
        f.write(json.dumps(tweet)+'\n')
    f.close()
    print("wrote ", len(tweets), " tweets to ", filename)
