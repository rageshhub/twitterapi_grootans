import requests
import json

"""
To fetch top 10 most retweeted tweets in past 5 days and store in json file

Using Twitter API v2 (Early Release)
"""


all_english_tweets = []    #It stores all english tweets
all_nonenglish_tweets =[]  #It stores all non english tweets
start_time = '2020-10-15T12:30:26.000Z' #Date in ISO 8601 format
max_results = 100  #Max tweets to fetch. Twitter allows only upto 100 in their API V2
search_query = 'corona' 

#Generate your own bearer token in twitter api dashboard
BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAAILUIwEAAAAAAdBacXqWjP6zB9MsNLO2fHgAHDk%3DoTrfnEwpcMPuGnqj8sZrIGCg9D2pxiAvSHhOXXX7ctfVrPgFmh'



"""
This function returns 100 tweets from last 5 days for the given search query
"""
def search_tweets():
    try:
        url = f'https://api.twitter.com/2/tweets/search/recent?query={search_query}&expansions=author_id&tweet.fields=public_metrics,created_at&max_results={max_results}&user.fields=name&start_time={start_time}'
    
        print(url)
        headers = {
        'Authorization': BEARER_TOKEN 
        }

        response = requests.request("GET", url, headers=headers)
        return json.loads(response.text)
    except Exception as e:
        print(e)

"""
The unwanted data is removed here and only the required data is retained

Required data: tweet, created time, retweet count, screen name
"""

def required_data(all_data):

    for tweet_data, user_data in zip(all_data['data'], all_data['includes']['users']):
        data = {}
        data['text'] = tweet_data['text']
        data['created_time'] = tweet_data['created_at']
        data['screen_name'] = user_data['username']
        data['retweet_count'] = tweet_data['public_metrics']['retweet_count']
        if(tweet_check(tweet_data['text'])): #checks whether the tweet is english or not
            all_english_tweets.append(data)
        else:
            all_nonenglish_tweets.append(data)
"""
tweet_check() 
It is used to find whether the tweet is any english or any other language

It returns true if the tweet is english else false
"""
def tweet_check(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    return True

"""
find_top(param)
It takes set of tweet data and sort them based on highest retweet count and returns it
"""

def find_top(top_tweets):
    return sorted(top_tweets, key=lambda x : (x['retweet_count']), reverse=True)
#Checks whether the tweet is english or not

"""
store_in_english(param, param)

This function takes in all english tweets and stores screen name and retweet count alone
in a json file
"""

def store_in_english(name, top_tweets):
    
    for tweet in top_tweets[:10]:
        del tweet['text']  #deletes unwanted data
        del tweet['created_time']
    with open(name, 'w+', encoding='utf-8') as f:
        json.dump(top_tweets[:10], f, ensure_ascii=False, indent=4)

"""
store_in_nonenglish(params, params)

This function takes in all NON english tweets and stores screen name, created time, hashtags(if available)
as comma seperated values
"""

def store_in_nonenglish(name, top_tweets):
    
    with open(name, 'w+', encoding='utf-8') as f:
        for tweet in top_tweets[:10]:
            tags = tweet['text']
            hashtags = {tag.strip("#") for tag in tags.split() if tag.startswith("#")}
            if len(hashtags)>=1:

                f.write(tweet['screen_name'] + ', ' + tweet['created_time'] + ', ' + ', '.join(hashtags) + '\n')
            else:
                f.write(tweet['screen_name'] +', ' + tweet['created_time'] + '\n')

"""
main() this is where the program starts to execute
"""

if __name__=="__main__":
    #Fetch all data
    all_data = search_tweets()
    print("Succesfully fetched")
    
    #clean the fetched data to get required fields
    required_data(all_data)
    print("Got required data")
    
    #fetch top tweet data
    top_english_tweets = find_top(all_english_tweets)
    top_nonenglish_tweets = find_top(all_nonenglish_tweets)

    #store top data
    store_in_english('retweets.json', top_english_tweets)
    store_in_nonenglish('nonenglishtweets.json', top_nonenglish_tweets)

    print('Finished storing')