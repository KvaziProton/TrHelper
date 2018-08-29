from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    is_translator = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class CloudAccount(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile_user'
    )
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    folder_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class ArticleCase(models.Model):
    published = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('published',)
        get_latest_by = 'published'


class Article(models.Model):
    case = models.ForeignKey(
        ArticleCase,
        on_delete=models.CASCADE,
        )
    translator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True)
    url = models.URLField()
    title = models.CharField(max_length=100)
    translated_title = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, null=True, blank=True)
    symbols_amount = models.IntegerField()
    published = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)
        #auto_now - автоматически ставит дату-время (datetime.datetime)
        #при каждом сохранении inst.save()
        #даные берет из настроек timezone

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=0,
        )
    img_url = models.URLField()
    loaded = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('published',)
        get_latest_by = 'last_change'


class TranslationStatistic(models.Model):
    translator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
        )
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        )
    translated = models.DateTimeField(auto_now_add=True)
    #ставит дату при создании
    symbols_ammount = models.IntegerField()

    def __str__(self):
        return self.translator, self.article
