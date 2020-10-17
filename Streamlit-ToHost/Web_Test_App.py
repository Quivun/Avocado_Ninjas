import yfinance as yf
import pandas as pd
import sklearn as sk
import streamlit as st
import plotly.express as px
import numpy as np

st.write("""
# City Search Tool

There are a lot of factors that go into making a big move, and for many people, the top priority is either their job or their family. But if you’re on your own and you have job flexibility to go basically wherever you want (i.e. you work remotely), then what? In that case, you have the luxury of finding a place that suits you—and not necessarily just your career.

A myriad of decisions go into picking the perfect place to call home — political leanings, crime rates, walkability, affordability, religious affiliations, weather and more — can you make a tool that allows aggie graduates and others to find thier next move?

[High speed internet](https://www.highspeedinternet.com/best-cities-to-live-work-remotely) (of all people?!) made a tool to do this.... but you can do better! Think of more factors: like median income of a location, cuisine, primary ethnicity, pollution index, happiness index, number of coffee shops or microbreweries in the city, etc. There's no end! Furthermore, maybe you are an international student and want to make this tool for global placement! Go for it! Maybe you want to penalize distance from POI's (points of interest) like family. Do it! The world is your oyster!

#### Starter Datasets
- [MoveHub City Ratings](https://www.kaggle.com/blitzr/movehub-city-rankings?select=movehubqualityoflife.csv)
  - [Notebooks for ideas on how to use data](https://www.kaggle.com/blitzr/movehub-city-rankings/notebooks)
- [World City Populations](https://www.kaggle.com/max-mind/world-cities-database?select=worldcitiespop.csv)
- [Rental Price](https://www.kaggle.com/zillow/rent-index)

#### Where to Find More Data
- [Google Datasets](https://datasetsearch.research.google.com/)
- [US Census](https://data.census.gov/cedsci/?q=United%20States)
- [Kaggle Datasets](https://www.kaggle.com/datasets)


#### How We Judge
- *Data Use*: Effectively used data, acquired additional data
- *Analytics*: Effective application of analytics (bonus points for ML/clustering techniques)
- *Visualization*: Solution is visually appealing and useful (Bonus points if you create an interactive tool/ application/ website)
- *Impact*: Clear impact of solution to solving problem

#### Helpful Workshops
- Intro to Python: Sat, 10:30-12:00
- Statistics for Data Scientists: Sat, 10:30-12:00
- How to Win TAMU Datathon: Sat, 13:00-14:00
- Data Wrangling: Sat, 17:00-18:15
- Data Visualization: Sat, 18:30-19:45
- Machine Learning Part 1 - Theory: Sat, 20:00-21:15
- Machine Learning Part 2 - Applied: Sat, 21:30-22:45
""")

df = pd.read_csv('https://drive.google.com/uc?id=1hSMhl-JeTCX-t72KjhasTQoL1LdWSRhw')
st.write(df.head())

df_1= px.data.gapminder()
fig = px.choropleth(df_1, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])
st.write(fig)

movehub_rating = "None" #@param ["None", "Low", "Med", "High"]
purchase_power = "High" #@param ["None", "Low", "Med", "High"]
health_care = "Low" #@param ["None", "Low", "Med", "High"]
quality_of_life = "None" #@param ["None", "Low", "Med", "High"]
pollution = "None" #@param ["None", "Low", "Med", "High"]
crime_rating = "None" #@param ["None", "Low", "Med", "High"]

weights = [
  movehub_rating,
  purchase_power,
  health_care,
  quality_of_life,
  pollution,
  crime_rating,
]
replace = {'None': 0, 'Low': 1, 'Med': 2, 'High': 3}
weights = np.array([replace[x] for x in weights])
weights *= [1, 1, 1, 1, -1, -1]

features = ['Movehub Rating', 'Purchase Power', 'Health Care', 'Quality of Life', 'Pollution', 'Crime Rating']
norm = lambda xs: (xs-xs.min())/(xs.max()-xs.min())

df['Score'] = norm(df[features].dot(weights))*10

fig = px.scatter_mapbox(df.sort_values('Score', ascending=False).round(),
                        lat="lat", lon="lng", color="Score", hover_name="City",
                        hover_data=features,
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1,
                        mapbox_style="carto-positron")
st.write(fig)

df.sort_values('Score', ascending=False)[['City', 'Score'] + features].round()


