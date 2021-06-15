"""
Main app/routing file for Twitoff.
The file that holds the function `create_app`
to collect our modules and organize the flask app.
"""

from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():

    # initilizes our application
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route("/")
    def root():
        """This will be presented when we visit '<BASE_URL>/ '"""
        insert_example_users()
        users = User.query.all()  # SQL equivalent: `SELECT * FROM user;`
        return render_template("base.html", title='Home', users=users)   
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()

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