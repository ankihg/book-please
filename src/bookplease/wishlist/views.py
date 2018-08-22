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

def register_user(request):
    print('welcome register_user')
    body = _parse_body(request)
    user = User.objects.create_user(body['first_name'], body['email'], body['password'])
    user.first_name = body['first_name']
    user.last_name = body['last_name']
    user.save()
    print(user)
    user_json = serializers.serialize('json', [ user ])
    return HttpResponse(user_json)

def add_book_to_wish_list(request):
    print('hello add_book_to_wish_list')
    # latest_book_list = Book.objects.order_by('-date_published')[:5]
    # output = ', '.join([b.title for b in latest_book_list])
    # return HttpResponse(output)

    body = _parse_body(request)


    book_wish = BookWish(user_id=body['user_id'], book_id=body['book_id'], date_wished=timezone.now())
    print(book_wish)
    book_wish.save()
    book_wish_json = serializers.serialize('json', [ book_wish ])
    # book_wish_json = serializers.serialize('json', BookWish.objects.all())

    print(book_wish_json)

    return HttpResponse(book_wish_json)


def _parse_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print('print body')
    print(body)
    return body



# TODO
# register user https://docs.djangoproject.com/en/2.1/topics/auth/default/#creating-users
# authenticate user https://docs.djangoproject.com/en/2.1/topics/auth/default/#authenticating-users
