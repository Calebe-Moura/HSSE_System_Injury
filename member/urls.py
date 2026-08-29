from django.urls import path

from .views import (
    list_user,
    detail_user,
    edit_user,
    edit_my_user,
    remove_user,
    my_user,
    my_user_delete,
)


urlpatterns = [

    path(
        "",
        list_user,
        name="list_user"
    ),

    path(
        "<int:user_id>/",
        detail_user,
        name="detail_user"
    ),

    path(
        "<int:user_id>/edit/",
        edit_user,
        name="edit_user"
    ),

    path(
        "<int:user_id>/remove/",
        remove_user,
        name="remove_user"
    ),

    path(
        "my_profile/",
        my_user,
        name="my_user"
    ),

    path(
        "profile/edit/",
        edit_my_user,
        name="edit_my_user"
    ),

    path(
        "profile/delete/",
        my_user_delete,
        name="my_user_delete"
    ),
]
