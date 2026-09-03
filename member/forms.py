from django import forms
from django.contrib.auth.models import User

from .models import PhotoUser


class FormUser(forms.ModelForm):
    """
    Formulário de criação/edição de usuários.

    allow_superuser_change:
        False -> não permite alterar is_superuser.
        True  -> permite alterar is_superuser.

    O padrão é False por segurança.
    """

    # ============================================================
    # PROFILE PHOTO
    # ============================================================

    photo = forms.ImageField(
        required=False,
        label="Profile Photo",
        widget=forms.ClearableFileInput(
            attrs={
                "class": (
                    "block w-full text-sm text-slate-600 "
                    "file:mr-4 file:rounded-lg file:border-0 "
                    "file:bg-blue-50 file:px-4 file:py-2 "
                    "file:text-sm file:font-semibold "
                    "file:text-blue-700 "
                    "hover:file:bg-blue-100"
                )
            }
        ),
    )

    # ============================================================
    # SUPERUSER
    # ============================================================

    is_superuser = forms.BooleanField(
        required=False,
        label="Super User",
        widget=forms.CheckboxInput(
            attrs={
                "class": "checkbox",
            }
        ),
    )

    # ============================================================
    # PASSWORD
    # ============================================================

    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Confirm password",
                "autocomplete": "new-password",
            }
        ),
    )

    # ============================================================
    # META
    # ============================================================

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_superuser",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "First name",
                    "autocomplete": "given-name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Last name",
                    "autocomplete": "family-name",
                }
            ),

            "username": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Username",
                    "autocomplete": "username",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "input",
                    "placeholder": "E-mail",
                    "autocomplete": "email",
                }
            ),
        }

    # ============================================================
    # INIT
    # ============================================================

    def __init__(
        self,
        *args,
        allow_superuser_change=False,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.allow_superuser_change = allow_superuser_change

        # --------------------------------------------------------
        # SUPERUSER PERMISSION
        # --------------------------------------------------------

        if not self.allow_superuser_change:
            # Remove completamente o campo quando não autorizado.
            self.fields.pop("is_superuser", None)

        # --------------------------------------------------------
        # UPDATE
        # --------------------------------------------------------

        if self.instance and self.instance.pk:

            # Nunca deixa o password existente aparecer.
            self.fields["password1"].initial = None
            self.fields["password2"].initial = None

            # Se o campo existir, mostra o valor atual.
            if "is_superuser" in self.fields:
                self.fields["is_superuser"].initial = (
                    self.instance.is_superuser
                )

    # ============================================================
    # CLEAN
    # ============================================================

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # --------------------------------------------------------
        # PASSWORD
        # --------------------------------------------------------

        if password1 or password2:

            if password1 != password2:
                self.add_error(
                    "password2",
                    "As senhas não coincidem."
                )

        # --------------------------------------------------------
        # USERNAME
        # --------------------------------------------------------

        username = cleaned_data.get("username")

        if username:
            qs = User.objects.filter(
                username__iexact=username
            )

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error(
                    "username",
                    "Este username já está em uso."
                )

        return cleaned_data

    # ============================================================
    # SAVE
    # ============================================================

    def save(self, commit=True):

        user = super().save(commit=False)

        # ========================================================
        # PASSWORD
        # ========================================================

        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        # ========================================================
        # SUPERUSER
        # ========================================================

        if self.allow_superuser_change:

            # Somente este formulário pode modificar
            # o privilégio de superusuário.

            user.is_superuser = self.cleaned_data.get(
                "is_superuser",
                user.is_superuser
            )

        else:

            # Segurança:
            # mantém exatamente o valor que o usuário já possuía.

            if self.instance and self.instance.pk:
                user.is_superuser = self.instance.is_superuser

        # ========================================================
        # STAFF
        # ========================================================

        # Superuser precisa ser staff para acessar o Django Admin.

        if user.is_superuser:
            user.is_staff = True
        else:
            user.is_staff = False

        # ========================================================
        # ACTIVE
        # ========================================================

        # Não altera o estado de usuários existentes.
        #
        # Para novos usuários, ativa automaticamente.

        if not self.instance.pk:
            user.is_active = True

        # ========================================================
        # SAVE USER
        # ========================================================

        if commit:

            user.save()

            # ====================================================
            # PROFILE PHOTO
            # ====================================================

            photo = self.cleaned_data.get("photo")

            if photo:

                PhotoUser.objects.update_or_create(
                    user=user,
                    defaults={
                        "image": photo
                    }
                )

        return user