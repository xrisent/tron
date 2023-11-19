import requests

TRC20_TOKEN = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'

def get_balance(address, api_key):
    url = f"https://api.trongrid.io/v1/accounts/{address}/"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }

    response = requests.get(url, headers=headers)

    data = response.json()['data']
    for trc20_dict in data[0]['trc20']:
        for key, value in trc20_dict.items():
            if key == TRC20_TOKEN:
                balance = value

    return balance