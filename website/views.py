from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment, User, Booking
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events=Event.query.all()
    return render_template('index.html', events=events)

@bp.route('/event')
def show():
    return render_template('events/show.html')

@bp.route('/search')
def search():
    #get the search string from request
    if request.args['search']:
        evnt = "%" + request.args['search'] + '%'
        events = Event.query.filter(Event.title.like(evnt)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))

@bp.route('/bookings', methods = ['GET', 'POST'])
@login_required
def bookings():
    
    bookings = Booking.query.filter_by(user_id=current_user.id)
    events = Event.query.filter().all()
    print(current_user.id)
    return render_template('events/booking_history.html', bookings=bookings, events=events)