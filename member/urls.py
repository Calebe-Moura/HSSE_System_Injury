from django.urls import path
from member import views

urlpatterns = [
    path("users/", views.list_user, name="list_user"),
    path("users/<int:user_id>/edit/", views.edit_user, name="edit_user"),
    path("users/<int:user_id>/remove/", views.remove_user, name="remove_user"),
]
