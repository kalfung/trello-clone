from flask import Blueprint, request, abort
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@auth_bp.route('/register/', methods=['POST'])
def register():
    try:
        #Parse, sanitise and validate the incoming JSON data via the schema
        user_info = UserSchema().load(request.json)
        # create a new user model instance with the schema data
        user = User(
            email=user_info['email'], 
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
            name=user_info['name']
        )

        #Add and commit the new user
        db.session.add(user)
        db.session.commit()
        
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409
        # print(user)
        # # print(request.json)
        # return{}

@auth_bp.route('/login', methods=['POST'])
@auth_bp.route('/login/', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt) #returns a single result, not in a list
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            return {'token':token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email address and password are required'}, 400


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)