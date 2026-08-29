from django.urls import path
from report_system import views

urlpatterns = [
    path("", views.start, name="start"),
    path("hub/", views.hub, name="hub")
]
