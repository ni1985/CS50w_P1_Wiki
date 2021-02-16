from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:entry_page>", views.entry, name="entry"),
    path("new", views.new_page, name="new"),
    path("rnd", views.rnd, name="rnd"),    
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search")
]
