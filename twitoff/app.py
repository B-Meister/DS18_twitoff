"""Main app/routing file for Twitoff!"""

# import flask
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import insert_example_users, add_or_update_user
from os import getenv
from .predict import predict_user


def create_app():
    app = Flask(__name__)
    # making the database for the API so we can reference
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializes the database within our app
    DB.init_app(app)
    # DB.create_all()

    # TODO make the app

    # listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        # a SELECT * query (in SQLAlchemy form)
        # users = User.query.all()
        # insert_example_users()
        # rendering template that we created passing Home to template
        return render_template('base.html', title='Home Page', users=User.query.all())

    @app.route('/example')
    def example():
        insert_example_users()
        return render_template('base.html', title='Added Example Users', users=User.query.all())

    @app.route('/update', methods=['GET'])
    def update():
        # add_or_update_user(request.values['user_name'])
        return render_template('base.html', title='Updated User List', users=User.query.all())

    @app.route('/reset')
    def reset():
        # "cleans" the database
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    # two decorators/routes depending upon actions in user.html file
    @app.route('/user', methods=['POST'])  # POST = changes available info FOR users
    @app.route('/user/<name>', methods=['GET'])  # GET = pulls inputted info FROM users
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                # add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            # assign empty list for tweets and display nothing since iterated through in user.html
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])  # POST=changing something for the users
    def compare():

        # using request to access user input(variables referenced in the html file)
        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        if user0 == user1:
            message = 'Cannot compare a user with themselves'
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0,
                user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/party')
    def party():
        return render_template('party.html', title='PARTY TIME!', message='Democracy requires participation')

    return app
