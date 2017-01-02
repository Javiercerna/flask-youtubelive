import requests
import credentials

def requestAccessToken(flask_uri):
    base_url = 'https://accounts.google.com/o/oauth2/auth?'
    client_id = credentials.oauth2_client_id
    redirect_uri = flask_uri
    response_type = 'code'
    scope = 'https://www.googleapis.com/auth/youtube.readonly'
    access_type = 'offline'

    url = (base_url + 'client_id=%s&redirect_uri=%s&response_type=%s&scope=%s&access_type=%s') \
          % (client_id,redirect_uri,response_type,scope,access_type)

    return url
    
if __name__ == '__main__':
    url = requestAccessToken('http://localhost:8888/oauth2callback/')
