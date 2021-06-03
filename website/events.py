import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Booking, Event, Comment
from .forms import EventForm
from .forms import BookingForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('event', __name__, url_prefix='/events')

def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(BASE_PATH, 'static/image/', secure_filename(filename))
    dp_upload_path='/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return dp_upload_path


@bp.route('/<id>', methods = ['GET', 'POST'])
def show(id):
  last_event = Event.query.order_by(Event.id.desc()).first()
  print(str(last_event.id) + "BITCH")
  if not id.isnumeric() or int(last_event.id) < int(id):
    print("WOWOWOWOWOWOWWOOWWOOWOWOWOWOWOWOWOWOW")
    return render_template('error404.html'), 404

  event = Event.query.filter_by(id=id).first()
  form = BookingForm()   
  error=None
  if form.validate_on_submit():      
    booking = Booking(tickets_booked=form.tickets_booked.data, user_id = form.user.data, event_id = form.event.data)

    Event.query.filter_by(id=booking.event_id).first()

    allowed_tickets = event.ticket_capacity  - event.tickets_booked    
    print(allowed_tickets)
    print(booking.tickets_booked)

    if booking.tickets_booked > allowed_tickets:
      print("error to many tickets booked")
      flash("Please reduce the number of tickets you would like to purchase")
    else:
      db.session.execute("UPDATE events SET tickets_booked = tickets_booked + " + str(booking.tickets_booked) + " WHERE id = " + booking.event_id)
      db.session.add(booking)
      db.session.commit()
  return render_template('events/show.html', event = event, form=form)


@bp.route('/create', methods = ['GET', 'POST'])
#@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    # if the form was successfully submitted
    # access the values in the form data
    start_date_time = datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day,
                               form.start_date.data.hour, form.start_date.data.minute)
    end_date_time = datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day,
                               form.end_date.data.hour, form.end_date.data.minute)
    event = Event(title=form.title.data, 
                featured_headline=form.featured_headline.data,
                description=form.description.data,
                status=form.status.data,
                image=db_file_path,
                category=form.category.data,
                location=form.venue.data,
                start_date=start_date_time,
                end_date=end_date_time,
                timezone=form.timezone.data,
                ticket_capacity=form.quantity.data,
                price=form.price.data)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    return redirect(url_for('main.index'))
  return render_template('events/create.html', form=form)