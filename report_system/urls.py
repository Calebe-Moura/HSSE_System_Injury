from django.urls import path
from report_system import views

urlpatterns = [
    path("start/", views.start, name="start"),
]
