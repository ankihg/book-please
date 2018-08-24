from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bookWish', views.add_book_to_wish_list, name='wish for book'),
    url(r'^users/register', views.register_user, name='register user'),
    url(r'^users/login', views.login_user, name='login user'),
    # url(r'^users/:userId/bookWishes', views.get_user_book_wishes, name='get user book wishes'),
    url(r'^user/(?P<user_id>\w{0,50})/bookWishes', views.get_user_book_wishes, name='get user book wishes'),
]
