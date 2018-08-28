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

        # browse latest books by Mystery Kitty
        books_by_mystery_kitty = self.get_books_by_author('Mystery Kitty')
        self.assertEqual(len(books_by_mystery_kitty), 1)

        # select a book by Mystery Kitty
        book_to_wish_for = books_by_mystery_kitty[0]
        self.assertEqual(book_to_wish_for['author'], 'Mystery Kitty')
        self.assertEqual(book_to_wish_for['title'], 'Lost on Lancaster')

        # user tad adds book to wish list
        book_wish = self.add_book_to_wish_list(tad_user_creds, book_to_wish_for['id'])
        self.assertEqual(book_wish['user'], user_tad['id'])
        self.assertEqual(book_wish['book'], book_to_wish_for['id'])

        # get book by id
        books = self.get_book_by_id(book_wish['book'])
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['author'], 'Mystery Kitty')

        # get all books
        all_books = self.get_books()
        self.assertEqual(len(all_books), 4)

        # user hilda adds latest book to wish list
        latest_book = all_books[0]
        book_wish = self.add_book_to_wish_list(hilda_user_creds, latest_book['id'])
        self.assertEqual(book_wish['user'], user_hilda['id'])
        self.assertEqual(book_wish['book'], latest_book['id'])

        # browse books by Woof Pack
        books_by_woof_pack = self.get_books_by_author('Woof Pack')
        self.assertEqual(len(books_by_woof_pack), 2)

        # user hilda adds oldest book to wish list
        first_book = books_by_woof_pack[-1]
        book_wish = self.add_book_to_wish_list(hilda_user_creds, first_book['id'])
        self.assertEqual(book_wish['user'], user_hilda['id'])
        self.assertEqual(book_wish['book'], first_book['id'])
        self.assertIsNone(book_wish['date_granted'])

        # get user hilda book wishlist
        hilda_book_wishes = self.get_user_book_wish_list(user_hilda['id'])
        self.assertEqual(len(hilda_book_wishes), 2)

        # get user tad book wishlist
        tad_book_wishes = self.get_user_book_wish_list(user_tad['id'])
        print('tad_book_wishes')
        print(tad_book_wishes)
        self.assertEqual(len(tad_book_wishes), 1)

        # grant user hilda's bookWish for Woof Pack's first book
        granted_book_wish = self.grant_book_wish(hilda_user_creds, first_book['id'])
        self.assertEqual(granted_book_wish['user'], user_hilda['id'])
        self.assertEqual(granted_book_wish['book'], first_book['id'])
        self.assertIsNotNone(granted_book_wish['date_granted'])

        # get user hilda's ungranted bookWishes
        hilda_ungranted_wish_list = self.get_user_book_ungranted_wish_list(user_hilda['id'])
        self.assertEqual(len(hilda_ungranted_wish_list), 1)
        self.assertEqual(hilda_ungranted_wish_list[0]['title'], 'Lost on Lancaster')
        hildas_ungranted_book_wish = hilda_ungranted_wish_list[0]

        # get user hilda's granted bookWishes
        hilda_granted_wish_list = self.get_user_book_granted_wish_list(user_hilda['id'])
        self.assertEqual(len(hilda_granted_wish_list), 1)
        self.assertEqual(hilda_granted_wish_list[0]['author'], 'Woof Pack')

        # cancel user hilda's ungranted bookWish
        canceled_book_wish = self.cancel_book_wish(hilda_user_creds, hildas_ungranted_book_wish['id'])
        self.assertEqual(canceled_book_wish['user'], user_hilda['id'])
        self.assertEqual(canceled_book_wish['book'], hildas_ungranted_book_wish['id'])

        # assert bookWish is deleted
        hilda_ungranted_wish_list = self.get_user_book_ungranted_wish_list(user_hilda['id'])
        self.assertEqual(len(hilda_ungranted_wish_list), 0)

        # FAILURE TESTS
        # make an authenticated request with invalid user creds
        invalid_user_creds = {'username': 'happy@cat.plz', 'password': 'p1z'}
        invalid_user_creds_error = self.add_book_to_wish_list(invalid_user_creds, book_to_wish_for['id'])
        self.assertEqual(invalid_user_creds_error['message'], 'Invalid user credentials')


    def load_books(self):
        Book.objects.create(title="Rush the Fence", author="Woof Pack", isbn="888", date_published=timezone.now())
        Book.objects.create(title="Play in Motion", author="Woof Pack", isbn="555", date_published=timezone.now())
        Book.objects.create(title="Of Mice and Men", author="John Steinbeck", isbn="777", date_published=timezone.now())
        Book.objects.create(title="Lost on Lancaster", author="Mystery Kitty", isbn="999", date_published=timezone.now())

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

    def get_books_by_author(self, author):
        c = Client()
        url = '/wishlist/books?author={:s}'.format(author)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def get_book_by_id(self, id):
        c = Client()
        url = '/wishlist/books?id={:d}'.format(id)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def add_book_to_wish_list(self, user_creds, book_id):
        """Add a book to user's wishlist"""
        c = Client()
        response = c.post('/wishlist/bookWishes', {'credentials': user_creds, 'book_id': book_id}, content_type="application/json")
        print('auth response')
        print(response)
        print(type(response))
        print(response.status_code)
        if (response.status_code != 200):
            return _parse_response(response)
        return _parse_response(response)[0]

    def get_user_book_wish_list(self, user_id):
        c = Client()
        url = '/wishlist/users/{:d}/bookWishes'.format(user_id)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def get_user_book_ungranted_wish_list(self, user_id):
        c = Client()
        url = '/wishlist/users/{:d}/bookWishes?granted=false'.format(user_id)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def get_user_book_granted_wish_list(self, user_id):
        c = Client()
        url = '/wishlist/users/{:d}/bookWishes?granted=true'.format(user_id)
        response = c.get(url, content_type="application/json")
        return _parse_response(response)

    def grant_book_wish(self, user_creds, book_id):
        c = Client()
        url = '/wishlist/bookWishes/books/{:d}/grant'.format(book_id)
        response = c.put(url, {'credentials': user_creds}, content_type="application/json")
        return _parse_response(response)[0]

    def cancel_book_wish(self, user_creds, book_id):
        c = Client()
        url = '/wishlist/bookWishes/books/{:d}'.format(book_id)
        response = c.delete(url, {'credentials': user_creds}, content_type="application/json")
        return _parse_response(response)[0]


# HELPER FNS
def _parse_response(response):
    s = response.content.decode("utf-8")
    return json.loads(s)
