from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # URLs que podem ser acessadas sem login
        login_not_required = [
            "/login/",
            "/register/",
        ]

        # Usuário NÃO autenticado
        if not request.user.is_authenticated:

            if request.path == "/" not in login_not_required:
                return redirect("login")

        # Usuário autenticado
        else:
            # Se acessar a raiz
            if request.path == "/":
                return redirect("start")

        return self.get_response(request)