from django.urls import path
from . import views

print('in url')
urlpatterns = [
    path('', views.ArticleFlow.as_view(), name='article_flow'),
    path('ajax/button_actions/', views.action, name='button_actions'),
    path('add/', views.CreateUser.as_view(), name='user_add'),
    path('user_list/', views.UserList.as_view()),

]
