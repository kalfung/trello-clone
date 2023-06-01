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
    date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
    db.drop_all() #drops all the tables, and ...
    db.create_all() #re-creates the tables from scratch
    print('Tables created successfully')

@app.cli.command('seed') #command for seeding data
def seed_db():
    # create an instance of the Card model in memory
    card = Card(
        title = 'Start the project',
        description = 'Stage 1 - Create an ERD',
        date_created = date.today()
    )

    #Truncate the Card table - keeps the schema, but clears out all the rows
    db.session.query(Card).delete()

    # Add the card to the session (i.e. transaction)
    db.session.add(card)

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')

@app.route('/')
def index():
    return 'Lali ho, friend!'

if __name__ == '__main__':
    app.run(debug=True) #this line runs the instance of Flask