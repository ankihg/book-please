
# Schema
## user
```
id
first_name
last_name
email
password
token
```

## book
```
id
title
author
isbn
date_of_publication
```

## wish
```
id
userId [user.id][not null]
bookId [book.id][not null]
dateAdded [not null]
dateWishGranted
```

# Technologies
- Web framework - [Django](https://www.djangoproject.com/)
- Database - [sqlite](https://docs.python.org/2/library/sqlite3.html)
- SQL query builder - [PyPika](https://github.com/kayak/pypika)

# Questions
- May I extend the attributes of user and book?
- Would you like token authentication?
