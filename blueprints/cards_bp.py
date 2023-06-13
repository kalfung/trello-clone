from flask import Blueprint, request
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

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
    card_info = CardSchema().load(request.json)
    print(card_info)
    return{}