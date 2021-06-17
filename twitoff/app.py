"""
Main app/routing file for Twitoff.
The file that holds the function `create_app`
to collect our modules and organize the flask app.
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user

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
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
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
        #insert_example_users()
        users = User.query.all()  # SQL equivalent: `SELECT * FROM user;`
        return render_template("base.html", title='Home', users=users)   

    @app.route("/reset")
    # Function used on /reset page
    # Drop all from database and creates it again based on insert _example_users
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Just Reset")

    @app.route("/compare", methods=["POST"])
    def compare():
        """This will be presented when we visit '<BASE_URL>/compare '"""
        user0, user1 = sorted(
            [request.values["user0"], request.values["user1"]])
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )
        return render_template("prediction.html", title="prediction", message=message)
    
    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=''):
        """This will be presented when we visit '<BASE_URL>/user '"""
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} succesfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error handling {}: {}".format(name, e)
            tweets = []
        return render_template("user.html", title=name,tweets=tweets, message=message)

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
    DB.session.add(jackblack)
    DB.session.add(elonmusk)
    DB.session.commit()