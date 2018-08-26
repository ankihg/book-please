import json
from django.test import TestCase
from django.test import Client
from django.utils import timezone
from .models import User, Book, BookWish

class WishListTestCase(TestCase):

    def setUp(self):
        # User.objects.create(first_name="tad", last_name="the cat", email="tad@meow.cat", password="sal3m", token="555")
        # User.objects.create(first_name="hilda", last_name="garde", email="hilda@garde.woof", password="b4RK11", token="666")
        self.load_books()

    def run_test(self):
        tad_user_data = {'first_name': 'tad', 'last_name': 'the cat', 'email': 'tad@meow.cat', 'password': 'sal3m'}
        tad_user_creds = {'username': tad_user_data['email'], 'password': tad_user_data['password']}
        hilda_user_data = {'first_name': 'hilda', 'last_name': 'garde', 'email': 'hilda@garde.woof', 'password': 'b4rk0n'}
        hilda_user_creds = {'username': hilda_user_data['email'], 'password': hilda_user_data['password']}

        # register and login user tad
        self.register_user(tad_user_data)
        user_tad = self.login_user(tad_user_creds)
        self.assertEqual(user_tad['first_name'], tad_user_data['first_name'])
        self.assertEqual(user_tad['username'], tad_user_data['email'])
        self.assertEqual(user_tad['email'], tad_user_data['email'])

        # register and login user hilda
        reg_user_hilda = self.register_user(hilda_user_data)
        user_hilda = self.login_user(hilda_user_creds)
        self.assertEqual(user_hilda['first_name'], hilda_user_data['first_name'])
        self.assertEqual(user_hilda['username'], hilda_user_data['email'])
        self.assertEqual(user_hilda['email'], hilda_user_data['email'])

        # get books
        # all_books = self.get_books

        # browse latest books by Mystery Kitty
        books_by_mystery_kitty = self.get_books_by('Mystery Kitty')
        self.assertEqual(len(books_by_mystery_kitty), 1)

        # select book
        book_to_wish_for = books_by_mystery_kitty[0]
        self.assertEqual(book_to_wish_for['author'], 'Mystery Kitty')
        self.assertEqual(book_to_wish_for['title'], 'Lost on Lancaster')

        # user tad adds book to wish list
        book_wish = self.add_book_to_wish_list(tad_user_creds, book_to_wish_for['id'])
        self.assertEqual(book_wish['user'], user_tad['id'])
        self.assertEqual(book_wish['book'], book_to_wish_for['id'])


    def load_books(self):
        Book.objects.create(title="Rush the Fence", author="Woof Pack", isbn="888", date_published=timezone.now())
        Book.objects.create(title="Lost on Lancaster", author="Mystery Kitty", isbn="999", date_published=timezone.now())
        Book.objects.create(title="Play in Motion", author="Woof Pack", isbn="888", date_published=timezone.now())
        Book.objects.create(title="Of Mice and Men", author="John Steinbeck", isbn="888", date_published=timezone.now())

    def register_user(self, user_data):
        """Register a user"""
        c = Client()
        response = c.post('/wishlist/users/register', user_data, content_type="application/json")
        return _parse_response(response)[0]

    def login_user(self, user_creds):
        """Login registered user"""
        c = Client()
        response = c.post('/wishlist/users/login', user_creds, content_type="application/json")
        return _parse_response(response)[0]


    def get_books(self):
        c = Client()
        response = c.get('/wishlist/books', content_type="application/json")
        return _parse_response(response)

    def get_books_by(self, author):
        c = Client()
        url = '/wishlist/books/?author={:s}'.format(author)
        print('url')
        print(url)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def add_book_to_wish_list(self, user_creds, book_id):
        """Add a book to user's wishlist"""
        c = Client()
        response = c.post('/wishlist/bookWish', {'credentials': user_creds, 'book_id': book_id}, content_type="application/json")
        return _parse_response(response)[0]

    def get_user_book_wist_list(self):
        user_tad = User.objects.get(first_name="tad")
        book = Book.objects.get(title="Lost on Lancaster")
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
