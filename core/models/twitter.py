from django.db import models


class TwitterAcount(models.Model):
    idol = models.ForeignKey("core.idol", on_delete=models.CASCADE)
    twitter_id = models.BigIntegerField(primary_key=True, db_index=True)

    def __str__(self):
        return self.idol.name

    @property
    def max_id(self):
        try:
            return self.tweet_set.order_by("-tweet_id")[0]
        except IndexError:
            return None

    @property
    def min_id(self):
        try:
            return self.tweet_set.order_by("tweet_id")[0].tweet_id
        except IndexError:
            return None


class Tweet(models.Model):
    acount = models.ForeignKey("TwitterAcount", on_delete=models.CASCADE)
    tweet_id = models.BigIntegerField(db_index=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField()
    favorite_count = models.IntegerField()
    retweet_count = models.IntegerField()
    retweeted = models.BooleanField(default=False)

    pictures = models.ManyToManyField("Picture", related_name="tweets")
    hashtags = models.ManyToManyField("HashTag", related_name="tweets")

    def __str__(self):
        return f"{self.acount.idol.name}-{self.text[0: 25]}"

    @classmethod
    def create(cls, acount, tweet_info):
        defaults = dict()
        defaults["id"] = tweet_info.id
        defaults["created_at"] = tweet_info.created_at
        defaults["text"] = tweet_info.full_text
        defaults["retweeted"] = tweet_info.retweeted
        defaults["favorite_count"] = tweet_info.favorite_count
        defaults["retweet_count"] = tweet_info.retweet_count
        defaults["acount"] = acount

        tweet, _ = cls.objects.get_or_create(tweet_id=tweet_info.id, defaults=defaults)

        # pictureの作成
        if hasattr(tweet_info, "extended_entities"):
            pics = []
            for media in tweet_info.extended_entities["media"]:
                pic, _ = Picture.objects.get_or_create(url=media["media_url_https"])
                pics.append(pic)
            tweet.pictures.set(pics)

        # hashtagの作成
        if hasattr(tweet, "entities"):
            hashtags = []
            for hashtag in tweet["entities"]["hashtags"]:
                ht = HashTag.objects.get_or_create(name=hashtag)
                hashtags.append(ht)
            tweet.hashtags.set(hashtags)


class Picture(models.Model):
    url = models.URLField()


class HashTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
