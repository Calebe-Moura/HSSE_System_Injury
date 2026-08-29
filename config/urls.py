from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('user/', include('member.urls')),
    path('', include('report_system.urls')),
    path('', include('incident.urls')),
]
