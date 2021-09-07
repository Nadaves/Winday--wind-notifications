from numpy import datetime64
import requests
import pandas as pd
import json
from urllib.request import urlopen
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
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
    with urlopen("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&exclude=current,minutely,hourly,alerts&appid="+ApiKey) as response:
        source = response.read()

    #Turn json code into python object
    data = json.loads(source)

    #create a dataframe and drop irrelevant columns
    df = pd.DataFrame(data['daily'])
    df = df.drop(columns=["sunrise", "sunset", "moonrise", "moonset", "moon_phase","temp", "feels_like", "clouds", "pop", "uvi", "weather", "dew_point", "humidity", "pressure"])

    #convert kmh into knots
    df['wind_speed'] = 1.852 * df['wind_speed']
    df['wind_gust'] = 1.852 * df['wind_gust']
    df['dt'] = pd.to_datetime(df['dt'],unit='s')

    #edit columns and date format
    df = df.rename(columns={'dt':'Date', 'wind_speed':'Speed', 'wind_gust':'Gust', 'wind_deg':'Direction'})
    df["Date"] = df["Date"].dt.strftime("%d/%m/%y")
    df["Spot"] = spot

    #write to csv file
    # df.to_csv(spot + '.csv')

    #appending new data to DataFrame
    Spots_df.append(df)

Spots_df = pd.concat(Spots_df)
Spots_df = Spots_df.drop(columns=['rain'])

Eilat = Spots_df[(Spots_df['Spot'] == 'Eilat')]
Beit_Yanai = Spots_df[(Spots_df['Spot'] == 'Beit_Yanai')]
Sedot_Yam = Spots_df[(Spots_df['Spot'] == 'Sedot_Yam')]
Sea_of_galilee = Spots_df[(Spots_df['Spot'] == 'Sea_of_galilee')]

y1 = Eilat['Speed']
y2 = Beit_Yanai['Speed']
y3 = Sedot_Yam['Speed']
y4 = Sea_of_galilee['Speed']

x = Eilat['Date']

plt.plot(x, y1, label = 'Eilat')
plt.plot(x, y2, label = "Yanai")
plt.plot(x, y3, label = 'Caesarea')
plt.plot(x, y4, label = 'Kineret')
plt.legend()
plt.title('Wind Speed in Israeli Spots')
plt.savefig('Figure')
#another method of converting unix time into readable time and date
# for i in df['dt']:
#     dt = df['dt'][i]
#     df['dt'][i] = datetime.utcfromtimestampdf(dt).strftime('%Y-%m-%d %H:%M:%S')



