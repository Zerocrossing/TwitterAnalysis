#---------- Twitter Interface ----------
# RWBTwitter allows you to download and analyze tweets from the command line
# It requires tweepy and NLTK as its only non-standard modules
# The two main download modes are stream and get
# Stream will open a livestream that grabs tweets in realtime containing keywords
# Get will allow you to choose a user and download all the most recent tweets the API will allow (about 3000)
# There are some (Work In Progress) functions to allow you to analyze the tweets and print results
# See readme for more info

#---------- IMPORTS ----------
import os
import sys
import html
import Twitter_Stream
import Tweet_Getter
import Tweet_Parser
import Tweet_Stats
import Twitter_Interface

#---------- FUNCTIONS ----------
def Create_Analysis_File(tweets, output_filename=None, title = "Twitter Analysis"):
    """Takes either a filename or a list of tweets and creates an analysis file"""
    #--- Read input file ---
    if type(tweets) == str:
        if title == "Twitter Analysis": #default title given, use filename instead
            title = tweets.replace(".txt", "")
            if output_filename is None: #no output filename given, use the filename as the output
                output_filename = title +" analysis.txt"
        tweets = Tweet_Parser.Get_Tweets_From_File(tweets)
    #--- Create output file ---
    if output_filename is None:
        print("No title given and no filename to draw analysis from, using default filename of untitled analysis.txt")
        output_filename = "untitled analysis.txt"
    out_file = open(output_filename, "w+", encoding='utf-8')
    out_file.write(Header(title, 60)[1:])
    #--- Collect Data ---
    #Rewtweeted
    top_retweeted = sorted(tweets, key=lambda tweet: tweet["retweet_count"], reverse=True)[:10]
    top_retweeted = [(Get_Text(x), x["retweet_count"]) for x in top_retweeted] #creates a tuple of (text,retweet_count)
    #Favourited
    top_favourited = sorted(tweets, key=lambda tweet: tweet["favorite_count"], reverse=True)[:10]
    top_favourited = [(Get_Text(x), x["favorite_count"]) for x in top_favourited] #creates a tuple of (text,favourite_count)

    #--- Write Data ---
    #Headers
    out_file.write("Total number of tweets: " + str(len(tweets)) +"\n")
    out_file.write("Average tweet length: " + str(round(sum([len(x["text"]) for x in tweets])/len(tweets)))+"\n") #TODO: CALCULATE THIS ELSEWHERE
    out_file.write("Earliest tweet created on: " +str(tweets[-1]["created_at"]) + "\n")
    out_file.write("Most recent tweet created on: " +str(tweets[0]["created_at"]) + "\n")
    out_file.write(Header("Most Retweeted"))
    #Top retweeted
    for tweet in top_retweeted:
        out_file.write(str(tweet[1]) + " retweets:\n")
        out_file.write(str(tweet[0])+"\n\n")
    out_file.write(Header("Most Favorited"))
    #Top favourited
    for tweet in top_favourited:
        out_file.write(str(tweet[1]) + " favorites:\n")
        out_file.write(str(tweet[0])+"\n\n")


#---------- HELPER FUNCTIONS ----------
def Header(text, len=40, fillchar="*"):
    """Makes a pretty looking header for output"""
    border = "\n"+fillchar*len+"\n"
    mid = text.center(len)
    return border + mid + border

def Get_Text(tweet):
    """Returns the text of a tweet"""
    return html.unescape(tweet["text"])

#---------- INTERFACE FUNCTION ----------

def Stream_Interface(args=[]):
    """A simple text based interface to help the user open a stream"""
    print(Header("RWB Twitter Stream"))
    if len(args) == 0:
        search_terms = input("You have decided to open a twitter stream. Please enter the terms you would like to search for, seperated by commas: ")
        conditions_done = False
        while not conditions_done: 
            stop_conditions = input(
                "\nHow would you like to stop the stream? \nYou may choose multiple values seperated by commas:"
                "\n\t0: None (Terminate Process Manually)"
                "\n\t1: Stop after time elapsed"
                "\n\t2: Stop after number of tweets collected"
                "\n\t3: Stop after filesize\n"
            )
            if "0" in stop_conditions:
                print("The process will be terminated manually")
                conditions_done = True


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        Twitter_Interface.Interface()
    #    print(Header("Rob's Twitter Interface"))
    #    usr_continue = False
    #    while not usr_continue:
    #        usrin = input('Please enter "stream" to begin streaming tweets live, "scrape" to retrieve all tweets from a specific user, or "quit" to exit: ').lower()
    #        if usrin == "stream":
    #            Stream_Interface(args)
    #elif args[1].lower() == "stream":
        #Stream_Interface(args[2:])
    #Tweet_Getter.Get_All_Tweets_From_User("@TheEllenShow",write_to_file=True)
    #Tweet_Parser.Get_Tweets_From_File("@TheEllenShow.txt")
    #Twitter_Stream.Open_Stream(["#halloween"],"halloween stream.txt",stop_on_filesize=True,stop_size=5e9)
    #Create_Analysis_File("@barackobama.txt")
    #Create_Analysis_File("@realDonaldTrump.txt")
