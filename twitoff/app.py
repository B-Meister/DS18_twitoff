"""Main app/routing file for Twitoff!"""

# import flask
from flask import Flask, render_template
from .models import DB, User, insert_example_users, insert_tweets


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initializes the database within our app
    DB.init_app(app)

    # TODO make the app

    # listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        # 'cleans' the database
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        insert_tweets()

        # a SELECT * query (in SQLAlchemy form)
        users = User.query.all()
        # rendering template that we created passing Home to template
        return render_template('base.html', title='Home Page', users=User.query.all())

    @app.route('/welcome')
    def working_or_nah():
        return f'Gang gang what up Twitoff Users \n Please enjoy this app!'

    @app.route('/update')
    def update():
        return "Can't update yet! Functionality coming soon"

    @app.route('/reset')
    def reset():
        return "Bruh... all that work making the database, just to scrub it?"

    return app
