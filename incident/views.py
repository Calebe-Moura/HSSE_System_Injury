from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.utils import timezone

from .models import (
    Injury,
    TypeAccident,
    TypeInjury,
    ActionInjury,
)

from .forms import (
    InjuryForm,
    ActionInjuryForm,
)

from incident.management import can_manage_injury, can_manage_action


# ============================================================
# INJURY LIST
# ============================================================

@login_required
def injury_list(request):

    injuries = (
        Injury.objects
        .select_related(
            "reported_by",
            "responsible",
        )
        .prefetch_related(
            "accident_types",
            "injury_types",
            "actions",
        )
        .order_by("-date_incident")
    )

    actions = (
        ActionInjury.objects
        .select_related(
            "injury",
            "responsible",
        )
        .order_by("limit_date_action")
    )

    count_total = injuries.count()
    count_open = injuries.filter(status="OPE").count()
    count_closed = injuries.filter(status="CLO").count()
    count_actions = actions.count()

    context = {
        "injuries": injuries,
        "actions": actions,
        "count_total": count_total,
        "count_open": count_open,
        "count_closed": count_closed,
        "count_actions": count_actions,
    }

    return render(
        request,
        "injury/injury_list.html",
        context,
    )

# ============================================================
# INJURY DETAIL
# ============================================================

@login_required
def injury_detail(request, injury_id):

    injury = get_object_or_404(
        Injury.objects
        .select_related(
            "reported_by",
            "responsible",
        )
        .prefetch_related(
            "accident_types",
            "injury_types",
            "actions__responsible",
        ),
        pk=injury_id,
    )

    context = {
        "injury": injury,
        "can_manage": can_manage_injury(
            request.user,
            injury,
        ),
    }

    return render(
        request,
        "injury/injury_detail.html",
        context,
    )


# ============================================================
# INJURY CREATE
# ============================================================

@login_required
def injury_create(request):

    if request.method == "POST":

        form = InjuryForm(
            request.POST
        )

        if form.is_valid():

            with transaction.atomic():

                injury = form.save(
                    commit=False
                )

                # ============================================
                # DEFAULT REPORTED BY
                # ============================================

                if not injury.reported_by:
                    injury.reported_by = request.user

                injury.save()

                # ============================================
                # TYPE ACCIDENT
                # ============================================

                accident_types = form.cleaned_data.get(
                    "type_accident",
                    [],
                )

                for accident_name in accident_types:

                    TypeAccident.objects.create(
                        injury=injury,
                        name=accident_name,
                    )

                # ============================================
                # TYPE INJURY
                # ============================================

                injury_types = form.cleaned_data.get(
                    "type_injury",
                    [],
                )

                for injury_name in injury_types:

                    TypeInjury.objects.create(
                        injury=injury,
                        name=injury_name,
                    )

            messages.success(
                request,
                "Injury created successfully.",
            )

            return redirect(
                "injury_detail",
                injury_id=injury.pk,
            )

    else:

        form = InjuryForm(
            initial={
                "reported_by": request.user,
                "date_report": timezone.now().strftime(
                    "%Y-%m-%dT%H:%M"
                ),
            }
        )

    context = {
        "form": form,
        "title": "Create Injury",
        "button_text": "Create Injury",
    }

    return render(
        request,
        "injury/injury_form.html",
        context,
    )


# ============================================================
# INJURY UPDATE
# ============================================================

@login_required
def injury_update(request, injury_id):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_injury(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to edit this injury.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        form = InjuryForm(
            request.POST,
            instance=injury,
        )

        if form.is_valid():

            with transaction.atomic():

                injury = form.save()

                # ============================================
                # REMOVE OLD ACCIDENT TYPES
                # ============================================

                TypeAccident.objects.filter(
                    injury=injury
                ).delete()

                # ============================================
                # CREATE NEW ACCIDENT TYPES
                # ============================================

                accident_types = form.cleaned_data.get(
                    "type_accident",
                    [],
                )

                for accident_name in accident_types:

                    TypeAccident.objects.create(
                        injury=injury,
                        name=accident_name,
                    )

                # ============================================
                # REMOVE OLD INJURY TYPES
                # ============================================

                TypeInjury.objects.filter(
                    injury=injury
                ).delete()

                # ============================================
                # CREATE NEW INJURY TYPES
                # ============================================

                injury_types = form.cleaned_data.get(
                    "type_injury",
                    [],
                )

                for injury_name in injury_types:

                    TypeInjury.objects.create(
                        injury=injury,
                        name=injury_name,
                    )

            messages.success(
                request,
                "Injury updated successfully.",
            )

            return redirect(
                "injury_detail",
                injury_id=injury.pk,
            )

    # ========================================================
    # GET
    # ========================================================

    else:

        form = InjuryForm(
            instance=injury,
        )

    context = {
        "form": form,
        "injury": injury,
        "title": "Update Injury",
        "button_text": "Update Injury",
    }

    return render(
        request,
        "injury/injury_form.html",
        context,
    )


# ============================================================
# INJURY DELETE
# ============================================================

@login_required
def injury_delete(request, injury_id):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_injury(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to delete this injury.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    if request.method == "POST":

        cod_sys = injury.cod_sys

        injury.delete()

        messages.success(
            request,
            f"Injury {cod_sys} was deleted successfully.",
        )

        return redirect(
            "injury_list"
        )

    context = {
        "injury": injury,
    }

    return render(
        request,
        "injury/injury_delete.html",
        context,
    )


# ============================================================
# CLOSE INJURY
# ============================================================

@login_required
def closed_report(request, injury_id):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_injury(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to close this injury.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # ONLY OPEN CAN BE CLOSED
    # ========================================================

    if injury.status != "OPE":

        messages.warning(
            request,
            "This injury is already closed.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # ONLY POST
    # ========================================================

    if request.method != "POST":

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # CLOSE
    # ========================================================

    injury.status = "CLO"

    injury.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        f"Injury {injury.cod_sys} was successfully closed.",
    )

    return redirect(
        "injury_detail",
        injury_id=injury.pk,
    )


# ============================================================
# ACTION CREATE
# ============================================================

@login_required
def action_create(request, injury_id):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_action(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to add an action.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # INJURY MUST BE OPEN
    # ========================================================

    if not injury.is_open:

        messages.warning(
            request,
            "This injury is closed. You cannot add actions.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        form = ActionInjuryForm(
            request.POST
        )

        if form.is_valid():

            action = form.save(
                commit=False
            )

            action.injury = injury

            action.save()

            messages.success(
                request,
                "Action created successfully.",
            )

            return redirect(
                "injury_detail",
                injury_id=injury.pk,
            )

    else:

        form = ActionInjuryForm()

    context = {
        "form": form,
        "injury": injury,
        "title": "Add Action",
        "button_text": "Create Action",
    }

    return render(
        request,
        "injury/action_form.html",
        context,
    )


# ============================================================
# ACTION UPDATE
# ============================================================

@login_required
def action_update(
    request,
    injury_id,
    action_id,
):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    action = get_object_or_404(
        ActionInjury,
        pk=action_id,
        injury=injury,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_action(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to edit this action.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # INJURY MUST BE OPEN
    # ========================================================

    if not injury.is_open:

        messages.warning(
            request,
            "This injury is closed. Its actions cannot be modified.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # COMPLETED ACTION CANNOT BE UPDATED
    # ========================================================

    if action.status == "COM":

        messages.warning(
            request,
            "Completed actions cannot be edited.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        form = ActionInjuryForm(
            request.POST,
            instance=action,
        )

        if form.is_valid():

            # ================================================
            # PROTECT COMPLETED DATE LOGIC
            # ================================================

            action = form.save(
                commit=False
            )

            # ================================================
            # IF STATUS BECOMES COMPLETED
            # ================================================

            if action.status == "COM":

                if not action.completed_date_action:

                    action.completed_date_action = (
                        timezone.now()
                    )

            action.save()

            messages.success(
                request,
                "Action updated successfully.",
            )

            return redirect(
                "injury_detail",
                injury_id=injury.pk,
            )

    else:

        form = ActionInjuryForm(
            instance=action,
        )

    context = {
        "form": form,
        "injury": injury,
        "action": action,
        "title": "Update Action",
        "button_text": "Update Action",
    }

    return render(
        request,
        "injury/action_form.html",
        context,
    )


# ============================================================
# COMPLETE ACTION
# ============================================================

@login_required
def closed_action(
    request,
    injury_id,
    action_id,
):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    action = get_object_or_404(
        ActionInjury,
        pk=action_id,
        injury=injury,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_action(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to complete this action.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # INJURY MUST BE OPEN
    # ========================================================

    if not injury.is_open:

        messages.warning(
            request,
            "This injury is closed. Its actions cannot be modified.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # ACTION MUST BE ACTIVE
    # ========================================================

    if action.status != "ACT":

        messages.warning(
            request,
            "This action is already completed or expired.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # ONLY POST
    # ========================================================

    if request.method != "POST":

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    action.status = "COM"

    action.completed_date_action = timezone.now()

    action.save(
        update_fields=[
            "status",
            "completed_date_action",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Action was successfully completed.",
    )

    return redirect(
        "injury_detail",
        injury_id=injury.pk,
    )


# ============================================================
# ACTION DELETE
# ============================================================

@login_required
def action_delete(
    request,
    injury_id,
    action_id,
):

    injury = get_object_or_404(
        Injury,
        pk=injury_id,
    )

    action = get_object_or_404(
        ActionInjury,
        pk=action_id,
        injury=injury,
    )

    # ========================================================
    # PERMISSION
    # ========================================================

    if not can_manage_action(
        request.user,
        injury,
    ):
        messages.error(
            request,
            "You do not have permission to delete this action.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # INJURY MUST BE OPEN
    # ========================================================

    if not injury.is_open:

        messages.warning(
            request,
            "This injury is closed. Its actions cannot be modified.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # COMPLETED ACTION CANNOT BE DELETED
    # ========================================================

    if action.status == "COM":

        messages.warning(
            request,
            "Completed actions cannot be deleted.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        action.delete()

        messages.success(
            request,
            "Action deleted successfully.",
        )

        return redirect(
            "injury_detail",
            injury_id=injury.pk,
        )

    context = {
        "injury": injury,
        "action": action,
    }

    return render(
        request,
        "injury/action_delete.html",
        context,
    )