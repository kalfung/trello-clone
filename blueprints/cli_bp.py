from flask import Blueprint
from datetime import date
# from flask_marshmallow import Marshmallow # moved to init.py
# from flask_bcrypt import Bcrypt  # moved to init.py
from models.user import User
from models.card import Card
from init import db, bcrypt

cli_bp = Blueprint('db', __name__) #this is simply a container

@cli_bp.cli.command('create')
def create_db():
    db.drop_all() #drops all the tables, and ...
    db.create_all() #re-creates the tables from scratch
    print('Tables created successfully')

@cli_bp.cli.command('seed') #command for seeding data
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('spinynorman').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='cleese@spam.com',
            password=bcrypt.generate_password_hash('tisbutascratch').decode('utf-8')
        )
    ]

    cards = [
        Card(
        title = 'Start the project',
        description = 'Stage 1 - Create an ERD',
        status='Done', 
        date_created = date.today()
        ),
        Card(
        title = 'ORM Queries',
        description = 'Stage 2 - Implement several queries',
        status='In Progress',
        date_created = date.today()
        ),
        Card(
        title = 'Marshmallow',
        description = 'Stage 3 - Implement JSONify of models',
        status='In Progress',
        date_created = date.today()
        )
    ]

    #Truncate the Card table - keeps the schema, but clears out all the rows
    db.session.query(Card).delete() # truncate the cards table
    db.session.query(User).delete() # truncate the users table

    # Add the card to the session (i.e. transaction)
    db.session.add_all(cards)
    db.session.add_all(users)

    # Commit the transaction to the database
    # until we commit, any queries that we add will simply be queued up until we commit
    db.session.commit()
    print('Models seeded')