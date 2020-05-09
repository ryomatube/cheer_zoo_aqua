import tweepy 
import json
import os

# Twitter APIで使用する各種キーをセット
# API Key
consumer_key = os.environ['CON_KEY']
# API secret key
consumer_secret = os.environ['CON_KEY_SEC']

# Twistantwinアカウントのアクセストークン
Access_token = os.environ['ACC_KEY']

# Twistantwinアカウントのアクセストークンシークレット
Access_token_secret = os.environ['ACC_KEY_SEC']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)

api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
    """ Handles tweets received from the stream. """

    def on_status(self, status):
        """ Prints tweet and hashtags """
        if "RT" not in status.text:
            print('------------------------------')
            print("@" + status.user.screen_name)
            print(status.text)
            print("")
            try:
                api.retweet(status.id)
            except:
                pass
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.filter(track=[os.environ['QUERY']], is_async=True)