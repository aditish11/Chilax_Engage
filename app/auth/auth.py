import os
from flask import Blueprint, request, redirect, url_for, session

from app.spotify_api.spotify_client import SpotifyClient

auth_blueprint = Blueprint('auth_bp', __name__)

#this is client ID and client Secret for my application
os.environ['CLIENT_ID']="YOUR CLIENT ID"
os.environ['CLIENT_SECRET']="YOUR CLIENT SECRET"

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
spotify_client = SpotifyClient(client_id, client_secret, port=8002)



#redirect to Spotify's log in page
@auth_blueprint.route("/login", methods=['POST', 'GET'])
def login():
    auth_url = spotify_client.get_auth_url()
    return redirect(auth_url)



#setting the authorization header for the session
@auth_blueprint.route("/callback")
def callback():
    
    auth_token = request.args['code']
    spotify_client.get_authorization(auth_token)
    authorization_header = spotify_client.authorization_header
    session['authorization_header'] = authorization_header
    return redirect(url_for("index_bp.index"))
