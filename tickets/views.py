from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from authentification.models import UserFollows
from .models import Ticket
from .forms import TicketForm
from reviews.forms import ReviewForm
from reviews.models import Review
from itertools import chain
from django.db.models import Value, CharField


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(
            request.POST, request.FILES
        )  # remplir le formulaire avec les données POST
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")  # rediriger vers la page du ticket créé
    else:
        form = TicketForm()

    return render(request, "tickets/create_ticket.html", {"form": form})


@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket, id=ticket_id, user=request.user
    )  # récupére que si ticket appartient à l'utilisateur

    if request.method == "POST":
        form = TicketForm(
            request.POST, request.FILES, instance=ticket
        )  # formulaire pré-rempli
        if form.is_valid():
            form.save()
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        form = TicketForm(
            instance=ticket
        )  # formulaire avec les valeurs actuelles du ticket

    return render(
        request, "tickets/modify_ticket.html", {"form": form, "ticket": ticket}
    )


@login_required
def delete_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("flux")

    return render(request, "tickets/confirm_delete.html", {"ticket": ticket})


@login_required
def create_ticket_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("ticket_detail", ticket_id=ticket.id)

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(
        request,
        "tickets/create_ticket_review.html",
        {
            "ticket_form": ticket_form,
            "review_form": review_form,
        },
    )


@login_required
def flux(request):
    user = request.user

    followed_users_ids = UserFollows.objects.filter(user=user).values_list(
        "followed_user_id", flat=True
    )

    # Tickets (you + followed users)
    tickets = Ticket.objects.filter(Q(user=user) | Q(user__id__in=followed_users_ids))

    # Reviews
    reviews = Review.objects.filter(
        Q(user=user) | Q(user__id__in=followed_users_ids) | Q(ticket__user=user)
    )

    # check deja review
    reviewed_ticket_ids = Review.objects.filter(user=user).values_list(
        "ticket_id", flat=True
    )

    posts = list(tickets) + list(reviews)

    for post in posts:
        post.is_own = post.user == user
        post.is_review = isinstance(post, Review)

    # Sort
    posts = sorted(
        posts,
        key=lambda x: x.time_created,
        reverse=True,
    )
    return render(
        request,
        "tickets/flux.html",
        {
            "posts": posts,
            "followed_users_ids": followed_users_ids,
            "reviewed_ticket_ids": reviewed_ticket_ids,
        },
    )


@login_required
def posts(request):
    user = request.user

    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

    posts = list(tickets) + list(reviews)

    for post in posts:
        post.is_own = post.user == user

    posts = sorted(
        posts,
        key=lambda x: x.time_created,
        reverse=True,
    )

    return render(
        request,
        "tickets/posts.html",
        {
            "posts": posts,
        },
    )
