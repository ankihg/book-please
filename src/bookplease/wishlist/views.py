from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

from django.core import serializers

import json

from .models import User, Book, BookWish


def index(request):
    latest_book_list = Book.objects.order_by('-date_published')[:5]
    output = ', '.join([b.title for b in latest_book_list])
    return HttpResponse(output)

def add_book_to_wish_list(request):
    print('hello add_book_to_wish_list')
    # latest_book_list = Book.objects.order_by('-date_published')[:5]
    # output = ', '.join([b.title for b in latest_book_list])
    # return HttpResponse(output)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print('print body')
    print(body)


    book_wish = BookWish(user_id=body['user_id'], book_id=body['book_id'], date_wished=timezone.now())
    print(book_wish)
    book_wish.save()
    book_wish_json = serializers.serialize('json', [ book_wish ])
    # book_wish_json = serializers.serialize('json', BookWish.objects.all())

    print(book_wish_json)

    return HttpResponse(book_wish_json)
