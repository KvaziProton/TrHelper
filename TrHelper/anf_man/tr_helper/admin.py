from django.contrib import admin
from .models import Article, ArticleCase, Translator, User

admin.site.register(Article)
admin.site.register(ArticleCase)
admin.site.register(Translator)
admin.site.register(User)
