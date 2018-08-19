from django.test import TestCase
from django.test import Client
from wishlist.models import User, Book, BookWish
from django.utils import timezone
import json

class WishListTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="tad", last_name="the cat", email="tad@meow.cat", password="sal3m", token="555")
        User.objects.create(first_name="hilda", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")

        Book.objects.create(title="rush the fence", author="woof pack", isbn="888", date_published=timezone.now())
        Book.objects.create(title="lost on lancaster", author="mystery kitty", isbn="999", date_published=timezone.now())
        # Book.objects.create(title="play in motion", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")
        # Book.objects.create(title="of mice and men", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")

    # def add_book_to_wish_list(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')

    def add_book_to_wish_list(self):
        """Animals that can speak are correctly identified"""
        print('hii')

        user_tad = User.objects.get(first_name="tad")
        book = Book.objects.get(title="lost on lancaster")
        c = Client()
        response = c.post('/wishlist/bookWish', {'user_id': user_tad.id, 'book_id': book.id})

        print(response.content)
        s = response.content.decode("utf-8")
        print(type(s))
        print(s)
        d = json.loads(s)

        # print(response.content)
        # dict = json.load(response.content)
        # dict=json.loads(s)
        print(d)
        print(d['plz'])
