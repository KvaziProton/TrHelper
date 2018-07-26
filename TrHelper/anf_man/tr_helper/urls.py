from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleFlow.as_view(), name='article-flow'),
    
]
