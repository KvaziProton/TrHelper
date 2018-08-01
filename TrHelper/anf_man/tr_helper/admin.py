from django.contrib import admin
from .models import Article, ArticleCase, User, CloudAccount

admin.site.register(Article)
admin.site.register(ArticleCase)
admin.site.register(User)
admin.site.register(CloudAccount)
