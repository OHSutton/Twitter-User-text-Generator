from twitterClient import TwitterClient
from markov import MarkovModel


# Enter your Twitter API Credentials here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


# ===========================================================
# Enter a Twitter handle
user_id = "realDonaldTrump"
tweet_max_length = 20

client = TwitterClient(consumer_key, consumer_secret, access_token, 
         access_token_secret)

# Downloads the tweets.  May take a while
all_tweets = client.fetch_tweets(user_id)

model = MarkovModel()
model.create_transition_dict(all_tweets)

# Generate a tweet of max length 20
print("\n" + model.generate_text(tweet_max_length)) 

# Save so next time you don't have to re-download the Tweets
model.save_model(user_id)

# ===========================================================
# Importing a saved markov model

model = MarkovModel.load_model(user_id)

# Generate a tweet of max length 20
print("\n" + model.generate_text(tweet_max_length)) 


