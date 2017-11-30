"""Opens a live twitter stream filtered to contain all words in FILTER_TERMS and appends the tweet as a line in JSON format to TEXT_FILE"""

# This file combined with Tweet_Parser.py is all you need to save and extract Twitter data
# It has been left intentionally sparse for a reason
# Tweepy is the only non-standard library import required
# You must have 4 tokens for API access from https://apps.twitter.com/ stored in an .ini file in the same directory as this script
# More complex functionality is available from other files in this project if you want to use them

#IMPORTS
import os
import time
import configparser
import json
#TWEEPY
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#CONSTANTS
#OUTPUT_FILENAME = "tweets.txt"
TOKEN_FILENAME = "tokens.ini"
#TOKENS
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#---------- FUNCTIONS ----------

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

class Twitter_Listener(StreamListener):
    """A tweepy listener that appends all the tweets in JSON format to output_filename"""
    num_tweets = 0
    output_filename = "/tweets/stream.txt"
    def on_data(self, data):
        """Runs whenever data is recieved"""
        #TODO can we get away with not loading the JSON and just writing directly?
        self.num_tweets += 1
        tweet = json.loads(data)
        f = open(self.output_filename,"a+")
        print("Tweet Collected: ",self.num_tweets)
        f.write(json.dumps(tweet)+'\n')
        f.close()
        if self.stop_cons.Conditions_Met(self.num_tweets,self.output_filename):
            return False
        return True

    def on_error(self, status):
        print (status)

class Stop_Conditions():
    """A class that holds information on when the listener should stop, has some reasonable default values"""
    stop_on_filesize = True
    stop_size =  1e8 #in bytes
    stop_after_time = True
    start_time = time.time()
    stop_time = 600 #in seconds
    stop_after_numtweets = True
    stop_numtweets = 1000

    def __init__(self, stop_on_filesize, stop_size, stop_after_time, stop_time, stop_after_numtweets, stop_numtweets):
            self.stop_on_filesize = stop_on_filesize
            self.stop_size =  stop_size
            self.stop_after_time = stop_after_time
            self.start_time = time.time()
            self.stop_time = stop_time
            self.stop_after_numtweets = stop_after_numtweets
            self.stop_numtweets = stop_numtweets

    def Conditions_Met(self,numtweets,output_file):
        """Takes in present conditions and checks them against the stop conditions, returning true if any are met"""
        if self.stop_after_numtweets and numtweets >= self.stop_numtweets:
            print ("Maximum number of tweets collected. Stopping stream...")
            return True
        if self.stop_after_time and time.time()-self.start_time >= self.stop_time:
            print("Collection time exceeded. Stopping stream...")
            return True
        if self.stop_on_filesize and os.stat(output_file).st_size >= self.stop_size:
            print("Maximum filesize exceeded. Stopping stream...")
            return True
        return False


def Open_Stream(filter_words , output_file, stop_on_filesize = False, stop_size=1e8, stop_after_time = False, stop_time = 600, stop_after_numtweets = False, stop_numtweets = 1000):
    """Opens a stream listening for all words in the list filter_words and writes them to output_file"""
    print("Opening stream at",time.strftime("%a, %d %b %Y %H:%M:%S"))
    #--- Tweepy auth and stream ---
    tokens = Get_Tokens()
    auth = OAuthHandler(tokens["consumer_key"], tokens["consumer_secret"])
    auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])
    stop = Stop_Conditions(stop_on_filesize,stop_size,stop_after_time,stop_time,stop_after_numtweets,stop_numtweets)
    #--- Create stop conditions object and append to listener ---
    stop_cons = Stop_Conditions(stop_on_filesize,stop_size,stop_after_time,stop_time,stop_after_numtweets,stop_numtweets)
    l =  Twitter_Listener()
    l.stop_cons = stop_cons
    l.output_filename = output_file
    #--- Open stream ---
    stream = Stream(auth, l)
    stream.filter(track=filter_words)
