#---------- TWITTER INTERFACE ----------
#   A simple text-based terminal interface
#   Used to launch the various methods of tweet retrieval
#   When the user has not specified any command line arguments


#---------- INTERFACE ----------
def Interface():
    """Asks the user which method of tweet retrieval they want to use"""
    print(Header("Rob's TwitterGetter",60))
    usrin=""
    while (True):
        usrin = input('Please enter "stream" to begin streaming tweets live, "scrape" to retrieve all tweets from a specific user, or "quit" to exit: ').lower()
        if usrin == "quit":
            quit()
        if usrin ==("stream" or "scrape"):
            break;
    if usrin =="stream":
        Stream_Interface()
    elif usrin == "scrape":
        pass #TODO 

#---------- STREAMING INTERFACE ----------
def Stream_Interface():
    """A simple text based interface to help the user open a stream"""
    print(Header("RWB Twitter Stream"))
    head = "Please select from the following options: "
    choices = [("filesize","Terminates when the output file reaches a certain size"),
               ("numtweets","terminates when a certain number of tweets have been collected"),
               ("time","terminates after a set amount of time"),
               ("none","terminate the stream manually")]
    Menu(head,choices)


#---------- HELPER FUNCTIONS ----------
def Header(text, len=40, fillchar="*"):
    """Makes a pretty looking header for output"""
    border = "\n"+fillchar*len+"\n"
    mid = text.center(len)
    return border + mid + border

def Menu(head, choices):
    """Creates a nicely formatted menu which displays the text of "head" and loops until a user chooses one of the choices"""
    #Choices is a list of tuples containing the keyword and a description
    while(True):
        print(head,'\n')
        for choice in choices:
            print("\t"+choice[0]+":\t"+choice[1]+'\n')
        usrin = input()
        if usrin in [choice[0] for choice in choices]:
            print("Thank you")
            break