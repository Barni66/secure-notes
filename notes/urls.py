from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("notes/", views.notes_view, name="notes"),
    path("create/", views.create_note, name="create"),
    path("note/<int:id>/", views.note_view, name="note"),
    path("delete/<int:id>/", views.delete_note, name="delete"),
    path("search/", views.search_view, name="search"),
]