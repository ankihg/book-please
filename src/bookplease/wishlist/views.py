from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder

import json

from .models import User, Book, BookWish
from django.contrib.auth import authenticate, login


def index(request):
    latest_book_list = Book.objects.order_by('-date_published')[:5]
    output = ', '.join([b.title for b in latest_book_list])
    return HttpResponse(output)

# USER ROUTES
def register_user(request):
    print('welcome register_user')
    body = _parse_body(request)
    user = User.objects.create_user(body['email'], body['email'], body['password'])
    user.first_name = body['first_name']
    user.last_name = body['last_name']
    user.save()
    print(user)
    user_json = _prep_response([ user ])
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
        # user_json = serializers.serialize('json', [ user ])
        user_json = _prep_response([ user ])
        return HttpResponse(user_json)


# BOOK ROUTES
def get_books(request):
    print('get_books now')
    author = request.GET.get('author', '')
    id = request.GET.get('id', '')
    print(author)
    print(type(author))

    if id:
        books = Book.objects.filter(id=id)
    elif author:
        books = Book.objects.filter(author=author).order_by('-date_published')
    else:
        books = Book.objects.order_by('-date_published')

    # books_json = serializers.serialize('json', books)
    # print(books_json)
    books_json = _prep_response(books)
    return HttpResponse(books_json)

# BOOKWISH ROUTES
def add_book_to_wish_list(request):
    body = _parse_body(request)
    user = _authenticate(request, body)
    if (user is None):
        return HttpResponse(json.dumps({'message': 'Invalid user credentials'}), status=403)


    book_wish = BookWish(user_id=user.id, book_id=body['book_id'], date_wished=timezone.now())
    print(book_wish)
    book_wish.save()

    book_wish_json = _prep_response([ book_wish ])
    return HttpResponse(book_wish_json)

def get_user_book_wishes(request, user_id):
    granted = request.GET.get('granted', '')
    print('granted')
    print(granted)
    print(type(granted))
    if granted == 'true' or granted == 'True':
        granted = True
    elif granted == 'false' or granted == 'False':
        granted = False
    else:
        granted = None


    if granted is None:
        book_wishes = BookWish.objects.filter(user_id=user_id).order_by('-date_wished')
    else:
        book_wishes = BookWish.objects.filter(user_id=user_id, date_granted__isnull=not granted).order_by('-date_wished')

    book_ids = list(map(lambda book_wish: book_wish.book_id, book_wishes))
    books = Book.objects.filter(id__in=book_ids)
    books_json = _prep_response(books)
    print(books_json)
    return HttpResponse(books_json)

def mark_book_wish_as_granted(request, book_id):
    body = _parse_body(request)
    user = _authenticate(request, body)
    book_wish = BookWish.objects.get(user_id=user.id, book_id=book_id)
    book_wish.date_granted = timezone.now()
    book_wish.save()
    book_wish_json = _prep_response([ book_wish ])
    return HttpResponse(book_wish_json)

def cancel_book_wish(request, book_id):
    print('welcome cancel_book_wish')
    body = _parse_body(request)
    user = _authenticate(request, body)
    # TODO : unauthenticated error response
    book_wish = BookWish.objects.get(user_id=user.id, book_id=book_id)
    book_wish.delete()
    book_wish_json = _prep_response([ book_wish ])
    return HttpResponse(book_wish_json)


# HELPER FNS
def _parse_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print('print body')
    print(body)
    return body

def _prep_response(data):
    # this gives you a list of dicts
    raw_data = serializers.serialize('python', data)
    # now extract the inner `fields` dicts
    print('raw_data')
    print(raw_data)
    # actual_data = [d['fields'] for d in raw_data]
    actual_data = list(map(_build_response_object, raw_data))
    # and now dump to JSON
    # output = json.dumps(actual_data)
    # return output;
    print('actual_data')
    print(actual_data)
    return json.dumps(
      actual_data,
      sort_keys=True,
      indent=1,
      cls=DjangoJSONEncoder)

def _build_response_object(model):
    print('model')
    print(model)
    d = model['fields']
    d['id'] = model['pk']
    return d


def _authenticate(request, body):
    credentials = body['credentials']
    username = credentials['username']
    password = credentials['password']
    return authenticate(request, username=username, password=password)


# TODO
# register user https://docs.djangoproject.com/en/2.1/topics/auth/default/#creating-users
# authenticate user https://docs.djangoproject.com/en/2.1/topics/auth/default/#authenticating-users
