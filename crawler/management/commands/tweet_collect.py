import tweepy
from django.core.management import BaseCommand

from core.models import Tweet, TwitterAcount
from core.utils.twitter import TweepyUtils


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        twitterの情報を取得する
        どんどん古い方に向かって取得していく
        """
        tweepy_util = TweepyUtils()
        for acount in TwitterAcount.objects.all().order_by("twitter_id"):
            for i in range(100):
                tweets = tweepy_util.get_old_tweet_from_max_id(acount)
                for tweet in tweets:
                    Tweet.create(acount, tweet)
