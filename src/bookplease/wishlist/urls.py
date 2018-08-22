from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bookWish', views.add_book_to_wish_list, name='wish for book'),
    url(r'^users/register', views.register_user, name='register user'),
    url(r'^users/login', views.login_user, name='login user'),
]
