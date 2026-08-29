from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .forms import FormUser


def list_user(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")

    users = User.objects.all().order_by("first_name", "last_name")

    return render(
        request,
        "member/user_list.html",
        {"users": users}
    )


def detail_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect("login")

    user = get_object_or_404(
        User,
        id=user_id
    )

    return render(
        request,
        "member/user_detail.html",
        {"my_user": user}
    )


def my_user(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "member/my_user_list.html",
        {"my_user": request.user}
    )


def edit_my_user(request):

    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

    if request.method == "POST":

        form = FormUser(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            return redirect("my_user")

    else:

        form = FormUser(
            instance=user
        )

    return render(
        request,
        "member/edit_my_user.html",
        {"form": form}
    )


def my_user_delete(request):

    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

    if request.method == "POST":

        logout(request)

        user.delete()

        return redirect("login")

    return render(
        request,
        "member/my_user_delete.html"
    )


def edit_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        form = FormUser(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            return redirect("list_user")

    else:

        form = FormUser(
            instance=user
        )

    return render(
        request,
        "member/user_edit.html",
        {"form": form}
    )


def remove_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        if user.id == request.user.id: # type: ignore
            return redirect("list_user")

        user.delete()

        return redirect("list_user")

    return render(
        request,
        "member/user_list.html",
        {"user": user}
    )
