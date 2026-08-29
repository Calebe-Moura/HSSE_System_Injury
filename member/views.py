from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import FormUser

def list_user(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")

    users = User.objects.all().order_by("first_name", "last_name")

    return render(request, "member/list.html", {"users": users})


def edit_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = FormUser(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("list_user")

    else:
        form = FormUser(instance=user)

    return render(request, "member/edit.html", {"form": form})


def remove_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return redirect("start")
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect("list_user")

    return render(request, "member/list.html", {"user": user})