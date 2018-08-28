
# Schema
## User
Imported from `django.contrib.auth`
```
id
first_name [type string]
last_name [type string]
email [type string][not null]
password [type string][not null]
```

## Book
```
id
title [type string][not null]
author [type string][not null]
isbn [type string][not null]
date_of_publication [type date][not null]
```

## BookWish
```
id
user_id [type id][fkey user.id][not null]
book_id [type id][fkey book.id][not null]
date_wished [type date][not null]
date_granted [type date]
```

# Technologies
- Web framework - [Django](https://www.djangoproject.com/)
I decided to use Django because it is widely used and I'd been interested in trying it out. In the end, I found Django a little heavy for the application but appreciated its power and ease of use.

# Routes
- `get_user_book_wishes` is unauthenticated. Anyone can see a users book wish list

## Users
### Register
```
POST /wishlist/users/register
{
  'first_name': 'tad',
  'last_name': 'the cat',
  'email': 'tad@meow.cat',
  'password': 'sal3m'
}
```

### Login
```
POST /wishlist/users/login
{
  'username': 'tad@meow.cat',
  'password': 'sal3m'
}
```

## Books

### Get many
- The returned books are ordered with the latest first
- Route supports an optional `author` or `id` query parameter
```
GET /wishlist/books?author="Mystery Kitty"
```

## BookWishes
### Post
- Authenticated
- Add a book to your wish list
- Only you can add books to your wish list
```
POST /wishlist/bookWishes
{
  'credentials': {
    'username': 'tad@meow.cat',
    'password': 'sal3m'
  },
  'book_id': book_id
}
```

### Get for user
- Get a user's book wish list
- Anyone can see a user's book wish list
```
GET /wishlist/users/<user_id>/bookWishes
```

### Mark as granted
- Authenticated
- Mark a book as granted on your wish list
- Only you can mark books as granted on your wish list
```
PUT /wishlist/bookWishes/books/<book_id>/grant
```
