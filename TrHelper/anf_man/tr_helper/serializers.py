from rest_framework import serializers
from .models import Article, Translator, TranslationStatistic

class TranslatorSingUpSer(serializers.ModelSerializer):

    class Meta:
        model = Translator

class TranslatorAccountSer(serializers.ModelSerializer):

    class Meta:
        model = Translator
        fields = ('id', 'username', 'password')


class TranslationStatistic(serializers.ModelSerializer):

    class Meta:
        model = TranslationStatistic


class ArticleSer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'translalor', 'url', 'title',
            'symbols_ammount', 'published'
        )

class ArticleAddSer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('url',)
