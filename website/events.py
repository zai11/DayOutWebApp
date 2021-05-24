from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
#from .forms import EventForm, CommentForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

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

@bp.route('/create', method=['GET', 'POST'])
@login_required
def create():
    print(f'Method Type: {request.method}')
    event_form = EventForm()

    if event_form.validate_on_submit():
        db_file_path = check_upload_file(event_form)
        event = Event(
            name = event_form.name.data,

        ) """