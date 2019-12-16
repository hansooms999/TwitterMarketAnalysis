
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
import json
import api_access
import TDstock
import threading


class TwitterClient():
    def __init__(self,user=None):

        #variable created to pass credentials to OAuthHandler to handle authentication
        auth = OAuthHandler(api_access.consumer_key, api_access.consumer_secret)

        #finishes authentication
        auth.set_access_token(api_access.access_token, api_access.access_token_secret)

        self.twitter_client = API(auth)
        self.twitter_user = user

    def getUserTimelineTweets(self,numTweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return(tweets)

    def getFriends(self,num_friends):
        friendList = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friendList.append(friend)
        return(friend)

    def streamUserTweets(self,stream):
        return(True)

#class streams and processes live tweets
class TwitterStreamer():

    def stream_tweets(self,tweetsFile, keywords,users):
        
        #listener object
        listener = TwitterListener(tweetsFile)
            
        #variable created to pass credentials to OAuthHandler to handle authentication
        auth = OAuthHandler(api_access.consumer_key, api_access.consumer_secret)
        #finishes authentication
        auth.set_access_token(api_access.access_token, api_access.access_token_secret)
        
        #create a stream passing authentication and listener object we created
        stream = Stream(auth, listener)
        
        #depending on if keyword or user is given as parameter, filter stream by what is given
        if len(keywords) > 0:
            if len(users) > 0:
                stream.filter(track=keywords,follow=users)
            else :
                stream.filter(track=keywords)
        elif len(users) > 0:
            stream.filter(follow=users)
        else:
            stream.userstream(_with="following")

    def stream_user_tweets(self, tweetsFile, users):
        
        #listener object
        listener = TwitterListener(tweetsFile)
        
        #variable created to pass credentials to OAuthHandler to handle authentication
        auth = OAuthHandler(access_second.consumer_key, access_second.consumer_secret)
        #finishes authentication
        auth.set_access_token(access_second.access_token, access_second.access_token_secret)
        
        #create a stream passing authentication and listener object we created
        stream = Stream(auth, listener)
        
        #This line filters (filter method from stream class) takes parameter list (track)
        stream.filter(follow=users)

#This is a basic listener that just prints received tweets to Twitter output. Inherits from StreamListener Class.
class TwitterListener(StreamListener):
    
    def __init__(self,tweetsFile):
        self.tweetsFile = tweetsFile
    
    #Overriding on_data and on_error method from StreamListener class
    #will take in data from StreamListener and we can deal with it however we want
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            t = threading.Thread(target=TDstock.search_tweet, args=(json_data,))
            t.start()
            return(True)
        except BaseException as e:
            print("Error on data: " + str(e))
            return(True)

    #what happens when an error occurs
    def on_error(self, status):
        
	    #nice
        if status == 420:
            print("Rates Limit has been exceeded")
            return(False)
        print (status)

#main method
if __name__ == '__main__':
    
    keywords = ['stocks']
    file = "tweetsFile.json"
    users = []

    twitterStreamer = TwitterStreamer()
    twitterStreamer.stream_tweets(file,keywords,users)



