from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.TrView.set_ru),
    path(r'translit', views.TrView.set_ru),
    path(r'transtit/<str:kurd_input>', views.TrView.set_ru),
    path(r'add_term/', views.TrView.add_term),
    path(r'dict', views.show_dict),
]
