import requests

url = "https://stormglass.p.rapidapi.com/forecast"

querystring = {"lat":"32.38","lng":"34.86"}

headers = {
    'x-rapidapi-host': "stormglass.p.rapidapi.com",
    'x-rapidapi-key': "898d16c808msh1226576a4196859p12b249jsnd3b06fc3e410"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)