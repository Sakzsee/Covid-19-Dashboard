import streamlit as st 
import pandas as pd 
import numpy as np 
import pydeck as pdk 
import altair as alt 
import datetime
from time import sleep

# Load data
st.markdown(
'''
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Suez+One">

    <div style="font-family: 'Suez One';font-size:70px; background-color:black; color:white"><center>Covid-19 Global Dashboard</center></div>
''',unsafe_allow_html=True
)

st.header(" ")
DATA_URL = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
@st.cache(allow_output_mutation=True)

def load_data():
    df = pd.read_csv(DATA_URL)
    countries = pd.read_csv("covid.csv")
    a = countries['Country'].unique().tolist()
    b = df['location'].unique().tolist()

    exclude_list = [i for i in b if i not in a]

    for i in exclude_list:
        df = df[df['location'] != i]
    

    lat = [countries[countries['Country'] == i]['Latitude'].tolist()[0] for i in df['location']]
    long = [countries[countries['Country'] == i]['Longitude'].tolist()[0] for i in df['location']]
    
    df['Longitude'] = long
    df['Latitude'] = lat

    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d' ).dt.strftime('%Y-%m-%d')
    return df

# Load rows of data into the dataframe.
df = load_data()

#today's date
date = datetime.date.today()

#Getting total no. of cases currently
total_no_cases = df[df['date'] == date.strftime("%Y-%m-%d")]['total_cases'].sum()

st.markdown(
'''
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Bebas+Neue">

    <div style="font-family: 'Babas Neue'; font-size:40px; color:red">Total number of cases:</div>
''',unsafe_allow_html=True
)
st.title(str(total_no_cases))

#Getting total no. of deaths currently
total_no_deaths = df[df['date'] == date.strftime("%Y-%m-%d")]['total_deaths'].sum()

st.markdown(
'''
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Bebas+Neue">

    <div style="font-family: 'Babas Neue'; font-size:40px; color:red">Total number of deaths:</div>
''',unsafe_allow_html=True
)
st.title(str(total_no_deaths))

#Filtering India data
filter_data = df[(df['date'] >='2020-01-01') & (df['Country']== 'India')].set_index("date")

st.markdown( "India daily Death cases from 1st January 2020")

st.bar_chart(filter_data[['total_deaths']])


# Widget by country name
if len(country_name_input) > 0:
    subset_data = df[df['Country'].isin(country_name_input)]

## linechart

st.subheader('Comparision of infection growth')

total_cases_graph  =alt.Chart(subset_data).transform_filter(
    alt.datum.total_cases > 0  
).mark_line().encode(
    x=alt.X('date', type='nominal', title='Date'),
    y=alt.Y('sum(total_cases):Q',  title='Confirmed cases'),
    color='Country',
    tooltip = 'sum(total_cases)',
).properties(
    width=1500,
    height=600
).configure_axis(
    labelFontSize=17,
    titleFontSize=20
)

st.altair_chart(total_cases_graph)
