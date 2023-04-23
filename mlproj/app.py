import pickle
import streamlit as st
import pandas as pd
import numpy as np

with open("model.obj", 'rb') as f:
    model = pickle.loads(f.read())

st.title("HR Analysis")
data = pd.read_csv("data.csv")

def missing(feature,cat='median'):
    catg_colm = ['city',
                 'gender',
                 'relevent_experience',
                 'enrolled_university',
                 'education_level',
                 'major_discipline',
                 'company_type',
                 'last_new_job',
                'company_size']
    num_colm = ['city_development_index',
                'relevent_experience',
                'experience',
                'training_hours']
    try:
        if feature in num_colm and cat == 'mean':
            return data[feature].mean()
        elif feature in num_colm and cat == 'median':
            return data[feature].median()
        elif feature in catg_colm and cat == 'mode':
            return data[feature].mode()[0]
    except:
        return np.nan
    
education_dict = {'Primary School' : 0,
                  'High School' : 1,
                  'Graduate' : 2,
                  'Masters' : 3,
                  'Phd' : 4
                  }

# For Reversing the keys and vlues of the dictionary to retrive the encoded values using copmrehension for loop
rev_education_dict = {value: key for key, value in education_dict.items()}
data['education_level'] = data['education_level'].map(education_dict)

data['gender'].fillna(missing(feature='gender',cat='mode'),inplace=True)
data['city'].fillna(missing(feature='city',cat='mode'),inplace=True)
data['enrolled_university'].fillna(missing(feature='enrolled_university',cat='mode'),inplace=True)
data['education_level'].fillna(missing(feature='education_level',cat='mode'),inplace=True)
data['major_discipline'].fillna(missing(feature='major_discipline',cat='mode'),inplace=True)
data['experience'].fillna(missing(feature='experience',cat='median'),inplace=True)
data['company_size'].fillna(missing(feature='company_size',cat='mode'),inplace=True)
data['last_new_job'].fillna(missing(feature='last_new_job',cat='mode'),inplace=True)

education_level = st.selectbox("Education Level", education_dict.keys())
training_hours = st.number_input("Training Hours")
city_development_index = st.number_input("City Development Index")
experience = st.number_input("Experience in years")
last_new_job = st.number_input("Last new job")

def predict():
    user_data = pd.DataFrame({
        "education_level": [education_dict[education_level]],
        "training_hours": [training_hours],
        "city_development_index": [city_development_index],
        "experience": [experience],
        "last_new_job": [last_new_job],
    })

    prediction = model.predict(user_data)[0]
    if prediction:
        st.write("You will be Hired")
    else:
        st.write("Your will not be Hired")

st.button("Predict", on_click=predict)
