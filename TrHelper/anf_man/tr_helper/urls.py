from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.ArticleFlow.as_view(), name='article_flow'),
    path(
        'ajax/button_actions/',
        views.ButtonActions.as_view(),
        name='button_actions'
        ),
    path('add/', views.CreateUser.as_view(), name='user_add'),
    path('user_list/', views.UserList.as_view()),
    path('file/', views.HandleFiles.as_view(), name='handle_file'),
    path('ajax_refresh/', views.flow_refresh, name='flow_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
