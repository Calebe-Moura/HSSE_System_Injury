from django.shortcuts import render, redirect
from django.db.models import Q

from incident.models import Injury, ActionInjury


def start(request):

    if not request.user.is_authenticated:
        return redirect("login")

    # ============================================================
    # MY REPORTS
    # Reports where the current user is either:
    # - the responsible person
    # - the person who reported the incident
    # ============================================================

    my_report_injury = (
        Injury.objects
        .filter(
            Q(responsible=request.user) |
            Q(reported_by=request.user)
        )
        .select_related(
            "responsible",
            "reported_by",
        )
        .prefetch_related(
            "accident_types",
            "injury_types",
        )
        .order_by("-date_incident")
        .distinct()
    )

    # ============================================================
    # MY ACTIONS
    # Actions where the current user is responsible
    # ============================================================

    my_action_injury = (
        ActionInjury.objects
        .filter(
            responsible=request.user
        )
        .select_related(
            "injury",
            "responsible",
        )
        .order_by("-limit_date_action")
    )

    # ============================================================
    # CONTEXT
    # ============================================================

    context = {
        "my_report": my_report_injury,
        "my_action": my_action_injury,
    }

    return render(
        request,
        "start/index.html",
        context,
    )