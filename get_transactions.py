import requests
from datetime import datetime


def get_transactions(address, api_key, params={}):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }

    response = requests.get(url, headers=headers, params=params)

    data = []

    for transaction in response.json()['data']:
        time = datetime.fromtimestamp(transaction['block_timestamp']/1000)
        data.append({
            'transaction_id': transaction['transaction_id'],
            'from': transaction['from'],
            'to': transaction['to'],
            'value': transaction['value'],
            'timestamp': transaction['block_timestamp'],
            'time': '%s'%time
        })
    
    return data