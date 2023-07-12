from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    users = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField()
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='publishers')

class Author(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    books_written = models.IntegerField()
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='authors')

class Customer(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    books = models.ManyToManyField(Book)
    total_book = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------------------------------------------
class MyBook(models.Model):
    book_name = models.CharField(max_length=100)
    published_date = models.DateTimeField()
    writer = models.CharField(max_length=100)


class Comment(models.Model):
    book = models.ForeignKey(MyBook, related_name="comments", on_delete=models.CASCADE)
    comments = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

