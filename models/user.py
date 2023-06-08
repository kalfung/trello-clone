from init import db, ma

class User(db.Model):
    __tablename__ = 'users' # plural due to standard relational database naming convention for tables

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True) #every value in this column MUST be unique
    password = db.Column(db.String, nullable=False) #every user MUST have a password
    is_admin = db.Column(db.Boolean, default=False) # a new user by default will not be an admin

class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email','password', 'is_admin') # password has not been included here