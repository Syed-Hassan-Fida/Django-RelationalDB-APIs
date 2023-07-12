from django.contrib import admin
from .models import Publisher, Author, Book, Customer, MyBook, Comment

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Customer)

admin.site.register(MyBook)
admin.site.register(Comment)
