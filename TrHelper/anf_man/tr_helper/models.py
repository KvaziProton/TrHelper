from django.contrib.auth.models import AbstractUser
from django.db import models


LANGUAGE_CHOICES = (
    ('0', 'english'),
    ('1', 'kurdi'),
    ('2', 'german'),
    ('3', 'espanol'),
    ('4', 'russian')
    )

DECISION_CHOICES = (
    ('0', 'new'),
    ('1', 'update'),
    ('2', 'user-choice'),
    ('3', 'found-version')
    )

class User(AbstractUser):
    is_translator = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)


class Translator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    language = models.CharField(
            max_length=5,
            choices=LANGUAGE_CHOICES,
            default=0,
            )

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


class ArticleCase(models.Model):
    pass


class Article(models.Model):
    case = models.ForeignKey(
        ArticleCase,
        on_delete=models.CASCADE,
        )
    translator = models.ForeignKey(
        Translator,
        on_delete=models.CASCADE,
        null=True, blank=True)
    url = models.URLField()
    title = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    symbols_amount = models.IntegerField()
    published = models.DateTimeField(auto_now_add=True)
        #автоматически ставит дату-время (datetime.datetime)
        #при каждом сохранении inst.save()
        #даные берет из настроек timezone
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=0,
        )
    img_url = models.URLField()

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
        )
    translated = models.DateTimeField(auto_now=True)
    #ставит дату при создании
    symbols_ammount = models.IntegerField()

    def __str__(self):
        return self.user.username, self.article.title


class Logger(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True, blank=True
        )



class TestLog(models.Model):
    article = models.CharField(max_length=100)
    img_index = models.IntegerField()
    text_index = models.IntegerField(null=True, blank=True)
    text_2 = models.IntegerField(null=True, blank=True)
    comp_article = models.ForeignKey(
        Logger,
        on_delete=models.CASCADE
        )
    decision = models.CharField(
        max_length=2,
        choices=DECISION_CHOICES,
        default=0,
        null=True, blank=True
        )
