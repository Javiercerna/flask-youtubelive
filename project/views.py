from flask import url_for, redirect, render_template, \
                     request, session, abort, jsonify
from live_streaming_api import requestAccessToken
from project import app, db
from project.models import User
import os
import json

@app.route('/')
def mainInterface():
    return 'Hello World'

@app.route('/oauth2callback/')
def accessYoutubeAccount():
    if ('code' not in request.args):
        auth_uri = requestAccessToken(url_for('accessYoutubeAccount',
                                              _external=True))
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        template = 'Signed in<br> Code: ' + auth_code
        return template

