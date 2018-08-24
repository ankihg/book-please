from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

from django.core import serializers

import json

from .models import User, Book, BookWish
from django.contrib.auth import authenticate, login


def index(request):
    latest_book_list = Book.objects.order_by('-date_published')[:5]
    output = ', '.join([b.title for b in latest_book_list])
    return HttpResponse(output)

def register_user(request):
    print('welcome register_user')
    body = _parse_body(request)
    user = User.objects.create_user(body['email'], body['email'], body['password'])
    user.first_name = body['first_name']
    user.last_name = body['last_name']
    user.save()
    print(user)
    user_json = serializers.serialize('json', [ user ])
    return HttpResponse(user_json)

def login_user(request):
    print('welcome login_user')
    body = _parse_body(request)
    username = body['username']
    password = body['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print(request)
        user_json = serializers.serialize('json', [ user ])
        return HttpResponse(user_json)

def add_book_to_wish_list(request):
    print('hello add_book_to_wish_list')
    # latest_book_list = Book.objects.order_by('-date_published')[:5]
    # output = ', '.join([b.title for b in latest_book_list])
    # return HttpResponse(output)

    body = _parse_body(request)
    user = _authenticate(request, body)
    print('authenticated user')
    print(user)
    print(user.id)

    book_wish = BookWish(user_id=user.id, book_id=body['book_id'], date_wished=timezone.now())
    print(book_wish)
    book_wish.save()
    book_wish_json = serializers.serialize('json', [ book_wish ])
    # book_wish_json = serializers.serialize('json', BookWish.objects.all())

    print(book_wish_json)

    return HttpResponse(book_wish_json)


def get_user_book_wishes(request, user_id):
    print('welcome get_user_book_wishes')
    print(user_id)
    book_wishes = BookWish.objects.filter(user_id=user_id)
    print(book_wishes)
    book_wishes_json = serializers.serialize('json', book_wishes)
    return HttpResponse(book_wishes_json)


def _parse_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print('print body')
    print(body)
    return body

def _authenticate(request, body):
    credentials = body['credentials']
    username = credentials['username']
    password = credentials['password']
    return authenticate(request, username=username, password=password)


# TODO
# register user https://docs.djangoproject.com/en/2.1/topics/auth/default/#creating-users
# authenticate user https://docs.djangoproject.com/en/2.1/topics/auth/default/#authenticating-users
