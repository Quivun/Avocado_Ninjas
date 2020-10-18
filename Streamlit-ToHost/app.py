import yfinance as yf
import pandas as pd
import sklearn as sk
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

#@title Answer the following. The higher the answer, the more important a factor is in determining where you live.
#@markdown ---

#@markdown Economy
#@markdown ---
#@markdown How much emphasis do you place on the economy of where you're living?
gdp = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How important is purchasing power to you?
purchase_power = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How important is the cost of rent to you?
rent = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How important is having disposable income?
disposable_income = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown ---

#@markdown Health
#@markdown ---
#@markdown How important is a country's healthcare quality and satisfaction?
health_care = 6 #@param {type:"slider", min:0, max:10, step:1}

#@markdown Is the life expectancy of where you want to live important?
life_expectancy = 3 #@param {type:"slider", min:0, max:10, step:1}

#@markdown ---

#@markdown Personal Values
#@markdown ---
#@markdown Is happinness important to you?
happiness_score = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How important is the quality of life?
quality_of_life = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown Is it important to feel like you have a support system within your community?
social_support = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How much do you value your freedom?
freedom = 6 #@param {type:"slider", min:0, max:10, step:1}
#@markdown Do you care if the average person is generous?
generosity = 2 #@param {type:"slider", min:0, max:10, step:1}
#@markdown ---

#@markdown Common Purchases
#@markdown ---
#@markdown How often do you purchase coffee?
cappuccino = 5 #@param {type:"slider", min:0, max:10, step:1}

#@markdown How often do you go to the cinema?
cinema = 0 #@param {type:"slider", min:0, max:10, step:1}

#@markdown How often do you purchase wine?
wine = 0 #@param {type:"slider", min:0, max:10, step:1}

#@markdown Is the cost of gasoline important to you?
gasoline = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown ---
#@markdown Potential Dangers
#@markdown ---
#@markdown How concerned are you about pollution?
pollution = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How concerned are you about crime?
crime_rating = 8 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How concerned are you about business and government corruption?
corruption = 6 #@param {type:"slider", min:0, max:10, step:1}
#@markdown ---

#@markdown Miscellaneous
#@markdown ---
#@markdown How important is MoveHub's (https://www.movehub.com/city-rankings/) rating to you?
movehub_rating = 0 #@param {type:"slider", min:0, max:10, step:1}
#@markdown Is it important to you to live in a "developed" country?
hdi = 7 #@param {type:"slider", min:0, max:10, step:1}
#@markdown Would you like to have a lot of culturally significant sites in your country?
world_heritage_sites = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown How important is it you to stay within the US?
international = 10 #@param {type:"slider", min:0, max:10, step:1}
#@markdown ---

import numpy as np

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

