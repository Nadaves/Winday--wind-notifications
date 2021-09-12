from numpy import datetime64
from numpy.core.fromnumeric import size
import requests
import pandas as pd
import json
from urllib.request import urlopen
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
from seaborn.palettes import color_palette
sns.set_theme()

url = "https://stormglass.p.rapidapi.com/forecast"

Spots = { 
    'Beit_Yanai': ['32.38', '34.86'],
    'Sedot_Yam': ['32.49', '34.89'],
    'Eilat': ['29.52', '34.93'],
    'Sea_of_galilee': ['32.87', '35.63']
}

Spot_names = ['Beit_Yanai']
# Spot_names = ['Beit_Yanai', 'Sedot_Yam', 'Eilat', 'Sea_of_galilee']
for spot in Spot_names:


    querystring = {"lat": Spots[spot][0],"lng": Spots[spot][1]}

    headers = {
        'x-rapidapi-host': "stormglass.p.rapidapi.com",
        'x-rapidapi-key': "898d16c808msh1226576a4196859p12b249jsnd3b06fc3e410"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    df = pd.DataFrame(data["hours"])
    df = df.drop(columns=["airTemperature", "cloudCover", "currentDirection", "currentSpeed", "humidity","precipitation", "pressure", "seaLevel", "swellDirection", "swellHeight", "swellPeriod", "waveDirection", "waveHeight", "wavePeriod", "windWavePeriod", "windWaveHeight", "windWaveDirection", "waterTemperature", "visibility"])
    df = df.rename(columns={'time':'Date', 'windSpeed':'Speed', 'gust':'Gust', 'windDirection':'Direction'})
    print(df['Gust'][3][1]['value'])