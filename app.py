from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__) #creating an instance of a Flask application
# print(app.config)

# database connection string below:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello_db'
# change the credentials to the dev one after remaking the user

db = SQLAlchemy(app) #passing the app object into the instance of SQLAlchemy
# print(db.__dict__) #can comment out this line

class Card(db.Model): # inheriting from db.Model to create table
    __tablename__ = 'cards' #plural table name is standard relational database convention

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #specifying a length limit
    description = db.Column(db.Text()) #text will have no limit on length
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
    db.drop_all() #drops all the tables, and ...
    db.create_all() #re-creates the tables from scratch
    print('Tables created successfully')

@app.cli.command('seed') #command for seeding data
def seed_db():
    # create an instance of the Card model in memory
    # card1 = Card(
    #     title = 'Start the project',
    #     description = 'Stage 1 - Create an ERD',
    #     date_created = date.today()
    # )
    # card2 = Card(
    #     title = 'ORM Queries',
    #     description = 'Stage 2 - Implement several queries',
    #     date_created = date.today()
    # )
    # card3 = Card(
    #     title = 'Marshmallow',
    #     description = 'Stage 3 - Implement JSONify of models',
    #     date_created = date.today()
    # )
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
    db.session.query(Card).delete()

    # Add the card to the session (i.e. transaction)
    # db.session.add(card1)
    # db.session.add(card2)
    # db.session.add(card3)
    db.session.add_all(cards)

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')

@app.cli.command('all_cards')
def all_cards():
    stmt = db.select(Card) # select * from cards;
    print(stmt)
    # cards = db.session.execute(stmt)
    # print(cards.all()) #this prints a list of tuples
    cards = db.session.scalars(stmt).all() #scalars enables us to print out a list as opposed to a tuple of the cards
    print(cards)
    for flub in cards:
        print(flub.title)
    first_card = db.session.scalars(stmt).first() #selecting and printing just the first card
    print(first_card)

    tworecords = db.select(Card).limit(2)
    printtwo = db.session.scalars(tworecords).all()
    print(printtwo)
    for floob in printtwo:
        print(floob.title)

@app.route('/')
def index():
    return 'Lali ho, friend!'

if __name__ == '__main__':
    app.run(debug=True) #this line runs the instance of Flask