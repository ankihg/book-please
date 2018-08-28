from django.urls import path
# from django.conf.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('bookWishes', views.add_book_to_wish_list, name='wish for book'),
    path('bookWishes/books/<book_id>', views.cancel_book_wish, name='cancel book wish'),
    path('users/register', views.register_user, name='register user'),
    path('users/login', views.login_user, name='login user'),
    path('users/<user_id>/bookWishes', views.get_user_book_wishes, name='get user book wishes'),
    path('books', views.get_books, name='get books'),
    path('bookWishes/books/<book_id>/grant', views.mark_book_wish_as_granted, name='mark book wish as granted'),
    # url(r'^books/(?P<author>\w{0,50})', views.get_books_by_author, name='get books by author'),
]
