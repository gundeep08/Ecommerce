from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:name>", views.listing, name="listing"),
    path("addToWatchlist/<str:name>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<str:name>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("closeListing/<str:name>", views.closelisting, name="closeListing"),
    path("createlisting", views.createlisting, name="createlisting")
]

