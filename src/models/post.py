import uuid
import datetime

from src.common.database import Database

class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None) -> object:
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date =  created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    # NEW METHOD:
    @classmethod
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection='blog',
                                      query={'_id' : _id})

        # general Python construct. Double asterisks in front
        # of a dictionary treats the dictionary keys and values
        # as names and arguments for a method.
        return cls(**blog_data)



    @staticmethod
    def from_blog(_id):
        # returns a list of posts
        return [post for post in Database.find('posts', {'blog_id':_id })]