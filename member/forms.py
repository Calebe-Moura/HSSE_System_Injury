from django import forms
from django.contrib.auth.models import User


class FormUser(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Password",
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
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "First name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Last name",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input",
                    "placeholder": "E-mail",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.instance.pk:

            if not password1:
                self.add_error(
                    "password1",
                    "A senha é obrigatória."
                )

            if not password2:
                self.add_error(
                    "password2",
                    "A confirmação da senha é obrigatória."
                )

        if password1 or password2:

            if password1 != password2:
                self.add_error(
                    "password2",
                    "As senhas não coincidem."
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        user.is_staff = True
        user.is_superuser = False
        user.is_active = True

        if commit:
            user.save()

        return user