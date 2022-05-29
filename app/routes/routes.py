import json
import requests
from flask import render_template, Blueprint, request, redirect, session
from app.spotify_api.spotify_handler import SpotifyHandler

blueprint = Blueprint('app', __name__)


@blueprint.route("/not-found")
def not_found():
    return render_template('../error/templates/error/404.html')



