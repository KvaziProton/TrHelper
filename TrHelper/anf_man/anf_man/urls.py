from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^', include('tr_helper.urls')),
    url(r'^admin/statuscheck/', include('celerybeat_status.urls')),
]
