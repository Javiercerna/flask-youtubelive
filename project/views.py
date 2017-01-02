from flask import url_for, redirect, render_template, \
                     request, session, abort, jsonify

from project import app, db
from project.models import User
import os
import json

@app.route('/')
def mainInterface():
    return 'Hello World'

