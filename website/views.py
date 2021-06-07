from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment, User

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
