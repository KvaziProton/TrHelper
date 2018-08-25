from rest_framework import serializers
from .models import Article, ArticleCase, User

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

# class CaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArticleCase
#         fields = '__all__'
#
# class TranslatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username')
