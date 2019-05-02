import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import pandas as pd

class TwitterClient(object): 
  
    def __init__(self): 
          
        consumer_key = 'zY3lB8ZLtVUJzyFfyQQIFT2Aq'
        consumer_secret = 'fvfiu0G0qTaCGJJ26P7zsDhGvFLVUsjnByYzFsbsws1EBqXeZH'
        access_token = '1052672668250587139-OgyHtZwPDyg9TWHDrMlcy6DOvYMYgf'
        access_token_secret = '6m2fPMX921n4QzGqwkcRxAk8s8PP7cuP2vqNAjbVniaNF'


        try: 
            
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
            
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
                                

    def get_tweet_sentiment(self, tweet): 
       
       
        analysis = TextBlob(self.clean_tweet(tweet)) 
      
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count = 100): 
       
        tweets = [] 

        try: 
      
            fetched_tweets = self.api.search(q = query, count = count) 

        
            for tweet in fetched_tweets: 
             
                parsed_tweet = {} 

                parsed_tweet['text'] = tweet.text 
             
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

               
                if tweet.retweet_count > 0: 
                   
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

       
            return tweets 

        except tweepy.TweepError as e: 
       
            print("Error : " + str(e)) 

def main(name): 

    api = TwitterClient() 
   
    tweets = api.get_tweets(query = name, count = 1000) 

  
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
  
    positive =100*len(ptweets)/len(tweets)
    print("Positive tweets percentage: {} %".format(positive)) 
     
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
   
    negative = 100*len(ntweets)/len(tweets)
    print("Negative tweets percentage: {} %".format(negative))
    neutral =100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
    print("Neutral tweets percentage: {} % \ ".format(neutral)) 
            
    
    #printing Tweets

    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 

  
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text'])
        
    return (positive, negative, neutral)

if __name__ == "__main__": 
    
    name = None
    output =  None
    xl_data = pd.read_excel("input.xlsx")
    for index in xl_data.index:
        name = xl_data["name"][index]
        output = main(name) 
        xl_data["pos"][index] = output[0]
        xl_data["neg"][index] = output[1]
        xl_data["neu"][index] = output[2]
    xl_data.to_excel("output.xlsx",index=False)
    print("END")