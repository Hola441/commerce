from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Categories, Watchlisted



def watch(request):
    yesWatchlisted = Watchlisted.objects.get(trueOrFalse = True)
    return render(request, "auctions/index.html", {
        "Listing": yesWatchlisted.listings.all()
    })
def categoriedIndexed(request, category):
    categoryItem = Categories.objects.get(categoryTitle=category)
    return render(request, "auctions/index.html", {
        "Listing": categoryItem.categoryList.all()
    })
def categories(request):
    return render(request, "auctions/categories.html", {
        "Categories": Categories.objects.all()
    })
def index(request):
    return render(request, "auctions/index.html", {
        "Listing": Listing.objects.all()
    })
def lists(request, listTitle):
    ListingItem = Listing.objects.get(title=listTitle)
    if request.method == "POST":      
        try:
            form = createBid(request.POST)
            if form.is_valid():
                spent = form.cleaned_data["cost"]
                if spent <= ListingItem.cost:
                    return render(request, "auctions/listing.html", {
                        "message": "Error, bid value less than initial cost of item.",
                        "ListingItem": ListingItem,
                        "bids": ListingItem.bids.all(),
                        "comments": ListingItem.comments.all(),
                        "Bid": createBid(),
                        "Comment": createComment()
                    })
                setattr(ListingItem, "cost", spent)
                bidItem = Bid.objects.create(spent=spent)
                bidItem.users.add(request.user)
                bidItem.listings.add(ListingItem)
                bidItem.save()
                ListingItem.save()
                return render(request, "auctions/listing.html", {
                    "ListingItem": ListingItem,
                    "bids": ListingItem.bids.all(),
                    "comments": ListingItem.comments.all(),
                    "Bid": createBid(),
                    "Comment": createComment()
                })
        except DataError:
            return render(request, "auctions/listing.html", {
                "message": "Error, post not accepted.",
                "ListingItem": ListingItem,
                "bids": ListingItem.bids.all(),
                "comments": ListingItem.comments.all(),
                "Bid": createBid(),
                "Comment": createComment()
            })
        else:
            form = createComment(request.POST)
            if form.is_valid():
                description = form.cleaned_data["description"]
                newComment = Comment.objects.create(description = description)
                newComment.users.add(request.user)
                newComment.listings.add(ListingItem)
                newComment.save()
                return render(request, "auctions/listing.html", {
                    "message": "successfully added",
                    "bids": ListingItem.bids.all(),
                    "comments": ListingItem.comments.all(),
                    "ListingItem": ListingItem,
                    "Bid": createBid(),
                    "Comment": createComment()
                })
    return render(request, "auctions/listing.html", {
        "ListingItem": ListingItem,
        "bids": ListingItem.bids.all(),
        "comments": ListingItem.comments.all(),
        "Bid": createBid(),
        "Comment": createComment()
    })
def create(request):
    if request.method == "POST":
        form = createListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            cost = form.cleaned_data["cost"]
            image = form.cleaned_data["image"]
            if request.user.is_authenticated:
                listing = Listing.objects.create(title = title, description = description, cost = cost, image = image)
                listing.users.add(request.user)
            else:
                return render(request, "auctions/newListing.html", {
                    "message": "You are not signed in."
                })
        try: 
            listing.save()
        except IntegrityError:
            return render(request, "auctions/newListing.html", {
                "message": "Title already taken."
            })
        else: 
            return render(request, "auctions/newListing.html", {
                "message": "Listing saved."
            })
    else:
        return render(request, "auctions/newListing.html", {
            "createListingItem": createListing()
        })


def login_view(request):
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class createListing(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(), label="Description")
    cost = forms.DecimalField(label="Cost")
    image = forms.URLField(label="Image URL", required=False)
class createBid(forms.Form):
    cost = forms.DecimalField(label="Cost")
class createComment(forms.Form):
    description = forms.CharField(widget=forms.Textarea(), label="Description")
