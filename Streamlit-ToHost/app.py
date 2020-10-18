import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
st.write("""
# City Search Tool
""")

df = pd.read_csv('https://drive.google.com/uc?export=download&id=1x_zb2qUJkcoCgoCUmTxo8xQn9F7XHwoX')

df_1= px.data.gapminder()
fig = px.choropleth(df_1, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])
st.write(fig)

movehub_rating = "None" #@param ["None", "Low", "Med", "High"]
purchase_power = "High" #@param ["None", "Low", "Med", "High"]
health_care = "Low" #@param ["None", "Low", "Med", "High"]
quality_of_life = "None" #@param ["None", "Low", "Med", "High"]
pollution = "None" #@param ["None", "Low", "Med", "High"]
crime_rating = "None" #@param ["None", "Low", "Med", "High"]

st.write("""# Answer the following. 
The higher the answer, the more important a factor is in determining where you live.""")
st.markdown("---")

st.markdown("Economy")
st.markdown("---")
gdp = st.slider("How much emphasis do you place on the economy of where you're living?", 0,10,1)
purchase_power = st.slider("How important is purchasing power to you?", 0,10,1)
rent = st.slider("How important is the cost of rent to you?", 0,10,1)
disposable_income = st.slider("How important is having disposable income?", 0,10,1)
st.markdown("---")


st.markdown("Health")
st.markdown("---")
health_care = st.slider("How important is a country's healthcare quality and satisfaction?",0,10,1)
life_expectancy = st.slider("Is the life expectancy of where you want to live important?",0,10,1)
st.markdown("---")

st.markdown("Personal Values")
st.markdown("---")
happiness_score = st.slider("Is happinness important to you?",0,10,1)
quality_of_life = st.slider("How important is the quality of life?",0,10,1)
social_support = st.slider("Is it important to feel like you have a support system within your community?",0,10,1)
freedom = st.slider("How much do you value your freedom?",0,10,1)
generosity = st.slider("Do you care if the average person is generous?",0,10,1)
st.markdown("---")

st.markdown("Common Purchases")
st.markdown("---")
cappuccino = st.slider("How often do you purchase coffee?",0,10,1)
cinema = st.slider("How often do you go to the cinema?",0,10,1)
wine = st.slider("How often do you purchase wine?",0,10,1)
gasoline = st.slider("Is the cost of gasoline important to you?",0,10,1)
st.markdown("---")

st.markdown("Potential Dangers")
st.markdown("---")
pollution = st.slider("How concerned are you about pollution?",0,10,1)
crime_rating = st.slider("How concerned are you about crime?",0,10,1)
corruption = st.slider("How concerned are you about business and government corruption?",0,10,1)
st.markdown("---")

st.markdown("Miscellaneous")
st.markdown("---")
movehub_rating = st.slider("How important is MoveHub's (https://www.movehub.com/city-rankings/) rating to you?",0,10,1)
hdi = st.slider("Is it important to you to live in a \"developed\" country?",0,10,1)
world_heritage_sites = st.slider("Would you like to have a lot of culturally significant sites in your country?",0,10,1)
international = st.slider("How important is it you to stay within the US?",0,10,1)
st.markdown("---")

weights = [
  movehub_rating,
  purchase_power,
  health_care,
  quality_of_life,
  pollution,
  crime_rating,
  cappuccino,
  cinema,
  wine,
  gasoline,
  rent,
  disposable_income,
  hdi,
  happiness_score,
  gdp,
  social_support,
  life_expectancy,
  freedom,
  generosity,
  corruption,
  world_heritage_sites,
  international
]
#replace = {'None': 0, 'Low': 1, 'Med': 2, 'High': 3}
#weights = np.array([replace[x] for x in weights])
weights = np.array(weights)
weights *= [1, 1, 1, 1, -1, -1,-1,
            -1, -1, -1, -1, 1, 100, 1,
            100, 100, 100, 100, 100, -100, 1,-100]

weights[11] = weights[11]/10

features = ['Movehub Rating', 'Purchase Power', 'Health Care', 'Quality of Life', 'Pollution', 'Crime Rating','Cappuccino',
            'Cinema', 'Wine', 'Gasoline', 'Avg Rent', 'Avg Disposable Income', 'HDI',
            'Happinness Score', 'GDP/capita', 'Social Support', 'Healthy Life Expectancy',
            'Freedom to make life choices', 'Generosity', 'Perception of Corruption', 'Country World Heritage Count',
            'International'] 
norm = lambda xs: (xs-xs.min())/(xs.max()-xs.min())

df['Score'] = norm(df[features].dot(weights))*100

fig = px.scatter_mapbox(df.sort_values('Score', ascending=False).round(),
                        lat="lat", lon="long", color="Score", hover_name="City",
                        hover_data=features,
                        color_continuous_scale="rainbow", size_max=30, zoom=1,
                        mapbox_style="open-street-map")
st.write(fig)
df.sort_values('Score', ascending=False)[['City', 'Country','Score'] + features]

