from flask import url_for, redirect, render_template, \
                     request, session, abort, jsonify

import httplib2
from apiclient import discovery
from oauth2client import client
from youtubelive_api import getOrCreateBroadcastExample, getAllLiveStreams, \
                     getLiveStream1080p, bindBroadcast, startBroadcast, \
                     stopBroadcast
from project import app, db
from project.models import User
import os
import json

@app.route('/')
def mainInterface():
    if ('credentials' not in session):
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if (credentials.access_token_expired):
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        youtube = discovery.build('youtube','v3',http_auth)
        broadcast_id = getOrCreateBroadcastExample(youtube)
        live_streams = getAllLiveStreams(youtube)
        # getLiveStream1080p only works with specific encoder brand
        stream_id = getLiveStream1080p(live_streams)
        if (stream_id != None):
            bindBroadcast(youtube,broadcast_id,stream_id)
            startBroadcast(youtube,broadcast_id,stream_id)
            stopBroadcast(youtube,broadcast_id,stream_id)
            return 'Sucessful'
        return 'Error'

@app.route('/oauth2callback/')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'project/client_secrets.json',
        scope='https://www.googleapis.com/auth/youtube',
        redirect_uri=url_for('oauth2callback',_external=True))
    if ('code' not in request.args):
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('mainInterface'))
