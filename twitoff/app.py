"""
Main app/routing file for Twitoff.
The file that holds the function `create_app`
to collect our modules and organize the flask app.
"""
from os import getenv
from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


def create_app():

    # initilizes our application
    app = Flask(__name__)
    """
    Flask puts it's configuration values and extention values
    
    Config is a subclass of a dictionary and can be modified 
    like one
    
    ENV indicates to Flask, extenstions, and other programs 
    what context Flask is running in. 
        - controlled by FLASK_ENV
        - FLASK_ENV to development will enable debug mode
            - flask run will use the interactive debugger

    ENV can behave inconsistently after the app has been set up

    """
    # use the following database for the connection 
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv["DATABASE_URI"]
    
    # Flask SQLalchemy will track modifications of objects and emit signals
    # default is None
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SQLAlchemy references Flask 
    DB.init_app(app)

    # route decorator tells flask what URL should run our function
    @app.route("/")
    # Function used on home page
    def root():
        """This will be presented when we visit '<BASE_URL>/ '"""
        insert_example_users()
        users = User.query.all()  # SQL equivalent: `SELECT * FROM user;`
        return render_template("base.html", title='Home', users=users)   
    
    @app.route("/reset")
    # Function used on /reset page
    # Drop all from database and creates it again based on insert _example_users
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Just Reset")

    @app.route("/update")
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.name)
        return "All the users have been updated!"

    return app


def insert_example_users():
    """
    Will get error if ran twice because of duplicate primary keys
    Not real data - just to play with
    """
    jackblack = User(id=1, name="JackBlack")
    elonmusk = User(id=2, name="ElonMusk")
    ChrisChilton = User(id=3, name="ChrisChilton")
    DavidSuarez = User(id=4, name="DavidSuarez")
    FalonSquare = User(id=5, name="FalonSquare")
    TrevorDewalt = User(id=6, name="TrevorDewalt")
    DB.session.add(jackblack)
    DB.session.add(elonmusk)
    DB.session.add(ChrisChilton)
    DB.session.add(DavidSuarez)
    DB.session.add(FalonSquare)
    DB.session.add(TrevorDewalt)
    DB.session.commit()