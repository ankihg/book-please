from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

import json

from .models import User, Book, BookWish


def index(request):
    latest_book_list = Book.objects.order_by('-date_published')[:5]
    output = ', '.join([b.title for b in latest_book_list])
    return HttpResponse(output)

@ensure_csrf_cookie
def add_book_to_wish_list(request):
    print('hello add_book_to_wish_list')
    # latest_book_list = Book.objects.order_by('-date_published')[:5]
    # output = ', '.join([b.title for b in latest_book_list])
    # return HttpResponse(output)

    body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # body = json.loads('{"plz": "respond"}')
    body = {}
    body['plz'] = 'respond'
    return HttpResponse(json.dumps(body))

    content = body['content']
    print(content)
    return HttpResponse(content)
