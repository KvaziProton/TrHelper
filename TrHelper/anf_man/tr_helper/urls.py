from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleFlow.as_view(), name='article_flow'),
    path('add/', views.CreateUser.as_view(), name='user_add'),
    path('user_list/', views.UserList.as_view()),

]
