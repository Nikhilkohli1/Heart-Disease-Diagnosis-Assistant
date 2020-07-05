import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
import os
#from sklearn.externals import joblib 
from features_utils import *
from pipeline import *
from subprocess import call
#import joblib


st.title('Heart Disease Diagnosis Assistant')
st.markdown('This application is meant to **_assist_ _doctors_ _in_ diagnosing**, if a patient has a **_Heart_ _Disease_ _or_ not** using few details about their health')

st.markdown('Please **Enter _the_ _below_ details** to know the results -')

age = st.text_input(label='Age')

gender_ls = ['Male', 'Female']
sex = st.selectbox('Gender', gender_ls)

cp_ls = ['Typical Angina', 'Atypical Angina', 'Non-anginal pain', 'Asymptomatic']
cp = st.selectbox('Chest pain Type', cp_ls)

restbp = st.slider('Resting Blood Pressure', 0, 220, 120)

chol = st.slider('Serum Cholestoral in mg/dl', 0, 600, 150)

fbs_ls = ['fasting blood sugar > 120 mg/dl', 'fasting blood sugar < 120 mg/dl']
fbs = st.selectbox('Fasting Blood Sugar (>126 mg/dL signals diabetes)', fbs_ls)


restecg_ls = ['Nothing to Note', 'ST-T Wave abnormality', 'Left Ventricular Hypertrophy']
restecg = st.selectbox('Resting ECG(Electrocardiographic)', restecg_ls)

thalach = st.slider('Maximum Heart Rate Achieved (Thalach)', 0, 250, 100)

exang_ls = ['Yes', 'No']
exang = st.selectbox('Exercise Induced Angina', exang_ls)

oldpeak = st.text_input(label= 'Oldpeak: ST Depression induced by exercise relative to rest (0-6)')

slope_ls = ['Unslopping: Better heart rate with exercise', 'Flatsloping: Minimal change', 'Downslopings: Signs of unhealthy heart']
slope = st.selectbox('Slope of Peak exercise ST Segment', slope_ls)

ca_ls = [0, 1, 2, 3, 4]
ca = st.selectbox('Number of Major vessels colored by flourosopy', ca_ls)

thal_ls = ['Normal:1', 'Normal:3', 'Fixed defect:6', 'Reversable defect:7']
thal = st.selectbox('Thalium Stress result', thal_ls)


ensemble_pred = ''

if st.button('Check Diagnosis'):

    if os.path.exists('inputData.csv'):
        #st.text('yes it exists 1')
        os.remove('inputData.csv')

    if os.path.exists('featuresDP.csv'):
        #st.text('yes it exists 2')
        os.remove('featuresDP.csv')

    if os.path.exists('featuresFE.csv'):
        #st.text('yes it exists 3')
        os.remove('featuresFE.csv')

    if os.path.exists('prediction.txt'):
        #st.text('yes it exists 4')
        os.remove('prediction.txt')


    with st.spinner('Running the Diagnostic.. '):
        #create input dataframe to send as input to Luigi Pipeline
        df_pred = pd.DataFrame([[age, sex, cp, restbp, chol, fbs, 
                        restecg, thalach, exang, oldpeak, slope, ca, thal]], 
                       columns= original_cols)
        df_pred.to_csv('./inputData.csv')

        #ensemble_pred = os.system(pipeline.py)
        #luigi.run()
    try:
        call("python pipeline.py PredictEnsemble --local-scheduler", shell=True)
    except Exception as e:
        st.text(e)

        
    try:
            
        with open('prediction.txt', 'r') as f:
            ensemble_pred = f.read()    
        st.header('The patient {}'.format(str(ensemble_pred)))
    except Exception as e:
        st.header('Please provide all the input values & within range')
        #st.text(e)

    #f = open('pred.txt', 'r')
    #st.text(str(f.read()))

st.text('\n')
st.text('\n')
st.text('\n')
st.text('\n')
st.text('\n')
st.text('\n')
st.text('\n')
st.text('\n')




st.markdown('This Application Uses an **_Ensemble_ _of_ _3_ models(KNN, Logistic, Random Forest for Prediction)**')
st.markdown('**App Framework** - **Streamlit**')
st.markdown('**Inference Pipeline** - **Luigi**')
st.markdown('**Developed by** - Nikhil Kohli')
st.markdown('**www.linkedin.com/in/nikhilkohli92**')
