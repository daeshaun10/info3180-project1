from . import db

class PropertyData(db.Model):   ## database model
    __tablename__ = 'property_data'     ##table name

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String)
    rooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    type = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)
   

    ## ------------------------------- initializing function -------------------- ##
    def __init__(self, title, description, rooms, bathrooms, price, type, location, url):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.price = price
        self.type = type
        self.location = location
        self.url = url
    ## -------------------------------------------------------------------------- ##

    def __repr__(self):
        return '<Property %r>' % (self.title)