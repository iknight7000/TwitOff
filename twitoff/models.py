"""SQLAlchemy models (schema) for twitoff"""
from flask_sqlalchemy import SQLAlchemy 


# classes can be mapped to the database in open ended ways
DB = SQLAlchemy()
# Creates User Table
# Similar to saying `CREATE TABLE user ...` in SQL
class User(DB.Model):
    """Twitter Users corresponding to tweets table"""
    # creating id column (primary key)
    id = DB.Column(DB.BigInteger, primary_key=True)
    # creates name column (string value, no nulls)
    name = DB.Column(DB.String, nullable=False)
    # newest_tweet_id = DB.Column(DB.BigInteger)
    def __repr__(self):
        return f"<User: {self.name}>"
# Creates Tweet Table
# Similar to saying `CREATE TABLE tweet ...` in SQL
class Tweet(DB.Model):
    """Tweet text and data"""
    # id column (integer values, primary key)
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column (unicode values up to 300)
    text = DB.Column(DB.UnicodeText())
    # vector column (holds python objects, that are serialized)
    vect = DB.Column(DB.PickleType, nullable=False)
    # user id column (integer values) ()
    """
    1 to many relationship places a foreign key on child 
    table referencing the parent

    .relationship() is specified on the parent for referencing 
    a collection of items represented by the child. 
    """
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'))
    # Is this supposed to be capitalized?
    # Is user the parent or child? 
    user = DB.relationship("User", backref=DB.backref('tweets', lazy=True))
    # __repr__ method represents class's objects as a string
    def __repr__(self):
        # returns the text of a tweet
        return f"<Tweet: {self.text}>"