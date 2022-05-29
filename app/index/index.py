from flask import render_template, Blueprint, request, session
from app.spotify_api.spotify_handler import SpotifyHandler
index_blueprint = Blueprint('index_bp', __name__, template_folder='templates')
import json
from app.cluster import Final_Recommendations,data_hindi,data_english,dh
import requests

sp=SpotifyHandler()    
rs=Final_Recommendations(data_hindi)               
@index_blueprint.route("/index", methods=['GET', 'POST'])

def index():
    authorization_header = session['authorization_header']

    def extract_letters(string):
        return ''.join([letter for letter in string if not letter.isdigit()])
    
    if request.method == 'GET':
        #For user's name, id, and setting session --------
        profile_data =sp.get_user_profile_data(authorization_header)
        user_display_name, user_id = profile_data['display_name'], profile_data['id']
        session['user_id'], session['user_display_name'] = user_id, user_display_name

        
    
    
    #based on popularity
    data_english.sort_values(
        "popularity",
        ascending=False,
        kind="mergesort"
    )
    popular=data_english['name'].tolist()
    popular_songs=[]
    p=0
    for song in popular:
        temp=sp.get_img_and_url(authorization_header,song)
        popular_songs.append(temp[0])
        p=p+1
        if p>9:
            break

    #Taylor Swift songs
    taylor=dh[dh['artist']=='Taylor Swift']
    taylor.sort_values("popularity", ascending=False)
    temp=taylor['name'].tolist()
    taylor_songs=[]

    i=0
    for song in temp:
        temp1=sp.get_img_and_url(authorization_header,song)
        taylor_songs.append(temp1[0])
        i=i+1
        if i>8:
            break

    #Ariana Grande Songs
    ariana=dh[dh['artist']=='Ariana Grande']
    ariana.sort_values("popularity", ascending=False)
    temp=ariana['name'].tolist()
    ariana_songs=[]

    i=0
    for song in temp:
        temp1=sp.get_img_and_url(authorization_header,song)
        ariana_songs.append(temp1[0])
        i=i+1
        if i>8:
            break    


    #Justin Bieber Songs
    justin=dh[dh['artist']=='Justin Bieber']
    justin.sort_values("popularity", ascending=False)
    temp=justin['name'].tolist()
    justin_songs=[]

    i=0
    for song in temp:
        temp1=sp.get_img_and_url(authorization_header,song)
        justin_songs.append(temp1[0])
        i=i+1
        if i>8:
            break  

         
    #Shawn Mendes Songs
    shawn=dh[dh['artist']=='Shawn Mendes']
    shawn.sort_values("popularity", ascending=False)
    temp=shawn['name'].tolist()
    shawn_songs=[]

    i=0
    for song in temp:
        temp1=sp.get_img_and_url(authorization_header,song)
        shawn_songs.append(temp1[0])
        i=i+1
        if i>8:
            break



    return render_template('index.html',user_display_name=user_display_name,popular_songs=popular_songs,
    taylor_songs=taylor_songs,ariana_songs=ariana_songs
    ,justin_songs=justin_songs,shawn_songs=shawn_songs
    ,func=extract_letters)


   