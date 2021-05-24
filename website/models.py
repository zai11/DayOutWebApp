from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    phone_number = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), index=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20))

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

    # relation to call user.bookings and booking.created_by
    bookings = db.relationship('Booking', backref='user')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    featured_headline = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))
    image = db.Column(db.String(400))
    category = db.Column(db.String(100))
    location = db.Column(db.String(100))
    start_date = db.Column(db.DateTime, default=datetime.now())
    end_date = db.Column(db.DateTime, default=datetime.now())
    timezone = db.Column(db.String(100))
    ticket_capacity = db.Column(db.Integer)
    price = db.Column(db.DECIMAL)


	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)
        

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    tickets_booked = db.Column(db.Integer)

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Booking: {}>".format(self.text)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)