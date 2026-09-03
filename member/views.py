from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.models import User
from django.contrib.auth import logout

from .forms import FormUser
from .models import PhotoUser


# ================================================================
# HELPER
# ================================================================

def is_authenticated(request):
    """
    Verifica se o usuário está autenticado.
    """

    return request.user.is_authenticated


def is_superuser(request):
    """
    Verifica se o usuário atual é superuser.
    """

    return request.user.is_superuser


# ================================================================
# USER LIST
# ================================================================

def list_user(request):

    if not is_authenticated(request):
        return redirect("login")

    if not is_superuser(request):
        return redirect("start")

    users = (
        User.objects
        .select_related("profile_photo")
        .all()
        .order_by(
            "first_name",
            "last_name",
            "username",
        )
    )

    return render(
        request,
        "member/user_list.html",
        {
            "users": users,
        }
    )


# ================================================================
# USER DETAIL
# ================================================================

def detail_user(request, user_id):

    if not is_authenticated(request):
        return redirect("login")

    if not is_superuser(request):
        return redirect("start")

    user = get_object_or_404(
        User.objects.select_related("profile_photo"),
        id=user_id,
    )
    
    

    return render(
        request,
        "member/user_detail.html",
        {
            "my_user": user,
        }
    )


# ================================================================
# MY PROFILE
# ================================================================

def my_user(request):

    if not is_authenticated(request):
        return redirect("login")

    user = (
        User.objects
        .select_related("profile_photo")
        .get(pk=request.user.pk)
    )

    return render(
        request,
        "member/my_user_list.html",
        {
            "my_user": user,
        }
    )


# ================================================================
# EDIT MY PROFILE
# ================================================================

def edit_my_user(request):

    if not is_authenticated(request):
        return redirect("login")

    user = request.user

    # ------------------------------------------------------------
    # POST
    # ------------------------------------------------------------

    if request.method == "POST":

        form = FormUser(
            request.POST,
            request.FILES,
            instance=user,
            allow_superuser_change=False,
        )

        if form.is_valid():

            form.save()

            return redirect("my_user")

    # ------------------------------------------------------------
    # GET
    # ------------------------------------------------------------

    else:

        form = FormUser(
            instance=user,
            allow_superuser_change=False,
        )

    return render(
        request,
        "member/my_user_edit.html",
        {
            "form": form,
            "my_user": user,
        }
    )


# ================================================================
# DELETE MY ACCOUNT
# ================================================================

def my_user_delete(request):

    if not is_authenticated(request):
        return redirect("login")

    user = request.user

    # ------------------------------------------------------------
    # POST
    # ------------------------------------------------------------

    if request.method == "POST":

        logout(request)

        user.delete()

        return redirect("login")

    # ------------------------------------------------------------
    # GET
    # ------------------------------------------------------------

    return render(
        request,
        "member/my_user_delete.html"
    )


# ================================================================
# EDIT USER - ADMIN
# ================================================================

def edit_user(request, user_id):

    if not is_authenticated(request):
        return redirect("login")

    if not is_superuser(request):
        return redirect("start")

    user = get_object_or_404(
        User,
        id=user_id,
    )

    # ------------------------------------------------------------
    # POST
    # ------------------------------------------------------------

    if request.method == "POST":

        form = FormUser(
            request.POST,
            request.FILES,
            instance=user,
            allow_superuser_change=True,
        )

        if form.is_valid():

            form.save()

            return redirect("list_user")

    # ------------------------------------------------------------
    # GET
    # ------------------------------------------------------------

    else:

        form = FormUser(
            instance=user,
            allow_superuser_change=True,
        )

    return render(
        request,
        "member/user_edit.html",
        {
            "form": form,
            "my_user": user,
        }
    )


# ================================================================
# REMOVE USER - ADMIN
# ================================================================

def remove_user(request, user_id):

    if not is_authenticated(request):
        return redirect("login")

    if not is_superuser(request):
        return redirect("start")

    user = get_object_or_404(
        User,
        id=user_id,
    )

    # ------------------------------------------------------------
    # POST
    # ------------------------------------------------------------

    if request.method == "POST":

        # Não permite que o administrador exclua
        # a própria conta.

        if user.pk == request.user.pk:
            return redirect("list_user")

        user.delete()

        return redirect("list_user")

    # ------------------------------------------------------------
    # GET
    # ------------------------------------------------------------

    return render(
        request,
        "member/user_delete.html",
        {
            "user": user,
        }
    )