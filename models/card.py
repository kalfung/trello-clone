from init import db, ma

class Card(db.Model): # inheriting from db.Model to create table
    __tablename__ = 'cards' #plural table name is standard relational database convention

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #specifying a length limit
    description = db.Column(db.Text()) #text will have no limit on length
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

class CardSchema(ma.Schema): #not the same as a database schema, this is a Marshmallow schema
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'date_created')