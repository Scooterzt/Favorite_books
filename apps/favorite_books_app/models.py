from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime

class UserManager(models.Manager):
    def register_validation(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Fisrt name should be at least 2 caracters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name shoud be at least 2 caracter"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address!"
        if User.objects.filter(email=postData["email"]):
            errors["email_used"] = "This email is in use alredy"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at leasr 8 character"
        if postData['password'] != postData["confirm_password"]:
            errors["confirm_password"] = "password and Condirm PW shoud match"
        return errors

    def login_validation(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData["email"])
        except:
            errors["email"] = "Email or Password not matching out database"
            return errors
        if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
            errors["password"] = "Password or Email not matching our Database"
        return errors
        
class bookManager(models.Manager):
    def books_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 1:
            errors["book_title"] = "seriously, do you want to add a book without a title?"
        if len(postData["description"]) < 5:
            errors["book_descripton"] = "Pretty short description, try again. I think at least 5 will be ok)"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: {self.first_name} ({self.id})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    uploaded_by = models.ForeignKey(User, related_name="uploaded_books", null=True)
    liked_books = models.ManyToManyField(User, related_name="favorite_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = bookManager()

    def __repr__(self):
        return f"<Book object: {self.title} ({self.id})"
