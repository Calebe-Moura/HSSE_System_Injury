from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # URLs que podem ser acessadas sem login
        login_not_required = [
            'login',
            'register',
        ]

        # Se o usuário NÃO estiver autenticado
        if not request.user.is_authenticated:

            # Se estiver tentando acessar uma página protegida
            if request.path == "/" not in login_not_required:
                return redirect('login')

        # Continua normalmente
        response = self.get_response(request)

        return response