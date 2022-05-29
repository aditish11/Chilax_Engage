from flask import render_template, Blueprint, request, redirect, url_for, session
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
from app.spotify_api.spotify_handler import SpotifyHandler
from app.cluster import Final_Recommendations
search_blueprint = Blueprint('search_bp', __name__, template_folder='templates')

#for handling API
sp=SpotifyHandler()

sns.set()

#reading the hindi songs data
data = pd.read_csv("app/song_data.csv")

df = data.drop(columns=['name'])
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
    
recommendations = Final_Recommendations(data)
newlist=[]
result=[]
@search_blueprint.route("/search", methods=['GET', 'POST'])
def search():
    list_of_songs=data['name'].tolist()
    authorization_header = session['authorization_header']

    newlist=[]
    result=[]
    img_details=[]
    if request.method == 'POST':
        search = request.form['search']
        #getting recommendations from the input given by user
        #recommend function from Final_Recommendations class
        #getting 10 songs for recommendations
        newlist = recommendations.recommend(search, 10)
        temp=newlist.values.tolist()
        result=(list(list(zip(*temp))[0]))
           
        i=0
        #getting song information
        for song in result:
          temp=sp.get_img_and_url(authorization_header,song) 
          img_details.append(temp[0])
          i=i+1
          if(i>9):
              break
            
        
    return render_template("search.html",result=result,img_details=img_details, list_of_songs=list_of_songs)
    