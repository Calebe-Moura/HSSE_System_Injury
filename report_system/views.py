from django.shortcuts import render, redirect
from incident.models import Injury, ActionInjury


def start(request):
    if not request.user.is_authenticated:
        return redirect("login")

    my_report_injury = (
        Injury.objects
        .filter(reported_by=request.user)
        .select_related("responsible")
        .prefetch_related("accident_types", "injury_types")
        .order_by("-date_incident")
    )

    my_action_injury = (
        ActionInjury.objects
        .filter(responsible=request.user)
        .select_related("injury")
        .order_by("-limit_date_action")
    )

    context = {
        "my_report": my_report_injury,
        "my_action": my_action_injury,
    }

    return render(
        request,
        "start/index.html",
        context,
    )