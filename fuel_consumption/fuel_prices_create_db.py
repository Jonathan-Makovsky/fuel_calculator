import requests
import pandas as pd

url_req_gasoline_95 = 'https://fuelcalc.energydmz.org/api/prices/getLatestPrice'

h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

response = requests.get(url=url_req_gasoline_95, headers=h)
gasoline_price = response.json()[2]['PriceValue']

data = {'gasoline': [gasoline_price]}
df = pd.DataFrame(data)
df.to_csv('fuel_prices_db.csv', index=False)
