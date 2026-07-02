from django.urls import path
from . import views

urlpatterns = [
    path("create_review/<int:ticket_id>/", views.create_review, name="create_review"),
    path("review/<int:id>/edit/", views.modify_review, name="modify_review"),
    path("review/<int:id>/delete/", views.delete_review, name="delete_review"),
]
