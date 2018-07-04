from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_translator = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    last_active = models.DateTimeField(blank=True, null=True)


class Translator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.username


class Editor(model.Models):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.username


class Articles(models.Model):
    translalor = models.ForeignKey(
        Translator,
        on_delete=models.CASCADE,
        blank=True)
    url = models.URLField()
    title = models.CharField(max_length=100)
    published_datetime = models.DateTimeField(auto_now_add=True)
    #автоматически ставит дату-время (datetime.datetime)
    #при каждом сохранении inst.save()
    #даные берет из настроек timezone

    def __str__(self):
        return self.title


class TranslationStatistic(models.Model):
    translalor = models.ForeignKey(
        Translator,
        on_delete=models.CASCADE
        )
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    translation_added = models.DateTimeField(auto_now=True)
    #ставит дату при создании
    symbols_ammount = models.IntegerField()

    def __str__(self):
        return self.user.username, self.article.title
