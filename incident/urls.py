from django.urls import path

from incident import views


urlpatterns = [

    # ========================================================
    # INJURY
    # ========================================================

    path(
        "injuries/",
        views.injury_list,
        name="injury_list",
    ),

    path(
        "injuries/create/",
        views.injury_create,
        name="injury_create",
    ),

    path(
        "injuries/<int:injury_id>/",
        views.injury_detail,
        name="injury_detail",
    ),

    path(
        "injuries/<int:injury_id>/update/",
        views.injury_update,
        name="injury_update",
    ),

    path(
        "injuries/<int:injury_id>/delete/",
        views.injury_delete,
        name="injury_delete",
    ),

    path(
        "injuries/<int:injury_id>/close/",
        views.closed_report,
        name="closed_report",
    ),

    # ========================================================
    # ACTION
    # ========================================================

    path(
        "injuries/<int:injury_id>/actions/create/",
        views.action_create,
        name="action_create",
    ),

    path(
        "injuries/<int:injury_id>/actions/<int:action_id>/update/",
        views.action_update,
        name="action_update",
    ),

    path(
        "injuries/<int:injury_id>/actions/<int:action_id>/delete/",
        views.action_delete,
        name="action_delete",
    ),

    path(
        "injuries/<int:injury_id>/actions/<int:action_id>/complete/",
        views.closed_action,
        name="closed_action",
    ),
]