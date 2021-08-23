import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(cat,cutoff):
    category_map = {}

    for i in range(len(cat)):
        if cat.values[i]>= cutoff:
            category_map[cat.index[i]]=cat.index[i]
        else:
            category_map[cat.index[i]]='Other'
    
    return category_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x=='Less than 1 year':
        return 0.5
    else:
        return float(x)


def clean_degree(y):
    if "Bachelor’s degree" in y:
        return "Bachelor’s degree"
    if "Master’s degree" in y:
        return "Master’s degree"
    if "Professional degree" in y or "Other doctoral" in y:
        return "Post grad"
    else:
        return "Less than a Bachelor’s"

@st.cache
def load_data():
	df = pd.read_csv("developer_survey_2020/survey_results_public.csv")                    

	df_new = df[['Country','EdLevel','YearsCode','Employment','ConvertedComp']]
	df_new = df_new.rename({'ConvertedComp':'Salary'},axis=1)

	df_new=df_new[df_new['Salary'].notnull()]
	df_new = df_new.dropna()

	df_new = df_new[df_new['Employment']=='Employed full-time']
	df_new = df_new.drop('Employment',axis=1)

	country_map = shorten_categories(df_new.Country.value_counts(),400)
	df_new['Country'] = df_new['Country'].map(country_map)

	df_new = df_new[df_new['Salary']<=250000]
	df_new = df_new[df_new['Salary']>=10000]
	df_new = df_new[df_new['Country']!='Other']

	df_new['YearsCode'] = df_new['YearsCode'].apply(clean_experience) 
	
	df_new['EdLevel'] = df_new['EdLevel'].apply(clean_degree) 

	return df_new

df = load_data()	

def show_explore_page():
	st.title("Explore Software Engineer Salaries")

	st.write("""
		### Stack Overflow Developer Survey 2020
		""")

	data = df["Country"].value_counts()

	fig1, ax1 = plt.subplots()
	ax1.pie(data,labels=data.index,startangle=90,autopct="%1.1f")
	ax1.axis("equal")

	st.write("""#### Number of Data from different Countries""")

	st.pyplot(fig1)

	st.write("""#### Mean Salary Based on Country""")

	data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

	st.bar_chart(data)

	st.write("""#### Mean Salary Based on Experience""")

	data = df.groupby(["YearsCode"])["Salary"].mean().sort_values(ascending=True)

	st.line_chart(data)	