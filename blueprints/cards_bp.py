from flask import Blueprint, request
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
@cards_bp.route('') #unsure if this is needed
@jwt_required()
# @app.cli.command('all_cards')
def all_cards():
    admin_required()
    
    stmt = db.select(Card).order_by(Card.status.desc()) # select * from cards;
    print(stmt)
    # cards = db.session.execute(stmt)
    # print(cards.all()) #this prints a list of tuples
    cards = db.session.scalars(stmt).all() #scalars enables us to print out a list as opposed to a tuple of the cards
    print(cards)
    for flub in cards:
        print(flub.title)
    # return json.dumps(cards) #this line doesn't work
    return CardSchema(many=True, exclude=['date_created']).dump(cards) #returning the Marshmallow schema

#Get one card
@cards_bp.route('/<int:card_id>')
@cards_bp.route('/<int:card_id>/')
def one_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': 'Card not found'}, 404
    
#Create a new card
@cards_bp.route('/', methods=['POST'])
def create_card():
    # Load the incoming POST data via the schema
    card_info = CardSchema().load(request.json)
    # Create a new Card instance from the card_info
    card = Card(
        title = card_info['title'],
        description = card_info['description'],
        status = card_info['status'],
        date_created = date.today()
    )
    # Add and commit the new card to the session
    db.session.add(card)
    db.session.commit()
    # Send the new card back to the client
    return CardSchema().dump(card), 201

#Update a card
@cards_bp.route('/<int:card_id>', methods=['PUT', 'PATCH'])
# @cards_bp.route('/<int:card_id>/', methods=['PUT', 'PATCH'])
def update_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    card_info = CardSchema().load(request.json)
    if card:
        card.title = card_info.get['title', card.title]
        card.description = card_info.get['description', card.description]
        card.status = card_info.get['status', card.status]
        db.session.commit() # DB does not update if it is not committed
        return CardSchema().dump(card)
    else:
        return {'error': 'Card not found'}, 404
    
# Delete a card
@cards_bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete_card(card_id):
  admin_required()
  stmt = db.select(Card).filter_by(id=card_id)
  card = db.session.scalar(stmt)
  if card:
    db.session.delete(card)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Card not found'}, 404