from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, UserManager, Book, bookManager
import bcrypt

def index(request):
    return render(request, "favorite_books_app/index.html")

def books(request):
    if "logged_user" not in request.session:
        return redirect ("/")
        
    context={
        "user" : User.objects.get(id=request.session["logged_user"]),
        "books" : Book.objects.all(),
    }
    return render(request, "favorite_books_app/books.html", context)

def edit_page(request, book_id):
    bookLikes = Book.objects.get(id=book_id)
    context={
        "user" : User.objects.get(id=request.session["logged_user"]),
        "book" : Book.objects.get(id=book_id),
        "likedBooks" : bookLikes.liked_books.all(),
        "book_creator" : bookLikes.uploaded_by
    }
    return render(request,"favorite_books_app/edit.html", context)

def info_page(request, book_id):
    bookLikes = Book.objects.get(id=book_id)
    context={
        "user" : User.objects.get(id=request.session["logged_user"]),
        "book" : Book.objects.get(id=book_id),
        "likedBooks" : bookLikes.liked_books.all(),
    }
    return render(request,"favorite_books_app/book_info.html", context)

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

def add_book(request):
    errors = Book.objects.books_validator(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
            return redirect ("/books")
    user = User.objects.get(id=request.session["logged_user"])
    print(user)
    new_book = Book.objects.create(
        title = request.POST["title"],
        desc = request.POST["description"],
        uploaded_by = user,
    )
    new_book.liked_books.add(user)
    return redirect ("/books")

def book_edit(request, book_id):
    errors = Book.objects.books_validator(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
            return redirect (f"/books/{book_id}")
    up_book = Book.objects.get(id=book_id)
    up_book.title = request.POST["title"]
    up_book.desc = request.POST["description"]
    up_book.save()
    return redirect(f"/books/{book_id}")

def unfavorite(request, book_id):
    user= User.objects.get(id=request.session["logged_user"])
    fav_book = Book.objects.get(id=book_id)
    user.favorite_books.remove(fav_book)
    return redirect ("/books")

def addfavorite(request, book_id):
    user = User.objects.get(id=request.session["logged_user"])
    favor_book = Book.objects.get(id=book_id)
    user.favorite_books.add(favor_book)
    return redirect ("/books")

def delete_book(request, book_id):
    delete_book = Book.objects.get(id=book_id)
    delete_book.delete()
    return redirect("/books")