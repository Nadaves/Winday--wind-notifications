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


#key for a spot format: [lat, lon, name]
Spots = { 
    'Beit_Yanai': ['32.38', '34.86'],
    'Sedot_Yam': ['32.49', '34.89'],
    'Eilat': ['29.52', '34.93'],
    'Sea_of_galilee': ['32.87', '35.63']
}

Spot_names = ['Beit_Yanai', 'Sedot_Yam', 'Eilat', 'Sea_of_galilee']

Spots_df = [] 


for spot in Spot_names:

    #variables
    ApiKey = "c8f08c8e937aef21399d0f8e4576b5af"
    lat = Spots[spot][0]
    lon = Spots[spot][1]
    
    #call openweather api
    with urlopen("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&exclude=current,minutely,daily,alerts&appid="+ApiKey) as response:
        source = response.read()

    #Turn json code into python object
    data = json.loads(source)

    #create a dataframe and drop irrelevant columns
    df = pd.DataFrame(data['hourly'])
    df = df.drop(columns=["temp", "feels_like", "pressure", "humidity", "dew_point","uvi", "visibility", "clouds", "pop", "uvi", "weather"])

    #convert kmh into knots
    df['wind_speed'] = 1.852 * df['wind_speed']
    df['wind_gust'] = 1.852 * df['wind_gust']
    df['dt'] = pd.to_datetime(df['dt'],unit='s')

    #edit columns and date format
    df = df.rename(columns={'dt':'Date', 'wind_speed':'Speed', 'wind_gust':'Gust', 'wind_deg':'Direction'})
    df["Date"] = df["Date"].dt.strftime("%d/%m/%y, %H:00")
    df["Spot"] = spot

    #write to csv file
    # df.to_csv(spot + '.csv')

    #appending new data to DataFrame
    Spots_df.append(df)

Spots_df = pd.concat(Spots_df)

Eilat = Spots_df[(Spots_df['Spot'] == 'Eilat')]
Beit_Yanai = Spots_df[(Spots_df['Spot'] == 'Beit_Yanai')]
Sedot_Yam = Spots_df[(Spots_df['Spot'] == 'Sedot_Yam')]
Sea_of_galilee = Spots_df[(Spots_df['Spot'] == 'Sea_of_galilee')]

plt.style.use('seaborn-poster')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)  

#Creating seperate plotted lines for each spot:

y1 = Eilat['Speed']
y2 = Beit_Yanai['Speed']
y3 = Sedot_Yam['Speed']
y4 = Sea_of_galilee['Speed']
y5 = Spots_df[(Spots_df["Speed"] > 16)]
y6 = y5['Speed']

x = Eilat['Date']

plt.plot(x, y1, label = 'Eilat')
plt.plot(x, y2, label = "Yanai")
plt.plot(x, y3, label = 'Caesarea')
plt.plot(x, y4, label = 'Kineret')
plt.legend()

#Creating the title and above 16Knots markers:
today = datetime.today()
d1 = today.strftime("%d/%m/%y, %H:00")
plt.title('Two-day Forecast, Generated: ' + d1)
plt.plot(y6, ls="", marker="*", color='gold', markersize=13)


#Change number of ticks for the X axis:
ax.xaxis.set_major_locator(mdates.HourLocator(interval=100))
plt.xticks(rotation='45')

# ax.set_facecolor((229/360,204/360,255/360))
# plt.grid(color=(191/360,0,255/360))

plt.tight_layout()
plt.show()

