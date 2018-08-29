from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=17, unique=True)
    date_published = models.DateTimeField()

class BookWish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_wished = models.DateTimeField(auto_now_add=True)
    date_granted = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('user', 'book')
