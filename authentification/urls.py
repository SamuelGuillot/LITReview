from django.urls import path, include
from . import views as auth_views

urlpatterns = [
    path("signup/", auth_views.signup_page, name="signup"),
    path("login/", auth_views.login_page, name="login"),
    path("logout/", auth_views.logout_user, name="logout"),
    path(
        "users/<int:user_id>/connections/",
        auth_views.user_connections,
        name="user_connections",
    ),
    path("tickets/", include("tickets.urls")),
]
