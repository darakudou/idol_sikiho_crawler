import environ
import tweepy


class TweepyUtils():

    def __init__(self):
        """
        tweepy.API
        :return: tweepy.API
        """
        env = environ.Env()
        env.read_env(".env")
        consumer_token = env("CONSUMER_TOKEN")
        consumer_secret = env("CONSUMER_SECRET")
        access_token = env("ACCESS_TOKEN")
        access_secret = env("ACCESS_SECRET")

        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def get_old_tweet_from_max_id(self, acount):

        # 今持っているデータの最小値を最大値としてAPIを取得する(DB上の最小値より前が欲しいため）
        if max_id := acount.min_id:
            return self.api.user_timeline(id=acount.twitter_id, tweet_mode='extended', max_id=max_id)
        return self.api.user_timeline(id=acount.twitter_id, tweet_mode='extended')
