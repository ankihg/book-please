from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bookWishes', views.add_book_to_wish_list, name='wish for book'),
    url(r'^users/register', views.register_user, name='register user'),
    url(r'^users/login', views.login_user, name='login user'),
    url(r'^users/(?P<user_id>\w{0,50})/bookWishes', views.get_user_book_wishes, name='get user book wishes'),
    url(r'^books', views.get_books, name='get books'),
    url(r'^users/(?P<user_id>\w{0,10})/books/(?P<book_id>\w{0,10})/grant', views.mark_book_wish_as_granted, name='mark book wish as granted'),
    # url(r'^books/(?P<author>\w{0,50})', views.get_books_by_author, name='get books by author'),
]
