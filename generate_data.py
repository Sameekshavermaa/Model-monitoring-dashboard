import requests
import numpy as np

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    try:
        res = requests.get(url).json()
        price = res["bitcoin"]["usd"]

        # simulate time series
        data = np.random.normal(price, price * 0.01, 100)
        return data

    except:
        return np.random.normal(0, 1, 100)