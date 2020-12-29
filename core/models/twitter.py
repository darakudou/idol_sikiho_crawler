from django.db import models


class TwitterAcount(models.Model):
    idol = models.ForeignKey("core.idol", on_delete=models.CASCADE)
    twitter_id = models.BigIntegerField(primary_key=True, db_index=True)

    @property
    def max_id(self):
        try:
            return self.tweet_set.order_by("-tweet_id")[0]
        except IndexError:
            return None

    @property
    def min_id(self):
        try:
            return self.tweet_set.order_by("tweet_id")[0]
        except IndexError:
            return None


class Tweet(models.Model):
    acount = models.ForeignKey("TwitterAcount", on_delete=models.CASCADE)
    tweet_id = models.BigIntegerField(db_index=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField()
    favorite_count = models.IntegerField()
    retweet_count = models.IntegerField()
    pictures = models.ManyToManyField("Picture", related_name="tweets")
    retweeted = models.BooleanField(default=False)

    @classmethod
    def create(cls, acount, tweet):
        defaults = dict()
        defaults["id"] = tweet.id
        defaults["created_at"] = tweet.created_at
        defaults["text"] = tweet.full_text
        defaults["retweeted"] = tweet.retweeted
        defaults["favorite_count"] = tweet.favorite_count
        defaults["retweet_count"] = tweet.retweet_count
        defaults["acount"] = acount

        cls.objects.get_or_create(tweet_id=tweet.id, defaults=defaults)
        # pictureの作成
        if hasattr(tweet, "extended_entities"):
            for media in tweet.extended_entities["media"]:
                Picture.objects.get_or_create(url=media["media_url_https"])
        # hashtagの作成


class Picture(models.Model):
    url = models.URLField()


class HashTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
