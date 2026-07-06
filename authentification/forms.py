from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UserFollows


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom d’utilisateur",
                "class": "signup_field",
                "autocomplete": "off",
            }
        ),
    )

    password = forms.CharField(
        max_length=64,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "signup_field"}
        ),
    )


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "signup_field"}
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmer le mot de passe",
                "class": "signup_field",
            }
        ),
    )


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Nom d'utilisateur",
                    "class": "signup_field",
                }
            ),
        }


User = get_user_model()


class FollowUsersForm(forms.Form):
    followed_user_username = forms.CharField(label="Nom d'utilisateur")

    def clean_followed_user_username(self):
        username = self.cleaned_data["followed_user_username"]

        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Utilisateur introuvable")

        if self.user == followed_user:
            raise forms.ValidationError("Impossible de se suivre soi-même")

        if UserFollows.objects.filter(
            user=self.user, followed_user=followed_user
        ).exists():
            raise forms.ValidationError("Vous suivez déjà cette personne")

        return followed_user

    def save(self):
        follow = UserFollows.objects.create(
            user=self.user,
            followed_user=self.cleaned_data["followed_user_username"],
        )
        return follow
