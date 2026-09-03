from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import FormLogin, FormUser


def login_user(request):
    if request.method == "POST":
        form = FormLogin(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                redirect_to = request.GET.get("next", "start")
                return redirect(redirect_to)

    else:
        form = FormLogin()

    return render(request, "account/login.html", {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("login")


def register_user(request):
    if request.method == "POST":
        form = FormUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = FormUser()

    return render(request, "account/register.html", {"form": form})