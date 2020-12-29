from django.db import models


class Idol(models.Model):
    name = models.CharField(max_length=255)
