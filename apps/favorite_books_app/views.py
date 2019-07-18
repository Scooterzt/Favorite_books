from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def index(request):
    return render(request, "favorite_books_app/index.html")

def books(request):
    if "logged_user" not in request.session:
        return redirect ("/")
    context={
        "user" : User.objects.get(id=request.session["logged_user"]),
    }
    return render(request, "favorite_books_app/books.html", context)

def registration(request):
    errors = User.objects.register_validation(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
        return redirect("/")
    new_user=User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    )
    request.session["logged_user"] = new_user.id 
    return redirect("/books")

def login(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
        return redirect ("/")
        
    user = User.objects.get(email=request.POST["email"])
    request.session["logged_user"] = user.id
    return redirect("/books")

def log_out(request):
    request.session.clear()
    return redirect ("/")