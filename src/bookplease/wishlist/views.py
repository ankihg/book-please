from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import User, Book, BookWish


def index(request):
    latest_book_list = Book.objects.order_by('-date_published')[:5]
    output = ', '.join([b.title for b in latest_book_list])
    return HttpResponse(output)
