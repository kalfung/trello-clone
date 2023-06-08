from flask import Blueprint
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/cards/')
@cards_bp.route('/cards')
@jwt_required()
# @app.cli.command('all_cards')
def all_cards():
    admin_required()
    # this block has been moved up to the admin_required function
    # user_email = get_jwt_identity()
    # stmt = db.select(User).filter_by(email=user_email)
    # user = db.session.scalar(stmt)
    # if not user.is_admin:
    #     return {'error': 'You must be an admin'}, 401
    
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