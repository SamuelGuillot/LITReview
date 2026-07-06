from django.urls import path
from . import views

urlpatterns = [
    path("create_ticket/", views.create_ticket, name="create_ticket"),

    path(
        "ticket/<int:ticket_id>/edit/",
        views.modify_ticket,
        name="modify_ticket",
    ),

    path(
        "ticket/<int:id>/delete/",
        views.delete_ticket,
        name="delete_ticket",
    ),

    path("flux/", views.flux, name="flux"),
    path("posts/", views.posts, name="posts"),

    path(
        "create_ticket_review/",
        views.create_ticket_review,
        name="create_ticket_review",
    ),
]
