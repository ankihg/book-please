import json
from django.test import TestCase
from django.test import Client
from django.utils import timezone
from .models import User, Book, BookWish

class WishListTestCase(TestCase):

    def setUp(self):
        tad_user_data = {'first_name': 'tad', 'last_name': 'the cat', 'email': 'tad@meow.cat', 'password': 'sal3m'}
        tad_user_creds = {'username': tad_user_data['email'], 'password': tad_user_data['password']}

        # User.objects.create(first_name="tad", last_name="the cat", email="tad@meow.cat", password="sal3m", token="555")
        # User.objects.create(first_name="hilda", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")
        self.load_books()
        reg_user = self.register_user(tad_user_data)
        logd_user = self.login_user(tad_user_creds)
        print('logd_user')
        print(logd_user)
        books = self.get_books()
        print('print the books')
        print(books)


    def load_books(self):
        Book.objects.create(title="rush the fence", author="woof pack", isbn="888", date_published=timezone.now())
        Book.objects.create(title="lost on lancaster", author="mystery kitty", isbn="999", date_published=timezone.now())
        # Book.objects.create(title="play in motion", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")
        # Book.objects.create(title="of mice and men", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")

    def register_user(self, user_data):
        """Register a user"""
        c = Client()
        response = c.post('/wishlist/users/register', user_data, content_type="application/json")
        return _parse_response(response)[0]

    def login_user(self, user_creds):
        """Login registered user"""
        c = Client()
        response = c.post('/wishlist/users/login', {'username': 'tad@meow.cat', 'password': 'sal3m'}, content_type="application/json")
        return _parse_response(response)[0]

    # def add_book_to_wish_list(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')

    def get_books(self):
        c = Client()
        response = c.get('/wishlist/books', content_type="application/json")
        return _parse_response(response)


    def add_book_to_wish_list(self):
        """Add a book to user's wishlist"""
        print('hii')
        self.get_books()

        user_tad = User.objects.get(first_name="tad")
        book = Book.objects.get(title="lost on lancaster")
        c = Client()
        response = c.post('/wishlist/bookWish', {'credentials': {'username': 'tad@meow.cat', 'password': 'sal3m'}, 'book_id': book.id}, content_type="application/json")

        print(response.content)
        s = response.content.decode("utf-8")
        print(type(s))
        print(s)
        d = json.loads(s)

        # print(response.content)
        # dict = json.load(response.content)
        # dict=json.loads(s)
        print(d[0])
        # print(d[0]['user_id'])
        self.add_another_book_to_wish_list()
        self.get_user_book_wist_list()

    def add_another_book_to_wish_list(self):
        """Animalsthat can speak are correctly identified"""
        print('hii')

        user_tad = User.objects.get(first_name="tad")
        book = Book.objects.get(title="rush the fence")
        c = Client()
        response = c.post('/wishlist/bookWish', {'credentials': {'username': 'tad@meow.cat', 'password': 'sal3m'}, 'book_id': book.id}, content_type="application/json")

        print(response.content)
        s = response.content.decode("utf-8")
        print(type(s))
        print(s)
        d = json.loads(s)

        # print(response.content)
        # dict = json.load(response.content)
        # dict=json.loads(s)
        print(d[0])
        # print(d[0]['user_id'])
        self.get_user_book_wist_list()

    def get_user_book_wist_list(self):
        user_tad = User.objects.get(first_name="tad")
        book = Book.objects.get(title="lost on lancaster")
        c = Client()
        url = '/wishlist/users/{:d}/bookWishes'.format(user_tad.id)
        print(url)
        response = c.get(url, content_type="application/json")

        s = response.content.decode("utf-8")
        response_json = json.loads(s)
        print('user bookWish model')
        print(response_json)



# HELPER FNS
def _parse_response(response):
    s = response.content.decode("utf-8")
    return json.loads(s)
