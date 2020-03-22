from flask import Blueprint, render_template
from app import app
from flask_security import login_required


statistic=Blueprint('statistic', __name__, template_folder='templates')

@statistic.route('/')
@login_required
def hello():
    return render_template('ind.html')