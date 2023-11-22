import httpx
from datetime import datetime

async def get_len(address, api_key):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }
    params = {'limit': 200}
    transactions_len = 0

    while True:
        response = httpx.get(url=url, headers=headers, params=params)
        transactions_len += len(response.json()['data'])
        fingerprint = response.json()['meta'].get('fingerprint')

        if fingerprint:
            params['fingerprint'] = fingerprint
        else:
            return transactions_len 
