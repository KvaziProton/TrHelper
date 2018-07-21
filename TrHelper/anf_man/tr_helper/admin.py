from django.contrib import admin
from .models import Article, ArticleCase, Logger, TestLog

admin.site.register(Article)
admin.site.register(ArticleCase)
admin.site.register(Logger)
admin.site.register(TestLog)
