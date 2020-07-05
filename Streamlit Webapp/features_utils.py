import pandas
import numpy 

original_features = ['age', 'sex', 'resting_BP', 'serum_cholestoral', 'fasting_blood_sugar',
       'max_heart_rate', 'exercise_induced_angina', 'oldpeak',
       'chest_pain_type_1', 'chest_pain_type_2', 'chest_pain_type_3',
       'resting_ECG_1', 'resting_ECG_2', 'slope_1', 'slope_2',
       'major_vessels_count_1', 'major_vessels_count_2',
       'major_vessels_count_3', 'major_vessels_count_4', 'thalium_stress_1',
       'thalium_stress_2', 'thalium_stress_3']


selected_features = ['sex', 'max_heart_rate', 'exercise_induced_angina', 'oldpeak',
       'chest_pain_type_1', 'chest_pain_type_2', 'chest_pain_type_3',
       'slope_2', 'major_vessels_count_1', 'major_vessels_count_2',
       'major_vessels_count_3', 'thalium_stress_3']


original_cols = ['age', 'sex', 'chest_pain_type', 'resting_BP', 'serum_cholestoral',
       'fasting_blood_sugar', 'resting_ECG', 'max_heart_rate',
       'exercise_induced_angina', 'oldpeak', 'slope', 'major_vessels_count',
       'thalium_stress']

categorical_cols = [
 'chest_pain_type',
 'resting_ECG',
 'slope',
 'major_vessels_count',
 'thalium_stress']


cat_lookup = {'Male':1, 'Female':0, 'Typical Angina':0, 'Atypical Angina':1, 'Non-anginal pain':2, 'Asymptomatic':3, 
             'fasting blood sugar > 120 mg/dl':1, 'fasting blood sugar < 120 mg/dl':0, 
              'Nothing to Note':0, 'ST-T Wave abnormality':1, 'Left Ventricular Hypertrophy':2, 
             'Yes':1, 'No':0, 'Unslopping: Better heart rate with exercise':0, 'Flatsloping: Minimal change':1,
              'Downslopings: Signs of unhealthy heart':2, 'Normal:1':0, 'Normal:3':1, 'Fixed defect:6':2, 'Reversable defect:7':3}



cat_dummies = ['chest_pain_type_1',
 'chest_pain_type_2',
 'chest_pain_type_3',
 'resting_ECG_1',
 'resting_ECG_2',
 'slope_1',
 'slope_2',
 'major_vessels_count_1',
 'major_vessels_count_2',
 'major_vessels_count_3',
 'major_vessels_count_4',
 'thalium_stress_1',
 'thalium_stress_2',
 'thalium_stress_3']