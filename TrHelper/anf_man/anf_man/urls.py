from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tr_helper.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('tr_helper.urls')),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
