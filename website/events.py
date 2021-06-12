import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Booking, Event, Comment, User
from .forms import CommentForm, EventForm, BookingForm
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
  if not id.isnumeric() or int(last_event.id) < int(id):
    return render_template('error404.html'), 404

  event = Event.query.filter_by(id=id).first()
  booking_form = BookingForm()   
  error=None
  if booking_form.validate_on_submit():      
    booking = Booking(tickets_booked=booking_form.tickets_booked.data, user_id = booking_form.user.data, event_id = booking_form.event.data)

    Event.query.filter_by(id=booking.event_id).first()  

    allowed_tickets = event.ticket_capacity  - event.tickets_booked        
    #print(allowed_tickets)
    #print(booking.tickets_booked)
    if booking.tickets_booked == allowed_tickets:
      #print("error123")
      event.status = "Booked"
    else:
      event.status = event.status
      
    if booking.tickets_booked > allowed_tickets:
      #print("error to many tickets booked")
      flash("Please reduce the number of tickets you would like to purchase")
    else:
      db.session.execute("UPDATE events SET tickets_booked = tickets_booked + " + str(booking.tickets_booked) + " WHERE id = " + booking.event_id)
      db.session.add(booking)
      db.session.commit()

  comment_form = CommentForm()
  if comment_form.validate_on_submit():
    #print("Called")
    comment = Comment(text=comment_form.text.data, user_id=current_user.get_id(), event_id=id)
    db.session.add(comment)
    db.session.commit()
    
  comments=[]
  for comment in Comment.query.all():
    for user in User.query.all():
      #print(type(id))
      if (comment.user_id == user.id) and (comment.event_id == int(id)):
        comments.append([comment, user])
      
  return render_template('events/show.html', event = event, booking_form=booking_form, comments=comments, comment_form=comment_form)


@bp.route('/create', methods = ['GET', 'POST'])
#@login_required
def create():
  #print('Method type: ', request.method)
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
  return render_template('events/create.html', form=form, current_time=datetime.now())

@bp.route('/<id>/update', methods = ['GET', 'POST'])
#@login_required
def update(id):
  #print('Method type: ', request.method)
  eventupdate = Event.query.get_or_404(id)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    start_date_time = datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day,
                               form.start_date.data.hour, form.start_date.data.minute)
    end_date_time = datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day,
                               form.end_date.data.hour, form.end_date.data.minute)
    eventupdate.title = form.title.data
    eventupdate.featured_headline = form.featured_headline.data
    eventupdate.description = form.description.data
    eventupdate.status = form.status.data
    eventupdate.image = db_file_path
    eventupdate.category = form.category.data
    eventupdate.location = form.venue.data
    eventupdate.start_date = start_date_time
    eventupdate.end_date = end_date_time
    eventupdate.timezone = form.timezone.data
    eventupdate.ticket_capacity = form.quantity.data
    eventupdate.price = form.price.data
    db.session.commit()
    flash('Your post has been updated!', 'success')
    return redirect(url_for('main.index'))
  elif request.method == 'GET':
    form.title.data = eventupdate.title
    form.featured_headline.data = eventupdate.featured_headline
    form.description.data = eventupdate.description
    form.status.data = eventupdate.status
    db_file_path = eventupdate.image
    form.category.data = eventupdate.category
    form.venue.data = eventupdate.location
    start_date_time = eventupdate.start_date
    end_date_time = eventupdate.end_date
    form.timezone.data = eventupdate.timezone
    form.quantity.data = eventupdate.ticket_capacity
    form.price.data = eventupdate.price
  return render_template('events/update.html', form=form, current_time=datetime.now())