from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_translator = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)


class Translator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    language = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Editor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.username


class Article(models.Model):
    translator = models.ForeignKey(
        Translator,
        on_delete=models.CASCADE,
        null=True, blank=True)
    url = models.URLField()
    title = models.CharField(max_length=100)
    symbols_amount = models.IntegerField()
    published = models.DateTimeField(auto_now_add=True)
    is_eng = models.BooleanField(default=True)
    #автоматически ставит дату-время (datetime.datetime)
    #при каждом сохранении inst.save()
    #даные берет из настроек timezone

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('published',)


class TranslationStatistic(models.Model):
    translator = models.ForeignKey(
        Translator,
        on_delete=models.CASCADE,
        null=True, blank=True
        )
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    translated = models.DateTimeField(auto_now=True)
    #ставит дату при создании
    symbols_ammount = models.IntegerField()

    def __str__(self):
        return self.user.username, self.article.title
