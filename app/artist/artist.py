from flask import render_template, Blueprint, request, redirect, url_for, session
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
from app.spotify_api.spotify_handler import SpotifyHandler
artist_blueprint = Blueprint('artist_bp', __name__, template_folder='templates')

sp=SpotifyHandler()

sns.set()

data = pd.read_csv("app/english_songs.csv")

df = data.drop(columns=['artists'])
df.fillna(0)
df.corr()

from sklearn.preprocessing import MinMaxScaler
datatypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
normarization = data.select_dtypes(include=datatypes)
for col in normarization.columns:
    MinMaxScaler (col)

from sklearn.cluster import KMeans
kmeans = KMeans (n_clusters=10)
features = kmeans.fit_predict(normarization)
data['features']=features

MinMaxScaler(data['features'])

# print(df.isnull().sum())
# print(df.info())
    
newlist=[]
result=[]
@artist_blueprint.route("/artist", methods=['GET', 'POST'])
def artist():
    list_of_artists=df['artist'].tolist()
    authorization_header = session['authorization_header']
    artist_songs=[]

    if request.method == 'POST':
        artist_name = request.form['artist']
        artist_temp=df[df['artist']==artist_name]
        artist_temp.sort_values("popularity", ascending=False)
        temp=artist_temp['name'].tolist()

        i=0
        for song in temp:
            temp1=sp.get_img_and_url(authorization_header,song)
            artist_songs.append(temp1[0])
            i=i+1
            if i>9:
                break    
            
            
        
    return render_template("artist.html",result=result,artist_songs=artist_songs, list_of_artists=list_of_artists)
    