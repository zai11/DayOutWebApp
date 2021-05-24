from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event#, Comment
from .forms import EventForm#, CommentForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')

def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    dp_upload_path='/static/image' + secure_filename(filename)
    fp.save(upload_path)
    return dp_upload_path


""" @bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    comment_form = CommentForm()
    return render_template('events/show.html', event=event, cform=comment_form)
"""

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
                               form.start_time.data.hour, form.start_time.data.minute)
    end_date_time = datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day,
                               form.end_time.data.hour, form.end_time.data.minute)
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