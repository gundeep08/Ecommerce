from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Comment, Bid, Watchlist


def index(request):
    # Return all auction Items for default page
    return render(request, "auctions/index.html", {
        "auction": Auction.objects.all(),
        "bids": Bid.objects.all()
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


def listing(request, name):
    # Product Details/Listing Page
    addtoWishlist=True
    allowclosingListing=False
    highestBid=0
    if request.method == "POST":
        # Bid is made or Comment is posted
        bidprice = request.POST["bidprice"]
        comment = request.POST["comment"]
        items=Auction.objects.all()
        for item in items:
            if item.title==name:
                wishlistgroup=Watchlist.objects.all()
                for wishlst in wishlistgroup:
                    if wishlst.auction.id==item.id:
                        addtoWishlist=False
                    if request.user.username == item.owner:
                        allowclosingListing=True
                if 'comment' in request.POST and comment:
                    commentObject = Comment(auction=item, comment=comment)
                    commentObject.save()
                    return render(request, "auctions/listing.html", {
                        "list": item,
                        "addtowishlist": addtoWishlist,
                        "comments":Comment.objects.all(),
                        "bids": Bid.objects.all(),
                        "closeListing":allowclosingListing,
                        "isListingValid":item.isListingAvailable,
                        "username": request.user.username
                    })
                elif 'bidprice' in request.POST:
                    bidinfo=Bid.objects.all()
                    for bid in bidinfo:
                        if bid.auction.id == item.id:
                            highestBid=bid.bidPrice
                    if bidprice and int(bidprice) >= highestBid:
                        bidObject = Bid.objects.get(auction=item)
                        bidObject.bidPrice=bidprice
                        bidObject.highestBidder=request.user.username
                        bidObject.save()
                        return render(request, "auctions/listing.html", {
                            "list": item,
                            "addtowishlist": addtoWishlist,
                            "comments":Comment.objects.all(),
                            "bids": Bid.objects.all(),
                            "closeListing":allowclosingListing,
                            "isListingValid":item.isListingAvailable,
                            "username": request.user.username
                        })
                    else:
                        return render(request, "auctions/error.html", {
                            "message": "Sorry, Your Bid Price is below the listed price"
                        })
    else:
         # Return Listing Page to display a specific product details
        items=Auction.objects.all()
        for item in items:
            if item.title==name:
                wishlistgroup=Watchlist.objects.all()
                for wishlst in wishlistgroup:
                    if wishlst.auction.id==item.id:
                        addtoWishlist=False
                if request.user.username == item.owner:
                    allowclosingListing=True
                return render(request, "auctions/listing.html", {
                    "list": item,
                    "addtowishlist": addtoWishlist,
                    "comments":Comment.objects.all(),
                    "bids": Bid.objects.all(),
                    "closeListing":allowclosingListing,
                    "isListingValid":item.isListingAvailable,
                    "username": request.user.username
                })
    return HttpResponseRedirect(reverse("index"))

@login_required
def addToWatchlist(request, name):
     # Add item to watchlist
    auctionItem= Auction.objects.get(title=name)
    watchlst = Watchlist(auction=auctionItem)
    watchlst.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def removeFromWatchlist(request, name):
     #Remove a item from watchlist
    auctionItem= Auction.objects.get(title=name)
    wishlistItem= Watchlist.objects.get(auction=auctionItem)
    wishlistItem.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def wishlist(request):
    #Show all the items in watchlist
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.all(),
        "auction": Auction.objects.all(),
        "bids": Bid.objects.all()
    })

@login_required
def closelisting(request, name):
     # Close Listing and assign a Winner
    auctionItem= Auction.objects.get(id=name)
    auctionItem.isListingAvailable=False
    auctionItem.save()
    return HttpResponseRedirect(reverse("index"))
   


@login_required
def createlisting(request):
    # Create a new Listing
    if request.method == "POST":
        price = request.POST["bidprice"]
        title=request.POST["pagetitle"]
        description=request.POST["pagecontent"]
        imgurl=request.POST["imgsrc"]
        if imgurl:
            auctionItem=Auction(title= title, description=description, owner=request.user.username, image=imgurl)
        else:
            auctionItem=Auction(title= title, description=description, owner=request.user.username)        
        auctionItem.save()
        startingbidprice=Bid(auction= auctionItem, bidPrice=price, highestBidder=request.user.username)
        startingbidprice.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html")
        
            

        
