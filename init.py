from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy(app) #passing the app object into the instance of SQLAlchemy
# print(db.__dict__) #can comment out this line

ma = Marshmallow(app) # set up instance of Marshmallow and passing through the app object
#creating a bcrypt instance and passing it into the flask application
bcrypt = Bcrypt(app)

jwt = JWTManager(app)
