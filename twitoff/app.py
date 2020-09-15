"""Main app/routing file for Twitoff!"""

# import flask
from flask import Flask, render_template
from .models import DB, User
from .twitter import insert_example_users, add_or_update_user


def create_app():
    app = Flask(__name__)
    # making the database for the API so we can reference
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializes the database within our app
    DB.init_app(app)

    # TODO make the app

    # listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        # a SELECT * query (in SQLAlchemy form)
        users = User.query.all()
        # rendering template that we created passing Home to template
        return render_template('base.html', title='Home Page', users=User.query.all())

    @app.route('/welcome')
    def working_or_nah():
        return f'Gang gang what up Twitoff Users \n Please enjoy this app!'

    @app.route('/example')
    def example():
        insert_example_users()
        return render_template('base.html', title='3 Users have been added', users=User.query.all())

    @app.route('/update')
    def update():
        print('Cannot add your own users at the moment. Coming Soon.')
        return render_template('base.html', title='Updated Users', users=User.query.all())

    @app.route('/reset')
    def reset():
        # "cleans" the database
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/user')
    def user():
        pass

    @app.route('/compare')
    def compare():
        return f'Cannot compare yet. Functionality coming soon.'

    @app.route('/party')
    def party():
        return render_template('party.html', title='PARTY TIME!')

    @app.route('/showtweets')
    def show_tweets():
        _ = User()

    return app
