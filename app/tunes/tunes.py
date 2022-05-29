from flask import render_template, Blueprint, request, redirect, url_for, session
from app.cluster import Final_Recommendations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import json
from app.spotify_api.spotify_handler import SpotifyHandler


sns.set() 

pd.options.mode.chained_assignment = None 


result=[]
tunes_blueprint = Blueprint('tunes_bp', __name__, template_folder='templates')
@tunes_blueprint.route("/tunes", methods=['GET', 'POST'])
def tunes():
    result=[]
    authorization_header = session['authorization_header']

    newlist=[]
    
    img_details=[]
    if request.method == 'POST':

        temp=request.form['tunes']
        if temp!="":
            fine_tune_vals = json.loads(f"[{request.form.get('tunes')}]")
            fine_tune_vals = [{val['key']: val['val'] for val in fine_tune_vals}][0]

            if request.method == 'POST':
                    data = pd.read_csv("app/song_data.csv")
                    
                    data.loc[946,'danceability']= float(fine_tune_vals['danceability']) / 10
                    data.loc[946,'energy']= float(fine_tune_vals['energy']) / 10
                    data.loc[946,'loudness']= -60 + (float(fine_tune_vals['loudness']) - 1) * 60 / 9
                    data.loc[946,'acousticness']= float(fine_tune_vals['acousticness']) * 10
                    data.loc[946,'mode']=0
                    data.loc[946,'speechiness']=0
                    data.loc[946, 'liveness']=0
                    data.loc[946, 'valence']=0
                    data.loc[946, 'tempo']=0
                    data.loc[946, 'name']="Variable"
            
            
            data=data.to_csv("app/song_data.csv", index=False)
            df=pd.read_csv("app/song_data.csv")
            df = df.drop(columns=['mode', 'speechiness', 'liveness', 'valence', 'tempo'])

            df.fillna(0)
            df.corr()     
            sp=SpotifyHandler()
            
            from sklearn.preprocessing import MinMaxScaler
            datatypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            normarization = df.select_dtypes(include=datatypes)
            for col in normarization.columns:
                MinMaxScaler (col)
            
            from sklearn.cluster import KMeans
            kmeans = KMeans (n_clusters=10)
            features = kmeans.fit_predict(normarization)
            df['features']=features
            
            MinMaxScaler(df['features'])
            #print (df.columns)
            
            
            recommendations=Final_Recommendations(df)
            newlist=[]
            if request.method == 'POST':
                tunes = request.form['tunes']
                newlist = recommendations.recommend("Variable", 10)
                temp=newlist.values.tolist()
                result=(list(list(zip(*temp))[0]))
                i=0
        for song in result:
          temp=sp.get_img_and_url(authorization_header,song) 
          img_details.append(temp[0])
          i=i+1
          if(i>9):
              break
    return render_template('tunes.html',result=result,img_details=img_details)