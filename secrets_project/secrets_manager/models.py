from django.db import models


class Secret(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name="Identifier of the secret")
    password = models.CharField(max_length=300, verbose_name="Encoded password of the secret")
    extra = models.TextField(default='', blank=True, verbose_name="Additional information about the secret")

    def __str__(self):
        return self.title
