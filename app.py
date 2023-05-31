from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
# print(app.config)

# database connection string below:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello_db'
# change the credentials to the dev one after remaking the user

db = SQLAlchemy(app)
# print(db.__dict__) #can comment out this line

class Card(db.Model): # inheriting from db.Model
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #specifying a length limit
    description = db.Column(db.Text()) #text will have no limit on length
    date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created successfully')

@app.cli.command('seed') #seeding data
def seed_db():
    # create an instance of the Card model in memory
    card = Card(
        title = 'Start the project',
        description = 'Stage 1 - Create an ERD',
        date_created = date.today()
    )

    #Truncate the Card table
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
    app.run(debug=True) 