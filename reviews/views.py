from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from tickets.models import Ticket

from django.http import Http404

# @login_required
# def homepage(request):
#     return render(request, "reviews/home.html")


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(
        Ticket, id=ticket_id
    )  # récupère le ticket correspondant à l'ID ou renvoie une 404 si inexistant
    does_exist = Review.objects.filter(user=request.user, ticket_id=ticket_id).exists()
    if does_exist:
        raise Http404
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # crée un objet review sans l'enregistrer
            review.user = request.user  # l'utilisateur = auteur
            review.ticket = ticket  # relie la review au ticket
            review.save()
            return redirect("flux")
    else:
        form = ReviewForm()  # formulaire vide

    return render(
        request,
        "reviews/create_review.html",
        {"form": form, "ticket": ticket},
    )


@login_required
def modify_review(
    request, id
):  # récupère la review uniquement si elle appartient à l'utilisateur connecté
    review = get_object_or_404(Review, id=id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        form = ReviewForm(
            request.POST, request.FILES, instance=review
        )  # instance pour review existente
        if form.is_valid():
            form.save()
            return redirect("flux")
    else:
        form = ReviewForm(instance=review)  # formulaire pré-rempli

    return render(
        request,
        "reviews/modify_review.html",
        {"form": form, "review": review, "ticket": ticket},
    )


@login_required
def delete_review(request, id):
    review = get_object_or_404(
        Review, id=id, user=request.user
    )  # récupère la review uniquement si elle appartient à l'utilisateur connecté
    if request.method == "POST":
        review.delete()
        return redirect("reviews_list")

    return render(request, "reviews/confirm_delete.html", {"review": review})
