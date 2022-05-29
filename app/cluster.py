from flask import Flask,render_template,request
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

app = Flask(__name__)

sns.set()

data_english = pd.read_csv("app/english_songs.csv")
data_hindi=pd.read_csv("app/song_data.csv")
df = data_hindi.drop(columns=['name'])
df.fillna(0)
df.corr()

dh = data_english.drop(columns=['artists'])
dh.fillna(0)
dh.corr()

from sklearn.preprocessing import MinMaxScaler
datatypes1 = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
normarization1 = data_hindi.select_dtypes(include=datatypes1)
for col in normarization1.columns:
    MinMaxScaler (col)

from sklearn.preprocessing import MinMaxScaler
datatypes2 = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
normarization2 = data_english.select_dtypes(include=datatypes2)
for col in normarization2.columns:
    MinMaxScaler (col)

df.fillna(0)
df.corr()
from sklearn.cluster import KMeans
kmeans1 = KMeans (n_clusters=10)
features1 = kmeans1.fit_predict(normarization1)
data_hindi['features1']=features1
MinMaxScaler(data_hindi['features1'])

dh.fillna(0)
dh.corr()
from sklearn.cluster import KMeans
kmeans2 = KMeans (n_clusters=10)
features2 = kmeans2.fit_predict(normarization2)
data_english['features2']=features2
MinMaxScaler(data_english['features2'])
# print(df.isnull().sum())
# print(df.info())

#class for k-means clustering
class Final_Recommendations ():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount=1):
        distance=[]
        song = self.dataset[(self.dataset.name.str.lower() == songs.lower())].head(1).values[0]
        rec = self.dataset[self.dataset.name.str.lower() != songs.lower()]
        for songs in tqdm(rec.values):
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [1, 6, 12, 14, 18]:
                    try:
                        d = d + np.absolute(float(song[col])-float(songs[col]))
                    except:
                        print("",end="")
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['name']
        return rec[columns][:amount]

recommendations = Final_Recommendations(data_hindi)
newlist=[]
result=[]



