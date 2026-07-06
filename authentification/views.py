from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from .forms import SignupForm, LoginForm, FollowUsersForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from .models import UserFollows
from django.contrib import messages

User = get_user_model()


def signup_page(request):
    form = SignupForm()

    if request.method == "POST":
        # on remplit le formulaire avec les données envoyées
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # connecte automatiquement l'utilisateur
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentification/signup.html", {"form": form})


def login_page(request):
    form = LoginForm()
    message = ""

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                # vérifie username + password
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                # si utilisateur existe et mot de passe correct

                # connecte automatiquement l'utilisateur
                login(request, user)

                next_url = request.POST.get("next") or request.GET.get("next")

                # redirige vers next ou home
                return redirect(next_url or "flux")
            else:
                message = "Identifiants invalides."

    return render(
        request,
        "authentification/login.html",
        {"form": form, "message": message},
    )


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def user_connections(request):

    if request.method == "POST":
        # Unfollow
        unfollow_id = request.POST.get("unfollow_user_id")

        if unfollow_id:
            try:
                unfollow_id = int(unfollow_id)

                user_to_unfollow = User.objects.get(id=unfollow_id)

                UserFollows.objects.filter(
                    user=request.user,
                    followed_user=user_to_unfollow,
                ).delete()

            except ValueError:
                messages.error(request, "Identifiant invalide.")

            except User.DoesNotExist:
                messages.error(request, "Utilisateur introuvable.")

            except TypeError:
                messages.error(request, "Requête invalide.")

        # Follow
        form = FollowUsersForm(request.POST)
        form.user = request.user  # définir l'utilisateur connecté

        if form.is_valid():
            form.save()
            return redirect("user_connections", user_id=request.user.id)
        else:
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = FollowUsersForm()
        form.user = request.user

    following = request.user.following.all()  # UserFollows instances
    followers = request.user.followers.all()

    return render(
        request,
        "authentification/follow_users.html",
        {
            "form": form,
            "following": following,
            "followers": followers,
        },
    )
