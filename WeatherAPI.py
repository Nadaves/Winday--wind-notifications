import requests

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q":"32.38,34.86","days":"2"}

headers = {
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
    'x-rapidapi-key': "898d16c808msh1226576a4196859p12b249jsnd3b06fc3e410"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)