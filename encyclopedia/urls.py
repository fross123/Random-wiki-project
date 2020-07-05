from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/<str:title>/edit/", views.edit, name="edit")
]
