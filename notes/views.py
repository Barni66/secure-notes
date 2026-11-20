
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Note

# Create your views here.
def home(request):
    return render(request, "notes/home.html")




def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("/")

    return render(request, "notes/register.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return redirect("/notes/")

    return render(request, "notes/login.html")


def logout_view(request):
    logout(request)

    return redirect("/")

def notes_view(request):
    return render(request, "notes/notes.html")

def create_note(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        Note.objects.create(
            owner=request.user,
            title=title,
            content=content
        )

        return redirect("/notes/")

    return render(request, "notes/create.html")

def notes_view(request):

    notes = Note.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "notes/notes.html",
        {"notes": notes}
    )

def note_view(request, id):

    # No ownership check
    # Broken Access Control
    note = Note.objects.get(id=id)

    # note = Note.objects.get(
    # id=id,
    # owner=request.user
    # )

    return render(
        request,
        "notes/note.html",
        {"note": note}
    )
