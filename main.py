from flask import Flask, request, abort
# from flask_sqlalchemy import SQLAlchemy # moved to init.py
# from datetime import date
# from flask_marshmallow import Marshmallow # moved to init.py
# from flask_bcrypt import Bcrypt  # moved to init.py
# from sqlalchemy.exc import IntegrityError
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from datetime import timedelta
from os import environ
# from dotenv import load_dotenv
# from models.user import User, UserSchema
# from models.card import Card, CardSchema
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.cards_bp import cards_bp

# load_dotenv()

#this is a factory function - it creates and configures an object, and then returns that object
def setup():
    
    app = Flask(__name__) #creating an instance of a Flask application
# print(app.config)

    app.config['JSON_SORT_KEYS'] = False #this line doesn't seem to do anything anymore

# app.config['JWT_SECRET_KEY'] = 'Ministry of Silly Walks'
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

# database connection string below:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
# change the credentials to the dev one after remaking the user

# ----- BELOW THIS LINE has been moved to init 
# db = SQLAlchemy(app) #passing the app object into the instance of SQLAlchemy
# # print(db.__dict__) #can comment out this line

# ma = Marshmallow(app) # set up instance of Marshmallow and passing through the app object
# #creating a bcrypt instance and passing it into the flask application
# bcrypt = Bcrypt(app)

# jwt = JWTManager(app)
#------ ABOVE THIS LINE has been moved to init

# solving the circular import problem
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

# #---- MOVING BELOW THIS LINE TO auth_bp.py
# def admin_required():
#     user_email = get_jwt_identity()
#     stmt = db.select(User).filter_by(email=user_email)
#     user = db.session.scalar(stmt)
#     if not (user and user.is_admin):
#         abort(401)
# #---- MOVING ABOVE THIS LINE TO auth_bp.py


    @app.errorhandler(401)
    def unathorized(err):
        return {'error': 'You must be an admin'}, 401

#----- MOVING BELOW THIS LINE TO USER
# creating a model for the users entity
# class User(db.Model):
#     __tablename__ = 'users' # plural due to standard relational database naming convention for tables

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     email = db.Column(db.String, nullable=False, unique=True) #every value in this column MUST be unique
#     password = db.Column(db.String, nullable=False) #every user MUST have a password
#     is_admin = db.Column(db.Boolean, default=False) # a new user by default will not be an admin

# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('name', 'email','password', 'is_admin') # password has not been included here
#----- MOVING ABOVE THIS LINE TO USER

#----- MOVING BELOW THIS LINE TO CARD
# class Card(db.Model): # inheriting from db.Model to create table
#     __tablename__ = 'cards' #plural table name is standard relational database convention

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100)) #specifying a length limit
#     description = db.Column(db.Text()) #text will have no limit on length
#     status = db.Column(db.String(30))
#     date_created = db.Column(db.Date())

# class CardSchema(ma.Schema): #not the same as a database schema, this is a Marshmallow schema
#     class Meta:
#         fields = ('id', 'title', 'description', 'status', 'date_created')
#----- MOVING ABOVE THIS LINE TO CARD

#----- MOVING BELOW THIS LINE TO cli_bp.py
# @app.cli.command('create')
# def create_db():
#     db.drop_all() #drops all the tables, and ...
#     db.create_all() #re-creates the tables from scratch
#     print('Tables created successfully')

# @app.cli.command('seed') #command for seeding data
# def seed_db():
#     users = [
#         User(
#             email='admin@spam.com',
#             password=bcrypt.generate_password_hash('spinynorman').decode('utf-8'),
#             is_admin=True
#         ),
#         User(
#             name='John Cleese',
#             email='cleese@spam.com',
#             password=bcrypt.generate_password_hash('tisbutascratch').decode('utf-8')
#         )
#     ]


#     # create an instance of the Card model in memory
#     # card1 = Card(
#     #     title = 'Start the project',
#     #     description = 'Stage 1 - Create an ERD',
#     #     date_created = date.today()
#     # )
#     # card2 = Card(
#     #     title = 'ORM Queries',
#     #     description = 'Stage 2 - Implement several queries',
#     #     date_created = date.today()
#     # )
#     # card3 = Card(
#     #     title = 'Marshmallow',
#     #     description = 'Stage 3 - Implement JSONify of models',
#     #     date_created = date.today()
#     # )
#     cards = [
#         Card(
#         title = 'Start the project',
#         description = 'Stage 1 - Create an ERD',
#         status='Done', 
#         date_created = date.today()
#         ),
#         Card(
#         title = 'ORM Queries',
#         description = 'Stage 2 - Implement several queries',
#         status='In Progress',
#         date_created = date.today()
#         ),
#         Card(
#         title = 'Marshmallow',
#         description = 'Stage 3 - Implement JSONify of models',
#         status='In Progress',
#         date_created = date.today()
#         )
#     ]
#     #Truncate the Card table - keeps the schema, but clears out all the rows
#     db.session.query(Card).delete() #truncate the cards table
#     db.session.query(User).delete() # truncate the users table

#     # Add the card to the session (i.e. transaction)
#     # db.session.add(card1)
#     # db.session.add(card2)
#     # db.session.add(card3)
#     db.session.add_all(cards)
#     db.session.add_all(users)

#     # Commit the transaction to the database
#     # until we commit, any queries that we add will simply be queued up until we commit
#     db.session.commit()
#     print('Models seeded')
# ------ MOVING ABOVE THIS LINE TO cli_bp.py

    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cards_bp)

    return app

# # ------ MOVING BELOW THIS LINE TO auth_bp.py
# @app.route('/register', methods=['POST'])
# @app.route('/register/', methods=['POST'])
# def register():
#     try:
#         #Parse, sanitise and validate the incoming JSON data via the schema
#         user_info = UserSchema().load(request.json)
#         # create a new user model instance with the schema data
#         user = User(
#             email=user_info['email'], 
#             password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
#             name=user_info['name']
#         )

#         #Add and commit the new user
#         db.session.add(user)
#         db.session.commit()
        
#         return UserSchema(exclude=['password']).dump(user), 201
#     except IntegrityError:
#         return {'error': 'Email address already in use'}, 409
#         # print(user)
#         # # print(request.json)
#         # return{}

# @app.route('/login', methods=['POST'])
# @app.route('/login/', methods=['POST'])
# def login():
#     try:
#         stmt = db.select(User).filter_by(email=request.json['email'])
#         user = db.session.scalar(stmt) #returns a single result, not in a list
#         if user and bcrypt.check_password_hash(user.password, request.json['password']):
#             token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
#             return {'token':token, 'user': UserSchema(exclude=['password']).dump(user)}
#         else:
#             return {'error': 'Invalid email address or password'}, 401
#     except KeyError:
#         return {'error': 'Email address and password are required'}, 400
# # ------ MOVING ABOVE THIS LINE TO auth_bp.py

#----- MOVING BELOW THIS LINE to cards_bp.py
# @app.route('/cards/')
# @app.route('/cards')
# @jwt_required()
# # @app.cli.command('all_cards')
# def all_cards():
#     admin_required()
#     # this block has been moved up to the admin_required function
#     # user_email = get_jwt_identity()
#     # stmt = db.select(User).filter_by(email=user_email)
#     # user = db.session.scalar(stmt)
#     # if not user.is_admin:
#     #     return {'error': 'You must be an admin'}, 401
    
#     stmt = db.select(Card).order_by(Card.status.desc()) # select * from cards;
#     print(stmt)
#     # cards = db.session.execute(stmt)
#     # print(cards.all()) #this prints a list of tuples
#     cards = db.session.scalars(stmt).all() #scalars enables us to print out a list as opposed to a tuple of the cards
#     print(cards)
#     for flub in cards:
#         print(flub.title)
#     # return json.dumps(cards) #this line doesn't work
#     return CardSchema(many=True, exclude=['date_created']).dump(cards) #returning the Marshmallow schema

#     #just first card
#     first_card = db.session.scalars(stmt).first() #selecting and printing just the first card
#     print(first_card)

#     # just first 2 cards
#     tworecords = db.select(Card).limit(2) #just two cards
#     printtwo = db.session.scalars(tworecords).all()
#     print(printtwo)
#     for floob in printtwo:
#         print(floob.title)

#     # cards that are not Done or ID >2
#     stmt = db.select(Card).where(Card.status != 'Done')
#     stmt = db. select(Card).where(db.or_(Card.status != 'Done', Card.id >2)).order_by(Card.title.desc())
#     inprogresscards = db.session.scalars(stmt).all()
#     for card in inprogresscards:
#         print(card.__dict__)
#----- MOVING ABOVE THIS LINE to cards_bp.py


# # this home route doesn't serve a resource in the API, so we don't need it anymore
# @app.route('/')
# @app.route('/home')
# @app.route('/home/')
# @app.route('/index')
# @app.route('/index/')
# def index():
#     return 'Lali ho, friend!'


# if __name__ == '__main__':
#     app.run(debug=True) #this line runs the instance of Flask