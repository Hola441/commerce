from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create, name="create_listing"),
    path("active_listings/<str:category>", views.categoriedIndexed, name="categoriedIndex"),
    path("categories", views.categories, name="categories"),
    path("my_watchlist", views.watch, name="watchlist"),
    path("<str:listTitle>", views.lists, name="listingItem"),
]
