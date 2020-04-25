print('Loading libraries...')

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

class Trainer:

    def __init__(self, datapath, save_folder):
        self.save_folder = save_folder

        self.youtube = pd.read_csv(datapath)
        self.youtube = self.youtube.dropna(how='any',axis=0)
        self.youtube.drop(['video_id','thumbnail_link'],axis=1,inplace=True)
        self.youtube.apply(lambda x: len(x.unique()))
        self.youtube.drop(['trending_date','publish_time','tags','title','description','channel_title'],axis=1,inplace=True)

    def trainModels(self):
        Inputs_Treino = self.youtube.iloc[:253,1:4].values
        Outputs_Treino = self.youtube.iloc[:253,-1].values
        Inputs_Teste = self.youtube.iloc[254:,1:4].values
        Outputs_Teste = self.youtube.iloc[254:,-1].values

        nEstimator = [140,160,180,200,220]
        depth = [10,15,20,25,30]

        ##taining views model
        print('starting training...')
        RF = RandomForestRegressor()

        hyperParam = [{'n_estimators':nEstimator,'max_depth': depth}]
        grid = GridSearchCV(RF,hyperParam,cv=5,verbose=1,scoring='r2',n_jobs=-1)
        grid.fit( Inputs_Treino, Outputs_Treino)

        views=self.youtube['views']
        youtube_view=self.youtube.drop(['views'],axis=1,inplace=False)
        train,test,y_train,y_test=train_test_split(youtube_view,views, test_size=0.2,shuffle=False)

        maxDepth=grid.best_params_['max_depth']
        nEstimators=grid.best_params_['n_estimators']

        model = RandomForestRegressor(n_estimators = nEstimators,max_depth=maxDepth)
        model.fit(train, y_train)

        pickle.dump(model, open(self.save_folder+'/viewPredictor.sav', 'wb'))

        print(f'Model score : {model.score(test, y_test)}\n\n\n')

        #training likes model

        likes=self.youtube['likes']
        youtube_like=self.youtube.drop(['likes'],axis=1,inplace=False)
        train,test,y_train,y_test=train_test_split(youtube_like,likes, test_size=0.2,shuffle=False)
        
        hyperParam = [{'n_estimators':nEstimator,'max_depth': depth}]
        grid = GridSearchCV(RF,hyperParam,cv=5,verbose=1,scoring='r2',n_jobs=-1)
        grid.fit(Inputs_Treino,Outputs_Treino)

        maxDepth=grid.best_params_['max_depth']
        nEstimators=grid.best_params_['n_estimators']

        model = RandomForestRegressor(n_estimators = nEstimators,max_depth=maxDepth)
        model.fit(train, y_train)


        pickle.dump(model, open(self.save_folder+'/likePredictor.sav', 'wb'))

        print(f'Model score : {model.score(test, y_test)}\n\n\n')


        #training comments model

        comment_count=self.youtube['comment_count']
        youtube_comment=self.youtube.drop(['comment_count'],axis=1,inplace=False)
        train,test,y_train,y_test=train_test_split(youtube_comment,comment_count, test_size=0.2,shuffle=False)

        
        hyperParam = [{'n_estimators':nEstimator,'max_depth': depth}]
        grid = GridSearchCV(RF,hyperParam,cv=5,verbose=1,scoring='r2',n_jobs=-1)
        grid.fit(Inputs_Treino,Outputs_Treino)

        maxDepth=grid.best_params_['max_depth']
        nEstimators=grid.best_params_['n_estimators']

        model = RandomForestRegressor(n_estimators = nEstimators,max_depth=maxDepth)
        model.fit(train, y_train)

        pickle.dump(model, open(self.save_folder+'/commentPredictor.sav', 'wb'))

        print(f'Model score : {model.score(test, y_test)}\n\n\n')

        print('training completed!!')
        print(f'Models saved in {self.save_folder} folder')


if __name__ == "__main__":
    trainer = Trainer('datasets/INvideos.csv', 'models')
    trainer.trainModels()