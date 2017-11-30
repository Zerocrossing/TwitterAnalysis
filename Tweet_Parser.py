"""Reads JSON tweets line by line from a file"""
#Tweet Parser contains functions to extract tweets from files on the HD
#---------- IMPORTS ----------
import json
import pandas as pd
#---------- FUNCTIONS ----------
def Get_Tweets_From_File(filename):
    """Returns a list of all tweets in a file. Tweets must be on seperate lines in the JSON format"""
    tweets = []
    file = open(filename,"r")
    for line in file:
        tweet = json.loads(line)
        tweets.append(tweet)
    print("Unpacked ",len(tweets)," tweets from ",filename)
    file.close()
    return tweets   

def Get_Only_Headers_From_File(filename,headers,get_hashtags = True):
    """Takes a filename and a list of attributes and returns a list of lists of those attributes in order"""
    #TODO: Have a boolean as to whether or not a tweet contains URLs or Media
    tweets = []
    file = open(filename,"r")
    for line in file:
        tweet = json.loads(line)
        cleaned_tweet = []
        for attribute in headers:
            if attribute == "hashtags": continue
            cleaned_tweet.append(tweet.get(attribute))
        if get_hashtags:
            hashtags = []
            for hashtag in tweet.get("entities").get("hashtags"):
                if hashtag == None: break
                hashtags.append(hashtag.get("text"))
            if len(hashtags) > 0:
                cleaned_tweet.append(hashtags)
        tweets.append(cleaned_tweet)
    if get_hashtags and not ("hashtags" in headers):
        headers.append("hashtags")
    return tweets

def Get_Panda_Dataframe_From_File(filename,headers,get_hashtags = True,offset_time = True):
    """Takes a list of twitter headers and returns a nicely formatted pandas dataframe"""
    raw_tweets = Get_Only_Headers_From_File(filename,headers,get_hashtags)
    if offset_time:
        f = open(filename,"r")
        tweet = json.loads(f.readline())
        time_offset = tweet["user"]["utc_offset"]
    tweets = pd.DataFrame(raw_tweets,columns = headers)
    #Exceptions
    for n,attr in enumerate(headers):
        #Convert time to pandas time
        if attr == "created_at":
            tweets.created_at = pd.to_datetime(tweets.created_at)
            if offset_time:
                tweets.created_at += pd.Timedelta(str(time_offset)+" seconds")
            tweets.set_index("created_at",inplace = True)
        #Parse retweets to booleans and rename column
        elif attr == "retweeted_status":
            tweets["retweeted_status"] = tweets["retweeted_status"].notnull()
            #tweets.columns = tweets.columns.str.replace("retweeted_status","is_retweet").str.title()
    #tweets.columns = tweets.columns.str.replace("_"," ").str.title()
    return tweets
