import uuid

import datetime
from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        # set the _id when initialized
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        # searches the "users" collection of db
        # stores the fields in data
        data = Database.find_one("users", {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        # searches the "users" collection of db
        # stores the fields in data
        data = Database.find_one("users", {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # first create user object
        user = User.get_by_email(email)

        # check the user's credentials are valid
        if user is not None:
            # returns true or false
            return password == user.password

    @classmethod
    def register(cls, email, password):

        test_user = cls.get_by_email(email)
        if test_user is not None:
            # user already exits
            return False
            # put message user already exists

        else:
            # create the new user
            user = cls(email, password)
            user.save_to_mongo()

            # log the user in
            session['email'] = email

            return True

    @staticmethod
    def login(user_email):
        # allows the returning user to login
        # login_valid already called
        # Flask handles the session cookies.
        session['email'] = user_email

    @staticmethod
    def logout():

        # clears the session cookies
        session['email'] = None

    def get_blogs(self):

        # to call a class / static method just use Blog.
        return Blog.find_by_author_id(self._id)


    def new_blog(self, title, description):
        # Blog(self, author, title, description, author_id, _id=None):

        # Here using email as the author of the blog
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        # note - we should do checking for duplicates / unsafe HTML
        # save blog after init
        blog.save_to_mongo()

    def new_post(self, blog_id, title, content, created_date=datetime.datetime.utcnow()):

        blog = Blog.from_mongo(blog_id)

        # pass args to blog method
        blog.new_post(title=title,
                      content=content,
                      created_date=created_date)

        # don't need to save to mongo because that's in the .new_post method

    def save_to_mongo(self):
        # Stores the JASON in the database
        Database.insert("users", self.jason())

    def jason(self):
        # method to transform object fields -> Json
        # do NOT send passwords over a network
        # - only between the app
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }


