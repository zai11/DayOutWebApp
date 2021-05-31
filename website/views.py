from flask import Blueprint, render_template
from .models import Event

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events=Event.query.all()
    return render_template('index.html', events=events)

@bp.route('/event')
def show():
    return render_template('events/show.html')