import uuid
import datetime

from src.models.post import Post
from src.common.database import Database

class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, created_date=datetime.datetime.utcnow()):

        post = Post(blog_id=self._id,
                    title=title,
                    author=self.author,
                    content=content,
                    created_date=created_date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, _id):

        # blog data will come as a Jason like array
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})

        # puts the filds into the properties of the class
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):

        # query format is dict?
        blogs = Database.find('blogs', {'author_id': author_id})

        # returns an array of Blog objects
        # with values of the blogs unpacked
        return [cls(**blog) for blog in blogs]

