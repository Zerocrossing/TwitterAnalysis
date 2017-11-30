"""Contains methods used to generate stasticics about tweets"""
#---------- IMPORTS ----------
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
import heapdict
import html
#---------- CONSTANTS ----------
STOPWORDS = set(stopwords.words('english'))

#---------- FUNCTIONS ----------
# Note that these functions are generalized and very redundant with eachother
# Once you know what datasets you'd like and in what form, consider writing your own functions to extract that data

def Get_Most_Used_Words(tweet_text, n):
    """Returns a list of the n most frequently used words"""
    #NOTE: Python only has support for a minheap so all the values are inverted until they are returned
    freq = heapdict.heapdict()
    output = []
    #Get frequency of words in all tweets
    for line in tweet_text:
        for word in line:
            if word in freq:
                freq[word]-=1
            else:
                freq[word] = 1
    #Return top n words
    for x in range(n):
        item = freq.popitem()
        item = item[0],-item[1]
        output.append(item)
    return output

def Remove_Stopwords(string, ignore_words = []):
    """Returns an array containing the individual words without stopwords or filterwords"""
    #Remove URLs
    remove = re.compile('https*[^ ]*') 
    string = html.unescape(string)
    string = re.sub(remove,"",string)
    #--- Below are several methods to tokenize words
    #--- The regex tokenize method used only grabs contiguous letters, meaning hashtags and words with numbers are filtered
    #words = string.split() #METHOD 1
    #words = word_tokenize(string) #METHOD 2
    reg = RegexpTokenizer(r'\w+') #METHOD 3 pt 1
    words = reg.tokenize(string.lower()) #METHOD 3 pt 2
    #Remove stop words from NLTK and words we've defined as ignore
    filter_words = STOPWORDS
    filter_words |= set(ignore_words)
    filtered = []
    #Iterate through the words in the tweet and remove ones we've decided to filter
    for word in words:
        if word in filter_words:
            continue
        filtered.append(word)
    return filtered

