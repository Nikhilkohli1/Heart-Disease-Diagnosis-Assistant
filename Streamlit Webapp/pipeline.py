import luigi
import numpy as np
import pandas as pd
import pickle
import statistics
import streamlit as st
import os
#from sklearn.externals import joblib 
#import joblib
from features_utils import *

#os.chdir('N:/GITHUB/Data-Science-Machine-Learning/Heart Disease Classification Web App/Streamlit Webapp')


class DataPreprocessing(luigi.Task):
    
    def output(self):
        return luigi.LocalTarget('featuresDP.csv')
    
    def run(self):
        df_pred = pd.read_csv('./inputData.csv', index_col=[0])
        
        lookup_cols = ['sex', 'chest_pain_type','fasting_blood_sugar', 'resting_ECG',
               'exercise_induced_angina', 'slope','thalium_stress']
        for col in lookup_cols:
            df_pred[col] = df_pred[col].apply(lambda x: cat_lookup[x])
            
        #cat_dummies = [col for col in original_features
        #      if '_' in col and '_'.join(col.split('_')[:-1]) in categorical_cols]
        
        df_heart = pd.get_dummies(df_pred, prefix_sep='_', columns=categorical_cols)
                
        df_heart.to_csv(self.output().path)
        
        
    
class FeatureEngineering(luigi.Task):
    
    def requires(self):
        yield DataPreprocessing()
        
    def output(self):
        return luigi.LocalTarget('featuresFE.csv')
    
    
    def run(self):
        
        df_heart= pd.read_csv(DataPreprocessing().output().path,  index_col=[0])
        ## Remove additional columns
        for col in df_heart.columns:
            if(('_' in col) and ('_'.join(col.split('_')[:-1]) in categorical_cols) and col not in cat_dummies):
                print('Removing additional feature {} not used in training'.format(col))
                df_heart.drop(columns=[col], axis=1, inplace=True)
                
        #add missing columns
        for col in cat_dummies:
            if col not in df_heart.columns:
                print('Adding missing feature {}'.format(col))
                df_heart[col] = 0
        
        #feature scaling 
        
        scalerfile = './Models/scaler.sav'
        scaler = pickle.load(open(scalerfile, 'rb'))
        features_SS = scaler.transform(df_heart)
        
        features_SS = pd.DataFrame(features_SS, columns=df_heart.columns)
        features_SS.to_csv(self.output().path)
        
        
class PredictEnsemble(luigi.Task):
    def requires(self):
        yield FeatureEngineering()
        
    def output(self):
        return luigi.LocalTarget('prediction.txt')
    
    def run(self):
        features_SS = pd.read_csv(FeatureEngineering().output().path,  index_col=[0])
        #selecting features for each of 3 models
        features_RF = features_SS[original_features]
        features_Logit = features_SS[selected_features]
        features_knn = features_SS[original_features]
        
        # load models from directory 
        rf = pickle.load(open('./Models/RandomForestclf.pkl', 'rb'))
        logit = pickle.load(open('./Models/LogisticRegression.pkl', 'rb'))
        knn = pickle.load(open('./Models/KNNClassifier.pkl', 'rb'))
        
        pred_rf = rf.predict(features_RF)
        pred_logit = logit.predict(features_Logit)
        pred_knn = knn.predict(features_knn)
        #Ensemble Max Voting Prediction
        print('RF :' ,pred_rf)
        print('logit :', pred_logit)
        print('knn :', pred_knn)
        ensemble_pred = statistics.mode([int(pred_logit), int(pred_knn), int(pred_rf)])
        ensemble_diagnostic = ''
        if ensemble_pred == 0:
            ensemble_diagnostic = 'does not have a Heart Disease'
        else:
            ensemble_diagnostic = 'might have a Heart Disease. Please perform further tests.'
        with self.output().open('w') as pred_file:
            pred_file.write(ensemble_diagnostic)
        
        
if __name__ == '__main__':
    luigi.run()