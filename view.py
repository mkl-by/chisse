from app import app, csrf
from flask import render_template, redirect
from flask_security import login_required

@app.route('/')
def hello_world():
    return render_template('index.html')


