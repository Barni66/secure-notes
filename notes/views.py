
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Note
from django.db import connection
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "notes/home.html")




def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Weak passwords are accepted
        #3 Identification and Authentication Failures

        # try:
        #     validate_password(password)
        # except ValidationError:
        #     return render(
        #         request,
        #         "notes/register.html",
        #         {"error": "Weak password"}
        #     )

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

        # Failed login attempts are not logged.
        # Administrators cannot detect brute-force attacks.
        #4 Security Logging and Monitoring Failures

        if user:
            login(request, user)

            return redirect("/notes/")

        # if user:
        #     login(request, user)

        #     logger.info(
        #         f"Successful login: {username}"
        #     )

        #     return redirect("/notes/")
        # else:

        #     logger.warning(
        #         f"Failed login attempt: {username}"
        #     )

    return render(request, "notes/login.html")


def logout_view(request):
    logout(request)

    return redirect("/")

@login_required
def notes_view(request):
    return render(request, "notes/notes.html")

@login_required
def create_note(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        secret = request.POST.get("secret")


        Note.objects.create(
            owner=request.user,
            title=title,
            content=content,
            secret=secret
        )

        # cipher = Fernet(settings.FERNET_KEY)
        
        # cipher.encrypt(
        #     secret.encode()
        # )

        # encrypted_secret = cipher.encrypt(
        #     secret.encode()
        # ).decode()

        # Note.objects.create(
        #     owner=request.user,
        #     title=title,
        #     content=content,
        #     secret=encrypted_secret
        # )

        return redirect("/notes/")

    return render(request, "notes/create.html")

@login_required
def notes_view(request):

    notes = Note.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "notes/notes.html",
        {"notes": notes}
    )

@login_required
def note_view(request, id):

    # No ownership check
    #1 Broken Access Control
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

@login_required
def delete_note(request, id):

    note = Note.objects.get(id=id)

    # note = Note.objects.get(
        # id=id,
        # owner=request.user
        # )

    note.delete()

    return redirect("/notes/")

@login_required
def search_view(request):

    results = []

    query = request.GET.get("q")

    if query:

        with connection.cursor() as cursor:
            cursor.execute(
                #2. SQL injection
                f"SELECT * FROM notes_note WHERE title LIKE '%{query}%'"
                
            )

            # cursor.execute(
            #     "SELECT * FROM notes_note WHERE title LIKE %s",
            #     [f"%{query}%"]
            # )

            # results = Note.objects.filter(
            #     owner=request.user,
            #     title__icontains=query
            # )

            results = cursor.fetchall()

    return render(
        request,
        "notes/search.html",
        {"results": results}
    )
