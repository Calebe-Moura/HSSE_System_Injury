from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

TAILWIND_INPUT = (
    "w-full rounded-xl border border-slate-200 bg-white "
    "px-4 py-3 text-sm text-slate-900 outline-none transition "
    "placeholder:text-slate-400 "
    "focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
)


class FormLogin(AuthenticationForm):

    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(
            attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Email or Username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        ),
    )


class FormUser(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
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

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "Username",
            "email": "Email Address",
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": TAILWIND_INPUT,
                    "placeholder": "First Name",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": TAILWIND_INPUT,
                    "placeholder": "Last Name",
                    "autocomplete": "family-name",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": TAILWIND_INPUT,
                    "placeholder": "Username",
                    "autocomplete": "username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": TAILWIND_INPUT,
                    "placeholder": "Email Address",
                    "autocomplete": "email",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.instance.pk:

            if not password1:
                self.add_error("password1", "Password is required.")

            if not password2:
                self.add_error("password2", "Password confirmation is required.")

        if password1 or password2:

            if password1 != password2:
                self.add_error("password2", "Passwords do not match.")

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
