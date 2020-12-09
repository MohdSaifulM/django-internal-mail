from accounts.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.


def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "accounts/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "accounts/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("all_books"))
    else:
        return render(request, "accounts/register.html")


def sign_in(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "accounts/login.html")
    else:
        return render(request, "accounts/login.html")


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))