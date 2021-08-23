import streamlit as st
import pickle
import numpy as np 

def load_model():
	with open('saved_steps.pkl','rb') as file:
		data = pickle.load(file)
	return data

data = load_model()    

regressor_loaded = data['model']
le_country = data['le_country']
le_education = data['le_education']

def show_predict_page():
	st.title("Software Developer Salary Prediction")


	st.write("""### We need some information to predict the salary""")


	countries=(
	'United States'
	,'India'
	,'United Kingdom'
	,'Germany'
	,'Canada'
	,'Brazil'
	,'France'
	,'Spain'
	,'Australia'
	,'Netherlands'
	,'Poland'
	,'Italy'
	,'Russian Federation'
	,'Sweden')

	education=('Bachelor’s degree'
	,'Master’s degree'
	,'Less than a Bachelor’s'
	,'Post grad')

	country = st.selectbox("Country",countries)

	education_lvl = st.selectbox("Education Level",education)

	experience = st.slider("Year's of experience",0,50,3)

	ok = st.button("Calculat Salary")

	if ok:
		X = np.array([[country,education_lvl,experience]])
		X[:,0]=le_country.transform(X[:,0])
		X[:,1]=le_education.transform(X[:,1])
		X = X.astype(float)

		salary = regressor_loaded.predict(X)

		st.subheader(f"The estimated salary is ${salary[0]:.2f}")